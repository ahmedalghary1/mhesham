document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('[data-header]');
  const menu = document.querySelector('[data-mobile-menu]');
  const openButton = document.querySelector('[data-menu-open]');
  const closeButton = document.querySelector('[data-menu-close]');
  const setMenu = (open) => {
    if (!menu) return;
    menu.classList.toggle('open', open);
    menu.setAttribute('aria-hidden', String(!open));
    openButton?.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) closeButton?.focus(); else if (document.activeElement === closeButton) openButton?.focus();
  };
  openButton?.addEventListener('click', () => setMenu(true));
  closeButton?.addEventListener('click', () => setMenu(false));
  menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu?.classList.contains('open')) setMenu(false); });
  window.addEventListener('resize', () => { if (window.innerWidth > 820 && menu?.classList.contains('open')) setMenu(false); }, {passive: true});
  window.addEventListener('scroll', () => header?.classList.toggle('scrolled', window.scrollY > 40), {passive: true});
  document.querySelectorAll('[data-year]').forEach(node => node.textContent = new Date().getFullYear());

  document.querySelectorAll('[data-contact-form]').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const responseNode = form.querySelector('[data-form-response]');
      const submit = form.querySelector('button[type="submit"]');
      submit.disabled = true;
      responseNode.textContent = document.documentElement.lang === 'ar' ? 'جارٍ الإرسال…' : 'Sending…';
      try {
        const response = await fetch(form.action, {method: 'POST', body: new FormData(form), headers: {'X-Requested-With': 'XMLHttpRequest'}});
        const data = await response.json();
        if (!response.ok) throw new Error(Object.values(data.errors || {}).flat().map(item => item.message).join(' '));
        form.reset();
        responseNode.textContent = document.documentElement.lang === 'ar' ? 'وصلت رسالتك. سأتواصل معك قريبًا.' : 'Message received. I will get back to you soon.';
      } catch (error) {
        responseNode.textContent = error.message || (document.documentElement.lang === 'ar' ? 'تعذر الإرسال الآن.' : 'Could not send right now.');
      } finally { submit.disabled = false; }
    });
  });

  document.querySelectorAll('.magnetic').forEach(button => {
    button.addEventListener('mousemove', event => {
      const rect = button.getBoundingClientRect();
      button.style.transform = `translate3d(${(event.clientX - rect.left - rect.width / 2) * .08}px,${(event.clientY - rect.top - rect.height / 2) * .08}px,0)`;
    });
    button.addEventListener('mouseleave', () => button.style.transform = '');
  });
});
