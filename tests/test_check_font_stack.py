"""Unit tests for tools.ci.check_font_stack."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.ci.check_font_stack import _scan_text


class CheckFontStackTests(unittest.TestCase):
    def test_rejects_css_family_inter(self) -> None:
        path = Path("public/x.html")
        hits = _scan_text(
            path,
            'body { font-family: "Inter", sans-serif; }',
        )
        self.assertTrue(any("CSS family Inter" in h for h in hits))

    def test_allows_plumera_sans(self) -> None:
        path = Path("public/x.html")
        hits = _scan_text(
            path,
            'body { font-family: "Plumera Sans", "Plumera Sans Fallback", sans-serif; }',
        )
        self.assertEqual(hits, [])

    def test_rejects_unfingerprinted_font_url(self) -> None:
        path = Path("public/x.html")
        hits = _scan_text(
            path,
            'src: url("/fonts/InterVariable.woff2") format("woff2");',
        )
        self.assertTrue(any("missing ?v=" in h for h in hits))

    def test_allows_fingerprinted_font_url(self) -> None:
        path = Path("public/x.html")
        hits = _scan_text(
            path,
            'src: url("/fonts/InterVariable.woff2?v=inter-2") format("woff2");',
        )
        self.assertEqual(hits, [])

    def test_ignores_inter_in_comments(self) -> None:
        path = Path("public/x.css")
        hits = _scan_text(
            path,
            '/* font-family: "Inter" */\nbody { font-family: "Plumera Sans", sans-serif; }',
        )
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
