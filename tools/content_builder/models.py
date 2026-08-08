"""Page models emitted by the content builder."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TocItem:
    id: str
    label: str


@dataclass
class Page:
    locale: str
    title: str
    description: str
    canonical_path: str
    eyebrow: str = ""
    heading_html: str = ""
    meta_line: str = ""
    body_html: str = ""
    after_body_html: str = ""
    # Prose after after_body_html (e.g. series index: intro, cards, then more copy).
    tail_body_html: str = ""
    toc: list[TocItem] = field(default_factory=list)
    related: list[dict[str, str]] = field(default_factory=list)
    active: str = ""
    show_hero_art: bool = False
    level: str = ""
    levels: list[str] = field(default_factory=list)
