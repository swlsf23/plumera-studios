"""Build dist/: copy public assets, emit content HTML, write sitemaps.

Writes into a staging directory, then atomically replaces ``dist/`` only on
success so a failed build never leaves a half-written site.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

from tools.content_builder.assets import (
    CONTENT,
    DIST,
    PUBLIC,
    TEMPLATES,
    _copy_content_images,
    _copy_public,
    _env,
    _publish_dist,
    _write,
    _write_css_bundles,
    _write_redirect,
)
from tools.content_builder.casefold_js import write_casefold_js
from tools.content_builder.catalog import (
    CATALOG_STEM,
    build_catalog_entries,
    catalog_after_body_html,
    catalog_index_payload,
    discover_catalog_targets,
    make_catalog_page,
    write_catalog_index,
)
from tools.content_builder.constants import SITE_ORIGIN, VOTW_INDEX_STEM
from tools.content_builder.markers import (
    _content_list_html,
    _expand_art_bands,
    _place_title_hero,
    _split_at_list_marker,
    _title_with_level,
    _votw_list_html,
    _votw_nav_hrefs,
    _whats_new_list_html,
)
from tools.content_builder.parse import (
    discover_article_pages,
    discover_core_pages,
    discover_votw_pages,
    discover_whats_new_pages,
    is_draft,
    parse_article_page,
    parse_core_page,
    parse_votw_page,
    parse_whats_new_page,
)
from tools.content_builder.render import (
    _enrich_related,
    _plain_heading,
    _render_page,
)
from tools.content_builder.sitemaps import write_sitemaps
from tools.content_builder.urls import dist_path_for_url

# Re-exports for tests.
__all__ = [
    "build",
    "main",
    "_enrich_related",
    "_expand_art_bands",
    "_place_title_hero",
    "_split_at_list_marker",
    "_title_with_level",
]

def build(dist: Path = DIST, *, include_drafts: bool = False) -> int:
    # Validate catalog metadata before any staging write so a failed build
    # cannot leave a half site (e.g. nav → catalog 404).
    final_dist = Path(dist)
    catalog_by_target: dict[tuple[str, str], list] = {}
    for locale, target in discover_catalog_targets(CONTENT):
        try:
            catalog_by_target[(locale, target)] = build_catalog_entries(
                CONTENT, locale, target, include_drafts=include_drafts
            )
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    final_dist.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{final_dist.name}-staging-",
            dir=final_dist.parent,
        )
    )
    published = False
    try:
        env = _env()
        template = env.get_template("content_page.html")
        _copy_public(staging)
        _copy_content_images(staging)
        _write_css_bundles(staging)
        # Same Python casefold as CatalogEntry.search_blob() — emit per build so the
        # client helper always matches this interpreter’s Unicode tables.
        write_casefold_js(staging / "js" / "unicode-casefold.js")

        core_pages = [
            (parse_core_page(p, loc), p) for p, loc in discover_core_pages(CONTENT)
        ]

        # Always parse for related-link labels; only emit non-drafts unless --drafts.
        draft_hrefs: set[str] = set()
        votw_pages = []
        votw_for_index = []
        for path, locale, target in discover_votw_pages(CONTENT):
            page = parse_votw_page(path, locale, target)
            votw_for_index.append(page)
            if is_draft(path):
                draft_hrefs.add(page.canonical_path)
                if not include_drafts:
                    print(f"skip draft: {path.relative_to(CONTENT)}", file=sys.stderr)
                    continue
                print(f"emit draft: {path.relative_to(CONTENT)}", file=sys.stderr)
            votw_pages.append((page, path, target))

        article_pages = []
        article_for_index = []
        for path, locale, target in discover_article_pages(CONTENT):
            page = parse_article_page(path, locale, target)
            article_for_index.append(page)
            if is_draft(path):
                draft_hrefs.add(page.canonical_path)
                if not include_drafts:
                    print(f"skip draft: {path.relative_to(CONTENT)}", file=sys.stderr)
                    continue
                print(f"emit draft: {path.relative_to(CONTENT)}", file=sys.stderr)
            article_pages.append((page, path, target))

        whats_new_pages = []
        whats_new_for_index = []
        for path, locale, target in discover_whats_new_pages(CONTENT):
            page = parse_whats_new_page(path, locale, target)
            whats_new_for_index.append(page)
            if is_draft(path):
                draft_hrefs.add(page.canonical_path)
                if not include_drafts:
                    print(f"skip draft: {path.relative_to(CONTENT)}", file=sys.stderr)
                    continue
                print(f"emit draft: {path.relative_to(CONTENT)}", file=sys.stderr)
            whats_new_pages.append((page, path, target))

        for page, path in core_pages:
            if is_draft(path):
                draft_hrefs.add(page.canonical_path)

        votw_nav = _votw_nav_hrefs(
            [
                (page.locale, target)
                for page, path, target in votw_pages
                if path.stem == VOTW_INDEX_STEM
            ]
        )
        pages_by_href: dict[str, dict[str, str]] = {}
        for page in (
            *[p for p, _path in core_pages],
            *votw_for_index,
            *article_for_index,
            *whats_new_for_index,
        ):
            pages_by_href[page.canonical_path] = {
                "heading": _plain_heading(page.heading_html),
                "title": page.title,
                "level": page.level,
            }
        warn_draft_targets = not include_drafts
        emitted = 0

        for page, path in core_pages:
            html = _render_page(
                template,
                page,
                votw_nav,
                pages_by_href,
                source=str(path.relative_to(CONTENT)),
                draft_hrefs=draft_hrefs,
                warn_draft_targets=warn_draft_targets,
            )
            # /en/contact/ → en/contact/index.html (plain static hosting)
            stem = path.stem
            out = dist_path_for_url(staging, page.canonical_path)
            _write(out, html)
            # Keep /en/contact.html working via a static redirect stub
            _write_redirect(
                staging / page.locale / f"{stem}.html", page.canonical_path
            )
            emitted += 1

        for page, path, target in votw_pages:
            locale = page.locale
            source = str(path.relative_to(CONTENT))
            if path.stem == VOTW_INDEX_STEM:
                # List replaces <!-- votw: list --> (outside .article-body).
                lesson_list = _votw_list_html(locale, target, include_drafts)
                split = _split_at_list_marker(page.body_html, "votw", source=source)
                if split is None:
                    print(
                        f"warning: missing <!-- votw: list --> in {source}; "
                        f"appending the lesson list after the body",
                        file=sys.stderr,
                    )
                    page.after_body_html = lesson_list
                else:
                    page.body_html, page.tail_body_html = split
                    page.after_body_html = lesson_list
            out = dist_path_for_url(staging, page.canonical_path)
            _write(
                out,
                _render_page(
                    template,
                    page,
                    votw_nav,
                    pages_by_href,
                    source=source,
                    draft_hrefs=draft_hrefs,
                    warn_draft_targets=warn_draft_targets,
                ),
            )
            emitted += 1

        for page, path, target in article_pages:
            out = dist_path_for_url(staging, page.canonical_path)
            _write(
                out,
                _render_page(
                    template,
                    page,
                    votw_nav,
                    pages_by_href,
                    source=str(path.relative_to(CONTENT)),
                    draft_hrefs=draft_hrefs,
                    warn_draft_targets=warn_draft_targets,
                ),
            )
            emitted += 1

        for page, path, target in whats_new_pages:
            # List replaces <!-- whats-new: list --> (outside .article-body).
            source = str(path.relative_to(CONTENT))
            lesson_list = _whats_new_list_html(page.locale, target, include_drafts)
            split = _split_at_list_marker(page.body_html, "whats-new", source=source)
            if split is None:
                print(
                    f"warning: missing <!-- whats-new: list --> in {source}; "
                    f"appending the lesson list after the body",
                    file=sys.stderr,
                )
                page.after_body_html = lesson_list
            else:
                page.body_html, page.tail_body_html = split
                page.after_body_html = lesson_list
            out = dist_path_for_url(staging, page.canonical_path)
            _write(
                out,
                _render_page(
                    template,
                    page,
                    votw_nav,
                    pages_by_href,
                    source=source,
                    draft_hrefs=draft_hrefs,
                    warn_draft_targets=warn_draft_targets,
                ),
            )
            emitted += 1

        catalog_count = 0
        for (locale, target), entries in catalog_by_target.items():
            if not entries:
                continue
            payload = catalog_index_payload(locale, target, entries)
            page = make_catalog_page(locale, target, content_root=CONTENT)
            catalog_html = dist_path_for_url(staging, page.canonical_path)
            write_catalog_index(catalog_html.parent / "index.json", payload)
            page.after_body_html = catalog_after_body_html(locale, entries)
            _write(
                catalog_html,
                _render_page(
                    template,
                    page,
                    votw_nav,
                    pages_by_href,
                    source=f"{locale}/{target}/{CATALOG_STEM}/",
                    draft_hrefs=draft_hrefs,
                    warn_draft_targets=warn_draft_targets,
                ),
            )
            catalog_count += 1
            emitted += 1

        sitemaps = write_sitemaps(staging)
        _publish_dist(staging, final_dist)
        published = True
        print(f"Emitted {emitted} content pages into {final_dist}")
        print(f"Wrote {catalog_count} catalog indexes")
        print(f"Wrote {len(sitemaps)} sitemap files")
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        if not published and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


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
