"""VOTW / what’s-new list builders from on-disk Markdown."""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

import frontmatter

from tools.content_builder.chrome import chrome_for, votw_series_label
from tools.content_builder.constants import ARTICLES_DIR, VOTW_INDEX_STEM
from tools.content_builder.discover import is_draft
from tools.content_builder.frontmatter_validate import (
    parse_draft,
    resolve_slug,
    validate_iso_date,
)
from tools.content_builder.pages import _format_date, _level_label
from tools.content_builder.urls import article_url, votw_lesson_url

def _frontmatter_sort_date(value: object) -> date:
    """ISO date for sorting; unknown/missing sorts to the epoch (oldest).

    ISO-shaped values must be real calendar dates (hard-fail fakes like
    2026-13-40). Free-text labels that are not ISO-shaped sort as oldest.
    """
    if value is None or value == "":
        return date.min
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value.strip():
        text = value.strip()
        # ISO-shaped → real calendar date required; free text → oldest.
        if len(text) >= 10 and text[4] == "-" and text[7] == "-":
            return validate_iso_date(text)
        try:
            return date.fromisoformat(text)
        except ValueError:
            return date.min
    return date.min


def _plain_list_title(text: str) -> str:
    """Strip light Markdown emphasis from a list label (e.g. *prendre* → prendre)."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    return text.strip()


def _list_title_from_post(post, fallback: str) -> str:
    """Prefer body H1 for list cards; else frontmatter title / fallback."""
    list_title = str(post.metadata.get("title") or fallback)
    for line in post.content.splitlines():
        if line.startswith("# "):
            return _plain_list_title(line[2:])
    return _plain_list_title(list_title)


# Lesson filenames: votw-prendre-a1.md, votw-faire-basics-a2.md, …
_VOTW_LESSON_STEM = re.compile(r"^votw-.+")


def _is_votw_series_index_path(path: Path) -> bool:
    """True for the series index at votw/index.md."""
    return path.parent.name == "votw" and path.stem == VOTW_INDEX_STEM


def _is_votw_lemma_hub_path(path: Path) -> bool:
    """True only for the canonical hub votw/{lemma}/votw-{lemma}-index.md."""
    parent = path.parent
    if parent.name == "votw":
        return False
    return path.stem == f"votw-{parent.name}-index"


def _is_votw_index_path(path: Path) -> bool:
    """Series index or canonical lemma hub (not every filename ending in -index)."""
    return _is_votw_series_index_path(path) or _is_votw_lemma_hub_path(path)


def _is_votw_lesson_path(path: Path) -> bool:
    """VOTW lesson page: votw-*.md that is not a series/lemma index."""
    if _is_votw_index_path(path):
        return False
    return bool(_VOTW_LESSON_STEM.fullmatch(path.stem))


def _votw_lesson_paths(votw: Path) -> list[Path]:
    """Flat + nested lesson pages (indexes and non-lesson markdown excluded).

    Used for what's-new and catalog: each lesson stays an individual entry.
    """
    paths = [p for p in votw.glob("*.md") if _is_votw_lesson_path(p)]
    paths.extend(p for p in votw.glob("*/*.md") if _is_votw_lesson_path(p))
    return sorted(set(paths))


def _votw_lemma_hub_path(lemma_dir: Path) -> Path | None:
    """Canonical hub votw-{lemma}-index.md, or None (no silent *-index fallback)."""
    preferred = lemma_dir / f"votw-{lemma_dir.name}-index.md"
    return preferred if preferred.is_file() else None


def _votw_series_list_paths(
    votw: Path, *, include_drafts: bool = False
) -> list[Path]:
    """Paths for VOTW series index cards.

    Hub pages are the rollout-safe series entry for a lemma folder: when
    ``votw-{lemma}-index.md`` exists and is publishable, it replaces nested
    lessons on this list (nested lessons remain on what's-new / catalog). Flat
    one-offs (prendre, tenir) stay listed. If a lemma folder has no hub yet,
    or only a draft hub while ``include_drafts`` is false, fall back to nested
    ``votw-*.md`` lessons so hubs can roll out without hiding published content.
    """
    paths = [p for p in votw.glob("*.md") if _is_votw_lesson_path(p)]
    for lemma_dir in sorted(p for p in votw.iterdir() if p.is_dir()):
        hub = _votw_lemma_hub_path(lemma_dir)
        if hub is not None and (include_drafts or not is_draft(hub)):
            paths.append(hub)
            continue
        paths.extend(p for p in lemma_dir.glob("*.md") if _is_votw_lesson_path(p))
    return sorted(set(paths))


def _votw_href(locale: str, target: str, path: Path, slug: str) -> str:
    lemma = None if path.parent.name == "votw" else path.parent.name
    return votw_lesson_url(locale, target, slug, lemma=lemma)


def votw_links(
    content_root: Path, locale: str, target: str, *, include_drafts: bool = False
) -> list[dict[str, str]]:
    """Series index cards: lemma hubs + flat one-offs, newest date first."""
    items: list[tuple[date, dict[str, str]]] = []
    votw = content_root / locale / target / "votw"
    if not votw.is_dir():
        return []
    for path in _votw_series_list_paths(votw, include_drafts=include_drafts):
        post = frontmatter.load(path)
        meta = post.metadata
        source = f"{locale}/{target}/votw/{path.name}"
        if parse_draft(meta.get("draft"), source=source) and not include_drafts:
            continue
        slug = resolve_slug(meta, stem=path.stem, source=source)
        # Series list uses the body H1 (the verb / path title). Frontmatter
        # title is the full document <title> and is often longer.
        list_title = _list_title_from_post(post, path.stem)
        date_label = _format_date(meta.get("date"), locale)
        description = str(meta.get("description") or "").strip()
        level = _level_label(meta)
        items.append(
            (
                _frontmatter_sort_date(meta.get("date")),
                {
                    "title": list_title,
                    "date": date_label,
                    "description": description,
                    "level": level,
                    "href": _votw_href(locale, target, path, slug),
                },
            )
        )
    # Newest date first; equal dates: title Z→A, then href for a stable order.
    items.sort(
        key=lambda pair: (pair[0], pair[1]["title"], pair[1]["href"]),
        reverse=True,
    )
    return [item for _sort_date, item in items]


def recent_target_links(
    content_root: Path, locale: str, target: str, *, include_drafts: bool = False
) -> list[dict[str, str]]:
    """VOTW lessons + articles for one locale/target, newest date first."""
    chrome = chrome_for(locale)
    series_name = votw_series_label(locale, target)
    items: list[tuple[date, dict[str, str]]] = []

    votw = content_root / locale / target / "votw"
    if votw.is_dir():
        for path in _votw_lesson_paths(votw):
            post = frontmatter.load(path)
            meta = post.metadata
            source = f"{locale}/{target}/votw/{path.name}"
            if parse_draft(meta.get("draft"), source=source) and not include_drafts:
                continue
            slug = resolve_slug(meta, stem=path.stem, source=source)
            items.append(
                (
                    _frontmatter_sort_date(meta.get("date")),
                    {
                        "title": _list_title_from_post(post, path.stem),
                        "date": _format_date(meta.get("date"), locale),
                        "description": str(meta.get("description") or "").strip(),
                        "level": _level_label(meta),
                        "kind": series_name,
                        "href": _votw_href(locale, target, path, slug),
                    },
                )
            )

    articles = content_root / locale / target / ARTICLES_DIR
    if articles.is_dir():
        for path in articles.glob("*.md"):
            post = frontmatter.load(path)
            meta = post.metadata
            source = f"{locale}/{target}/{ARTICLES_DIR}/{path.name}"
            if parse_draft(meta.get("draft"), source=source) and not include_drafts:
                continue
            slug = resolve_slug(meta, stem=path.stem, source=source)
            items.append(
                (
                    _frontmatter_sort_date(meta.get("date")),
                    {
                        # Same as VOTW / related: list label is the body H1
                        # (emphasis stripped), not the document <title>.
                        "title": _list_title_from_post(post, path.stem),
                        "date": _format_date(meta.get("date"), locale),
                        "description": str(meta.get("description") or "").strip(),
                        "level": _level_label(meta),
                        "kind": chrome["article"],
                        "href": article_url(locale, target, slug),
                    },
                )
            )

    items.sort(
        key=lambda pair: (pair[0], pair[1]["title"], pair[1]["href"]),
        reverse=True,
    )
    return [item for _sort_date, item in items]
