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
from tools.content_builder.sidebar import SOCIAL_LINKS
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


def _lang_hrefs(locale: str) -> list[dict[str, str | bool]]:
    """Switching language goes to that locale's home. Locales are separate
    audiences, not translations of each other, so pages have no counterparts."""
    return language_menu(locale, lambda code: f"/{code}/")


def _write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def _canonical_url(page_path: str) -> str:
    return f"{SITE_ORIGIN}{page_path}"


def _render_page(template, page, votw_nav: dict[str, str]) -> str:
    locale = page.locale
    return template.render(
        page=page,
        chrome=chrome_for(locale),
        site_origin=SITE_ORIGIN,
        languages=_lang_hrefs(locale),
        canonical_url=_canonical_url(page.canonical_path),
        related=page.related,
        social_links=SOCIAL_LINKS,
        votw_href=votw_nav.get(locale),
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


def _votw_list_html(locale: str, target: str, include_drafts: bool) -> str:
    """Card list for a series index, built from the files on disk."""
    links = votw_links(CONTENT, locale, target, include_drafts=include_drafts)
    if not links:
        return ""
    cards: list[str] = []
    for link in links:
        meta = escape(link["date"]) if link.get("date") else ""
        dek = escape(link["description"]) if link.get("description") else ""
        level = escape(link["level"]) if link.get("level") else ""
        level_html = (
            f'\n      <span class="votw-card__level">{level}</span>' if level else ""
        )
        meta_html = (
            f'\n    <p class="votw-card__meta">{meta}</p>' if meta else ""
        )
        dek_html = f'\n    <p class="votw-card__dek">{dek}</p>' if dek else ""
        cards.append(
            f'  <a class="votw-card" href="{escape(link["href"])}">\n'
            f'    <div class="votw-card__heading">\n'
            f'      <h2 class="votw-card__title">{escape(link["title"])}</h2>'
            f"{level_html}\n"
            f"    </div>"
            f"{meta_html}{dek_html}\n"
            f"  </a>"
        )
    return (
        f'<nav class="votw-card-list" aria-label="Verb of the Week">\n'
        f"{chr(10).join(cards)}\n"
        f"</nav>\n"
    )


def _votw_nav_hrefs(series: list[tuple[str, str]]) -> dict[str, str]:
    """Where the header's VOTW item points, per locale, given the series
    indexes this build emits. A locale with none does not get the item."""
    by_locale: dict[str, list[str]] = {}
    for locale, target in sorted(series):
        by_locale.setdefault(locale, []).append(target)

    hrefs: dict[str, str] = {}
    for locale, targets in by_locale.items():
        if len(targets) > 1:
            print(
                f"warning: {locale} has VOTW series for {', '.join(targets)}; the "
                f"header can only point at one and uses {targets[0]!r}. Decide on a "
                f"hub page or per-target nav items",
                file=sys.stderr,
            )
        hrefs[locale] = f"/{locale}/{targets[0]}/votw/"
    return hrefs


def build(dist: Path = DIST, *, include_drafts: bool = False) -> int:
    env = _env()
    template = env.get_template("content_page.html")
    _copy_public(dist)

    core_pages = [(parse_core_page(p, loc), p) for p, loc in discover_core_pages(CONTENT)]

    votw_pages = []
    for path, locale, target in discover_votw_pages(CONTENT):
        if is_draft(path):
            if not include_drafts:
                print(f"skip draft: {path.relative_to(CONTENT)}", file=sys.stderr)
                continue
            print(f"emit draft: {path.relative_to(CONTENT)}", file=sys.stderr)
        votw_pages.append((parse_votw_page(path, locale, target), path, target))

    votw_nav = _votw_nav_hrefs(
        [
            (page.locale, target)
            for page, path, target in votw_pages
            if path.stem == VOTW_INDEX_STEM
        ]
    )
    emitted = 0

    for page, path in core_pages:
        html = _render_page(template, page, votw_nav)
        # /en/updates/ → en/updates/index.html (plain static hosting)
        stem = path.stem
        out = dist / page.locale / stem / "index.html"
        _write(out, html)
        # Keep /en/updates.html working via a static redirect stub
        _write_redirect(dist / page.locale / f"{stem}.html", page.canonical_path)
        emitted += 1

    for page, path, target in votw_pages:
        locale = page.locale
        series = dist / locale / target / "votw"
        if path.stem == VOTW_INDEX_STEM:
            # /en/fr/votw/ → en/fr/votw/index.html, with the article cards
            # outside .article-body so prose link styles do not flatten them.
            page.after_body_html = _votw_list_html(locale, target, include_drafts)
            out = series / "index.html"
        else:
            # /en/fr/votw/slug/ → en/fr/votw/slug/index.html
            slug = page.canonical_path.rstrip("/").split("/")[-1]
            out = series / slug / "index.html"
        _write(out, _render_page(template, page, votw_nav))
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
