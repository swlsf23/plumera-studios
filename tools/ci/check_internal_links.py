"""Fail if dist/ HTML points at missing internal paths.

Resolves same-origin and root-relative hrefs against the built tree.
Directory URLs require an index.html (trailing-slash static hosting).
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
SITE_ORIGIN = "https://plumerastudios.com"

_HREF_RE = re.compile(
    r"""(?:href|src)\s*=\s*["']([^"']+)["']""",
    re.IGNORECASE,
)


class _HrefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k: v for k, v in attrs}
        for key in ("href", "src"):
            value = attr_map.get(key)
            if value:
                self.hrefs.append(value)


def _collect_refs(html: str) -> list[str]:
    parser = _HrefCollector()
    try:
        parser.feed(html)
        parser.close()
        if parser.hrefs:
            return parser.hrefs
    except Exception:
        pass
    return _HREF_RE.findall(html)


def _local_path_from_ref(ref: str) -> str | None:
    ref = ref.strip()
    if not ref or ref.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None

    parsed = urlparse(ref)
    if parsed.scheme in ("http", "https"):
        if parsed.netloc and parsed.netloc != urlparse(SITE_ORIGIN).netloc:
            return None
        path = unquote(parsed.path or "/")
    elif ref.startswith("/"):
        path = unquote(urlparse(ref).path)
    else:
        # Relative links are rare in this site; skip for now.
        return None

    if not path.startswith("/"):
        path = "/" + path
    return path


def _exists_in_dist(url_path: str) -> bool:
    rel = url_path.lstrip("/")
    if rel == "" or rel.endswith("/"):
        candidate = DIST / rel / "index.html" if rel else DIST / "index.html"
        return candidate.is_file()

    direct = DIST / rel
    if direct.is_file():
        return True
    if direct.is_dir() and (direct / "index.html").is_file():
        return True
    # Bare .html redirect stubs and assets
    if not rel.endswith(".html") and (DIST / f"{rel}.html").is_file():
        return True
    return False


def main() -> int:
    if not DIST.is_dir():
        print("dist/ missing; build the site first", file=sys.stderr)
        return 1

    missing: list[str] = []
    checked = 0

    for html_path in sorted(DIST.rglob("*.html")):
        # Skip tiny redirect stubs? Still check their links if any.
        text = html_path.read_text(encoding="utf-8")
        for ref in _collect_refs(text):
            path = _local_path_from_ref(ref)
            if path is None:
                continue
            checked += 1
            if not _exists_in_dist(path):
                missing.append(
                    f"{html_path.relative_to(DIST)}: broken {ref!r} → {path}"
                )

    if missing:
        # Unique, stable order
        for line in sorted(set(missing)):
            print(line, file=sys.stderr)
        print(
            f"Internal link check failed ({len(set(missing))} broken, {checked} checked)",
            file=sys.stderr,
        )
        return 1

    print(f"ok: internal links resolve ({checked} checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
