"""Generate root + per-locale sitemaps from files present in dist/.

URL discovery still scans dist/ (so drafts and missing pages stay out).
lastmod comes from source: frontmatter date when set, else source file mtime.
Dist is wiped each build, so emitted HTML mtimes are not used.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

import frontmatter

from tools.content_builder.parse import (
    ARTICLES_DIR,
    CONTENT_NON_LOCALES,
    CORE_DIR,
    CORE_SKIP,
    SITE_ORIGIN,
    VOTW_INDEX_STEM,
    WHATS_NEW_STEM,
)

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"

SKIP_DIR_NAMES = {"css", "js"}


def _iso(d: date) -> str:
    return d.isoformat()


def _mtime_date(path: Path) -> date:
    """UTC calendar date for file mtime (stable across build host timezones)."""
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date()


def _frontmatter_date(md_path: Path) -> date | None:
    """Publish date from YAML when present and parseable."""
    post = frontmatter.load(md_path)
    value = post.metadata.get("date")
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def _lastmod_for_source(path: Path) -> str:
    """Prefer frontmatter date on Markdown; otherwise file mtime."""
    if path.suffix == ".md":
        published = _frontmatter_date(path)
        if published is not None:
            return _iso(published)
    return _iso(_mtime_date(path))


def _content_url_for(md_path: Path) -> str | None:
    """Map a content Markdown path to its canonical trailing-slash URL."""
    try:
        rel = md_path.relative_to(CONTENT)
    except ValueError:
        return None
    parts = rel.parts
    if len(parts) < 2 or parts[0] in CONTENT_NON_LOCALES:
        return None

    locale = parts[0]
    # content/{locale}/core/{stem}.md → /{locale}/{stem}/ (index.md not emitted)
    if len(parts) == 3 and parts[1] == CORE_DIR:
        if parts[2] in CORE_SKIP:
            return None
        if not parts[2].endswith(".md"):
            return None
        stem = parts[2][: -len(".md")]
        return f"/{locale}/{stem}/"

    # content/{locale}/{target}/…
    if len(parts) < 3:
        return None
    target = parts[1]
    if target == CORE_DIR:
        return None

    # …/whats-new.md
    if len(parts) == 3 and parts[2] == f"{WHATS_NEW_STEM}.md":
        return f"/{locale}/{target}/{WHATS_NEW_STEM}/"

    # …/votw/index.md or …/votw/{slug}.md
    if len(parts) == 4 and parts[2] == "votw" and parts[3].endswith(".md"):
        stem = parts[3][: -len(".md")]
        if stem == VOTW_INDEX_STEM:
            return f"/{locale}/{target}/votw/"
        return f"/{locale}/{target}/votw/{stem}/"

    # …/votw/{lemma}/{job}.md
    if len(parts) == 5 and parts[2] == "votw" and parts[4].endswith(".md"):
        lemma = parts[3]
        stem = parts[4][: -len(".md")]
        return f"/{locale}/{target}/votw/{lemma}/{stem}/"

    # …/articles/{slug}.md
    if len(parts) == 4 and parts[2] == ARTICLES_DIR and parts[3].endswith(".md"):
        stem = parts[3][: -len(".md")]
        return f"/{locale}/{target}/{ARTICLES_DIR}/{stem}/"

    return None


def _source_lastmods() -> dict[str, str]:
    """Canonical URL → lastmod ISO date from public/ + content/ sources."""
    lastmods: dict[str, str] = {}

    root_html = PUBLIC / "index.html"
    if root_html.is_file():
        lastmods["/"] = _lastmod_for_source(root_html)

    for path in PUBLIC.rglob("*.html"):
        rel = path.relative_to(PUBLIC).as_posix()
        if rel == "index.html":
            continue  # already handled as /
        if rel.endswith("/index.html"):
            url = "/" + rel[: -len("index.html")]
        elif rel.endswith(".html"):
            # Unexpected bare public HTML; skip (redirects live only in dist/)
            continue
        else:
            continue
        lastmods[url] = _lastmod_for_source(path)

    if CONTENT.is_dir():
        for path in CONTENT.rglob("*.md"):
            url = _content_url_for(path)
            if url is None:
                continue
            lastmods[url] = _lastmod_for_source(path)

    return lastmods


def _urlset(entries: list[tuple[str, str]]) -> str:
    """entries: (path, lastmod_iso)."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, lastmod in entries:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{escape(f'{SITE_ORIGIN}{path}')}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                "  </url>",
            ]
        )
    lines.extend(["</urlset>", ""])
    return "\n".join(lines)


def _sitemap_index(entries: list[tuple[str, str]]) -> str:
    """entries: (sitemap path relative to site root, lastmod_iso)."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry, lastmod in entries:
        lines.extend(
            [
                "  <sitemap>",
                f"    <loc>{escape(f'{SITE_ORIGIN}/{entry}')}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                "  </sitemap>",
            ]
        )
    lines.extend(["</sitemapindex>", ""])
    return "\n".join(lines)


def _urls_for_locale(locale: str, locale_dir: Path) -> list[str]:
    """Index documents use trailing-slash URLs; skip *.html redirect stubs."""
    urls: list[str] = []
    for path in sorted(locale_dir.rglob("*.html")):
        rel = path.relative_to(locale_dir).as_posix()
        if rel == "index.html":
            urls.append(f"/{locale}/")
            continue
        if rel.endswith("/index.html"):
            urls.append(f"/{locale}/{rel[: -len('index.html')]}")
            continue
        # Ignore legacy redirect stubs like contact.html → contact/
    return urls


def _entries_with_lastmod(
    urls: list[str], source_lastmods: dict[str, str], fallback: str
) -> list[tuple[str, str]]:
    return [(url, source_lastmods.get(url, fallback)) for url in urls]


def write_sitemaps(dist: Path) -> list[str]:
    locales = sorted(
        p.name
        for p in dist.iterdir()
        if p.is_dir() and p.name not in SKIP_DIR_NAMES and not p.name.startswith(".")
    )
    written: list[str] = []
    index_entries: list[tuple[str, str]] = []
    source_lastmods = _source_lastmods()
    # Only if a dist URL has no source mapping (should be rare).
    today = _iso(datetime.now(timezone.utc).date())

    # Domain root entry page (public/index.html → dist/index.html).
    if (dist / "index.html").is_file():
        root_entries = _entries_with_lastmod(["/"], source_lastmods, today)
        root_urls = dist / "sitemap-root.xml"
        root_urls.write_text(_urlset(root_entries), encoding="utf-8")
        written.append("sitemap-root.xml")
        index_entries.append(("sitemap-root.xml", root_entries[0][1]))

    for locale in locales:
        locale_dir = dist / locale
        urls = _urls_for_locale(locale, locale_dir)
        entries = _entries_with_lastmod(urls, source_lastmods, today)
        out = locale_dir / "sitemap.xml"
        out.write_text(_urlset(entries), encoding="utf-8")
        written.append(str(out.relative_to(dist)))
        child_lastmod = max((lm for _url, lm in entries), default=today)
        index_entries.append((f"{locale}/sitemap.xml", child_lastmod))

    root = dist / "sitemap.xml"
    root.write_text(_sitemap_index(index_entries), encoding="utf-8")
    written.append("sitemap.xml")
    return written
