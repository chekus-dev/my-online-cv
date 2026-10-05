import logging
import os
import time
import urllib.error
import urllib.request
import json
from datetime import date, datetime, timezone
from pathlib import Path

import frontmatter
import markdown
from flask import Flask, abort, redirect, render_template, url_for
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
    ("portfolio", "Portfolio"),
    ("blog", "Blog"),
    ("contact", "Contact"),
]

POSTS_DIR = Path(__file__).resolve().parent / "posts"

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

GITHUB_PROJECTS = [
    {
        "account": "chekus-dev", "name": "ASCII Art Web", "language": "Go · HTML/CSS",
        "description": "Turns text into ASCII art using Standard, Shadow, and Thinkertoy styles.",
        "url": "https://github.com/chekus-dev/ascii-art-web", "upstream": "hmaach/ascii-art-web",
    },
    {
        "account": "chekus-dev", "name": "ASCII Web", "language": "Go · HTML/CSS/JavaScript",
        "description": "A browser-based ASCII art generator with multiple text-art styles.",
        "url": "https://github.com/chekus-dev/ascii-web", "upstream": "01founders-crack/ascii-art-web",
    },
    {
        "account": "chekus-dev", "name": "EJISCHOOL", "language": "Next.js · TypeScript · Go · PostgreSQL",
        "description": "A software learning platform with tutorials, references, exercises, auth, and a Go API.",
        "url": "https://github.com/chekus-dev/Ejischool", "upstream": "victorejike/Ejischool",
    },
    {
        "account": "chekus-dev", "name": "Go HTTP Template Server", "language": "Go · net/http · html/template",
        "description": "A small HTTP server demonstrating routing, method validation, error handling, and server-rendered HTML templates.",
        "url": "https://github.com/chekus-dev/go-http-template-server",
    },
    {
        "account": "chekus-dev", "name": "Learn Go HTTP Server", "language": "Go · Standard Library",
        "description": "A learning server covering routes, GET/POST methods, status codes, query parameters, JSON, and 404/405 handling.",
        "url": "https://github.com/chekus-dev/learn-go-http-server",
    },
    {
        "account": "chekus-dev", "name": "Lem-in", "language": "Go · Graph Algorithms",
        "description": "A student algorithm project that finds paths for ants through a colony using graph and path-search concepts.",
        "url": "https://github.com/chekus-dev/lem-in", "upstream": "appak21/lem-in",
    },
    {
        "account": "chekus-dev", "name": "9jaWonderPal (My Creative Partner)", "language": "React · Three.js · Node.js · Blender",
        "description": "A voice-first creative studio where children describe ideas and build 3D worlds to explore with a parent.",
        "url": "https://github.com/chekus-dev/my-creative-partner", "upstream": "asobuilds/my-creative-partner",
        "homepage": "https://my-creative-partner.vercel.app",
    },
    {
        "account": "chekus-dev", "name": "Online CV and Portfolio", "language": "Python · Flask · Tailwind CSS",
        "description": "This Flask site, with service pages, responsive navigation, security headers, and GitHub project listings.",
        "url": "https://github.com/chekus-dev/my-online-cv",
    },
    {
        "account": "chekus-dev", "name": "Simple Go HTTP Server", "language": "Go · net/http",
        "description": "A beginner-friendly server showing route registration, request handlers, and plain-text responses.",
        "url": "https://github.com/chekus-dev/simple-http-server-in-golang",
    },
    {
        "account": "chekus-dev", "name": "Todo App", "language": "Python · Flask · SQLAlchemy",
        "description": "A Flask task manager with accounts, due dates, reminders, recurring tasks, tags, search, and JSON import/export.",
        "url": "https://github.com/chekus-dev/todo-list-app",
    },
    {
        "account": "chekus-dev", "name": "Updated Go HTTP Server", "language": "Go · net/http · encoding/json",
        "description": "A JSON HTTP service with profile endpoints, health/readiness checks, request timeouts, and graceful shutdown.",
        "url": "https://github.com/chekus-dev/updated-http-server-in-golang",
    },
    {
        "account": "chekus-dev", "name": "Web ASCII Art", "language": "Go",
        "description": "A Go repository; its README currently contains only the project title, so project details are not documented there.",
        "url": "https://github.com/chekus-dev/web-ascii-art",
    },
    {
        "account": "chekus-dev", "name": "Budget Tracker", "language": "Go · MySQL · JavaScript · Python",
        "description": "A personal budget tracker with a Go HTTP server, PostgresSQL persistence, no-reload expense management, and a separate Python reporting script.",
        "url": "https://github.com/chekus-dev/budget-tracker",
    },
    {
        "account": "chokafor-bit", "name": "AdSense Bot Loader", "language": "Python · Selenium",
        "description": "A browser-automation fork with Selenium scripts and proxy/worker configuration.",
        "url": "https://github.com/chokafor-bit/Adsense-bot-loader", "upstream": "caseykingsley77/Adsense-bot-loader",
    },
    {
        "account": "chokafor-bit", "name": "Branch Blockchain", "language": "JavaScript · Blockchain tooling",
        "description": "A collection of blockchain learning exercises covering transactions, cryptography, smart contracts, tokens, NFTs, and DeFi.",
        "url": "https://github.com/chokafor-bit/Branch-Blockchain", "upstream": "kuzikov/Branch-Blockchain",
    },
    {
        "account": "chokafor-bit", "name": "Groupie Tracker", "language": "Go · HTML/CSS · REST API",
        "description": "An artist and concert explorer showing artist details, members, dates, venues, and related locations.",
        "url": "https://github.com/chokafor-bit/groupie-tracker", "upstream": "hmaach/groupie-tracker",
    },
    {
        "account": "chokafor-bit", "name": "HTTP Server in Golang", "language": "Go · net/http",
        "description": "A Go HTTP server repository; a README is not currently present, so its purpose is not documented there.",
        "url": "https://github.com/chokafor-bit/http-server-in-golang",
    },
    {
        "account": "chokafor-bit", "name": "My Text Editing Tool", "language": "Go",
        "description": "A command-line text processor that converts numbers, adjusts casing, punctuation, quotation marks, and article usage.",
        "url": "https://github.com/chokafor-bit/my-text-editing-tool",
    },
    {
        "account": "chokafor-bit", "name": "Pro Go", "language": "Go",
        "description": "Source examples accompanying Adam Freeman's Pro Go, covering Go language features and application examples.",
        "url": "https://github.com/chokafor-bit/pro-go", "upstream": "Apress/pro-go",
    },
    {
        "account": "chokafor-bit", "name": "01 Edu Public Curriculum", "language": "Course and project materials",
        "description": "A fork of 01 Edu's public educational repository and its programming course materials.",
        "url": "https://github.com/chokafor-bit/public", "upstream": "01-edu/public",
    },
    {
        "account": "chokafor-bit", "name": "Quiz Server", "language": "Go",
        "description": "A Go quiz-server repository; README content was unavailable during review, so feature details could not be verified.",
        "url": "https://github.com/chokafor-bit/quiz-server", "upstream": "brownstyl/quiz-server",
    },
    {
        "account": "chokafor-bit", "name": "Quize", "language": "Go tooling · JavaScript assets",
        "description": "A quiz project repository with Go utilities for extracting questions, achievements, shop data, CSS, and JavaScript and generating HTML.",
        "url": "https://github.com/chokafor-bit/quize",
    },
    {
        "account": "chokafor-bit", "name": "The Codecrafters", "language": "Go",
        "description": "A Go learning repository organized around Codecrafters-style exercises; no README was available during review.",
        "url": "https://github.com/chokafor-bit/the-codecrafters",
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
GITHUB_USERNAMES = (GITHUB_USERNAME, "chokafor-bit")
_github_cache = {}
GITHUB_CACHE_TTL = 60 * 60  # 1 hour — avoids hammering the unauthenticated API rate limit


def _github_get(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "chekus-portfolio",
    }
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())


def get_github_stats(username=GITHUB_USERNAME):
    """Live, verifiable stats pulled from the GitHub API. Cached for an hour.
    Returns None on any failure so the template can render a graceful fallback
    instead of fabricating numbers or crashing the page.
    """
    now = time.time()
    cached = _github_cache.get(username)
    if cached and (now - cached["fetched_at"]) < GITHUB_CACHE_TTL:
        return cached["data"]

    try:
        profile = _github_get(f"/users/{username}")
        repos = _github_get(f"/users/{username}/repos?per_page=100&sort=updated")

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
            "username": username,
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
            "profile_url": profile.get("html_url", f"https://github.com/{username}"),
        }
        _github_cache[username] = {"data": data, "fetched_at": now}
        return data
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as e:
        logger.warning("Could not fetch GitHub stats, falling back gracefully: %s", e)
        return None


