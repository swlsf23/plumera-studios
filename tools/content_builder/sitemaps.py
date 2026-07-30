"""Generate root + per-locale sitemaps from files present in dist/."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from tools.content_builder.parse import SITE_ORIGIN

SKIP_DIR_NAMES = {"css", "js"}


def _lastmod() -> str:
    return date.today().isoformat()


def _urlset(paths: list[str]) -> str:
    lastmod = _lastmod()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in paths:
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


def _sitemap_index(entries: list[str]) -> str:
    """entries are sitemap paths relative to site root, e.g. 'sitemap-root.xml'."""
    lastmod = _lastmod()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in entries:
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


def write_sitemaps(dist: Path) -> list[str]:
    locales = sorted(
        p.name
        for p in dist.iterdir()
        if p.is_dir() and p.name not in SKIP_DIR_NAMES and not p.name.startswith(".")
    )
    written: list[str] = []
    index_entries: list[str] = []

    # Domain root entry page (public/index.html → dist/index.html).
    if (dist / "index.html").is_file():
        root_urls = dist / "sitemap-root.xml"
        root_urls.write_text(_urlset(["/"]), encoding="utf-8")
        written.append("sitemap-root.xml")
        index_entries.append("sitemap-root.xml")

    for locale in locales:
        locale_dir = dist / locale
        out = locale_dir / "sitemap.xml"
        out.write_text(_urlset(_urls_for_locale(locale, locale_dir)), encoding="utf-8")
        written.append(str(out.relative_to(dist)))
        index_entries.append(f"{locale}/sitemap.xml")

    root = dist / "sitemap.xml"
    root.write_text(_sitemap_index(index_entries), encoding="utf-8")
    written.append("sitemap.xml")
    return written
