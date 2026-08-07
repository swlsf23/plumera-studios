"""Conjugation verb emit (hub selector, verbs.json, verb pages)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.content_builder.build import build
from tools.content_builder.conjugation import (
    load_conjugation_verbs,
    parse_conjugation_fragment,
)


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
HUB = "/en/learn-french/conjugation/"


class ConjugationFragmentTests(unittest.TestCase):
    def test_sample_fragments_parse(self) -> None:
        verbs_dir = CONTENT / "en" / "learn-french" / "conjugation" / "verbs"
        paths = sorted(verbs_dir.glob("*.html"))
        self.assertGreaterEqual(len(paths), 1)
        for path in paths:
            meta = parse_conjugation_fragment(path)
            self.assertTrue(meta["lemma"])
            self.assertRegex(meta["cefr"], r"^A1|A2|B1|B2|C1|C2$")


class ConjugationBuildTests(unittest.TestCase):
    def test_emit_hub_json_and_verb_html(self) -> None:
        verbs = load_conjugation_verbs(CONTENT)
        if not verbs:
            self.skipTest("no conjugation verb fragments in content/")
        sample = next(v for v in verbs if v.slug == "revenir")

        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            self.assertEqual(build(dist), 0)

            index = dist / "en" / "learn-french" / "conjugation" / "index.html"
            self.assertTrue(index.is_file())
            index_html = index.read_text(encoding="utf-8")
            self.assertNotIn("location.replace", index_html)
            self.assertNotIn("data-conjugation-drawer", index_html)
            self.assertIn("data-conjugation-controls", index_html)
            self.assertIn("data-conjugation-results", index_html)
            self.assertIn("data-conjugation-q", index_html)
            self.assertIn("data-conjugation-az", index_html)
            self.assertIn("data-conjugation-az-letter", index_html)
            self.assertRegex(
                index_html,
                r'data-conjugation-index-url="/en/learn-french/conjugation/verbs\.json\?v=[0-9a-f]{10}"',
            )
            # Lists are filled from verbs.json — not a baked-in verb inventory.
            self.assertNotIn(sample.href, index_html)
            self.assertNotIn('class="content-list__item"', index_html)
            self.assertIn("conjugation-index.js", index_html)
            self.assertNotIn("conjugation-drawer.js", index_html)
            self.assertIn("unicode-casefold.js", index_html)
            self.assertIn("content-page--conjugation", index_html)
            self.assertIn(
                f'rel="canonical" href="https://plumerastudios.com{HUB}"',
                index_html,
            )

            verbs_json_path = (
                dist / "en" / "learn-french" / "conjugation" / "verbs.json"
            )
            self.assertTrue(verbs_json_path.is_file())
            payload = json.loads(verbs_json_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["verbs"]), len(verbs))
            self.assertTrue(
                any(v["href"] == sample.href for v in payload["verbs"])
            )

            verb_out = (
                dist
                / "en"
                / "learn-french"
                / "conjugation"
                / "verbs"
                / f"{sample.slug}.html"
            )
            self.assertTrue(verb_out.is_file())
            vhtml = verb_out.read_text(encoding="utf-8")
            self.assertIn(
                f'rel="canonical" href="https://plumerastudios.com{sample.href}"',
                vhtml,
            )
            self.assertIn('class="conjugation"', vhtml)
            self.assertIn("page-grid--lesson", vhtml)
            self.assertIn("conjugation-header", vhtml)
            self.assertIn("conjugation-toolbar", vhtml)
            self.assertIn("conjugation-tables", vhtml)
            self.assertIn("conjugation-stage", vhtml)
            self.assertIn(
                f"<h1>{sample.lemma[:1].upper()}{sample.lemma[1:]}</h1>",
                vhtml,
            )
            self.assertNotIn("conjugation-sidebar", vhtml)
            self.assertNotIn("conjugation-shell", vhtml)
            self.assertNotIn("data-conjugation-drawer", vhtml)
            self.assertNotIn("conjugation-drawer.js", vhtml)
            self.assertNotIn("conjugation-index.js", vhtml)
            self.assertNotIn("conjugation-browse", vhtml)
            self.assertNotIn("← Verb list", vhtml)
            self.assertIn("content-column", vhtml)
            toolbar_idx = vhtml.index('class="conjugation-toolbar"')
            body_idx = vhtml.index("conjugation-tables")
            self.assertLess(toolbar_idx, body_idx)
            self.assertIn("conjugaison.js", vhtml)

            landing = (dist / "en" / "index.html").read_text(encoding="utf-8")
            self.assertIn(f'href="{HUB}"', landing)
            self.assertNotIn(
                'href="/en/learn-french/conjugation/verbs/abandonner.html"',
                landing,
            )

            sitemap = (dist / "en" / "sitemap.xml").read_text(encoding="utf-8")
            self.assertIn(HUB, sitemap)
            self.assertIn(sample.href, sitemap)


if __name__ == "__main__":
    unittest.main()
