document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.querySelector('[data-dashboard-sidebar]');
  const sidebarToggle = document.querySelector('[data-sidebar-toggle]');
  const setSidebar = open => { sidebar?.classList.toggle('open', open); sidebarToggle?.setAttribute('aria-expanded', String(open)); };
  sidebarToggle?.addEventListener('click', () => setSidebar(!sidebar?.classList.contains('open')));
  document.addEventListener('keydown', event => { if (event.key === 'Escape') setSidebar(false); });
  document.addEventListener('click', event => {
    if (window.innerWidth <= 760 && sidebar?.classList.contains('open') && !sidebar.contains(event.target) && !sidebarToggle?.contains(event.target)) setSidebar(false);
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 760) setSidebar(false); }, {passive: true});

  const modal = document.querySelector('[data-confirm-modal]');
  let pendingForm = null;
  document.querySelectorAll('[data-delete-form]').forEach(form => form.addEventListener('submit', event => {
    event.preventDefault(); pendingForm = form; modal.hidden = false;
  }));
  modal?.querySelector('[data-confirm-cancel]')?.addEventListener('click', () => { modal.hidden = true; pendingForm = null; });
  modal?.querySelector('[data-confirm-accept]')?.addEventListener('click', () => pendingForm?.submit());

  const upload = document.querySelector('[data-upload-form] input[type=file]');
  const previews = document.querySelector('[data-upload-previews]');
  upload?.addEventListener('change', () => {
    previews.innerHTML = '';
    [...upload.files].forEach(file => {
      if (!file.type.startsWith('image/')) return;
      const image = document.createElement('img'); image.src = URL.createObjectURL(file); image.alt = file.name; previews.append(image);
    });
  });

  document.querySelectorAll('[data-sortable-list]').forEach(list => {
    let dragging = null;
    [...list.children].forEach(item => {
      item.draggable = true;
      item.addEventListener('dragstart', () => { dragging = item; item.style.opacity = '.45'; });
      item.addEventListener('dragend', async () => {
        item.style.opacity = ''; dragging = null;
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value || document.cookie.match(/csrftoken=([^;]+)/)?.[1];
        const body = new URLSearchParams(); [...list.children].forEach(child => body.append('ids[]', child.dataset.id));
        await fetch(list.dataset.reorderUrl, {method: 'POST', headers: {'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded'}, body});
      });
      item.addEventListener('dragover', event => { event.preventDefault(); if (!dragging || dragging === item) return; const rect = item.getBoundingClientRect(); list.insertBefore(dragging, event.clientY < rect.top + rect.height / 2 ? item : item.nextSibling); });
    });
  });
});
