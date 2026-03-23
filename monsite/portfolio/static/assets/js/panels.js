// panels.js — gestion des 5 onglets avec debug complet
document.addEventListener("DOMContentLoaded", () => {

  console.log("===== PANELS DEBUG INIT =====");

  // Mapping id-bouton → id-panel
  const panels = {
    cert:  { btn: "btn-cert",  content: "content-cert"  },
    proj:  { btn: "btn-proj",  content: "content-proj"  },
    soft:  { btn: "btn-soft",  content: "content-soft"  },
    cyber: { btn: "btn-cyber", content: "content-cyber" },
    algo:  { btn: "btn-algo",  content: "content-algo"  },
  };

  // ── Fonctions de panels ─────────────────────────────
  function closeAll() {
    console.log("Closing all panels...");
    Object.keys(panels).forEach(key => {
      const { btn, content } = panels[key];
      const b = document.getElementById(btn);
      const c = document.getElementById(content);

      if (!b) console.warn("closeAll: BUTTON not found:", btn);
      if (!c) console.warn("closeAll: CONTENT not found:", content);

      if (b) b.classList.remove("active");
      if (c) c.style.display = "none";
    });
  }

  function openPanel(key) {
    console.log("Opening panel:", key);
    if (!panels[key]) {
      console.error("openPanel: panel key not found:", key);
      return;
    }

    closeAll();
    const { btn, content } = panels[key];
    const b = document.getElementById(btn);
    const c = document.getElementById(content);

    if (!b) console.error("openPanel: BUTTON not found:", btn);
    if (!c) console.error("openPanel: CONTENT not found:", content);

    if (b) {
      b.classList.add("active");
      console.log("Button activated:", btn);
    }

    if (c) {
      if (c.classList.contains("projects-grid")) {
        c.style.display = "grid";
      } else {
        c.style.display = "block";
      }
      console.log("Panel displayed:", content, "display style:", c.style.display);
    }
  }

  // ── Bind click on each panel button ─────────────────
  Object.keys(panels).forEach(key => {
    const btn = document.getElementById(panels[key].btn);
    const content = document.getElementById(panels[key].content);

    if (!btn) console.warn("Button not found for panel:", key, panels[key].btn);
    if (!content) console.warn("Content not found for panel:", key, panels[key].content);

    if (btn && content) {
      btn.addEventListener("click", () => {
        console.log("Clicked panel button:", key);
        openPanel(key);
      });
    }
  });

  // ── Sliders (Softwares panel) ─────────────────────
  document.querySelectorAll(".slider-wrapper").forEach((wrapper, index) => {
    const track   = wrapper.querySelector(".slider-horizontal");
    const prevBtn = wrapper.querySelector(".prev-btn");
    const nextBtn = wrapper.querySelector(".next-btn");

    if (!track) {
      console.warn("Slider wrapper #" + index + " has no track");
      return;
    }

    const STEP = 200;

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        track.scrollBy({ left: -STEP, behavior: "smooth" });
        console.log("Slider #" + index + " scrolled left");
      });
    } else {
      console.warn("Slider #" + index + " prev-btn missing");
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        track.scrollBy({ left: STEP, behavior: "smooth" });
        console.log("Slider #" + index + " scrolled right");
      });
    } else {
      console.warn("Slider #" + index + " next-btn missing");
    }
  });

  console.log("===== PANELS DEBUG READY =====");

});