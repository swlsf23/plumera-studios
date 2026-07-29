"""Regression tests for related-link label enrichment."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stderr

from tools.content_builder.build import _enrich_related, _title_with_level


PAGES = {
    "/en/learn-french/votw/votw-prendre-a1/": {
        "heading": "Prendre",
        "title": "Plumera | French Verb of the Week: Prendre",
        "level": "A1",
    },
    "/en/learn-french/articles/verb-prendre-b1/": {
        "heading": "Prendre: Idioms and Fixed Expressions",
        "title": "Plumera | Prendre (French): idioms and fixed expressions",
        "level": "B1",
    },
    "/en/cefr/": {
        "heading": "How we use CEFR levels",
        "title": "Plumera | How we use CEFR levels",
        "level": "",
    },
}


class RelatedEnrichmentTests(unittest.TestCase):
    def test_href_only_uses_target_h1(self) -> None:
        related = [{"title": "", "href": "/en/cefr/", "meta": ""}]
        out = _enrich_related(related, PAGES, source="fixture.md")
        self.assertEqual(out[0]["title"], "How we use CEFR levels")

    def test_override_title_wins_over_h1(self) -> None:
        related = [
            {
                "title": "CEFR levels",
                "href": "/en/cefr/",
                "meta": "",
            }
        ]
        out = _enrich_related(related, PAGES, source="fixture.md")
        self.assertEqual(out[0]["title"], "CEFR levels")

    def test_cefr_suffix_on_default_h1(self) -> None:
        related = [
            {"title": "", "href": "/en/learn-french/votw/votw-prendre-a1/", "meta": ""}
        ]
        out = _enrich_related(related, PAGES, source="fixture.md")
        self.assertEqual(out[0]["title"], "Prendre · A1")

    def test_cefr_suffix_on_override_when_missing(self) -> None:
        related = [
            {
                "title": "Idioms and fixed expressions",
                "href": "/en/learn-french/articles/verb-prendre-b1/",
                "meta": "",
            }
        ]
        out = _enrich_related(related, PAGES, source="fixture.md")
        self.assertEqual(out[0]["title"], "Idioms and fixed expressions · B1")

    def test_no_double_suffix_when_override_already_has_level(self) -> None:
        related = [
            {
                "title": "Prendre · A1",
                "href": "/en/learn-french/votw/votw-prendre-a1/",
                "meta": "",
            }
        ]
        out = _enrich_related(related, PAGES, source="fixture.md")
        self.assertEqual(out[0]["title"], "Prendre · A1")
        self.assertEqual(_title_with_level("Prendre · A1", "A1"), "Prendre · A1")

    def test_unresolved_href_warning_includes_source_and_href(self) -> None:
        related = [{"title": "", "href": "/en/missing/", "meta": ""}]
        buf = io.StringIO()
        with redirect_stderr(buf):
            out = _enrich_related(related, PAGES, source="en/fr/votw/index.md")
        self.assertEqual(out, [])
        msg = buf.getvalue()
        self.assertIn("en/fr/votw/index.md", msg)
        self.assertIn("/en/missing/", msg)
        self.assertIn("unresolved href", msg)


if __name__ == "__main__":
    unittest.main()
