import re
import streamlit as st
from UI import hide_sidebar

from sheet_writer import append_to_sheet  # ✅ 新增：寫入 Google Sheet

hide_sidebar(page_title="聯絡資訊")


def is_valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or "") is not None


def guard():
    if not st.session_state.get("agreed", False):
        st.switch_page("pages/00_Notice.py")
    if not st.session_state.get("data"):
        st.switch_page("pages/05_Review.py")


guard()

st.title("聯絡資訊")

saved = st.session_state.get("contact", {})

# -------------------------
# 輸入欄位（不用 form）
# -------------------------
name = st.text_input("姓名（必填）", value=saved.get("name", ""))
email = st.text_input("E-mail（必填）", value=saved.get("email", ""))

phone = st.text_input("手機（選填）", value=saved.get("phone", ""))
line_id = st.text_input("Line ID（選填）", value=saved.get("line_id", ""))
social = st.text_input("FB / IG（選填）", value=saved.get("social", ""))

st.divider()


def make_payload_for_sheet(branch: str, data: dict, contact: dict) -> dict:
    """
    把你目前 session_state.data / contact 轉成你指定的 Sheet key（demand/efficacy/...）
    """
    data = data or {}
    contact = contact or {}

    # ---------- A ----------
    if branch == "A":
        # note：你 A 頁的 data key 是 usage/performance/...（這裡做轉換）
        # 顏色/燈光若是「其他」就用 xxx_other
        color = data.get("color")
        if color == "其他":
            color = data.get("color_other")

        rgb = data.get("lighting")
        if rgb == "其他":
            rgb = data.get("lighting_other")

        return {
            "demand": data.get("usage"),
            "efficacy": data.get("performance"),
            "budget": data.get("budget"),
            "periphery": data.get("peripherals_included"),
            "peri_item": data.get("peripherals"),
            "cool": data.get("cooling"),
            "size": data.get("case_size"),
            "style": data.get("style"),
            "color": color,
            "rgb": rgb,
            "note": data.get("other_needs"),
            "name": contact.get("name"),
            "email": contact.get("email"),
            "phone": contact.get("phone"),
            "line": contact.get("line_id"),
            "social": contact.get("social"),
        }

    # ---------- B ----------
    if branch == "B":
        return {
            "cpu_model": data.get("cpu_model"),
            "cooler_model": data.get("cooler_model"),
            "mb_model": data.get("mobo_model"),
            "ram_model": data.get("ram_model"),
            "ram_size": data.get("ram_capacity"),
            "gpu_model": data.get("gpu_model"),
            "psu_model": data.get("psu_model"),
            "psu_wattage": data.get("psu_watt"),
            "hdd_model": data.get("hdd_model"),
            "hdd_qty": data.get("hdd_qty"),
            "ssd_model": data.get("ssd_model"),
            "ssd_qty": data.get("ssd_qty"),
            "case_model": data.get("case_model"),
            "upg_item": data.get("upgrade_targets"),
            "upg_note": data.get("upgrade_targets_other"),
            "upg_budget": data.get("budget"),
            "data_mig": data.get("migrate"),
            "name": contact.get("name"),
            "email": contact.get("email"),
            "phone": contact.get("phone"),
            "line": contact.get("line_id"),
            "social": contact.get("social"),
        }

    # ---------- C ----------
    # 你的 C 頁資料：mod_items / mod_other / budget
    return {
        "cpu_model": data.get("cpu_model"),
        "cooler_model": data.get("cooler_model"),
        "mb_model": data.get("mobo_model"),
        "ram_model": data.get("ram_model"),
        "ram_size": data.get("ram_capacity"),
        "gpu_model": data.get("gpu_model"),
        "psu_model": data.get("psu_model"),
        "psu_wattage": data.get("psu_watt"),
        "hdd_model": data.get("hdd_model"),
        "hdd_qty": data.get("hdd_qty"),
        "ssd_model": data.get("ssd_model"),
        "ssd_qty": data.get("ssd_qty"),
        "case_model": data.get("case_model"),
        "mod_item": data.get("mod_items"),
        "mod_note": data.get("mod_other"),
        "mod_budget": data.get("budget"),
        "name": contact.get("name"),
        "email": contact.get("email"),
        "phone": contact.get("phone"),
        "line": contact.get("line_id"),
        "social": contact.get("social"),
    }


# -------------------------
# 按鈕列（左右各一顆）
# -------------------------
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("返回"):
        st.switch_page("pages/05_Review.py")

with col2:
    if st.button("完成", type="primary"):
        # 驗證
        if not name.strip():
            st.error("姓名為必填。")
            st.stop()

        if not is_valid_email(email.strip()):
            st.error("E-mail 格式不正確或未填寫。")
            st.stop()

        # 儲存聯絡資訊
        st.session_state.contact = {
            "name": name.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "line_id": line_id.strip(),
            "social": social.strip(),
        }

        # ✅ 寫入 Google Sheet（依 A/B/C 分頁）
        branch = st.session_state.get("service_type")  # "A" / "B" / "C"
        data = st.session_state.get("data", {})
        contact = st.session_state.get("contact", {})

        if branch not in ("A", "B", "C"):
            st.error("找不到 service_type（A/B/C），請回上一頁重新選擇。")
            st.stop()

        payload = make_payload_for_sheet(branch, data, contact)

        try:
            append_to_sheet(
                service_account_info=st.secrets["gcp_service_account"],
                branch=branch,
                payload=payload,
                sleep_seconds=5,  # ✅ 你指定等待 5 秒
            )
        except Exception as e:
            st.error(f"寫入 Google Sheet 失敗：{e}")
            st.stop()

        st.success("已送出，謝謝！")

        # 清除流程資料（回到服務類型）
        st.session_state.pop("data", None)
        st.session_state.pop("service_type", None)

        st.switch_page("pages/01_ServiceType.py")