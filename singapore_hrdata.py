from __future__ import annotations

from io import BytesIO
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st


# =========================================================
# App configuration
# =========================================================
st.set_page_config(
    page_title="MUSTER | Attendance & Leave",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# Styling
# =========================================================
st.markdown(
    """
    <style>
        .stApp {
            background: #f4f6f9;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #dfe3ea;
        }

        .brand-title {
            font-size: 30px;
            font-weight: 900;
            letter-spacing: -1px;
            margin-bottom: 0;
            color: #202738;
        }

        .brand-subtitle {
            font-family: monospace;
            font-size: 13px;
            color: #8a93a5;
            margin-top: -4px;
            margin-bottom: 28px;
        }

        .page-title {
            font-size: 30px;
            font-weight: 800;
            color: #202738;
            margin-bottom: 12px;
        }

        .panel {
            background: #ffffff;
            border: 1px solid #d8dde6;
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 18px;
        }

        .section-label {
            font-family: monospace;
            font-size: 12px;
            letter-spacing: 1.6px;
            color: #8f98aa;
            margin-bottom: 14px;
        }

        .metric-card {
            background: #ffffff;
            border: 1px solid #d8dde6;
            border-radius: 12px;
            padding: 18px 18px 15px 18px;
            min-height: 112px;
        }

        .metric-label {
            font-size: 13px;
            color: #7f889a;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 30px;
            font-weight: 800;
            color: #202738;
        }

        .status-pill {
            display: inline-block;
            padding: 4px 9px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
        }

        div[data-testid="stFileUploader"] {
            background: #f4f6f9;
            border: 1px dashed #bcc5d1;
            border-radius: 12px;
            padding: 8px;
        }

        div[data-testid="stDataFrame"] {
            background: white;
            border-radius: 10px;
        }

        .small-note {
            color: #8992a3;
            font-size: 13px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Required column names
# =========================================================
ATTENDANCE_REQUIRED_COLUMNS = [
    "工號",
    "姓名",
    "考勤日期",
    "上段應上班時間",
    "上段實際上班時間",
    "下段實際下班時間",
]

SCHEDULE_COL = "上段應上班時間"
ACTUAL_START_COL = "上段實際上班時間"
ACTUAL_END_COL = "下段實際下班時間"


# =========================================================
# Session state
# =========================================================
def initialise_state() -> None:
    defaults = {
        "attendance_df": None,
        "leave_df": None,
        "processed_df": None,
        "attendance_filename": None,
        "leave_filename": None,
        "history": [],
        "last_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialise_state()


# =========================================================
# Utility functions
# =========================================================
def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.columns = (
        result.columns.astype(str)
        .str.strip()
        .str.replace("\n", "", regex=False)
        .str.replace("\r", "", regex=False)
    )
    return result


def normalise_employee_id(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.upper().replace({"NAN": ""})


def is_blank(value: object) -> bool:
    if pd.isna(value):
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"", "nan", "nat", "none", "null", "-", "--"}
    return False


def has_datetime(value: object) -> bool:
    """Return True when a cell contains a usable date/time value."""
    if is_blank(value):
        return False

    if isinstance(value, (pd.Timestamp, np.datetime64)):
        return not pd.isna(value)

    if isinstance(value, (int, float, np.integer, np.floating)):
        number = float(value)
        if number == 0:
            return False
        # Excel time fraction or Excel serial date.
        return 0 < number < 1 or number > 20000

    parsed = pd.to_datetime(str(value).strip(), errors="coerce")
    return not pd.isna(parsed)


def combine_date_and_time(date_value: object, time_value: object) -> pd.Timestamp:
    """Combine Excel date and time cells into one timestamp."""
    date_part = pd.to_datetime(date_value, errors="coerce")
    if pd.isna(date_part):
        return pd.NaT

    date_part = date_part.normalize()

    if pd.isna(time_value) or str(time_value).strip() == "":
        return date_part

    if isinstance(time_value, pd.Timestamp):
        return date_part + pd.Timedelta(
            hours=time_value.hour,
            minutes=time_value.minute,
            seconds=time_value.second,
        )

    if isinstance(time_value, (int, float, np.integer, np.floating)):
        number = float(time_value)
        if 0 <= number < 1:
            return date_part + pd.to_timedelta(number, unit="D")

    parsed_time = pd.to_datetime(str(time_value), errors="coerce")
    if pd.isna(parsed_time):
        return date_part

    return date_part + pd.Timedelta(
        hours=parsed_time.hour,
        minutes=parsed_time.minute,
        seconds=parsed_time.second,
    )


def detect_attendance_sheet(file_bytes: bytes) -> Tuple[str, pd.DataFrame]:
    excel = pd.ExcelFile(BytesIO(file_bytes))

    for sheet_name in excel.sheet_names:
        candidate = clean_columns(pd.read_excel(BytesIO(file_bytes), sheet_name=sheet_name))
        if all(column in candidate.columns for column in ATTENDANCE_REQUIRED_COLUMNS):
            return sheet_name, candidate

    raise ValueError(
        "No worksheet contains all required attendance columns: "
        + ", ".join(ATTENDANCE_REQUIRED_COLUMNS)
    )


def read_leave_workbook(file_bytes: bytes) -> pd.DataFrame:
    excel = pd.ExcelFile(BytesIO(file_bytes))
    frames: List[pd.DataFrame] = []

    for sheet_name in excel.sheet_names:
        sheet = clean_columns(pd.read_excel(BytesIO(file_bytes), sheet_name=sheet_name))
        lower_to_original = {str(column).lower(): column for column in sheet.columns}

        employee_column = lower_to_original.get("empid")
        start_date_column = lower_to_original.get("startdate")
        end_date_column = lower_to_original.get("enddate")

        if not employee_column or not start_date_column or not end_date_column:
            continue

        start_time_column = lower_to_original.get("starttime")
        end_time_column = lower_to_original.get("endtime")
        leave_type_column = lower_to_original.get("leavetype")
        employee_name_column = lower_to_original.get("empname")
        department_column = lower_to_original.get("departmentname")
        request_column = lower_to_original.get("reqno")

        normalised = pd.DataFrame()
        normalised["工號"] = normalise_employee_id(sheet[employee_column])
        normalised["姓名"] = sheet[employee_name_column] if employee_name_column else ""
        normalised["部門"] = sheet[department_column] if department_column else ""
        normalised["請假類型"] = (
            sheet[leave_type_column].astype(str)
            if leave_type_column
            else ("Annual Leave" if sheet_name.strip().upper() == "AL" else sheet_name)
        )
        normalised["申請編號"] = sheet[request_column] if request_column else ""
        normalised["來源工作表"] = sheet_name

        start_times = sheet[start_time_column] if start_time_column else pd.Series([None] * len(sheet))
        end_times = sheet[end_time_column] if end_time_column else pd.Series([None] * len(sheet))

        normalised["請假開始"] = [
            combine_date_and_time(date_value, time_value)
            for date_value, time_value in zip(sheet[start_date_column], start_times)
        ]
        normalised["請假結束"] = [
            combine_date_and_time(date_value, time_value)
            for date_value, time_value in zip(sheet[end_date_column], end_times)
        ]

        # When end date/time is missing or not after start, use end of that day.
        invalid_end = normalised["請假結束"].isna() | (
            normalised["請假結束"] <= normalised["請假開始"]
        )
        normalised.loc[invalid_end, "請假結束"] = (
            normalised.loc[invalid_end, "請假開始"].dt.normalize()
            + pd.Timedelta(days=1)
            - pd.Timedelta(seconds=1)
        )

        # Preserve approval fields when present.
        approval_columns = [
            column
            for column in sheet.columns
            if str(column).lower().startswith("isagree")
        ]
        if approval_columns:
            normalised["核准狀態"] = sheet[approval_columns].apply(
                lambda row: " / ".join(
                    [str(value) for value in row.tolist() if not pd.isna(value)]
                ),
                axis=1,
            )
        else:
            normalised["核准狀態"] = ""

        frames.append(normalised)

    if not frames:
        raise ValueError(
            "No valid leave worksheet was found. The workbook needs Empid, startdate and enddate columns."
        )

    result = pd.concat(frames, ignore_index=True)
    result = result[result["工號"] != ""].copy()
    return result


def classify_attendance(row: pd.Series) -> Tuple[str, str]:
    scheduled = has_datetime(row.get(SCHEDULE_COL))
    actual_start = has_datetime(row.get(ACTUAL_START_COL))
    actual_end = has_datetime(row.get(ACTUAL_END_COL))

    if not scheduled:
        return "No Schedule", "No scheduled start time"

    if not actual_start and not actual_end:
        return "Absent", "Scheduled, but both actual start and actual end are blank"

    if not actual_start and actual_end:
        return "Forgot Clock-in", "Actual end exists, but actual start is blank"

    if actual_start and not actual_end:
        return "Forgot Clock-out", "Actual start exists, but actual end is blank"

    return "Normal", "Both actual start and actual end are present"


def build_schedule_window(row: pd.Series) -> Tuple[pd.Timestamp, pd.Timestamp]:
    start = pd.to_datetime(row.get(SCHEDULE_COL), errors="coerce")

    possible_end_columns = [
        "下段應下班時間",
        "上段應下班時間",
        SCHEDULE_COL,
    ]
    end = pd.NaT
    for column in possible_end_columns:
        if column in row.index:
            candidate = pd.to_datetime(row.get(column), errors="coerce")
            if not pd.isna(candidate):
                end = candidate
                break

    if pd.isna(start):
        return pd.NaT, pd.NaT

    if pd.isna(end) or end <= start:
        end = start + pd.Timedelta(hours=12)

    return start, end


def find_overlapping_leave(
    employee_id: str,
    schedule_start: pd.Timestamp,
    schedule_end: pd.Timestamp,
    leave_df: Optional[pd.DataFrame],
) -> Optional[pd.Series]:
    if leave_df is None or leave_df.empty or pd.isna(schedule_start) or pd.isna(schedule_end):
        return None

    employee_leave = leave_df[leave_df["工號"] == employee_id]
    if employee_leave.empty:
        return None

    overlap = employee_leave[
        (employee_leave["請假開始"] < schedule_end)
        & (employee_leave["請假結束"] > schedule_start)
    ]

    if overlap.empty:
        return None

    return overlap.sort_values("請假開始").iloc[0]


def process_attendance(
    attendance_df: pd.DataFrame,
    leave_df: Optional[pd.DataFrame],
) -> pd.DataFrame:
    result = clean_columns(attendance_df)

    missing = [column for column in ATTENDANCE_REQUIRED_COLUMNS if column not in result.columns]
    if missing:
        raise ValueError("Missing attendance columns: " + ", ".join(missing))

    result["工號"] = normalise_employee_id(result["工號"])
    result["考勤日期"] = pd.to_datetime(result["考勤日期"], errors="coerce")

    classifications = result.apply(classify_attendance, axis=1)
    result["原始出勤判斷"] = classifications.apply(lambda value: value[0])
    result["判斷說明"] = classifications.apply(lambda value: value[1])

    final_statuses: List[str] = []
    leave_types: List[str] = []
    leave_starts: List[pd.Timestamp] = []
    leave_ends: List[pd.Timestamp] = []
    leave_requests: List[str] = []

    for _, row in result.iterrows():
        original_status = row["原始出勤判斷"]
        employee_id = row["工號"]
        schedule_start, schedule_end = build_schedule_window(row)
        overlapping_leave = find_overlapping_leave(
            employee_id,
            schedule_start,
            schedule_end,
            leave_df,
        )

        if overlapping_leave is not None and original_status in {
            "Absent",
            "Forgot Clock-in",
            "Forgot Clock-out",
        }:
            final_status = "On Leave"
            leave_type = str(overlapping_leave.get("請假類型", "Leave"))
            leave_start = overlapping_leave.get("請假開始", pd.NaT)
            leave_end = overlapping_leave.get("請假結束", pd.NaT)
            leave_request = str(overlapping_leave.get("申請編號", ""))
        else:
            final_status = original_status
            leave_type = ""
            leave_start = pd.NaT
            leave_end = pd.NaT
            leave_request = ""

        final_statuses.append(final_status)
        leave_types.append(leave_type)
        leave_starts.append(leave_start)
        leave_ends.append(leave_end)
        leave_requests.append(leave_request)

    result["最終出勤判斷"] = final_statuses
    result["請假類型"] = leave_types
    result["請假開始"] = leave_starts
    result["請假結束"] = leave_ends
    result["請假申請編號"] = leave_requests

    return result


def dataframe_to_excel(
    processed_df: pd.DataFrame,
    leave_df: Optional[pd.DataFrame],
) -> bytes:
    output = BytesIO()

    abnormal = processed_df[
        processed_df["最終出勤判斷"].isin(
            ["Absent", "Forgot Clock-in", "Forgot Clock-out"]
        )
    ].copy()

    summary = (
        processed_df["最終出勤判斷"]
        .value_counts(dropna=False)
        .rename_axis("Status")
        .reset_index(name="Count")
    )

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
        datetime_format="yyyy-mm-dd hh:mm:ss",
    ) as writer:
        processed_df.to_excel(writer, sheet_name="All Results", index=False)
        abnormal.to_excel(writer, sheet_name="Exceptions", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)
        if leave_df is not None:
            leave_df.to_excel(writer, sheet_name="Leave Data", index=False)

        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for column_cells in worksheet.columns:
                width = min(
                    max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                    + 2,
                    35,
                )
                worksheet.column_dimensions[column_cells[0].column_letter].width = max(width, 10)

    output.seek(0)
    return output.getvalue()


def get_week_label(processed_df: pd.DataFrame) -> str:
    dates = processed_df["考勤日期"].dropna()
    if dates.empty:
        return "Unknown period"
    start = dates.min().strftime("%d %b %Y")
    end = dates.max().strftime("%d %b %Y")
    return f"{start} – {end}"


def status_colour(status: str) -> str:
    return {
        "Absent": "background-color: #ffd6d6; color: #8b1e1e; font-weight: 700;",
        "Forgot Clock-in": "background-color: #fff0c2; color: #7a5300; font-weight: 700;",
        "Forgot Clock-out": "background-color: #fff0c2; color: #7a5300; font-weight: 700;",
        "On Leave": "background-color: #dfe8ff; color: #274f9b; font-weight: 700;",
        "Normal": "background-color: #dff2e4; color: #246b38; font-weight: 700;",
        "No Schedule": "background-color: #eceff4; color: #5d6575; font-weight: 700;",
    }.get(status, "")


def render_metric(label: str, value: int) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Sidebar
# =========================================================
with st.sidebar:
    st.markdown('<div class="brand-title">MUSTER</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-subtitle">attendance & leave, at a glance</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        ["Upload", "Attendance & Absenteeism", "Leave Data", "History"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Files are processed only in the current Streamlit session unless you add external storage.")


# =========================================================
# Upload page
# =========================================================
if page == "Upload":
    st.markdown('<div class="page-title">Upload</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">ADD THIS WEEK\'S FILES</div>', unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        attendance_file = st.file_uploader(
            "ATTENDANCE FILE",
            type=["xlsx", "xlsm"],
            key="attendance_upload",
            help="Upload the weekly attendance export.",
        )

    with right:
        leave_file = st.file_uploader(
            "LEAVE FILE",
            type=["xlsx", "xlsm"],
            key="leave_upload",
            help="Optional, but recommended. Upload the leave export containing AL and other leave sheets.",
        )

    process_clicked = st.button(
        "Process files",
        type="primary",
        disabled=attendance_file is None,
    )

    if process_clicked:
        try:
            attendance_bytes = attendance_file.getvalue()
            _, attendance_df = detect_attendance_sheet(attendance_bytes)

            leave_df = None
            if leave_file is not None:
                leave_df = read_leave_workbook(leave_file.getvalue())

            processed_df = process_attendance(attendance_df, leave_df)

            st.session_state.attendance_df = attendance_df
            st.session_state.leave_df = leave_df
            st.session_state.processed_df = processed_df
            st.session_state.attendance_filename = attendance_file.name
            st.session_state.leave_filename = leave_file.name if leave_file else None
            st.session_state.last_error = None

            week_label = get_week_label(processed_df)
            history_entry = {
                "week": week_label,
                "attendance_file": attendance_file.name,
                "leave_file": leave_file.name if leave_file else "Not uploaded",
                "rows": len(processed_df),
                "absent": int((processed_df["最終出勤判斷"] == "Absent").sum()),
                "forgot_punch": int(
                    processed_df["最終出勤判斷"]
                    .isin(["Forgot Clock-in", "Forgot Clock-out"])
                    .sum()
                ),
            }
            st.session_state.history = [
                entry for entry in st.session_state.history if entry["week"] != week_label
            ]
            st.session_state.history.insert(0, history_entry)

            st.success(f"Processed successfully: {week_label}")

        except Exception as exc:
            st.session_state.last_error = str(exc)
            st.error(f"Could not process the files: {exc}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">CURRENT SESSION</div>', unsafe_allow_html=True)

    if st.session_state.processed_df is None:
        st.info("No files processed yet. Upload the attendance file above to begin.")
    else:
        processed_df = st.session_state.processed_df
        week_label = get_week_label(processed_df)
        st.write(f"**Period:** {week_label}")
        st.write(f"**Attendance file:** {st.session_state.attendance_filename}")
        st.write(f"**Leave file:** {st.session_state.leave_filename or 'Not uploaded'}")
        st.write(f"**Rows processed:** {len(processed_df):,}")

        excel_bytes = dataframe_to_excel(processed_df, st.session_state.leave_df)
        st.download_button(
            "Download analysis Excel",
            data=excel_bytes,
            file_name="Attendance_Analysis_Result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# Attendance page
# =========================================================
elif page == "Attendance & Absenteeism":
    st.markdown('<div class="page-title">Attendance & Absenteeism</div>', unsafe_allow_html=True)

    processed_df = st.session_state.processed_df
    if processed_df is None:
        st.warning("Upload and process an attendance file first.")
        st.stop()

    status_counts = processed_df["最終出勤判斷"].value_counts()

    columns = st.columns(6)
    metrics = [
        ("Scheduled rows", int((processed_df["最終出勤判斷"] != "No Schedule").sum())),
        ("Absent", int(status_counts.get("Absent", 0))),
        ("Forgot clock-in", int(status_counts.get("Forgot Clock-in", 0))),
        ("Forgot clock-out", int(status_counts.get("Forgot Clock-out", 0))),
        ("On leave", int(status_counts.get("On Leave", 0))),
        ("Normal", int(status_counts.get("Normal", 0))),
    ]

    for column, (label, value) in zip(columns, metrics):
        with column:
            render_metric(label, value)

    st.markdown("### Filters")
    filter_cols = st.columns(4)

    with filter_cols[0]:
        status_options = sorted(processed_df["最終出勤判斷"].dropna().unique().tolist())
        selected_statuses = st.multiselect(
            "Status",
            status_options,
            default=[
                status
                for status in ["Absent", "Forgot Clock-in", "Forgot Clock-out"]
                if status in status_options
            ],
        )

    with filter_cols[1]:
        department_options = (
            sorted(processed_df["部門"].dropna().astype(str).unique().tolist())
            if "部門" in processed_df.columns
            else []
        )
        selected_departments = st.multiselect("Department", department_options)

    with filter_cols[2]:
        manager_options = (
            sorted(processed_df["Reporting To"].dropna().astype(str).unique().tolist())
            if "Reporting To" in processed_df.columns
            else []
        )
        selected_managers = st.multiselect("Reporting To", manager_options)

    with filter_cols[3]:
        search_text = st.text_input("Employee ID or name")

    filtered = processed_df.copy()

    if selected_statuses:
        filtered = filtered[filtered["最終出勤判斷"].isin(selected_statuses)]
    if selected_departments and "部門" in filtered.columns:
        filtered = filtered[filtered["部門"].astype(str).isin(selected_departments)]
    if selected_managers and "Reporting To" in filtered.columns:
        filtered = filtered[filtered["Reporting To"].astype(str).isin(selected_managers)]
    if search_text.strip():
        text = search_text.strip().lower()
        filtered = filtered[
            filtered["工號"].astype(str).str.lower().str.contains(text, na=False)
            | filtered["姓名"].astype(str).str.lower().str.contains(text, na=False)
        ]

    preferred_display_columns = [
        "工號",
        "姓名",
        "部門",
        "Pay Group",
        "考勤日期",
        "Reporting To",
        SCHEDULE_COL,
        ACTUAL_START_COL,
        ACTUAL_END_COL,
        "最終出勤判斷",
        "請假類型",
        "判斷說明",
    ]
    display_columns = [column for column in preferred_display_columns if column in filtered.columns]

    st.caption(f"Showing {len(filtered):,} records")
    styled = filtered[display_columns].style.map(status_colour, subset=["最終出勤判斷"])
    st.dataframe(styled, use_container_width=True, height=560)

    excel_bytes = dataframe_to_excel(filtered, st.session_state.leave_df)
    st.download_button(
        "Download filtered results",
        data=excel_bytes,
        file_name="Filtered_Attendance_Results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# =========================================================
# Leave page
# =========================================================
elif page == "Leave Data":
    st.markdown('<div class="page-title">Leave Data</div>', unsafe_allow_html=True)

    leave_df = st.session_state.leave_df
    if leave_df is None:
        st.warning("No leave file has been processed in this session.")
        st.stop()

    leave_type_counts = leave_df["請假類型"].fillna("Unknown").value_counts()
    metric_columns = st.columns(min(4, max(1, len(leave_type_counts))))
    for column, (leave_type, count) in zip(metric_columns, leave_type_counts.head(4).items()):
        with column:
            render_metric(str(leave_type), int(count))

    search_cols = st.columns(3)
    with search_cols[0]:
        leave_types = sorted(leave_df["請假類型"].dropna().astype(str).unique().tolist())
        selected_leave_types = st.multiselect("Leave type", leave_types)
    with search_cols[1]:
        leave_employee = st.text_input("Employee ID or name", key="leave_employee")
    with search_cols[2]:
        leave_sheet = st.multiselect(
            "Source sheet",
            sorted(leave_df["來源工作表"].dropna().astype(str).unique().tolist()),
        )

    filtered_leave = leave_df.copy()
    if selected_leave_types:
        filtered_leave = filtered_leave[
            filtered_leave["請假類型"].astype(str).isin(selected_leave_types)
        ]
    if leave_employee.strip():
        text = leave_employee.strip().lower()
        filtered_leave = filtered_leave[
            filtered_leave["工號"].astype(str).str.lower().str.contains(text, na=False)
            | filtered_leave["姓名"].astype(str).str.lower().str.contains(text, na=False)
        ]
    if leave_sheet:
        filtered_leave = filtered_leave[
            filtered_leave["來源工作表"].astype(str).isin(leave_sheet)
        ]

    st.caption(f"Showing {len(filtered_leave):,} leave records")
    st.dataframe(filtered_leave, use_container_width=True, height=580)


# =========================================================
# History page
# =========================================================
elif page == "History":
    st.markdown('<div class="page-title">History</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("No weeks saved in this browser session yet.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        history_df = history_df.rename(
            columns={
                "week": "Week",
                "attendance_file": "Attendance File",
                "leave_file": "Leave File",
                "rows": "Rows",
                "absent": "Absent",
                "forgot_punch": "Forgot Punch",
            }
        )
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        if st.button("Clear session history"):
            st.session_state.history = []
            st.rerun()
