document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.language-link').forEach(link => link.addEventListener('click', () => localStorage.setItem('portfolio-language', link.lang)));
});
