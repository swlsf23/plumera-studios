"""Parse Markdown sources into page models."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import frontmatter
import markdown
from markdown.extensions.toc import slugify as md_slugify

from tools.content_builder.chrome import chrome_for, format_date, votw_series_label

SITE_ORIGIN = "https://plumerastudios.com"
CORE_SKIP = {"index.md"}  # landings are copied HTML; MD is reference-only
VOTW_INDEX_STEM = "index"  # series index; emitted at /{locale}/{target}/votw/
ARTICLES_DIR = "articles"  # standalone target-language pages (not a series)
WHATS_NEW_STEM = "whats-new"  # target hub: /{locale}/{target}/whats-new/
# Top-level content/ dirs that are not UI locales
CONTENT_NON_LOCALES = frozenset({"templates"})
CORE_DIR = "core"  # the one second-level dir with no target language


@dataclass
class TocItem:
    id: str
    label: str


@dataclass
class Page:
    locale: str
    title: str
    description: str
    canonical_path: str
    eyebrow: str = ""
    heading_html: str = ""
    meta_line: str = ""
    body_html: str = ""
    after_body_html: str = ""
    # Prose after after_body_html (e.g. series index: intro, cards, then more copy).
    tail_body_html: str = ""
    toc: list[TocItem] = field(default_factory=list)
    related: list[dict[str, str]] = field(default_factory=list)
    active: str = ""
    show_hero_art: bool = False
    level: str = ""


def slugify(value: str) -> str:
    return md_slugify(value, "-")


def _md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False, "slugify": md_slugify}},
    )


def _strip_tag(html: str, tag: str) -> tuple[str, str]:
    pattern = re.compile(rf"<{tag}[^>]*>(.*?)</{tag}>", re.I | re.S)
    match = pattern.search(html)
    if not match:
        return "", html
    inner = re.sub(r"<[^>]+>", "", match.group(1)).strip()
    rest = (html[: match.start()] + html[match.end() :]).lstrip()
    return inner, rest


# Localized Incorrect/Correct table headers (UI locale of the article).
_CORRECTION_HEADER_PAIRS = frozenset(
    {
        ("incorrect", "correct"),
        ("incorrecto", "correcto"),
    }
)

# Optional Markdown hint immediately above a table: <!-- table: forms -->
_TABLE_HINT_KINDS = {
    "example": "pair-table--example",
    "correction": "pair-table--correction",
    "forms": "pair-table--forms",
    "conjugation": "pair-table--forms",
}


def _classify_votw_tables(html: str) -> str:
    """Tag pair tables for CSS (hint comment, else header heuristics)."""

    def repl(match: re.Match[str]) -> str:
        hint = (match.group(1) or "").strip().lower()
        table = match.group(2)
        if 'class="' in table[:48].lower():
            return table
        kind = _TABLE_HINT_KINDS.get(hint)
        if kind is None:
            ths = re.findall(r"<th[^>]*>(.*?)</th>", table, re.I | re.S)
            labels = tuple(
                re.sub(r"<[^>]+>", "", th).strip().lower() for th in ths[:2]
            )
            kind = (
                "pair-table--correction"
                if labels in _CORRECTION_HEADER_PAIRS
                else "pair-table--example"
            )
        return re.sub(
            r"<table\b",
            f'<table class="pair-table {kind}"',
            table,
            count=1,
            flags=re.I,
        )

    return re.sub(
        r"(?:<!--\s*table:\s*(\w+)\s*-->\s*)?(<table\b[^>]*>.*?</table>)",
        repl,
        html,
        flags=re.I | re.S,
    )


def _inject_heading_ids(html: str) -> tuple[str, list[TocItem]]:
    toc: list[TocItem] = []
    used: dict[str, int] = {}

    def repl(match: re.Match[str]) -> str:
        level = match.group(1)
        attrs = match.group(2) or ""
        inner = match.group(3)
        label = re.sub(r"<[^>]+>", "", inner).strip()
        existing = re.search(r'\bid=["\']([^"\']+)["\']', attrs)
        if existing:
            hid = existing.group(1)
        else:
            base = slugify(label) or "section"
            count = used.get(base, 0)
            used[base] = count + 1
            hid = base if count == 0 else f"{base}-{count}"
            attrs = f'{attrs} id="{hid}"'.strip()
        if level == "2":
            toc.append(TocItem(id=hid, label=label))
        return f"<h{level} {attrs}>{inner}</h{level}>".replace(" >", ">")

    html = re.sub(r"<h([2-3])([^>]*)>(.*?)</h\1>", repl, html, flags=re.I | re.S)
    return html, toc


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


def parse_core_page(path: Path, locale: str) -> Page:
    raw = path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    body = post.content.strip()
    lines = body.splitlines()
    meta = post.metadata

    eyebrow = str(meta.get("eyebrow") or "").strip()
    if not eyebrow and lines and not lines[0].startswith("#") and lines[0].strip():
        eyebrow = lines[0].strip()
        body = "\n".join(lines[1:]).lstrip()

    html = _md_to_html(body)
    heading, html = _strip_tag(html, "h1")
    html, toc = _inject_heading_ids(html)

    stem = path.stem
    title = str(meta.get("title") or eyebrow or heading or stem)
    description = str(meta.get("description") or "")

    return Page(
        locale=locale,
        title=title,
        description=description,
        canonical_path=f"/{locale}/{stem}/",
        eyebrow=eyebrow,
        heading_html=heading.replace(" — ", "<br>") if " — " in heading else heading,
        body_html=html,
        toc=toc,
        related=_parse_related(meta, path),
        active=stem,
        show_hero_art=True,
    )


def parse_votw_page(path: Path, locale: str, target: str) -> Page:
    post = frontmatter.load(path)
    meta = post.metadata
    stem = path.stem
    meta_target = meta.get("target")
    if meta_target and str(meta_target) != target:
        print(
            f"warning: frontmatter target {str(meta_target)!r} disagrees with folder "
            f"{target!r} ({path}); the folder decides the URL",
            file=sys.stderr,
        )
    if "slug" in meta and meta["slug"] is not None:
        slug = str(meta["slug"])
        if slug != stem:
            print(
                f"warning: VOTW slug {slug!r} != filename stem {stem!r} ({path}); "
                f"emitting URL from slug, consider renaming the file to match",
                file=sys.stderr,
            )
    else:
        slug = stem
    title = str(meta.get("title") or stem)
    description = str(meta.get("description") or "")
    author = str(meta.get("author") or "")
    date_label = _format_date(meta.get("date"), locale)

    html = _md_to_html(post.content.strip())
    heading, html = _strip_tag(html, "h1")
    if not heading:
        heading = title
    html, toc = _inject_heading_ids(html)
    html = _classify_votw_tables(html)

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
    series = f"/{locale}/{target}/votw/"
    canonical_path = series if stem == VOTW_INDEX_STEM else f"{series}{slug}/"

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
        show_hero_art=True,
        level=str(meta.get("level") or "").strip(),
    )


def parse_article_page(path: Path, locale: str, target: str) -> Page:
    """Standalone page under content/{locale}/{target}/articles/."""
    post = frontmatter.load(path)
    meta = post.metadata
    stem = path.stem
    meta_target = meta.get("target")
    if meta_target and str(meta_target) != target:
        print(
            f"warning: frontmatter target {str(meta_target)!r} disagrees with folder "
            f"{target!r} ({path}); the folder decides the URL",
            file=sys.stderr,
        )
    if "slug" in meta and meta["slug"] is not None:
        slug = str(meta["slug"])
        if slug != stem:
            print(
                f"warning: article slug {slug!r} != filename stem {stem!r} ({path}); "
                f"emitting URL from slug, consider renaming the file to match",
                file=sys.stderr,
            )
    else:
        slug = stem
    title = str(meta.get("title") or stem)
    description = str(meta.get("description") or "")
    author = str(meta.get("author") or "")
    date_label = _format_date(meta.get("date"), locale)

    html = _md_to_html(post.content.strip())
    heading, html = _strip_tag(html, "h1")
    if not heading:
        heading = title
    html, toc = _inject_heading_ids(html)
    html = _classify_votw_tables(html)

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
    canonical_path = f"/{locale}/{target}/{ARTICLES_DIR}/{slug}/"

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
        show_hero_art=True,
        level=str(meta.get("level") or "").strip(),
    )


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
    return bool(post.metadata.get("draft"))


def discover_votw_pages(content_root: Path) -> list[tuple[Path, str, str]]:
    """Find content/{locale}/{target}/votw/*.md, series index.md included."""
    pages: list[tuple[Path, str, str]] = []
    for locale_dir in _locale_dirs(content_root):
        for target_dir in _target_dirs(locale_dir):
            votw = target_dir / "votw"
            if not votw.is_dir():
                continue
            for path in sorted(votw.glob("*.md")):
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


def parse_whats_new_page(path: Path, locale: str, target: str) -> Page:
    """Target-scoped recent-content page at /{locale}/{target}/whats-new/."""
    post = frontmatter.load(path)
    meta = post.metadata
    meta_target = meta.get("target")
    if meta_target and str(meta_target) != target:
        print(
            f"warning: frontmatter target {str(meta_target)!r} disagrees with folder "
            f"{target!r} ({path}); the folder decides the URL",
            file=sys.stderr,
        )

    title = str(meta.get("title") or chrome_for(locale)["whats_new"])
    description = str(meta.get("description") or "")
    html = _md_to_html(post.content.strip())
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
        canonical_path=f"/{locale}/{target}/{WHATS_NEW_STEM}/",
        eyebrow=eyebrow,
        heading_html=heading_html,
        body_html=html,
        toc=toc,
        related=_parse_related(meta, path),
        active=WHATS_NEW_STEM,
        show_hero_art=True,
    )


def _frontmatter_sort_date(value: object) -> date:
    """ISO date for sorting; unknown/missing sorts to the epoch (oldest)."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return date.fromisoformat(value.strip())
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


def votw_links(
    content_root: Path, locale: str, target: str, *, include_drafts: bool = False
) -> list[dict[str, str]]:
    """Article links for one series index, newest frontmatter date first."""
    items: list[tuple[date, dict[str, str]]] = []
    votw = content_root / locale / target / "votw"
    if not votw.is_dir():
        return []
    for path in votw.glob("*.md"):
        if path.stem == VOTW_INDEX_STEM:
            continue
        post = frontmatter.load(path)
        meta = post.metadata
        if meta.get("draft") and not include_drafts:
            continue
        slug = str(meta.get("slug") or path.stem)
        # Series list uses the body H1 (the verb). Frontmatter title is the
        # full document <title> and is often longer (series name + verb).
        list_title = _list_title_from_post(post, path.stem)
        date_label = _format_date(meta.get("date"), locale)
        description = str(meta.get("description") or "").strip()
        level = str(meta.get("level") or "").strip()
        items.append(
            (
                _frontmatter_sort_date(meta.get("date")),
                {
                    "title": list_title,
                    "date": date_label,
                    "description": description,
                    "level": level,
                    "href": f"/{locale}/{target}/votw/{slug}/",
                },
            )
        )
    items.sort(key=lambda pair: (pair[0], pair[1]["title"]), reverse=True)
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
        for path in votw.glob("*.md"):
            if path.stem == VOTW_INDEX_STEM:
                continue
            post = frontmatter.load(path)
            meta = post.metadata
            if meta.get("draft") and not include_drafts:
                continue
            slug = str(meta.get("slug") or path.stem)
            items.append(
                (
                    _frontmatter_sort_date(meta.get("date")),
                    {
                        "title": _list_title_from_post(post, path.stem),
                        "date": _format_date(meta.get("date"), locale),
                        "description": str(meta.get("description") or "").strip(),
                        "level": str(meta.get("level") or "").strip(),
                        "kind": series_name,
                        "href": f"/{locale}/{target}/votw/{slug}/",
                    },
                )
            )

    articles = content_root / locale / target / ARTICLES_DIR
    if articles.is_dir():
        for path in articles.glob("*.md"):
            post = frontmatter.load(path)
            meta = post.metadata
            if meta.get("draft") and not include_drafts:
                continue
            slug = str(meta.get("slug") or path.stem)
            items.append(
                (
                    _frontmatter_sort_date(meta.get("date")),
                    {
                        # Same as VOTW / related: list label is the body H1
                        # (emphasis stripped), not the document <title>.
                        "title": _list_title_from_post(post, path.stem),
                        "date": _format_date(meta.get("date"), locale),
                        "description": str(meta.get("description") or "").strip(),
                        "level": str(meta.get("level") or "").strip(),
                        "kind": chrome["article"],
                        "href": f"/{locale}/{target}/{ARTICLES_DIR}/{slug}/",
                    },
                )
            )

    items.sort(key=lambda pair: (pair[0], pair[1]["title"]), reverse=True)
    return [item for _sort_date, item in items]
