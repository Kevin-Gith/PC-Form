# UI.py
import streamlit as st

def hide_sidebar(
    page_title: str = "電腦組裝服務諮詢表單",
    page_icon: str = "🖥️",
    layout: str = "centered",
):
    """
    作用：
    1) 統一頁面設定（避免每頁各自 set_page_config）
    2) 預設收起 sidebar
    3) 用 CSS 隱藏左側 pages 導覽與左上角的展開按鈕（讓流程更像正式表單）
    """

    # 注意：每個 page 只能呼叫一次 set_page_config
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="collapsed",
    )

    # 隱藏左側 sidebar（pages 清單）＋隱藏左上角展開鈕
    st.markdown(
        """
<style>
/* Hide Streamlit sidebar (pages navigation) */
[data-testid="stSidebar"] { display: none !important; }

/* Hide the top-left hamburger button that toggles the sidebar */
[data-testid="collapsedControl"] { display: none !important; }

/* Optional: slightly tighten top padding so the layout feels cleaner */
.block-container { padding-top: 2.2rem; }
</style>
""",
        unsafe_allow_html=True,
    )