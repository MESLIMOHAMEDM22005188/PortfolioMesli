// theme.js — Clair/Sombre
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('theme-toggle');
  // Appliquer le thème mémorisé (ou 'light')
  const current = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', current);

  toggle.addEventListener('click', () => {
    const now = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', now);
    localStorage.setItem('theme', now);
  });
});
