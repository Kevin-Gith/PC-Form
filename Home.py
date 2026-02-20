import streamlit as st
from UI import hide_sidebar
from pathlib import Path

hide_sidebar(page_title="電腦組裝服務諮詢表單")

# -------------------------
# Helpers
# -------------------------
def ss_setdefault(key: str, value):
    if key not in st.session_state:
        st.session_state[key] = value


# 如果你希望每次打開都當作新客戶（清空上次資料），把下面這行打開
st.session_state.clear()

# -------------------------
# UI
# -------------------------
st.title("電腦組裝服務諮詢表單")
st.caption("歡迎閱讀簡介，點選「繼續」後進入事前須知。")

# ✅ PPT 轉圖片放這裡：Assets/Intro/01.png、02.png...
Intro_DIR = Path("Assets/Intro")
imgs = []
if Intro_DIR.exists():
    for ext in ("*.PNG", "*.JPG", "*.png", "*.jpg", "*.jpeg", "*.webp"):
        imgs += sorted(Intro_DIR.glob(ext))

if imgs:
    # 近似簡報：整頁寬顯示（每張圖視為一頁）
    st.image([str(p) for p in imgs], use_container_width=True)
else:
    st.info(
        "尚未放入簡介圖片。\n\n"
        "請將 PPT 每頁匯出成圖片（01.png、02.png…）後放到：Assets/Intro/"
    )

st.divider()

# 記錄已看過簡介（可選）
ss_setdefault("Intro_viewed", False)

col1, col2 = st.columns([1, 1])
with col2:
    if st.button("繼續", type="primary"):
        st.session_state.Intro_viewed = True
        st.switch_page("pages/00_Notice.py")