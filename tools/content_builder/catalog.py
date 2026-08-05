"""Per-target catalog index (JSON) and generated catalog page (phase 1)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

import frontmatter

from tools.content_builder.chrome import chrome_for, format_date, votw_series_label
from tools.content_builder.parse import (
    ARTICLES_DIR,
    Page,
    _frontmatter_sort_date,
    _list_title_from_post,
    _votw_href,
    _votw_lesson_paths,
    is_draft,
)

CATALOG_STEM = "catalog"
SCHEMA_VERSION = 1

CEFR_LEVELS: tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")
CATALOG_TYPES: tuple[str, ...] = (
    "verb",
    "grammar",
    "conjugation",
    "vocabulary",
    "pronunciation",
)
LEVEL_RANK = {code: i for i, code in enumerate(CEFR_LEVELS)}
TYPE_RANK = {code: i for i, code in enumerate(CATALOG_TYPES)}


@dataclass(frozen=True)
class CatalogEntry:
    id: str
    title: str
    href: str
    date: str
    level: list[str]
    type: list[str]
    summary: str = ""
    kind: str = ""

    def to_json(self) -> dict[str, object]:
        out: dict[str, object] = {
            "id": self.id,
            "title": self.title,
            "href": self.href,
            "date": self.date,
            "level": list(self.level),
            "type": list(self.type),
        }
        if self.summary:
            out["summary"] = self.summary
        if self.kind:
            out["kind"] = self.kind
        return out

    def search_blob(self) -> str:
        """Lowercased title + summary for client text filter (not body)."""
        return f"{self.title} {self.summary}".casefold()


def normalize_str_list(value: object) -> list[str]:
    """Normalize frontmatter scalar / list / comma-string to a clean list."""
    if value is None:
        return []
    if isinstance(value, bool):
        return []
    if isinstance(value, (int, float)):
        text = str(value).strip()
        return [text] if text else []
    if isinstance(value, list):
        items: list[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                items.extend(_split_comma_parts(text))
        return items
    text = str(value).strip()
    if not text:
        return []
    return _split_comma_parts(text)


def _split_comma_parts(text: str) -> list[str]:
    if "," in text:
        return [part.strip() for part in text.split(",") if part.strip()]
    return [text]


def iso_date_string(value: object) -> str:
    """Return YYYY-MM-DD or empty if missing/unparseable."""
    if value is None or value == "":
        return ""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    return ""


def validate_levels(levels: list[str], *, source: str) -> list[str]:
    bad = [code for code in levels if code not in LEVEL_RANK]
    if bad:
        raise ValueError(f"{source}: unknown level(s) {bad}; allowed {list(CEFR_LEVELS)}")
    return levels


def validate_types(types: list[str], *, source: str) -> list[str]:
    bad = [code for code in types if code not in TYPE_RANK]
    if bad:
        raise ValueError(f"{source}: unknown type(s) {bad}; allowed {list(CATALOG_TYPES)}")
    return types


def _default_types_for_path(path: Path, meta: dict) -> list[str]:
    explicit = normalize_str_list(meta.get("type"))
    if explicit:
        return explicit
    # votw lessons default to verb; articles must set type explicitly.
    parts = path.parts
    if "votw" in parts and path.stem != "index":
        return ["verb"]
    return []


def discover_catalog_targets(content_root: Path) -> list[tuple[str, str]]:
    """Locale/target pairs that have at least one listable VOTW lesson or article."""
    found: set[tuple[str, str]] = set()
    for locale_dir in sorted(content_root.iterdir()):
        if not locale_dir.is_dir() or locale_dir.name == "templates":
            continue
        locale = locale_dir.name
        for target_dir in sorted(locale_dir.iterdir()):
            if not target_dir.is_dir() or target_dir.name == "core":
                continue
            target = target_dir.name
            votw = target_dir / "votw"
            articles = target_dir / ARTICLES_DIR
            has_votw = votw.is_dir() and any(_votw_lesson_paths(votw))
            has_articles = articles.is_dir() and any(articles.glob("*.md"))
            if has_votw or has_articles:
                found.add((locale, target))
    return sorted(found)


def build_catalog_entries(
    content_root: Path,
    locale: str,
    target: str,
    *,
    include_drafts: bool = False,
) -> list[CatalogEntry]:
    """Build catalog entries for one locale/target. Raises ValueError on bad metadata."""
    chrome = chrome_for(locale)
    series_name = votw_series_label(locale, target)
    items: list[tuple[date, CatalogEntry]] = []
    errors: list[str] = []

    votw = content_root / locale / target / "votw"
    if votw.is_dir():
        for path in _votw_lesson_paths(votw):
            draft = is_draft(path)
            if draft and not include_drafts:
                continue
            try:
                entry = _entry_from_votw(path, locale, target, series_name)
            except ValueError as exc:
                if draft and not include_drafts:
                    continue
                if draft:
                    print(f"warning: skip draft catalog entry: {exc}", file=sys.stderr)
                    continue
                errors.append(str(exc))
                continue
            items.append((_frontmatter_sort_date(frontmatter.load(path).metadata.get("date")), entry))

    articles = content_root / locale / target / ARTICLES_DIR
    if articles.is_dir():
        for path in sorted(articles.glob("*.md")):
            draft = is_draft(path)
            if draft and not include_drafts:
                continue
            try:
                entry = _entry_from_article(path, locale, target, chrome["article"])
            except ValueError as exc:
                if draft:
                    print(f"warning: skip draft catalog entry: {exc}", file=sys.stderr)
                    continue
                errors.append(str(exc))
                continue
            items.append((_frontmatter_sort_date(frontmatter.load(path).metadata.get("date")), entry))

    if errors:
        raise ValueError("catalog metadata errors:\n- " + "\n- ".join(errors))

    items.sort(key=lambda pair: (pair[0], pair[1].title), reverse=True)
    return [entry for _sort_date, entry in items]


def _entry_from_votw(
    path: Path, locale: str, target: str, kind: str
) -> CatalogEntry:
    post = frontmatter.load(path)
    meta = post.metadata
    source = f"{locale}/{target}/votw/{path.name}"
    rel = path.as_posix()
    if "/votw/" in rel:
        source = rel.split("/content/", 1)[-1] if "/content/" in rel else rel

    slug = str(meta.get("slug") or path.stem)
    levels = validate_levels(normalize_str_list(meta.get("level")), source=source)
    types = validate_types(_default_types_for_path(path, meta), source=source)
    date_s = iso_date_string(meta.get("date"))
    if not levels:
        raise ValueError(f"{source}: missing level")
    if not types:
        raise ValueError(f"{source}: missing type")
    if not date_s:
        raise ValueError(f"{source}: missing date")

    href = _votw_href(locale, target, path, slug)
    entry_id = href.strip("/")
    return CatalogEntry(
        id=entry_id,
        title=_list_title_from_post(post, path.stem),
        href=href,
        date=date_s,
        level=levels,
        type=types,
        summary=str(meta.get("description") or "").strip(),
        kind=kind,
    )


def _entry_from_article(
    path: Path, locale: str, target: str, kind: str
) -> CatalogEntry:
    post = frontmatter.load(path)
    meta = post.metadata
    source = f"{locale}/{target}/{ARTICLES_DIR}/{path.name}"
    slug = str(meta.get("slug") or path.stem)
    levels = validate_levels(normalize_str_list(meta.get("level")), source=source)
    types = validate_types(_default_types_for_path(path, meta), source=source)
    date_s = iso_date_string(meta.get("date"))
    if not levels:
        raise ValueError(f"{source}: missing level")
    if not types:
        raise ValueError(f"{source}: missing type (required for articles)")
    if not date_s:
        raise ValueError(f"{source}: missing date")

    href = f"/{locale}/{target}/{ARTICLES_DIR}/{slug}/"
    return CatalogEntry(
        id=href.strip("/"),
        title=_list_title_from_post(post, path.stem),
        href=href,
        date=date_s,
        level=levels,
        type=types,
        summary=str(meta.get("description") or "").strip(),
        kind=kind,
    )


def catalog_index_payload(
    locale: str, target: str, entries: list[CatalogEntry]
) -> dict[str, object]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "locale": locale,
        "target": target,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entries": [entry.to_json() for entry in entries],
    }


def write_catalog_index(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def make_catalog_page(locale: str, target: str) -> Page:
    chrome = chrome_for(locale)
    title = chrome["catalog"]
    intro = chrome["catalog_intro"]
    return Page(
        locale=locale,
        title=title,
        description=chrome["catalog_description"],
        canonical_path=f"/{locale}/{target}/{CATALOG_STEM}/",
        eyebrow=chrome["catalog_eyebrow"],
        heading_html=f"<h1>{escape(title)}</h1>",
        body_html=f"<p>{escape(intro)}</p>",
        active=CATALOG_STEM,
        show_hero_art=False,
    )


def _title_with_levels(title: str, levels: list[str]) -> str:
    title = title.strip()
    if not title or not levels:
        return title
    # Match site standard: append primary level when not already present.
    primary = levels[0]
    if title.endswith(primary):
        return title
    return f"{title} · {primary}"


def catalog_list_html(
    entries: list[CatalogEntry], aria_label: str, *, locale: str
) -> str:
    """Content-list markup with data attributes for client filter/sort."""
    if not entries:
        return (
            f'<nav class="content-list catalog-list" aria-label="{escape(aria_label)}">\n'
            f"<ul data-catalog-list></ul>\n"
            f"</nav>\n"
        )
    items: list[str] = []
    prev_date = None
    for entry in entries:
        raw_date = entry.date
        show_date = bool(raw_date) and raw_date != prev_date
        if raw_date:
            prev_date = raw_date
        date_label = ""
        if show_date and raw_date:
            try:
                date_label = format_date(date.fromisoformat(raw_date), locale)
            except ValueError:
                date_label = raw_date
        date_html = (
            f'\n      <span class="content-list__date">{escape(date_label)}</span>'
            if date_label
            else ""
        )
        kind_html = (
            f'\n      <p class="content-list__kind">{escape(entry.kind)}</p>'
            if entry.kind
            else ""
        )
        summary_html = (
            f'\n      <p class="content-list__summary">{escape(entry.summary)}</p>'
            if entry.summary
            else ""
        )
        levels_attr = " ".join(entry.level)
        types_attr = " ".join(entry.type)
        title = _title_with_levels(entry.title, entry.level)
        items.append(
            f'  <li class="content-list__item"\n'
            f'      data-date="{escape(entry.date)}"\n'
            f'      data-levels="{escape(levels_attr)}"\n'
            f'      data-types="{escape(types_attr)}"\n'
            f'      data-primary-level="{escape(entry.level[0])}"\n'
            f'      data-primary-type="{escape(entry.type[0])}"\n'
            f'      data-search="{escape(entry.search_blob())}">\n'
            f'    <div class="content-list__row">\n'
            f'      <a class="content-list__link" href="{escape(entry.href)}">'
            f'<span class="content-list__title">{escape(title)}</span></a>'
            f"{date_html}\n"
            f"    </div>"
            f"{kind_html}{summary_html}\n"
            f"  </li>"
        )
    return (
        f'<nav class="content-list catalog-list" aria-label="{escape(aria_label)}">\n'
        f"<ul data-catalog-list>\n"
        f"{chr(10).join(items)}\n"
        f"</ul>\n"
        f"</nav>\n"
    )


def catalog_controls_html(locale: str, entries: list[CatalogEntry]) -> str:
    """Filter/sort controls; level/type options only for values present in entries."""
    chrome = chrome_for(locale)
    levels_present = sorted(
        {code for entry in entries for code in entry.level},
        key=lambda c: LEVEL_RANK.get(c, 99),
    )
    types_present = sorted(
        {code for entry in entries for code in entry.type},
        key=lambda c: TYPE_RANK.get(c, 99),
    )

    def _options(values: list[str], labels: dict[str, str]) -> str:
        parts = [
            f'<option value="">{escape(chrome["catalog_filter_all"])}</option>'
        ]
        for value in values:
            label = labels.get(value, value)
            parts.append(f'<option value="{escape(value)}">{escape(label)}</option>')
        return "\n        ".join(parts)

    type_labels = {
        "verb": chrome["catalog_type_verb"],
        "grammar": chrome["catalog_type_grammar"],
        "conjugation": chrome["catalog_type_conjugation"],
        "vocabulary": chrome["catalog_type_vocabulary"],
        "pronunciation": chrome["catalog_type_pronunciation"],
    }
    level_labels = {code: code for code in CEFR_LEVELS}

    sort_options = "\n        ".join(
        [
            f'<option value="date-desc">{escape(chrome["catalog_sort_date_desc"])}</option>',
            f'<option value="date-asc">{escape(chrome["catalog_sort_date_asc"])}</option>',
            f'<option value="level-asc">{escape(chrome["catalog_sort_level_asc"])}</option>',
            f'<option value="level-desc">{escape(chrome["catalog_sort_level_desc"])}</option>',
            f'<option value="type-asc">{escape(chrome["catalog_sort_type_asc"])}</option>',
            f'<option value="type-desc">{escape(chrome["catalog_sort_type_desc"])}</option>',
        ]
    )

    return f"""\
