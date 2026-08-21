# Mohamed Hesham - Full-Stack Portfolio

A bilingual Arabic/English portfolio for graphic designer Mohamed Hesham Abdul-Rahman. It uses Django server-side rendering, Django Templates, custom CSS, and small vanilla JavaScript modules. The public portfolio and the staff-only custom dashboard share the same visual identity.

## What is included

- Arabic `/ar/` and English `/en/` public experiences with correct RTL/LTR behavior.
- Editorial portfolio archive, category filtering, project case studies, ordered galleries, and accessible lightbox.
- Homepage content, experience, volunteering, education, skills, certificates, social links, site settings, and media models.
- Staff-only `/dashboard/` with overview, search, allow-listed CRUD, media management, multiple project-image upload, drag ordering, message inbox, and delete confirmations.
- Contact persistence with server validation, CSRF, honeypot, and ten-minute submission throttling.
- Canonical metadata, Open Graph/Twitter tags, JSON-LD, sitemap, robots rules, error pages, WhiteNoise, PostgreSQL-ready settings, and secure production defaults.
- GSAP/ScrollTrigger motion, Lenis smooth scrolling, subtle pointer parallax, fullscreen mobile navigation, reduced-motion support, and no frontend framework.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_portfolio
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/ar/` for Arabic, `http://127.0.0.1:8000/en/` for English, and `http://127.0.0.1:8000/dashboard/` for the owner dashboard.

## Honest content workflow

No fake projects were seeded. Add real projects from Dashboard > Projects, save the project, upload its gallery, then mark it published. Until a profile portrait is uploaded under Settings, the hero deliberately shows an MH monogram. Add the licensed Thamanya Sans files and local font-face declarations described in `static/fonts/README.md`.

## Production

The production Docker setup runs Gunicorn and PostgreSQL with persistent database and media volumes. It exposes the application only to a shared Docker proxy network by default. It can initially run over HTTP using the server IP; set `DEBUG=False`, a unique `SECRET_KEY`, the server IP, database password, and proxy network name in `.env`.

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the exact first-deployment, Nginx, HTTPS, update, backup, and troubleshooting commands. Use `deploy/nginx.example.conf` as the reverse-proxy reference.

## Useful commands

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```

See `DESIGN_PLAN.md` for the design system, data model, animation language, and responsive/RTL strategy.
