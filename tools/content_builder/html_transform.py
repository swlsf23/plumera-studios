"""Markdown → HTML and post-process transforms on emitted body HTML."""

from __future__ import annotations

import re
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify as md_slugify

from tools.content_builder.models import TocItem

def slugify(value: str) -> str:
    return md_slugify(value, "-")


def _md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False, "slugify": md_slugify}},
    )


def _rewrite_local_images(html: str, md_path: Path, locale: str) -> str:
    """Turn repo-relative img src into site URLs so MD preview and dist both work.

    Authors can use paths relative to the Markdown file (e.g. ``../../img/x.png``)
    for Cursor/VS Code preview. The build rewrites those to ``/{locale}/img/...``.
    """
    img_root: Path | None = None
    for parent in md_path.parents:
        candidate = parent / "img"
        if parent.name == locale and candidate.is_dir():
            img_root = candidate.resolve()
            break
        if parent.name == "content":
            break
    if img_root is None:
        return html

    def repl(match: re.Match[str]) -> str:
        src = match.group(1)
        if not src or src.startswith(("http://", "https://", "data:", "/")):
            return match.group(0)
        resolved = (md_path.parent / src).resolve()
        try:
            rel = resolved.relative_to(img_root)
        except ValueError:
            return match.group(0)
        if ".." in rel.parts:
            return match.group(0)
        return f'src="/{locale}/img/{rel.as_posix()}"'

    return re.sub(r'src="([^"]+)"', repl, html)


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


def _tag_grammar_patterns(html: str) -> str:
    """Optional Markdown hint above a pattern line: <!-- pattern -->."""

    def repl(match: re.Match[str]) -> str:
        paragraph = match.group(1)
        if re.search(r'\bclass="', paragraph[:48], flags=re.I):
            return paragraph
        return re.sub(
            r"<p\b",
            '<p class="grammar-pattern"',
            paragraph,
            count=1,
            flags=re.I,
        )

    return re.sub(
        r"<!--\s*pattern\s*-->\s*(<p\b[^>]*>.*?</p>)",
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
