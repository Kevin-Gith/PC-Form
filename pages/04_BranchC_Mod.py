import streamlit as st
from UI import hide_sidebar
from pathlib import Path

hide_sidebar(page_title="外觀改裝 / 散熱進化")

def guard():
    if not st.session_state.get("agreed", False):
        st.switch_page("pages/00_Notice.py")
    if st.session_state.get("service_type") != "C":
        st.switch_page("pages/01_ServiceType.py")


guard()

st.title("外觀改裝 / 散熱進化")

st.markdown(
    """
<style>
hr { margin: 26px 0; }
.section-title { font-size: 18px; font-weight: 700; margin: 4px 0 10px 0; }
.spec-title { font-size: 18px; font-weight: 800; margin: 14px 0 10px 0; }

/* 放大 slider */
div[data-baseweb="slider"] { padding-top: 20px; padding-bottom: 20px; }
div[data-baseweb="slider"] > div { height: 12px !important; }
div[data-baseweb="slider"] span { width: 26px !important; height: 26px !important; }

/* 讓同列欄位更緊湊一些 */
div[data-testid="stHorizontalBlock"] { gap: 16px; }

/* 小提示文字 */
.small-muted { color: rgba(49,51,63,0.6); font-size: 14px; margin-top: -6px; }
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# Brand options (Selectbox)
# -------------------------
cpu_brand_options = ["英特爾 Intel", "超微 AMD", "其他"]

cooler_brand_options = [
    "貓頭鷹 Noctua",
    "必酷 be quiet!",
    "酷碼 Cooler Master",
    "海盜船 Corsair",
    "九州風神 DeepCool",
    "君主 Montech",
    "美洲獅 COUGAR",
    "大飛 DarkFlash",
    "威剛 XPG",
    "保銳 ENERMAX",
    "旋剛 Sharkoon",
    "恩傑 NZXT",
    "利民 Thermalright",
    "銀欣 SilverStone",
    "追風者 Phanteks",
    "全漢 FSP",
    "喬思伯 JONSBO",
    "創氪星系 TRYX",
    "ID-COOLING",
    "其他",
]

mobo_brand_options = ["華碩 ASUS", "微星 MSI", "技嘉 Gigabyte", "華擎 ASRock", "其他"]

ram_brand_options = [
    "海盜船 Corsair",
    "芝奇 G.Skill",
    "金士頓 Kingston",
    "美光 Crucial",
    "威剛 ADATA",
    "十銓 TEAMGROUP",
    "其他",
]

gpu_brand_options = [
    "華碩 ASUS",
    "微星 MSI",
    "技嘉 Gigabyte",
    "藍寶石 Sapphire",
    "撼訊 PowerColor",
    "索泰 Zotac",
    "華擎 ASRock",
    "英特爾 Intel",
    "其他",
]

psu_brand_options = [
    "華碩 ASUS",
    "微星 MSI",
    "技嘉 Gigabyte",
    "海韻 Seasonic",
    "海盜船 Corsair",
    "全漢 FSP",
    "君主 Montech",
    "酷碼 Cooler Master",
    "曜越 Thermaltake",
    "威剛 XPG",
    "聯力 Lian Li",
    "台達 Delta",
    "恩傑 NZXT",
    "振華 SuperFlower",
    "安鈦克 Antec",
    "其他",
]

hdd_brand_options = ["希捷 Seagate", "威騰 Western Digital", "東芝 Toshiba", "其他"]

ssd_brand_options = [
    "微星 MSI",
    "技嘉 Gigabyte",
    "三星 Samsung",
    "威騰 Western Digital",
    "美光 Crucial",
    "金士頓 Kingston",
    "威剛 XPG",
    "海力士 SK Hynix",
    "十銓 TEAMGROUP",
    "科賦 KLEVV",
    "其他",
]

case_brand_options = [
    "華碩 ASUS",
    "微星 MSI",
    "技嘉 Gigabyte",
    "聯力 Lian Li",
    "海盜船 Corsair",
    "恩傑 NZXT",
    "酷碼 Cooler Master",
    "追風者 Phanteks",
    "曜越 Thermaltake",
    "全漢 FSP",
    "君主 Montech",
    "威剛 XPG",
    "喬思伯 JONSBO",
    "安鈦克 Antec",
    "大飛 DarkFlash",
    "旋剛 Sharkoon",
    "銀欣 SilverStone",
    "保銳 ENERMAX",
    "迎廣 InWin",
    "其他",
]

# -------------------------
# Other options
# -------------------------
mod_item_options = [
    "更換機殼",
    "增加直立顯示卡支架",
    "增加 RGB 燈效",
    "增加副螢幕",
    "客製化分體式水冷",
    "客製化電源編織線",
    "客製化 LED 燈板",
    "客製化雷雕 / 噴繪",
    "其他",
]
OTHER_MOD_LABEL = "其他"

# Load saved (only C)
saved = st.session_state.get("data", {}) if st.session_state.get("data", {}).get("branch") == "C" else {}


def ss_setdefault(key: str, value):
    if key not in st.session_state:
        st.session_state[key] = value


# Init session state
ss_setdefault("c_cpu_brand", saved.get("cpu_brand", cpu_brand_options[0]))
ss_setdefault("c_cpu_brand_other", saved.get("cpu_brand_other", ""))
ss_setdefault("c_cpu_model", saved.get("cpu_model", ""))

ss_setdefault("c_cooler_brand", saved.get("cooler_brand", cooler_brand_options[0]))
ss_setdefault("c_cooler_brand_other", saved.get("cooler_brand_other", ""))
ss_setdefault("c_cooler_model", saved.get("cooler_model", ""))

ss_setdefault("c_mobo_brand", saved.get("mobo_brand", mobo_brand_options[0]))
ss_setdefault("c_mobo_brand_other", saved.get("mobo_brand_other", ""))
ss_setdefault("c_mobo_model", saved.get("mobo_model", ""))

ss_setdefault("c_ram_brand", saved.get("ram_brand", ram_brand_options[0]))
ss_setdefault("c_ram_brand_other", saved.get("ram_brand_other", ""))
ss_setdefault("c_ram_model", saved.get("ram_model", ""))
ss_setdefault("c_ram_capacity", saved.get("ram_capacity", ""))

ss_setdefault("c_gpu_brand", saved.get("gpu_brand", gpu_brand_options[0]))
ss_setdefault("c_gpu_brand_other", saved.get("gpu_brand_other", ""))
ss_setdefault("c_gpu_model", saved.get("gpu_model", ""))

ss_setdefault("c_psu_brand", saved.get("psu_brand", psu_brand_options[0]))
ss_setdefault("c_psu_brand_other", saved.get("psu_brand_other", ""))
ss_setdefault("c_psu_model", saved.get("psu_model", ""))
ss_setdefault("c_psu_watt", saved.get("psu_watt", ""))

ss_setdefault("c_hdd_brand", saved.get("hdd_brand", hdd_brand_options[0]))
ss_setdefault("c_hdd_brand_other", saved.get("hdd_brand_other", ""))
ss_setdefault("c_hdd_model", saved.get("hdd_model", ""))
ss_setdefault("c_hdd_qty", saved.get("hdd_qty", ""))

ss_setdefault("c_ssd_brand", saved.get("ssd_brand", ssd_brand_options[0]))
ss_setdefault("c_ssd_brand_other", saved.get("ssd_brand_other", ""))
ss_setdefault("c_ssd_model", saved.get("ssd_model", ""))
ss_setdefault("c_ssd_qty", saved.get("ssd_qty", ""))

ss_setdefault("c_case_brand", saved.get("case_brand", case_brand_options[0]))
ss_setdefault("c_case_brand_other", saved.get("case_brand_other", ""))
ss_setdefault("c_case_model", saved.get("case_model", ""))

ss_setdefault("c_mod_items", saved.get("mod_items", []))
ss_setdefault("c_mod_other", saved.get("mod_other", ""))

ss_setdefault("c_budget", int(saved.get("budget", 20000)))

# -------------------------
# ✅ 專業版型：同列規格輸入（新增 helper）
# -------------------------
def spec_block(
    title: str,
    brand_label: str,
    model_label: str,
    brand_options: list[str],
    brand_key: str,
    model_key: str,
    other_key: str,
    model_placeholder: str = "",
    extra_label: str | None = None,
    extra_key: str | None = None,
    extra_placeholder: str = "",
):
    """一個規格區塊：
    - 上方顯示 title（例如 CPU）
    - 下一列：品牌下拉 + 型號輸入 (+ 可選第三欄額外欄位)
    - 若品牌選「其他」才顯示品牌說明
    """
    st.markdown(f'<div class="spec-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">請選擇品牌並填寫型號</div>', unsafe_allow_html=True)

    if extra_label and extra_key:
        c1, c2, c3 = st.columns([1, 2, 1], vertical_alignment="bottom")
        with c1:
            st.selectbox(brand_label, brand_options, key=brand_key)
        with c2:
            st.text_input(model_label, key=model_key, placeholder=model_placeholder)
        with c3:
            st.text_input(extra_label, key=extra_key, placeholder=extra_placeholder)
    else:
        c1, c2 = st.columns([1, 2], vertical_alignment="bottom")
        with c1:
            st.selectbox(brand_label, brand_options, key=brand_key)
        with c2:
            st.text_input(model_label, key=model_key, placeholder=model_placeholder)

    if st.session_state.get(brand_key) == "其他":
        st.text_input(f"{title} 品牌說明", key=other_key, placeholder="請輸入品牌名稱")

    st.divider()


# -------------------------
# UI
# -------------------------
st.markdown('<div class="section-title">現有主機規格</div>', unsafe_allow_html=True)

spec_block(
    title="CPU",
    brand_label="品牌",
    model_label="型號",
    brand_options=cpu_brand_options,
    brand_key="c_cpu_brand",
    model_key="c_cpu_model",
    other_key="c_cpu_brand_other",
    model_placeholder="例如：i7-14700K / R7 7800X3D",
)

spec_block(
    title="散熱器",
    brand_label="品牌",
    model_label="型號",
    brand_options=cooler_brand_options,
    brand_key="c_cooler_brand",
    model_key="c_cooler_model",
    other_key="c_cooler_brand_other",
    model_placeholder="例如：NH-D15 / AK620 / 360 AIO",
)

spec_block(
    title="主機板",
    brand_label="品牌",
    model_label="型號",
    brand_options=mobo_brand_options,
    brand_key="c_mobo_brand",
    model_key="c_mobo_model",
    other_key="c_mobo_brand_other",
    model_placeholder="例如：B650 / Z790 / X670 型號",
)

spec_block(
    title="記憶體",
    brand_label="品牌",
    model_label="型號",
    brand_options=ram_brand_options,
    brand_key="c_ram_brand",
    model_key="c_ram_model",
    other_key="c_ram_brand_other",
    model_placeholder="例如：DDR5 6000 CL30",
    extra_label="容量",
    extra_key="c_ram_capacity",
    extra_placeholder="例如：32GB / 64GB",
)

spec_block(
    title="顯示卡",
    brand_label="品牌",
    model_label="型號",
    brand_options=gpu_brand_options,
    brand_key="c_gpu_brand",
    model_key="c_gpu_model",
    other_key="c_gpu_brand_other",
    model_placeholder="例如：RTX 4070 SUPER / RX 7800 XT",
)

spec_block(
    title="電源供應器",
    brand_label="品牌",
    model_label="型號",
    brand_options=psu_brand_options,
    brand_key="c_psu_brand",
    model_key="c_psu_model",
    other_key="c_psu_brand_other",
    model_placeholder="例如：RM850x / PRIME",
    extra_label="瓦數",
    extra_key="c_psu_watt",
    extra_placeholder="例如：750W / 1000W",
)

spec_block(
    title="HDD",
    brand_label="品牌",
    model_label="型號",
    brand_options=hdd_brand_options,
    brand_key="c_hdd_brand",
    model_key="c_hdd_model",
    other_key="c_hdd_brand_other",
    model_placeholder="例如：Barracuda 2TB",
    extra_label="數量",
    extra_key="c_hdd_qty",
    extra_placeholder="例如：1 / 2",
)

spec_block(
    title="SSD",
    brand_label="品牌",
    model_label="型號",
    brand_options=ssd_brand_options,
    brand_key="c_ssd_brand",
    model_key="c_ssd_model",
    other_key="c_ssd_brand_other",
    model_placeholder="例如：990 PRO 2TB / SN850X",
    extra_label="數量",
    extra_key="c_ssd_qty",
    extra_placeholder="例如：1 / 2",
)

spec_block(
    title="機殼",
    brand_label="品牌",
    model_label="型號",
    brand_options=case_brand_options,
    brand_key="c_case_brand",
    model_key="c_case_model",
    other_key="c_case_brand_other",
    model_placeholder="例如：O11 / H9 / Meshify",
)

st.markdown('<div class="section-title">改裝需求</div>', unsafe_allow_html=True)

st.multiselect("改裝項目", mod_item_options, key="c_mod_items")
if OTHER_MOD_LABEL in st.session_state.c_mod_items:
    st.text_input("其他改裝說明", key="c_mod_other")

st.slider("改裝預算", 0, 500_000, step=1000, key="c_budget")
st.caption(f"目前預算：NT$ {int(st.session_state.c_budget):,}")

st.divider()

# Buttons
col1, col2 = st.columns([1, 1])

with col2:
    if st.button("繼續", type="primary"):
        if OTHER_MOD_LABEL in st.session_state.c_mod_items and not st.session_state.c_mod_other.strip():
            st.error("你選擇了「其他」改裝項目，請填寫說明。")
            st.stop()

        def require_other(selected: str, other_text: str, label: str):
            if selected == "其他" and not other_text.strip():
                st.error(f"你選擇了「{label}：其他」，請填寫品牌說明。")
                st.stop()

        require_other(st.session_state.c_cpu_brand, st.session_state.c_cpu_brand_other, "CPU 品牌")
        require_other(st.session_state.c_cooler_brand, st.session_state.c_cooler_brand_other, "散熱器 品牌")
        require_other(st.session_state.c_mobo_brand, st.session_state.c_mobo_brand_other, "主機板 品牌")
        require_other(st.session_state.c_ram_brand, st.session_state.c_ram_brand_other, "記憶體 品牌")
        require_other(st.session_state.c_gpu_brand, st.session_state.c_gpu_brand_other, "顯示卡 品牌")
        require_other(st.session_state.c_psu_brand, st.session_state.c_psu_brand_other, "電源供應器 品牌")
        require_other(st.session_state.c_hdd_brand, st.session_state.c_hdd_brand_other, "HDD 品牌")
        require_other(st.session_state.c_ssd_brand, st.session_state.c_ssd_brand_other, "SSD 品牌")
        require_other(st.session_state.c_case_brand, st.session_state.c_case_brand_other, "機殼 品牌")

        st.session_state.data = {
            "branch": "C",
            "branch_name": "外觀 / 散熱相關改裝（客製化改裝）",

            "cpu_brand": st.session_state.c_cpu_brand,
            "cpu_brand_other": st.session_state.c_cpu_brand_other.strip(),
            "cpu_model": st.session_state.c_cpu_model.strip(),

            "cooler_brand": st.session_state.c_cooler_brand,
            "cooler_brand_other": st.session_state.c_cooler_brand_other.strip(),
            "cooler_model": st.session_state.c_cooler_model.strip(),

            "mobo_brand": st.session_state.c_mobo_brand,
            "mobo_brand_other": st.session_state.c_mobo_brand_other.strip(),
            "mobo_model": st.session_state.c_mobo_model.strip(),

            "ram_brand": st.session_state.c_ram_brand,
            "ram_brand_other": st.session_state.c_ram_brand_other.strip(),
            "ram_model": st.session_state.c_ram_model.strip(),
            "ram_capacity": st.session_state.c_ram_capacity.strip(),

            "gpu_brand": st.session_state.c_gpu_brand,
            "gpu_brand_other": st.session_state.c_gpu_brand_other.strip(),
            "gpu_model": st.session_state.c_gpu_model.strip(),

            "psu_brand": st.session_state.c_psu_brand,
            "psu_brand_other": st.session_state.c_psu_brand_other.strip(),
            "psu_model": st.session_state.c_psu_model.strip(),
            "psu_watt": st.session_state.c_psu_watt.strip(),

            "hdd_brand": st.session_state.c_hdd_brand,
            "hdd_brand_other": st.session_state.c_hdd_brand_other.strip(),
            "hdd_model": st.session_state.c_hdd_model.strip(),
            "hdd_qty": st.session_state.c_hdd_qty.strip(),

            "ssd_brand": st.session_state.c_ssd_brand,
            "ssd_brand_other": st.session_state.c_ssd_brand_other.strip(),
            "ssd_model": st.session_state.c_ssd_model.strip(),
            "ssd_qty": st.session_state.c_ssd_qty.strip(),

            "case_brand": st.session_state.c_case_brand,
            "case_brand_other": st.session_state.c_case_brand_other.strip(),
            "case_model": st.session_state.c_case_model.strip(),

            "mod_items": st.session_state.c_mod_items,
            "mod_other": st.session_state.c_mod_other.strip(),

            "budget": int(st.session_state.c_budget),
        }

        st.switch_page("pages/05_Review.py")

with col1:
    if st.button("返回"):
        st.switch_page("pages/01_ServiceType.py")