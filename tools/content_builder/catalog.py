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
    CORE_DIR,
    Page,
    WHATS_NEW_STEM,
    _frontmatter_sort_date,
    _list_title_from_post,
    _votw_href,
    _votw_lesson_paths,
    is_draft,
)

CATALOG_STEM = "catalog"
SCHEMA_VERSION = 1

# Phase 1: only the English → French learning path. Locale-wide en/core guides
# (CEFR, exams) still appear in that catalog via catalog: true; es/fr catalogs
# are not emitted.
CATALOG_TARGETS: frozenset[tuple[str, str]] = frozenset({("en", "learn-french")})

CEFR_LEVELS: tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")
CATALOG_TYPES: tuple[str, ...] = (
    "verb",
    "grammar",
    "conjugation",
    "vocabulary",
    "pronunciation",
    "guide",
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
        """Unicode-casefolded title + summary for client text filter (not body).

        Must stay aligned with public/js/unicode-casefold.js (Python casefold).
        """
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
    """Locale/target pairs that get a catalog page (phase 1: en/learn-french only)."""
    return [
        (locale, target)
        for locale, target in sorted(CATALOG_TARGETS)
        if (content_root / locale / target).is_dir()
    ]


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

    # Locale-wide core pages (CEFR, exams, …) opt in with catalog: true.
    core = content_root / locale / CORE_DIR
    if core.is_dir():
        for path in sorted(core.glob("*.md")):
            if path.stem == "index":
                continue
            post = frontmatter.load(path)
            if not _catalog_opt_in(post.metadata):
                continue
            draft = is_draft(path)
            if draft and not include_drafts:
                continue
            try:
                entry = _entry_from_core(path, locale, post)
            except ValueError as exc:
                if draft:
                    print(f"warning: skip draft catalog entry: {exc}", file=sys.stderr)
                    continue
                errors.append(str(exc))
                continue
            items.append(
                (_frontmatter_sort_date(post.metadata.get("date")), entry)
            )

    if errors:
        raise ValueError("catalog metadata errors:\n- " + "\n- ".join(errors))

    items.sort(key=lambda pair: (pair[0], pair[1].title), reverse=True)
    return [entry for _sort_date, entry in items]


def _catalog_opt_in(meta: dict) -> bool:
    raw = meta.get("catalog")
    if raw is True:
        return True
    if isinstance(raw, str) and raw.strip().lower() in {"true", "yes", "1"}:
        return True
    return False


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


def _entry_from_core(path: Path, locale: str, post: object) -> CatalogEntry:
    meta = post.metadata
    source = f"{locale}/{CORE_DIR}/{path.name}"
    slug = str(meta.get("slug") or path.stem)
    levels = validate_levels(normalize_str_list(meta.get("level")), source=source)
    types = validate_types(normalize_str_list(meta.get("type")), source=source)
    date_s = iso_date_string(meta.get("date"))
    if not levels:
        raise ValueError(f"{source}: missing level")
    if not types:
        raise ValueError(f"{source}: missing type")
    if not date_s:
        raise ValueError(f"{source}: missing date")

    href = f"/{locale}/{slug}/"
    kind = str(meta.get("eyebrow") or "").strip()
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


def make_catalog_page(
    locale: str, target: str, *, content_root: Path | None = None
) -> Page:
    chrome = chrome_for(locale)
    title = chrome["catalog"]
    related: list[dict[str, str]] = []
    if content_root is not None:
        votw_index = content_root / locale / target / "votw" / "index.md"
        if votw_index.is_file() and not is_draft(votw_index):
            related.append({"href": f"/{locale}/{target}/votw/"})
        whats_new = content_root / locale / target / f"{WHATS_NEW_STEM}.md"
        if whats_new.is_file() and not is_draft(whats_new):
            related.append({"href": f"/{locale}/{target}/{WHATS_NEW_STEM}/"})
    else:
        related.append({"href": f"/{locale}/{target}/votw/"})
        related.append({"href": f"/{locale}/{target}/{WHATS_NEW_STEM}/"})
    return Page(
        locale=locale,
        title=title,
        description=chrome["catalog_description"],
        canonical_path=f"/{locale}/{target}/{CATALOG_STEM}/",
        eyebrow=chrome["catalog_eyebrow"],
        heading_html=escape(title),
        # Intro sits on the filters toolbar row (see catalog_controls_html).
        body_html="",
        related=related,
        active=CATALOG_STEM,
        show_hero_art=False,
    )


def _title_with_levels(title: str, levels: list[str]) -> str:
    title = title.strip()
    if not title or not levels:
        return title
    # Multi-level reference pages (e.g. CEFR guide) keep a bare title.
    if len(levels) != 1:
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
        date_html = ""
        if raw_date:
            try:
                date_label = format_date(date.fromisoformat(raw_date), locale)
            except ValueError:
                date_label = raw_date
            # Always emit a label node so JS can reveal it after filter/sort.
            hidden_attr = "" if show_date else " hidden"
            date_html = (
                f'\n      <span class="content-list__date"{hidden_attr}>'
                f"{escape(date_label)}</span>"
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

    def _level_options(values: list[str]) -> str:
        parts = [
            f'<option value="">{escape(chrome["catalog_filter_all"])}</option>'
        ]
        for value in values:
            parts.append(f'<option value="{escape(value)}">{escape(value)}</option>')
        return "\n        ".join(parts)

    type_labels = {
        "verb": chrome["catalog_type_verb"],
        "grammar": chrome["catalog_type_grammar"],
        "conjugation": chrome["catalog_type_conjugation"],
        "vocabulary": chrome["catalog_type_vocabulary"],
        "pronunciation": chrome["catalog_type_pronunciation"],
        "guide": chrome["catalog_type_guide"],
    }

    type_pills = [
        (
            f'<label class="catalog-pill">'
            f'<input type="radio" name="type" value="" data-catalog-type checked> '
            f'<span>{escape(chrome["catalog_filter_all"])}</span></label>'
        )
    ]
    for value in types_present:
        label = type_labels.get(value, value)
        type_pills.append(
            f'<label class="catalog-pill">'
            f'<input type="radio" name="type" value="{escape(value)}" data-catalog-type> '
            f"<span>{escape(label)}</span></label>"
        )
    type_pills_html = "\n      ".join(type_pills)

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

    total = len(entries)
    count_default = chrome["catalog_results_count"].replace("{n}", str(total))

    return f"""\
<form class="catalog-controls" data-catalog-controls
      data-chip-search="{escape(chrome["catalog_chip_search"])}"
      data-chip-date="{escape(chrome["catalog_chip_date"])}"
      data-count-all="{escape(chrome["catalog_results_count"])}"
      data-count-filtered="{escape(chrome["catalog_results_count_filtered"])}">
  <noscript>
    <p class="catalog-noscript">{escape(chrome["catalog_noscript"])}</p>
  </noscript>
  <div class="catalog-refine" data-catalog-enhance hidden>
    <p class="catalog-intro">{escape(chrome["catalog_intro"])}</p>
    <details class="catalog-controls__filters" data-catalog-filters>
      <summary class="catalog-controls__filters-summary">
        <span class="catalog-controls__filters-show">{escape(chrome["catalog_filters_show"])}</span>
        <span class="catalog-controls__filters-hide">{escape(chrome["catalog_filters_hide"])}</span>
        <span class="catalog-controls__filters-badge" data-catalog-filters-badge hidden></span>
      </summary>
      <div class="catalog-controls__panel">
        <label class="catalog-controls__field catalog-controls__field--q">
          <span class="catalog-controls__label">{escape(chrome["catalog_filter_q"])}</span>
          <input type="search" name="q" data-catalog-q autocomplete="off"
                 placeholder="{escape(chrome["catalog_filter_q_placeholder"])}">
        </label>
        <div class="catalog-controls__grid">
          <label class="catalog-controls__field catalog-controls__field--level">
            <span class="catalog-controls__label">{escape(chrome["catalog_filter_level"])}</span>
            <select name="level" data-catalog-level>
              {_level_options(levels_present)}
            </select>
          </label>
          <label class="catalog-controls__field catalog-controls__field--sort">
            <span class="catalog-controls__label">{escape(chrome["catalog_sort"])}</span>
            <select name="sort" data-catalog-sort>
              {sort_options}
            </select>
          </label>
          <fieldset class="catalog-controls__content">
            <legend class="catalog-controls__label">{escape(chrome["catalog_filter_type"])}</legend>
            <div class="catalog-controls__pills" role="radiogroup" aria-label="{escape(chrome["catalog_filter_type"])}">
              {type_pills_html}
            </div>
          </fieldset>
          <fieldset class="catalog-controls__dates" title="{escape(chrome["catalog_date_hint"])}"
                    aria-label="{escape(chrome["catalog_filter_date"])}">
            <div class="catalog-controls__dates-row">
              <label class="catalog-controls__field catalog-controls__field--date">
                <span class="catalog-controls__sublabel">{escape(chrome["catalog_date_from"])}</span>
                <input type="date" name="dateFrom" data-catalog-date-from>
              </label>
              <label class="catalog-controls__field catalog-controls__field--date">
                <span class="catalog-controls__sublabel">{escape(chrome["catalog_date_to"])}</span>
                <input type="date" name="dateTo" data-catalog-date-to>
              </label>
              <div class="catalog-controls__date-actions">
                <button type="button" class="catalog-controls__clear-dates" data-catalog-date-clear>
                  {escape(chrome["catalog_date_clear"])}
                </button>
              </div>
            </div>
          </fieldset>
        </div>
      </div>
    </details>
    <div class="catalog-chips" data-catalog-chips>
      <span class="catalog-chip catalog-chip--idle" data-catalog-chips-empty>
        {escape(chrome["catalog_chips_empty"])}
      </span>
    </div>
  </div>
</form>
<div class="catalog-meta">
  <p class="catalog-count" data-catalog-count>{escape(count_default)}</p>
</div>
<p class="catalog-empty" data-catalog-empty hidden>{escape(chrome["catalog_empty"])}</p>
"""


def catalog_after_body_html(locale: str, entries: list[CatalogEntry]) -> str:
    chrome = chrome_for(locale)
    return catalog_controls_html(locale, entries) + catalog_list_html(
        entries, chrome["catalog"], locale=locale
    )
