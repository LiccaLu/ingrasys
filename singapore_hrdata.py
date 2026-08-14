import io
from datetime import datetime
from typing import Optional

import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

    # Recruitment weekly report
    "recruitment_hc_df": None,

    # OT report
    "ot_df": None,

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

# ============================================================
# RECRUITMENT WEEKLY REPORT
# One uploaded Excel = one reporting week
#
# TWO DIFFERENT DL / IDL CLASSIFICATIONS ARE KEPT:
#
# 1) Weekly to Monthly Review
#    -> uses the Excel "Type" column
#
# 2) Plant Workforce / Latest Week Hiring Overview
#    -> uses "just for report" ONLY
#       IDL         -> IDL
#       Number      -> DL
#       NOT INCLUDE -> excluded
#
# Older weekly reports do NOT need "just for report".
# They can still be used in the Weekly to Monthly trend.
# ============================================================
def read_recruitment_weekly_reports(files):

    import re

    results = []

    for upload_order, file in enumerate(files):

        # ====================================================
        # 1. GET REPORT DATE FROM FILE NAME
        # ====================================================
        file_name = file.name

        match = re.search(
            r"(?<!\d)(0?[1-9]|1[0-2])[-_/ ]?([0-3]?\d)(?!\d)",
            file_name,
        )

        if not match:
            raise ValueError(
                f"{file_name}: "
                "Unable to identify the reporting date from the file name. "
                "Please include MMDD in the file name, for example "
                "'Recruitment Weekly Report0713.xlsx'."
            )

        month = int(match.group(1))
        day = int(match.group(2))
        report_year = datetime.now().year

        report_date = pd.Timestamp(
            year=report_year,
            month=month,
            day=day,
        )

        # ====================================================
        # 2. READ WORKBOOK
        # ====================================================
        excel = pd.ExcelFile(file)

        # ----------------------------------------------------
        # WEEKLY TO MONTHLY TREND
        # Uses Type column
        # ----------------------------------------------------
        file_dl = 0
        file_idl = 0

        # ----------------------------------------------------
        # PLANT WORKFORCE / LATEST WEEK
        # Uses "just for report"
        # ----------------------------------------------------
        plant_dl_last_week = 0
        plant_idl_last_week = 0

        plant_dl_this_week = 0
        plant_idl_this_week = 0

        plant_dl_pending_acceptance = 0
        plant_idl_pending_acceptance = 0

        plant_dl_pending_onboard = 0
        plant_idl_pending_onboard = 0

        plant_dl_attrition = 0
        plant_idl_attrition = 0

        has_just_for_report = False

        used_sheets = []
        plant_used_sheets = []

        # ====================================================
        # 3. CHECK EACH SHEET
        # ====================================================
        for sheet_name in excel.sheet_names:

            raw = pd.read_excel(
                file,
                sheet_name=sheet_name,
                header=None,
            )

            if raw.empty:
                continue

            search_rows = min(
                20,
                len(raw),
            )

            # =================================================
            # FIND TYPE COLUMN
            # Used ONLY for Weekly to Monthly Review
            # =================================================
            type_row = None
            type_col = None

            for row_index in range(search_rows):

                for col_index in range(raw.shape[1]):

                    value = raw.iat[
                        row_index,
                        col_index,
                    ]

                    text = (
                        str(value)
                        .replace("\n", " ")
                        .strip()
                        .lower()
                    )

                    if text == "type":
                        type_row = row_index
                        type_col = col_index
                        break

                if type_col is not None:
                    break

            # =================================================
            # FIND "JUST FOR REPORT"
            # Used ONLY for Plant Workforce / Latest Week
            # =================================================
            report_group_row = None
            report_group_col = None

            for row_index in range(search_rows):

                for col_index in range(raw.shape[1]):

                    value = raw.iat[
                        row_index,
                        col_index,
                    ]

                    text = (
                        str(value)
                        .replace("\n", " ")
                        .strip()
                        .lower()
                    )

                    if text == "just for report":
                        report_group_row = row_index
                        report_group_col = col_index
                        break

                if report_group_col is not None:
                    break

            # =================================================
            # FIND CURRENT WEEK TOTAL HC
            # Total HC (A+B-C)(4)
            # =================================================
            total_row = None
            total_col = None

            for row_index in range(search_rows):

                for col_index in range(raw.shape[1]):

                    value = raw.iat[
                        row_index,
                        col_index,
                    ]

                    text = (
                        str(value)
                        .replace("\n", "")
                        .replace(" ", "")
                        .lower()
                    )

                    if (
                        "totalhc" in text
                        and "a+b-c" in text
                    ):
                        total_row = row_index
                        total_col = col_index
                        break

                if total_col is not None:
                    break

            # Need Type + Current HC for Weekly trend.
            # If missing, this sheet is not a usable recruitment sheet.
            if (
                type_col is None
                or total_col is None
            ):
                continue

            # =================================================
            # FIND EXTRA PLANT WORKFORCE COLUMNS
            # =================================================
            last_week_hc_col = None
            last_week_hc_row = None

            pending_acceptance_col = None
            pending_onboard_col = None
            attrition_col = None

            for row_index in range(search_rows):

                for col_index in range(raw.shape[1]):

                    value = raw.iat[
                        row_index,
                        col_index,
                    ]

                    text = (
                        str(value)
                        .replace("\n", "")
                        .replace(" ", "")
                        .lower()
                    )

                    # Last Week HC = Total HC (A)
                    # Exclude Total HC (A+B-C)(4)
                    if (
                        "totalhc" in text
                        and "(a)" in text
                        and "a+b-c" not in text
                    ):
                        last_week_hc_col = col_index
                        last_week_hc_row = row_index

                    elif "pendingacceptance" in text:
                        pending_acceptance_col = col_index

                    elif any(
                        keyword in text
                        for keyword in [
                            "awaitingonboarding",
                            "awaitingonboard",
                            "pendingonboarding",
                            "pendingonboard",
                        ]
                    ):
                        pending_onboard_col = col_index

         
                    elif (
                        attrition_col is None
                        and "resign" in text
                        and "transfer" in text
                    ):
                        attrition_col = col_index

            # =================================================
            # 4. DATA START
            # =================================================
            header_rows = [
                type_row,
                total_row,
            ]

            if report_group_row is not None:
                header_rows.append(
                    report_group_row
                )

            if last_week_hc_row is not None:
                header_rows.append(
                    last_week_hc_row
                )

            data_start = (
                max(header_rows)
                + 1
            )

            # =================================================
            # 5. CURRENT WEEK HC VALUES
            # =================================================
            current_hc_values = (
                pd.to_numeric(
                    raw.iloc[
                        data_start:,
                        total_col,
                    ],
                    errors="coerce",
                )
                .fillna(0)
                .reset_index(drop=True)
            )

            # =================================================
            # 6. WEEKLY TO MONTHLY TREND
            # Classification = Type
            # =================================================
            type_values = (
                raw.iloc[
                    data_start:,
                    type_col,
                ]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.upper()
                .reset_index(drop=True)
            )

            weekly_dl_mask = (
                type_values == "DL"
            )

            weekly_idl_mask = (
                type_values == "IDL"
            )

            sheet_dl = int(
                current_hc_values[
                    weekly_dl_mask
                ].sum()
            )

            sheet_idl = int(
                current_hc_values[
                    weekly_idl_mask
                ].sum()
            )

            file_dl += sheet_dl
            file_idl += sheet_idl

            used_sheets.append(
                sheet_name
            )

            # =================================================
            # 7. PLANT WORKFORCE / LATEST WEEK
            # Classification = "just for report"
            #
            # If this older sheet has no "just for report",
            # simply skip Plant calculations.
            # Weekly trend above is still retained.
            # =================================================
            if report_group_col is None:
                continue

            has_just_for_report = True

            report_group = (
                raw.iloc[
                    data_start:,
                    report_group_col,
                ]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.upper()
                .reset_index(drop=True)
            )

            report_group = (
                report_group
                .str.replace(
                    r"\s+",
                    " ",
                    regex=True,
                )
            )

            # IDL -> IDL
            plant_idl_mask = (
                report_group == "IDL"
            )

            # NOT INCLUDE -> excluded
            not_include_mask = (
                report_group
                == "NOT INCLUDE"
            )

            # Numeric -> DL
            numeric_group = pd.to_numeric(
                report_group,
                errors="coerce",
            )

            plant_dl_mask = (
                numeric_group.notna()
                & ~not_include_mask
            )

            plant_idl_mask = (
                plant_idl_mask
                & ~not_include_mask
            )

            # -------------------------------------------------
            # This Week HC
            # Total HC (A+B-C)(4)
            # -------------------------------------------------
            plant_dl_this_week += int(
                current_hc_values[
                    plant_dl_mask
                ].sum()
            )

            plant_idl_this_week += int(
                current_hc_values[
                    plant_idl_mask
                ].sum()
            )

            # -------------------------------------------------
            # Last Week HC
            # Total HC (A)
            # -------------------------------------------------
            if last_week_hc_col is not None:

                last_week_values = (
                    pd.to_numeric(
                        raw.iloc[
                            data_start:,
                            last_week_hc_col,
                        ],
                        errors="coerce",
                    )
                    .fillna(0)
                    .reset_index(drop=True)
                )

                plant_dl_last_week += int(
                    last_week_values[
                        plant_dl_mask
                    ].sum()
                )

                plant_idl_last_week += int(
                    last_week_values[
                        plant_idl_mask
                    ].sum()
                )

            # -------------------------------------------------
            # Pending Acceptance
            # -------------------------------------------------
            if pending_acceptance_col is not None:

                pending_acceptance_values = (
                    pd.to_numeric(
                        raw.iloc[
                            data_start:,
                            pending_acceptance_col,
                        ],
                        errors="coerce",
                    )
                    .fillna(0)
                    .reset_index(drop=True)
                )

                plant_dl_pending_acceptance += int(
                    pending_acceptance_values[
                        plant_dl_mask
                    ].sum()
                )

                plant_idl_pending_acceptance += int(
                    pending_acceptance_values[
                        plant_idl_mask
                    ].sum()
                )

            # -------------------------------------------------
            # Awaiting Onboarding
            # -------------------------------------------------
            if pending_onboard_col is not None:

                pending_onboard_values = (
                    pd.to_numeric(
                        raw.iloc[
                            data_start:,
                            pending_onboard_col,
                        ],
                        errors="coerce",
                    )
                    .fillna(0)
                    .reset_index(drop=True)
                )

                plant_dl_pending_onboard += int(
                    pending_onboard_values[
                        plant_dl_mask
                    ].sum()
                )

                plant_idl_pending_onboard += int(
                    pending_onboard_values[
                        plant_idl_mask
                    ].sum()
                )

            # -------------------------------------------------
            # Attrition = Resign / Transfer (C)
            #
            # Classification:
            #   just for report = numeric -> DL
            #   just for report = IDL     -> IDL
            #   NOT INCLUDE               -> excluded
            # -------------------------------------------------
            if attrition_col is not None:
            
                attrition_values = (
                    pd.to_numeric(
                        raw.iloc[
                            data_start:,
                            attrition_col,
                        ],
                        errors="coerce",
                    )
                    .fillna(0)
                    .reset_index(drop=True)
                )
            
                # Make sure all three Series have identical length
                common_length = min(
                    len(attrition_values),
                    len(report_group),
                    len(plant_dl_mask),
                    len(plant_idl_mask),
                )
            
                attrition_values = (
                    attrition_values
                    .iloc[:common_length]
                    .reset_index(drop=True)
                )
            
                attrition_report_group = (
                    report_group
                    .iloc[:common_length]
                    .reset_index(drop=True)
                )
            
                # ---------------------------------------------
                # IDL:
                # just for report explicitly says IDL
                # ---------------------------------------------
                attrition_idl_mask = (
                    attrition_report_group
                    .eq("IDL")
                )
            
                # ---------------------------------------------
                # DL:
                # just for report is a number
                # ---------------------------------------------
                attrition_numeric_group = (
                    pd.to_numeric(
                        attrition_report_group,
                        errors="coerce",
                    )
                )
            
                attrition_dl_mask = (
                    attrition_numeric_group
                    .notna()
                )
            
                # ---------------------------------------------
                # NEVER include NOT INCLUDE
                # ---------------------------------------------
                attrition_exclude_mask = (
                    attrition_report_group
                    .str.replace(
                        r"\s+",
                        " ",
                        regex=True,
                    )
                    .eq("NOT INCLUDE")
                )
            
                attrition_dl_mask = (
                    attrition_dl_mask
                    & ~attrition_exclude_mask
                )
            
                attrition_idl_mask = (
                    attrition_idl_mask
                    & ~attrition_exclude_mask
                )
            
                # ---------------------------------------------
                # SUM
                # ---------------------------------------------
                sheet_dl_attrition = int(
                    attrition_values[
                        attrition_dl_mask
                    ].sum()
                )
            
                sheet_idl_attrition = int(
                    attrition_values[
                        attrition_idl_mask
                    ].sum()
                )
            
                plant_dl_attrition += (
                    sheet_dl_attrition
                )
            
                plant_idl_attrition += (
                    sheet_idl_attrition
                )

        # ====================================================
        # 8. VALIDATE WEEKLY TREND DATA
        #
        # Do NOT require "just for report".
        # Older reports are allowed.
        # ====================================================
        if (
            file_dl == 0
            and file_idl == 0
        ):
            raise ValueError(
                f"{file_name}: "
                "No usable DL / IDL Total HC data found for the weekly trend. "
                "Please check the Type column and "
                "Total HC (A+B-C)(4) column."
            )

        # ====================================================
        # 9. STORE ONE ROW PER UPLOADED FILE
        # ====================================================
        results.append(
            {
                "Date": report_date,

                # ============================================
                # WEEKLY TO MONTHLY TREND
                # Uses Type
                # ============================================
                "DL": file_dl,
                "IDL": file_idl,
                "Total HC": (
                    file_dl
                    + file_idl
                ),

                # ============================================
                # PLANT WORKFORCE / LATEST WEEK
                # Uses "just for report"
                # ============================================
                "Plant DL Last Week HC": (
                    plant_dl_last_week
                ),
                "Plant IDL Last Week HC": (
                    plant_idl_last_week
                ),

                "Plant DL This Week HC": (
                    plant_dl_this_week
                ),
                "Plant IDL This Week HC": (
                    plant_idl_this_week
                ),

                "Plant DL Pending Acceptance": (
                    plant_dl_pending_acceptance
                ),
                "Plant IDL Pending Acceptance": (
                    plant_idl_pending_acceptance
                ),

                "Plant DL Pending Onboard": (
                    plant_dl_pending_onboard
                ),
                "Plant IDL Pending Onboard": (
                    plant_idl_pending_onboard
                ),

                "Plant DL Attrition": (
                    plant_dl_attrition
                ),
                "Plant IDL Attrition": (
                    plant_idl_attrition
                ),

                "Has Just For Report": (
                    has_just_for_report
                ),

                "Source File": file_name,

                "Source Sheets": ", ".join(
                    used_sheets
                ),

                "Plant Source Sheets": ", ".join(
                    plant_used_sheets
                ),

                "_upload_order": upload_order,
            }
        )

    # ========================================================
    # 10. EMPTY RESULT
    # ========================================================
    if not results:

        return pd.DataFrame(
            columns=[
                "Date",

                "DL",
                "IDL",
                "Total HC",

                "Plant DL Last Week HC",
                "Plant IDL Last Week HC",

                "Plant DL This Week HC",
                "Plant IDL This Week HC",

                "Plant DL Pending Acceptance",
                "Plant IDL Pending Acceptance",

                "Plant DL Pending Onboard",
                "Plant IDL Pending Onboard",

                "Plant DL Attrition",
                "Plant IDL Attrition",

                "Has Just For Report",

                "Source File",
                "Source Sheets",
                "Plant Source Sheets",
            ]
        )

    # ========================================================
    # 11. BUILD FINAL DATAFRAME
    # ========================================================
    recruitment_df = pd.DataFrame(
        results
    )

    recruitment_df["Date"] = (
        pd.to_datetime(
            recruitment_df["Date"]
        )
    )

    # ========================================================
    # 12. SAME DATE:
    # Use latest uploaded file
    # ========================================================
    recruitment_df = (
        recruitment_df
        .sort_values(
            [
                "Date",
                "_upload_order",
            ]
        )
        .drop_duplicates(
            subset=[
                "Date"
            ],
            keep="last",
        )
        .sort_values(
            "Date"
        )
        .drop(
            columns=[
                "_upload_order"
            ]
        )
        .reset_index(
            drop=True
        )
    )

    return recruitment_df


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

    # ========================================================
    # RECRUITMENT WEEKLY REPORTS
    # ========================================================
    st.markdown(
        '<div class="section-title">'
        'RECRUITMENT WEEKLY REPORTS'
        '</div>',
        unsafe_allow_html=True,
    )

    recruitment_files = st.file_uploader(
        "Recruitment Weekly Reports",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        key="recruitment_upload",
        label_visibility="collapsed",
    )

    # --------------------------------------------------------
    # Automatically process CURRENT uploaded recruitment files
    # --------------------------------------------------------
    if recruitment_files:
    
        current_signature = tuple(
            (
                file.name,
                file.size,
            )
            for file in recruitment_files
        )
    
        previous_signature = (
            st.session_state.get(
                "recruitment_file_signature"
            )
        )
    
        if (
            current_signature
            != previous_signature
        ):
    
            try:
    
                recruitment_hc_df = (
                    read_recruitment_weekly_reports(
                        recruitment_files
                    )
                )
    
                # IMPORTANT:
                # Replace old data completely.
                # Do NOT concat with previous session data.
                st.session_state[
                    "recruitment_hc_df"
                ] = recruitment_hc_df
    
                st.session_state[
                    "recruitment_file_signature"
                ] = current_signature
    
                st.session_state.file_names[
                    "recruitment"
                ] = [
                    file.name
                    for file
                    in recruitment_files
                ]
    
                st.success(
                    f"{len(recruitment_files)} "
                    "Recruitment Weekly Report(s) loaded."
                )
    
            except Exception as exc:
    
                st.session_state[
                    "recruitment_hc_df"
                ] = None
    
                st.session_state.pop(
                    "recruitment_file_signature",
                    None,
                )
    
                st.error(
                    "Unable to read Recruitment Weekly Reports: "
                    f"{exc}"
                )
    
    else:
        # IMPORTANT:
        # If uploader is empty, remove old recruitment data
        st.session_state[
            "recruitment_hc_df"
        ] = None
    
        st.session_state.pop(
            "recruitment_file_signature",
            None,
        )
    
        st.session_state.file_names.pop(
            "recruitment",
            None,
        )
        
    # ========================================================
    # OT REPORT
    # ========================================================
    st.markdown(
        '<div class="section-title">'
        'OT REPORT'
        '</div>',
        unsafe_allow_html=True,
    )

    ot_file = st.file_uploader(
        "OT Report",
        type=["xlsx", "xls"],
        key="ot_upload",
        label_visibility="collapsed",
    )

    if ot_file is not None:

        current_ot_signature = (
            ot_file.name,
            ot_file.size,
        )

        previous_ot_signature = (
            st.session_state.get(
                "ot_file_signature"
            )
        )

        if current_ot_signature != previous_ot_signature:

            try:
                ot_excel = pd.ExcelFile(
                    ot_file
                )

                if "Data" in ot_excel.sheet_names:
                    ot_sheet = "Data"
                else:
                    ot_sheet = ot_excel.sheet_names[0]

                ot_df = pd.read_excel(
                    ot_file,
                    sheet_name=ot_sheet,
                )

                ot_df.columns = (
                    ot_df.columns
                    .astype(str)
                    .str.strip()
                )

                required_ot_columns = [
                    "Dept",
                    "Applied O/T Hrs",
                ]

                missing_ot_columns = [
                    column
                    for column in required_ot_columns
                    if column not in ot_df.columns
                ]

                if missing_ot_columns:
                    raise ValueError(
                        "OT Report is missing column(s): "
                        + ", ".join(
                            missing_ot_columns
                        )
                    )

                ot_df["Dept"] = (
                    ot_df["Dept"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                ot_df["Applied O/T Hrs"] = (
                    pd.to_numeric(
                        ot_df["Applied O/T Hrs"],
                        errors="coerce",
                    )
                    .fillna(0)
                )

                ot_df = ot_df[
                    ot_df["Dept"] != ""
                ].copy()

                st.session_state["ot_df"] = ot_df

                st.session_state[
                    "ot_file_signature"
                ] = current_ot_signature

                st.session_state.file_names[
                    "ot"
                ] = ot_file.name

                st.success(
                    "OT Report loaded."
                )

            except Exception as exc:

                st.session_state["ot_df"] = None

                st.session_state.pop(
                    "ot_file_signature",
                    None,
                )

                st.error(
                    "Unable to read OT Report: "
                    f"{exc}"
                )

    else:
        st.session_state["ot_df"] = None

        st.session_state.pop(
            "ot_file_signature",
            None,
        )

        st.session_state.file_names.pop(
            "ot",
            None,
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

### Daily Absence Rate

These charts summarize daily absence rates across the selected reporting period and distinguish between overall absence and unplanned absence.

#### Chart A – Absence Rate incl. Approved Leave
- Includes both approved leave and unplanned absences.
- Formula:

  **(Absent shifts + Approved leave) ÷ Scheduled shifts × 100**

This represents the overall workforce unavailable for scheduled work.

#### Chart B – Absence Rate excl. Approved Leave (Unplanned)
- Excludes approved leave and counts only unplanned absences.
- Formula:

  **Absent shifts ÷ Scheduled shifts × 100**

This highlights unexpected absenteeism and attendance issues.

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
    # WEEKLY TO MONTHLY REVIEW — DL & IDL
    # ============================================================
    recruitment_hc_df = (
        st.session_state.get(
            "recruitment_hc_df"
        )
    )

    if (
        isinstance(
            recruitment_hc_df,
            pd.DataFrame,
        )
        and not recruitment_hc_df.empty
    ):

        with st.container(border=True):

            st.markdown(
                '<div class="dashboard-section-title">'
                'Weekly to Monthly Review (DL & IDL)'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="dashboard-section-note">'
                'Weekly DL and IDL headcount composition '
                'from uploaded Recruitment Weekly Reports.'
                '</div>',
                unsafe_allow_html=True,
            )

            # Use all uploaded weeks.
            # If you later want only latest 5 weeks,
            # change this to .tail(5)
            hc_chart_data = (
                recruitment_hc_df
                .sort_values("Date")
                .copy()
            )

            hc_chart_data["Week"] = (
                pd.to_datetime(
                    hc_chart_data["Date"]
                )
                .dt.strftime(
                    "Wk %m/%d"
                )
            )

            # Mark newest report as Current
            if not hc_chart_data.empty:

                latest_index = (
                    hc_chart_data.index[-1]
                )

                latest_date = (
                    pd.to_datetime(
                        hc_chart_data.loc[
                            latest_index,
                            "Date"
                        ]
                    )
                )

                hc_chart_data.loc[
                    latest_index,
                    "Week"
                ] = (
                    "Current ("
                    + latest_date.strftime(
                        "%m/%d"
                    )
                    + ")"
                )

            # ----------------------------------------------------
            # Graph
            # ----------------------------------------------------
            fig_hc = go.Figure()

            # DL
            fig_hc.add_trace(
                go.Bar(
                    x=hc_chart_data["Week"],
                    y=hc_chart_data["DL"],
                    name="DL",
                    marker_color="#34738F",
                    text=hc_chart_data["DL"],
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(
                        size=16,
                        color="white",
                    ),
                    customdata=hc_chart_data[
                        [
                            "Date",
                            "Source File",
                        ]
                    ],
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "DL: %{y:,}<br>"
                        "Date: %{customdata[0]|%Y-%m-%d}<br>"
                        "Source: %{customdata[1]}"
                        "<extra></extra>"
                    ),
                )
            )

            # IDL
            fig_hc.add_trace(
                go.Bar(
                    x=hc_chart_data["Week"],
                    y=hc_chart_data["IDL"],
                    name="IDL",
                    marker_color="#ED7A3B",
                    text=hc_chart_data["IDL"],
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(
                        size=16,
                        color="white",
                    ),
                    customdata=hc_chart_data[
                        [
                            "Date",
                            "Source File",
                        ]
                    ],
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "IDL: %{y:,}<br>"
                        "Date: %{customdata[0]|%Y-%m-%d}<br>"
                        "Source: %{customdata[1]}"
                        "<extra></extra>"
                    ),
                )
            )

            # Total HC line
            fig_hc.add_trace(
                go.Scatter(
                    x=hc_chart_data["Week"],
                    y=hc_chart_data[
                        "Total HC"
                    ],
                    name="Total HC",
                    mode=(
                        "lines+markers+text"
                    ),
                    line=dict(
                        color="#243247",
                        width=4,
                    ),
                    marker=dict(
                        color="#243247",
                        size=10,
                    ),
                    text=hc_chart_data[
                        "Total HC"
                    ].map(
                        lambda value: (
                            f"{int(value):,}"
                        )
                    ),
                    textposition="top center",
                    textfont=dict(
                        size=16,
                        color="#243247",
                    ),
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Total HC: %{y:,}"
                        "<extra></extra>"
                    ),
                )
            )

            maximum_hc = (
                hc_chart_data[
                    "Total HC"
                ].max()
            )

            fig_hc.update_layout(
                title=dict(
                    text=(
                        "Weekly overview: "
                        "DL + IDL composition "
                        "(bars) vs Total HC (line)"
                    ),
                    x=0.5,
                    xanchor="center",
                    font=dict(
                        size=20,
                        color="#243247",
                    ),
                ),

                barmode="stack",
                bargap=0.60,

                height=520,

                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",

                margin=dict(
                    l=80,
                    r=60,
                    t=100,
                    b=90,
                ),

                font=dict(
                    family="Arial, sans-serif",
                    size=14,
                    color="#243247",
                ),

                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.12,
                    xanchor="center",
                    x=0.5,
                    title_text="",
                    font=dict(
                        size=14,
                    ),
                ),

                xaxis=dict(
                    title="",
                    type="category",
                    showgrid=False,
                    showline=True,
                    linecolor="#667085",
                    ticks="outside",
                    tickfont=dict(
                        size=15,
                    ),
                    automargin=True,
                ),

                yaxis=dict(
                    title=dict(
                        text="Headcount",
                        font=dict(
                            size=16,
                        ),
                    ),
                    range=[
                        0,
                        maximum_hc * 1.20,
                    ],
                    showgrid=True,
                    gridcolor="#E5E7EB",
                    zeroline=False,
                    showline=True,
                    linecolor="#667085",
                    tickfont=dict(
                        size=13,
                    ),
                    automargin=True,
                ),

                hoverlabel=dict(
                    bgcolor="#243247",
                    font_size=13,
                    font_color="white",
                    bordercolor="#243247",
                ),
            )

            st.plotly_chart(
                fig_hc,
                use_container_width=True,
                config={
                    "displayModeBar": True,
                    "displaylogo": False,
                    "toImageButtonOptions": {
                        "format": "png",
                        "filename": (
                            "Weekly_to_Monthly_"
                            "DL_IDL_Headcount"
                        ),
                        "height": 900,
                        "width": 1600,
                        "scale": 2,
                    },
                },
            )

            # ----------------------------------------------------
            # Table
            # ----------------------------------------------------
            hc_table = (
                hc_chart_data[
                    [
                        "Date",
                        "DL",
                        "IDL",
                        "Total HC",
                        "Source File",
                    ]
                ]
                .copy()
            )

            hc_table["Date"] = (
                pd.to_datetime(
                    hc_table["Date"]
                )
                .dt.strftime(
                    "%Y-%m-%d"
                )
            )

            st.dataframe(
                hc_table,
                use_container_width=True,
                hide_index=True,
            )

        # ============================================================
        # LATEST WEEK HIRING OVERVIEW
        # ============================================================
        recruitment_hc_df = st.session_state.get(
            "recruitment_hc_df"
        )
    
        if (
            isinstance(
                recruitment_hc_df,
                pd.DataFrame,
            )
            and not recruitment_hc_df.empty
            and "Has Just For Report" in recruitment_hc_df.columns
            and recruitment_hc_df[
                "Has Just For Report"
            ].fillna(False).any()
        ):
    
            # --------------------------------------------------------
            # Plant Workforce uses ONLY reports that contain
            # "just for report", then selects the latest uploaded date.
            #
            # Weekly to Monthly Review above still uses ALL uploaded
            # reports and classifies DL / IDL from the Type column.
            plant_reports = recruitment_hc_df[
                recruitment_hc_df[
                    "Has Just For Report"
                ].fillna(False)
            ].copy()

            latest_recruitment = (
                plant_reports
                .sort_values("Date")
                .iloc[-1]
            )
    
            latest_recruitment_date = pd.to_datetime(
                latest_recruitment["Date"],
                errors="coerce",
            )
    
            if pd.notna(latest_recruitment_date):
                latest_recruitment_date_text = (
                    latest_recruitment_date.strftime(
                        "%Y-%m-%d"
                    )
                )
            else:
                latest_recruitment_date_text = (
                    "Latest report"
                )
    
            latest_source_file = str(
                latest_recruitment.get(
                    "Source File",
                    "",
                )
            )
    
            # ========================================================
            # VALUES
            # ========================================================
    
            # Last week = Total HC (A)
            dl_last_week = int(
                latest_recruitment.get(
                    "Plant DL Last Week HC",
                    0,
                )
                or 0
            )
    
            idl_last_week = int(
                latest_recruitment.get(
                    "Plant IDL Last Week HC",
                    0,
                )
                or 0
            )
    
            # This week = Total HC (A+B-C)(4)
            dl_this_week = int(
                latest_recruitment.get(
                    "Plant DL This Week HC",
                    0,
                )
                or 0
            )
    
            idl_this_week = int(
                latest_recruitment.get(
                    "Plant IDL This Week HC",
                    0,
                )
                or 0
            )
    
            # Pending Acceptance
            dl_pending_acceptance = int(
                latest_recruitment.get(
                    "Plant DL Pending Acceptance",
                    0,
                )
                or 0
            )
    
            idl_pending_acceptance = int(
                latest_recruitment.get(
                    "Plant IDL Pending Acceptance",
                    0,
                )
                or 0
            )
    
            # Awaiting Onboarding
            dl_pending_onboard = int(
                latest_recruitment.get(
                    "Plant DL Pending Onboard",
                    0,
                )
                or 0
            )
    
            idl_pending_onboard = int(
                latest_recruitment.get(
                    "Plant IDL Pending Onboard",
                    0,
                )
                or 0
            )
    
            # Resign / Transfer (C)
            dl_attrition = int(
                latest_recruitment.get(
                    "Plant DL Attrition",
                    0,
                )
                or 0
            )
    
            idl_attrition = int(
                latest_recruitment.get(
                    "Plant IDL Attrition",
                    0,
                )
                or 0
            )
    
            # ========================================================
            # HIRING RATE
            #
            # (This week HC - Last week HC)
            # -------------------------------- × 100
            #          Last week HC
            # ========================================================
            dl_hiring_rate = (
                (
                    dl_this_week
                    - dl_last_week
                )
                / dl_last_week
                * 100
                if dl_last_week > 0
                else 0
            )
    
            idl_hiring_rate = (
                (
                    idl_this_week
                    - idl_last_week
                )
                / idl_last_week
                * 100
                if idl_last_week > 0
                else 0
            )
    
            # ========================================================
            # CONTAINER
            # ========================================================
            with st.container(border=True):
    
                st.markdown(
                    '<div class="dashboard-section-title">'
                    'Latest Week Hiring Overview'
                    '</div>',
                    unsafe_allow_html=True,
                )
    
                st.markdown(
                    (
                        '<div class="dashboard-section-note">'
                        'Latest uploaded Recruitment Weekly Report: '
                        f'<b>{latest_recruitment_date_text}</b>'
                        + (
                            f' — {latest_source_file}'
                            if latest_source_file
                            else ""
                        )
                        + '</div>'
                    ),
                    unsafe_allow_html=True,
                )
    
                # ====================================================
                # HIRING RATE CARDS
                # ====================================================
                rate_col1, rate_col2 = st.columns(2)
    
                with rate_col1:
                
                    dl_rate_color = (
                        "#32A852"
                        if dl_hiring_rate >= 0
                        else "#ED6A2C"
                    )
                
                    st.markdown(
                        f"""<div class="metric-card">
                <div class="metric-label">DL HIRING RATE</div>
                <div class="metric-value" style="color:{dl_rate_color};">{dl_hiring_rate:+.1f}%</div>
                <div class="metric-note">{dl_last_week:,} last week / {dl_this_week:,} this week</div>
                </div>""",
                        unsafe_allow_html=True,
                    )
                
                
                with rate_col2:
                
                    idl_rate_color = (
                        "#32A852"
                        if idl_hiring_rate >= 0
                        else "#ED6A2C"
                    )
                
                    st.markdown(
                        f"""<div class="metric-card">
                <div class="metric-label">IDL HIRING RATE</div>
                <div class="metric-value" style="color:{idl_rate_color};">{idl_hiring_rate:+.1f}%</div>
                <div class="metric-note">{idl_last_week:,} last week / {idl_this_week:,} this week</div>
                </div>""",
                        unsafe_allow_html=True,
                    )
    
                st.markdown("<br>", unsafe_allow_html=True)
    
                # ====================================================
                # GRAPHS
                # ====================================================
                graph_col1, graph_col2, graph_col3 = (
                    st.columns(3)
                )
    
                # ----------------------------------------------------
                # DL HIRING FUNNEL
                # ----------------------------------------------------
                with graph_col1:
    
                    dl_funnel_df = pd.DataFrame(
                        {
                            "Stage": [
                                "Last Week HC",
                                "This Week HC",
                                "Pending\nOnboard",
                                "Pending\nAcceptance",
                                "Attrition",
                            ],
                            "Count": [
                                dl_last_week,
                                dl_this_week,
                                dl_pending_onboard,
                                dl_pending_acceptance,
                                dl_attrition,
                            ],
                        }
                    )
    
                    fig_dl_funnel = px.bar(
                        dl_funnel_df,
                        x="Stage",
                        y="Count",
                        text="Count",
                    )
    
                    fig_dl_funnel.update_traces(
                        marker_color="#1F6885",
                        textposition="outside",
                        textfont=dict(
                            size=14,
                            color="#243247",
                        ),
                        cliponaxis=False,
                        width=0.48,
                        hovertemplate=(
                            "<b>%{x}</b><br>"
                            "Headcount: %{y:,}"
                            "<extra></extra>"
                        ),
                    )
    
                    dl_graph_max = max(
                        dl_funnel_df["Count"].max(),
                        1,
                    )
    
                    fig_dl_funnel.update_layout(
                        title=dict(
                            text="DL Hiring Funnel",
                            x=0.5,
                            xanchor="center",
                            font=dict(
                                size=18,
                                color="#243247",
                            ),
                        ),
                        height=430,
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFFFF",
                        showlegend=False,
                        margin=dict(
                            l=50,
                            r=25,
                            t=75,
                            b=85,
                        ),
                        xaxis=dict(
                            title="",
                            showgrid=False,
                            tickfont=dict(
                                size=11,
                            ),
                            automargin=True,
                        ),
                        yaxis=dict(
                            title="Headcount",
                            range=[
                                0,
                                dl_graph_max * 1.18,
                            ],
                            gridcolor="#E5E7EB",
                            zeroline=False,
                            automargin=True,
                        ),
                    )
    
                    st.plotly_chart(
                        fig_dl_funnel,
                        use_container_width=True,
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                        },
                    )
    
                # ----------------------------------------------------
                # IDL HIRING FUNNEL
                # ----------------------------------------------------
                with graph_col2:
    
                    idl_funnel_df = pd.DataFrame(
                        {
                            "Stage": [
                                "Last Week HC",
                                "This Week HC",
                                "Pending\nOnboard",
                                "Pending\nAcceptance",
                                "Attrition",
                            ],
                            "Count": [
                                idl_last_week,
                                idl_this_week,
                                idl_pending_onboard,
                                idl_pending_acceptance,
                                idl_attrition,
                            ],
                        }
                    )
    
                    fig_idl_funnel = px.bar(
                        idl_funnel_df,
                        x="Stage",
                        y="Count",
                        text="Count",
                    )
    
                    fig_idl_funnel.update_traces(
                        marker_color="#EF742C",
                        textposition="outside",
                        textfont=dict(
                            size=14,
                            color="#243247",
                        ),
                        cliponaxis=False,
                        width=0.48,
                        hovertemplate=(
                            "<b>%{x}</b><br>"
                            "Headcount: %{y:,}"
                            "<extra></extra>"
                        ),
                    )
    
                    idl_graph_max = max(
                        idl_funnel_df["Count"].max(),
                        1,
                    )
    
                    fig_idl_funnel.update_layout(
                        title=dict(
                            text="IDL Hiring Funnel",
                            x=0.5,
                            xanchor="center",
                            font=dict(
                                size=18,
                                color="#243247",
                            ),
                        ),
                        height=430,
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFFFF",
                        showlegend=False,
                        margin=dict(
                            l=50,
                            r=25,
                            t=75,
                            b=85,
                        ),
                        xaxis=dict(
                            title="",
                            showgrid=False,
                            tickfont=dict(
                                size=11,
                            ),
                            automargin=True,
                        ),
                        yaxis=dict(
                            title="Headcount",
                            range=[
                                0,
                                idl_graph_max * 1.18,
                            ],
                            gridcolor="#E5E7EB",
                            zeroline=False,
                            automargin=True,
                        ),
                    )
    
                    st.plotly_chart(
                        fig_idl_funnel,
                        use_container_width=True,
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                        },
                    )
    
                # ----------------------------------------------------
                # ATTRITION
                # ----------------------------------------------------
                with graph_col3:
    
                    attrition_df = pd.DataFrame(
                        {
                            "Type": [
                                "DL",
                                "IDL",
                            ],
                            "Count": [
                                dl_attrition,
                                idl_attrition,
                            ],
                        }
                    )
    
                    fig_attrition = px.bar(
                        attrition_df,
                        x="Type",
                        y="Count",
                        text="Count",
                    )
    
                    fig_attrition.update_traces(
                        marker_color="#A62B97",
                        textposition="outside",
                        textfont=dict(
                            size=15,
                            color="#243247",
                        ),
                        cliponaxis=False,
                        width=0.55,
                        hovertemplate=(
                            "<b>%{x}</b><br>"
                            "Attrition: %{y:,}"
                            "<extra></extra>"
                        ),
                    )
    
                    attrition_max = max(
                        attrition_df["Count"].max(),
                        1,
                    )
    
                    fig_attrition.update_layout(
                        title=dict(
                            text=(
                                "Attrition This Week "
                                "(Resign / Transfer)"
                            ),
                            x=0.5,
                            xanchor="center",
                            font=dict(
                                size=18,
                                color="#243247",
                            ),
                        ),
                        height=430,
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFFFF",
                        showlegend=False,
                        margin=dict(
                            l=50,
                            r=25,
                            t=75,
                            b=85,
                        ),
                        xaxis=dict(
                            title="",
                            showgrid=False,
                            tickfont=dict(
                                size=13,
                            ),
                        ),
                        yaxis=dict(
                            title="Headcount",
                            range=[
                                0,
                                attrition_max * 1.30,
                            ],
                            gridcolor="#E5E7EB",
                            zeroline=False,
                        ),
                    )
    
                    st.plotly_chart(
                        fig_attrition,
                        use_container_width=True,
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                        },
                    )

                # ====================================================
                # OT BY DEPARTMENT
                # ====================================================
                ot_df = st.session_state.get(
                    "ot_df"
                )

                if (
                    isinstance(
                        ot_df,
                        pd.DataFrame,
                    )
                    and not ot_df.empty
                ):

                    st.markdown(
                        "<br>",
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        '<div class="dashboard-section-title">'
                        'OT by Department'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        '<div class="dashboard-section-note">'
                        'Department overtime hours and each '
                        'department’s share of total overtime.'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    # ---------------------------------------------
                    # Department summary
                    # ---------------------------------------------
                    ot_summary = (
                        ot_df
                        .groupby(
                            "Dept",
                            as_index=False,
                        )[
                            "Applied O/T Hrs"
                        ]
                        .sum()
                        .rename(
                            columns={
                                "Applied O/T Hrs":
                                "OT Hours",
                            }
                        )
                    )

                    # Remove departments with no OT
                    ot_summary = (
                        ot_summary[
                            ot_summary[
                                "OT Hours"
                            ] > 0
                        ]
                        .copy()
                    )

                    total_ot_hours = (
                        ot_summary[
                            "OT Hours"
                        ].sum()
                    )

                    # ---------------------------------------------
                    # Ratio:
                    # Department OT / Total OT
                    # ---------------------------------------------
                    if total_ot_hours > 0:

                        ot_summary[
                            "OT Ratio"
                        ] = (
                            ot_summary[
                                "OT Hours"
                            ]
                            / total_ot_hours
                            * 100
                        )

                    else:

                        ot_summary[
                            "OT Ratio"
                        ] = 0.0

                    ot_summary = (
                        ot_summary
                        .sort_values(
                            "OT Hours",
                            ascending=False,
                        )
                        .reset_index(
                            drop=True
                        )
                    )

                    # ---------------------------------------------
                    # Build dual-axis graph
                    # ---------------------------------------------
                    fig_ot = make_subplots(
                        specs=[
                            [
                                {
                                    "secondary_y": True
                                }
                            ]
                        ]
                    )

                    # BAR — OT hours
                    fig_ot.add_trace(
                        go.Bar(
                            x=ot_summary[
                                "Dept"
                            ],
                            y=ot_summary[
                                "OT Hours"
                            ],
                            name="OT Hours",
                            marker_color="#1F6885",
                            text=[
                                f"{value:,.1f}"
                                for value
                                in ot_summary[
                                    "OT Hours"
                                ]
                            ],
                            textposition="outside",
                            textfont=dict(
                                size=14,
                                color="#243247",
                            ),
                            cliponaxis=False,
                            hovertemplate=(
                                "<b>%{x}</b><br>"
                                "OT Hours: "
                                "%{y:,.2f}"
                                "<extra></extra>"
                            ),
                        ),
                        secondary_y=False,
                    )

                    # LINE — Department share of total OT
                    fig_ot.add_trace(
                        go.Scatter(
                            x=ot_summary[
                                "Dept"
                            ],
                            y=ot_summary[
                                "OT Ratio"
                            ],
                            name="OT Ratio (%)",
                            mode=(
                                "lines+markers+text"
                            ),
                            line=dict(
                                color="#ED6A2C",
                                width=4,
                            ),
                            marker=dict(
                                color="#ED6A2C",
                                size=10,
                            ),
                            text=[
                                f"{value:.1f}%"
                                for value
                                in ot_summary[
                                    "OT Ratio"
                                ]
                            ],
                            textposition=(
                                "top center"
                            ),
                            textfont=dict(
                                size=14,
                                color="#ED6A2C",
                            ),
                            hovertemplate=(
                                "<b>%{x}</b><br>"
                                "Share of Total OT: "
                                "%{y:.2f}%"
                                "<extra></extra>"
                            ),
                        ),
                        secondary_y=True,
                    )

                    maximum_ot = max(
                        ot_summary[
                            "OT Hours"
                        ].max(),
                        1,
                    )

                    maximum_ratio = max(
                        ot_summary[
                            "OT Ratio"
                        ].max(),
                        1,
                    )

                    fig_ot.update_layout(
                        title=dict(
                            text=(
                                "OT Hours (Bars) "
                                "vs Share of Total OT (Line)"
                            ),
                            x=0.5,
                            xanchor="center",
                            font=dict(
                                size=20,
                                color="#243247",
                            ),
                        ),
                        height=500,
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFFFF",
                        bargap=0.55,
                        hovermode="x unified",
                        margin=dict(
                            l=70,
                            r=70,
                            t=85,
                            b=95,
                        ),
                        legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=-0.16,
                            xanchor="center",
                            x=0.5,
                            title_text="",
                        ),
                        xaxis=dict(
                            title="",
                            showgrid=False,
                            tickfont=dict(
                                size=13,
                            ),
                            automargin=True,
                        ),
                    )

                    fig_ot.update_yaxes(
                        title_text="OT Hours",
                        range=[
                            0,
                            maximum_ot * 1.20,
                        ],
                        gridcolor="#E5E7EB",
                        zeroline=False,
                        secondary_y=False,
                    )

                    fig_ot.update_yaxes(
                        title_text=(
                            "Share of Total OT (%)"
                        ),
                        range=[
                            0,
                            maximum_ratio * 1.20,
                        ],
                        ticksuffix="%",
                        showgrid=False,
                        zeroline=False,
                        secondary_y=True,
                    )

                    st.plotly_chart(
                        fig_ot,
                        use_container_width=True,
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                        },
                    )

                    # ---------------------------------------------
                    # Table
                    # ---------------------------------------------
                    ot_table = (
                        ot_summary.copy()
                    )

                    ot_table[
                        "OT Hours"
                    ] = (
                        ot_table[
                            "OT Hours"
                        ]
                        .round(2)
                    )

                    ot_table[
                        "OT Ratio (%)"
                    ] = (
                        ot_table[
                            "OT Ratio"
                        ]
                        .round(2)
                    )

                    ot_table = ot_table[
                        [
                            "Dept",
                            "OT Hours",
                            "OT Ratio (%)",
                        ]
                    ]

                    st.dataframe(
                        ot_table,
                        use_container_width=True,
                        hide_index=True,
                    )
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
                        tickformat="%Y-%m-%d",
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
                        tickformat="%Y-%m-%d",
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
    # ABSENCE RATE TREND BY DEPARTMENT
    # ============================================================
    with st.container(border=True):
        st.markdown(
            '<div class="dashboard-section-title">'
            'Absence Rate Trend by Department'
            '</div>',
            unsafe_allow_html=True,
        )
    
        st.markdown(
            '<div class="dashboard-section-note">'
            'Daily unplanned absence rate for each department '
            'across the selected reporting period.'
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
            # Convert scheduled clock-in into date
            # ----------------------------------------------------
            department_daily["Scheduled Start"] = pd.to_datetime(
                department_daily["上段應上班時間"],
                errors="coerce",
            )
    
            department_daily["Date"] = (
                department_daily["Scheduled Start"]
                .dt.normalize()
            )
    
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
            # Count each employee scheduled start only once
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
                    "No valid department attendance records are available."
                )
    
            else:
                # ------------------------------------------------
                # Daily summary by department
                # ------------------------------------------------
                department_trend = (
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
                    .sort_values(
                        [
                            "部門",
                            "Date",
                        ]
                    )
                )
    
                department_trend["Scheduled"] = (
                    department_trend["Scheduled"]
                    .astype(int)
                )
    
                department_trend["Absent"] = (
                    department_trend["Absent"]
                    .astype(int)
                )
    
                department_trend["Approved Leave"] = (
                    department_trend["Approved_Leave"]
                    .astype(int)
                )
    
                # Unplanned absence rate:
                # approved leave is excluded
                department_trend["Absence Rate"] = (
                    department_trend["Absent"]
                    / department_trend[
                        "Scheduled"
                    ].replace(0, pd.NA)
                    * 100
                ).fillna(0)
    
                # Optional overall rate including approved leave
                department_trend[
                    "Absence Rate incl. Approved Leave"
                ] = (
                    (
                        department_trend["Absent"]
                        + department_trend[
                            "Approved Leave"
                        ]
                    )
                    / department_trend[
                        "Scheduled"
                    ].replace(0, pd.NA)
                    * 100
                ).fillna(0)
    
                # ------------------------------------------------
                # Department selector
                # ------------------------------------------------
                available_departments = sorted(
                    department_trend["部門"]
                    .dropna()
                    .unique()
                    .tolist()
                )
    
                selected_departments = st.multiselect(
                    "Departments",
                    options=available_departments,
                    default=available_departments,
                    key="department_trend_departments",
                )
    
                department_rate_mode = st.radio(
                    "Department absence rate",
                    [
                        "Excl. Approved Leave",
                        "Incl. Approved Leave",
                    ],
                    horizontal=True,
                    key="department_rate_mode",
                    label_visibility="collapsed",
                )
    
                if not selected_departments:
                    st.info(
                        "Select at least one department."
                    )
    
                else:
                    filtered_department_trend = (
                        department_trend[
                            department_trend["部門"].isin(
                                selected_departments
                            )
                        ]
                        .copy()
                    )
    
                    if (
                        department_rate_mode
                        == "Incl. Approved Leave"
                    ):
                        y_column = (
                            "Absence Rate incl. Approved Leave"
                        )
                        chart_note = (
                            "Includes both unplanned absence "
                            "and approved leave."
                        )
                    else:
                        y_column = "Absence Rate"
                        chart_note = (
                            "Shows unplanned absence only and "
                            "excludes approved leave."
                        )
    
                    st.caption(chart_note)
    
                    # ------------------------------------------------
                    # Build line chart
                    # ------------------------------------------------
                    fig_department_trend = px.line(
                        filtered_department_trend,
                        x="Date",
                        y=y_column,
                        color="部門",
                        markers=True,
                        custom_data=[
                            "Scheduled",
                            "Absent",
                            "Approved Leave",
                            "Absence Rate",
                            (
                                "Absence Rate incl. "
                                "Approved Leave"
                            ),
                        ],
                    )
    
                    fig_department_trend.update_traces(
                        line=dict(
                            width=3,
                            shape="linear",
                        ),
                        marker=dict(
                            size=8,
                        ),
                        hovertemplate=(
                            "<b>%{fullData.name}</b><br>"
                            "Date: %{x|%Y-%m-%d}<br>"
                            "Scheduled shifts: "
                            "%{customdata[0]:,}<br>"
                            "Unplanned absent: "
                            "%{customdata[1]:,}<br>"
                            "Approved leave: "
                            "%{customdata[2]:,}<br>"
                            "Rate excl. approved leave: "
                            "%{customdata[3]:.2f}%<br>"
                            "Rate incl. approved leave: "
                            "%{customdata[4]:.2f}%"
                            "<extra></extra>"
                        ),
                    )
    
                    maximum_department_rate = (
                        filtered_department_trend[
                            y_column
                        ].max()
                    )
    
                    fig_department_trend.update_layout(
                        title=dict(
                            text=(
                                "Absence Rate Trend "
                                "by Department"
                            ),
                            x=0.5,
                            xanchor="center",
                            font=dict(
                                size=22,
                                color="#243247",
                            ),
                        ),
                        height=520,
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#FFFFFF",
                        margin=dict(
                            l=85,
                            r=50,
                            t=115,
                            b=90,
                        ),
                        font=dict(
                            family="Arial, sans-serif",
                            size=14,
                            color="#243247",
                        ),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="center",
                            x=0.5,
                            title_text="",
                            font=dict(
                                size=15,
                            ),
                        ),
                        xaxis=dict(
                            title=dict(
                                text="Date",
                                font=dict(size=17),
                            ),
                            type="date",
                            tickformat="%Y-%m-%d",
                            dtick="D1",
                            showgrid=True,
                            gridcolor="#E8ECF2",
                            showline=True,
                            linecolor="#222222",
                            ticks="outside",
                            tickfont=dict(
                                size=14,
                            ),
                            automargin=True,
                        ),
                        yaxis=dict(
                            title=dict(
                                text="Absence Rate (%)",
                                font=dict(size=17),
                            ),
                            range=[
                                0,
                                max(
                                    5,
                                    maximum_department_rate
                                    * 1.18,
                                ),
                            ],
                            ticksuffix="%",
                            tickformat=".0f",
                            showgrid=True,
                            gridcolor="#E8ECF2",
                            zeroline=False,
                            showline=True,
                            linecolor="#222222",
                            ticks="outside",
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
                        fig_department_trend,
                        use_container_width=True,
                        config={
                            "displayModeBar": True,
                            "displaylogo": False,
                            "toImageButtonOptions": {
                                "format": "png",
                                "filename": (
                                    "Absence_Rate_Trend_"
                                    "by_Department"
                                ),
                                "height": 1000,
                                "width": 1800,
                                "scale": 2,
                            },
                        },
                    )
    
                    # ------------------------------------------------
                    # Table
                    # ------------------------------------------------
                    department_trend_table = (
                        filtered_department_trend[
                            [
                                "Date",
                                "部門",
                                "Scheduled",
                                "Absent",
                                "Approved Leave",
                                "Absence Rate",
                                (
                                    "Absence Rate incl. "
                                    "Approved Leave"
                                ),
                            ]
                        ]
                        .copy()
                    )
    
                    department_trend_table[
                        "Date"
                    ] = (
                        pd.to_datetime(
                            department_trend_table["Date"]
                        )
                        .dt.strftime("%Y-%m-%d")
                    )
    
                    department_trend_table[
                        "Absence Rate"
                    ] = (
                        department_trend_table[
                            "Absence Rate"
                        ]
                        .round(2)
                    )
    
                    department_trend_table[
                        "Absence Rate incl. Approved Leave"
                    ] = (
                        department_trend_table[
                            "Absence Rate incl. Approved Leave"
                        ]
                        .round(2)
                    )
    
                    department_trend_table = (
                        department_trend_table
                        .sort_values(
                            [
                                "Date",
                                "部門",
                            ]
                        )
                        .reset_index(drop=True)
                    )
    
                    st.dataframe(
                        department_trend_table,
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
