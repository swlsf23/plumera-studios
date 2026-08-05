"""UI chrome strings for emitted content pages (not landing pages).

If a locale is missing from CHROME or LANGUAGE_LABELS, the builder falls back
to English and prints a warning so new locales are not silently half-translated.
"""

from __future__ import annotations

import sys
from datetime import date

CHROME: dict[str, dict[str, str]] = {
    "en": {
        "brand_home": "Plumera Studios home",
        "home": "Home",
        "votw": "VOTW",
        "contact": "Contact",
        "privacy": "Privacy",
        "subscribe": "Subscribe",
        "choose_language": "Choose language",
        "menu": "Menu",
        "on_this_page": "On this page",
        "you_might_also_like": "You might also like",
        "follow_us": "Follow us:",
        "by_author": "By {author}",
        "article": "Article",
        "whats_new": "What's new",
        "level_prefix": "Level:",
        "catalog": "Catalog",
        "catalog_eyebrow": "Browse",
        "catalog_description": "Browse lessons and articles by level, type, and date.",
        "catalog_intro": "Filter and sort everything published for this learning path.",
        "catalog_filter_q": "Contains",
        "catalog_filter_q_placeholder": "e.g. être, passé composé",
        "catalog_filter_level": "Level",
        "catalog_filter_type": "Type",
        "catalog_filter_date": "Date",
        "catalog_filter_all": "All",
        "catalog_date_from": "From",
        "catalog_date_to": "To",
        "catalog_date_hint": "Leave blank for any date. Set both to the same day for one date.",
        "catalog_sort": "Sort",
        "catalog_sort_date_desc": "Date (newest first)",
        "catalog_sort_date_asc": "Date (oldest first)",
        "catalog_sort_level_asc": "Level (A1 → C2)",
        "catalog_sort_level_desc": "Level (C2 → A1)",
        "catalog_sort_type_asc": "Type (A → Z)",
        "catalog_sort_type_desc": "Type (Z → A)",
        "catalog_type_verb": "Verb",
        "catalog_type_grammar": "Grammar",
        "catalog_type_conjugation": "Conjugation",
        "catalog_type_vocabulary": "Vocabulary",
        "catalog_type_pronunciation": "Pronunciation",
        "catalog_empty": "No pages match these filters.",
        "copyright": "© 2026 Plumera Studios",
    },
    "es": {
        "brand_home": "Inicio de Plumera Studios",
        "home": "Inicio",
        "votw": "VOTW",
        "contact": "Contacto",
        "privacy": "Privacidad",
        "subscribe": "Suscribirse",
        "choose_language": "Elegir idioma",
        "menu": "Menú",
        "on_this_page": "En esta página",
        "you_might_also_like": "También te puede interesar",
        "follow_us": "Síguenos:",
        "by_author": "Por {author}",
        "article": "Artículo",
        "whats_new": "Novedades",
        "level_prefix": "Nivel:",
        "catalog": "Catálogo",
        "catalog_eyebrow": "Explorar",
        "catalog_description": "Explora lecciones y artículos por nivel, tipo y fecha.",
        "catalog_intro": "Filtra y ordena todo lo publicado en esta ruta de aprendizaje.",
        "catalog_filter_q": "Contiene",
        "catalog_filter_q_placeholder": "p. ej. être, passé composé",
        "catalog_filter_level": "Nivel",
        "catalog_filter_type": "Tipo",
        "catalog_filter_date": "Fecha",
        "catalog_filter_all": "Todos",
        "catalog_date_from": "Desde",
        "catalog_date_to": "Hasta",
        "catalog_date_hint": "Déjalo vacío para cualquier fecha. Usa el mismo día en ambos para una sola fecha.",
        "catalog_sort": "Orden",
        "catalog_sort_date_desc": "Fecha (más recientes)",
        "catalog_sort_date_asc": "Fecha (más antiguos)",
        "catalog_sort_level_asc": "Nivel (A1 → C2)",
        "catalog_sort_level_desc": "Nivel (C2 → A1)",
        "catalog_sort_type_asc": "Tipo (A → Z)",
        "catalog_sort_type_desc": "Tipo (Z → A)",
        "catalog_type_verb": "Verbo",
        "catalog_type_grammar": "Gramática",
        "catalog_type_conjugation": "Conjugación",
        "catalog_type_vocabulary": "Vocabulario",
        "catalog_type_pronunciation": "Pronunciación",
        "catalog_empty": "Ninguna página coincide con estos filtros.",
        "copyright": "© 2026 Plumera Studios",
    },
    "fr": {
        "brand_home": "Accueil Plumera Studios",
        "home": "Accueil",
        "votw": "VOTW",
        "contact": "Contact",
        "privacy": "Confidentialité",
        "subscribe": "S’abonner",
        "choose_language": "Choisir la langue",
        "menu": "Menu",
        "on_this_page": "Sur cette page",
        "you_might_also_like": "Vous aimerez aussi",
        "follow_us": "Suivez-nous :",
        "by_author": "Par {author}",
        "article": "Article",
        "whats_new": "Nouveautés",
        "level_prefix": "Niveau :",
        "catalog": "Catalogue",
        "catalog_eyebrow": "Parcourir",
        "catalog_description": "Parcourez les leçons et articles par niveau, type et date.",
        "catalog_intro": "Filtrez et triez tout ce qui est publié pour ce parcours.",
        "catalog_filter_q": "Contient",
        "catalog_filter_q_placeholder": "ex. être, passé composé",
        "catalog_filter_level": "Niveau",
        "catalog_filter_type": "Type",
        "catalog_filter_date": "Date",
        "catalog_filter_all": "Tous",
        "catalog_date_from": "Du",
        "catalog_date_to": "Au",
        "catalog_date_hint": "Laissez vide pour toute date. Même jour dans les deux champs pour une date précise.",
        "catalog_sort": "Trier",
        "catalog_sort_date_desc": "Date (plus récentes)",
        "catalog_sort_date_asc": "Date (plus anciennes)",
        "catalog_sort_level_asc": "Niveau (A1 → C2)",
        "catalog_sort_level_desc": "Niveau (C2 → A1)",
        "catalog_sort_type_asc": "Type (A → Z)",
        "catalog_sort_type_desc": "Type (Z → A)",
        "catalog_type_verb": "Verbe",
        "catalog_type_grammar": "Grammaire",
        "catalog_type_conjugation": "Conjugaison",
        "catalog_type_vocabulary": "Vocabulaire",
        "catalog_type_pronunciation": "Prononciation",
        "catalog_empty": "Aucune page ne correspond à ces filtres.",
        "copyright": "© 2026 Plumera Studios",
    },
}

