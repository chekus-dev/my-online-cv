import logging
import time
import urllib.error
import urllib.request
import json
from datetime import datetime, timezone

from flask import Flask, render_template, url_for
from dotenv import load_dotenv

load_dotenv()

from config import get_config

app = Flask(__name__)
app.config.from_object(get_config())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("portfolio")

NAV_LINKS = [
    ("home", "Home"),
    ("about", "About"),
    ("services", "Services"),
    ("contact", "Contact"),
]

PROJECTS = [
    {
        "name": "Go HTTP Template Server", "tag": "Go", "color": "amber",
        "description": "A Go-based HTTP server built around Go's templating system, used as a foundation for building server-rendered web applications.",
        "url": "https://github.com/chekus-dev/go-http-template-server", "featured": False,
        "path": "~/go-http-template-server", "kind": "terminal",
    },
    {
        "name": "Updated HTTP Server in Golang", "tag": "Go", "color": "emerald",
        "description": "An iteration on my Go HTTP server work, refining routing and request handling as I deepened my understanding of the net/http package.",
        "url": "https://github.com/chekus-dev/updated-http-server-in-golang", "featured": False,
        "path": "~/updated-http-server", "kind": "terminal",
    },
    {
        "name": "Simple HTTP Server in Golang", "tag": "Go", "color": "violet",
        "description": "A lightweight HTTP server built from scratch in Go to understand the fundamentals of handling requests and responses without a framework.",
        "url": "https://github.com/chekus-dev/simple-http-server-in-golang", "featured": False,
        "path": "~/simple-http-server", "kind": "terminal",
    },
    {
        "name": "Learn Go HTTP Server", "tag": "Go", "color": "rose",
        "description": "A teaching-focused repo built to explain HTTP status codes and pattern matching in Go, aimed at helping others learn server fundamentals.",
        "url": "https://github.com/chekus-dev/learn-go-http-server", "featured": False,
        "path": "~/learn-go-http-server", "kind": "terminal",
    },
    {
        "name": "Todo List App", "tag": "Python", "color": "fuchsia",
        "description": "A task management web app built with Python and Flask, covering full CRUD functionality — creating, editing, completing, and organizing tasks.",
        "url": "https://github.com/chekus-dev/todo-list-app", "featured": False,
        "path": "~/todo-list-app", "kind": "todo",
    },
]

SITE_STATS = [
    {"value": str(len(PROJECTS)), "label": "Shipped projects"},
    {"value": "Go · Flask", "label": "Primary stack"},
    {"value": "Full-Stack", "label": "Front end to backend"},
    {"value": "Nigeria", "label": "Based in"},
]

REPOS = [
    {"slug": "go-http-template-server", "name": "Go HTTP Template Server", "color": "amber"},
    {"slug": "updated-http-server-in-golang", "name": "Updated HTTP Server in Golang", "color": "emerald"},
    {"slug": "simple-http-server-in-golang", "name": "Simple HTTP Server in Golang", "color": "violet"},
    {"slug": "learn-go-http-server", "name": "Learn Go HTTP Server", "color": "rose"},
    {"slug": "todo-list-app", "name": "Todo List App", "color": "fuchsia"},
]

GITHUB_USERNAME = "chekus-dev"
_github_cache = {"data": None, "fetched_at": 0}
GITHUB_CACHE_TTL = 60 * 60  # 1 hour — avoids hammering the unauthenticated API rate limit


def _github_get(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "chekus-portfolio"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())


def get_github_stats():
    """Live, verifiable stats pulled from the GitHub API. Cached for an hour.
    Returns None on any failure so the template can render a graceful fallback
    instead of fabricating numbers or crashing the page.
    """
    now = time.time()
    if _github_cache["data"] and (now - _github_cache["fetched_at"]) < GITHUB_CACHE_TTL:
        return _github_cache["data"]

    try:
        profile = _github_get(f"/users/{GITHUB_USERNAME}")
        repos = _github_get(f"/users/{GITHUB_USERNAME}/repos?per_page=100&sort=updated")

        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        lang_counts = {}
        for r in repos:
            lang = r.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
        top_languages = sorted(lang_counts, key=lang_counts.get, reverse=True)[:4]

        top_repos = sorted(repos, key=lambda r: (r.get("stargazers_count", 0), r.get("updated_at", "")), reverse=True)[:6]

        created = datetime.strptime(profile["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        years_active = max(1, datetime.now(timezone.utc).year - created.year)

        data = {
            "public_repos": profile.get("public_repos", 0),
            "followers": profile.get("followers", 0),
            "total_stars": total_stars,
            "years_active": years_active,
            "top_languages": top_languages,
            "top_repos": [
                {
                    "name": r["name"],
                    "description": r.get("description") or "",
                    "stars": r.get("stargazers_count", 0),
                    "language": r.get("language") or "",
                    "url": r["html_url"],
                }
                for r in top_repos
            ],
            "profile_url": profile.get("html_url", f"https://github.com/{GITHUB_USERNAME}"),
        }
        _github_cache["data"] = data
        _github_cache["fetched_at"] = now
        return data
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as e:
        logger.warning("Could not fetch GitHub stats, falling back gracefully: %s", e)
        return None


@app.context_processor
def inject_globals():
    return {"nav_links": NAV_LINKS, "current_year": datetime.now(timezone.utc).year}


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.route("/")
def home():
    return render_template(
        "landing.html",
        stats=SITE_STATS,
        featured=PROJECTS[0],
        github=get_github_stats(),
        github_username=GITHUB_USERNAME,
    )


@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/services")
@app.route("/services.html")
def services():
    return render_template("services.html")


@app.route("/contact")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/robots.txt")
def robots():
    return (
        "User-agent: *\nAllow: /\nSitemap: " + url_for("sitemap", _external=True) + "\n",
        200,
        {"Content-Type": "text/plain"},
    )


@app.route("/sitemap.xml")
def sitemap():
    pages = [url_for(endpoint, _external=True) for endpoint, _ in NAV_LINKS]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in pages:
        xml.append(f"<url><loc>{loc}</loc></url>")
    xml.append("</urlset>")
    return "\n".join(xml), 200, {"Content-Type": "application/xml"}


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
