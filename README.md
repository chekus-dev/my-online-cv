# Chekus Joseph - Online CV

A Flask-powered personal portfolio and online CV. The site includes home, about,
services, portfolio, and contact pages, plus custom 404 and 500 error pages.

Live site: https://my-online-cv.onrender.com/

## Features

- Responsive portfolio layout styled with Tailwind CSS and custom CSS.
- README-based summaries of public projects from the `chekus-dev` and
  `chokafor-bit` GitHub accounts, with fork and upstream attribution.
- Live GitHub repository, star, language, and account-age stats for both
  accounts, cached independently for one hour.
- Mobile navigation handled by `static/js/main.js`.
- Environment-based Flask configuration through `.env` and `config.py`.
- Security headers added to every response.
- `robots.txt` and `sitemap.xml` routes.
- Gunicorn entry point for production deployment.

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

The default configuration runs in production mode. Set `FLASK_ENV=development`
and `FLASK_DEBUG=1` when developing locally.

## Production

Run behind gunicorn (put nginx/Caddy in front of it for TLS):

```bash
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

Set these environment variables in production (see `.env.example`):

- `SECRET_KEY` - a random secret used by Flask
- `FLASK_ENV` - leave unset or set to `production`
- `FLASK_DEBUG` - leave unset or set to `0`
- `GITHUB_TOKEN` - optional GitHub personal access token used for authenticated
  GitHub API requests and a higher API rate limit. Create one in GitHub's
  Developer settings and put it only in your local `.env` or deployment secret
  store. No repository permissions are needed for these public profile reads.

## Project structure

```
app.py                    Flask app, routes, navigation, and error handlers
config.py                 Development and production configuration
wsgi.py                   Gunicorn entry point
requirements.txt          Python dependencies
templates/
  landing.html            Home page
  200.html                Request-success page
  about.html              About page
  services.html           Services page
  portfolio.html          GitHub project index
  contact.html            Contact page
  404.html                Not-found page
  500.html                Server-error page
static/
  css/site.css            Site styles and animations
  js/main.js              Mobile menu behavior
  js/tailwind-config.js   Tailwind configuration
  img/profile.jpg         Profile image
```

## Routes

| URL | Page |
| --- | --- |
| `/` | Home |
| `/about` | About |
| `/services` | Services |
| `/portfolio` | Portfolio and GitHub project index |
| `/contact` | Contact |
| `/200.html` | Request-success page (HTTP 200) |
| `/robots.txt` | Crawler instructions |
| `/sitemap.xml` | Sitemap |

## GitHub project references

The home page summarizes all 23 public repositories reviewed across both
accounts. Project descriptions are based on the repositories' READMEs; where a
README is missing or only has a title, the page says so rather than guessing.

Forks are presented as forked projects with the upstream repository linked.
The portfolio labels the user's role on those forks as partner contribution;
this does not claim authorship of the upstream project.md

The project index covers Go HTTP servers and template rendering, JSON APIs,
Flask applications, a task manager, a voice-first 3D creative studio, an
education platform, ASCII-art tools, a text processor, an artist/concert
explorer, blockchain learning exercises, and graph-algorithm coursework.