"""Parse Markdown files into Page models."""

from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

import frontmatter

from tools.content_builder.chrome import chrome_for, format_date, votw_series_label
from tools.content_builder.constants import (
    ARTICLES_DIR,
    CORE_DIR,
    VOTW_INDEX_STEM,
    WHATS_NEW_STEM,
)
from tools.content_builder.frontmatter_validate import (
    resolve_slug,
    validate_target,
)
from tools.content_builder.html_transform import (
    _classify_votw_tables,
    _inject_heading_ids,
    _md_to_html,
    _rewrite_local_images,
    _strip_tag,
    _tag_grammar_patterns,
)
from tools.content_builder.levels import (
    level_codes_for_page,
    level_label_for_page,
    normalize_level_list,
)
from tools.content_builder.models import Page
from tools.content_builder.urls import (
    article_url,
    core_url,
    votw_lesson_url,
    votw_series_url,
    whats_new_url,
)

def _format_date(value: object, locale: str) -> str:
    """Normalize a frontmatter date, then render it in the locale's convention.

    A non-ISO string is passed through as authored, so a page can override the
    label with free text.
    """
    if isinstance(value, datetime):
        return format_date(value.date(), locale)
    if isinstance(value, date):
        return format_date(value, locale)
    if isinstance(value, str) and value.strip():
        try:
            return format_date(date.fromisoformat(value.strip()), locale)
        except ValueError:
            return value.strip()
    return ""


def _parse_related(meta: dict, path: Path) -> list[dict[str, str]]:
    """Sidebar related cards from frontmatter `related:` (href required; title optional)."""
    raw = meta.get("related")
    if raw is None:
        return []
    if not isinstance(raw, list):
        print(
            f"warning: related must be a list ({path}); ignoring",
            file=sys.stderr,
        )
        return []
    items: list[dict[str, str]] = []
    for i, entry in enumerate(raw):
        if not isinstance(entry, dict):
            print(
                f"warning: related[{i}] must be a mapping with href "
                f"({path}); skipping",
                file=sys.stderr,
            )
            continue
        title = str(entry.get("title") or "").strip()
        href = str(entry.get("href") or "").strip()
        label = str(entry.get("meta") or "").strip()
        if not href:
            print(
                f"warning: related[{i}] needs non-empty href ({path}); skipping",
                file=sys.stderr,
            )
            continue
        items.append({"title": title, "href": href, "meta": label})
    return items


def _show_hero_art(meta: dict) -> bool:
    """Title hero on by default; set frontmatter ``hero: false`` to omit it."""
    if "hero" not in meta or meta["hero"] is None:
        return True
    return bool(meta["hero"])


def parse_core_page(path: Path, locale: str) -> Page:
    raw = path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    body = post.content.strip()
    lines = body.splitlines()
    meta = post.metadata
    source = f"{locale}/{CORE_DIR}/{path.name}"

    eyebrow = str(meta.get("eyebrow") or "").strip()
    if not eyebrow and lines and not lines[0].startswith("#") and lines[0].strip():
        eyebrow = lines[0].strip()
        body = "\n".join(lines[1:]).lstrip()

    html = _md_to_html(body)
    html = _rewrite_local_images(html, path, locale)
    heading, html = _strip_tag(html, "h1")
    html, toc = _inject_heading_ids(html)

    stem = path.stem
    slug = resolve_slug(meta, stem=stem, source=source)
    title = str(meta.get("title") or eyebrow or heading or stem)
    description = str(meta.get("description") or "")

    return Page(
        locale=locale,
        title=title,
        description=description,
        canonical_path=core_url(locale, slug),
        eyebrow=eyebrow,
        heading_html=heading.replace(" — ", "<br>") if " — " in heading else heading,
        body_html=html,
        toc=toc,
        related=_parse_related(meta, path),
        active=slug,
        show_hero_art=_show_hero_art(meta),
    )


