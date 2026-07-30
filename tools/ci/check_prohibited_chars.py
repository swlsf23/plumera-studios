"""Fail if shippable site copy contains ';' or an em dash (U+2014).

Scans locale Markdown under content/ and prose text in public/**/*.html
(comments, tags, and HTML entities are stripped first). CSS/JS are ignored.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"

# Second-level dirs under content/ that are not UI locales.
CONTENT_NON_LOCALES = frozenset({"templates"})

PROHIBITED = (
    (";", "semicolon"),
    ("\u2014", "em dash"),
)

_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
_STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_ENTITY_RE = re.compile(r"&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);")


def _locale_content_files() -> list[Path]:
    if not CONTENT.is_dir():
        return []
    files: list[Path] = []
    for locale_dir in sorted(CONTENT.iterdir()):
        if not locale_dir.is_dir() or locale_dir.name in CONTENT_NON_LOCALES:
            continue
        if locale_dir.name.startswith("."):
            continue
        files.extend(sorted(locale_dir.rglob("*.md")))
    return files


def _html_prose(text: str) -> str:
    text = _COMMENT_RE.sub(" ", text)
    text = _SCRIPT_RE.sub(" ", text)
    text = _STYLE_RE.sub(" ", text)
    text = _TAG_RE.sub(" ", text)
    text = _ENTITY_RE.sub(" ", text)
    return text


def _find_hits(path: Path, text: str) -> list[str]:
    hits: list[str] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for char, label in PROHIBITED:
            if char in line:
                hits.append(f"{path.relative_to(ROOT)}:{i}: contains {label} ({char!r})")
    return hits


def main() -> int:
    hits: list[str] = []

    for path in _locale_content_files():
        hits.extend(_find_hits(path, path.read_text(encoding="utf-8")))

    if PUBLIC.is_dir():
        for path in sorted(PUBLIC.rglob("*.html")):
            prose = _html_prose(path.read_text(encoding="utf-8"))
            hits.extend(_find_hits(path, prose))

    if hits:
        print("Prohibited characters found in site content:", file=sys.stderr)
        for hit in hits:
            print(f"  {hit}", file=sys.stderr)
        print(
            "Remove ';' and em dashes (—) from shippable copy.",
            file=sys.stderr,
        )
        return 1

    print("ok: no prohibited ';' or em dash in shippable site content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
