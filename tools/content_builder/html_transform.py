"""Markdown → HTML and DOM-based post-process transforms on body HTML."""

from __future__ import annotations

import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, Comment, Tag
from markdown.extensions.toc import slugify as md_slugify

from tools.content_builder.models import TocItem

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

_TABLE_HINT_RE = re.compile(r"^\s*table:\s*(\w+)\s*$", re.I)
_PATTERN_HINT_RE = re.compile(r"^\s*pattern\s*$", re.I)


def slugify(value: str) -> str:
    return md_slugify(value, "-")


def _md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False, "slugify": md_slugify}},
    )


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html or "", "html.parser")


def _fragment(soup: BeautifulSoup) -> str:
    """Serialize a fragment soup without wrapping html/body."""
    if soup.body is not None and soup.html is not None:
        return soup.body.decode_contents()
    return "".join(str(child) for child in soup.contents)


def _previous_comment(tag: Tag) -> Comment | None:
    """Nearest preceding HTML comment sibling, skipping whitespace text."""
    for sibling in tag.previous_siblings:
        if isinstance(sibling, Comment):
            return sibling
        if isinstance(sibling, str) and not str(sibling).strip():
            continue
        break
    return None


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

    soup = _soup(html)
    changed = False
    for img in soup.find_all("img"):
        if not isinstance(img, Tag):
            continue
        src = img.get("src")
        if not isinstance(src, str) or not src:
            continue
        if src.startswith(("http://", "https://", "data:", "/")):
            continue
        resolved = (md_path.parent / src).resolve()
        try:
            rel = resolved.relative_to(img_root)
        except ValueError:
            continue
        if ".." in rel.parts:
            continue
        img["src"] = f"/{locale}/img/{rel.as_posix()}"
        changed = True
    return _fragment(soup) if changed else html


def _strip_tag(html: str, tag: str) -> tuple[str, str]:
    soup = _soup(html)
    node = soup.find(tag)
    if not isinstance(node, Tag):
        return "", html
    inner = node.get_text(strip=True)
    node.extract()
    rest = _fragment(soup).lstrip()
    return inner, rest


def _classify_votw_tables(html: str) -> str:
    """Tag pair tables for CSS (hint comment, else header heuristics)."""
    soup = _soup(html)
    for table in soup.find_all("table"):
        if not isinstance(table, Tag):
            continue
        existing = table.get("class")
        if existing:
            continue
        hint = ""
        comment = _previous_comment(table)
        if comment is not None:
            match = _TABLE_HINT_RE.match(str(comment))
            if match:
                hint = match.group(1).strip().lower()
                comment.extract()
        kind = _TABLE_HINT_KINDS.get(hint)
        if kind is None:
            ths = table.find_all("th", limit=2)
            labels = tuple(th.get_text(strip=True).lower() for th in ths)
            kind = (
                "pair-table--correction"
                if labels in _CORRECTION_HEADER_PAIRS
                else "pair-table--example"
            )
        table["class"] = ["pair-table", kind]
    return _fragment(soup)


def _tag_grammar_patterns(html: str) -> str:
    """Optional Markdown hint above a pattern line: <!-- pattern -->."""
    soup = _soup(html)
    for comment in soup.find_all(string=lambda value: isinstance(value, Comment)):
        if not isinstance(comment, Comment):
            continue
        if not _PATTERN_HINT_RE.match(str(comment)):
            continue
        target: Tag | None = None
        for sibling in comment.next_siblings:
            if isinstance(sibling, Tag) and sibling.name == "p":
                target = sibling
                break
            if isinstance(sibling, str) and not str(sibling).strip():
                continue
            break
        if target is None:
            continue
        if target.has_attr("class"):
            comment.extract()
            continue
        target["class"] = ["grammar-pattern"]
        comment.extract()
    return _fragment(soup)


def _inject_heading_ids(html: str) -> tuple[str, list[TocItem]]:
    toc: list[TocItem] = []
    used: dict[str, int] = {}
    soup = _soup(html)
    for heading in soup.find_all(["h2", "h3"]):
        if not isinstance(heading, Tag):
            continue
        label = heading.get_text(strip=True)
        hid = heading.get("id")
        if isinstance(hid, str) and hid:
            pass
        else:
            base = slugify(label) or "section"
            count = used.get(base, 0)
            used[base] = count + 1
            hid = base if count == 0 else f"{base}-{count}"
            heading["id"] = hid
        if heading.name == "h2" and isinstance(hid, str):
            toc.append(TocItem(id=hid, label=label))
    return _fragment(soup), toc
