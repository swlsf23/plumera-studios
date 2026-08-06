"""Conjugation verb emit (+ optional JSON index for a future selector)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.content_builder.build import build
from tools.content_builder.conjugation import (
    default_conjugation_verb,
    load_conjugation_verbs,
    parse_conjugation_fragment,
)


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


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
    def test_emit_redirect_json_and_verb_html(self) -> None:
        verbs = load_conjugation_verbs(CONTENT)
        if not verbs:
            self.skipTest("no conjugation verb fragments in content/")
        land = default_conjugation_verb(verbs)
        sample = next(v for v in verbs if v.slug == "revenir")

        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            self.assertEqual(build(dist), 0)

            index = dist / "en" / "learn-french" / "conjugation" / "index.html"
            self.assertTrue(index.is_file())
            index_html = index.read_text(encoding="utf-8")
            self.assertIn(f"url={land.href}", index_html)
            self.assertIn("location.replace", index_html)
            self.assertIn("location.search", index_html)
            # Hub is a redirect, not a verb list page.
            self.assertNotIn("data-conjugation-results", index_html)
            self.assertNotIn('class="conjugation"', index_html)

            verbs_json_path = (
                dist / "en" / "learn-french" / "conjugation" / "verbs.json"
            )
            self.assertTrue(verbs_json_path.is_file())
            payload = json.loads(verbs_json_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["verbs"]), len(verbs))

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
            # Hero lemma: initial capital, not all-lowercase / all-caps.
            self.assertIn(f"<h1 class=\"lemma-title\">{sample.lemma[:1].upper()}{sample.lemma[1:]}</h1>", vhtml)
            # Selector rail deferred.
            self.assertNotIn("conjugation-sidebar", vhtml)
            self.assertNotIn("conjugation-shell", vhtml)
            self.assertNotIn("data-conjugation-results", vhtml)
            self.assertNotIn("conjugation-index.js", vhtml)
            toolbar_idx = vhtml.index('class="conjugation-toolbar"')
            body_idx = vhtml.index("conjugation-tables")
            self.assertLess(toolbar_idx, body_idx)
            self.assertIn("conjugaison.js", vhtml)
            # Header skips the hub redirect (avoids flash).
            land = default_conjugation_verb(verbs)
            self.assertIn(f'href="{land.href}"', vhtml)
            self.assertNotIn('href="/en/learn-french/conjugation/"', vhtml)

            sitemap = (dist / "en" / "sitemap.xml").read_text(encoding="utf-8")
            self.assertIn("/en/learn-french/conjugation/", sitemap)
            self.assertIn(sample.href, sitemap)


if __name__ == "__main__":
    unittest.main()