def _as_date(value):
    """Front matter dates arrive as date objects or ISO strings; normalise both."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        return date.min


def load_posts(include_drafts=False):
    """Read every posts/*.md file, newest first.

    A post needs `title` and `date` in its front matter. `summary` is optional.
    Set `draft: true` to keep a post off the site while you write it. A broken
    file is logged and skipped so one bad post can never take the blog down.
    """
    posts = []
    for path in POSTS_DIR.glob("*.md"):
        try:
            post = frontmatter.load(path)
            if post.get("draft") and not include_drafts:
                continue
            words = len(post.content.split())
            posts.append({
                "slug": path.stem,
                "title": post["title"],
                "date": _as_date(post["date"]),
                "summary": post.get("summary", ""),
                "reading_time": max(1, round(words / 200)),
                "html": markdown.markdown(
                    post.content,
                    extensions=["fenced_code", "tables", "sane_lists"],
                ),
            })
        except (KeyError, OSError, ValueError, TypeError) as e:
            logger.warning("Skipping post %s: %s", path.name, e)
    return sorted(posts, key=lambda p: p["date"], reverse=True)


@app.context_processor
def inject_globals():
    """Inject variables available to all templates."""
    return {
        "nav_links": NAV_LINKS,
        "current_year": datetime.now(timezone.utc).year,
    }


@app.after_request
def set_security_headers(response):
    """Add security headers to all responses."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


def _base_context():
    """Shared context variables used across multiple routes."""
    return {
        "stats": SITE_STATS,
        "featured": PROJECTS[0],
        "github_accounts": [
            {"username": username, "stats": get_github_stats(username)}
            for username in GITHUB_USERNAMES
        ],
        "github_username": GITHUB_USERNAME,
        "github_projects": GITHUB_PROJECTS,
    }


# ============================================================================
# Routes
# ============================================================================

@app.route("/")
def home():
    """Home page — displays featured project and GitHub stats."""
    context = _base_context()
    context["active_page"] = "home"
    return render_template("landing.html", **context)


@app.route("/portfolio")
@app.route("/portfolio.html")
def portfolio():
    """Portfolio page — displays all GitHub projects in a grid."""
    context = _base_context()
    context["active_page"] = "portfolio"
    return render_template("portfolio.html", **context)


@app.route("/about")
@app.route("/about.html")
def about():
    """About page."""
    return render_template("about.html", active_page="about")


@app.route("/services")
@app.route("/services.html")
def services():
    """Services page."""
    return render_template("services.html", active_page="services")


@app.route("/blog")
def blog():
    """Blog index — every published post, newest first."""
    return render_template("blog.html", posts=load_posts(), active_page="blog")


@app.route("/blog.html")
def blog_html():
    """The other pages end in .html, so people may guess it. One canonical URL: /blog."""
    return redirect(url_for("blog"), code=301)


@app.route("/blog/<slug>")
def post(slug):
    """A single blog post, looked up by its file name (without .md)."""
    found = next((p for p in load_posts() if p["slug"] == slug), None)
    if found is None:
        abort(404)
    return render_template("post.html", post=found, active_page="blog")


@app.route("/contact")
@app.route("/contact.html")
def contact():
    """Contact page."""
    return render_template("contact.html", active_page="contact")


@app.route("/200")
@app.route("/200.html")
def success_page():
    """Success confirmation page."""
    return render_template("200.html", active_page=None), 200


# ============================================================================
# Utility Routes
# ============================================================================

@app.route("/robots.txt")
def robots():
    """Robots.txt for search engine crawling directives."""
    return (
        "User-agent: *\nAllow: /\nSitemap: " + url_for("sitemap", _external=True) + "\n",
        200,
        {"Content-Type": "text/plain"},
    )


@app.route("/sitemap.xml")
def sitemap():
    """Sitemap.xml for search engine indexing."""
    pages = [url_for(endpoint, _external=True) for endpoint, _ in NAV_LINKS]
    pages += [url_for("post", slug=p["slug"], _external=True) for p in load_posts()]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc in pages:
        xml.append(f"<url><loc>{loc}</loc></url>")
    xml.append("</urlset>")
    return "\n".join(xml), 200, {"Content-Type": "application/xml"}


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 Not Found errors."""
    return render_template("404.html", active_page=None), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 Internal Server Error."""
    return render_template("500.html", active_page=None), 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)