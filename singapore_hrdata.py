import io
from datetime import datetime
from typing import Optional

import pandas as pd
import plotly.express as px
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
# STYLING — LARGE BOOKMARK NAVIGATION
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --navy: #243247;
        --gold: #b47a26;
        --bg: #f4f6f9;
        --card: #ffffff;
        --border: #dfe4ec;
        --muted: #758196;
        --danger: #b42318;
    }

    .stApp {
        background: var(--bg);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
        min-width: 295px;
        max-width: 295px;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }

    .brand {
        padding: 0.5rem 0.5rem 1.3rem;
    }

    .brand-name {
        font-size: 1.6rem;
        font-weight: 900;
        color: var(--navy);
        letter-spacing: -0.04em;
    }

    .brand-subtitle {
        color: var(--muted);
        margin-top: 0.35rem;
        font-size: 0.82rem;
        line-height: 1.45;
    }

    /* Make the sidebar radio look like large bookmarks */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 0.65rem;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: #f7f8fa;
        border: 1px solid var(--border);
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1rem;
        min-height: 58px;
        cursor: pointer;
        transition: all 0.15s ease;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: #eef2f7;
        transform: translateX(3px);
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: var(--navy);
        border-color: var(--navy);
        border-left: 7px solid var(--gold);
        color: white;
        box-shadow: 0 7px 18px rgba(36, 50, 71, 0.18);
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
        color: white !important;
        font-weight: 800;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        font-size: 0.98rem;
        font-weight: 700;
        color: var(--navy);
    }

    [data-testid="stSidebar"] div[role="radiogroup"] input {
        display: none;
    }

    .page-title {
        font-size: 2.05rem;
        font-weight: 900;
        color: var(--navy);
        letter-spacing: -0.04em;
        margin-bottom: 0.15rem;
    }

    .page-subtitle {
        color: var(--muted);
        margin-bottom: 1.4rem;
    }

    .section-title {
        font-size: 0.76rem;
        color: var(--muted);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: 0.8rem;
    }

    .panel {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(16, 24, 40, 0.035);
    }

    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 1rem 1.1rem;
        min-height: 112px;
        box-shadow: 0 2px 5px rgba(16, 24, 40, 0.035);
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.74rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 800;
    }

    .metric-value {
        color: var(--navy);
        font-size: 2rem;
        font-weight: 900;
        line-height: 1.1;
        margin-top: 0.45rem;
    }

    .metric-note {
        color: var(--muted);
        font-size: 0.78rem;
        margin-top: 0.35rem;
    }

    div[data-testid="stFileUploader"] section {
        background: #fafbfc;
        border: 1.5px dashed #b8c0cc;
        border-radius: 13px;
        padding: 1.4rem;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    .rule-box {
        background: #eef3f9;
        border: 1px solid #d4dfed;
        border-radius: 12px;
        padding: 0.95rem 1.05rem;
        color: #344054;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    footer, #MainMenu, header {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "attendance_df": None,
    "al_df": None,
    "other_leave_df": None,
    "file_names": {},
    "history": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPERS
# ============================================================
STATUS_ORDER = [
    "Normal",
    "Leave Approved",
    "Absent",
    "Forgot Clock-in",
    "Forgot Clock-out",
    "No schedule",
]

WORKING_STATUSES = [
    "Normal",
    "Forgot Clock-in",
    "Forgot Clock-out",
    "Absent",
]


def normalize_id(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\.0$", "", regex=True)
    )


def has_value(value) -> bool:
    if pd.isna(value):
        return False
    if isinstance(value, str):
        return value.strip().lower() not in {"", "nan", "nat", "none", "null", "-", "--"}
    return True


def check_attendance(row: pd.Series) -> str:
    if not has_value(row.get("上段應上班時間")):
        return "No schedule"

    actual_start_missing = not has_value(row.get("上段實際上班時間"))
    actual_end_missing = not has_value(row.get("下段實際下班時間"))

    if actual_start_missing and actual_end_missing:
        return "Absent"
    if actual_start_missing:
        return "Forgot Clock-in"
    if actual_end_missing:
        return "Forgot Clock-out"
    return "Normal"


def parse_al_time(value) -> Optional[str]:
    if pd.isna(value):
        return None

    if isinstance(value, str) and ":" in value:
        parsed = pd.to_datetime(value, errors="coerce")
        return parsed.strftime("%H%M") if not pd.isna(parsed) else None

    try:
        return str(int(float(value))).zfill(4)
    except (ValueError, TypeError):
        return None


def build_datetime(date_series: pd.Series, time_series: pd.Series, mode: str) -> pd.Series:
    if mode == "al":
        time_text = time_series.map(parse_al_time)
        return pd.to_datetime(
            date_series.astype(str) + " " + time_text.astype(str),
            format="%Y-%m-%d %H%M",
            errors="coerce",
        )

    return pd.to_datetime(
        date_series.astype(str) + " " + time_series.astype(str),
        errors="coerce",
    )


def clean_leave_sheet(df: pd.DataFrame, source: str) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = cleaned.columns.astype(str).str.strip().str.lower()

    required = {"empid", "startdate", "starttime", "enddate", "endtime"}
    missing = required - set(cleaned.columns)

    if missing:
        raise ValueError(
            f"{source} is missing columns: {', '.join(sorted(missing))}"
        )

    cleaned["empid"] = normalize_id(cleaned["empid"])
    cleaned["leave source"] = source

    if source == "AL":
        cleaned["leave type"] = "Annual Leave"
        cleaned["請假開始"] = build_datetime(
            cleaned["startdate"], cleaned["starttime"], "al"
        )
        cleaned["請假結束"] = build_datetime(
            cleaned["enddate"], cleaned["endtime"], "al"
        )
    else:
        if "leavetype" in cleaned.columns:
            cleaned["leave type"] = cleaned["leavetype"].fillna("Other Leave")
        else:
            cleaned["leave type"] = "Other Leave"

        cleaned["請假開始"] = build_datetime(
            cleaned["startdate"], cleaned["starttime"], "other"
        )
        cleaned["請假結束"] = build_datetime(
            cleaned["enddate"], cleaned["endtime"], "other"
        )

    return cleaned


def get_shift_times(row: pd.Series):
    shift_start = pd.to_datetime(row.get("上段應上班時間"), errors="coerce")
    shift_end = pd.to_datetime(row.get("下段應下班時間"), errors="coerce")

    if pd.isna(shift_end):
        shift_end = pd.to_datetime(row.get("上段應下班時間"), errors="coerce")

    if not pd.isna(shift_start) and not pd.isna(shift_end) and shift_end <= shift_start:
        shift_end += pd.Timedelta(days=1)

    return shift_start, shift_end


def find_leave_match(
    leave_data: pd.DataFrame,
    empid: str,
    shift_start: pd.Timestamp,
    shift_end: pd.Timestamp,
):
    if leave_data is None or leave_data.empty:
        return None

    matches = leave_data[
        (leave_data["empid"] == empid)
        & (leave_data["請假開始"] < shift_end)
        & (leave_data["請假結束"] > shift_start)
    ]

    return None if matches.empty else matches.sort_values("請假開始").iloc[0]


def compare_with_leave(row: pd.Series, al_df: pd.DataFrame, other_df: pd.DataFrame):
    old_status = row["判斷出勤before leave"]

    # Based on the user's current business rule, leave only replaces Absent.
    if old_status != "Absent":
        return pd.Series([old_status, "", pd.NaT, pd.NaT, ""])

    shift_start, shift_end = get_shift_times(row)

    if pd.isna(shift_start) or pd.isna(shift_end):
        return pd.Series([old_status, "", pd.NaT, pd.NaT, ""])

    empid = row["工號"]

    al_match = find_leave_match(al_df, empid, shift_start, shift_end)
    if al_match is not None:
        return pd.Series([
            "Leave Approved",
            "Annual Leave",
            al_match["請假開始"],
            al_match["請假結束"],
            "AL",
        ])

    other_match = find_leave_match(other_df, empid, shift_start, shift_end)
    if other_match is not None:
        return pd.Series([
            "Leave Approved",
            other_match.get("leave type", "Other Leave"),
            other_match["請假開始"],
            other_match["請假結束"],
            "Other Leave",
        ])

    return pd.Series([old_status, "", pd.NaT, pd.NaT, ""])


def read_and_process(attendance_file, leave_file):
    
    def clean_text(series):
        return (
        series.astype(str)
        .str.replace("\n", " ", regex=False)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\s*-\s*", " - ", regex=True)
        )

    attendance_df["部門"] = clean_text(attendance_df["部門"])
    al_df["departmentname"] = clean_text(al_df["departmentname"])
    other_leave_df["departmentname"] = clean_text(other_leave_df["departmentname"])

    attendance_excel = pd.ExcelFile(attendance_file)
    attendance_sheet = attendance_excel.sheet_names[0]

    attendance = pd.read_excel(
        attendance_file,
        sheet_name=attendance_sheet,
    )
    attendance.columns = attendance.columns.astype(str).str.strip()

    required_attendance = {
        "工號",
        "上段應上班時間",
        "上段實際上班時間",
        "下段實際下班時間",
    }
    missing = required_attendance - set(attendance.columns)

    if missing:
        raise ValueError(
            "Attendance file is missing columns: " + ", ".join(sorted(missing))
        )

    leave_excel = pd.ExcelFile(leave_file)

    if "AL" not in leave_excel.sheet_names:
        raise ValueError("Leave file does not contain an AL sheet.")
    if "Other Leave" not in leave_excel.sheet_names:
        raise ValueError("Leave file does not contain an Other Leave sheet.")

    al_raw = pd.read_excel(leave_file, sheet_name="AL")
    other_raw = pd.read_excel(leave_file, sheet_name="Other Leave")

    al = clean_leave_sheet(al_raw, "AL")
    other = clean_leave_sheet(other_raw, "Other Leave")

    attendance["工號"] = normalize_id(attendance["工號"])
    attendance["判斷出勤before leave"] = attendance.apply(
        check_attendance,
        axis=1,
    )

    result_columns = [
        "判斷出勤after leave",
        "Leave Type",
        "Matched Leave Start",
        "Matched Leave End",
        "Leave Source",
    ]

    attendance[result_columns] = attendance.apply(
        lambda row: compare_with_leave(row, al, other),
        axis=1,
    )

    return attendance, al, other, attendance_sheet


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle=None):
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)

    if subtitle:
        st.markdown(f"<p>{subtitle}</p>", unsafe_allow_html=True)


