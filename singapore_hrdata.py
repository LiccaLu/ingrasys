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

    /* --------------------------------------------------------
       APP
    -------------------------------------------------------- */
    .stApp {
        background: var(--bg);
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */
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

    /* Make sidebar radio options look like bookmarks */
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

    /* --------------------------------------------------------
       PAGE TEXT
    -------------------------------------------------------- */
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

    /* --------------------------------------------------------
       PANELS AND METRICS
    -------------------------------------------------------- */
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

    /* --------------------------------------------------------
       FILE UPLOADER
    -------------------------------------------------------- */
    div[data-testid="stFileUploader"] section {
        background: #fafbfc;
        border: 1.5px dashed #b8c0cc;
        border-radius: 13px;
        padding: 1.4rem;
    }

    /* --------------------------------------------------------
       DATAFRAME
    -------------------------------------------------------- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* --------------------------------------------------------
       RULE BOX
    -------------------------------------------------------- */
    .rule-box {
        background: #eef3f9;
        border: 1px solid #d4dfed;
        border-radius: 12px;
        padding: 0.95rem 1.05rem;
        color: #344054;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    /* --------------------------------------------------------
       DASHBOARD CARDS
    -------------------------------------------------------- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 1px solid #e4e9f0 !important;
        border-radius: 18px !important;
        box-shadow: 0 5px 18px rgba(36, 50, 71, 0.06);
        padding: 0.35rem;
    }

    [data-testid="stPlotlyChart"] {
        border-radius: 14px;
        overflow: hidden;
    }

    .dashboard-section-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #243247;
        margin-bottom: 0.15rem;
    }

    .dashboard-section-note {
        font-size: 0.78rem;
        color: #758196;
        margin-bottom: 0.75rem;
    }

    div[role="radiogroup"] {
        gap: 0.8rem;
    }

    div[role="radiogroup"] label {
        font-size: 0.86rem;
    }

    /* --------------------------------------------------------
       STREAMLIT HEADER AND SIDEBAR TOGGLE
    -------------------------------------------------------- */

    /* Hide menu and footer only */
    #MainMenu,
    footer {
        visibility: hidden !important;
    }

    /* Never hide the complete header */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        display: block !important;
        background: transparent !important;
    }

    /* Keep the toolbar container alive */
    [data-testid="stToolbar"] {
        visibility: visible !important;
        display: flex !important;
        background: transparent !important;
    }

    /* Hide only right-side toolbar actions */
    [data-testid="stToolbarActions"] {
        visibility: hidden !important;
    }

    /* Sidebar collapse button when sidebar is open */
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }

    /* Sidebar expand button when sidebar is closed */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 999999 !important;
    }

    /* Some Streamlit versions place the control inside this container */
    [data-testid="stHeaderActionElements"] {
        visibility: visible !important;
    }

    /* Keep buttons inside the header clickable */
    header[data-testid="stHeader"] button {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
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

    attendance_excel = pd.ExcelFile(attendance_file)
    attendance_sheet = attendance_excel.sheet_names[0]

    attendance = pd.read_excel(
        attendance_file,
        sheet_name=attendance_sheet,
    )
    attendance.columns = attendance.columns.astype(str).str.strip()

    attendance["部門"] = (
    attendance["部門"]
    .astype(str)
    .str.replace("\n", " ", regex=False)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.replace(r"\s*-\s*", " - ", regex=True)
    )
    
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
    
    # ------------------------------------------------------------
    # Read AL sheet if it exists
    # ------------------------------------------------------------
    if "AL" in leave_excel.sheet_names:
        al_raw = pd.read_excel(
            leave_file,
            sheet_name="AL",
        )
        al_raw.columns = (
            al_raw.columns
            .astype(str)
            .str.strip()
        )
    else:
        al_raw = pd.DataFrame()
    
    # ------------------------------------------------------------
    # Read Other Leave sheet if it exists
    # ------------------------------------------------------------
    if "Other Leave" in leave_excel.sheet_names:
        other_raw = pd.read_excel(
            leave_file,
            sheet_name="Other Leave",
        )
        other_raw.columns = (
            other_raw.columns
            .astype(str)
            .str.strip()
        )
    else:
        other_raw = pd.DataFrame()
    
    # At least one usable leave sheet must exist
    if al_raw.empty and other_raw.empty:
        raise ValueError(
            "Leave file does not contain usable AL or Other Leave data."
        )
    
    # ------------------------------------------------------------
    # Clean only the sheets that contain data
    # ------------------------------------------------------------
    if not al_raw.empty:
        al = clean_leave_sheet(
            al_raw,
            "AL",
        )
    else:
        al = pd.DataFrame(
            columns=[
                "empid",
                "Leave Type",
                "Leave Start",
                "Leave End",
                "Leave Source",
            ]
        )
    
    if not other_raw.empty:
        other = clean_leave_sheet(
            other_raw,
            "Other Leave",
        )
    else:
        other = pd.DataFrame(
            columns=[
                "empid",
                "Leave Type",
                "Leave Start",
                "Leave End",
                "Leave Source",
            ]
        )
    
    # ------------------------------------------------------------
    # Process Attendance
    # ------------------------------------------------------------
    attendance["工號"] = normalize_id(
        attendance["工號"]
    )
    
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
        lambda row: compare_with_leave(
            row,
            al,
            other,
        ),
        axis=1,
        result_type="expand",
    )
    
    return attendance, al, other, attendance_sheet



