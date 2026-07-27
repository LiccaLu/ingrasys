import io
import re
from datetime import datetime, time
from typing import Optional, Tuple

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Ingrasys Singapore HR Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLE
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --background: #f4f6f8;
        --card: #ffffff;
        --border: #d9dee7;
        --text: #202633;
        --muted: #7d8798;
        --navy: #243247;
        --accent: #b8791c;
        --accent-soft: #f5eee3;
        --danger: #b42318;
        --danger-soft: #fee4e2;
        --warning: #b54708;
        --warning-soft: #fef0c7;
        --success: #027a48;
        --success-soft: #d1fadf;
        --blue-soft: #eaf1fb;
    }

    html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: var(--text);
    }

    .stApp {
        background: var(--background);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.6rem;
    }

    .brand {
        padding: 0 0.5rem 1.5rem 0.5rem;
    }

    .brand-title {
        font-weight: 900;
        font-size: 1.65rem;
        letter-spacing: -0.04em;
        color: var(--navy);
        line-height: 1;
    }

    .brand-subtitle {
        margin-top: 0.45rem;
        color: #8c96a7;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 0.79rem;
        line-height: 1.45;
    }

    .page-title {
        font-size: 2rem;
        font-weight: 850;
        letter-spacing: -0.04em;
        color: var(--navy);
        margin-bottom: 0.25rem;
    }

    .page-subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        margin-bottom: 1.3rem;
    }

    .section-label {
        color: #8c96a7;
        font-size: 0.75rem;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 1.3rem 1.45rem;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
        margin-bottom: 1rem;
    }

    .upload-card {
        border: 1px dashed #b9c1cd;
        border-radius: 13px;
        padding: 1.4rem 1.2rem;
        background: #fafbfc;
        text-align: center;
    }

    .upload-title {
        font-weight: 800;
        color: var(--navy);
        font-size: 1.05rem;
        margin-bottom: 0.2rem;
    }

    .upload-help {
        color: var(--muted);
        font-size: 0.85rem;
    }

    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        min-height: 112px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }

    .metric-value {
        color: var(--navy);
        font-size: 2rem;
        font-weight: 850;
        margin-top: 0.4rem;
        line-height: 1;
    }

    .metric-note {
        color: var(--muted);
        font-size: 0.78rem;
        margin-top: 0.45rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.22rem 0.58rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 750;
    }

    div[data-testid="stFileUploader"] section {
        background: #fafbfc;
        border: 1px dashed #b9c1cd;
        border-radius: 12px;
        padding: 1.2rem;
    }

    div[data-testid="stFileUploader"] section > div {
        text-align: center;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 750;
        padding: 0.55rem 1rem;
        border: 1px solid #9ba3af;
    }

    .stButton > button[kind="primary"] {
        background: var(--navy);
        border-color: var(--navy);
        color: white;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    .info-box {
        background: var(--blue-soft);
        border: 1px solid #c9d8ef;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        color: #344054;
        font-size: 0.88rem;
    }

    .empty-state {
        min-height: 230px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--muted);
        text-align: center;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONSTANTS
# ============================================================
ATTENDANCE_COLUMNS = {
    "employee_id": "工號",
    "employee_name": "姓名",
    "department": "部門",
    "pay_group": "Pay Group",
    "attendance_date": "考勤日期",
    "scheduled_start": "上段應上班時間",
    "actual_start": "上段實際上班時間",
    "scheduled_end": "下段應下班時間",
    "actual_end": "下段實際下班時間",
    "reporting_to": "Reporting To",
}

STATUS_ORDER = [
    "Absent",
    "On Leave",
    "Forgot Clock-in",
    "Forgot Clock-out",
    "Normal",
    "No Schedule",
]

ABNORMAL_STATUSES = ["Absent", "Forgot Clock-in", "Forgot Clock-out"]


# ============================================================
# SESSION STATE
# ============================================================
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None

if "leave_data" not in st.session_state:
    st.session_state.leave_data = None

if "history" not in st.session_state:
    st.session_state.history = []

if "current_file_names" not in st.session_state:
    st.session_state.current_file_names = {}


# ============================================================
# HELPERS
# ============================================================
def normalize_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def clean_employee_id(value) -> str:
    text = normalize_text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return text.upper()


def value_exists(value) -> bool:
    if pd.isna(value):
        return False

    if isinstance(value, str):
        return value.strip().lower() not in {"", "nan", "nat", "none", "null", "-", "--", "0"}

    if isinstance(value, (int, float)):
        return value != 0

    return True


def parse_date(value) -> pd.Timestamp:
    return pd.to_datetime(value, errors="coerce").normalize()


def parse_hhmm(value) -> Optional[time]:
    if pd.isna(value):
        return None

    if isinstance(value, time):
        return value

    if isinstance(value, pd.Timestamp):
        return value.time()

    if isinstance(value, datetime):
        return value.time()

    if isinstance(value, (int, float)):
        if pd.isna(value):
            return None

        numeric = int(value)

        # Excel time fraction
        if 0 < float(value) < 1:
            total_seconds = round(float(value) * 86400)
            hour = (total_seconds // 3600) % 24
            minute = (total_seconds % 3600) // 60
            return time(hour, minute)

        # HHMM number such as 700, 1900, 100
        text = str(numeric).zfill(4)
    else:
        text = str(value).strip()

        if re.match(r"^\d{1,4}(\.0)?$", text):
            text = text.split(".")[0].zfill(4)
        else:
            parsed = pd.to_datetime(text, errors="coerce")
            if not pd.isna(parsed):
                return parsed.time()
            return None

    try:
        hour = int(text[:-2])
        minute = int(text[-2:])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return time(hour, minute)
    except (TypeError, ValueError):
        pass

    return None


def combine_date_time(date_value, time_value) -> pd.Timestamp:
    date_part = pd.to_datetime(date_value, errors="coerce")
    time_part = parse_hhmm(time_value)

    if pd.isna(date_part) or time_part is None:
        return pd.NaT

    return pd.Timestamp.combine(date_part.date(), time_part)


def find_attendance_sheet(file_bytes: bytes) -> Tuple[str, pd.DataFrame]:
    excel = pd.ExcelFile(io.BytesIO(file_bytes))

    for sheet in excel.sheet_names:
        sample = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet, nrows=5)
        sample.columns = [str(col).strip() for col in sample.columns]

        required = {
            ATTENDANCE_COLUMNS["employee_id"],
            ATTENDANCE_COLUMNS["scheduled_start"],
            ATTENDANCE_COLUMNS["actual_start"],
            ATTENDANCE_COLUMNS["actual_end"],
        }

        if required.issubset(set(sample.columns)):
            full_df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet)
            full_df.columns = [str(col).strip() for col in full_df.columns]
            return sheet, full_df

    raise ValueError(
        "No attendance worksheet was found. The file must contain 工號, "
        "上段應上班時間, 上段實際上班時間 and 下段實際下班時間."
    )