def parse_votw_page(path: Path, locale: str, target: str) -> Page:
    post = frontmatter.load(path)
    meta = post.metadata
    stem = path.stem
    source = f"{locale}/{target}/votw/{path.name}"
    validate_target(meta.get("target"), folder=target, source=source)
    slug = resolve_slug(meta, stem=stem, source=source)
    title = str(meta.get("title") or stem)
    description = str(meta.get("description") or "")
    author = str(meta.get("author") or "")
    date_label = _format_date(meta.get("date"), locale)

    html = _md_to_html(post.content.strip())
    html = _rewrite_local_images(html, path, locale)
    heading, html = _strip_tag(html, "h1")
    if not heading:
        heading = title
    html, toc = _inject_heading_ids(html)
    html = _classify_votw_tables(html)
    html = _tag_grammar_patterns(html)

    # Eyebrow: frontmatter override, else series name (+ date on articles).
    series_name = str(meta.get("category") or votw_series_label(locale, target))
    eyebrow_override = str(meta.get("eyebrow") or "").strip()
    if eyebrow_override:
        eyebrow = eyebrow_override
    elif date_label and stem != VOTW_INDEX_STEM:
        eyebrow = f"{series_name} · {date_label}"
    else:
        eyebrow = series_name

    meta_parts: list[str] = []
    if author:
        meta_parts.append(chrome_for(locale)["by_author"].format(author=author))
    meta_line = " · ".join(meta_parts)

    heading_html = heading.replace(" — ", "<br>") if " — " in heading else heading
    if stem == VOTW_INDEX_STEM:
        canonical_path = votw_series_url(locale, target)
    elif path.parent.name != "votw":
        # content/.../votw/{lemma}/{job}.md → /.../votw/{lemma}/{job}/
        canonical_path = votw_lesson_url(
            locale, target, slug, lemma=path.parent.name
        )
    else:
        canonical_path = votw_lesson_url(locale, target, slug)

    return Page(
        locale=locale,
        title=title,
        description=description,
        canonical_path=canonical_path,
        eyebrow=eyebrow,
        heading_html=heading_html,
        meta_line=meta_line,
        body_html=html,
        toc=toc,
        related=_parse_related(meta, path),
        active="votw",
        show_hero_art=_show_hero_art(meta),
        level=_level_label(meta),
        levels=_level_codes(meta),
    )


def parse_article_page(path: Path, locale: str, target: str) -> Page:
    """Standalone page under content/{locale}/{target}/articles/."""
    post = frontmatter.load(path)
    meta = post.metadata
    stem = path.stem
    source = f"{locale}/{target}/{ARTICLES_DIR}/{path.name}"
    validate_target(meta.get("target"), folder=target, source=source)
    slug = resolve_slug(meta, stem=stem, source=source)
    title = str(meta.get("title") or stem)
    description = str(meta.get("description") or "")
    author = str(meta.get("author") or "")
    date_label = _format_date(meta.get("date"), locale)

    html = _md_to_html(post.content.strip())
    html = _rewrite_local_images(html, path, locale)
    heading, html = _strip_tag(html, "h1")
    if not heading:
        heading = title
    html, toc = _inject_heading_ids(html)
    html = _classify_votw_tables(html)
    html = _tag_grammar_patterns(html)

    eyebrow_override = str(meta.get("eyebrow") or "").strip()
    if eyebrow_override:
        eyebrow = eyebrow_override
    elif date_label:
        eyebrow = f"{chrome_for(locale)['article']} · {date_label}"
    else:
        eyebrow = chrome_for(locale)["article"]

    meta_parts: list[str] = []
    if author:
        meta_parts.append(chrome_for(locale)["by_author"].format(author=author))
    meta_line = " · ".join(meta_parts)

    heading_html = heading.replace(" — ", "<br>") if " — " in heading else heading
    canonical_path = article_url(locale, target, slug)

    return Page(
        locale=locale,
        title=title,
        description=description,
        canonical_path=canonical_path,
        eyebrow=eyebrow,
        heading_html=heading_html,
        meta_line=meta_line,
        body_html=html,
        toc=toc,
        related=_parse_related(meta, path),
        active="articles",
        show_hero_art=_show_hero_art(meta),
        level=_level_label(meta),
        levels=_level_codes(meta),
    )


def _levels_from_meta(meta: dict) -> list[str]:
    """CEFR codes from frontmatter (scalar, list, or comma-separated)."""
    return normalize_level_list(meta.get("level"))


def _level_codes(meta: dict) -> list[str]:
    """On-page badge codes (empty for all-level reference pages)."""
    return level_codes_for_page(_levels_from_meta(meta))


def _level_label(meta: dict) -> str:
    """List/card suffix: A1 or B1 B2 (empty for all-level reference pages)."""
    return level_label_for_page(_levels_from_meta(meta))

def parse_whats_new_page(path: Path, locale: str, target: str) -> Page:
    """Target-scoped recent-content page at /{locale}/{target}/whats-new/."""
    post = frontmatter.load(path)
    meta = post.metadata
    source = f"{locale}/{target}/{WHATS_NEW_STEM}.md"
    validate_target(meta.get("target"), folder=target, source=source)
    resolve_slug(meta, stem=path.stem, source=source)

    title = str(meta.get("title") or chrome_for(locale)["whats_new"])
    description = str(meta.get("description") or "")
    html = _md_to_html(post.content.strip())
    html = _rewrite_local_images(html, path, locale)
    heading, html = _strip_tag(html, "h1")
    if not heading:
        heading = title
    html, toc = _inject_heading_ids(html)

    eyebrow = str(meta.get("eyebrow") or "").strip() or chrome_for(locale)["whats_new"]
    heading_html = heading.replace(" — ", "<br>") if " — " in heading else heading

    return Page(
        locale=locale,
        title=title,
        description=description,
        canonical_path=whats_new_url(locale, target),
        eyebrow=eyebrow,
        heading_html=heading_html,
        body_html=html,
        toc=toc,
        related=_parse_related(meta, path),
        active=WHATS_NEW_STEM,
        show_hero_art=_show_hero_art(meta),
    )
