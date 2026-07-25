"""Build dist/: copy public assets, emit content HTML, write sitemaps."""

from __future__ import annotations

import argparse
import shutil
import sys
from html import escape
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tools.content_builder.chrome import chrome_for, language_menu
from tools.content_builder.parse import (
    SITE_ORIGIN,
    VOTW_INDEX_STEM,
    discover_core_pages,
    discover_votw_pages,
    is_draft,
    parse_core_page,
    parse_votw_page,
    votw_links,
)
from tools.content_builder.sidebar import SOCIAL_LINKS, related_for
from tools.content_builder.sitemaps import write_sitemaps

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"
TEMPLATES = Path(__file__).resolve().parent / "templates"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def _copy_public(dist: Path) -> None:
    if dist.exists():
        shutil.rmtree(dist)
    shutil.copytree(
        PUBLIC,
        dist,
        ignore=shutil.ignore_patterns("sitemap.xml"),
    )


def _lang_hrefs(locale: str, canonical_path: str) -> list[dict[str, str | bool]]:
    """Same path shape in each locale (self-canonical pages; no hreflang head tags)."""
    suffix = canonical_path[len(f"/{locale}") :]  # e.g. /updates.html or /votw/slug/

    def href_for(code: str) -> str:
        return f"/{code}{suffix}"

    return language_menu(locale, href_for)


def _write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def _canonical_url(page_path: str) -> str:
    return f"{SITE_ORIGIN}{page_path}"


def _render_page(template, page, votw_locales: set[str] = frozenset()) -> str:
    locale = page.locale
    return template.render(
        page=page,
        chrome=chrome_for(locale),
        site_origin=SITE_ORIGIN,
        languages=_lang_hrefs(locale, page.canonical_path),
        canonical_url=_canonical_url(page.canonical_path),
        related=related_for(locale),
        social_links=SOCIAL_LINKS,
        show_votw=locale in votw_locales,
    )


def _write_redirect(path: Path, target: str) -> None:
    """Tiny static redirect stub (works on any static host, including local)."""
    _write(
        path,
        (
            "<!doctype html>\n"
            f'<html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={target}">'
            f'<link rel="canonical" href="{SITE_ORIGIN}{target}">'
            f"<title>Redirecting…</title>"
            f"<script>location.replace({target!r})</script>"
            f'</head><body><p><a href="{target}">Continue</a></p></body></html>\n'
        ),
    )


def _votw_list_html(locale: str, include_drafts: bool) -> str:
    """Link list appended to a series index, built from the files on disk."""
    links = votw_links(CONTENT, locale, include_drafts=include_drafts)
    if not links:
        return ""
    items = "\n".join(
        f'  <li><a href="{escape(link["href"])}">{escape(link["title"])}</a></li>'
        for link in links
    )
    return f'\n<ul class="votw-list">\n{items}\n</ul>\n'


def _votw_locales(include_drafts: bool) -> set[str]:
    """Locales whose series index lands in this build, so nav has a target."""
    return {
        locale
        for path, locale in discover_votw_pages(CONTENT)
        if path.stem == VOTW_INDEX_STEM and (include_drafts or not is_draft(path))
    }


def build(dist: Path = DIST, *, include_drafts: bool = False) -> int:
    env = _env()
    template = env.get_template("content_page.html")
    _copy_public(dist)

    votw_locales = _votw_locales(include_drafts)
    emitted = 0

    for path, locale in discover_core_pages(CONTENT):
        page = parse_core_page(path, locale)
        html = _render_page(template, page, votw_locales)
        # /en/updates/ → en/updates/index.html (plain static hosting)
        stem = path.stem
        out = dist / locale / stem / "index.html"
        _write(out, html)
        # Keep /en/updates.html working via a static redirect stub
        _write_redirect(dist / locale / f"{stem}.html", page.canonical_path)
        emitted += 1

    for path, locale in discover_votw_pages(CONTENT):
        if is_draft(path):
            if not include_drafts:
                print(f"skip draft: {path.relative_to(CONTENT)}", file=sys.stderr)
                continue
            print(f"emit draft: {path.relative_to(CONTENT)}", file=sys.stderr)
        page = parse_votw_page(path, locale)
        if path.stem == VOTW_INDEX_STEM:
            # /en/votw/ → en/votw/index.html, with the article list appended
            page.body_html += _votw_list_html(locale, include_drafts)
            out = dist / locale / "votw" / "index.html"
        else:
            # /en/votw/slug/ → en/votw/slug/index.html
            slug = page.canonical_path.rstrip("/").split("/")[-1]
            out = dist / locale / "votw" / slug / "index.html"
        _write(out, _render_page(template, page, votw_locales))
        emitted += 1

    sitemaps = write_sitemaps(dist)
    print(f"Emitted {emitted} content pages into {dist}")
    print(f"Wrote {len(sitemaps)} sitemap files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.content_builder")
    parser.add_argument(
        "--drafts",
        action="store_true",
        help="also emit pages marked draft: true (local builds only)",
    )
    args = parser.parse_args()
    return build(include_drafts=args.drafts)


if __name__ == "__main__":
    raise SystemExit(main())
