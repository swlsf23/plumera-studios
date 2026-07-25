"""Sidebar content for emitted pages (related links, social)."""

from __future__ import annotations

RELATED_VOTW: list[dict[str, str]] = []

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
