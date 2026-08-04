"""Regression tests for <!-- pattern --> grammar-shape lines."""

from __future__ import annotations

import unittest

from tools.content_builder.parse import _md_to_html, _tag_grammar_patterns


class GrammarPatternTests(unittest.TestCase):
    def test_pattern_hint_tags_following_paragraph(self) -> None:
        html = _md_to_html(
            "Lead-in.\n\n<!-- pattern -->\n*avoir* + past participle\n\nNext.\n"
        )
        out = _tag_grammar_patterns(html)
        self.assertIn('<p class="grammar-pattern">', out)
        self.assertIn("<em>avoir</em> + past participle", out)

    def test_plain_paragraph_untouched(self) -> None:
        html = _md_to_html("Just a sentence.\n")
        out = _tag_grammar_patterns(html)
        self.assertNotIn("grammar-pattern", out)


if __name__ == "__main__":
    unittest.main()
