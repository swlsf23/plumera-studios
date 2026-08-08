"""Parse Markdown sources into page models.

Public import surface for the content builder. Implementation lives in
``constants``, ``models``, ``html_transform``, ``pages``, ``discover``, and
``lists``.
"""

from __future__ import annotations

from tools.content_builder.constants import (
    ARTICLES_DIR,
    CONTENT_NON_LOCALES,
    CORE_DIR,
    CORE_SKIP,
    SITE_ORIGIN,
    VOTW_INDEX_STEM,
    WHATS_NEW_STEM,
)
from tools.content_builder.discover import (
    discover_article_pages,
    discover_core_pages,
    discover_votw_pages,
    discover_whats_new_pages,
    is_draft,
)
from tools.content_builder.html_transform import (
    _classify_votw_tables,
    _inject_heading_ids,
    _md_to_html,
    _rewrite_local_images,
    _strip_tag,
    _tag_grammar_patterns,
    slugify,
)
from tools.content_builder.lists import (
    _frontmatter_sort_date,
    _list_title_from_post,
    _plain_list_title,
    _votw_href,
    _votw_lesson_paths,
    recent_target_links,
    votw_links,
)
from tools.content_builder.models import Page, TocItem
from tools.content_builder.pages import (
    _level_codes,
    _level_label,
    _levels_from_meta,
    parse_article_page,
    parse_core_page,
    parse_votw_page,
    parse_whats_new_page,
)

__all__ = [
    "ARTICLES_DIR",
    "CONTENT_NON_LOCALES",
    "CORE_DIR",
    "CORE_SKIP",
    "SITE_ORIGIN",
    "VOTW_INDEX_STEM",
    "WHATS_NEW_STEM",
    "Page",
    "TocItem",
    "discover_article_pages",
    "discover_core_pages",
    "discover_votw_pages",
    "discover_whats_new_pages",
    "is_draft",
    "parse_article_page",
    "parse_core_page",
    "parse_votw_page",
    "parse_whats_new_page",
    "recent_target_links",
    "slugify",
    "votw_links",
    "_classify_votw_tables",
    "_frontmatter_sort_date",
    "_inject_heading_ids",
    "_level_codes",
    "_level_label",
    "_levels_from_meta",
    "_list_title_from_post",
    "_md_to_html",
    "_plain_list_title",
    "_rewrite_local_images",
    "_strip_tag",
    "_tag_grammar_patterns",
    "_votw_href",
    "_votw_lesson_paths",
]
