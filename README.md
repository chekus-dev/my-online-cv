# Chekus Joseph — Portfolio Site

Flask + Tailwind portfolio/services site.

## What changed from the original

- **One `base.html`** instead of six near-duplicate HTML files — header, nav, mobile menu, and footer now live in a single place.
- **Tailwind config and mobile-menu JS extracted** into `static/js/tailwind-config.js` and `static/js/main.js` instead of being copy-pasted into every page.
- **Portfolio and Blog pages are now data-driven** (`PROJECTS` / `REPOS` lists in `app.py`) instead of hardcoded card blocks on every page.
- **Shared window-mockup component** (`templates/_macros.html`) renders each project's browser/terminal-style preview from one place instead of repeating markup per card.
- **Live GitHub stats** on the homepage — public repo count, stars, followers, top languages, and top repos, pulled from the GitHub API at request time and cached for an hour. Falls back to a simple link if the API is unreachable, instead of breaking the page or showing fake numbers.
- **Case study page** (`/portfolio/cv-portfolio`) documenting the real decisions behind this site's build — linked from the homepage hero and the Portfolio page.
- **Real favicon and Open Graph image** as static SVG files, so links shared on WhatsApp/social show a proper preview.
- **Contact page** with direct links (email, phone, WhatsApp, GitHub) — no form to maintain or secure.
- **Environment-based config** (`config.py` + `.env`) — no more hardcoded `debug=True` in production.
- **Security headers** (`X-Frame-Options`, `X-Content-Type-Options`, etc.) added on every response.
- **404 / 500 error pages**, `robots.txt`, and `sitemap.xml`.
- **Accessibility**: skip-to-content link, visible focus rings, `aria-current` on active nav links.
- **Production entrypoint** (`wsgi.py`) for gunicorn, with `requirements.txt` pinned and separated from dev tooling.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env if needed

export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

Visit `http://localhost:5000`.

## Production

Run behind gunicorn (put nginx/Caddy in front of it for TLS):

```bash
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

Set these environment variables in production (see `.env.example`):

- `SECRET_KEY` — required, random string

## Project structure

```
app.py                            Routes, GitHub stats fetcher, error handlers
config.py                          Environment-based configuration
wsgi.py                            Production entrypoint (gunicorn)
templates/
  base.html                         Shared layout (header, nav, footer)
  _macros.html                      Shared window-mockup component for project cards
  landing.html, about.html, services.html,
  portfolio.html, blog.html, contact.html
  case_study_cv_portfolio.html      Case study for the featured project
  404.html, 500.html
static/
  css/site.css                      Animations, accessibility, focus states
  js/tailwind-config.js             Shared Tailwind theme
  js/main.js                        Mobile menu behavior
  img/favicon.svg, og-cover.svg
```

## Adding a new project or repo card

Edit the `PROJECTS` or `REPOS` list at the top of `app.py` — no template changes needed. Each project entry supports:

- `name`, `tag`, `description`, `url` — displayed on the card
- `path`, `kind` — passed to the `window_mockup` macro; `kind` can be `browser`, `terminal`, `todo`, or `profile`
- `featured` — set `True` on exactly one project to feature it in the homepage hero
- `case_study` — optional; set to a route name if you write a dedicated case study page for that project

## GitHub stats

`get_github_stats()` in `app.py` calls the public GitHub API for the username set in `GITHUB_USERNAME`. No auth token is required, but unauthenticated calls are capped at 60/hour per IP — the 1-hour cache keeps normal traffic well under that. If you outgrow the limit, add a GitHub personal access token and pass it as a `Authorization` header in `_github_get()`.