import streamlit as st
from UI import hide_sidebar
from pathlib import Path

hide_sidebar(page_title="服務需求類型")

def guard():
    if not st.session_state.get("agreed", False):
        st.warning("請先同意事前須知")
        st.switch_page("pages/00_Notice.py")

guard()

st.title("請選擇本次服務需求類型")

labels = {
    "簡易諮詢 / 了解需求 (全新電腦組裝請選我)": "A",
    "電腦效能 / 容量提升（既有主機升級請選我）": "B",
    "外觀改裝 / 散熱進化（相關客製改裝請選我）": "C",
}
reverse = {v: k for k, v in labels.items()}
default_label = reverse.get(st.session_state.get("service_type"), list(labels.keys())[0])

choice = st.selectbox("需求類型", list(labels.keys()), index=list(labels.keys()).index(default_label))
st.session_state.service_type = labels[choice]

st.divider()

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("返回"):
        st.switch_page("pages/00_Notice.py")
with col2:
    if st.button("繼續", type="primary"):
        t = st.session_state.service_type
        if t == "A":
            st.switch_page("pages/02_BranchA_NewBuild.py")
        elif t == "B":
            st.switch_page("pages/03_BranchB_Upgrade.py")
        else:
            st.switch_page("pages/04_BranchC_Mod.py")
