"""Strict frontmatter checks shared by emit paths and catalog builders."""

from __future__ import annotations

import re
from datetime import date, datetime

# URL path segment: lowercase kebab-case only (no /, .., empty, or mixed case).
_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_draft(value: object, *, source: str = "") -> bool:
    """Return whether the page is a draft.

    Absent/None → False. Only real YAML booleans are accepted; string
    ``"false"`` / ``"true"`` and other types hard-fail (no coercion).
    """
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    prefix = f"{source}: " if source else ""
    raise ValueError(
        f"{prefix}draft must be a YAML boolean (true/false), not {value!r}"
    )


def validate_slug(slug: object, *, stem: str, source: str) -> str:
    """Allowlist a URL-safe slug and require it to match the filename stem."""
    if not isinstance(slug, str) or not slug:
        raise ValueError(f"{source}: slug must be a non-empty string, got {slug!r}")
    if "/" in slug or "\\" in slug or ".." in slug or not _SLUG_RE.fullmatch(slug):
        raise ValueError(
            f"{source}: invalid slug {slug!r}; "
            f"use lowercase kebab-case (a-z, 0-9, hyphens)"
        )
    if slug != stem:
        raise ValueError(
            f"{source}: slug {slug!r} != filename stem {stem!r}"
        )
    return slug


def resolve_slug(meta: dict, *, stem: str, source: str) -> str:
    """Slug from frontmatter or stem; always validated against stem + allowlist."""
    if "slug" in meta and meta["slug"] is not None:
        raw = meta["slug"]
    else:
        raw = stem
    return validate_slug(raw, stem=stem, source=source)


def validate_target(meta_target: object, *, folder: str, source: str) -> None:
    """Hard-fail when frontmatter target disagrees with the folder target."""
    if meta_target is None or meta_target == "":
        return
    if str(meta_target) != folder:
        raise ValueError(
            f"{source}: frontmatter target {str(meta_target)!r} "
            f"!= folder {folder!r}"
        )


def validate_iso_date(value: object, *, source: str = "") -> date:
    """Parse a real calendar date (``date.fromisoformat``); reject fakes."""
    prefix = f"{source}: " if source else ""
    if value is None or value == "":
        raise ValueError(f"{prefix}missing date")
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError(f"{prefix}missing date")
        try:
            return date.fromisoformat(text)
        except ValueError as exc:
            raise ValueError(f"{prefix}invalid date {value!r}") from exc
    raise ValueError(
        f"{prefix}date must be a YAML date or ISO string (YYYY-MM-DD), "
        f"not {type(value).__name__} ({value!r})"
    )