<form class="catalog-controls" data-catalog-controls>
  <div class="catalog-controls__row">
    <label class="catalog-controls__field catalog-controls__field--q">
      <span class="catalog-controls__label">{escape(chrome["catalog_filter_q"])}</span>
      <input type="search" name="q" data-catalog-q autocomplete="off"
             placeholder="{escape(chrome["catalog_filter_q_placeholder"])}">
    </label>
    <label class="catalog-controls__field">
      <span class="catalog-controls__label">{escape(chrome["catalog_filter_level"])}</span>
      <select name="level" data-catalog-level>
        {_options(levels_present, level_labels)}
      </select>
    </label>
    <label class="catalog-controls__field">
      <span class="catalog-controls__label">{escape(chrome["catalog_filter_type"])}</span>
      <select name="type" data-catalog-type>
        {_options(types_present, type_labels)}
      </select>
    </label>
    <label class="catalog-controls__field">
      <span class="catalog-controls__label">{escape(chrome["catalog_sort"])}</span>
      <select name="sort" data-catalog-sort>
        {sort_options}
      </select>
    </label>
  </div>
  <fieldset class="catalog-controls__dates">
    <legend class="catalog-controls__label">{escape(chrome["catalog_filter_date"])}</legend>
    <label class="catalog-controls__field catalog-controls__field--date">
      <span class="catalog-controls__sublabel">{escape(chrome["catalog_date_from"])}</span>
      <input type="date" name="dateFrom" data-catalog-date-from>
    </label>
    <label class="catalog-controls__field catalog-controls__field--date">
      <span class="catalog-controls__sublabel">{escape(chrome["catalog_date_to"])}</span>
      <input type="date" name="dateTo" data-catalog-date-to>
    </label>
    <p class="catalog-controls__hint">{escape(chrome["catalog_date_hint"])}</p>
  </fieldset>
</form>
<p class="catalog-empty" data-catalog-empty hidden>{escape(chrome["catalog_empty"])}</p>
"""


def catalog_after_body_html(locale: str, entries: list[CatalogEntry]) -> str:
    chrome = chrome_for(locale)
    return catalog_controls_html(locale, entries) + catalog_list_html(
        entries, chrome["catalog"], locale=locale
    )
