# python/sheet_writer.py
from __future__ import annotations

import time
from typing import Any, Dict, List

import gspread
from google.oauth2.service_account import Credentials


SPREADSHEET_NAME = "PC_From"

# 你指定的分頁名稱
SHEET_BY_BRANCH = {
    "A": "Page_A",
    "B": "Page_B",
    "C": "Page_C",
}

# ✅ Page_A：欄位(試算表標題) -> key
COLUMNS_A = [
    ("使用需求", "demand"),
    ("整體效能", "efficacy"),
    ("預算規劃", "budget"),
    ("週邊", "periphery"),
    ("週邊項目", "peri_item"),
    ("散熱類型", "cool"),
    ("主機尺寸", "size"),
    ("外觀風格", "style"),
    ("主機顏色", "color"),
    ("燈光效果", "rgb"),
    ("其他需求", "note"),
    ("姓名", "name"),
    ("E-mail", "email"),
    ("手機", "phone"),
    ("Line ID", "line"),
    ("FB / IG", "social"),
]

# ✅ Page_B：欄位 -> key
COLUMNS_B = [
    ("CPU型號", "cpu_model"),
    ("散熱器型號", "cooler_model"),
    ("主機板型號", "mb_model"),
    ("記憶體型號", "ram_model"),
    ("記憶體容量", "ram_size"),
    ("顯示卡型號", "gpu_model"),
    ("電源供應器型號", "psu_model"),
    ("電源供應器瓦數", "psu_wattage"),
    ("HDD型號", "hdd_model"),
    ("HDD數量", "hdd_qty"),
    ("SSD型號", "ssd_model"),
    ("SSD數量", "ssd_qty"),
    ("機殼型號", "case_model"),
    ("升級項目", "upg_item"),
    ("其他升級說明", "upg_note"),
    ("升級預算", "upg_budget"),
    ("資料轉移", "data_mig"),
    ("姓名", "name"),
    ("E-mail", "email"),
    ("手機", "phone"),
    ("Line ID", "line"),
    ("FB / IG", "social"),
]

# ✅ Page_C：欄位 -> key
COLUMNS_C = [
    ("CPU型號", "cpu_model"),
    ("散熱器型號", "cooler_model"),
    ("主機板型號", "mb_model"),
    ("記憶體型號", "ram_model"),
    ("記憶體容量", "ram_size"),
    ("顯示卡型號", "gpu_model"),
    ("電源供應器型號", "psu_model"),
    ("電源供應器瓦數", "psu_wattage"),
    ("HDD型號", "hdd_model"),
    ("HDD數量", "hdd_qty"),
    ("SSD型號", "ssd_model"),
    ("SSD數量", "ssd_qty"),
    ("機殼型號", "case_model"),
    ("改裝項目", "mod_item"),
    ("其他改裝說明", "mod_note"),
    ("改裝預算", "mod_budget"),
    ("姓名", "name"),
    ("E-mail", "email"),
    ("手機", "phone"),
    ("Line ID", "line"),
    ("FB / IG", "social"),
]

COLUMNS_BY_BRANCH = {"A": COLUMNS_A, "B": COLUMNS_B, "C": COLUMNS_C}


def _normalize_value(v: Any) -> str:
    """把 list / None / 其他型態統一成寫入 sheet 的字串。"""
    if v is None:
        return ""
    if isinstance(v, list):
        # 多選內容建議用「、」串起來
        return "、".join([str(x) for x in v if str(x).strip()])
    return str(v).strip()


def build_row(branch: str, payload: Dict[str, Any]) -> List[str]:
    """依照分頁欄位順序，把 payload 轉成一列 row。"""
    cols = COLUMNS_BY_BRANCH[branch]
    return [_normalize_value(payload.get(key)) for _, key in cols]


def ensure_header(ws, branch: str) -> None:
    """
    可選：確保第一列是正確標題（沒有就補上）
    如果你已經手動在 Sheet 做好標題，可以不呼叫這個。
    """
    cols = COLUMNS_BY_BRANCH[branch]
    header = [title for title, _ in cols]
    existing = ws.row_values(1)
    if existing != header:
        # 如果你不想覆蓋原本的第一列，改成只在空白時寫入
        if len(existing) == 0:
            ws.append_row(header, value_input_option="RAW")


def get_gspread_client(service_account_info: Dict[str, Any]) -> gspread.Client:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    return gspread.authorize(creds)


def append_to_sheet(
    *,
    service_account_info: Dict[str, Any],
    branch: str,
    payload: Dict[str, Any],
    sleep_seconds: int = 5,  # ✅ 你指定的 5 秒
) -> None:
    """
    寫入流程：
    1) 依 branch 找到 Page_A/B/C
    2) 等待 5 秒
    3) append row（寫到新的一列）
    """
    if branch not in ("A", "B", "C"):
        raise ValueError("branch 必須是 A / B / C")

    # 你指定：先等 5 秒避免擠在同一行（append 本身基本不會同一行，但照做）
    if sleep_seconds and sleep_seconds > 0:
        time.sleep(sleep_seconds)

    client = get_gspread_client(service_account_info)
    sh = client.open(SPREADSHEET_NAME)
    ws = sh.worksheet(SHEET_BY_BRANCH[branch])

    # 可選：確保 header（可移除）
    ensure_header(ws, branch)

    row = build_row(branch, payload)
    ws.append_row(row, value_input_option="RAW")