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

from tools.content_builder.chrome import chrome_for, format_date

SITE_ORIGIN = "https://plumerastudios.com"
CORE_SKIP = {"index.md"}  # landings are copied HTML; MD is reference-only
VOTW_SKIP = {"index.md"}  # series intros — not emitted as verb articles (yet)
# Top-level content/ dirs that are not UI locales
CONTENT_NON_LOCALES = frozenset({"templates"})


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
    dek: str = ""
    meta_line: str = ""
    body_html: str = ""
    toc: list[TocItem] = field(default_factory=list)
    active: str = ""
    show_hero_art: bool = False


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


def _extract_dek(html: str) -> tuple[str, str]:
    match = re.match(r"<p>(.*?)</p>\s*", html, re.I | re.S)
    if not match:
        return "", html
    dek = re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return dek, html[match.end() :].lstrip()


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


def parse_core_page(path: Path, locale: str) -> Page:
    raw = path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    body = post.content.strip()
    lines = body.splitlines()

    eyebrow = ""
    if lines and not lines[0].startswith("#") and lines[0].strip():
        eyebrow = lines[0].strip()
        body = "\n".join(lines[1:]).lstrip()

    meta = post.metadata
    html = _md_to_html(body)
    heading, html = _strip_tag(html, "h1")
    dek, html = _extract_dek(html)
    html, toc = _inject_heading_ids(html)

    stem = path.stem
    title = str(meta.get("title") or eyebrow or heading or stem)
    description = str(meta.get("description") or dek)
    page_title = f"{title} — Plumera Studios" if "Plumera" not in title else title

    return Page(
        locale=locale,
        title=page_title,
        description=description,
        canonical_path=f"/{locale}/{stem}/",
        eyebrow=eyebrow,
        heading_html=heading.replace(" — ", "<br>") if " — " in heading else heading,
        dek=dek,
        body_html=html,
        toc=toc,
        active=stem,
    )


def parse_votw_page(path: Path, locale: str) -> Page:
    post = frontmatter.load(path)
    meta = post.metadata
    stem = path.stem
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
    category = str(meta.get("category") or "VOTW")
    author = str(meta.get("author") or "")
    date_label = _format_date(meta.get("date"), locale)

    html = _md_to_html(post.content.strip())
    heading, html = _strip_tag(html, "h1")
    if not heading:
        heading = title
    dek_from_body, html = _extract_dek(html)
    if not description:
        description = dek_from_body
    dek = description or dek_from_body
    html, toc = _inject_heading_ids(html)

    meta_parts: list[str] = []
    if author:
        meta_parts.append(chrome_for(locale)["by_author"].format(author=author))
    if date_label:
        meta_parts.append(date_label)
    meta_line = " · ".join(meta_parts)

    heading_html = heading.replace(" — ", "<br>") if " — " in heading else heading

    return Page(
        locale=locale,
        title=f"{title} — Plumera Studios",
        description=description,
        canonical_path=f"/{locale}/votw/{slug}/",
        eyebrow=category,
        heading_html=heading_html,
        dek=dek,
        meta_line=meta_line,
        body_html=html,
        toc=toc,
        active="votw",
        show_hero_art=True,
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


def discover_core_pages(content_root: Path) -> list[tuple[Path, str]]:
    """Find content/{locale}/core/*.md (except index.md)."""
    pages: list[tuple[Path, str]] = []
    for locale_dir in _locale_dirs(content_root):
        core = locale_dir / "core"
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


def discover_votw_pages(content_root: Path) -> list[tuple[Path, str]]:
    """Find content/{locale}/learn/votw/*.md (except series index.md)."""
    pages: list[tuple[Path, str]] = []
    for locale_dir in _locale_dirs(content_root):
        votw = locale_dir / "learn" / "votw"
        if not votw.is_dir():
            continue
        locale = locale_dir.name
        for path in sorted(votw.glob("*.md")):
            if path.name in VOTW_SKIP:
                continue
            pages.append((path, locale))
    return pages
