"""Conjugation verb pages + shared verbs.json browse index (en/learn-french phase 1).

Verb paradigms are static HTML. Browse/filter uses one shared JSON index so pages
do not embed thousands of verb links.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html import escape
from pathlib import Path

from tools.content_builder.catalog import CEFR_LEVELS, LEVEL_RANK
from tools.content_builder.chrome import chrome_for
from tools.content_builder.parse import CONTENT_NON_LOCALES, CORE_DIR, Page

CONJUGATION_STEM = "conjugation"
VERBS_DIR = "verbs"
VERBS_JSON = "verbs.json"
SCHEMA_VERSION = 1

# Phase 1: same scope as catalog.
CONJUGATION_TARGETS: frozenset[tuple[str, str]] = frozenset({("en", "learn-french")})

_ROOT_ATTR_RE = re.compile(
    r"<div\s+class=\"conjugation-page\"([^>]*)>",
    re.IGNORECASE,
)
_ATTR_RE = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*"([^"]*)"')

# Toolbar lives in sticky chrome (title + finder + moods/voice); body keeps tables only.
_TOOLBAR_RE = re.compile(
    r'(<div\s+class="conjugation-toolbar">.*?</div>)\s*'
    r'(?=<div\s+class="conjugation-body">)',
    re.IGNORECASE | re.DOTALL,
)


def split_conjugation_toolbar(fragment_html: str) -> tuple[str, str]:
    """Return (toolbar_html, body_html_without_toolbar)."""
    match = _TOOLBAR_RE.search(fragment_html)
    if not match:
        return "", fragment_html
    toolbar = match.group(1).strip()
    body = (fragment_html[: match.start()] + fragment_html[match.end() :]).strip()
    if not body.endswith("\n"):
        body += "\n"
    return toolbar, body


@dataclass(frozen=True)
class ConjugationVerb:
    slug: str
    lemma: str
    cefr: str
    conjugation_class: str
    construction: str
    title: str
    description: str
    href: str
    fragment_html: str
    source: Path

    def search_blob(self) -> str:
        """Unicode-casefolded lemma (+ title) for client text filter."""
        return f"{self.lemma} {self.title}".casefold()

    def to_json(self) -> dict[str, str]:
        return {
            "slug": self.slug,
            "lemma": self.lemma,
            "cefr": self.cefr,
            "class": self.conjugation_class,
            "construction": self.construction,
            "href": self.href,
            "search": self.search_blob(),
        }


def _parse_attrs(attr_blob: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in _ATTR_RE.finditer(attr_blob)}


def parse_conjugation_fragment(path: Path) -> dict[str, str]:
    """Read required data-* attrs from a chrome-free conjugation fragment."""
    text = path.read_text(encoding="utf-8")
    match = _ROOT_ATTR_RE.search(text)
    if not match:
        raise ValueError(
            f"{path}: missing root <div class=\"conjugation-page\" …>"
        )
    attrs = _parse_attrs(match.group(1))
    required = (
        "data-lemma",
        "data-cefr",
        "data-conjugation-class",
        "data-construction",
        "data-title",
        "data-description",
    )
    missing = [key for key in required if not (attrs.get(key) or "").strip()]
    if missing:
        raise ValueError(f"{path}: missing attrs {', '.join(missing)}")
    cefr = attrs["data-cefr"].strip()
    if cefr not in CEFR_LEVELS:
        raise ValueError(f"{path}: invalid data-cefr {cefr!r}")
    return {
        "lemma": attrs["data-lemma"].strip(),
        "cefr": cefr,
        "conjugation_class": attrs["data-conjugation-class"].strip(),
        "construction": attrs["data-construction"].strip(),
        "title": attrs["data-title"].strip(),
        "description": attrs["data-description"].strip(),
        "fragment_html": text.strip() + "\n",
    }


def discover_conjugation_verbs(
    content_root: Path,
) -> list[tuple[Path, str, str]]:
    """Yield (path, locale, target) for conjugation verb fragments."""
    found: list[tuple[Path, str, str]] = []
    for locale_dir in sorted(content_root.iterdir()):
        if not locale_dir.is_dir() or locale_dir.name in CONTENT_NON_LOCALES:
            continue
        if locale_dir.name.startswith("."):
            continue
        locale = locale_dir.name
        for target_dir in sorted(locale_dir.iterdir()):
            if not target_dir.is_dir() or target_dir.name == CORE_DIR:
                continue
            if target_dir.name.startswith("."):
                continue
            target = target_dir.name
            if (locale, target) not in CONJUGATION_TARGETS:
                continue
            verbs = target_dir / CONJUGATION_STEM / VERBS_DIR
            if not verbs.is_dir():
                continue
            for path in sorted(verbs.glob("*.html")):
                found.append((path, locale, target))
    return found


def load_conjugation_verbs(content_root: Path) -> list[ConjugationVerb]:
    verbs: list[ConjugationVerb] = []
    for path, locale, target in discover_conjugation_verbs(content_root):
        meta = parse_conjugation_fragment(path)
        slug = path.stem
        href = f"/{locale}/{target}/{CONJUGATION_STEM}/{VERBS_DIR}/{slug}.html"
        verbs.append(
            ConjugationVerb(
                slug=slug,
                lemma=meta["lemma"],
                cefr=meta["cefr"],
                conjugation_class=meta["conjugation_class"],
                construction=meta["construction"],
                title=meta["title"],
                description=meta["description"],
                href=href,
                fragment_html=meta["fragment_html"],
                source=path,
            )
        )
    verbs.sort(key=lambda v: (v.lemma.casefold(), v.slug))
    return verbs


def verbs_json_payload(locale: str, target: str, verbs: list[ConjugationVerb]) -> dict:
    return {
        "version": SCHEMA_VERSION,
        "locale": locale,
        "target": target,
        "verbs": [verb.to_json() for verb in verbs],
    }


def write_verbs_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _class_label(value: str) -> str:
    return value.replace("_", " ")


def conjugation_filter_html(
    locale: str,
    target: str,
    verbs: list[ConjugationVerb],
    *,
    current_slug: str = "",
) -> str:
    """Left sidebar verb browser (corpus-generation viewer layout)."""
    chrome = chrome_for(locale)
    index_url = f"/{locale}/{target}/{CONJUGATION_STEM}/{VERBS_JSON}"
    levels_present = sorted(
        {verb.cefr for verb in verbs},
        key=lambda c: LEVEL_RANK.get(c, 99),
    )
    classes_present = sorted({verb.conjugation_class for verb in verbs})
    constructions_present = sorted({verb.construction for verb in verbs})

    def _options(values: list[str], *, label_fn=None) -> str:
        parts = [
            f'<option value="">{escape(chrome["conjugation_filter_all"])}</option>'
        ]
        for value in values:
            label = label_fn(value) if label_fn else value
            parts.append(
                f'<option value="{escape(value)}">{escape(label)}</option>'
            )
        return "\n            ".join(parts)

    current_attr = (
        f'\n      data-conjugation-current="{escape(current_slug)}"'
        if current_slug
        else ""
    )

    construction_field = ""
    if len(constructions_present) > 1:
        construction_field = f"""
          <label class="conjugation-sidebar__field">
            <span class="conjugation-sidebar__field-label">{escape(chrome["conjugation_filter_construction"])}</span>
            <select name="construction" data-conjugation-construction>
              {_options(constructions_present)}
            </select>
          </label>"""

    return f"""\
