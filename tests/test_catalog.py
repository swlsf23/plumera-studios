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


class CatalogDateMatchDocTests(unittest.TestCase):
    """Document the client date-filter contract (mirrored in catalog.js)."""

    @staticmethod
    def normalize_date_range(date_from: str, date_to: str) -> tuple[str, str]:
        if date_from and date_to and date_from > date_to:
            return date_to, date_from
        return date_from, date_to

    @classmethod
    def matches_date(cls, entry_date: str, date_from: str, date_to: str) -> bool:
        date_from, date_to = cls.normalize_date_range(date_from, date_to)
        if not date_from and not date_to:
            return True
        if not entry_date:
            return False
        if date_from and not date_to:
            return entry_date == date_from
        if date_to and not date_from:
            return entry_date == date_to
        if entry_date < date_from:
            return False
        if entry_date > date_to:
            return False
        return True

    def test_single_field_is_exact_day(self) -> None:
        self.assertTrue(self.matches_date("2026-07-28", "2026-07-28", ""))
        self.assertFalse(self.matches_date("2026-08-01", "2026-07-28", ""))
        self.assertTrue(self.matches_date("2026-07-28", "", "2026-07-28"))

    def test_both_fields_are_inclusive_range(self) -> None:
        self.assertTrue(self.matches_date("2026-07-15", "2026-07-10", "2026-07-20"))
        self.assertFalse(self.matches_date("2026-07-08", "2026-07-10", "2026-07-20"))
        self.assertTrue(self.matches_date("2026-07-28", "2026-07-28", "2026-07-28"))

    def test_inverted_range_is_swapped(self) -> None:
        self.assertEqual(
            self.normalize_date_range("2026-07-20", "2026-07-10"),
            ("2026-07-10", "2026-07-20"),
        )
        self.assertTrue(self.matches_date("2026-07-15", "2026-07-20", "2026-07-10"))


class CatalogIndexTests(unittest.TestCase):
    def test_en_learn_french_entries(self) -> None:
        entries = build_catalog_entries(CONTENT, "en", "learn-french")
        self.assertGreaterEqual(len(entries), 10)
        hrefs = {e.href for e in entries}
        self.assertIn("/en/learn-french/votw/etre/votw-etre-basics-a1/", hrefs)
        self.assertIn("/en/learn-french/articles/passe-compose-avoir-etre/", hrefs)
        self.assertIn("/en/cefr/", hrefs)
        self.assertIn("/en/language-certification-exams/", hrefs)
        for entry in entries:
            self.assertTrue(entry.level)
            self.assertTrue(entry.type)
            self.assertTrue(entry.date)
            for code in entry.type:
                self.assertIn(code, CATALOG_TYPES)

    def test_phase1_only_en_learn_french(self) -> None:
        from tools.content_builder.catalog import discover_catalog_targets

        self.assertEqual(discover_catalog_targets(CONTENT), [("en", "learn-french")])

    def test_drafts_excluded_by_default(self) -> None:
        # Helper still lists es core guides if called; phase-1 emit never builds
        # an es/fr catalog (see discover_catalog_targets).
        entries = build_catalog_entries(CONTENT, "es", "aprender-frances")
        hrefs = {e.href for e in entries}
        self.assertEqual(hrefs, {"/es/cefr/"})
        self.assertTrue(all("/votw/" not in e.href for e in entries))

    def test_controls_only_present_facets(self) -> None:
        entries = build_catalog_entries(CONTENT, "en", "learn-french")
        html = catalog_controls_html("en", entries)
        self.assertIn("data-catalog-q", html)
        self.assertIn('data-catalog-enhance hidden', html)
        self.assertIn("<noscript>", html)
        self.assertIn("catalog-noscript", html)
        self.assertIn("data-catalog-date-clear", html)
        self.assertIn('value="A1"', html)
        self.assertIn('value="verb"', html)
        self.assertIn('value="grammar"', html)
        self.assertIn('value="guide"', html)
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
            self.assertIn('data-catalog-enhance hidden', html)
            self.assertIn("catalog-noscript", html)
            self.assertIn("Filtering and sorting need JavaScript", html)
            self.assertIn("/js/catalog.js", html)
            self.assertIn('rel="canonical" href="https://plumerastudios.com/en/learn-french/catalog/"', html)
            self.assertIn('href="/en/learn-french/votw/"', html)
            self.assertIn('href="/en/learn-french/whats-new/"', html)
            self.assertIn("You might also like", html)
            # Sitemap should mention the catalog URL.
            sitemap = (dist / "en" / "sitemap.xml").read_text(encoding="utf-8")
            self.assertIn("/en/learn-french/catalog/", sitemap)
            # Phase 1: no es/fr catalogs (would link draft VOTW hubs).
            self.assertFalse((dist / "es" / "aprender-frances" / "catalog").exists())
            self.assertFalse((dist / "fr" / "apprendre-anglais" / "catalog").exists())


if __name__ == "__main__":
    unittest.main()