LANGUAGE_LABELS = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
}

# Spelled-out VOTW series label for article eyebrows: locale → target → label.
# Nav chrome keeps the short "VOTW"; this is the reader-facing series name.
VOTW_SERIES: dict[str, dict[str, str]] = {
    "en": {
        "learn-french": "French Verb of the Week",
        "learn-spanish": "Spanish Verb of the Week",
    },
    "es": {
        "aprender-frances": "Verbo francés de la semana",
        "aprender-ingles": "Verbo inglés de la semana",
    },
    "fr": {
        "apprendre-anglais": "Verbe anglais de la semaine",
        "apprendre-espagnol": "Verbe espagnol de la semaine",
    },
}

MONTHS: dict[str, list[str]] = {
    "en": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ],
    "es": [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ],
    "fr": [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre",
    ],
}

DATE_FORMATS = {
    "en": "{month} {day}, {year}",
    "es": "{day} de {month} de {year}",
    "fr": "{day} {month} {year}",
}


def chrome_for(locale: str) -> dict[str, str]:
    """Return chrome copy for locale, falling back to English with a warning."""
    if locale in CHROME:
        return CHROME[locale]
    print(
        f"warning: no chrome strings for locale {locale!r}; falling back to 'en'",
        file=sys.stderr,
    )
    return CHROME["en"]


def votw_series_label(locale: str, target: str) -> str:
    """Spelled-out series name for a locale/target pair (article eyebrow)."""
    by_target = VOTW_SERIES.get(locale)
    if by_target is None:
        print(
            f"warning: no VOTW series labels for locale {locale!r}; falling back to 'en'",
            file=sys.stderr,
        )
        by_target = VOTW_SERIES["en"]
    label = by_target.get(target)
    if label is None:
        print(
            f"warning: no VOTW series label for locale {locale!r} target {target!r}; "
            f"using a fallback",
            file=sys.stderr,
        )
        return f"Verb of the Week ({target})"
    return label


def language_menu(locale: str, href_for) -> list[dict[str, str | bool]]:
    """Build language-switcher items; warn if a known chrome locale lacks a label."""
    codes = sorted(set(CHROME) | set(LANGUAGE_LABELS))
    items: list[dict[str, str | bool]] = []
    for code in codes:
        label = LANGUAGE_LABELS.get(code)
        if label is None:
            print(
                f"warning: no language label for locale {code!r}; using code as label",
                file=sys.stderr,
            )
            label = code
        items.append(
            {
                "code": code,
                "label": label,
                "href": href_for(code),
                "current": code == locale,
            }
        )
    return items


def format_date(value: date, locale: str) -> str:
    """Format a date in the locale's convention, falling back to English."""
    months = MONTHS.get(locale)
    if months is None:
        # Only warn for locales we otherwise support; chrome_for already
        # reports wholly unknown locales.
        if locale in CHROME:
            print(
                f"warning: no month names for locale {locale!r}; falling back to 'en'",
                file=sys.stderr,
            )
        months = MONTHS["en"]
    pattern = DATE_FORMATS.get(locale, DATE_FORMATS["en"])
    return pattern.format(day=value.day, month=months[value.month - 1], year=value.year)
