// panels.js — gestion des 5 onglets

document.addEventListener("DOMContentLoaded", () => {

  // Mapping id-bouton → id-panel
  const panels = {
    cert:  { btn: "btn-cert",  content: "content-cert"  },
    proj:  { btn: "btn-proj",  content: "content-proj"  },
    soft:  { btn: "btn-soft",  content: "content-soft"  },
    cyber: { btn: "btn-cyber", content: "content-cyber" },
    algo:  { btn: "btn-algo",  content: "content-algo"  },
  };

  function closeAll() {
    Object.values(panels).forEach(({ btn, content }) => {
      const b = document.getElementById(btn);
      const c = document.getElementById(content);
      if (b) b.classList.remove("active");
      if (c) c.style.display = "none";
    });
  }

  function openPanel(key) {
    closeAll();
    const { btn, content } = panels[key];
    const b = document.getElementById(btn);
    const c = document.getElementById(content);
    if (b) b.classList.add("active");
    if (c) {
      // projects-grid panels use display:grid, others use display:block
      c.style.display = c.classList.contains("projects-grid") ? "grid" : "block";
    }
  }

  // Bind click on each button
  Object.keys(panels).forEach(key => {
    const btn = document.getElementById(panels[key].btn);
    if (btn) btn.addEventListener("click", () => openPanel(key));
  });

  // ── Sliders (Softwares panel) ──────────────────────────
  document.querySelectorAll(".slider-wrapper").forEach(wrapper => {
    const track   = wrapper.querySelector(".slider-horizontal");
    const prevBtn = wrapper.querySelector(".prev-btn");
    const nextBtn = wrapper.querySelector(".next-btn");
    if (!track) return;

    const STEP = 200;

    if (prevBtn) prevBtn.addEventListener("click", () => {
      track.scrollBy({ left: -STEP, behavior: "smooth" });
    });

    if (nextBtn) nextBtn.addEventListener("click", () => {
      track.scrollBy({ left: STEP, behavior: "smooth" });
    });
    if (btn) btn.addEventListener("click", () => {
  console.log("Clicked:", key);  // vérifie si btn-cyber est détecté
  openPanel(key)
});
  });

});