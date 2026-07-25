"""UI chrome strings for emitted content pages (not landing pages).

If a locale is missing from CHROME or LANGUAGE_LABELS, the builder falls back
to English and prints a warning so new locales are not silently half-translated.
"""

from __future__ import annotations

import sys
from datetime import date

CHROME: dict[str, dict[str, str]] = {
    "en": {
        "brand_home": "Plumera home",
        "home": "Home",
        "votw": "VOTW",
        "updates": "Updates",
        "privacy": "Privacy",
        "subscribe": "Subscribe",
        "choose_language": "Choose language",
        "menu": "Menu",
        "on_this_page": "On this page",
        "related_votw": "Related VOTW",
        "follow_us": "Follow us:",
        "by_author": "By {author}",
        "copyright": "© 2026 Plumera Studios",
    },
    "es": {
        "brand_home": "Inicio de Plumera",
        "home": "Inicio",
        "votw": "VOTW",
        "updates": "Novedades",
        "privacy": "Privacidad",
        "subscribe": "Suscribirse",
        "choose_language": "Elegir idioma",
        "menu": "Menú",
        "on_this_page": "En esta página",
        "related_votw": "VOTW relacionados",
        "follow_us": "Síguenos:",
        "by_author": "Por {author}",
        "copyright": "© 2026 Plumera Studios",
    },
    "fr": {
        "brand_home": "Accueil Plumera",
        "home": "Accueil",
        "votw": "VOTW",
        "updates": "Actualités",
        "privacy": "Confidentialité",
        "subscribe": "S’abonner",
        "choose_language": "Choisir la langue",
        "menu": "Menu",
        "on_this_page": "Sur cette page",
        "related_votw": "VOTW associés",
        "follow_us": "Suivez-nous :",
        "by_author": "Par {author}",
        "copyright": "© 2026 Plumera Studios",
    },
}

LANGUAGE_LABELS = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
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
