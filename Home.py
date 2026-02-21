import streamlit as st
from UI import hide_sidebar
from pathlib import Path
import base64
import mimetypes
import streamlit.components.v1 as components

hide_sidebar(page_title="電腦組裝服務諮詢表單")

# -------------------------
# Helpers
# -------------------------
def ss_setdefault(key: str, value):
    if key not in st.session_state:
        st.session_state[key] = value

def _img_to_data_uri(path: Path) -> str:
    """把本機圖片轉成 data URI，讓 HTML 可以直接顯示。"""
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = "image/png"
    b = path.read_bytes()
    b64 = base64.b64encode(b).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def marquee_images(image_paths, height_px=1000, duration_sec=1000):
    """
    水平跑馬燈（由左到右移動，無限循環）。
    - height_px：顯示高度
    - duration_sec：跑完整段所需秒數（越大越慢）
    """
    uris = [_img_to_data_uri(Path(p)) for p in image_paths][::-1]
    # 為了無縫循環：把內容複製一份接在後面
    items = uris + uris

    imgs_html = "\n".join(
        f'<img src="{u}" class="marquee-img" />' for u in items
    )

    html = f"""
    <style>
      .marquee-wrap {{
        width: 100%;
        overflow: hidden;
        border-radius: 16px;
        background: transparent;
      }}

      .marquee-track {{
        display: flex;
        gap: 28px;
        align-items: center;
        width: max-content;
        animation: marquee {duration_sec}s linear infinite;
      }}

      /* 由左到右：從 -50% 滑回 0%（內容已複製一份才會無縫） */
      @keyframes marquee {{
        0%   {{ transform: translateX(-50%); }}
        100% {{ transform: translateX(0%); }}
      }}

      .marquee-img {{
        height: {height_px}px;
        width: auto;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
      }}

      /* 手機/窄螢幕：降低高度 */
      @media (max-width: 768px) {{
        .marquee-img {{
          height: 320px;
        }}
      }}
    </style>

    <div class="marquee-wrap">
      <div class="marquee-track">
        {imgs_html}
      </div>
    </div>
    """
    # height 要略大於圖片高度，避免被裁切
    components.html(html, height=height_px + 40, scrolling=False)

# -------------------------
# 若你希望每次打開都當作新客戶（清空上次資料），保留即可
st.session_state.clear()

# -------------------------
# UI
# -------------------------
st.title("電腦組裝服務諮詢表單")
st.caption("歡迎閱讀簡介，點選「繼續」後進入事前須知。")

Intro_DIR = Path("Assets/Intro")
imgs = []
if Intro_DIR.exists():
    for ext in ("*.PNG", "*.JPG", "*.png", "*.jpg", "*.jpeg", "*.webp"):
        imgs += sorted(Intro_DIR.glob(ext))

if imgs:
    # ✅ 改成跑馬燈顯示（由左到右）
    marquee_images([str(p) for p in imgs], height_px=520, duration_sec=40)
else:
    st.info(
        "尚未放入簡介圖片。\n\n"
        "請將 PPT 每頁匯出成圖片（01.png、02.png…）後放到：Assets/Intro/"
    )

st.divider()

ss_setdefault("Intro_viewed", False)

col1, col2 = st.columns([1, 1])
with col2:
    if st.button("繼續", type="primary"):
        st.session_state.Intro_viewed = True
        st.switch_page("pages/00_Notice.py")