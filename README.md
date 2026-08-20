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

1. Set `DEBUG=False`, a long `SECRET_KEY`, the public host/origin, and a PostgreSQL `DATABASE_URL` in `.env`.
2. Configure SMTP settings and `CONTACT_NOTIFICATION_EMAIL` if email delivery is desired.
3. Run `python manage.py collectstatic --noinput` and `python manage.py migrate`.
4. Run Gunicorn behind Nginx with `gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3`.
5. Serve `/media/` directly from durable storage. The model architecture can later swap Django's default storage for S3 or Cloudinary.

The included Docker files are optional and use PostgreSQL without changing application code. Review `deploy/nginx.conf` and replace the example domain before launch.

## Useful commands

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```

See `DESIGN_PLAN.md` for the design system, data model, animation language, and responsive/RTL strategy.
