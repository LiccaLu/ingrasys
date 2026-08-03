import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO


st.set_page_config(
    page_title="DL基本資料整理工具",
    page_icon="📄",
    layout="centered",
)

st.title("DL基本資料整理工具")
st.write(
    "上傳履歷表 Excel，系統會自動整理，完成後可下載處理後檔案。"
)

uploaded_file = st.file_uploader(
    "請上傳 Excel 檔案",
    type=["xlsx", "xls"],
)


def safe_check_columns(df, required_cols):
    missing = [
        column
        for column in required_cols
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Excel 缺少以下欄位："
            + "、".join(missing)
        )


def split_period_column(
    df,
    column_name,
    new_column_name,
):
    """
    將「開始日期 ~ 結束日期」拆成兩欄。
    如果沒有結束日期，結束欄保持空白。
    """
    position = df.columns.get_loc(column_name)

    split_data = (
        df[column_name]
        .fillna("")
        .astype(str)
        .str.split(
            r"\s*[~～]\s*",
            n=1,
            expand=True,
        )
    )

    start_values = (
        split_data[0]
        .fillna("")
        .str.strip()
    )

    if split_data.shape[1] >= 2:
        end_values = (
            split_data[1]
            .fillna("")
            .str.strip()
        )
    else:
        end_values = pd.Series(
            "",
            index=df.index,
            dtype="object",
        )

    # 防止重複插入同名欄位
    if new_column_name in df.columns:
        df[new_column_name] = end_values
    else:
        df.insert(
            position + 1,
            new_column_name,
            end_values,
        )

    df[column_name] = start_values


