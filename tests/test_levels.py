"""CEFR single-code and multi-level labels."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.content_builder.catalog import _title_with_levels
from tools.content_builder.levels import (
    format_level_labels,
    level_codes_for_page,
    level_label_for_page,
    normalize_level_list,
    ordered_levels,
    primary_level,
)
from tools.content_builder.parse import _level_label, parse_votw_page


class NormalizeLevelListTests(unittest.TestCase):
    def test_scalar_list_and_comma(self) -> None:
        self.assertEqual(normalize_level_list("B1"), ["B1"])
        self.assertEqual(normalize_level_list("B1,B2"), ["B1", "B2"])
        self.assertEqual(normalize_level_list(["B1", "B2"]), ["B1", "B2"])
        self.assertEqual(normalize_level_list(["B1, B2", "A2"]), ["B1", "B2", "A2"])


class FormatLevelLabelsTests(unittest.TestCase):
    def test_single_and_multi(self) -> None:
        self.assertEqual(format_level_labels(["A2"]), "A2")
        self.assertEqual(format_level_labels(["B2", "B1"]), "B1 B2")
        self.assertEqual(ordered_levels(["B2", "A2", "B1"]), ["A2", "B1", "B2"])
        # Primary is first author-declared value, not lowest CEFR code.
        self.assertEqual(primary_level(["B2", "B1"]), "B2")

    def test_all_level_reference_pages_omit_badge_label(self) -> None:
        all_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        self.assertEqual(level_label_for_page(all_levels), "")
        self.assertEqual(level_codes_for_page(all_levels), [])
        self.assertEqual(
            format_level_labels(all_levels),
            "A1 A2 B1 B2 C1 C2",
        )

    def test_title_with_levels_appends_codes(self) -> None:
        self.assertEqual(
            _title_with_levels("Faire idioms", ["B1", "B2"]),
            "Faire idioms · B1 B2",
        )
        self.assertEqual(_title_with_levels("Prendre", ["A1"]), "Prendre · A1")
        self.assertEqual(
            _title_with_levels("CEFR", ["A1", "A2", "B1", "B2", "C1", "C2"]),
            "CEFR",
        )


class PageLevelLabelTests(unittest.TestCase):
    def test_votw_page_badge_uses_separate_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "votw-sample-b1-b2.md"
            path.write_text(
                "---\n"
                'title: "Sample | Plumera"\n'
                "slug: votw-sample-b1-b2\n"
                "target: learn-french\n"
                "locale: en\n"
                "level: B1,B2\n"
                "date: 2026-08-07\n"
                "draft: false\n"
                "---\n\n"
                "# Sample\n\n"
                "Body.\n",
                encoding="utf-8",
            )
            page = parse_votw_page(path, "en", "learn-french")

        self.assertEqual(page.levels, ["B1", "B2"])
        self.assertEqual(page.level, "B1 B2")
        self.assertEqual(_level_label({"level": "B1,B2"}), "B1 B2")
        self.assertEqual(_level_label({"level": "A2"}), "A2")


if __name__ == "__main__":
    unittest.main()
