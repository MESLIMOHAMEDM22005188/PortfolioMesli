// timeline.js — Basculer Education / Work dans la section Qualification
document.addEventListener('DOMContentLoaded', () => {
  const eduBtn    = document.getElementById('edu-btn');
  const workBtn   = document.getElementById('work-btn');
  const eduPanel  = document.getElementById('timeline-edu');
  const workPanel = document.getElementById('timeline-work');

  function switchTimeline(showEdu) {
    if (showEdu) {
      eduPanel.classList.add('active');
      workPanel.classList.remove('active');
      eduBtn.classList.add('active');
      workBtn.classList.remove('active');
    } else {
      workPanel.classList.add('active');
      eduPanel.classList.remove('active');
      workBtn.classList.add('active');
      eduBtn.classList.remove('active');
    }
  }

  eduBtn.addEventListener('click', () => switchTimeline(true));
  workBtn.addEventListener('click', () => switchTimeline(false));

  // Init : afficher Work
  switchTimeline(false);
});