def standardize_leave_sheet(df: pd.DataFrame, source_sheet: str) -> pd.DataFrame:
    original_columns = {str(col).strip(): col for col in df.columns}
    lowered = {str(col).strip().lower(): col for col in df.columns}

    def get_column(*names):
        for name in names:
            if name in original_columns:
                return original_columns[name]
            if name.lower() in lowered:
                return lowered[name.lower()]
        return None

    employee_id_col = get_column("empid", "Empid", "工號")
    employee_name_col = get_column("empname", "姓名")
    department_col = get_column("departmentname", "部門")
    leave_type_col = get_column("leavetype", "Leave Type")
    start_date_col = get_column("startdate")
    start_time_col = get_column("starttime")
    end_date_col = get_column("enddate")
    end_time_col = get_column("endtime")
    reason_col = get_column("reason")
    request_no_col = get_column("reqno")

    if employee_id_col is None or start_date_col is None or end_date_col is None:
        return pd.DataFrame()

    result = pd.DataFrame()
    result["Employee ID"] = df[employee_id_col].map(clean_employee_id)
    result["Employee Name"] = (
        df[employee_name_col].map(normalize_text)
        if employee_name_col is not None else ""
    )
    result["Department"] = (
        df[department_col].map(normalize_text)
        if department_col is not None else ""
    )
    result["Leave Type"] = (
        df[leave_type_col].map(normalize_text)
        if leave_type_col is not None else source_sheet
    )
    result["Leave Type"] = result["Leave Type"].replace("", source_sheet)
    result["Reason"] = (
        df[reason_col].map(normalize_text)
        if reason_col is not None else ""
    )
    result["Request No."] = (
        df[request_no_col].map(normalize_text)
        if request_no_col is not None else ""
    )
    result["Source Sheet"] = source_sheet

    result["Leave Start"] = [
        combine_date_time(date_value, time_value)
        for date_value, time_value in zip(
            df[start_date_col],
            df[start_time_col] if start_time_col is not None else [None] * len(df),
        )
    ]

    result["Leave End"] = [
        combine_date_time(date_value, time_value)
        for date_value, time_value in zip(
            df[end_date_col],
            df[end_time_col] if end_time_col is not None else [None] * len(df),
        )
    ]

    # When time is absent, treat the leave as a full-day period.
    start_dates = pd.to_datetime(df[start_date_col], errors="coerce")
    end_dates = pd.to_datetime(df[end_date_col], errors="coerce")

    missing_start_time = result["Leave Start"].isna() & start_dates.notna()
    missing_end_time = result["Leave End"].isna() & end_dates.notna()

    result.loc[missing_start_time, "Leave Start"] = start_dates[missing_start_time].dt.normalize()
    result.loc[missing_end_time, "Leave End"] = (
        end_dates[missing_end_time].dt.normalize() + pd.Timedelta(days=1)
    )

    result = result[
        result["Employee ID"].ne("")
        & result["Leave Start"].notna()
        & result["Leave End"].notna()
    ].copy()

    return result


