def marquee_images(image_paths, height_px=520, px_per_sec=45):
    """
    水平跑馬燈（無縫循環）+ 點擊放大檢視
    - height_px：圖片高度
    - px_per_sec：每秒移動像素（越小越慢），建議 25~80
    """
    uris = [_img_to_data_uri(Path(p)) for p in image_paths][::-1]  # 需要反轉順序就保留
    items = uris + uris  # 無縫循環

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
        display: none;            /* hidden by default */
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
          const distance = track.scrollWidth / 2; // items duplicated
          const duration = distance / pxPerSec;

          const style = document.createElement("style");
          style.innerHTML = `
            @keyframes marquee {{
              0%   {{ transform: translateX(0px); }}
              100% {{ transform: translateX(-${{distance}}px); }}
            }}
            #track {{
              animation: marquee ${{duration}}s linear infinite;
            }}
          `;
          document.head.appendChild(style);
        }}

        // Wait images loaded so widths are correct
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

        // Click any image to zoom
        track.addEventListener("click", (e) => {{
          const t = e.target;
          if (t && t.tagName === "IMG") {{
            openModal(t.src);
          }}
        }});

        // Close: button
        closeBtn.addEventListener("click", closeModal);

        // Close: click backdrop (but not the image)
        modal.addEventListener("click", (e) => {{
          if (e.target === modal) closeModal();
        }});

        // Close: ESC
        document.addEventListener("keydown", (e) => {{
          if (e.key === "Escape") closeModal();
        }});
      }})();
    </script>
    """

    components.html(html, height=height_px + 60, scrolling=False)