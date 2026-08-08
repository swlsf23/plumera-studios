"""Filesystem discovery of content Markdown sources."""

from __future__ import annotations

from pathlib import Path

import frontmatter

from tools.content_builder.constants import (
    ARTICLES_DIR,
    CONTENT_NON_LOCALES,
    CORE_DIR,
    CORE_SKIP,
    WHATS_NEW_STEM,
)
from tools.content_builder.frontmatter_validate import parse_draft

def _locale_dirs(content_root: Path) -> list[Path]:
    """UI locale folders under content/ (skips templates and other non-locales)."""
    if not content_root.is_dir():
        return []
    return sorted(
        path
        for path in content_root.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and path.name not in CONTENT_NON_LOCALES
    )


def _target_dirs(locale_dir: Path) -> list[Path]:
    """Target-language folders under a locale: everything beside core/."""
    return sorted(
        path
        for path in locale_dir.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name != CORE_DIR
    )


def discover_core_pages(content_root: Path) -> list[tuple[Path, str]]:
    """Find content/{locale}/core/*.md (except index.md)."""
    pages: list[tuple[Path, str]] = []
    for locale_dir in _locale_dirs(content_root):
        core = locale_dir / CORE_DIR
        if not core.is_dir():
            continue
        locale = locale_dir.name
        for path in sorted(core.glob("*.md")):
            if path.name in CORE_SKIP:
                continue
            pages.append((path, locale))
    return pages


def is_draft(path: Path) -> bool:
    """True when frontmatter sets draft: true (pages must not be emitted)."""
    post = frontmatter.load(path)
    return parse_draft(post.metadata.get("draft"), source=str(path))


def discover_votw_pages(content_root: Path) -> list[tuple[Path, str, str]]:
    """Find votw/*.md and votw/{lemma}/*.md under each locale/target."""
    pages: list[tuple[Path, str, str]] = []
    for locale_dir in _locale_dirs(content_root):
        for target_dir in _target_dirs(locale_dir):
            votw = target_dir / "votw"
            if not votw.is_dir():
                continue
            for path in sorted(votw.glob("*.md")):
                pages.append((path, locale_dir.name, target_dir.name))
            for path in sorted(votw.glob("*/*.md")):
                pages.append((path, locale_dir.name, target_dir.name))
    return pages


def discover_article_pages(content_root: Path) -> list[tuple[Path, str, str]]:
    """Find content/{locale}/{target}/articles/*.md (no series index)."""
    pages: list[tuple[Path, str, str]] = []
    for locale_dir in _locale_dirs(content_root):
        for target_dir in _target_dirs(locale_dir):
            articles = target_dir / ARTICLES_DIR
            if not articles.is_dir():
                continue
            for path in sorted(articles.glob("*.md")):
                pages.append((path, locale_dir.name, target_dir.name))
    return pages


def discover_whats_new_pages(content_root: Path) -> list[tuple[Path, str, str]]:
    """Find content/{locale}/{target}/whats-new.md."""
    pages: list[tuple[Path, str, str]] = []
    for locale_dir in _locale_dirs(content_root):
        for target_dir in _target_dirs(locale_dir):
            path = target_dir / f"{WHATS_NEW_STEM}.md"
            if path.is_file():
                pages.append((path, locale_dir.name, target_dir.name))
    return pages