def read_leave_file(file_bytes: bytes) -> pd.DataFrame:
    excel = pd.ExcelFile(io.BytesIO(file_bytes))
    frames = []

    for sheet in excel.sheet_names:
        df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet)
        df.columns = [str(col).strip() for col in df.columns]
        standardized = standardize_leave_sheet(df, sheet)

        if not standardized.empty:
            frames.append(standardized)

    if not frames:
        return pd.DataFrame(
            columns=[
                "Employee ID", "Employee Name", "Department", "Leave Type",
                "Reason", "Request No.", "Source Sheet", "Leave Start", "Leave End"
            ]
        )

    return pd.concat(frames, ignore_index=True)


def create_attendance_shift(row: pd.Series) -> Tuple[pd.Timestamp, pd.Timestamp]:
    scheduled_start = pd.to_datetime(
        row.get(ATTENDANCE_COLUMNS["scheduled_start"]), errors="coerce"
    )

    scheduled_end = pd.to_datetime(
        row.get(ATTENDANCE_COLUMNS["scheduled_end"]), errors="coerce"
    )

    # Fallback: if 下段應下班時間 does not exist, use 上段應下班時間.
    if pd.isna(scheduled_end):
        scheduled_end = pd.to_datetime(
            row.get("上段應下班時間"), errors="coerce"
        )

    # Final fallback: use attendance date + 24 hours.
    if pd.isna(scheduled_end) and not pd.isna(scheduled_start):
        scheduled_end = scheduled_start + pd.Timedelta(hours=24)

    if (
        not pd.isna(scheduled_start)
        and not pd.isna(scheduled_end)
        and scheduled_end <= scheduled_start
    ):
        scheduled_end += pd.Timedelta(days=1)

    return scheduled_start, scheduled_end


