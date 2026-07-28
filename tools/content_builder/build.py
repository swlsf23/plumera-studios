"""Build dist/: copy public assets, emit content HTML, write sitemaps."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from html import escape
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tools.content_builder.chrome import chrome_for, language_menu
from tools.content_builder.parse import (
    ARTICLES_DIR,
    SITE_ORIGIN,
    VOTW_INDEX_STEM,
    WHATS_NEW_STEM,
    discover_article_pages,
    discover_core_pages,
    discover_votw_pages,
    discover_whats_new_pages,
    is_draft,
    parse_article_page,
    parse_core_page,
    parse_votw_page,
    parse_whats_new_page,
    recent_target_links,
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


def _normalize_href(href: str) -> str:
    href = href.strip()
    if href and not href.endswith("/"):
        href += "/"
    return href


def _title_with_level(title: str, level: str) -> str:
    """Site standard: CEFR level at the end of a link label (Title · A1)."""
    title = title.strip()
    level = level.strip()
    if not title or not level or title.endswith(level):
        return title
    return f"{title} · {level}"


def _enrich_related(
    related: list[dict[str, str]],
    pages_by_href: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    """Prefer the target page's document title, then append CEFR level."""
    if not related or not pages_by_href:
        return related
    enriched: list[dict[str, str]] = []
    for item in related:
        entry = dict(item)
        target = pages_by_href.get(_normalize_href(entry.get("href", "")))
        if target:
            title = target.get("title") or entry.get("title", "")
            entry["title"] = _title_with_level(title, target.get("level") or "")
        enriched.append(entry)
    return enriched