def style_chart(
    fig,
    height=360,
    show_legend=True,
    legend_position="bottom",
):
    fig.update_layout(
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial, sans-serif",
            size=13,
            color="#243247",
        ),
        margin=dict(
            l=45,
            r=35,
            t=70,
            b=55,
        ),
        hoverlabel=dict(
            bgcolor="#243247",
            font_size=13,
            font_color="white",
            bordercolor="#243247",
        ),
        showlegend=show_legend,
    )

    if show_legend:
        if legend_position == "bottom":
            fig.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.12,
                    xanchor="center",
                    x=0.5,
                    title_text="",
                )
            )
        else:
            fig.update_layout(
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    title_text="",
                )
            )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#E5EAF0",
        tickfont=dict(color="#667085"),
        title_font=dict(color="#667085"),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EEF1F5",
        zeroline=False,
        linecolor="#E5EAF0",
        tickfont=dict(color="#667085"),
        title_font=dict(color="#667085"),
    )

    return fig


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

    st.dataframe(
        leave_view,
        use_container_width=True,
        hide_index=True,
        height=600,
    )


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

    if "部門" in df.columns:
        df["部門"] = (
            df["部門"]
            .astype(str)
            .str.replace("\n", " ", regex=False)
            .str.replace("\u00a0", " ", regex=False)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.replace(r"\s*-\s*", " - ", regex=True)
        )

    working_df = df[
        df["判斷出勤after leave"].isin(WORKING_STATUSES)
    ].copy()

    status = df["判斷出勤after leave"]

    scheduled_shifts = len(working_df)
    absent_shifts = int(
        (working_df["判斷出勤after leave"] == "Absent").sum()
    )

    absence_shift_rate = (
        absent_shifts / scheduled_shifts * 100
        if scheduled_shifts > 0
        else 0
    )

    unique_scheduled_employees = working_df["工號"].nunique()
    unique_absent_employees = working_df.loc[
        working_df["判斷出勤after leave"] == "Absent",
        "工號",
    ].nunique()

    absent_employee_rate = (
        unique_absent_employees
        / unique_scheduled_employees
        * 100
        if unique_scheduled_employees > 0
        else 0
    )

    leave_approved_count = int((status == "Leave Approved").sum())
    forgot_clock_in_count = int((status == "Forgot Clock-in").sum())
    forgot_clock_out_count = int((status == "Forgot Clock-out").sum())

    with st.expander("ℹ️ Data & Graphs Descriptions", expanded=False):
        st.markdown(
            """
### Leave Approved
Attendance records originally classified as **Absent** that overlap an
approved AL or Other Leave period.

### Forgot Clock-in
A scheduled shift has no actual clock-in, but an actual clock-out exists.

### Forgot Clock-out
A scheduled shift has an actual clock-in, but no actual clock-out.

### Daily Absence Trend

This chart summarizes overall attendance performance across the selected reporting period.

- **X-axis:** Attendance date.
- **Y-axis:** Number of absent shifts or absence rate (%), depending on the selected view.
- **Count mode:** Displays the total number of employees recorded as absent each day.
- **Percentage mode:** Displays the daily absence rate, calculated as:

  **Absent shifts ÷ Scheduled shifts × 100**


Each data point also displays:
- Absent shifts
- Scheduled shifts
- Daily absence rate

### Daily Attendance by Department

This chart compares attendance performance across departments for the selected attendance date.

- **Scheduled and Absent mode:** Shows the total scheduled shifts alongside the number of absent shifts for each department.
- **Absence Percentage mode:** Shows the percentage of scheduled shifts that were absent for each department.

The accompanying table includes:
- Attendance date
- Department
- Scheduled shifts
- Absent shifts
- Absence percentage
            """
        )

    st.divider()

    # Daily trend card
    with st.container(border=True):
        st.markdown(
            '<div class="dashboard-section-title">'
            'Daily Absence Trend'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="dashboard-section-note">'
            'Scheduled shifts are counted from the scheduled clock-in time.'
            '</div>',
            unsafe_allow_html=True,
        )
    
        if "上段應上班時間" in df.columns:
            daily_mode = st.radio(
                "Daily trend display",
                ["Count", "Percentage"],
                horizontal=True,
                key="daily_mode",
                label_visibility="collapsed",
            )
    
            daily = df.copy()
    
            # 將上段應上班時間轉成 datetime
            daily["Scheduled Start"] = pd.to_datetime(
                daily["上段應上班時間"],
                errors="coerce",
            )
    
            # 直接從上段應上班時間取得排班日期
            daily["Date"] = (
                daily["Scheduled Start"]
                .dt.normalize()
            )
    
            # 只保留確實有排班時間的紀錄
            daily_scheduled = daily[
                daily["Scheduled Start"].notna()
            ].copy()
    
            # 避免同一員工、同一排班時間重複計算
            daily_scheduled = (
                daily_scheduled
                .sort_values(
                    [
                        "工號",
                        "Scheduled Start",
                    ]
                )
                .drop_duplicates(
                    subset=[
                        "工號",
                        "Scheduled Start",
                    ],
                    keep="first",
                )
            )
    
            # 每日 Scheduled 與 Absent
            daily_summary = (
                daily_scheduled
                .groupby("Date")
                .agg(
                    Scheduled=(
                        "工號",
                        "size",
                    ),
                    Count=(
                        "判斷出勤after leave",
                        lambda values: (
                            values == "Absent"
                        ).sum(),
                    ),
                )
                .reset_index()
                .sort_values("Date")
            )
    
            daily_summary["Scheduled"] = (
                daily_summary["Scheduled"]
                .astype(int)
            )
    
            daily_summary["Count"] = (
                daily_summary["Count"]
                .astype(int)
            )
    
            daily_summary["Percentage"] = (
                daily_summary["Count"]
                / daily_summary["Scheduled"]
                .replace(0, pd.NA)
                * 100
            ).fillna(0)
    
            fig_daily = px.area(
                daily_summary,
                x="Date",
                y=daily_mode,
                custom_data=[
                    "Count",
                    "Scheduled",
                    "Percentage",
                ],
            )
    
            text_positions = [
                    "top right"
                    if index == 0
                    else "top left"
                    if index == len(daily_summary) - 1
                    else "top center"
                    for index in range(len(daily_summary))
                ]
            
            fig_daily.update_traces(
                line=dict(
                    width=3,
                    color="#3957A5",
                    shape="spline",
                ),
                fillcolor="rgba(57, 87, 165, 0.18)",
                marker=dict(
                    size=7,
                    color="#3957A5",
                ),
                
                mode="lines+markers+text",
    
                text=[
                    (
                        f"Count: {count}<br>"
                        f"Scheduled: {scheduled}<br>"
                        f"{percentage:.2f}%"
                    )
                    for count, scheduled, percentage in zip(
                        daily_summary["Count"],
                        daily_summary["Scheduled"],
                        daily_summary["Percentage"],
                    )
                ],
                
                textposition=text_positions,
            
                textfont=dict(
                    size=11,
                    color="#243247",
                ),
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x|%Y-%m-%d}</b><br>"
                    "Absent shifts: %{customdata[0]:,}<br>"
                    "Scheduled shifts: %{customdata[1]:,}<br>"
                    "Absence rate: %{customdata[2]:.2f}%"
                    "<extra></extra>"
                ),
            )
    
            fig_daily = style_chart(
                fig_daily,
                height=360,
                show_legend=False,
            )
    
            
            fig_daily.update_layout(
                title="",
                xaxis_title="",
                yaxis_title=(
                    "Absence rate (%)"
                    if daily_mode == "Percentage"
                    else "Absent shifts"
                ),
                margin=dict(
                l=110,
                r=110,
                t=130,
                b=70,
            ),
        )
    
            fig_daily.update_xaxes(
                type="date",
                tickformat="%d %b",
                dtick="D1",
            )
    
            st.plotly_chart(
        fig_daily,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "Daily_Absence_Trend",
                "height": 700,
                "width": 1400,
                "scale": 2,
            },
    
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
                "autoScale2d",
                "toggleSpikelines",
            ],
        },
    )
    
            daily_table = daily_summary.copy()
    
            daily_table["Date"] = (
                pd.to_datetime(
                    daily_table["Date"]
                )
                .dt.strftime("%Y-%m-%d")
            )
    
            daily_table["Percentage"] = (
                daily_table["Percentage"]
                .round(2)
            )
    
            st.dataframe(
                daily_table[
                    [
                        "Date",
                        "Count",
                        "Scheduled",
                        "Percentage",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )
    
        else:
            st.info(
                "Scheduled clock-in time column is unavailable."
            )


    # Absence and Scheduled Shifts by Department and Date
    
    with st.container(border=True):
        st.markdown(
            '<div class="dashboard-section-title">'
            'Daily Attendance by Department'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="dashboard-section-note">'
            'Scheduled and absent shifts for each department by date.'
            '</div>',
            unsafe_allow_html=True,
        )

        if (
            "部門" in df.columns
            and "上段應上班時間" in df.columns
        ):
            department_daily = df.copy()

            department_daily["Scheduled Start"] = pd.to_datetime(
                department_daily["上段應上班時間"],
                errors="coerce",
            )

            department_daily["Schedule Date"] = (
                department_daily["Scheduled Start"]
                .dt.normalize()
            )

            # 只保留有排班時間的紀錄
            department_daily = department_daily[
                department_daily["Scheduled Start"].notna()
                & department_daily["部門"].notna()
            ].copy()

            # 清理部門名稱中的空格與換行
            department_daily["部門"] = (
                department_daily["部門"]
                .astype(str)
                .str.replace("\n", " ", regex=False)
                .str.replace("\u00a0", " ", regex=False)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.replace(r"\s*-\s*", " - ", regex=True)
            )

            # 同一員工、同一排班時間只保留一次
            department_daily = (
                department_daily
                .sort_values(
                    [
                        "工號",
                        "Scheduled Start",
                    ]
                )
                .drop_duplicates(
                    subset=[
                        "工號",
                        "Scheduled Start",
                    ],
                    keep="first",
                )
            )

            available_department_dates = (
                department_daily["Schedule Date"]
                .dropna()
                .drop_duplicates()
                .sort_values()
                .tolist()
            )

            if available_department_dates:
                selected_department_date = st.selectbox(
                    "Attendance date",
                    options=available_department_dates,
                    format_func=lambda value: value.strftime(
                        "%Y-%m-%d"
                    ),
                    key="department_attendance_date",
                )

                department_mode = st.radio(
                    "Department display",
                    [
                        "Scheduled and Absent",
                        "Absence Percentage",
                    ],
                    horizontal=True,
                    key="department_daily_mode",
                    label_visibility="collapsed",
                )

                # 只分析所選日期
                selected_department_df = department_daily[
                    department_daily["Schedule Date"]
                    == selected_department_date
                ].copy()

                department_summary = (
                    selected_department_df
                    .groupby(
                        "部門",
                        dropna=False,
                    )
                    .agg(
                        Scheduled=(
                            "工號",
                            "size",
                        ),
                        Absent=(
                            "判斷出勤after leave",
                            lambda values: (
                                values == "Absent"
                            ).sum(),
                        ),
                    )
                    .reset_index()
                )

                department_summary["Percentage"] = (
                    department_summary["Absent"]
                    / department_summary["Scheduled"]
                    .replace(0, pd.NA)
                    * 100
                ).fillna(0)

                if department_mode == "Scheduled and Absent":
                    # 轉換為 Plotly grouped bar 所需格式
                    department_chart_df = (
                        department_summary[
                            [
                                "部門",
                                "Scheduled",
                                "Absent",
                            ]
                        ]
                        .melt(
                            id_vars="部門",
                            value_vars=[
                                "Scheduled",
                                "Absent",
                            ],
                            var_name="Shift Type",
                            value_name="Count",
                        )
                    )

                    fig_dept = px.bar(
                        department_chart_df,
                        x="Count",
                        y="部門",
                        color="Shift Type",
                        orientation="h",
                        barmode="group",
                        text="Count",
                        color_discrete_map={
                            "Scheduled": "#3957A5",
                            "Absent": "#EF5B5B",
                        },
                    )

                    fig_dept.update_traces(
                        textposition="outside",
                        cliponaxis=False,
                        hovertemplate=(
                            "<b>%{y}</b><br>"
                            "%{fullData.name}: %{x:,}"
                            "<extra></extra>"
                        ),
                    )

                    fig_dept.update_layout(
                        xaxis_title="Number of shifts",
                    )

                else:
                    department_chart_df = (
                        department_summary
                        .sort_values(
                            "Percentage",
                            ascending=True,
                        )
                    )

                    department_chart_df["Label"] = (
                        department_chart_df["Percentage"]
                        .map(
                            lambda value: f"{value:.2f}%"
                        )
                    )

                    fig_dept = px.bar(
                        department_chart_df,
                        x="Percentage",
                        y="部門",
                        orientation="h",
                        text="Label",
                    )

                    fig_dept.update_traces(
                        marker_color="#EF5B5B",
                        textposition="outside",
                        cliponaxis=False,
                        hovertemplate=(
                            "<b>%{y}</b><br>"
                            "Absence rate: %{x:.2f}%"
                            "<extra></extra>"
                        ),
                    )

                    fig_dept.update_layout(
                        xaxis_title="Absence rate (%)",
                    )

                fig_dept = style_chart(
                    fig_dept,
                    height=470,
                    show_legend=(
                        department_mode
                        == "Scheduled and Absent"
                    ),
                    legend_position="bottom",
                )

                fig_dept.update_layout(
                    title_text="",
                    yaxis_title="",
                    margin=dict(
                        l=220,
                        r=80,
                        t=35,
                        b=80,
                    ),
                )

                st.plotly_chart(
                    fig_dept,
                    use_container_width=True,
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": (
                                "Department_Attendance_"
                                + selected_department_date.strftime(
                                    "%Y-%m-%d"
                                )
                            ),
                            "height": 900,
                            "width": 1500,
                            "scale": 2,
                        },
                    },
                )

                department_table = (
                    department_summary.copy()
                )

                department_table["Percentage"] = (
                    department_table["Percentage"]
                    .round(2)
                )

                department_table.insert(
                    0,
                    "Date",
                    selected_department_date.strftime(
                        "%Y-%m-%d"
                    ),
                )

                st.dataframe(
                    department_table[
                        [
                            "Date",
                            "部門",
                            "Scheduled",
                            "Absent",
                            "Percentage",
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

            else:
                st.info(
                    "No valid scheduled dates are available."
                )

        else:
            st.info(
                "Department or scheduled clock-in column "
                "is unavailable."
            )

# ============================================================
# 05 HISTORY
# ============================================================
elif page == "05  History":
    page_header(
        "History",
        "Files processed during the current browser session.",
    )

    if not st.session_state.history:
        st.info(
            "No processed history is available yet."
        )
        st.stop()

    def to_taiwan_time(value):
        timestamp = pd.Timestamp(value)

        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize(
                "Asia/Taipei"
            )

        return timestamp.tz_convert(
            "Asia/Taipei"
        )

    # --------------------------------------------------------
    # Build history summary
    # --------------------------------------------------------
    history_rows = []
    
    for item in st.session_state.history:
        period_start = pd.to_datetime(
            item.get("Period Start"),
            errors="coerce",
        )
    
        period_end = pd.to_datetime(
            item.get("Period End"),
            errors="coerce",
        )
    
        history_rows.append(
            {
                "Processed At": to_taiwan_time(
                    item.get("Processed At")
                ).strftime("%Y-%m-%d %H:%M:%S"),
    
                "Period Start": (
                    period_start.strftime("%Y-%m-%d")
                    if pd.notna(period_start)
                    else ""
                ),
    
                "Period End": (
                    period_end.strftime("%Y-%m-%d")
                    if pd.notna(period_end)
                    else ""
                ),
    
                "Attendance File": item.get(
                    "Attendance File",
                    "",
                ),
    
                "Leave File": item.get(
                    "Leave File",
                    "",
                ),
    
                "Attendance Rows": item.get(
                    "Attendance Rows",
                    0,
                ),
    
                "Absent": item.get(
                    "Absent",
                    0,
                ),
    
                "Leave Approved": item.get(
                    "Leave Approved",
                    0,
                ),
    
                "Forgot Clock-in": item.get(
                    "Forgot Clock-in",
                    0,
                ),
    
                "Forgot Clock-out": item.get(
                    "Forgot Clock-out",
                    0,
                ),
            }
        )
    
    history_table = pd.DataFrame(history_rows)

    # --------------------------------------------------------
    # Create selection labels
    # --------------------------------------------------------
    history_labels = []

    for item in st.session_state.history:
        period_start = pd.to_datetime(
            item.get("Period Start"),
            errors="coerce",
        )
    
        period_end = pd.to_datetime(
            item.get("Period End"),
            errors="coerce",
        )
    
        if pd.notna(period_start) and pd.notna(period_end):
            period_text = (
                f"{period_start:%Y-%m-%d} to "
                f"{period_end:%Y-%m-%d}"
            )
        else:
            # 舊的 history 沒有 Period Start / Period End
            item_data = item.get("data", pd.DataFrame())
    
            if (
                isinstance(item_data, pd.DataFrame)
                and not item_data.empty
                and "考勤日期" in item_data.columns
            ):
                attendance_dates = pd.to_datetime(
                    item_data["考勤日期"],
                    errors="coerce",
                ).dropna()
    
                if not attendance_dates.empty:
                    period_start = attendance_dates.min().normalize()
                    period_end = attendance_dates.max().normalize()
    
                    # 補回舊 history，之後就可直接使用
                    item["Period Start"] = period_start
                    item["Period End"] = period_end
    
                    period_text = (
                        f"{period_start:%Y-%m-%d} to "
                        f"{period_end:%Y-%m-%d}"
                    )
                else:
                    period_text = "Date unavailable"
            else:
                period_text = "Date unavailable"
    
        history_labels.append(
            f"{period_text} — {item.get('Attendance File', 'Unknown file')}"
        )

    # --------------------------------------------------------
    # Combine all weeks
    # --------------------------------------------------------
    if selected_label == "Combine all processed weeks":
        combined_history = pd.concat(
            [
                item["data"].copy()
                for item
                in st.session_state.history
            ],
            ignore_index=True,
        )

        # Remove identical employee/date/shift duplicates
        duplicate_columns = [
            column
            for column in [
                "工號",
                "考勤日期",
                "上段應上班時間",
            ]
            if column in combined_history.columns
        ]

        if duplicate_columns:
            combined_history = (
                combined_history
                .drop_duplicates(
                    subset=duplicate_columns,
                    keep="last",
                )
                .reset_index(drop=True)
            )

        st.caption(
            f"Combined records: "
            f"{len(combined_history):,}"
        )

        st.dataframe(
            combined_history,
            use_container_width=True,
            hide_index=True,
            height=520,
        )

    # --------------------------------------------------------
    # Show one selected week
    # --------------------------------------------------------
    else:
        selected_index = (
            history_labels.index(
                selected_label
            )
        )

        selected_item = (
            st.session_state.history[
                selected_index
            ]
        )

        st.dataframe(
            selected_item["data"],
            use_container_width=True,
            hide_index=True,
            height=520,
        )

    st.caption(
        "History is stored only during the current browser session. "
        "It clears when the app restarts. Permanent history requires a database."
    )
