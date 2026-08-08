"""Page rendering and related-card enrichment."""

from __future__ import annotations

import re
import sys

from tools.content_builder.chrome import chrome_for, language_menu
from tools.content_builder.constants import SITE_ORIGIN
from tools.content_builder.markers import (
    _expand_art_bands,
    _place_title_hero,
    _title_with_level,
)
from tools.content_builder.sidebar import SOCIAL_LINKS

def _lang_hrefs(locale: str) -> list[dict[str, str | bool]]:
    """Switching language goes to that locale's home. Locales are separate
    audiences, not translations of each other, so pages have no counterparts."""
    return language_menu(locale, lambda code: f"/{code}/")


def _canonical_url(page_path: str) -> str:
    return f"{SITE_ORIGIN}{page_path}"


def _normalize_href(href: str) -> str:
    href = href.strip()
    if href and not href.endswith("/"):
        href += "/"
    return href


def _plain_heading(heading_html: str) -> str:
    """Strip tags from page H1 HTML for use as a related-card label."""
    return re.sub(r"<[^>]+>", "", heading_html or "").strip()


def _enrich_related(
    related: list[dict[str, str]],
    pages_by_href: dict[str, dict[str, str]],
    *,
    source: str = "",
    draft_hrefs: set[str] | None = None,
    warn_draft_targets: bool = False,
) -> list[dict[str, str]]:
    """Label related cards: author title override, else target H1, then CEFR level."""
    if not related:
        return related
    draft_hrefs = draft_hrefs or set()
    where = f" in {source}" if source else ""
    enriched: list[dict[str, str]] = []
    for i, item in enumerate(related):
        entry = dict(item)
        href = _normalize_href(entry.get("href", ""))
        author_title = (entry.get("title") or "").strip()
        target = pages_by_href.get(href)
        if author_title:
            label = author_title
            level = (target or {}).get("level") or ""
        elif target:
            label = (
                (target.get("heading") or "").strip()
                or (target.get("title") or "").strip()
            )
            level = target.get("level") or ""
        else:
            print(
                f"warning: related[{i}]{where}: unresolved href {href!r} "
                f"(no title override and no matching content page); skipping",
                file=sys.stderr,
            )
            continue
        if not label:
            print(
                f"warning: related[{i}]{where}: href {href!r} resolved with "
                f"empty label; skipping",
                file=sys.stderr,
            )
            continue
        if warn_draft_targets and href in draft_hrefs:
            print(
                f"warning: related[{i}]{where}: href {href!r} points at a "
                f"draft page; the label resolves, but that URL is not emitted "
                f"without --drafts",
                file=sys.stderr,
            )
        entry["title"] = _title_with_level(label, level)
        enriched.append(entry)
    return enriched


def _render_page(
    template,
    page,
    votw_nav: dict[str, str],
    pages_by_href: dict[str, dict[str, str]] | None = None,
    *,
    source: str = "",
    draft_hrefs: set[str] | None = None,
    warn_draft_targets: bool = False,
) -> str:
    locale = page.locale
    related = _enrich_related(
        page.related,
        pages_by_href or {},
        source=source,
        draft_hrefs=draft_hrefs,
        warn_draft_targets=warn_draft_targets,
    )
    page.body_html = _expand_art_bands(page.body_html)
    page.tail_body_html = _expand_art_bands(page.tail_body_html)
    if page.show_hero_art:
        page.body_html = _place_title_hero(page.body_html, source=source or "")
        page.show_hero_art = False
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


