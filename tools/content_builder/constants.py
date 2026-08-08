"""Shared content-builder path/URL constants."""

from __future__ import annotations

SITE_ORIGIN = "https://plumerastudios.com"
CORE_SKIP = {"index.md"}  # landings are copied HTML; MD is reference-only
VOTW_INDEX_STEM = "index"  # series index; emitted at /{locale}/{target}/votw/
ARTICLES_DIR = "articles"  # standalone target-language pages (not a series)
WHATS_NEW_STEM = "whats-new"  # target hub: /{locale}/{target}/whats-new/
# Top-level content/ dirs that are not UI locales
CONTENT_NON_LOCALES = frozenset({"templates"})
CORE_DIR = "core"  # the one second-level dir with no target language
