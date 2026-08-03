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

    # ============================================================
    # DAILY ABSENCE RATE — WITH AND WITHOUT APPROVED LEAVE
    # ============================================================
    with st.container(border=True):
        st.markdown(
            '<div class="dashboard-section-title">'
            'Daily Absence Rate'
            '</div>',
            unsafe_allow_html=True,
        )
    
        st.markdown(
            '<div class="dashboard-section-note">'
            'Comparison of total absence including approved leave '
            'and unplanned absence excluding approved leave.'
            '</div>',
            unsafe_allow_html=True,
        )
    
        if (
            "上段應上班時間" in df.columns
            and "判斷出勤after leave" in df.columns
        ):
            daily = df.copy()
    
            # ----------------------------------------------------
            # Parse scheduled clock-in time
            # ----------------------------------------------------
            daily["Scheduled Start"] = pd.to_datetime(
                daily["上段應上班時間"],
                errors="coerce",
            )
    
            daily["Date"] = (
                daily["Scheduled Start"]
                .dt.normalize()
            )
    
            # Only scheduled records
            daily_scheduled = daily[
                daily["Scheduled Start"].notna()
            ].copy()
    
            # One employee + one scheduled start = one shift
            duplicate_columns = [
                column
                for column in [
                    "工號",
                    "Scheduled Start",
                ]
                if column in daily_scheduled.columns
            ]
    
            if duplicate_columns:
                daily_scheduled = (
                    daily_scheduled
                    .sort_values(duplicate_columns)
                    .drop_duplicates(
                        subset=duplicate_columns,
                        keep="first",
                    )
                    .reset_index(drop=True)
                )
    
            # ----------------------------------------------------
            # Daily summary
            # ----------------------------------------------------
            daily_summary = (
                daily_scheduled
                .groupby("Date")
                .agg(
                    Scheduled=(
                        "判斷出勤after leave",
                        "size",
                    ),
                    Absent=(
                        "判斷出勤after leave",
                        lambda values: (
                            values == "Absent"
                        ).sum(),
                    ),
                    Approved_Leave=(
                        "判斷出勤after leave",
                        lambda values: (
                            values == "Leave Approved"
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
    
            daily_summary["Absent"] = (
                daily_summary["Absent"]
                .astype(int)
            )
    
            daily_summary["Approved Leave"] = (
                daily_summary["Approved_Leave"]
                .astype(int)
            )
    
            # Chart A numerator:
            # Absent + approved leave
            daily_summary["Absence incl. Approved Leave"] = (
                daily_summary["Absent"]
                + daily_summary["Approved Leave"]
            )
    
            # Chart A percentage
            daily_summary["Rate A"] = (
                daily_summary[
                    "Absence incl. Approved Leave"
                ]
                / daily_summary["Scheduled"].replace(0, pd.NA)
                * 100
            ).fillna(0)
    
            # Chart B percentage:
            # Actual unplanned absence only
            daily_summary["Rate B"] = (
                daily_summary["Absent"]
                / daily_summary["Scheduled"].replace(0, pd.NA)
                * 100
            ).fillna(0)
    
            daily_summary["Date Label"] = (
                pd.to_datetime(daily_summary["Date"])
                  .dt.strftime("%d %b")
            )
    
            # ============================================================
            # CHART A — INCLUDING APPROVED LEAVE
            # ============================================================
            with st.container(border=True):
                fig_rate_a = px.bar(
                    daily_summary,
                    x="Date",
                    y="Rate A",
                    text=daily_summary["Rate A"].map(
                        lambda value: f"{value:.1f}%"
                    ),
                    custom_data=[
                        "Scheduled",
                        "Absent",
                        "Approved Leave",
                        "Absence incl. Approved Leave",
                        "Rate A",
                    ],
                )
            
                fig_rate_a.update_traces(
                    marker_color="#285781",
            
                    # Do not set width=0.42 when x is a date axis.
                    # Plotly interprets date-axis width in milliseconds.
                    textposition="outside",
                    textfont=dict(
                        size=16,
                        color="#111111",
                    ),
                    cliponaxis=False,
                    hovertemplate=(
                        "<b>%{x|%Y-%m-%d}</b><br>"
                        "Scheduled shifts: %{customdata[0]:,}<br>"
                        "Unplanned absent: %{customdata[1]:,}<br>"
                        "Approved leave: %{customdata[2]:,}<br>"
                        "Total incl. approved leave: "
                        "%{customdata[3]:,}<br>"
                        "Absence rate A: %{customdata[4]:.2f}%"
                        "<extra></extra>"
                    ),
                )
            
                maximum_rate_a = daily_summary["Rate A"].max()
            
                fig_rate_a.update_layout(
                    title=dict(
                        text=(
                            "Chart A - Absence Rate "
                            "incl. Approved Leave"
                        ),
                        x=0.5,
                        xanchor="center",
                        font=dict(
                            size=22,
                            color="#111111",
                        ),
                    ),
                    height=520,
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    showlegend=False,
                    bargap=0.55,
                    margin=dict(
                        l=80,
                        r=50,
                        t=100,
                        b=100,
                    ),
                    font=dict(
                        family="Arial, sans-serif",
                        size=14,
                        color="#243247",
                    ),
                    xaxis=dict(
                        title="",
                        type="date",
                        tickformat="%d %b",
                        dtick="D1",
                        showgrid=False,
                        zeroline=False,
                        showline=True,
                        linecolor="#222222",
                        linewidth=1.3,
                        ticks="outside",
                        ticklen=7,
                        tickangle=0,
                        tickfont=dict(
                            size=16,
                        ),
                        automargin=True,
                    ),
                    yaxis=dict(
                        title=dict(
                            text="Absence Rate",
                            font=dict(
                                size=17,
                            ),
                        ),
                        range=[
                            0,
                            max(
                                5,
                                maximum_rate_a * 1.28,
                            ),
                        ],
                        ticksuffix="%",
                        tickformat=".0f",
                        showgrid=False,
                        zeroline=False,
                        showline=True,
                        linecolor="#222222",
                        linewidth=1.3,
                        ticks="outside",
                        ticklen=7,
                        tickfont=dict(
                            size=14,
                        ),
                        automargin=True,
                    ),
                    hoverlabel=dict(
                        bgcolor="#243247",
                        font_size=14,
                        font_color="white",
                        bordercolor="#243247",
                    ),
                )
            
                st.plotly_chart(
                    fig_rate_a,
                    use_container_width=True,
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": (
                                "Absence_Rate_"
                                "Including_Approved_Leave"
                            ),
                            "height": 900,
                            "width": 1600,
                            "scale": 2,
                        },
                    },
                )
            
            
            # ============================================================
            # CHART B — EXCLUDING APPROVED LEAVE
            # ============================================================
            with st.container(border=True):
                fig_rate_b = px.bar(
                    daily_summary,
                    x="Date",
                    y="Rate B",
                    text=daily_summary["Rate B"].map(
                        lambda value: f"{value:.1f}%"
                    ),
                    custom_data=[
                        "Scheduled",
                        "Absent",
                        "Approved Leave",
                        "Rate B",
                    ],
                )
            
                fig_rate_b.update_traces(
                    marker_color="#C95A08",
            
                    # Do not set width=0.42 when x is a date axis.
                    textposition="outside",
                    textfont=dict(
                        size=16,
                        color="#111111",
                    ),
                    cliponaxis=False,
                    hovertemplate=(
                        "<b>%{x|%Y-%m-%d}</b><br>"
                        "Scheduled shifts: %{customdata[0]:,}<br>"
                        "Unplanned absent: %{customdata[1]:,}<br>"
                        "Approved leave excluded: "
                        "%{customdata[2]:,}<br>"
                        "Absence rate B: %{customdata[3]:.2f}%"
                        "<extra></extra>"
                    ),
                )
            
                maximum_rate_b = daily_summary["Rate B"].max()
            
                fig_rate_b.update_layout(
                    title=dict(
                        text=(
                            "Chart B - Absence Rate "
                            "excl. Approved Leave (Unplanned)"
                        ),
                        x=0.5,
                        xanchor="center",
                        font=dict(
                            size=22,
                            color="#111111",
                        ),
                    ),
                    height=520,
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    showlegend=False,
                    bargap=0.55,
                    margin=dict(
                        l=80,
                        r=50,
                        t=100,
                        b=100,
                    ),
                    font=dict(
                        family="Arial, sans-serif",
                        size=14,
                        color="#243247",
                    ),
                    xaxis=dict(
                        title="",
                        type="date",
                        tickformat="%d %b",
                        dtick="D1",
                        showgrid=False,
                        zeroline=False,
                        showline=True,
                        linecolor="#222222",
                        linewidth=1.3,
                        ticks="outside",
                        ticklen=7,
                        tickangle=0,
                        tickfont=dict(
                            size=14,
                        ),
                        automargin=True,
                    ),
                    yaxis=dict(
                        title=dict(
                            text="Absence Rate",
                            font=dict(
                                size=17,
                            ),
                        ),
                        range=[
                            0,
                            max(
                                5,
                                maximum_rate_b * 1.28,
                            ),
                        ],
                        ticksuffix="%",
                        tickformat=".0f",
                        showgrid=False,
                        zeroline=False,
                        showline=True,
                        linecolor="#222222",
                        linewidth=1.3,
                        ticks="outside",
                        ticklen=7,
                        tickfont=dict(
                            size=16,
                        ),
                        automargin=True,
                    ),
                    hoverlabel=dict(
                        bgcolor="#243247",
                        font_size=14,
                        font_color="white",
                        bordercolor="#243247",
                    ),
                )
            
                st.plotly_chart(
                    fig_rate_b,
                    use_container_width=True,
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": (
                                "Absence_Rate_"
                                "Excluding_Approved_Leave"
                            ),
                            "height": 900,
                            "width": 1600,
                            "scale": 2,
                        },
                    },
                )
    
            # ====================================================
            # DATA TABLE
            # ====================================================
            daily_rate_table = daily_summary[
                [
                    "Date Label",
                    "Scheduled",
                    "Absent",
                    "Approved Leave",
                    "Absence incl. Approved Leave",
                    "Rate A",
                    "Rate B",
                ]
            ].copy()
    
            daily_rate_table = daily_rate_table.rename(
                columns={
                    "Date Label": "Date",
                    "Rate A": (
                        "Rate A incl. Approved Leave (%)"
                    ),
                    "Rate B": (
                        "Rate B excl. Approved Leave (%)"
                    ),
                }
            )
    
            daily_rate_table[
                "Rate A incl. Approved Leave (%)"
            ] = daily_rate_table[
                "Rate A incl. Approved Leave (%)"
            ].round(2)
    
            daily_rate_table[
                "Rate B excl. Approved Leave (%)"
            ] = daily_rate_table[
                "Rate B excl. Approved Leave (%)"
            ].round(2)
    
            st.dataframe(
                daily_rate_table,
                use_container_width=True,
                hide_index=True,
            )
    
        else:
            st.info(
                "Scheduled clock-in time or final attendance "
                "status column is unavailable."
            )
    # ============================================================
    # DAILY ATTENDANCE BY DEPARTMENT
    # ============================================================
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
    
        required_department_columns = [
            "部門",
            "上段應上班時間",
            "判斷出勤after leave",
        ]
    
        missing_department_columns = [
            column
            for column in required_department_columns
            if column not in df.columns
        ]
    
        if missing_department_columns:
            st.info(
                "Required department attendance columns are unavailable: "
                + ", ".join(missing_department_columns)
            )
    
        else:
            department_daily = df.copy()
    
            # ----------------------------------------------------
            # Parse scheduled clock-in date and time
            # ----------------------------------------------------
            department_daily["Scheduled Start"] = pd.to_datetime(
                department_daily["上段應上班時間"],
                errors="coerce",
            )
    
            department_daily["Date"] = (
                department_daily["Scheduled Start"]
                .dt.normalize()
            )
    
            # Only rows with a valid scheduled clock-in
            department_daily = department_daily[
                department_daily["Scheduled Start"].notna()
                & department_daily["Date"].notna()
                & department_daily["部門"].notna()
            ].copy()
    
            department_daily["部門"] = (
                department_daily["部門"]
                .astype(str)
                .str.strip()
            )
    
            # ----------------------------------------------------
            # One employee + scheduled start = one scheduled shift
            # ----------------------------------------------------
            duplicate_columns = [
                column
                for column in [
                    "工號",
                    "Scheduled Start",
                ]
                if column in department_daily.columns
            ]
    
            if duplicate_columns:
                department_daily = (
                    department_daily
                    .sort_values(duplicate_columns)
                    .drop_duplicates(
                        subset=duplicate_columns,
                        keep="first",
                    )
                    .reset_index(drop=True)
                )
    
            if department_daily.empty:
                st.info(
                    "No valid scheduled department attendance records are available."
                )
    
            else:
                # ------------------------------------------------
                # Build department summary by date
                # ------------------------------------------------
                department_summary_all = (
                    department_daily
                    .groupby(
                        [
                            "Date",
                            "部門",
                        ],
                        dropna=False,
                    )
                    .agg(
                        Scheduled=(
                            "判斷出勤after leave",
                            "size",
                        ),
                        Absent=(
                            "判斷出勤after leave",
                            lambda values: (
                                values == "Absent"
                            ).sum(),
                        ),
                        Approved_Leave=(
                            "判斷出勤after leave",
                            lambda values: (
                                values == "Leave Approved"
                            ).sum(),
                        ),
                    )
                    .reset_index()
                )
    
                department_summary_all["Scheduled"] = (
                    department_summary_all["Scheduled"]
                    .astype(int)
                )
    
                department_summary_all["Absent"] = (
                    department_summary_all["Absent"]
                    .astype(int)
                )
    
                department_summary_all["Approved Leave"] = (
                    department_summary_all["Approved_Leave"]
                    .astype(int)
                )
    
                department_summary_all["Percentage"] = (
                    department_summary_all["Absent"]
                    / department_summary_all[
                        "Scheduled"
                    ].replace(0, pd.NA)
                    * 100
                ).fillna(0)
    
                # Optional rate including approved leave
                department_summary_all[
                    "Percentage incl. Approved Leave"
                ] = (
                    (
                        department_summary_all["Absent"]
                        + department_summary_all[
                            "Approved Leave"
                        ]
                    )
                    / department_summary_all[
                        "Scheduled"
                    ].replace(0, pd.NA)
                    * 100
                ).fillna(0)
    
                available_department_dates = (
                    department_summary_all["Date"]
                    .dropna()
                    .sort_values()
                    .unique()
                    .tolist()
                )
    
                if not available_department_dates:
                    st.info(
                        "No valid attendance dates are available."
                    )
    
                else:
                    selected_department_date = st.selectbox(
                        "Attendance date",
                        options=available_department_dates,
                        format_func=lambda value: pd.Timestamp(
                            value
                        ).strftime("%Y-%m-%d"),
                        key="department_attendance_date",
                    )
    
                    department_chart_mode = st.radio(
                        "Department chart display",
                        [
                            "Scheduled and Absent",
                            "Absence Percentage",
                        ],
                        horizontal=True,
                        key="department_chart_mode",
                        label_visibility="collapsed",
                    )
    
                    selected_department_summary = (
                        department_summary_all[
                            department_summary_all["Date"]
                            == pd.Timestamp(
                                selected_department_date
                            )
                        ]
                        .copy()
                    )
    
                    # Remove departments with no scheduled shift
                    selected_department_summary = (
                        selected_department_summary[
                            selected_department_summary[
                                "Scheduled"
                            ] > 0
                        ]
                        .copy()
                    )
    
                    selected_department_summary["Date Label"] = (
                        pd.to_datetime(
                            selected_department_summary["Date"]
                        )
                        .dt.strftime("%Y-%m-%d")
                    )
    
                    if selected_department_summary.empty:
                        st.info(
                            "No department attendance records are available "
                            "for the selected date."
                        )
    
                    else:
                        # ========================================
                        # MODE 1: Scheduled and Absent
                        # ========================================
                        if (
                            department_chart_mode
                            == "Scheduled and Absent"
                        ):
                            selected_department_summary = (
                                selected_department_summary
                                .sort_values(
                                    "Scheduled",
                                    ascending=True,
                                )
                                .reset_index(drop=True)
                            )
    
                            department_long = (
                                selected_department_summary
                                .melt(
                                    id_vars=[
                                        "部門",
                                        "Date",
                                        "Percentage",
                                    ],
                                    value_vars=[
                                        "Scheduled",
                                        "Absent",
                                    ],
                                    var_name="Attendance Type",
                                    value_name="Shifts",
                                )
                            )
    
                            fig_department = px.bar(
                                department_long,
                                x="Shifts",
                                y="部門",
                                color="Attendance Type",
                                orientation="h",
                                barmode="group",
                                text="Shifts",
                                custom_data=[
                                    "Date",
                                    "Percentage",
                                ],
                                color_discrete_map={
                                    "Scheduled": "#3957A5",
                                    "Absent": "#FF5A5F",
                                },
                            )
    
                            fig_department.update_traces(
                                textposition="outside",
                                cliponaxis=False,
                                textfont=dict(
                                    size=14,
                                    color="#243247",
                                ),
                                hovertemplate=(
                                    "<b>%{y}</b><br>"
                                    "Date: %{customdata[0]|%Y-%m-%d}<br>"
                                    "%{fullData.name}: %{x:,}<br>"
                                    "Absence rate: "
                                    "%{customdata[1]:.2f}%"
                                    "<extra></extra>"
                                ),
                            )
    
                            department_height = max(
                                420,
                                len(
                                    selected_department_summary
                                ) * 75 + 150,
                            )
    
                            fig_department = style_chart(
                                fig_department,
                                height=department_height,
                                show_legend=True,
                                legend_position="bottom",
                            )
    
                            fig_department.update_layout(
                                title_text="",
                                xaxis_title="Number of shifts",
                                yaxis_title="",
                                bargap=0.30,
                                margin=dict(
                                    l=250,
                                    r=90,
                                    t=45,
                                    b=90,
                                ),
                                legend_title_text="",
                            )
    
                        # ========================================
                        # MODE 2: Absence Percentage
                        # ========================================
                        else:
                            selected_department_summary = (
                                selected_department_summary
                                .sort_values(
                                    "Percentage",
                                    ascending=True,
                                )
                                .reset_index(drop=True)
                            )
    
                            selected_department_summary[
                                "Percentage Label"
                            ] = (
                                selected_department_summary[
                                    "Percentage"
                                ]
                                .map(
                                    lambda value: (
                                        f"{value:.2f}%"
                                    )
                                )
                            )
    
                            fig_department = px.bar(
                                selected_department_summary,
                                x="Percentage",
                                y="部門",
                                orientation="h",
                                text="Percentage Label",
                                custom_data=[
                                    "Scheduled",
                                    "Absent",
                                    "Approved Leave",
                                    "Percentage",
                                ],
                            )
    
                            fig_department.update_traces(
                                marker_color="#3957A5",
                                textposition="outside",
                                cliponaxis=False,
                                textfont=dict(
                                    size=14,
                                    color="#243247",
                                ),
                                hovertemplate=(
                                    "<b>%{y}</b><br>"
                                    "Scheduled shifts: "
                                    "%{customdata[0]:,}<br>"
                                    "Absent shifts: "
                                    "%{customdata[1]:,}<br>"
                                    "Approved leave: "
                                    "%{customdata[2]:,}<br>"
                                    "Absence rate: "
                                    "%{customdata[3]:.2f}%"
                                    "<extra></extra>"
                                ),
                            )
    
                            department_height = max(
                                420,
                                len(
                                    selected_department_summary
                                ) * 70 + 140,
                            )
    
                            fig_department = style_chart(
                                fig_department,
                                height=department_height,
                                show_legend=False,
                            )
    
                            maximum_department_rate = (
                                selected_department_summary[
                                    "Percentage"
                                ].max()
                            )
    
                            fig_department.update_layout(
                                title_text="",
                                xaxis_title="Absence rate",
                                yaxis_title="",
                                bargap=0.38,
                                margin=dict(
                                    l=250,
                                    r=100,
                                    t=45,
                                    b=75,
                                ),
                            )
    
                            fig_department.update_xaxes(
                                range=[
                                    0,
                                    max(
                                        5,
                                        maximum_department_rate
                                        * 1.25,
                                    ),
                                ],
                                ticksuffix="%",
                                tickformat=".0f",
                            )
    
                        # ------------------------------------------------
                        # Display department chart
                        # ------------------------------------------------
                        st.plotly_chart(
                            fig_department,
                            use_container_width=True,
                            config={
                                "displayModeBar": True,
                                "displaylogo": False,
                                "toImageButtonOptions": {
                                    "format": "png",
                                    "filename": (
                                        "Daily_Attendance_by_Department_"
                                        + pd.Timestamp(
                                            selected_department_date
                                        ).strftime("%Y-%m-%d")
                                        + "_"
                                        + department_chart_mode
                                        .replace(" ", "_")
                                    ),
                                    "height": 1000,
                                    "width": 1800,
                                    "scale": 2,
                                },
                            },
                        )
    
                        # ------------------------------------------------
                        # Department summary table
                        # ------------------------------------------------
                        department_table = (
                            selected_department_summary[
                                [
                                    "Date Label",
                                    "部門",
                                    "Scheduled",
                                    "Absent",
                                    "Approved Leave",
                                    "Percentage",
                                    (
                                        "Percentage incl. "
                                        "Approved Leave"
                                    ),
                                ]
                            ]
                            .copy()
                            .rename(
                                columns={
                                    "Date Label": "Date",
                                    (
                                        "Percentage incl. "
                                        "Approved Leave"
                                    ): (
                                        "Rate incl. "
                                        "Approved Leave (%)"
                                    ),
                                }
                            )
                        )
    
                        department_table[
                            "Percentage"
                        ] = (
                            department_table[
                                "Percentage"
                            ]
                            .round(2)
                        )
    
                        department_table[
                            "Rate incl. Approved Leave (%)"
                        ] = (
                            department_table[
                                "Rate incl. Approved Leave (%)"
                            ]
                            .round(2)
                        )
    
                        department_table = (
                            department_table
                            .sort_values(
                                "Scheduled",
                                ascending=False,
                            )
                            .reset_index(drop=True)
                        )
    
                        st.dataframe(
                            department_table,
                            use_container_width=True,
                            hide_index=True,
                        )
                    
    # ============================================================
    # APPROVED LEAVE BY TYPE — FROM AL + OTHER LEAVE SHEETS
    # ============================================================
    with st.container(border=True):
        st.markdown(
            '<div class="dashboard-section-title">'
            'Approved Leave by Type'
            '</div>',
            unsafe_allow_html=True,
        )
    
        st.markdown(
            '<div class="dashboard-section-note">'
            'Count and percentage of leave applications recorded '
            'in the AL and Other Leave sheets.'
            '</div>',
            unsafe_allow_html=True,
        )
    
        leave_parts = []
    
        # --------------------------------------------------------
        # AL sheet
        # Every row in AL is Annual Leave
        # --------------------------------------------------------
        al_data = st.session_state.get("al_df")
    
        if isinstance(al_data, pd.DataFrame) and not al_data.empty:
            al_copy = al_data.copy()
    
            al_copy["Leave Type"] = "Annual Leave"
    
            leave_parts.append(
                al_copy
            )
    
        # --------------------------------------------------------
        # Other Leave sheet
        # Use the actual leave type from the sheet
        # --------------------------------------------------------
        other_data = st.session_state.get(
            "other_leave_df"
        )
    
        if (
            isinstance(other_data, pd.DataFrame)
            and not other_data.empty
        ):
            other_copy = other_data.copy()
    
            # Find the actual leave-type column
            if "leavetype" in other_copy.columns:
                other_copy["Leave Type"] = (
                    other_copy["leavetype"]
                )
    
            elif "Leave Type" in other_copy.columns:
                other_copy["Leave Type"] = (
                    other_copy["Leave Type"]
                )
    
            elif "reason" in other_copy.columns:
                other_copy["Leave Type"] = (
                    other_copy["reason"]
                )
    
            else:
                other_copy["Leave Type"] = (
                    "Other Leave"
                )
    
            leave_parts.append(
                other_copy
            )
    
        # --------------------------------------------------------
        # Check whether leave data exists
        # --------------------------------------------------------
        if not leave_parts:
            st.info(
                "No AL or Other Leave records are available."
            )
    
        else:
            leave_records = pd.concat(
                leave_parts,
                ignore_index=True,
                sort=False,
            )
    
            # Clean leave type names
            leave_records["Leave Type"] = (
                leave_records["Leave Type"]
                .astype(str)
                .str.replace(
                    "\n",
                    " ",
                    regex=False,
                )
                .str.replace(
                    "\u00a0",
                    " ",
                    regex=False,
                )
                .str.strip()
                .str.replace(
                    r"\s+",
                    " ",
                    regex=True,
                )
            )
    
            leave_records = leave_records[
                ~leave_records["Leave Type"].isin(
                    [
                        "",
                        "nan",
                        "None",
                        "NaT",
                    ]
                )
            ].copy()
    
            # ----------------------------------------------------
            # Remove duplicate leave applications
            # ----------------------------------------------------
            duplicate_candidates = [
                "empid",
                "工號",
                "leaveid",
                "Leave Start",
                "Leave End",
                "startdate",
                "enddate",
                "Leave Type",
            ]
    
            duplicate_columns = [
                column
                for column in duplicate_candidates
                if column in leave_records.columns
            ]
    
            if duplicate_columns:
                leave_records = (
                    leave_records
                    .drop_duplicates(
                        subset=duplicate_columns,
                        keep="first",
                    )
                    .reset_index(drop=True)
                )
    
            leave_type_mode = st.radio(
                "Leave type display",
                [
                    "Count",
                    "Percentage",
                ],
                horizontal=True,
                key="leave_type_chart_mode",
                label_visibility="collapsed",
            )
    
            # ----------------------------------------------------
            # Build summary
            # ----------------------------------------------------
            leave_type_summary = (
                leave_records
                .groupby(
                    "Leave Type",
                    dropna=False,
                )
                .size()
                .rename("Count")
                .reset_index()
            )
    
            total_leave_records = int(
                leave_type_summary["Count"].sum()
            )
    
            leave_type_summary["Percentage"] = (
                leave_type_summary["Count"]
                / total_leave_records
                * 100
            ).fillna(0)
    
            leave_type_summary = (
                leave_type_summary
                .sort_values(
                    leave_type_mode,
                    ascending=True,
                )
                .reset_index(drop=True)
            )
    
            # ----------------------------------------------------
            # Chart labels
            # ----------------------------------------------------
            if leave_type_mode == "Count":
                leave_type_summary["Label"] = (
                    leave_type_summary["Count"]
                    .map(
                        lambda value: f"{value:,}"
                    )
                )
    
                x_axis_title = (
                    "Leave applications"
                )
    
            else:
                leave_type_summary["Label"] = (
                    leave_type_summary["Percentage"]
                    .map(
                        lambda value: f"{value:.2f}%"
                    )
                )
    
                x_axis_title = (
                    "Percentage of leave applications"
                )
    
            # ----------------------------------------------------
            # Chart
            # ----------------------------------------------------
            fig_leave_type = px.bar(
                leave_type_summary,
                x=leave_type_mode,
                y="Leave Type",
                orientation="h",
                text="Label",
                custom_data=[
                    "Count",
                    "Percentage",
                ],
            )
    
            fig_leave_type.update_traces(
                marker_color="#55C6A5",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Applications: %{customdata[0]:,}<br>"
                    "Percentage: %{customdata[1]:.2f}%"
                    "<extra></extra>"
                ),
            )
    
            fig_leave_type = style_chart(
                fig_leave_type,
                height=max(
                    380,
                    len(leave_type_summary) * 45
                    + 120,
                ),
                show_legend=False,
            )
    
            fig_leave_type.update_layout(
                title_text="",
                xaxis_title=x_axis_title,
                yaxis_title="",
                margin=dict(
                    l=190,
                    r=100,
                    t=35,
                    b=70,
                ),
            )
    
            if leave_type_mode == "Percentage":
                fig_leave_type.update_xaxes(
                    ticksuffix="%",
                )
    
            st.plotly_chart(
                fig_leave_type,
                use_container_width=True,
                config={
                    "displayModeBar": True,
                    "displaylogo": False,
                },
            )
    
            # ----------------------------------------------------
            # Table
            # ----------------------------------------------------
            leave_type_table = (
                leave_type_summary[
                    [
                        "Leave Type",
                        "Count",
                        "Percentage",
                    ]
                ]
                .sort_values(
                    "Count",
                    ascending=False,
                )
                .reset_index(drop=True)
            )
    
            leave_type_table["Percentage"] = (
                leave_type_table["Percentage"]
                .round(2)
            )
    
            st.dataframe(
                leave_type_table,
                use_container_width=True,
                hide_index=True,
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
        st.info("No processed history is available yet.")
        st.stop()

    # --------------------------------------------------------
    # Convert timestamps to Taiwan time
    # --------------------------------------------------------
    def to_taiwan_time(value):
        timestamp = pd.Timestamp(value)

        if pd.isna(timestamp):
            return pd.NaT

        # Current history records created with datetime.now()
        # on Streamlit Cloud are usually naive UTC timestamps.
        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize("UTC")

        return timestamp.tz_convert("Asia/Taipei")

    # --------------------------------------------------------
    # Recover missing period dates from the saved attendance data
    # --------------------------------------------------------
    for item in st.session_state.history:
        period_start = pd.to_datetime(
            item.get("Period Start"),
            errors="coerce",
        )
        period_end = pd.to_datetime(
            item.get("Period End"),
            errors="coerce",
        )

        if pd.isna(period_start) or pd.isna(period_end):
            item_data = item.get("data")

            if (
                isinstance(item_data, pd.DataFrame)
                and not item_data.empty
            ):
                if "上段應上班時間" in item_data.columns:
                    attendance_dates = pd.to_datetime(
                        item_data["上段應上班時間"],
                        errors="coerce",
                    ).dropna()

                elif "考勤日期" in item_data.columns:
                    attendance_dates = pd.to_datetime(
                        item_data["考勤日期"],
                        errors="coerce",
                    ).dropna()

                else:
                    attendance_dates = pd.Series(
                        dtype="datetime64[ns]"
                    )

                if not attendance_dates.empty:
                    item["Period Start"] = (
                        attendance_dates.min().normalize()
                    )
                    item["Period End"] = (
                        attendance_dates.max().normalize()
                    )

    # --------------------------------------------------------
    # Build history summary table
    # --------------------------------------------------------
    history_rows = []

    for item in st.session_state.history:
        processed_at = to_taiwan_time(
            item.get("Processed At")
        )

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
                "Processed At": (
                    processed_at.strftime("%Y-%m-%d %H:%M:%S")
                    if pd.notna(processed_at)
                    else ""
                ),
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

    st.dataframe(
        history_table,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # Create labels for each processed period
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
            period_text = "Date unavailable"

        history_labels.append(
            f"{period_text} — "
            f"{item.get('Attendance File', 'Unknown file')}"
        )

    # --------------------------------------------------------
    # Selector: combine all weeks or view one week
    # --------------------------------------------------------
    view_options = [
        "Combine all processed weeks"
    ] + history_labels

    selected_label = st.selectbox(
        "Open processed result",
        view_options,
        key="history_result_selector",
    )

    # --------------------------------------------------------
    # Combine all processed weeks
    # --------------------------------------------------------
    if selected_label == "Combine all processed weeks":
        dataframes = [
            item["data"].copy()
            for item in st.session_state.history
            if (
                isinstance(item.get("data"), pd.DataFrame)
                and not item["data"].empty
            )
        ]

        if not dataframes:
            st.info("No processed attendance data is available.")
            st.stop()

        combined_history = pd.concat(
            dataframes,
            ignore_index=True,
            sort=False,
        )

        # Convert date/time columns before detecting duplicates
        if "考勤日期" in combined_history.columns:
            combined_history["考勤日期"] = pd.to_datetime(
                combined_history["考勤日期"],
                errors="coerce",
            )

        if "上段應上班時間" in combined_history.columns:
            combined_history["上段應上班時間"] = pd.to_datetime(
                combined_history["上段應上班時間"],
                errors="coerce",
            )

        # Employee + scheduled start uniquely identifies a shift.
        # If scheduled start is unavailable, use attendance date.
        if (
            "工號" in combined_history.columns
            and "上段應上班時間" in combined_history.columns
        ):
            duplicate_columns = [
                "工號",
                "上段應上班時間",
            ]

        elif (
            "工號" in combined_history.columns
            and "考勤日期" in combined_history.columns
        ):
            duplicate_columns = [
                "工號",
                "考勤日期",
            ]

        else:
            duplicate_columns = []

        if duplicate_columns:
            combined_history = (
                combined_history
                .sort_values(duplicate_columns)
                .drop_duplicates(
                    subset=duplicate_columns,
                    keep="last",
                )
                .reset_index(drop=True)
            )

        combined_status = (
            combined_history["判斷出勤after leave"]
            if "判斷出勤after leave" in combined_history.columns
            else pd.Series(dtype="object")
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card(
                "Combined rows",
                f"{len(combined_history):,}",
                "After removing duplicates",
            )

        with c2:
            metric_card(
                "Absent",
                f"{(combined_status == 'Absent').sum():,}",
            )

        with c3:
            metric_card(
                "Leave Approved",
                f"{(combined_status == 'Leave Approved').sum():,}",
            )

        with c4:
            forgot_count = combined_status.isin(
                [
                    "Forgot Clock-in",
                    "Forgot Clock-out",
                ]
            ).sum()

            metric_card(
                "Forgot Punch",
                f"{forgot_count:,}",
            )

        st.dataframe(
            combined_history,
            use_container_width=True,
            hide_index=True,
            height=520,
        )

    # --------------------------------------------------------
    # Show one selected processed week
    # --------------------------------------------------------
    else:
        selected_index = history_labels.index(
            selected_label
        )

        selected_item = st.session_state.history[
            selected_index
        ]

        selected_data = selected_item.get(
            "data",
            pd.DataFrame(),
        )

        if (
            isinstance(selected_data, pd.DataFrame)
            and not selected_data.empty
        ):
            st.dataframe(
                selected_data,
                use_container_width=True,
                hide_index=True,
                height=520,
            )
        else:
            st.info(
                "No attendance data is available "
                "for this history record."
            )

    st.caption(
        "History is stored only during the current browser session. "
        "It clears when the app restarts. Permanent history requires a database."
    )