def process_excel(file):
    df = pd.read_excel(file)

    # 清除欄位名稱前後多餘空格
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    required_cols = [
        "開始時間",
        "性別",
        "生日",
        "婚姻狀況",
        "血型",
        "是否有原住民身分？",
        "兵歷",
        "入伍與退伍時間",
        "住宿情形",
        "學士 學業狀態",
        "專科 學業狀態",
        "高中/職 學業狀態",
        "1公司規模",
        "2公司規模",
        "3公司規模",
        "4公司規模",
        "5公司規模",
        "1服務期間",
        "2服務期間",
        "3服務期間",
        "4服務期間",
        "5服務期間",
        "存歿",
        "存歿2",
        "存歿3",
        "存歿4",
        "存歿5",
    ]

    safe_check_columns(
        df,
        required_cols,
    )

    # ========================================================
    # 填表時間
    # ========================================================
    df["開始時間"] = (
        pd.to_datetime(
            df["開始時間"],
            errors="coerce",
        )
        .dt.strftime("%Y年%m月%d日")
        .fillna("")
    )

    # ========================================================
    # 性別
    # ========================================================
    df["性別"] = np.select(
        [
            df["性別"].astype(str).str.strip() == "男",
            df["性別"].astype(str).str.strip() == "女",
        ],
        [
            "■男    □女",
            "□男    ■女",
        ],
        default="□男    □女",
    )

    # ========================================================
    # 學歷狀態
    # ========================================================
    graduate_columns = [
        "學士 學業狀態",
        "專科 學業狀態",
        "高中/職 學業狀態",
    ]

    for column in graduate_columns:
        position = df.columns.get_loc(column)

        graduate_column = f"{column}_畢業"
        completed_column = f"{column}_結業"
        unfinished_column = f"{column}_肄業"

        values = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        columns_to_add = [
            (
                graduate_column,
                np.where(
                    values == "畢業",
                    "■",
                    "□",
                ),
            ),
            (
                completed_column,
                np.where(
                    values == "結業",
                    "■",
                    "□",
                ),
            ),
            (
                unfinished_column,
                np.where(
                    values.isin(["肄業", "肆業"]),
                    "■",
                    "□",
                ),
            ),
        ]

        for offset, (
            new_column,
            new_values,
        ) in enumerate(
            columns_to_add,
            start=1,
        ):
            if new_column in df.columns:
                df[new_column] = new_values
            else:
                df.insert(
                    position + offset,
                    new_column,
                    new_values,
                )

    # ========================================================
    # 公司規模
    # ========================================================
    company_columns = [
        "1公司規模",
        "2公司規模",
        "3公司規模",
        "4公司規模",
        "5公司規模",
    ]

    company_size_map = {
        "1000人 以上": (
            "■1000人以上  □500～1000人  "
            "□100～500人  □100人以下"
        ),
        "1000人以上": (
            "■1000人以上  □500～1000人  "
            "□100～500人  □100人以下"
        ),
        "500-1000人": (
            "□1000人以上  ■500～1000人  "
            "□100～500人  □100人以下"
        ),
        "500～1000人": (
            "□1000人以上  ■500～1000人  "
            "□100～500人  □100人以下"
        ),
        "100-500人": (
            "□1000人以上  □500～1000人  "
            "■100～500人  □100人以下"
        ),
        "100～500人": (
            "□1000人以上  □500～1000人  "
            "■100～500人  □100人以下"
        ),
        "100人 以下": (
            "□1000人以上  □500～1000人  "
            "□100～500人  ■100人以下"
        ),
        "100人以下": (
            "□1000人以上  □500～1000人  "
            "□100～500人  ■100人以下"
        ),
    }

    for column in company_columns:
        cleaned_values = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df[column] = (
            cleaned_values
            .replace(company_size_map)
        )

    # ============================================================
    # 服務期間
    # ============================================================
    worktime = [
        "1服務期間",
        "2服務期間 ",
        "3服務期間 ",
        "4服務期間 ",
        "5服務期間 ",
    ]
    
    for col in worktime:
        idx2 = df.columns.get_loc(col)
    
        split = (
            df[col]
            .fillna("")
            .astype(str)
            .str.split(
                r"[~～]",
                n=1,
                expand=True,
            )
        )
    
        start_values = (
            split[0]
            .fillna("")
            .str.strip()
        )
    
        if split.shape[1] >= 2:
            end_values = (
                split[1]
                .fillna("")
                .str.strip()
            )
        else:
            end_values = pd.Series(
                "",
                index=df.index,
                dtype="object",
            )
    
        end_column = f"{col}_結束"
    
        if end_column in df.columns:
            df[end_column] = end_values
        else:
            df.insert(
                idx2 + 1,
                end_column,
                end_values,
            )
    
        df[col] = start_values

    # ========================================================
    # 生日
    # ========================================================
    birthday = pd.to_datetime(
        df["生日"],
        errors="coerce",
        format="mixed",
    )

    df["生日"] = (
        birthday
        .dt.strftime("%Y年%m月%d日")
        .fillna("")
    )

    # ========================================================
    # 婚姻狀況
    # ========================================================
    marriage_values = (
        df["婚姻狀況"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    marriage_map = {
        "已婚": "■已婚    □未婚    □離異",
        "未婚": "□已婚    ■未婚    □離異",
        "離異": "□已婚    □未婚    ■離異",
    }

    df["婚姻狀況"] = (
        marriage_values
        .map(marriage_map)
        .fillna("□已婚    □未婚    □離異")
    )

    # ========================================================
    # 血型
    # ========================================================
    blood_values = (
        df["血型"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    blood_map = {
        "A": "■A    □B    □O    □AB",
        "B": "□A    ■B    □O    □AB",
        "O": "□A    □B    ■O    □AB",
        "AB": "□A    □B    □O    ■AB",
    }

    df["血型"] = (
        blood_values
        .map(blood_map)
        .fillna("□A    □B    □O    □AB")
    )

    # ========================================================
    # 原住民身分
    # ========================================================
    indigenous_values = (
        df["是否有原住民身分？"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["是否有原住民身分？"] = np.where(
        indigenous_values.str.startswith("是"),
        "■是    □否",
        "□是    ■否",
    )

    # ========================================================
    # 兵歷
    # ========================================================
    military_values = (
        df["兵歷"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["兵歷"] = np.select(
        [
            military_values == "役畢",
            military_values == "免役",
        ],
        [
            "■役畢    □免役",
            "□役畢    ■免役",
        ],
        default="□役畢    □免役",
    )

    # ============================================================
    # 入伍與退伍時間
    # ============================================================
    col = "入伍與退伍時間"
    idx2 = df.columns.get_loc(col)
    
    split1 = (
        df[col]
        .fillna("")
        .astype(str)
        .str.split(
            r"[~～]",
            n=1,
            expand=True,
        )
    )
    
    start_values = (
        split1[0]
        .fillna("")
        .str.strip()
    )
    
    if split1.shape[1] >= 2:
        end_values = (
            split1[1]
            .fillna("")
            .str.strip()
        )
    else:
        end_values = pd.Series(
            "",
            index=df.index,
            dtype="object",
        )
    
    end_column = f"{col}_退伍"
    
    if end_column in df.columns:
        df[end_column] = end_values
    else:
        df.insert(
            idx2 + 1,
            end_column,
            end_values,
        )
    
    df[col] = start_values

    # ========================================================
    # 住宿情況
    # ========================================================
    accommodation_values = (
        df["住宿情形"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["住宿情形"] = np.select(
        [
            accommodation_values == "自宅",
            accommodation_values == "租屋",
            accommodation_values == "",
        ],
        [
            "■自宅    □租屋    □其他＿＿＿＿",
            "□自宅    ■租屋    □其他＿＿＿＿",
            "□自宅    □租屋    □其他＿＿＿＿",
        ],
        default=(
            "□自宅    □租屋    ■其他＿＿"
            + accommodation_values
            + "＿＿"
        ),
    )

    # ========================================================
    # 存歿
    # ========================================================
    live_columns = [
        "存歿",
        "存歿2",
        "存歿3",
        "存歿4",
        "存歿5",
    ]

    for column in live_columns:
        live_values = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df[column] = np.select(
            [
                live_values == "存",
                live_values == "歿",
            ],
            [
                "■存    □歿",
                "□存    ■歿",
            ],
            default="□存    □歿",
        )

    return df


if uploaded_file is not None:
    st.success("檔案上傳成功")

    if st.button(
        "開始處理",
        type="primary",
        use_container_width=True,
    ):
        try:
            result_df = process_excel(
                uploaded_file
            )

            output = BytesIO()

            result_df.to_excel(
                output,
                index=False,
                engine="openpyxl",
            )

            output.seek(0)

            st.success("處理完成")

            st.download_button(
                label="下載處理後 Excel",
                data=output.getvalue(),
                file_name="處理後履歷表.xlsx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                ),
                use_container_width=True,
            )

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                f"處理檔案時發生錯誤：{error}"
            )
