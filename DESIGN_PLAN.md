# Mohamed Hesham Portfolio - Technical and Design Plan

## 1. Reference and content analysis

- The supplied CV is a clean, text-led three-page document and contains no embedded portrait or portfolio artwork.
- The website brief therefore drives the art direction; the CV supplies verified biography, employment, volunteering, education, certificates, contact details, and skills.
- Until a portrait and project imagery are uploaded, the public site uses an intentional MH monogram composition and honest empty states. It never invents projects, clients, awards, testimonials, or metrics.
- The portfolio must feel like a designer's visual identity, not a CV placed online. Work appears immediately after the hero and becomes the dominant content once projects are published.

## 2. Visual system

- Palette: deep blue `#1F4D95`, indigo `#3B3B8E`, purple `#58037E`, magenta `#700481`, dark teal `#053844`, teal `#0D5969`, pale lavender `#F1ECF4`, coral `#E99A84`, and white.
- Background: layered blue-purple-magenta radial gradients, a low-contrast CSS grid, a light grain layer, and carefully limited glow.
- Typography: local Thamanya Sans files are wired through `@font-face`; Noto Sans Arabic, Arial, and sans-serif remain robust fallbacks until the supplied font files are added.
- Spacing: 8px base scale (`8, 12, 16, 24, 32, 48, 72, 96, 128`) with fluid `clamp()` values.
- Radius: 12px controls, 20px surfaces, 32px portfolio cards, and pill navigation/actions.
- Grid: a fluid 12-column desktop system; 8 columns on tablet; 4 columns on mobile. Logical properties keep RTL and LTR equal citizens.

## 3. Components and page structure

- Public shell: floating pill navigation, full-screen mobile menu, language switch, custom cursor for fine pointers, footer, messages, SEO metadata, and JSON-LD.
- Home: signature hero orbit, editorial project grid, about, skills, experience timeline, optional volunteering, education, certificates, and contact.
- Work: filterable published-project archive with real empty states.
- Project detail: localized content, project facts, responsive ordered gallery, accessible lightbox, Behance/external links, and previous/next navigation.
- Contact: standalone form plus embedded homepage form, both with CSRF, honeypot, server validation, and session/IP-aware throttling.
- Dashboard: staff-only login, overview, search, custom CRUD screens, message inbox/status actions, media library, site/home settings, and safe delete confirmation.

## 4. Django architecture

- `config`: environment-driven settings, root URLs, ASGI/WSGI, security, logging, static/media, email, and production configuration.
- `core`: site settings, home copy, social links, skills, shared context, homepage, language-safe helpers, SEO, robots, and sitemap.
- `projects`: categories, projects, ordered project media, archive/filter endpoint, and detail pages.
- `experience`: work experience and volunteering records.
- `certificates`: certificates and education records.
- `contact`: validated messages, honeypot and throttling.
- `media_library`: reusable uploads with bilingual alt text and file validation.
- `accounts`: staff authentication boundary.
- `dashboard`: custom staff UI and registry-driven CRUD with explicit allow-listed models.

## 5. Data model strategy

- All visitor-facing dynamic copy has Arabic and English fields.
- Sortable records expose `sort_order`; projects also support draft/published and featured states.
- `ProjectImage.layout_type` supports full, half, portrait, landscape, and grid presentation.
- Site-wide settings are a singleton; content sections have visibility switches.
- Uploads use Pillow-backed `ImageField` where appropriate, safe extension checks, size limits, predictable folders, and bilingual alt text.
- SQLite is the zero-configuration development database. `DATABASE_URL` switches production to PostgreSQL without model changes.

## 6. URL and template architecture

- Public URLs are language-prefixed: `/ar/`, `/en/`, localized project archives and detail URLs, contact, sitemap, and robots.
- Operational URLs remain stable: `/dashboard/`, `/dashboard/login/`, and Django's internal language endpoint.
- Templates inherit from `templates/base.html`; public and dashboard partials/cards are includes; each app owns its page templates where useful.

## 7. Static architecture

- CSS is split into variables, base, components, animations, responsive, and dashboard files.
- JavaScript is split into navigation/core behavior, motion, project filtering/lightbox, cursor/parallax, language behavior, and dashboard previews/confirmations.
- Uploaded portfolio files live under `media/`; collected production assets live under `staticfiles/` and are served through WhiteNoise.

## 8. Motion language

- Hero: deliberate GSAP sequence, then CSS orbital motion with three speeds and alternating direction.
- Headings: masked reveal; paragraphs: soft opacity/translate; work: clip reveal; timeline: staggered entries; certificates: subtle scale.
- Lenis integrates with ScrollTrigger when motion is enabled. All motion and smooth scrolling stop for `prefers-reduced-motion`.
- Pointer parallax is limited to 3-6px and only runs on fine pointers. Magnetic movement is similarly restrained.

## 9. Responsive and direction strategy

- Mobile-first rules preserve readable hierarchy and keep the hero portrait/monogram centered with four orbit tools.
- Editorial work cards collapse from 12-column compositions to a single, visually varied stack.
- CSS logical properties control inline alignment, spacing, positioning, arrows, and timeline rails; document `dir` and language come from Django.
- Navigation becomes an accessible full-screen menu with focus-aware controls and scroll locking.

## 10. Security, performance, and production

- Staff-only dashboard, no public registration, CSRF on all mutations, POST-only destructive actions, permission checks, safe redirects, secure cookie settings in production, `DEBUG=False`, and environment-only secrets.
- Images reserve dimensions, below-fold media lazy-loads, project uploads can be converted by the owner before upload, JavaScript is deferred, and motion only changes compositor-friendly properties.
- Sitemap, robots exclusions, canonical URLs, localized titles/descriptions, Open Graph/Twitter tags, Person/WebSite/CreativeWork schema, custom 403/404/500 pages, and cache-aware static delivery are included.
- Gunicorn + Nginx/VPS deployment is documented; optional Docker and PostgreSQL configuration are included without affecting local SQLite setup.
