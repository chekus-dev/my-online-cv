<div align="center">

# 💼 Chekus Joseph — Online CV

**A data-driven portfolio, built on Flask and shipped to production.**

<img width="1317" height="597" alt="Site screenshot" src="https://github.com/user-attachments/assets/6f905ebe-835b-4fbd-ae7d-f25da76fa335" style="border-radius: 12px;" />

<br/><br/>

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)

[![Live Site](https://img.shields.io/badge/▶_Live_Site-my--online--cv-f97316?style=for-the-badge)](https://my-online-cv-4.onrender.com/)

</div>

<br/>

A Flask-powered personal portfolio and online CV — home, about, services, portfolio, and contact pages, plus custom 404 and 500 error pages. Not a static template: it pulls live data from GitHub's API to build the project index on every cache cycle.

---

## ✨ Features

- 📱 Responsive layout styled with Tailwind CSS and custom CSS
- 📚 README-based summaries of public projects from the `chekus-dev` and `chokafor-bit` GitHub accounts, with fork and upstream attribution
- 📊 Live GitHub repository, star, language, and account-age statistics for both accounts, cached independently for one hour
- 🍔 Mobile navigation handled by `static/js/main.js`
- 🔐 Environment-based Flask configuration through `.env` and `config.py`
- 🛡️ Security headers applied to every response
- 🗺️ `robots.txt` and `sitemap.xml` routes
- 🚀 Gunicorn entry point for production deployment

---

## 🧪 Local Development

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

Visit **`http://localhost:5000`**.

> The default configuration runs in production mode. Set `FLASK_ENV=development` and `FLASK_DEBUG=1` for local development.

---

## 🚀 Production

Run behind Gunicorn, with nginx or Caddy in front for TLS:

```bash
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

**Environment variables:**

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Random secret used by Flask |
| `FLASK_ENV` | Leave unset or set to `production` |
| `FLASK_DEBUG` | Leave unset or set to `0` |
| `GITHUB_TOKEN` | Optional — a GitHub personal access token for authenticated API requests and a higher rate limit. Create one in GitHub's Developer settings and store it only in your local `.env` or deployment secret store. No repository permissions are required, since these are public profile reads. |

---

## 🗂️ Project Structure

---

## 🧭 Routes

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

---

## 🔗 GitHub Project References

The home page summarizes all **23 public repositories** reviewed across both accounts. Project descriptions are drawn from each repository's README; where a README is missing or contains only a title, the page states that rather than inferring a description.

Forked repositories are presented as such, with the upstream repository linked. The portfolio labels the user's role on these forks as a **partner contribution** — this does not claim authorship of the upstream project.

The project index spans Go HTTP servers and template rendering, JSON APIs, Flask applications, a task manager, a voice-first 3D creative studio, an education platform, ASCII-art tools, a text processor, an artist/concert explorer, blockchain learning exercises, and graph-algorithm coursework.

<div align="center">
<br/>

[![Live Site](https://img.shields.io/badge/🌍_Visit_the_Live_Site-f97316?style=for-the-badge)](https://my-online-cv-4.onrender.com/)

</div>
