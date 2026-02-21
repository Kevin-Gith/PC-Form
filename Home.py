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
    水平跑馬燈（無縫循環）+ 右上角放大按鈕（開啟全部圖片相簿）+ 點縮圖再放大
    - height_px：跑馬燈圖片高度
    - px_per_sec：每秒移動像素（越小越慢），建議 25~80
    - reverse_order：是否反轉顯示順序（照片順序反了就 True）
    """
    uris = [_img_to_data_uri(Path(p)) for p in image_paths]
    if reverse_order:
        uris = uris[::-1]

    # 無縫跑馬燈：複製一份接在後面
    marquee_items = uris + uris
    marquee_html = "\n".join(
        f'<img src="{u}" class="marquee-img" loading="lazy" />' for u in marquee_items
    )

    # Gallery：只用原始清單（不要複製）
    gallery_html = "\n".join(
        f'<button class="thumb-btn" data-src="{u}" title="點擊放大">'
        f'<img src="{u}" class="thumb-img" loading="lazy"/></button>'
        for u in uris
    )

    html = f"""
    <style>
      .marquee-wrap {{
        width: 100%;
        overflow: hidden;
        border-radius: 16px;
        background: transparent;
        position: relative;
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

      /* 右上角放大按鈕 */
      .open-gallery {{
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 10;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 0;
        border-radius: 999px;
        padding: 10px 14px;
        cursor: pointer;
        background: rgba(0,0,0,0.55);
        color: rgba(255,255,255,0.95);
        font-size: 14px;
      }}
      .open-gallery:hover {{
        background: rgba(0,0,0,0.68);
      }}

      @media (max-width: 768px) {{
        .marquee-img {{ height: 320px; }}
        .open-gallery {{ padding: 9px 12px; font-size: 13px; }}
      }}

      /* ===== Modal base ===== */
      .modal {{
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.75);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 999999;
        padding: 20px;
      }}
      .modal.open {{
        display: flex;
      }}
      .modal-close {{
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
      .modal-close:hover {{
        background: rgba(255,255,255,0.22);
      }}

      /* ===== Zoom (single) ===== */
      .zoom-img {{
        max-width: min(1200px, 96vw);
        max-height: 92vh;
        border-radius: 14px;
        box-shadow: 0 18px 60px rgba(0,0,0,0.6);
        background: rgba(20,20,20,0.2);
      }}
      .hint {{
        position: fixed;
        bottom: 14px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255,255,255,0.75);
        font-size: 13px;
        z-index: 1000000;
        user-select: none;
      }}

      /* ===== Gallery (all images) ===== */
      .gallery-panel {{
        width: min(1200px, 96vw);
        max-height: 90vh;
        background: rgba(20,20,20,0.92);
        border-radius: 16px;
        box-shadow: 0 18px 60px rgba(0,0,0,0.6);
        overflow: hidden;
        display: flex;
        flex-direction: column;
      }}

      .gallery-header {{
        padding: 14px 16px;
        color: rgba(255,255,255,0.92);
        font-size: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }}

      .gallery-count {{
        color: rgba(255,255,255,0.68);
        font-size: 13px;
      }}

      .gallery-grid {{
        padding: 14px;
        overflow: auto;
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
      }}

      @media (max-width: 1024px) {{
        .gallery-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      }}
      @media (max-width: 640px) {{
        .gallery-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      }}

      .thumb-btn {{
        border: 0;
        padding: 0;
        background: transparent;
        cursor: zoom-in;
      }}

      .thumb-img {{
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
      }}
      .thumb-btn:hover .thumb-img {{
        transform: scale(1.01);
        transition: transform 120ms ease;
      }}
    </style>

    <div class="marquee-wrap">
      <button id="openGallery" class="open-gallery" type="button">🔍 放大</button>
      <div id="track" class="marquee-track">
        {marquee_html}
      </div>
    </div>

    <!-- Gallery Modal: show ALL images -->
    <div id="galleryModal" class="modal" aria-hidden="true">
      <button id="galleryClose" class="modal-close" aria-label="Close">✕</button>
      <div class="gallery-panel" role="dialog" aria-modal="true">
        <div class="gallery-header">
          <div>全部圖片</div>
          <div class="gallery-count">共 {len(uris)} 張（點縮圖放大）</div>
        </div>
        <div id="galleryGrid" class="gallery-grid">
          {gallery_html}
        </div>
      </div>
      <div class="hint">點背景或按 ESC 關閉</div>
    </div>

    <!-- Zoom Modal: single image -->
    <div id="zoomModal" class="modal" aria-hidden="true">
      <button id="zoomClose" class="modal-close" aria-label="Close">✕</button>
      <img id="zoomImg" class="zoom-img" src="" alt="Zoomed image" />
      <div class="hint">點背景或按 ESC 關閉</div>
    </div>

    <script>
      (function() {{
        const track = document.getElementById("track");
        const pxPerSec = {px_per_sec};

        function startMarquee() {{
          // duplicated items => half width is loop distance
          const distance = track.scrollWidth / 2;
          const duration = distance / pxPerSec;

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

        // wait images loaded for accurate width
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
        setTimeout(startMarquee, 900);

        // ===== Modals =====
        const galleryModal = document.getElementById("galleryModal");
        const galleryClose = document.getElementById("galleryClose");
        const openGalleryBtn = document.getElementById("openGallery");

        const zoomModal = document.getElementById("zoomModal");
        const zoomClose = document.getElementById("zoomClose");
        const zoomImg = document.getElementById("zoomImg");

        function openGallery() {{
          galleryModal.classList.add("open");
          galleryModal.setAttribute("aria-hidden", "false");
        }}
        function closeGallery() {{
          galleryModal.classList.remove("open");
          galleryModal.setAttribute("aria-hidden", "true");
        }}

        function openZoom(src) {{
          zoomImg.src = src;
          zoomModal.classList.add("open");
          zoomModal.setAttribute("aria-hidden", "false");
        }}
        function closeZoom() {{
          zoomModal.classList.remove("open");
          zoomModal.setAttribute("aria-hidden", "true");
          zoomImg.src = "";
        }}

        openGalleryBtn.addEventListener("click", openGallery);
        galleryClose.addEventListener("click", closeGallery);
        zoomClose.addEventListener("click", closeZoom);

        // click marquee image -> zoom
        track.addEventListener("click", (e) => {{
          const t = e.target;
          if (t && t.tagName === "IMG") {{
            openZoom(t.src);
          }}
        }});

        // click thumbnail -> zoom
        const grid = document.getElementById("galleryGrid");
        grid.addEventListener("click", (e) => {{
          const btn = e.target.closest(".thumb-btn");
          if (!btn) return;
          const src = btn.getAttribute("data-src");
          if (src) openZoom(src);
        }});

        // click backdrop to close
        galleryModal.addEventListener("click", (e) => {{
          if (e.target === galleryModal) closeGallery();
        }});
        zoomModal.addEventListener("click", (e) => {{
          if (e.target === zoomModal) closeZoom();
        }});

        // ESC: close zoom first, then gallery
        document.addEventListener("keydown", (e) => {{
          if (e.key !== "Escape") return;
          if (zoomModal.classList.contains("open")) closeZoom();
          else if (galleryModal.classList.contains("open")) closeGallery();
        }});
      }})();
    </script>
    """

    components.html(html, height=height_px + 80, scrolling=False)


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
    # 速度：px_per_sec 越小越慢；照片順序反了就把 reverse_order=True
    marquee_images([str(p) for p in imgs], height_px=520, px_per_sec=35, reverse_order=True)
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