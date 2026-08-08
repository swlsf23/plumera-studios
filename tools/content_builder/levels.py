"""CEFR level parsing and display labels (one or more codes)."""

from __future__ import annotations

CEFR_LEVELS: tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")
LEVEL_RANK = {code: i for i, code in enumerate(CEFR_LEVELS)}

# Between codes in a multi-level list/card suffix (Title · B1 B2).
_LABEL_SEP = " "


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


def format_level_labels(levels: list[str]) -> str:
    """Join codes for list/card suffixes: A1, or B1 B2."""
    ordered = ordered_levels(levels)
    if not ordered:
        return ""
    return _LABEL_SEP.join(ordered)


# Back-compat alias for callers that still import the old name.
format_level_band = format_level_labels


def level_codes_for_page(levels: list[str]) -> list[str]:
    """Badge codes; omit for all-level reference pages (CEFR guide)."""
    ordered = ordered_levels(levels)
    if not ordered:
        return []
    if len(ordered) >= len(CEFR_LEVELS) and set(ordered) >= set(CEFR_LEVELS):
        return []
    return ordered


def level_label_for_page(levels: list[str]) -> str:
    """Joined list/card level label; empty when there are no page codes."""
    return format_level_labels(level_codes_for_page(levels))


def primary_level(levels: list[str]) -> str:
    """First author-declared CEFR code (catalog sort / data-primary-level)."""
    for code in levels:
        text = str(code).strip()
        if text:
            return text
    return ""
