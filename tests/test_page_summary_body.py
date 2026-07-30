"""Regression: description is summary; first body paragraph stays in the body."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.content_builder.parse import parse_votw_page


class PageSummaryBodyTests(unittest.TestCase):
    def test_description_present_keeps_first_body_paragraph(self) -> None:
        md = """---
title: "French Verb of the Week | Plumera"
description: One French verb at a time.
slug: index
target: learn-french
locale: en
draft: false
---

# French Verb of the Week

**French Verb of the Week** walks you through one French verb at a time.

## Learning with Plumera

More prose here.
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.md"
            path.write_text(md, encoding="utf-8")
            page = parse_votw_page(path, "en", "learn-french")

        self.assertEqual(page.description, "One French verb at a time.")
        self.assertIn(
            "walks you through one French verb at a time",
            page.body_html,
        )
        self.assertTrue(
            page.body_html.lstrip().startswith("<p>"),
            msg="first body paragraph should remain in body_html",
        )

    def test_missing_description_means_no_summary_not_body_extraction(self) -> None:
        md = """---
title: "Test | Plumera"
slug: index
target: learn-french
locale: en
draft: false
---

# Test

First paragraph stays in the body.

Second paragraph too.
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.md"
            path.write_text(md, encoding="utf-8")
            page = parse_votw_page(path, "en", "learn-french")

        self.assertEqual(page.description, "")
        self.assertIn("First paragraph stays in the body", page.body_html)
        self.assertIn("Second paragraph too", page.body_html)


class ListMarkerTests(unittest.TestCase):
    def test_missing_marker_returns_none(self) -> None:
        from tools.content_builder.build import _split_at_list_marker

        self.assertIsNone(_split_at_list_marker("<p>hi</p>", "votw"))

    def test_first_of_multiple_markers_wins(self) -> None:
        from tools.content_builder.build import _split_at_list_marker
        import io
        from contextlib import redirect_stderr

        html = "<p>a</p><!-- votw: list --><p>b</p><!-- votw: list --><p>c</p>"
        buf = io.StringIO()
        with redirect_stderr(buf):
            split = _split_at_list_marker(html, "votw", source="fixture.md")
        self.assertIsNotNone(split)
        before, after = split
        self.assertEqual(before, "<p>a</p>")
        self.assertIn("<p>b</p>", after)
        self.assertIn("<!-- votw: list -->", after)
        self.assertIn("multiple", buf.getvalue())
        self.assertIn("fixture.md", buf.getvalue())


class ArtBandMarkerTests(unittest.TestCase):
    def test_expands_every_marker(self) -> None:
        from tools.content_builder.build import _expand_art_bands

        html = "<p>a</p><!-- art: band --><h2>Mid</h2><!-- art: band --><p>b</p>"
        out = _expand_art_bands(html)
        self.assertEqual(out.count("hero-art--inline"), 2)
        self.assertEqual(out.count("hero-art-slot"), 2)
        self.assertNotIn("<!-- art: band -->", out)
        self.assertIn("<h2>Mid</h2>", out)

    def test_leaves_html_without_marker(self) -> None:
        from tools.content_builder.build import _expand_art_bands

        html = "<p>plain</p>"
        self.assertEqual(_expand_art_bands(html), html)


if __name__ == "__main__":
    unittest.main()
