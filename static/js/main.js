(function () {
  const btn = document.getElementById('menu-toggle');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;
  const iconOpen = document.getElementById('icon-open');
  const iconClose = document.getElementById('icon-close');

  function setOpen(open) {
    menu.classList.toggle('hidden', !open);
    btn.setAttribute('aria-expanded', String(open));
    if (iconOpen) iconOpen.classList.toggle('hidden', open);
    if (iconClose) iconClose.classList.toggle('hidden', !open);
  }

  btn.addEventListener('click', () => setOpen(menu.classList.contains('hidden')));

  // Close after tapping a link (matters for same-page #anchors)
  menu.querySelectorAll('a').forEach((a) =>
    a.addEventListener('click', () => setOpen(false))
  );

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });

  // Reset when resizing up to desktop
  window.matchMedia('(min-width: 768px)').addEventListener('change', (e) => {
    if (e.matches) setOpen(false);
  });
})();