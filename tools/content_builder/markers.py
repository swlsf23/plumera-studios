"""Body markers, decorative bands, and generated content lists."""

from __future__ import annotations

import re
import sys
from html import escape

from tools.content_builder.assets import CONTENT
from tools.content_builder.chrome import chrome_for
from tools.content_builder.parse import recent_target_links, votw_links
from tools.content_builder.urls import votw_series_url

def _title_with_level(title: str, level: str) -> str:
    """Site standard: CEFR level at the end of a link label (Title · A1)."""
    title = title.strip()
    level = level.strip()
    if not title or not level or title.endswith(level):
        return title
    return f"{title} · {level}"

_ART_BAND_MARKER_RE = re.compile(r"<!--\s*art:\s*band\s*-->", re.I)
_ART_HERO_MARKER_RE = re.compile(r"<!--\s*art:\s*hero\s*-->", re.I)
_FIRST_P_CLOSE_RE = re.compile(r"</p\s*>", re.I)

# Title hero band (default: after the first body paragraph).
_HERO_ART_HTML = """\
<div class="hero-art-slot" aria-hidden="true">
  <div class="hero-art">
    <div class="hero-art__arc"></div>
    <svg class="hero-art__flourish" viewBox="0 0 800 30" preserveAspectRatio="none" focusable="false">
      <path class="hero-art__stroke hero-art__stroke--warm" d="M-30 22 C 90 2, 190 34, 320 10 S 520 -2, 860 20"></path>
      <path class="hero-art__stroke hero-art__stroke--cool" d="M-20 14 C 150 32, 280 -2, 430 18 S 650 30, 860 6"></path>
      <circle class="hero-art__ring hero-art__ring--left" cx="110" cy="2" r="20"></circle>
      <circle class="hero-art__ring hero-art__ring--right" cx="670" cy="16" r="14"></circle>
      <path class="hero-art__stroke hero-art__stroke--fine" d="M 240 26 L 360 4 M 520 24 L 620 8"></path>
    </svg>
    <div class="hero-art__panel">
      <span class="hero-art__shape hero-art__shape--circle"></span>
      <span class="hero-art__shape hero-art__shape--bar"></span>
      <span class="hero-art__shape hero-art__shape--dot"></span>
    </div>
  </div>
</div>"""

# Mid-article decorative band (same language as the title hero, different marks).
_ART_BAND_HTML = """\
<div class="hero-art-slot" aria-hidden="true">
  <div class="hero-art hero-art--inline">
    <div class="hero-art__arc"></div>
    <svg class="hero-art__flourish" viewBox="0 0 800 30" preserveAspectRatio="none" focusable="false">
      <path class="hero-art__stroke hero-art__stroke--warm" d="M860 8 C 640 28, 520 -4, 380 20 S 160 34, -30 10"></path>
      <path class="hero-art__stroke hero-art__stroke--cool" d="M860 24 C 680 0, 540 32, 360 8 S 140 -2, -30 22"></path>
      <circle class="hero-art__ring hero-art__ring--left" cx="690" cy="4" r="18"></circle>
      <circle class="hero-art__ring hero-art__ring--right" cx="160" cy="22" r="12"></circle>
      <path class="hero-art__stroke hero-art__stroke--fine" d="M 480 4 L 580 26 M 220 6 L 300 24"></path>
    </svg>
  </div>
</div>"""


def _expand_art_bands(html: str) -> str:
    """Replace every <!-- art: band --> with the inline decorative band."""
    if not html or "art:" not in html.lower():
        return html
    return _ART_BAND_MARKER_RE.sub(_ART_BAND_HTML, html)


def _inject_hero_after_first_paragraph(html: str) -> str:
    """Place the title hero band after the first <p>, or at the top if none."""
    if not html:
        return _HERO_ART_HTML
    match = _FIRST_P_CLOSE_RE.search(html)
    if not match:
        return f"{_HERO_ART_HTML}\n{html}"
    at = match.end()
    return f"{html[:at]}\n{_HERO_ART_HTML}\n{html[at:]}"


def _place_title_hero(html: str, *, source: str = "") -> str:
    """Default: after the first <p>. Override with <!-- art: hero --> in the body."""
    if not html:
        return _HERO_ART_HTML
    markers = list(_ART_HERO_MARKER_RE.finditer(html))
    if not markers:
        return _inject_hero_after_first_paragraph(html)
    if len(markers) > 1 and source:
        print(
            f"warning: multiple <!-- art: hero --> in {source}; using the first",
            file=sys.stderr,
        )
    return _ART_HERO_MARKER_RE.sub(_HERO_ART_HTML, html, count=1)


def _list_marker_re(kind: str) -> re.Pattern[str]:
    """<!-- {kind}: list --> insert point for an automated content list."""
    return re.compile(rf"<!--\s*{re.escape(kind)}:\s*list\s*-->", re.I)


def _split_at_list_marker(
    html: str, kind: str, *, source: str = ""
) -> tuple[str, str] | None:
    """Split body on <!-- {kind}: list -->; None if the marker is missing.

    Only the first marker is used. Extra markers stay in the HTML and trigger
    a warning.
    """
    matches = list(_list_marker_re(kind).finditer(html))
    if not matches:
        return None
    if len(matches) > 1:
        where = f" in {source}" if source else ""
        print(
            f"warning: multiple <!-- {kind}: list -->{where}; using the first",
            file=sys.stderr,
        )
    match = matches[0]
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
        hrefs[locale] = votw_series_url(locale, targets[0])
    return hrefs