def require_data():
    if st.session_state.attendance_df is None:
        st.warning("Please upload and process the Attendance and Leave Excel files first.")
        st.stop()


def show_count_percentage_chart(
    df: pd.DataFrame,
    category_column: str,
    status_value: Optional[str],
    title: str,
    key: str,
):
    mode = st.radio(
        "Display",
        ["Count", "Percentage"],
        horizontal=True,
        key=f"{key}_mode",
    )

    working = df.copy()
    if status_value is not None:
        working = working[working["判斷出勤after leave"] == status_value]

    count = (
        working.groupby(category_column, dropna=False)
        .size()
        .sort_values(ascending=False)
        .rename("Count")
        .reset_index()
    )

    if count.empty:
        st.info("No matching records.")
        return

    count["Percentage"] = count["Count"] / count["Count"].sum() * 100
    value_column = mode

    fig = px.bar(
        count,
        x=category_column,
        y=value_column,
        text=count[value_column].map(
            lambda x: f"{x:.1f}%" if mode == "Percentage" else f"{int(x)}"
        ),
        title=title,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Percentage (%)" if mode == "Percentage" else "Count",
        margin=dict(l=20, r=20, t=55, b=20),
        height=440,
    )
    st.plotly_chart(fig, use_container_width=True)

    table = count.copy()
    table["Percentage"] = table["Percentage"].round(2)
    st.dataframe(table, use_container_width=True, hide_index=True)


