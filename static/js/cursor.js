document.addEventListener('DOMContentLoaded', () => {
  if (!window.matchMedia('(pointer: fine)').matches || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const cursor = document.querySelector('.custom-cursor');
  if (!cursor || !document.body.classList.contains('has-cursor')) return;
  window.addEventListener('pointermove', event => { cursor.style.transform = `translate3d(${event.clientX - 34}px,${event.clientY - 34}px,0) scale(${cursor.classList.contains('visible') ? 1 : .4})`; });
  document.querySelectorAll('[data-project-card], [data-lightbox-src]').forEach(item => {
    item.addEventListener('mouseenter', () => cursor.classList.add('visible'));
    item.addEventListener('mouseleave', () => cursor.classList.remove('visible'));
  });
  document.querySelectorAll('[data-parallax-root]').forEach(root => {
    root.addEventListener('pointermove', event => {
      const rect = root.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - .5;
      const y = (event.clientY - rect.top) / rect.height - .5;
      root.querySelectorAll('[data-parallax]').forEach(layer => {
        const amount = Number(layer.dataset.parallax || 1) * 3;
        layer.style.transform = `translate3d(${x * amount}px,${y * amount}px,0)`;
      });
    });
    root.addEventListener('pointerleave', () => root.querySelectorAll('[data-parallax]').forEach(layer => layer.style.transform = ''));
  });
});
