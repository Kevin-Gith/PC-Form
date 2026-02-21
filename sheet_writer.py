# sheet_writer.py
from __future__ import annotations

import json
import time
from typing import Dict, Any, Tuple, Optional

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ✅ 你的 Google Sheet 名稱（Google Drive 裡看到的試算表名稱）
SPREADSHEET_NAME = "PC_From"

# ✅ 分頁名稱對應（請確認你的試算表分頁真的叫這些）
WORKSHEET_BY_BRANCH = {
    "A": "Page_A",
    "B": "Page_B",
    "C": "Page_C",
}


# ----------------------------
# Secrets / Auth
# ----------------------------
def _load_sa_info_from_secrets() -> Dict[str, Any]:
    """
    從 Streamlit secrets 讀取 service account：
    - 支援兩種格式：
      1) st.secrets["gcp_service_account"] 是「JSON字串」(推薦)
      2) st.secrets["gcp_service_account"] 是「TOML dict」([gcp_service_account] ...)
    並修正 private_key 換行格式。
    """
    if "gcp_service_account" not in st.secrets:
        raise KeyError(
            "st.secrets 找不到 key 'gcp_service_account'。\n"
            "請到 Streamlit Cloud -> App settings -> Secrets 設定。\n"
            "推薦用：gcp_service_account = \"\"\"{...整份JSON...}\"\"\""
        )

    raw = st.secrets["gcp_service_account"]

    # ✅ 情況 1：Secrets 是 JSON 字串
    if isinstance(raw, str):
        try:
            sa = json.loads(raw)
        except Exception as e:
            raise ValueError(f"gcp_service_account 是字串，但不是合法 JSON：{e}")

    # ✅ 情況 2：Secrets 是 TOML dict
    elif isinstance(raw, dict):
        sa = dict(raw)

    else:
        raise TypeError(f"不支援的 secrets 型態：{type(raw)}")

    # ✅ 修正 private_key：把 '\\n' 轉為真正換行
    pk = (sa.get("private_key") or "").strip()
    pk = pk.replace("\\n", "\n").replace("\r\n", "\n").replace("\r", "\n").strip()

    if "BEGIN PRIVATE KEY" not in pk or "END PRIVATE KEY" not in pk:
        raise ValueError(
            "private_key 看起來不是有效 PEM。\n"
            "請確認 secrets 的 private_key 是完整的：\n"
            "-----BEGIN PRIVATE KEY----- ... -----END PRIVATE KEY-----"
        )

    sa["private_key"] = pk
    return sa


@st.cache_resource(show_spinner=False)
def _get_gspread_client() -> gspread.Client:
    """
    建立並快取 gspread client（避免每次寫入都重新驗證）。
    """
    sa = _load_sa_info_from_secrets()
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(sa, scopes=scopes)
    return gspread.authorize(creds)


def _open_worksheet(branch: str) -> gspread.Worksheet:
    """
    依 branch 取得 worksheet
    """
    branch = (branch or "").upper().strip()
    ws_name = WORKSHEET_BY_BRANCH.get(branch)
    if not ws_name:
        raise ValueError(f"找不到分頁設定：branch={branch}")

    gc = _get_gspread_client()
    sh = gc.open(SPREADSHEET_NAME)
    return sh.worksheet(ws_name)


# ----------------------------
# Payload mapping
# ----------------------------
def _format_note_A(data: Dict[str, Any]) -> str:
    other_needs = data.get("other_needs", []) or []
    storage_need = (data.get("storage_need") or "").strip()

    parts = []
    if other_needs:
        parts.append("、".join(other_needs))
    if storage_need:
        parts.append(f"硬碟容量需求：{storage_need}")

    return " / ".join([p for p in parts if p])


