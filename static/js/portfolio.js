document.addEventListener('DOMContentLoaded', () => {
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-project-card]')];
  filterButtons.forEach(button => button.addEventListener('click', () => {
    filterButtons.forEach(item => item.classList.toggle('active', item === button));
    cards.forEach(card => {
      const visible = !button.dataset.filter || card.dataset.category === button.dataset.filter;
      card.hidden = !visible;
    });
  }));

  const lightbox = document.querySelector('[data-lightbox]');
  if (!lightbox) return;
  const items = [...document.querySelectorAll('[data-lightbox-src]')];
  const image = lightbox.querySelector('img');
  let index = 0, touchStart = 0;
  const show = next => { index = (next + items.length) % items.length; image.src = items[index].dataset.lightboxSrc; };
  const open = item => { index = items.indexOf(item); show(index); lightbox.classList.add('open'); lightbox.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden'; };
  const close = () => { lightbox.classList.remove('open'); lightbox.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; };
  items.forEach(item => { item.addEventListener('click', () => open(item)); item.addEventListener('keydown', event => { if (event.key === 'Enter') open(item); }); });
  lightbox.querySelector('[data-lightbox-close]')?.addEventListener('click', close);
  lightbox.querySelector('[data-lightbox-prev]')?.addEventListener('click', () => show(index - 1));
  lightbox.querySelector('[data-lightbox-next]')?.addEventListener('click', () => show(index + 1));
  document.addEventListener('keydown', event => { if (!lightbox.classList.contains('open')) return; if (event.key === 'Escape') close(); if (event.key === 'ArrowLeft') show(index - 1); if (event.key === 'ArrowRight') show(index + 1); });
  lightbox.addEventListener('touchstart', event => touchStart = event.touches[0].clientX, {passive: true});
  lightbox.addEventListener('touchend', event => { const delta = event.changedTouches[0].clientX - touchStart; if (Math.abs(delta) > 45) show(index + (delta < 0 ? 1 : -1)); }, {passive: true});
});