def _render_page(
    template,
    page,
    votw_nav: dict[str, str],
    pages_by_href: dict[str, dict[str, str]] | None = None,
) -> str:
    locale = page.locale
    related = _enrich_related(page.related, pages_by_href or {})
    return template.render(
        page=page,
        chrome=chrome_for(locale),
        site_origin=SITE_ORIGIN,
        languages=_lang_hrefs(locale),
        canonical_url=_canonical_url(page.canonical_path),
        related=related,
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


def _list_marker_re(kind: str) -> re.Pattern[str]:
    """<!-- {kind}: list --> insert point for an automated content list."""
    return re.compile(rf"<!--\s*{re.escape(kind)}:\s*list\s*-->", re.I)


def _split_at_list_marker(html: str, kind: str) -> tuple[str, str] | None:
    """Split body on <!-- {kind}: list -->; None if the marker is missing."""
    match = _list_marker_re(kind).search(html)
    if not match:
        return None
    before = html[: match.start()].rstrip()
    after = html[match.end() :].lstrip()
    return before, after


def _content_list_html(
    aria_label: str, entries: list[dict[str, str]]
) -> str:
    """Shared dense link list used by VOTW series index and what’s-new.

    Date labels print only when the date changes from the previous row, so
    same-day items read as one block.
    """
    if not entries:
        return ""
    items: list[str] = []
    prev_date = None
    for entry in entries:
        kind = escape(entry["kind"]) if entry.get("kind") else ""
        raw_date = entry.get("date") or ""
        date = escape(raw_date) if raw_date else ""
        show_date = bool(date) and raw_date != prev_date
        if raw_date:
            prev_date = raw_date
        summary = escape(entry["summary"]) if entry.get("summary") else ""
        title = escape(entry["title"])
        date_html = (
            f'\n      <span class="content-list__date">{date}</span>'
            if show_date
            else ""
        )
        kind_html = (
            f'\n      <p class="content-list__kind">{kind}</p>' if kind else ""
        )
        summary_html = (
            f'\n      <p class="content-list__summary">{summary}</p>'
            if summary
            else ""
        )
        items.append(
            f'  <li class="content-list__item">\n'
            f'    <div class="content-list__row">\n'
            f'      <a class="content-list__link" href="{escape(entry["href"])}">'
            f'<span class="content-list__title">{title}</span></a>'
            f"{date_html}\n"
            f"    </div>"
            f"{kind_html}{summary_html}\n"
            f"  </li>"
        )
    return (
        f'<nav class="content-list" aria-label="{escape(aria_label)}">\n'
        f"<ul>\n"
        f"{chr(10).join(items)}\n"
        f"</ul>\n"
        f"</nav>\n"
    )


def _votw_list_html(locale: str, target: str, include_drafts: bool) -> str:
    """Lesson list for a series index, built from the files on disk."""
    links = votw_links(CONTENT, locale, target, include_drafts=include_drafts)
    entries = [
        {
            "href": link["href"],
            "title": _title_with_level(link["title"], link.get("level") or ""),
            "date": link.get("date") or "",
            "summary": link.get("description") or "",
        }
        for link in links
    ]
    return _content_list_html("Verb of the Week", entries)


def _whats_new_list_html(locale: str, target: str, include_drafts: bool) -> str:
    """What’s-new list: VOTW lessons + articles, newest first."""
    links = recent_target_links(
        CONTENT, locale, target, include_drafts=include_drafts
    )
    label = chrome_for(locale)["whats_new"]
    entries = [
        {
            "href": link["href"],
            "title": _title_with_level(link["title"], link.get("level") or ""),
            "kind": link.get("kind") or "",
            "date": link.get("date") or "",
            "summary": link.get("description") or "",
        }
        for link in links
    ]
    return _content_list_html(label, entries)


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

    article_pages = []
    for path, locale, target in discover_article_pages(CONTENT):
        if is_draft(path):
            if not include_drafts:
                print(f"skip draft: {path.relative_to(CONTENT)}", file=sys.stderr)
                continue
            print(f"emit draft: {path.relative_to(CONTENT)}", file=sys.stderr)
        article_pages.append((parse_article_page(path, locale, target), path, target))

    whats_new_pages = []
    for path, locale, target in discover_whats_new_pages(CONTENT):
        if is_draft(path):
            if not include_drafts:
                print(f"skip draft: {path.relative_to(CONTENT)}", file=sys.stderr)
                continue
            print(f"emit draft: {path.relative_to(CONTENT)}", file=sys.stderr)
        whats_new_pages.append(
            (parse_whats_new_page(path, locale, target), path, target)
        )

    votw_nav = _votw_nav_hrefs(
        [
            (page.locale, target)
            for page, path, target in votw_pages
            if path.stem == VOTW_INDEX_STEM
        ]
    )
    pages_by_href = {
        page.canonical_path: {"title": page.title, "level": page.level}
        for page, _path, _target in [*article_pages, *votw_pages]
    }
    emitted = 0

    for page, path in core_pages:
        html = _render_page(template, page, votw_nav, pages_by_href)
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
            # /en/fr/votw/ → en/fr/votw/index.html
            # List replaces <!-- votw: list --> (outside .article-body).
            lesson_list = _votw_list_html(locale, target, include_drafts)
            split = _split_at_list_marker(page.body_html, "votw")
            if split is None:
                print(
                    f"warning: missing <!-- votw: list --> in {path}; "
                    f"appending the lesson list after the body",
                    file=sys.stderr,
                )
                page.after_body_html = lesson_list
            else:
                page.body_html, page.tail_body_html = split
                page.after_body_html = lesson_list
            out = series / "index.html"
        else:
            # /en/fr/votw/slug/ → en/fr/votw/slug/index.html
            slug = page.canonical_path.rstrip("/").split("/")[-1]
            out = series / slug / "index.html"
        _write(out, _render_page(template, page, votw_nav, pages_by_href))
        emitted += 1

    for page, path, target in article_pages:
        # /en/fr/articles/slug/ → en/fr/articles/slug/index.html
        slug = page.canonical_path.rstrip("/").split("/")[-1]
        out = dist / page.locale / target / ARTICLES_DIR / slug / "index.html"
        _write(out, _render_page(template, page, votw_nav, pages_by_href))
        emitted += 1

    for page, path, target in whats_new_pages:
        # /en/fr/whats-new/ → en/fr/whats-new/index.html
        # List replaces <!-- whats-new: list --> (outside .article-body).
        lesson_list = _whats_new_list_html(page.locale, target, include_drafts)
        split = _split_at_list_marker(page.body_html, "whats-new")
        if split is None:
            print(
                f"warning: missing <!-- whats-new: list --> in {path}; "
                f"appending the lesson list after the body",
                file=sys.stderr,
            )
            page.after_body_html = lesson_list
        else:
            page.body_html, page.tail_body_html = split
            page.after_body_html = lesson_list
        out = dist / page.locale / target / WHATS_NEW_STEM / "index.html"
        _write(out, _render_page(template, page, votw_nav, pages_by_href))
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
