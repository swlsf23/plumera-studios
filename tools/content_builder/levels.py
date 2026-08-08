"""CEFR level parsing and display labels (single code or band)."""

from __future__ import annotations

CEFR_LEVELS: tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")
LEVEL_RANK = {code: i for i, code in enumerate(CEFR_LEVELS)}

# en dash between band ends (A2–B1), matching copy/style elsewhere on the site.
_BAND_SEP = "\u2013"


def normalize_level_list(value: object) -> list[str]:
    """Normalize frontmatter scalar / list / comma-string to CEFR codes (order kept)."""
    if value is None or value == "" or isinstance(value, bool):
        return []
    if isinstance(value, (int, float)):
        text = str(value).strip()
        return [text] if text else []
    if isinstance(value, list):
        items: list[str] = []
        for item in value:
            text = str(item).strip()
            if not text:
                continue
            items.extend(_split_comma_parts(text))
        return items
    return _split_comma_parts(str(value).strip())


def _split_comma_parts(text: str) -> list[str]:
    if not text:
        return []
    if "," in text:
        return [part.strip() for part in text.split(",") if part.strip()]
    return [text]


def ordered_levels(levels: list[str]) -> list[str]:
    """Unique levels sorted A1→C2; unknown codes keep stable tail order."""
    seen: set[str] = set()
    known: list[str] = []
    unknown: list[str] = []
    for code in levels:
        if code in seen:
            continue
        seen.add(code)
        if code in LEVEL_RANK:
            known.append(code)
        else:
            unknown.append(code)
    known.sort(key=lambda code: LEVEL_RANK[code])
    return known + unknown


def format_level_band(levels: list[str]) -> str:
    """Display label: A1, or B1–B2 for a multi-level band."""
    ordered = ordered_levels(levels)
    if not ordered:
        return ""
    if len(ordered) == 1:
        return ordered[0]
    return f"{ordered[0]}{_BAND_SEP}{ordered[-1]}"


def level_label_for_page(levels: list[str]) -> str:
    """Badge / card level label; omit for all-level reference pages (CEFR guide)."""
    ordered = ordered_levels(levels)
    if not ordered:
        return ""
    if len(ordered) >= len(CEFR_LEVELS) and set(ordered) >= set(CEFR_LEVELS):
        return ""
    return format_level_band(ordered)


def primary_level(levels: list[str]) -> str:
    """Lowest CEFR code in the set (sort / data-primary-level)."""
    ordered = ordered_levels(levels)
    return ordered[0] if ordered else ""