<form class="conjugation-sidebar" data-conjugation-controls
      data-conjugation-index-url="{escape(index_url)}"{current_attr}
      data-empty="{escape(chrome["conjugation_empty"])}"
      data-collapse-label="{escape(chrome["conjugation_sidebar_collapse"])}"
      data-expand-label="{escape(chrome["conjugation_sidebar_expand"])}">
  <noscript>
    <p class="catalog-noscript">{escape(chrome["conjugation_noscript"])}</p>
  </noscript>
  <nav class="conjugation-sidebar__nav" data-conjugation-enhance hidden aria-label="{escape(chrome["conjugation_list_label"])}">
    <section class="conjugation-nav-section">
      <div class="conjugation-nav-section__header">
        <span class="conjugation-nav-section__title">{escape(chrome["conjugation_list_label"])}</span>
        <span class="conjugation-nav-section__count" data-conjugation-count></span>
        <button type="button" class="conjugation-sidebar__toggle"
                data-conjugation-sidebar-toggle
                aria-expanded="true"
                aria-controls="conjugation-verb-list"
                aria-label="{escape(chrome["conjugation_sidebar_collapse"])}"
                title="{escape(chrome["conjugation_sidebar_collapse"])}">‹</button>
      </div>
      <div class="conjugation-nav-section__body" data-conjugation-sidebar-body>
        <label class="conjugation-sidebar__search">
          <span class="visually-hidden">{escape(chrome["conjugation_filter_q"])}</span>
          <input type="search" name="q" data-conjugation-q autocomplete="off"
                 placeholder="{escape(chrome["conjugation_filter_q_placeholder"])}"
                 aria-controls="conjugation-verb-list">
        </label>
        <div class="conjugation-sidebar__filters">
          <label class="conjugation-sidebar__field">
            <span class="conjugation-sidebar__field-label">{escape(chrome["conjugation_filter_level"])}</span>
            <select name="level" data-conjugation-level>
              {_options(levels_present)}
            </select>
          </label>
          <label class="conjugation-sidebar__field">
            <span class="conjugation-sidebar__field-label">{escape(chrome["conjugation_filter_class"])}</span>
            <select name="class" data-conjugation-class>
              {_options(classes_present, label_fn=_class_label)}
            </select>
          </label>{construction_field}
        </div>
        <ul id="conjugation-verb-list" class="lemma-list"
            data-conjugation-results hidden></ul>
        <p class="conjugation-sidebar__empty" data-conjugation-empty hidden></p>
      </div>
    </section>
  </nav>
</form>
"""


def make_conjugation_verb_page(
    verb: ConjugationVerb,
    locale: str,
    target: str,
    verbs: list[ConjugationVerb] | None = None,
) -> Page:
    """Chrome-wrapped verb page. Selector rail deferred (`verbs` unused for now)."""
    del target, verbs
    chrome = chrome_for(locale)
    toolbar, body = split_conjugation_toolbar(verb.fragment_html)
    return Page(
        locale=locale,
        title=verb.title,
        description=verb.description,
        canonical_path=verb.href,
        eyebrow=chrome["conjugation_eyebrow"],
        heading_html=escape(verb.lemma),
        body_html=body,
        after_body_html=toolbar,
        active="conjugation-verb",
        show_hero_art=False,
        level=verb.cefr,
    )


def default_conjugation_verb(verbs: list[ConjugationVerb]) -> ConjugationVerb:
    """Landing verb for /conjugation/ redirect (first by lemma sort)."""
    if not verbs:
        raise ValueError("no conjugation verbs to land on")
    return verbs[0]
