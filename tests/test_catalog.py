"""Catalog index + page emission (filterable content phase 1)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.content_builder.build import build
from tools.content_builder.catalog import (
    CATALOG_TYPES,
    build_catalog_entries,
    catalog_controls_html,
    normalize_str_list,
    validate_types,
)


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


class NormalizeListTests(unittest.TestCase):
    def test_scalar_and_list_and_comma(self) -> None:
        self.assertEqual(normalize_str_list("A1"), ["A1"])
        self.assertEqual(normalize_str_list(["A1", "A2"]), ["A1", "A2"])
        self.assertEqual(normalize_str_list("verb, grammar"), ["verb", "grammar"])


class CatalogIndexTests(unittest.TestCase):
    def test_en_learn_french_entries(self) -> None:
        entries = build_catalog_entries(CONTENT, "en", "learn-french")
        self.assertGreaterEqual(len(entries), 8)
        hrefs = {e.href for e in entries}
        self.assertIn("/en/learn-french/votw/etre/votw-etre-basics-a1/", hrefs)
        self.assertIn("/en/learn-french/articles/passe-compose-avoir-etre/", hrefs)
        for entry in entries:
            self.assertTrue(entry.level)
            self.assertTrue(entry.type)
            self.assertTrue(entry.date)
            for code in entry.type:
                self.assertIn(code, CATALOG_TYPES)

    def test_drafts_excluded_by_default(self) -> None:
        entries = build_catalog_entries(CONTENT, "es", "aprender-frances")
        self.assertEqual(entries, [])

    def test_controls_only_present_facets(self) -> None:
        entries = build_catalog_entries(CONTENT, "en", "learn-french")
        html = catalog_controls_html("en", entries)
        self.assertIn("data-catalog-q", html)
        self.assertIn('value="A1"', html)
        self.assertIn('value="verb"', html)
        self.assertIn('value="grammar"', html)
        # No empty pronunciation/conjugation facets until pages exist.
        self.assertNotIn('value="pronunciation"', html)
        self.assertNotIn('value="conjugation"', html)
        self.assertNotIn('value="vocabulary"', html)

    def test_search_blob_title_and_summary(self) -> None:
        entries = build_catalog_entries(CONTENT, "en", "learn-french")
        etre = next(e for e in entries if "etre-basics" in e.id)
        blob = etre.search_blob()
        self.assertIn("être", blob)
        self.assertNotIn("topic", etre.to_json())

    def test_unknown_type_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_types(["idiom"], source="x.md")


class CatalogBuildTests(unittest.TestCase):
    def test_build_emits_catalog_json_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            code = build(dist)
            self.assertEqual(code, 0)
            catalog = dist / "en" / "learn-french" / "catalog"
            html_path = catalog / "index.html"
            json_path = catalog / "index.json"
            self.assertTrue(html_path.is_file())
            self.assertTrue(json_path.is_file())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schemaVersion"], 1)
            self.assertEqual(payload["locale"], "en")
            self.assertEqual(payload["target"], "learn-french")
            self.assertGreaterEqual(len(payload["entries"]), 8)
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("data-catalog-controls", html)
            self.assertIn("data-catalog-list", html)
            self.assertIn("/js/catalog.js", html)
            self.assertIn('rel="canonical" href="https://plumerastudios.com/en/learn-french/catalog/"', html)
            # Sitemap should mention the catalog URL.
            sitemap = (dist / "en" / "sitemap.xml").read_text(encoding="utf-8")
            self.assertIn("/en/learn-french/catalog/", sitemap)


if __name__ == "__main__":
    unittest.main()