def _map_payload(branch: str, data: Dict[str, Any], contact: Dict[str, Any]) -> Dict[str, Any]:
    """
    將 data + contact 轉成要寫入 sheet 的欄位 dict
    欄位 key 必須對得上你 Google Sheet 的表頭（第一列 headers）
    """
    branch = (branch or "").upper().strip()
    if branch not in ("A", "B", "C"):
        raise ValueError(f"未知分支 branch={branch}")

    common = {
        "name": contact.get("name", ""),
        "email": contact.get("email", ""),
        "phone": contact.get("phone", ""),
        "line": contact.get("line_id", ""),
        "social": contact.get("social", ""),
    }

    if branch == "A":
        return {
            "demand": data.get("usage", ""),
            "efficacy": data.get("performance", ""),
            "budget": data.get("budget", ""),
            "periphery": data.get("peripherals_included", ""),
            "peri_item": ", ".join(data.get("peripherals", []) or []),
            "cool": data.get("cooling", ""),
            "size": data.get("case_size", ""),
            "style": data.get("style", ""),
            "color": data.get("color_other", "") if data.get("color") == "其他" else data.get("color", ""),
            "rgb": data.get("lighting_other", "") if data.get("lighting") == "其他" else data.get("lighting", ""),
            "note": _format_note_A(data),
            **common,
        }

    if branch == "B":
        return {
            "cpu_model": data.get("cpu_model", ""),
            "cooler_model": data.get("cooler_model", ""),
            "mb_model": data.get("mobo_model", ""),
            "ram_model": data.get("ram_model", ""),
            "ram_size": data.get("ram_capacity", ""),
            "gpu_model": data.get("gpu_model", ""),
            "psu_model": data.get("psu_model", ""),
            "psu_wattage": data.get("psu_watt", ""),
            "hdd_model": data.get("hdd_model", ""),
            "hdd_qty": data.get("hdd_qty", ""),
            "ssd_model": data.get("ssd_model", ""),
            "ssd_qty": data.get("ssd_qty", ""),
            "case_model": data.get("case_model", ""),
            "upg_item": ", ".join(data.get("upgrade_targets", []) or []),
            "upg_note": data.get("upgrade_targets_other", ""),
            "upg_budget": data.get("budget", ""),
            "data_mig": data.get("migrate", ""),
            **common,
        }

    # branch == "C"
    return {
        "cpu_model": data.get("cpu_model", ""),
        "cooler_model": data.get("cooler_model", ""),
        "mb_model": data.get("mobo_model", ""),
        "ram_model": data.get("ram_model", ""),
        "ram_size": data.get("ram_capacity", ""),
        "gpu_model": data.get("gpu_model", ""),
        "psu_model": data.get("psu_model", ""),
        "psu_wattage": data.get("psu_watt", ""),
        "hdd_model": data.get("hdd_model", ""),
        "hdd_qty": data.get("hdd_qty", ""),
        "ssd_model": data.get("ssd_model", ""),
        "ssd_qty": data.get("ssd_qty", ""),
        "case_model": data.get("case_model", ""),
        "mod_item": ", ".join(data.get("mod_items", []) or []),
        "mod_note": data.get("mod_other", ""),
        "mod_budget": data.get("budget", ""),
        **common,
    }


# ----------------------------
# Write
# ----------------------------
def _append_by_headers(ws: gspread.Worksheet, payload: Dict[str, Any]) -> None:
    """
    依照 worksheet 第一列表頭順序 append 一行
    """
    headers = ws.row_values(1)
    if not headers:
        raise ValueError(f"分頁 {ws.title} 第一列沒有表頭（header）。請先建立欄位名稱。")

    row = [payload.get(h, "") for h in headers]
    ws.append_row(row, value_input_option="USER_ENTERED")


def write_to_google_sheet(
    branch: str,
    data: Dict[str, Any],
    contact: Dict[str, Any],
    delay_sec: int = 0,
) -> Tuple[bool, str]:
    """
    ✅ 寫入指定分頁（Page_A / Page_B / Page_C）
    - delay_sec：可選延遲（避免你想要的「連點送出」）
    """
    try:
        if delay_sec and delay_sec > 0:
            time.sleep(delay_sec)

        payload = _map_payload(branch, data, contact)
        ws = _open_worksheet(branch)

        _append_by_headers(ws, payload)
        return True, "已寫入 Google Sheet"

    except gspread.exceptions.APIError as e:
        # 常見：403 沒分享、404 找不到試算表/分頁、quota
        return False, f"寫入 Google Sheet 失敗（APIError）：{e}"

    except Exception as e:
        return False, f"寫入 Google Sheet 失敗：{e}"


# ----------------------------
# Optional: quick self-test in app
# ----------------------------
def self_test(branch: str = "A") -> Tuple[bool, str]:
    """
    可在 app 啟動時呼叫，用來測試連線是否成功（不寫入）
    """
    try:
        ws = _open_worksheet(branch)
        _ = ws.title  # 讀取標題確認可存取
        return True, f"連線成功：{SPREADSHEET_NAME} / {ws.title}"
    except Exception as e:
        return False, f"連線測試失敗：{e}"