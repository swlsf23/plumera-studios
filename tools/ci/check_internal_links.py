"""Fail if dist/ HTML points at missing internal paths.

Resolves same-origin, root-relative, and page-relative hrefs against the built
tree. Directory URLs require an index.html (trailing-slash static hosting).
Fragment-only links and non-site schemes (mailto, external http(s), …) are ignored.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

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


def _page_url_for_html(html_path: Path, dist: Path) -> str:
    """Canonical-ish URL for a dist HTML file (base for relative resolution)."""
    rel = html_path.relative_to(dist).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    # Bare .html redirect stubs keep the filename so urljoin replaces that segment.
    return "/" + rel


def _local_path_from_ref(ref: str, *, page_url: str) -> str | None:
    """Return a site path to check, or None when the ref is out of scope."""
    ref = ref.strip()
    # Fragment-only (#section) and non-site schemes: OK / ignore.
    if not ref or ref.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None

    parsed = urlparse(ref)
    if parsed.scheme in ("http", "https"):
        if parsed.netloc and parsed.netloc != urlparse(SITE_ORIGIN).netloc:
            return None
        path = unquote(parsed.path or "/")
    elif parsed.scheme:
        # Other schemes (ftp, …) are not site paths.
        return None
    elif ref.startswith("/"):
        path = unquote(parsed.path)
    else:
        # Relative href: resolve against the containing page (origin + page URL).
        joined = urljoin(f"{SITE_ORIGIN}{page_url}", ref)
        joined_parsed = urlparse(joined)
        if joined_parsed.netloc != urlparse(SITE_ORIGIN).netloc:
            return None
        path = unquote(joined_parsed.path or "/")

    if not path.startswith("/"):
        path = "/" + path
    return path


def _exists_in_dist(url_path: str, dist: Path | None = None) -> bool:
    dist = dist if dist is not None else DIST
    rel = url_path.lstrip("/")
    if rel == "" or rel.endswith("/"):
        candidate = dist / rel / "index.html" if rel else dist / "index.html"
        return candidate.is_file()

    direct = dist / rel
    if direct.is_file():
        return True
    if direct.is_dir() and (direct / "index.html").is_file():
        return True
    # Bare .html redirect stubs and assets
    if not rel.endswith(".html") and (dist / f"{rel}.html").is_file():
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
        page_url = _page_url_for_html(html_path, DIST)
        for ref in _collect_refs(text):
            path = _local_path_from_ref(ref, page_url=page_url)
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