def match_leave(
    employee_id: str,
    shift_start: pd.Timestamp,
    shift_end: pd.Timestamp,
    leave_df: pd.DataFrame,
) -> Optional[pd.Series]:
    if leave_df.empty or not employee_id or pd.isna(shift_start) or pd.isna(shift_end):
        return None

    matches = leave_df[
        (leave_df["Employee ID"] == employee_id)
        & (leave_df["Leave Start"] < shift_end)
        & (leave_df["Leave End"] > shift_start)
    ]

    if matches.empty:
        return None

    return matches.sort_values("Leave Start").iloc[0]


def process_attendance(attendance_df: pd.DataFrame, leave_df: pd.DataFrame) -> pd.DataFrame:
    required_columns = [
        ATTENDANCE_COLUMNS["employee_id"],
        ATTENDANCE_COLUMNS["scheduled_start"],
        ATTENDANCE_COLUMNS["actual_start"],
        ATTENDANCE_COLUMNS["actual_end"],
    ]

    missing = [col for col in required_columns if col not in attendance_df.columns]
    if missing:
        raise ValueError("Missing attendance columns: " + ", ".join(missing))

    result = attendance_df.copy()
    result["Employee ID Clean"] = result[
        ATTENDANCE_COLUMNS["employee_id"]
    ].map(clean_employee_id)

    statuses = []
    leave_types = []
    leave_reasons = []
    leave_starts = []
    leave_ends = []
    shift_starts = []
    shift_ends = []

    for _, row in result.iterrows():
        scheduled_exists = value_exists(row.get(ATTENDANCE_COLUMNS["scheduled_start"]))
        actual_start_exists = value_exists(row.get(ATTENDANCE_COLUMNS["actual_start"]))
        actual_end_exists = value_exists(row.get(ATTENDANCE_COLUMNS["actual_end"]))

        shift_start, shift_end = create_attendance_shift(row)
        shift_starts.append(shift_start)
        shift_ends.append(shift_end)

        leave_match = match_leave(
            row["Employee ID Clean"],
            shift_start,
            shift_end,
            leave_df,
        )

        leave_type = ""
        leave_reason = ""
        leave_start = pd.NaT
        leave_end = pd.NaT

        if leave_match is not None:
            leave_type = leave_match["Leave Type"]
            leave_reason = leave_match["Reason"]
            leave_start = leave_match["Leave Start"]
            leave_end = leave_match["Leave End"]

        # Exact user rule:
        # Scheduled start exists + both actual start and actual end missing = absent,
        # unless a corresponding leave period overlaps the employee's shift.
        if not scheduled_exists:
            status = "No Schedule"
        elif not actual_start_exists and not actual_end_exists:
            status = "On Leave" if leave_match is not None else "Absent"
        elif not actual_start_exists and actual_end_exists:
            status = "Forgot Clock-in"
        elif actual_start_exists and not actual_end_exists:
            status = "Forgot Clock-out"
        else:
            status = "Normal"

        statuses.append(status)
        leave_types.append(leave_type)
        leave_reasons.append(leave_reason)
        leave_starts.append(leave_start)
        leave_ends.append(leave_end)

    result["Shift Start"] = shift_starts
    result["Shift End"] = shift_ends
    result["Attendance Status"] = statuses
    result["Matched Leave Type"] = leave_types
    result["Matched Leave Start"] = leave_starts
    result["Matched Leave End"] = leave_ends
    result["Leave Reason"] = leave_reasons

    return result


def calculate_week_label(df: pd.DataFrame) -> str:
    date_col = ATTENDANCE_COLUMNS["attendance_date"]

    if date_col in df.columns:
        dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
    else:
        dates = pd.to_datetime(df["Shift Start"], errors="coerce").dropna()

    if dates.empty:
        return datetime.now().strftime("%d %b %Y")

    return f"{dates.min():%d %b %Y} – {dates.max():%d %b %Y}"