def make_download_excel():
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        st.session_state.attendance_df.to_excel(
            writer, sheet_name="Attendance Analysis", index=False
        )
        st.session_state.al_df.to_excel(
            writer, sheet_name="AL Cleaned", index=False
        )
        st.session_state.other_leave_df.to_excel(
            writer, sheet_name="Other Leave Cleaned", index=False
        )

    return output.getvalue()


# ============================================================
# SIDEBAR — BOOKMARKS
# ============================================================
st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-name">INGRASYS HR</div>
        <div class="brand-subtitle">
            Singapore attendance,<br>
            absenteeism and leave analysis
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigation",
    [
        "01  Upload",
        "02  Attendance & Absenteeism",
        "03  Leave Data",
        "04  Dashboard",
        "05  History",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")

if st.session_state.attendance_df is not None:
    st.sidebar.success("Data loaded")
    st.sidebar.caption(st.session_state.file_names.get("attendance", ""))
    st.sidebar.caption(st.session_state.file_names.get("leave", ""))
else:
    st.sidebar.caption("No files processed yet.")


# ============================================================
# 01 UPLOAD
# ============================================================
if page == "01  Upload":
    page_header("Upload")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            '<div class="section-title">ATTENDANCE FILE</div>',
            unsafe_allow_html=True
        )

        attendance_file = st.file_uploader(
            "Attendance file",
            type=["xlsx", "xls"],
            key="attendance_upload",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown(
            '<div class="section-title">LEAVE FILE</div>',
            unsafe_allow_html=True
        )

        leave_file = st.file_uploader(
            "Leave file",
            type=["xlsx", "xls"],
            key="leave_upload",
            label_visibility="collapsed"
        )

    # Process button directly below uploaders
    process_clicked = st.button(
        "Process Files",
        type="primary",
        disabled=attendance_file is None or leave_file is None,
        use_container_width=True
    )

    if process_clicked:
        try:
            with st.spinner("Processing Attendance, AL and Other Leave..."):
                attendance, al, other, sheet = read_and_process(
                    attendance_file,
                    leave_file
                )

                st.session_state.attendance_df = attendance
                st.session_state.al_df = al
                st.session_state.other_leave_df = other

                st.session_state.file_names = {
                    "attendance": attendance_file.name,
                    "leave": leave_file.name,
                    "sheet": sheet
                }

                statuses = attendance["判斷出勤after leave"]

                history_item = {
                    "Processed At": datetime.now(),
                    "Attendance File": attendance_file.name,
                    "Leave File": leave_file.name,
                    "Attendance Rows": len(attendance),
                    "Absent": int((statuses == "Absent").sum()),
                    "Leave Approved": int(
                        (statuses == "Leave Approved").sum()
                    ),
                    "Forgot Clock-in": int(
                        (statuses == "Forgot Clock-in").sum()
                    ),
                    "Forgot Clock-out": int(
                        (statuses == "Forgot Clock-out").sum()
                    ),
                    "data": attendance.copy()
                }

                st.session_state.history.insert(0, history_item)

            st.success("Files processed successfully.")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                metric_card(
                    "Attendance rows",
                    f"{len(attendance):,}",
                    f"Sheet: {sheet}"
                )

            with c2:
                metric_card(
                    "Absent",
                    f"{(statuses == 'Absent').sum():,}",
                    "After leave matching"
                )

            with c3:
                metric_card(
                    "Leave Approved",
                    f"{(statuses == 'Leave Approved').sum():,}",
                    "AL + Other Leave"
                )

            with c4:
                missing_punch = statuses.isin([
                    "Forgot Clock-in",
                    "Forgot Clock-out"
                ]).sum()

                metric_card(
                    "Forgot Punch",
                    f"{missing_punch:,}",
                    "Incomplete punch records"
                )

        except Exception as exc:
            st.error(f"Unable to process files: {exc}")


# ============================================================
# 02 ATTENDANCE & ABSENTEEISM
# ============================================================
elif page == "02  Attendance & Absenteeism":
    require_data()
    page_header(
        "Attendance & Absenteeism",
        "Review final attendance results after matching approved leave.",
    )

    df = st.session_state.attendance_df.copy()

    f1, f2, f3 = st.columns(3)
    with f1:
        status_options = STATUS_ORDER
        selected_status = st.multiselect(
            "Status",
            status_options,
            default=["Absent", "Forgot Clock-in", "Forgot Clock-out", "Leave Approved"],
        )
    with f2:
        departments = (
            sorted(df["部門"].dropna().astype(str).unique())
            if "部門" in df.columns else []
        )
        selected_departments = st.multiselect("Department", departments)
    with f3:
        employee_search = st.text_input(
            "Employee search",
            placeholder="Employee ID or name",
        )

    filtered = df[df["判斷出勤after leave"].isin(selected_status)]

    if selected_departments and "部門" in filtered.columns:
        filtered = filtered[filtered["部門"].astype(str).isin(selected_departments)]

    if employee_search:
        id_match = filtered["工號"].astype(str).str.contains(
            employee_search, case=False, na=False
        )
        if "姓名" in filtered.columns:
            name_match = filtered["姓名"].astype(str).str.contains(
                employee_search, case=False, na=False
            )
            filtered = filtered[id_match | name_match]
        else:
            filtered = filtered[id_match]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Records shown", f"{len(filtered):,}", "After filters")
    with c2:
        metric_card("Absent", f"{(filtered['判斷出勤after leave'] == 'Absent').sum():,}")
    with c3:
        metric_card("Leave Approved", f"{(filtered['判斷出勤after leave'] == 'Leave Approved').sum():,}")
    with c4:
        forgot = filtered["判斷出勤after leave"].isin(
            ["Forgot Clock-in", "Forgot Clock-out"]
        ).sum()
        metric_card("Forgot Punch", f"{forgot:,}")

    preferred_columns = [
        "工號",
        "姓名",
        "部門",
        "考勤日期",
        "上段應上班時間",
        "上段實際上班時間",
        "下段應下班時間",
        "下段實際下班時間",
        "判斷出勤before leave",
        "判斷出勤after leave",
        "Leave Type",
        "Matched Leave Start",
        "Matched Leave End",
        "Leave Source",
        "Reporting To",
    ]
    display_columns = [column for column in preferred_columns if column in filtered.columns]

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        height=600,
    )
    st.download_button(
        "Download Full Analysis Excel",
        data=make_download_excel(),
        file_name="Ingrasys_Singapore_HR_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 03 LEAVE DATA
# ============================================================
elif page == "03  Leave Data":
    require_data()
    page_header(
        "Leave Data",
        "AL and Other Leave remain separate because their source formats differ.",
    )

    leave_tab = st.radio(
        "Leave source",
        ["Annual Leave (AL)", "Other Leave"],
        horizontal=True,
    )

    if leave_tab == "Annual Leave (AL)":
        leave_view = st.session_state.al_df.copy()
    else:
        leave_view = st.session_state.other_leave_df.copy()

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Leave records", f"{len(leave_view):,}", leave_tab)
    with c2:
        metric_card("Employees", f"{leave_view['empid'].nunique():,}", "Unique employee IDs")
    with c3:
        valid_periods = (
            leave_view["請假開始"].notna() & leave_view["請假結束"].notna()
        ).sum()
        metric_card("Valid periods", f"{valid_periods:,}", "Parsed start and end")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        if "departmentname" in leave_view.columns:
            leave_departments = sorted(
                leave_view["departmentname"].dropna().astype(str).unique()
            )
            leave_dept_filter = st.multiselect(
                "Department",
                leave_departments,
                key="leave_dept_filter",
            )
        else:
            leave_dept_filter = []
    with filter_col2:
        leave_search = st.text_input(
            "Employee search",
            placeholder="Employee ID or name",
            key="leave_search",
        )

    if leave_dept_filter:
        leave_view = leave_view[
            leave_view["departmentname"].astype(str).isin(leave_dept_filter)
        ]

    if leave_search:
        id_match = leave_view["empid"].astype(str).str.contains(
            leave_search, case=False, na=False
        )
        if "empname" in leave_view.columns:
            name_match = leave_view["empname"].astype(str).str.contains(
                leave_search, case=False, na=False
            )
            leave_view = leave_view[id_match | name_match]
        else:
            leave_view = leave_view[id_match]

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.dataframe(
        leave_view,
        use_container_width=True,
        hide_index=True,
        height=600,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 04 DASHBOARD
# ============================================================
elif page == "04  Dashboard":
    require_data()
    page_header(
        "Dashboard",
        "Switch each visual between Count and Percentage.",
    )

    df = st.session_state.attendance_df.copy()
    working_df = df[df["判斷出勤after leave"].isin(WORKING_STATUSES)]

    scheduled_shifts = len(working_df)
    absent_shifts = int((working_df["判斷出勤after leave"] == "Absent").sum())
    absent_rate = (absent_shifts / scheduled_shifts * 100) if scheduled_shifts else 0

    unique_scheduled = working_df["工號"].nunique()
    unique_absent = working_df.loc[
        working_df["判斷出勤after leave"] == "Absent", "工號"
    ].nunique()
    employee_absent_rate = (
        unique_absent / unique_scheduled * 100 if unique_scheduled else 0
    )

    status = df["判斷出勤after leave"]

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Absence shift rate", f"{absent_rate:.2f}%", f"{absent_shifts:,} absent shifts")
    with c2:
        metric_card("Absent employee rate", f"{employee_absent_rate:.2f}%", f"{unique_absent:,} employees")
    with c3:
        metric_card("Leave Approved", f"{(status == 'Leave Approved').sum():,}", "Covered attendance shifts")
    with c4:
        metric_card("Forgot Clock-in", f"{(status == 'Forgot Clock-in').sum():,}")
    with c5:
        metric_card("Forgot Clock-out", f"{(status == 'Forgot Clock-out').sum():,}")

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    chart_mode = st.radio(
        "Attendance status display",
        ["Count", "Percentage"],
        horizontal=True,
        key="status_chart_mode",
    )

    status_summary = (
        status.value_counts()
        .reindex(STATUS_ORDER, fill_value=0)
        .rename("Count")
        .reset_index()
        .rename(columns={"index": "Status"})
    )
    status_summary["Percentage"] = (
        status_summary["Count"] / status_summary["Count"].sum() * 100
    )

    fig_status = px.pie(
        status_summary,
        names="Status",
        values=chart_mode,
        hole=0.48,
        title=f"Attendance Status — {chart_mode}",
    )
    fig_status.update_traces(
        textinfo="percent+label" if chart_mode == "Count" else "label+value",
        hovertemplate="<b>%{label}</b><br>%{value}<extra></extra>",
    )
    fig_status.update_layout(height=470, margin=dict(l=20, r=20, t=60, b=20))
    st.plotly_chart(fig_status, use_container_width=True)

    status_table = status_summary.copy()
    status_table["Percentage"] = status_table["Percentage"].round(2)
    st.dataframe(status_table, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        if "部門" in df.columns:
            show_count_percentage_chart(
                df=df,
                category_column="部門",
                status_value="Absent",
                title="Absences by Department",
                key="dept_absent",
            )
        else:
            st.info("Department column is unavailable.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        leave_approved = df[df["判斷出勤after leave"] == "Leave Approved"].copy()
        if not leave_approved.empty:
            show_count_percentage_chart(
                df=leave_approved,
                category_column="Leave Type",
                status_value=None,
                title="Approved Leave by Type",
                key="leave_type",
            )
        else:
            st.info("No approved leave records matched Attendance.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    if "考勤日期" in df.columns:
        daily = df.copy()
        daily["Date"] = pd.to_datetime(daily["考勤日期"], errors="coerce").dt.date

        daily_mode = st.radio(
            "Daily trend display",
            ["Count", "Percentage"],
            horizontal=True,
            key="daily_mode",
        )

        daily_summary = daily.groupby("Date").agg(
            Count=("判斷出勤after leave", lambda x: (x == "Absent").sum()),
            Total=("判斷出勤after leave", lambda x: x.isin(WORKING_STATUSES).sum()),
        ).reset_index()

        daily_summary["Percentage"] = (
            daily_summary["Count"] / daily_summary["Total"].replace(0, pd.NA) * 100
        ).fillna(0)

        fig_daily = px.line(
            daily_summary,
            x="Date",
            y=daily_mode,
            markers=True,
            title=f"Daily Absence Trend — {daily_mode}",
        )
        fig_daily.update_layout(
            yaxis_title="Percentage (%)" if daily_mode == "Percentage" else "Count",
            xaxis_title="",
            height=430,
        )
        st.plotly_chart(fig_daily, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 05 HISTORY
# ============================================================
elif page == "05  History":
    page_header(
        "History",
        "Files processed during the current browser session.",
    )

    if not st.session_state.history:
        st.info("No processed history is available yet.")
        st.stop()

    history_table = pd.DataFrame(
        [
            {key: value for key, value in item.items() if key != "data"}
            for item in st.session_state.history
        ]
    )
    history_table["Processed At"] = history_table["Processed At"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.dataframe(
        history_table,
        use_container_width=True,
        hide_index=True,
    )

    history_labels = [
        f"{item['Processed At']:%Y-%m-%d %H:%M} — {item['Attendance File']}"
        for item in st.session_state.history
    ]

    selected_label = st.selectbox("Open processed result", history_labels)
    selected_index = history_labels.index(selected_label)
    selected_item = st.session_state.history[selected_index]

    st.dataframe(
        selected_item["data"],
        use_container_width=True,
        hide_index=True,
        height=520,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "History is session-based in this GitHub/Streamlit version. "
        "It clears when the app restarts. Permanent history requires a database."
    )
