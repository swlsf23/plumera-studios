"""Sidebar content for emitted pages (related links, social)."""

from __future__ import annotations

RELATED_VOTW = [
    {
        "title": "Building trust through quality content",
        "meta": "May 5, 2024",
        "href": "/{locale}/votw/thoughtful-content/",
    },
    {
        "title": "Content that connects: a practical guide",
        "meta": "April 28, 2024",
        "href": "/{locale}/votw/thoughtful-content/",
    },
    {
        "title": "Sustainable content strategies for growth",
        "meta": "April 20, 2024",
        "href": "/{locale}/votw/thoughtful-content/",
    },
]

SOCIAL_LINKS = [
    {"id": "x", "label": "X", "href": "https://x.com/plumerastudios"},
    {"id": "youtube", "label": "YouTube", "href": "https://www.youtube.com/@plumerastudios"},
    {"id": "instagram", "label": "Instagram", "href": "https://www.instagram.com/plumerastudios"},
]


def related_for(locale: str) -> list[dict[str, str]]:
    return [
        {
            "title": item["title"],
            "meta": item["meta"],
            "href": item["href"].format(locale=locale),
        }
        for item in RELATED_VOTW
    ]
