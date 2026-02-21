import streamlit as st
from UI import hide_sidebar
from pathlib import Path
from typing import Optional

hide_sidebar(page_title="簡易諮詢 / 了解需求")


def guard():
    if not st.session_state.get("agreed", False):
        st.switch_page("pages/00_Notice.py")
    if st.session_state.get("service_type") != "A":
        st.switch_page("pages/01_ServiceType.py")


guard()

st.title("簡易諮詢 / 了解需求")

# 讓分隔線更有間距 + 放大預算滑桿
st.markdown(
    """
<style>
hr { margin: 26px 0; }
.section-title { font-size: 18px; font-weight: 700; margin: 4px 0 10px 0; }

/* 放大 slider（預算拉桿會更明顯） */
div[data-baseweb="slider"] {
    padding-top: 20px;
    padding-bottom: 20px;
}
div[data-baseweb="slider"] > div {
    height: 12px !important;
}
div[data-baseweb="slider"] span {
    width: 26px !important;
    height: 26px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# ✅ 圖片設定（用你提供程式碼修正）
# -------------------------
# Streamlit Cloud 沒有 C:\Users\...，只用專案內相對路徑
# 你的 repo 結構：Assets/Images/ITX.jpg ... 這裡就要指到 Assets/Images
ROOT_DIR = Path(__file__).resolve().parents[1]  # pages/02_... -> 回到專案根目錄
Images_DIR = ROOT_DIR / "Assets" / "Images"

CASE_SIZE_IMAGE = {
    "Mini-ITX（小型主機）": "ITX",
    "Micro-ATX（中小型主機）": "MATX",
    "ATX（標準主機）": "ATX",
    "E-ATX（大型主機 / 工作站）": "EATX",
}

STYLE_IMAGE = {
    "簡約": "Simple",
    "靜音": "Mute",
    "海景": "Sea",
    "開放": "Open",
    "開放式": "Open",  # 兼容
}

COOLING_IMAGE = {
    "風冷（原廠風扇 / 塔式散熱）": "Fan",
    "一體式水冷（120風扇 / 240風扇 / 360風扇）": "Close_Loop",
    "分體式水冷（單迴路 / 雙迴路）": "Open_Loop",
    # 「依建議配置」不顯示圖片
}


def _find_image_path(stem: str) -> Optional[Path]:
    """
    ✅ 穩定版找圖：
    - 不依賴 glob(f"{stem}.*") 的大小寫與副檔名
    - 支援 .png/.jpg/.jpeg/.webp，並且檔名大小寫不敏感
    - 例如：stem="ITX" 可以找到 ITX.jpg / itx.JPG / ITX.jpeg ...
    """
    if not Images_DIR.exists():
        return None

    allow = {".png", ".jpg", ".jpeg", ".webp"}

    # 逐一掃描資料夾檔案，做 stem 比對（不怕大小寫）
    for p in Images_DIR.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() not in allow:
            continue
        if p.stem.lower() == stem.lower():
            return p

    return None


def show_option_image(mapping: dict, selected: str) -> None:
    """選到某選項時，在下方顯示對應圖片（找不到檔案就提示）"""
    stem = mapping.get(selected)
    if not stem:
        return

    p = _find_image_path(stem)
    if p is None:
        st.warning(
            f"找不到對應圖片：{stem}.png / .jpg / .jpeg / .webp（目前圖片資料夾：{Images_DIR}）"
        )
        return

    st.image(str(p), use_container_width=True)
    st.caption("選項圖片多為網路截圖/示意圖，僅供參考；實際外觀與規格以實際商品/實機為準。")


# -------------------------
# Options（保留你原本長文字）
# -------------------------
usage_options = [
    "文書上網（YouTube、Office）",
    "輕度遊戲（LOL、Minecraft）",
    "3A 遊戲（GTA、Assassin's Creed、Call of Duty、The Last of Us）",
    "模擬器 & 多開（BlueStacks、MuMu、Nox）",
    "直播 & 影片剪輯（OBS、Adobe、DaVinci、Pinnacle）",
    "平面設計（Adobe、AutoCAD）",
    "3D 建模（Blender、SolidWorks、Creo）",
    "工程計算（Ansys、Siemens、MSC）",
    "AI 繪圖 & 模型訓練（PyTorch、Stable Diffusion 等）",
    "其他用途 & 使用軟體",
]
OTHER_USAGE_LABEL = "其他用途 & 使用軟體"

perf_options = [
    "1080P 入門（較低預算並以效能優先）",
    "2K 主流（效能與畫質之間取得平衡）",
    "4K 高階（追求極致效能與高畫質）",
    "AI 工作站（長時間高負載運算使用）",
]

peripheral_options = ["滑鼠 & 鍵盤 & 耳機", "螢幕", "喇叭", "椅子", "桌子"]

cooling_options = [
    "風冷（原廠風扇 / 塔式散熱）",
    "一體式水冷（120風扇 / 240風扇 / 360風扇）",
    "分體式水冷（單迴路 / 雙迴路）",
    "依建議配置",
]

case_options = [
    "Mini-ITX（小型主機）",
    "Micro-ATX（中小型主機）",
    "ATX（標準主機）",
    "E-ATX（大型主機 / 工作站）",
]

style_options = ["簡約", "靜音", "海景", "開放"]

color_options = ["黑色", "白色", "其他"]
COLOR_OTHER_LABEL = "其他"

light_options = ["需要（RGB / ARGB）", "不需要", "其他"]
LIGHT_OTHER_LABEL = "其他"

other_need_options = [
    "Windows 11 正版安裝",
    "Microsoft Office 正版",
    "無線傳輸（WiFi / Bluetooth）",
    "硬碟容量需求",
]
STORAGE_NEED_LABEL = "硬碟容量需求"

# -------------------------
# Load saved values (only for branch A)
# -------------------------
saved = (
    st.session_state.get("data", {})
    if st.session_state.get("data", {}).get("branch") == "A"
    else {}
)


def ss_setdefault(key: str, value):
    if key not in st.session_state:
        st.session_state[key] = value


# 即時互動，不用 st.form
ss_setdefault("a_usage", saved.get("usage", usage_options[0]))
ss_setdefault("a_usage_other", saved.get("usage_other", ""))

ss_setdefault("a_perf", saved.get("performance", perf_options[1]))
ss_setdefault("a_budget", int(saved.get("budget", 30000)))

ss_setdefault("a_peripherals_included", saved.get("peripherals_included", "不包含"))
ss_setdefault("a_peripherals", saved.get("peripherals", []))

ss_setdefault("a_cooling", saved.get("cooling", "依建議配置"))
ss_setdefault("a_case_size", saved.get("case_size", case_options[2]))
ss_setdefault("a_style", saved.get("style", style_options[0]))

ss_setdefault("a_color", saved.get("color", "黑色"))
ss_setdefault("a_color_other", saved.get("color_other", ""))

ss_setdefault("a_lighting", saved.get("lighting", "不需要"))
ss_setdefault("a_lighting_other", saved.get("lighting_other", ""))

ss_setdefault("a_other_needs", saved.get("other_needs", []))
ss_setdefault("a_storage_need", saved.get("storage_need", ""))

# -------------------------
# UI（即時展開：不使用 st.form）
# -------------------------
st.markdown('<div class="section-title">用途與效能</div>', unsafe_allow_html=True)

st.selectbox("使用需求", usage_options, key="a_usage")
if st.session_state.a_usage == OTHER_USAGE_LABEL:
    st.text_input(
        "其他用途 / 使用軟體",
        placeholder="例如：MATLAB、Revit、Premiere、Unity、特定遊戲名稱…",
        key="a_usage_other",
    )

st.selectbox("整體效能", perf_options, key="a_perf")

st.slider("預算規劃", 0, 500_000, step=1000, key="a_budget")
st.caption(f"目前預算：NT$ {int(st.session_state.a_budget):,}")

st.divider()

st.markdown('<div class="section-title">週邊</div>', unsafe_allow_html=True)
st.selectbox("是否包含週邊", ["包含", "不包含"], key="a_peripherals_included")

if st.session_state.a_peripherals_included == "包含":
    st.multiselect("週邊項目", peripheral_options, key="a_peripherals")

st.divider()

st.markdown('<div class="section-title">散熱與外觀</div>', unsafe_allow_html=True)

# 散熱類型（選完顯示圖片）
st.selectbox("散熱類型", cooling_options, key="a_cooling")
show_option_image(COOLING_IMAGE, st.session_state.a_cooling)

# 主機尺寸（選完顯示圖片）
st.selectbox("主機尺寸", case_options, key="a_case_size")
show_option_image(CASE_SIZE_IMAGE, st.session_state.a_case_size)

# 外觀風格（選完顯示圖片）
st.selectbox("外觀風格", style_options, key="a_style")
show_option_image(STYLE_IMAGE, st.session_state.a_style)

st.selectbox("主機顏色", color_options, key="a_color")
if st.session_state.a_color == COLOR_OTHER_LABEL:
    st.text_input("顏色說明", placeholder="例如：灰色、銀色、粉色…", key="a_color_other")

st.selectbox("燈光效果", light_options, key="a_lighting")
if st.session_state.a_lighting == LIGHT_OTHER_LABEL:
    st.text_input("燈光說明", placeholder="例如：只要前風扇ARGB、主機內不要燈…", key="a_lighting_other")

st.divider()

st.markdown('<div class="section-title">其他需求</div>', unsafe_allow_html=True)

st.multiselect("其他需求", other_need_options, key="a_other_needs")
if STORAGE_NEED_LABEL in st.session_state.a_other_needs:
    st.text_input("硬碟容量需求", placeholder="例如：SSD 2TB + HDD 4TB", key="a_storage_need")

st.divider()

# -------------------------
# Buttons
# -------------------------
col1, col2 = st.columns([1, 1])

with col2:
    if st.button("繼續", type="primary"):
        if st.session_state.a_usage == OTHER_USAGE_LABEL and not st.session_state.a_usage_other.strip():
            st.error("你選擇了「其他用途 & 使用軟體」，請填寫內容。")
            st.stop()
        if st.session_state.a_color == COLOR_OTHER_LABEL and not st.session_state.a_color_other.strip():
            st.error("你選擇了「主機顏色：其他」，請填寫顏色。")
            st.stop()
        if st.session_state.a_lighting == LIGHT_OTHER_LABEL and not st.session_state.a_lighting_other.strip():
            st.error("你選擇了「燈光效果：其他」，請填寫需求。")
            st.stop()
        if STORAGE_NEED_LABEL in st.session_state.a_other_needs and not st.session_state.a_storage_need.strip():
            st.error("你勾選了「硬碟容量需求」，請填寫容量需求。")
            st.stop()

        st.session_state.data = {
            "branch": "A",
            "branch_name": "簡易諮詢 & 全新電腦組裝",
            "usage": st.session_state.a_usage,
            "usage_other": st.session_state.a_usage_other.strip(),
            "performance": st.session_state.a_perf,
            "budget": int(st.session_state.a_budget),
            "peripherals_included": st.session_state.a_peripherals_included,
            "peripherals": st.session_state.a_peripherals
            if st.session_state.a_peripherals_included == "包含"
            else [],
            "cooling": st.session_state.a_cooling,
            "case_size": st.session_state.a_case_size,
            "style": st.session_state.a_style,
            "color": st.session_state.a_color,
            "color_other": st.session_state.a_color_other.strip(),
            "lighting": st.session_state.a_lighting,
            "lighting_other": st.session_state.a_lighting_other.strip(),
            "other_needs": st.session_state.a_other_needs,
            "storage_need": st.session_state.a_storage_need.strip(),
        }

        st.switch_page("pages/05_Review.py")

with col1:
    if st.button("返回"):
        st.switch_page("pages/01_ServiceType.py")