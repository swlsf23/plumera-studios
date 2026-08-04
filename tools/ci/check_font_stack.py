"""Fail if shipped CSS/HTML uses CSS family Inter or an unfingerprinted font URL.

Live pages register InterVariable as Plumera Sans so extension @font-face
rules named Inter cannot hijack the stack. Font URLs must carry ?v= when
deployed with long immutable Cache-Control.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCAN_ROOTS = (
    ROOT / "public",
    ROOT / "tools" / "content_builder" / "templates",
    ROOT / "dist",
)

# Non-shipped / fixture trees that must never trip this check if they appear
# under a scan root (e.g. future snapshots copied into public/ or dist/).
_SKIP_DIR_NAMES = frozenset(
    {
        "snapshots",
        "fixtures",
        "__snapshots__",
        "__fixtures__",
        "testdata",
        "test_fixtures",
    }
)

# font-family: …Inter… as a family token (not InterVariable in urls).
_FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;{}]+)", re.IGNORECASE)
_FAMILY_TOKEN_RE = re.compile(r"^[\"']?([^\"',]+)[\"']?$")
_FONT_URL_RE = re.compile(
    r"""url\(\s*["']?(/fonts/InterVariable\.woff2[^"')\s]*)["']?\s*\)""",
    re.IGNORECASE,
)
_QUERY_RE = re.compile(r"\?v=[A-Za-z0-9._-]+")


def _strip_css_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)


def _strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)


def _family_tokens(value: str) -> list[str]:
    tokens: list[str] = []
    for part in value.split(","):
        m = _FAMILY_TOKEN_RE.match(part.strip())
        if m:
            tokens.append(m.group(1).strip())
    return tokens


def _is_skipped(path: Path) -> bool:
    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
    return any(part in _SKIP_DIR_NAMES for part in parts)


def _scan_text(path: Path, text: str) -> list[str]:
    hits: list[str] = []
    try:
        rel = path.resolve().relative_to(ROOT)
    except ValueError:
        rel = path
    cleaned = _strip_html_comments(_strip_css_comments(text))

    for i, line in enumerate(cleaned.splitlines(), start=1):
        for m in _FONT_FAMILY_RE.finditer(line):
            for token in _family_tokens(m.group(1)):
                if token == "Inter":
                    hits.append(
                        f"{rel}:{i}: font-family uses CSS family Inter "
                        f"(use Plumera Sans)"
                    )
        for m in _FONT_URL_RE.finditer(line):
            url = m.group(1)
            if not _QUERY_RE.search(url):
                hits.append(
                    f"{rel}:{i}: font URL missing ?v= fingerprint: {url}"
                )
    return hits


def _iter_shipped_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if not root.is_dir():
            continue
        for pattern in ("*.html", "*.css"):
            for path in sorted(root.rglob(pattern)):
                if _is_skipped(path):
                    continue
                files.append(path)
    return files


def main() -> int:
    hits: list[str] = []
    for path in _iter_shipped_files():
        hits.extend(_scan_text(path, path.read_text(encoding="utf-8")))

    if hits:
        print("Font stack check failed:", file=sys.stderr)
        for hit in hits:
            print(f"  {hit}", file=sys.stderr)
        print(
            "Shipped pages must use font-family Plumera Sans and "
            "InterVariable.woff2?v=… URLs.",
            file=sys.stderr,
        )
        return 1

    print("Font stack check ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