def build_excel_download(
    processed_df: pd.DataFrame,
    leave_df: pd.DataFrame,
) -> bytes:
    output = io.BytesIO()

    summary = (
        processed_df["Attendance Status"]
        .value_counts()
        .reindex(STATUS_ORDER, fill_value=0)
        .rename_axis("Status")
        .reset_index(name="Records")
    )

    with pd.ExcelWriter(output, engine="openpyxl", datetime_format="yyyy-mm-dd hh:mm:ss") as writer:
        processed_df.to_excel(writer, sheet_name="Attendance Analysis", index=False)
        processed_df[
            processed_df["Attendance Status"].isin(ABNORMAL_STATUSES)
        ].to_excel(writer, sheet_name="Exceptions", index=False)
        processed_df[
            processed_df["Attendance Status"] == "Absent"
        ].to_excel(writer, sheet_name="Absentees", index=False)
        leave_df.to_excel(writer, sheet_name="Leave Data", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    return output.getvalue()


def display_metric(label: str, value: int, note: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value:,}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_filters(df: pd.DataFrame, key_prefix: str) -> pd.DataFrame:
    filtered = df.copy()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        status_options = sorted(filtered["Attendance Status"].dropna().unique())
        selected_statuses = st.multiselect(
            "Status",
            status_options,
            default=status_options,
            key=f"{key_prefix}_status",
        )

    department_col = ATTENDANCE_COLUMNS["department"]
    with c2:
        if department_col in filtered.columns:
            department_options = sorted(
                filtered[department_col].dropna().astype(str).unique()
            )
            selected_departments = st.multiselect(
                "Department",
                department_options,
                default=[],
                key=f"{key_prefix}_department",
            )
        else:
            selected_departments = []

    manager_col = ATTENDANCE_COLUMNS["reporting_to"]
    with c3:
        if manager_col in filtered.columns:
            manager_options = sorted(
                filtered[manager_col].dropna().astype(str).unique()
            )
            selected_managers = st.multiselect(
                "Reporting To",
                manager_options,
                default=[],
                key=f"{key_prefix}_manager",
            )
        else:
            selected_managers = []

    with c4:
        search_text = st.text_input(
            "Employee search",
            placeholder="ID or employee name",
            key=f"{key_prefix}_search",
        ).strip()

    if selected_statuses:
        filtered = filtered[filtered["Attendance Status"].isin(selected_statuses)]

    if selected_departments and department_col in filtered.columns:
        filtered = filtered[filtered[department_col].astype(str).isin(selected_departments)]

    if selected_managers and manager_col in filtered.columns:
        filtered = filtered[filtered[manager_col].astype(str).isin(selected_managers)]

    if search_text:
        employee_id_col = ATTENDANCE_COLUMNS["employee_id"]
        employee_name_col = ATTENDANCE_COLUMNS["employee_name"]

        id_match = (
            filtered[employee_id_col].astype(str).str.contains(
                search_text, case=False, na=False
            )
            if employee_id_col in filtered.columns else False
        )
        name_match = (
            filtered[employee_name_col].astype(str).str.contains(
                search_text, case=False, na=False
            )
            if employee_name_col in filtered.columns else False
        )

        filtered = filtered[id_match | name_match]

    return filtered


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-title">INGRASYS HR</div>
        <div class="brand-subtitle">Singapore attendance<br>and leave analysis</div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Upload",
        "Attendance & Absenteeism",
        "Dashboard",
        "History",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
if st.session_state.processed_data is not None:
    current_week = calculate_week_label(st.session_state.processed_data)
    st.sidebar.caption("Current processed period")
    st.sidebar.markdown(f"**{current_week}**")
else:
    st.sidebar.caption("Upload attendance and leave files to begin.")


# ============================================================
# PAGE 1 — UPLOAD
# ============================================================
if page == "Upload":
    st.markdown('<div class="page-title">Upload</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Add the weekly attendance and leave exports for Ingrasys Singapore.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Add this week’s files</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="upload-card">
                <div class="upload-title">ATTENDANCE FILE</div>
                <div class="upload-help">Excel export containing scheduled and actual punch times</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        attendance_file = st.file_uploader(
            "Attendance file",
            type=["xlsx", "xls"],
            label_visibility="collapsed",
            key="attendance_upload",
        )

    with col2:
        st.markdown(
            """
            <div class="upload-card">
                <div class="upload-title">LEAVE FILE</div>
                <div class="upload-help">Excel export containing Annual Leave and Other Leave sheets</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        leave_file = st.file_uploader(
            "Leave file",
            type=["xlsx", "xls"],
            label_visibility="collapsed",
            key="leave_upload",
        )

    st.markdown(
        """
        <div class="info-box">
        An employee is marked <b>Absent</b> when a scheduled start exists and both
        the actual start and actual end are blank. When an overlapping leave record
        exists for the same employee, the record becomes <b>On Leave</b> instead.
        </div>
        """,
        unsafe_allow_html=True,
    )

    process_clicked = st.button(
        "Process files",
        type="primary",
        disabled=attendance_file is None or leave_file is None,
    )

    if process_clicked:
        try:
            with st.spinner("Reading and matching attendance with leave records..."):
                attendance_bytes = attendance_file.getvalue()
                leave_bytes = leave_file.getvalue()

                attendance_sheet, attendance_df = find_attendance_sheet(attendance_bytes)
                leave_df = read_leave_file(leave_bytes)
                processed_df = process_attendance(attendance_df, leave_df)

                week_label = calculate_week_label(processed_df)

                st.session_state.processed_data = processed_df
                st.session_state.leave_data = leave_df
                st.session_state.current_file_names = {
                    "attendance": attendance_file.name,
                    "leave": leave_file.name,
                    "attendance_sheet": attendance_sheet,
                }

                history_entry = {
                    "processed_at": datetime.now(),
                    "week": week_label,
                    "attendance_file": attendance_file.name,
                    "leave_file": leave_file.name,
                    "rows": len(processed_df),
                    "absent": int((processed_df["Attendance Status"] == "Absent").sum()),
                    "on_leave": int((processed_df["Attendance Status"] == "On Leave").sum()),
                    "forgot_punch": int(
                        processed_df["Attendance Status"].isin(
                            ["Forgot Clock-in", "Forgot Clock-out"]
                        ).sum()
                    ),
                    "data": processed_df.copy(),
                    "leave_data": leave_df.copy(),
                }

                # Replace the current week's entry if processed again.
                st.session_state.history = [
                    item for item in st.session_state.history
                    if item["week"] != week_label
                ]
                st.session_state.history.insert(0, history_entry)

            st.success(
                f"Files processed successfully for {week_label}. "
                f"{len(processed_df):,} attendance records were analysed."
            )

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                display_metric(
                    "Attendance rows",
                    len(processed_df),
                    f"Sheet: {attendance_sheet}",
                )
            with c2:
                display_metric(
                    "Absent",
                    int((processed_df["Attendance Status"] == "Absent").sum()),
                    "No punch and no matching leave",
                )
            with c3:
                display_metric(
                    "On leave",
                    int((processed_df["Attendance Status"] == "On Leave").sum()),
                    "Matched by employee and time",
                )
            with c4:
                display_metric(
                    "Forgot punch",
                    int(
                        processed_df["Attendance Status"].isin(
                            ["Forgot Clock-in", "Forgot Clock-out"]
                        ).sum()
                    ),
                    "Only one punch is present",
                )

        except Exception as exc:
            st.error(f"Could not process the files: {exc}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Saved weeks</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            """
            <div class="empty-state">
                <div>
                    <b>No weeks processed yet.</b><br>
                    Add the first pair of files above.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        history_preview = pd.DataFrame(
            [
                {
                    "Week": item["week"],
                    "Processed": item["processed_at"].strftime("%Y-%m-%d %H:%M"),
                    "Rows": item["rows"],
                    "Absent": item["absent"],
                    "On Leave": item["on_leave"],
                    "Forgot Punch": item["forgot_punch"],
                }
                for item in st.session_state.history
            ]
        )
        st.dataframe(history_preview, use_container_width=True, hide_index=True)

    st.caption(
        "History is stored only in the current Streamlit session. "
        "For permanent company-wide history, connect the app to a database."
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE 2 — ATTENDANCE & ABSENTEEISM
# ============================================================
elif page == "Attendance & Absenteeism":
    st.markdown(
        '<div class="page-title">Attendance & Absenteeism</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Combined attendance and leave results with exception-focused filtering.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.processed_data is None:
        st.warning("Upload and process the attendance and leave files first.")
        st.stop()

    processed_df = st.session_state.processed_data
    filtered_df = apply_filters(processed_df, "attendance")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        display_metric(
            "Absent",
            int((filtered_df["Attendance Status"] == "Absent").sum()),
            "No matching leave",
        )
    with c2:
        display_metric(
            "On Leave",
            int((filtered_df["Attendance Status"] == "On Leave").sum()),
            "Excused absence",
        )
    with c3:
        display_metric(
            "Forgot Clock-in",
            int((filtered_df["Attendance Status"] == "Forgot Clock-in").sum()),
            "End punch only",
        )
    with c4:
        display_metric(
            "Forgot Clock-out",
            int((filtered_df["Attendance Status"] == "Forgot Clock-out").sum()),
            "Start punch only",
        )

    display_columns = [
        ATTENDANCE_COLUMNS["employee_id"],
        ATTENDANCE_COLUMNS["employee_name"],
        ATTENDANCE_COLUMNS["department"],
        ATTENDANCE_COLUMNS["attendance_date"],
        ATTENDANCE_COLUMNS["scheduled_start"],
        ATTENDANCE_COLUMNS["actual_start"],
        ATTENDANCE_COLUMNS["actual_end"],
        "Attendance Status",
        "Matched Leave Type",
        "Matched Leave Start",
        "Matched Leave End",
        "Leave Reason",
        ATTENDANCE_COLUMNS["reporting_to"],
    ]
    display_columns = [col for col in display_columns if col in filtered_df.columns]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-label">Attendance records · {len(filtered_df):,} results</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True,
        height=540,
        column_config={
            "Attendance Status": st.column_config.TextColumn("Status"),
            "Matched Leave Type": st.column_config.TextColumn("Leave Type"),
            "Leave Reason": st.column_config.TextColumn("Leave Reason", width="large"),
        },
    )

    excel_bytes = build_excel_download(
        st.session_state.processed_data,
        st.session_state.leave_data,
    )
    st.download_button(
        "Download analysis Excel",
        data=excel_bytes,
        file_name="Ingrasys_HR_Attendance_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE 3 — DASHBOARD
# ============================================================
elif page == "Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Weekly overview of attendance, absence, leave and missed punches.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.processed_data is None:
        st.warning("Upload and process the attendance and leave files first.")
        st.stop()

    processed_df = st.session_state.processed_data.copy()

    total = len(processed_df)
    absent = int((processed_df["Attendance Status"] == "Absent").sum())
    on_leave = int((processed_df["Attendance Status"] == "On Leave").sum())
    forgot_punch = int(
        processed_df["Attendance Status"].isin(
            ["Forgot Clock-in", "Forgot Clock-out"]
        ).sum()
    )
    normal = int((processed_df["Attendance Status"] == "Normal").sum())

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        display_metric("Total records", total, calculate_week_label(processed_df))
    with c2:
        display_metric("Absent", absent, "Requires HR review")
    with c3:
        display_metric("On Leave", on_leave, "Excused by leave")
    with c4:
        display_metric("Forgot punch", forgot_punch, "Incomplete punch")
    with c5:
        display_metric("Normal", normal, "Complete punches")

    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Status distribution</div>', unsafe_allow_html=True)

        status_counts = (
            processed_df["Attendance Status"]
            .value_counts()
            .reindex(STATUS_ORDER, fill_value=0)
        )
        st.bar_chart(status_counts)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Absence by department</div>', unsafe_allow_html=True)

        department_col = ATTENDANCE_COLUMNS["department"]
        absence_by_department = (
            processed_df[processed_df["Attendance Status"] == "Absent"]
            .groupby(department_col, dropna=False)
            .size()
            .sort_values(ascending=False)
            .head(12)
        )

        if absence_by_department.empty:
            st.info("No unexcused absence records were found.")
        else:
            st.bar_chart(absence_by_department)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Daily attendance trend</div>', unsafe_allow_html=True)

    date_col = ATTENDANCE_COLUMNS["attendance_date"]
    daily = processed_df.copy()
    daily["_date"] = pd.to_datetime(daily[date_col], errors="coerce").dt.date

    daily_summary = (
        daily.groupby(["_date", "Attendance Status"])
        .size()
        .unstack(fill_value=0)
    )

    trend_columns = [
        col for col in ["Absent", "On Leave", "Forgot Clock-in", "Forgot Clock-out"]
        if col in daily_summary.columns
    ]

    if trend_columns:
        st.line_chart(daily_summary[trend_columns])
    else:
        st.info("No daily exception data is available.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Employees requiring attention</div>', unsafe_allow_html=True)

    attention = processed_df[
        processed_df["Attendance Status"].isin(ABNORMAL_STATUSES)
    ].copy()

    employee_id_col = ATTENDANCE_COLUMNS["employee_id"]
    employee_name_col = ATTENDANCE_COLUMNS["employee_name"]

    if attention.empty:
        st.info("No absence or incomplete-punch records were found.")
    else:
        attention_summary = (
            attention.groupby(
                [employee_id_col, employee_name_col, "Attendance Status"],
                dropna=False,
            )
            .size()
            .reset_index(name="Records")
            .sort_values("Records", ascending=False)
        )
        st.dataframe(
            attention_summary,
            use_container_width=True,
            hide_index=True,
            height=360,
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE 4 — HISTORY
# ============================================================
elif page == "History":
    st.markdown('<div class="page-title">History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Review weekly files processed during the current session.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.history:
        st.markdown(
            """
            <div class="card">
                <div class="empty-state">
                    <div>
                        <b>No history yet.</b><br>
                        Process a weekly attendance and leave pair first.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    history_table = pd.DataFrame(
        [
            {
                "Week": item["week"],
                "Processed At": item["processed_at"].strftime("%Y-%m-%d %H:%M"),
                "Attendance File": item["attendance_file"],
                "Leave File": item["leave_file"],
                "Rows": item["rows"],
                "Absent": item["absent"],
                "On Leave": item["on_leave"],
                "Forgot Punch": item["forgot_punch"],
            }
            for item in st.session_state.history
        ]
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Processed weeks</div>', unsafe_allow_html=True)
    st.dataframe(history_table, use_container_width=True, hide_index=True)

    selected_week = st.selectbox(
        "Open a saved week",
        [item["week"] for item in st.session_state.history],
    )

    selected_item = next(
        item for item in st.session_state.history
        if item["week"] == selected_week
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        display_metric("Rows", selected_item["rows"], selected_week)
    with c2:
        display_metric("Absent", selected_item["absent"], "Unexcused")
    with c3:
        display_metric("On Leave", selected_item["on_leave"], "Leave overlap")
    with c4:
        display_metric("Forgot Punch", selected_item["forgot_punch"], "Incomplete punch")

    history_excel = build_excel_download(
        selected_item["data"],
        selected_item["leave_data"],
    )
    st.download_button(
        f"Download {selected_week}",
        data=history_excel,
        file_name=f"Ingrasys_HR_{selected_week.replace(' ', '_').replace('–', '-')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.caption(
        "This version keeps history in browser-session memory only. "
        "Restarting or redeploying the app clears it."
    )
