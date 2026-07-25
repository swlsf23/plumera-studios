"""UI chrome strings for emitted content pages (not landing pages).

If a locale is missing from CHROME or LANGUAGE_LABELS, the builder falls back
to English and prints a warning so new locales are not silently half-translated.
"""

from __future__ import annotations

import sys

CHROME: dict[str, dict[str, str]] = {
    "en": {
        "brand_home": "Plumera home",
        "home": "Home",
        "votd": "VOTD",
        "updates": "Updates",
        "privacy": "Privacy",
        "subscribe": "Subscribe",
        "choose_language": "Choose language",
        "menu": "Menu",
        "on_this_page": "On this page",
        "copyright": "© 2026 Plumera Studios",
    },
    "es": {
        "brand_home": "Inicio de Plumera",
        "home": "Inicio",
        "votd": "VOTD",
        "updates": "Novedades",
        "privacy": "Privacidad",
        "subscribe": "Suscribirse",
        "choose_language": "Elegir idioma",
        "menu": "Menú",
        "on_this_page": "En esta página",
        "copyright": "© 2026 Plumera Studios",
    },
    "fr": {
        "brand_home": "Accueil Plumera",
        "home": "Accueil",
        "votd": "VOTD",
        "updates": "Actualités",
        "privacy": "Confidentialité",
        "subscribe": "S’abonner",
        "choose_language": "Choisir la langue",
        "menu": "Menu",
        "on_this_page": "Sur cette page",
        "copyright": "© 2026 Plumera Studios",
    },
}

LANGUAGE_LABELS = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
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
