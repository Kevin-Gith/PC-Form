import streamlit as st
from UI import hide_sidebar
from pathlib import Path

hide_sidebar(page_title="分支B｜效能 / 容量提升")

def guard():
    if not st.session_state.get("agreed", False):
        st.switch_page("pages/00_Notice.py")
    if not st.session_state.get("service_type"):
        st.switch_page("pages/01_ServiceType.py")
    if not st.session_state.get("data"):
        t = st.session_state.get("service_type")
        if t == "A":
            st.switch_page("pages/02_BranchA_NewBuild.py")
        elif t == "B":
            st.switch_page("pages/03_BranchB_Upgrade.py")
        else:
            st.switch_page("pages/04_BranchC_Mod.py")


guard()

data = st.session_state.get("data", {})
branch = data.get("branch", st.session_state.get("service_type", ""))
branch_name = data.get("branch_name", "")

# -------------------------
# Style：統一對齊、間距、字級
# -------------------------
st.markdown(
    """
<style>
/* 讓整體更乾淨 */
.block-container { padding-top: 2.2rem; }

/* 統一各 section title 的間距 */
h2, h3 { margin-bottom: .2rem !important; }
hr { margin: 18px 0 !important; }

/* key/value 對齊 */
.kv-label { font-weight: 800; font-size: 16px; }
.kv-value { font-size: 16px; }

/* spec 區塊 */
.spec-title { font-weight: 900; font-size: 18px; margin-top: 12px; }
.spec-head  { color: rgba(49,51,63,.55); font-size: 13px; margin-bottom: 6px; }
.spec-val   { font-size: 16px; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("確認填寫資訊")
st.caption("如需修改請點選「返回」回到上一頁重新填寫，確認無誤後點選「繼續」。")

# -------------------------
# Helpers
# -------------------------
def is_blank(x) -> bool:
    if x is None:
        return True
    if isinstance(x, str) and x.strip() == "":
        return True
    if isinstance(x, (int, float)) and x == 0:
        return True
    if isinstance(x, list) and len(x) == 0:
        return True
    return False


def v(x) -> str:
    """空值顯示 —；list 用 、 連接；數字 0 視為空"""
    if is_blank(x):
        return "—"
    if isinstance(x, str):
        return x.strip() if x.strip() else "—"
    if isinstance(x, list):
        items = [str(i).strip() for i in x if str(i).strip()]
        return "、".join(items) if items else "—"
    if isinstance(x, (int, float)):
        return f"{int(x):,}"
    return str(x)


def money(x) -> str:
    if is_blank(x):
        return "—"
    try:
        return f"NT$ {int(x):,}"
    except Exception:
        return str(x)


def brand_with_other(brand: str, other: str) -> str:
    if (brand or "").strip() == "其他":
        return v(other)
    return v(brand)


# 固定所有列的對齊比例（整頁一致）
KV_COLS = [1.1, 2.0]          # 左：欄位名 右：值
SPEC_COLS_2 = [1.0, 1.6]      # 品牌 / 型號
SPEC_COLS_3 = [1.0, 1.6, 1.0] # 品牌 / 型號 / 額外（容量/瓦數/數量）


def section(title: str):
    st.subheader(title)
    st.divider()


def row_kv(label: str, value: str):
    c1, c2 = st.columns(KV_COLS, vertical_alignment="center")
    with c1:
        st.markdown(f'<div class="kv-label">{label}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kv-value">{value}</div>', unsafe_allow_html=True)


def row_spec(title: str, brand_value: str, model_value: str,
             extra_label: str | None = None, extra_value: str | None = None):
    st.markdown(f'<div class="spec-title">{title}</div>', unsafe_allow_html=True)

    if extra_label is None:
        c1, c2 = st.columns(SPEC_COLS_2, vertical_alignment="center")
        with c1:
            st.markdown('<div class="spec-head">品牌</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-val">{brand_value}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="spec-head">型號</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-val">{model_value}</div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(SPEC_COLS_3, vertical_alignment="center")
        with c1:
            st.markdown('<div class="spec-head">品牌</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-val">{brand_value}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="spec-head">型號</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-val">{model_value}</div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="spec-head">{extra_label}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="spec-val">{extra_value}</div>', unsafe_allow_html=True)

    st.divider()


# -------------------------
# Header summary（✅移除頂部預算：只保留類型）
# -------------------------
st.markdown("## 你填寫的內容")
row_kv("服務需求類型", v(branch_name) if branch_name else v(branch))
st.divider()

# -------------------------
# A 預覽
# -------------------------
if branch == "A":
    section("用途與效能")
    usage = data.get("usage")
    usage_other = data.get("usage_other")
    show_usage = v(usage_other) if (usage == "其他用途 & 使用軟體" and not is_blank(usage_other)) else v(usage)
    row_kv("使用需求", show_usage)
    row_kv("整體效能", v(data.get("performance")))
    row_kv("預算規劃", money(data.get("budget")))

    section("週邊")
    row_kv("是否包含週邊", v(data.get("peripherals_included")))
    row_kv("週邊項目", v(data.get("peripherals")))

    section("散熱與外觀")
    row_kv("散熱類型", v(data.get("cooling")))
    row_kv("主機外觀", v(data.get("case_size")))
    row_kv("外觀風格", v(data.get("style")))

    color = data.get("color")
    color_other = data.get("color_other")
    show_color = v(color_other) if (color == "其他" and not is_blank(color_other)) else v(color)
    row_kv("主機顏色", show_color)

    lighting = data.get("lighting")
    lighting_other = data.get("lighting_other")
    show_light = v(lighting_other) if (lighting == "其他" and not is_blank(lighting_other)) else v(lighting)
    row_kv("燈光效果", show_light)

    section("其他需求")
    other_needs = data.get("other_needs", [])
    row_kv("其他需求", v(other_needs))
    if "硬碟容量需求" in (other_needs or []):
        row_kv("硬碟容量需求", v(data.get("storage_need")))

# -------------------------
# B 預覽
# -------------------------
elif branch == "B":
    section("現有主機規格")

    row_spec("CPU",
             brand_with_other(data.get("cpu_brand"), data.get("cpu_brand_other")),
             v(data.get("cpu_model")))

    row_spec("散熱器",
             brand_with_other(data.get("cooler_brand"), data.get("cooler_brand_other")),
             v(data.get("cooler_model")))

    row_spec("主機板",
             brand_with_other(data.get("mobo_brand"), data.get("mobo_brand_other")),
             v(data.get("mobo_model")))

    row_spec("記憶體",
             brand_with_other(data.get("ram_brand"), data.get("ram_brand_other")),
             v(data.get("ram_model")),
             extra_label="容量",
             extra_value=v(data.get("ram_capacity")))

    row_spec("顯示卡",
             brand_with_other(data.get("gpu_brand"), data.get("gpu_brand_other")),
             v(data.get("gpu_model")))

    row_spec("電源供應器",
             brand_with_other(data.get("psu_brand"), data.get("psu_brand_other")),
             v(data.get("psu_model")),
             extra_label="瓦數",
             extra_value=v(data.get("psu_watt")))

    row_spec("HDD",
             brand_with_other(data.get("hdd_brand"), data.get("hdd_brand_other")),
             v(data.get("hdd_model")),
             extra_label="數量",
             extra_value=v(data.get("hdd_qty")))

    row_spec("SSD",
             brand_with_other(data.get("ssd_brand"), data.get("ssd_brand_other")),
             v(data.get("ssd_model")),
             extra_label="數量",
             extra_value=v(data.get("ssd_qty")))

    row_spec("機殼",
             brand_with_other(data.get("case_brand"), data.get("case_brand_other")),
             v(data.get("case_model")))

    section("升級需求")
    targets = data.get("upgrade_targets", [])
    row_kv("升級目標", v(targets))
    if "其他" in (targets or []):
        row_kv("其他目標說明", v(data.get("upgrade_targets_other")))
    row_kv("升級預算", money(data.get("budget")))
    row_kv("是否需要資料轉移", v(data.get("migrate")))

# -------------------------
# C 預覽
# -------------------------
else:
    section("現有主機規格")

    row_spec("CPU",
             brand_with_other(data.get("cpu_brand"), data.get("cpu_brand_other")),
             v(data.get("cpu_model")))

    row_spec("散熱器",
             brand_with_other(data.get("cooler_brand"), data.get("cooler_brand_other")),
             v(data.get("cooler_model")))

    row_spec("主機板",
             brand_with_other(data.get("mobo_brand"), data.get("mobo_brand_other")),
             v(data.get("mobo_model")))

    row_spec("記憶體",
             brand_with_other(data.get("ram_brand"), data.get("ram_brand_other")),
             v(data.get("ram_model")),
             extra_label="容量",
             extra_value=v(data.get("ram_capacity")))

    row_spec("顯示卡",
             brand_with_other(data.get("gpu_brand"), data.get("gpu_brand_other")),
             v(data.get("gpu_model")))

    row_spec("電源供應器",
             brand_with_other(data.get("psu_brand"), data.get("psu_brand_other")),
             v(data.get("psu_model")),
             extra_label="瓦數",
             extra_value=v(data.get("psu_watt")))

    row_spec("HDD",
             brand_with_other(data.get("hdd_brand"), data.get("hdd_brand_other")),
             v(data.get("hdd_model")),
             extra_label="數量",
             extra_value=v(data.get("hdd_qty")))

    row_spec("SSD",
             brand_with_other(data.get("ssd_brand"), data.get("ssd_brand_other")),
             v(data.get("ssd_model")),
             extra_label="數量",
             extra_value=v(data.get("ssd_qty")))

    row_spec("機殼",
             brand_with_other(data.get("case_brand"), data.get("case_brand_other")),
             v(data.get("case_model")))

    section("改裝需求")
    items = data.get("mod_items", [])
    row_kv("改裝項目", v(items))
    if "其他" in (items or []):
        row_kv("其他改裝說明", v(data.get("mod_other")))
    row_kv("改裝預算", money(data.get("budget")))

# -------------------------
# Buttons
# -------------------------
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("返回"):
        t = st.session_state.get("service_type")
        if t == "A":
            st.switch_page("pages/02_BranchA_NewBuild.py")
        elif t == "B":
            st.switch_page("pages/03_BranchB_Upgrade.py")
        else:
            st.switch_page("pages/04_BranchC_Mod.py")

with col2:
    if st.button("繼續", type="primary"):
        st.switch_page("pages/06_Contact.py")