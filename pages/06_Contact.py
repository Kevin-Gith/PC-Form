import streamlit as st
from UI import hide_sidebar
from pathlib import Path
import re

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

        # 清除流程資料（回到服務類型）
        st.session_state.pop("data", None)
        st.session_state.pop("service_type", None)

        st.switch_page("pages/01_ServiceType.py")
