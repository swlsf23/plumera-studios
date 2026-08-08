"""Canonical site URL and dist path assembly (pure string helpers).

Callers supply already-validated locale / target / slug / lemma. This module
does not parse frontmatter, walk the filesystem, or apply draft rules.
"""

from __future__ import annotations

from pathlib import Path

ARTICLES_SEGMENT = "articles"
VOTW_SEGMENT = "votw"
WHATS_NEW_SEGMENT = "whats-new"
CATALOG_SEGMENT = "catalog"


def core_url(locale: str, slug: str) -> str:
    """Core page: /{locale}/{slug}/."""
    return f"/{locale}/{slug}/"


def votw_series_url(locale: str, target: str) -> str:
    """VOTW series index: /{locale}/{target}/votw/."""
    return f"/{locale}/{target}/{VOTW_SEGMENT}/"


def votw_flat_url(locale: str, target: str, slug: str) -> str:
    """Flat VOTW lesson: /{locale}/{target}/votw/{slug}/."""
    return f"/{locale}/{target}/{VOTW_SEGMENT}/{slug}/"


def votw_nested_url(locale: str, target: str, lemma: str, slug: str) -> str:
    """Nested VOTW lesson: /{locale}/{target}/votw/{lemma}/{slug}/."""
    return f"/{locale}/{target}/{VOTW_SEGMENT}/{lemma}/{slug}/"


def votw_lesson_url(
    locale: str, target: str, slug: str, *, lemma: str | None = None
) -> str:
    """VOTW lesson URL; pass lemma for nested paths under votw/{lemma}/."""
    if lemma:
        return votw_nested_url(locale, target, lemma, slug)
    return votw_flat_url(locale, target, slug)


def article_url(locale: str, target: str, slug: str) -> str:
    """Standalone article: /{locale}/{target}/articles/{slug}/."""
    return f"/{locale}/{target}/{ARTICLES_SEGMENT}/{slug}/"


def whats_new_url(locale: str, target: str) -> str:
    """What's-new hub: /{locale}/{target}/whats-new/."""
    return f"/{locale}/{target}/{WHATS_NEW_SEGMENT}/"


def catalog_url(locale: str, target: str) -> str:
    """Catalog hub: /{locale}/{target}/catalog/."""
    return f"/{locale}/{target}/{CATALOG_SEGMENT}/"


def dist_path_for_url(dist: Path, canonical_url: str) -> Path:
    """Map a trailing-slash canonical URL to dist/.../index.html."""
    rel = canonical_url.strip("/")
    if not rel:
        return dist / "index.html"
    return dist.joinpath(*rel.split("/")) / "index.html"
