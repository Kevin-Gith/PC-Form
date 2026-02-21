import streamlit as st
from UI import hide_sidebar
import re

from sheet_writer import write_to_google_sheet  # ✅ 新增：寫入 Google Sheet

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

# ✅ 避免使用者狂按造成重複送出
if "submitting" not in st.session_state:
    st.session_state.submitting = False

saved = st.session_state.get("contact", {})

# -------------------------
# 輸入欄位
# -------------------------
name = st.text_input("姓名（必填）", value=saved.get("name", ""))
email = st.text_input("E-mail（必填）", value=saved.get("email", ""))

phone = st.text_input("手機（選填）", value=saved.get("phone", ""))
line_id = st.text_input("Line ID（選填）", value=saved.get("line_id", ""))
social = st.text_input("FB / IG（選填）", value=saved.get("social", ""))

st.divider()

# -------------------------
# Buttons
# -------------------------
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("返回", disabled=st.session_state.submitting):
        st.switch_page("pages/05_Review.py")

with col2:
    if st.button("完成", type="primary", disabled=st.session_state.submitting):

        # ---------- 驗證 ----------
        if not name.strip():
            st.error("姓名為必填。")
            st.stop()

        if not is_valid_email(email.strip()):
            st.error("E-mail 格式不正確或未填寫。")
            st.stop()

        # ---------- 儲存聯絡資訊 ----------
        st.session_state.contact = {
            "name": name.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "line_id": line_id.strip(),
            "social": social.strip(),
        }

        # ---------- 取得分支 + 表單資料 ----------
        branch = (st.session_state.get("service_type") or "").strip().upper()  # A / B / C
        data = st.session_state.get("data", {})
        contact = st.session_state.get("contact", {})

        if branch not in ("A", "B", "C"):
            st.error(f"找不到服務類型（service_type），目前值：{branch!r}。請回上一頁重新選擇。")
            st.stop()

        # ---------- 寫入 Google Sheet ----------
        st.session_state.submitting = True
        try:
            with st.spinner("資料寫入中（系統會延遲 5 秒避免同時寫入衝突）..."):
                ok, msg = write_to_google_sheet(
                    branch=branch,
                    data=data,
                    contact=contact,
                    delay_sec=5
                )

            if not ok:
                st.error(msg)
                st.session_state.submitting = False
                st.stop()

            st.success(msg)

            # ✅ 成功後才清除流程資料
            st.session_state.pop("data", None)
            st.session_state.pop("service_type", None)

            # 可選：也清掉「contact」，讓下一位客戶不帶到上一位資料
            # st.session_state.pop("contact", None)

            st.session_state.submitting = False
            st.switch_page("pages/01_ServiceType.py")

        except Exception as e:
            st.session_state.submitting = False
            st.error(f"寫入過程發生例外：{e}")
            st.stop()