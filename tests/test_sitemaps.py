"""Sitemap URL mapping from content paths and lastmod source rules."""

from __future__ import annotations

import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from tools.content_builder import sitemaps as sm


class ContentUrlMappingTests(unittest.TestCase):
    def test_maps_core_votw_article_whats_new(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = [
                (
                    root / "en" / "core" / "cefr.md",
                    "/en/cefr/",
                ),
                (
                    root / "en" / "core" / "index.md",
                    None,
                ),
                (
                    root / "en" / "learn-french" / "whats-new.md",
                    "/en/learn-french/whats-new/",
                ),
                (
                    root / "en" / "learn-french" / "votw" / "index.md",
                    "/en/learn-french/votw/",
                ),
                (
                    root / "en" / "learn-french" / "votw" / "votw-prendre-a1.md",
                    "/en/learn-french/votw/votw-prendre-a1/",
                ),
                (
                    root
                    / "en"
                    / "learn-french"
                    / "votw"
                    / "etre"
                    / "votw-etre-basics-a1.md",
                    "/en/learn-french/votw/etre/votw-etre-basics-a1/",
                ),
                (
                    root
                    / "en"
                    / "learn-french"
                    / "articles"
                    / "verb-prendre-b1.md",
                    "/en/learn-french/articles/verb-prendre-b1/",
                ),
                (
                    root / "templates" / "votw" / "en-fr.md",
                    None,
                ),
            ]
            with mock.patch.object(sm, "CONTENT", root):
                for path, want in cases:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("---\ntitle: t\n---\n\n# t\n", encoding="utf-8")
                    with self.subTest(path=str(path.relative_to(root))):
                        self.assertEqual(sm._content_url_for(path), want)


class LastmodTests(unittest.TestCase):
    def test_frontmatter_date_preferred_over_mtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.md"
            path.write_text(
                "---\ntitle: t\ndate: 2026-07-28\n---\n\n# t\n",
                encoding="utf-8",
            )
            # Make mtime clearly different from the frontmatter date.
            os.utime(path, (1_700_000_000, 1_700_000_000))
            self.assertEqual(sm._lastmod_for_source(path), "2026-07-28")

    def test_missing_frontmatter_date_uses_mtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.md"
            path.write_text("---\ntitle: t\n---\n\n# t\n", encoding="utf-8")
            os.utime(path, (1_700_000_000, 1_700_000_000))
            self.assertEqual(
                sm._lastmod_for_source(path),
                sm._iso(sm._mtime_date(path)),
            )

    def test_non_markdown_uses_mtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.html"
            path.write_text("<html></html>", encoding="utf-8")
            os.utime(path, (1_700_000_000, 1_700_000_000))
            self.assertEqual(
                sm._lastmod_for_source(path),
                sm._iso(sm._mtime_date(path)),
            )

    def test_entries_fallback_when_source_lastmod_missing(self) -> None:
        entries = sm._entries_with_lastmod(
            ["/en/orphan/", "/en/cefr/"],
            {"/en/cefr/": "2026-07-25"},
            fallback="2026-08-08",
        )
        self.assertEqual(
            entries,
            [
                ("/en/orphan/", "2026-08-08"),
                ("/en/cefr/", "2026-07-25"),
            ],
        )

    def test_iso_formats_date(self) -> None:
        self.assertEqual(sm._iso(date(2026, 1, 2)), "2026-01-02")


if __name__ == "__main__":
    unittest.main()
