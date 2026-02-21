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


def marquee_images(image_paths, height_px=520, px_per_sec=35, reverse_order=False):
    """
    水平跑馬燈（無縫循環）+ 點擊放大檢視
    - height_px：圖片高度
    - px_per_sec：每秒移動像素（越小越慢），建議 25~80
    - reverse_order：是否反轉顯示順序（照片順序反了就 True）
    """
    uris = [_img_to_data_uri(Path(p)) for p in image_paths]
    if reverse_order:
        uris = uris[::-1]

    # 為了無縫循環：把內容複製一份接在後面
    items = uris + uris

    imgs_html = "\n".join(
        f'<img src="{u}" class="marquee-img" loading="lazy" />' for u in items
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
        will-change: transform;
        padding: 6px 0;
      }}

      .marquee-img {{
        height: {height_px}px;
        width: auto;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        cursor: zoom-in;
        user-select: none;
        -webkit-user-drag: none;
      }}

      .marquee-img:hover {{
        transform: scale(1.01);
        transition: transform 120ms ease;
      }}

      @media (max-width: 768px) {{
        .marquee-img {{ height: 320px; }}
      }}

      /* ====== Modal (Zoom viewer) ====== */
      .zoom-modal {{
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.75);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 999999;
        padding: 24px;
      }}

      .zoom-modal.open {{
        display: flex;
      }}

      .zoom-content {{
        max-width: min(1200px, 96vw);
        max-height: 92vh;
        width: auto;
        height: auto;
        border-radius: 14px;
        box-shadow: 0 18px 60px rgba(0,0,0,0.6);
        background: rgba(20,20,20,0.2);
      }}

      .zoom-close {{
        position: fixed;
        top: 18px;
        right: 18px;
        width: 44px;
        height: 44px;
        border-radius: 999px;
        border: 0;
        background: rgba(255,255,255,0.14);
        color: rgba(255,255,255,0.95);
        font-size: 22px;
        cursor: pointer;
        z-index: 1000000;
      }}

      .zoom-close:hover {{
        background: rgba(255,255,255,0.22);
      }}

      .zoom-hint {{
        position: fixed;
        bottom: 14px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255,255,255,0.75);
        font-size: 13px;
        z-index: 1000000;
        user-select: none;
      }}
    </style>

    <div class="marquee-wrap">
      <div id="track" class="marquee-track">
        {imgs_html}
      </div>
    </div>

    <!-- Zoom Modal -->
    <div id="zoomModal" class="zoom-modal" aria-hidden="true">
      <button id="zoomClose" class="zoom-close" aria-label="Close">✕</button>
      <img id="zoomImg" class="zoom-content" src="" alt="Zoomed image" />
      <div class="zoom-hint">點背景或按 ESC 關閉</div>
    </div>

    <script>
      (function() {{
        const track = document.getElementById("track");
        const pxPerSec = {px_per_sec};

        // ====== Marquee speed: fixed px/sec ======
        function startMarquee() {{
          // items = uris + uris，所以一半寬度就是循環距離
          const distance = track.scrollWidth / 2;
          const duration = distance / pxPerSec; // seconds

          const style = document.createElement("style");
          style.innerHTML = `
            @keyframes marquee {{
              0%   {{ transform: translateX(-${{distance}}px); }}
              100% {{ transform: translateX(0px); }}
            }}
            #track {{
              animation: marquee ${{duration}}s linear infinite;
            }}
          `;
          document.head.appendChild(style);
        }}

        // 等圖片載入後再算寬度（更準）
        const imgs = track.querySelectorAll("img");
        let loaded = 0;
        imgs.forEach(img => {{
          if (img.complete) {{
            loaded++;
            if (loaded === imgs.length) startMarquee();
          }} else {{
            img.addEventListener("load", () => {{
              loaded++;
              if (loaded === imgs.length) startMarquee();
            }});
            img.addEventListener("error", () => {{
              loaded++;
              if (loaded === imgs.length) startMarquee();
            }});
          }}
        }});

        // 保險：若某些瀏覽器事件沒觸發，延遲啟動
        setTimeout(startMarquee, 900);

        // ====== Zoom modal ======
        const modal = document.getElementById("zoomModal");
        const zoomImg = document.getElementById("zoomImg");
        const closeBtn = document.getElementById("zoomClose");

        function openModal(src) {{
          zoomImg.src = src;
          modal.classList.add("open");
          modal.setAttribute("aria-hidden", "false");
        }}

        function closeModal() {{
          modal.classList.remove("open");
          modal.setAttribute("aria-hidden", "true");
          zoomImg.src = "";
        }}

        // 點任何圖片放大
        track.addEventListener("click", (e) => {{
          const t = e.target;
          if (t && t.tagName === "IMG") {{
            openModal(t.src);
          }}
        }});

        // 關閉：右上角按鈕
        closeBtn.addEventListener("click", closeModal);

        // 關閉：點背景（但不能點到圖片）
        modal.addEventListener("click", (e) => {{
          if (e.target === modal) closeModal();
        }});

        // 關閉：ESC
        document.addEventListener("keydown", (e) => {{
          if (e.key === "Escape") closeModal();
        }});
      }})();
    </script>
    """

    components.html(html, height=height_px + 70, scrolling=False)


# -------------------------
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
    # ✅ 跑馬燈顯示（可調慢：px_per_sec 越小越慢）
    # reverse_order=True 代表反轉順序；如果你現在順序已正常就改 False
    marquee_images([str(p) for p in imgs], height_px=520, px_per_sec=35, reverse_order=False)
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