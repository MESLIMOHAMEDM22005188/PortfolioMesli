document.addEventListener('DOMContentLoaded', () => {
  const mapBtn = {
    'btn-cert':  'content-cert',
    'btn-proj':  'content-proj',
    'btn-soft': 'content-soft'
  };

  function showPanel(id) {
    document.querySelectorAll('.panel-content').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.panel-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(id).style.display = (id === 'content-proj') ? 'grid' : 'block';
  }

  Object.entries(mapBtn).forEach(([btnId, panelId]) => {
    document.getElementById(btnId).addEventListener('click', () => {
      showPanel(panelId);
      document.getElementById(btnId).classList.add('active');
    });
  });

  // affichage par défaut
  showPanel('content-proj');
  document.getElementById('btn-proj').classList.add('active');
});
