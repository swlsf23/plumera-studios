"""Build dist/: copy public assets, emit content HTML, write sitemaps."""

from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tools.content_builder.chrome import chrome_for, language_menu
from tools.content_builder.parse import (
    SITE_ORIGIN,
    discover_core_pages,
    discover_votd_pages,
    parse_core_page,
    parse_votd_page,
)
from tools.content_builder.sitemaps import write_sitemaps

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"
DIST = ROOT / "dist"
TEMPLATES = Path(__file__).resolve().parent / "templates"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def _copy_public(dist: Path) -> None:
    if dist.exists():
        shutil.rmtree(dist)
    shutil.copytree(
        PUBLIC,
        dist,
        ignore=shutil.ignore_patterns("sitemap.xml"),
    )


def _lang_hrefs(locale: str, canonical_path: str) -> list[dict[str, str | bool]]:
    """Same path shape in each locale (self-canonical pages; no hreflang head tags)."""
    suffix = canonical_path[len(f"/{locale}") :]  # e.g. /updates.html or /votd/slug/

    def href_for(code: str) -> str:
        return f"/{code}{suffix}"

    return language_menu(locale, href_for)


def _write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def _canonical_url(page_path: str) -> str:
    if page_path.endswith("/"):
        return f"{SITE_ORIGIN}{page_path}"
    return f"{SITE_ORIGIN}{page_path}"


def build(dist: Path = DIST) -> int:
    env = _env()
    template = env.get_template("content_page.html")
    _copy_public(dist)

    emitted = 0

    for path, locale in discover_core_pages(CONTENT):
        page = parse_core_page(path, locale)
        html = template.render(
            page=page,
            chrome=chrome_for(locale),
            site_origin=SITE_ORIGIN,
            languages=_lang_hrefs(locale, page.canonical_path),
            canonical_url=_canonical_url(page.canonical_path),
        )
        out = dist / locale / f"{path.stem}.html"
        _write(out, html)
        emitted += 1

    for path, locale in discover_votd_pages(CONTENT):
        page = parse_votd_page(path, locale)
        html = template.render(
            page=page,
            chrome=chrome_for(locale),
            site_origin=SITE_ORIGIN,
            languages=_lang_hrefs(locale, page.canonical_path),
            canonical_url=_canonical_url(page.canonical_path),
        )
        # /en/votd/slug/ → en/votd/slug/index.html
        slug = page.canonical_path.rstrip("/").split("/")[-1]
        out = dist / locale / "votd" / slug / "index.html"
        _write(out, html)
        emitted += 1

    sitemaps = write_sitemaps(dist)
    print(f"Emitted {emitted} content pages into {dist}")
    print(f"Wrote {len(sitemaps)} sitemap files")
    return 0


def main() -> int:
    return build()


if __name__ == "__main__":
    raise SystemExit(main())
