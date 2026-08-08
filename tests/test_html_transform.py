"""DOM-based HTML post-process transforms."""

from __future__ import annotations

import unittest

from tools.content_builder.html_transform import (
    _classify_votw_tables,
    _inject_heading_ids,
    _strip_tag,
    _tag_grammar_patterns,
)


class HtmlTransformTests(unittest.TestCase):
    def test_strip_h1(self) -> None:
        heading, rest = _strip_tag("<h1>Title</h1>\n<p>Body</p>", "h1")
        self.assertEqual(heading, "Title")
        self.assertIn("<p>Body</p>", rest)
        self.assertNotIn("<h1>", rest)

    def test_table_hint_and_header_heuristic(self) -> None:
        hinted = _classify_votw_tables(
            '<!-- table: forms -->\n<table><tr><th>A</th><th>B</th></tr></table>'
        )
        self.assertIn('class="pair-table pair-table--forms"', hinted)
        self.assertNotIn("<!-- table: forms -->", hinted)

        correction = _classify_votw_tables(
            "<table><tr><th>Incorrect</th><th>Correct</th></tr></table>"
        )
        self.assertIn("pair-table--correction", correction)

    def test_pattern_comment(self) -> None:
        out = _tag_grammar_patterns("<!-- pattern -->\n<p><em>avoir</em> + pp</p>")
        self.assertIn('<p class="grammar-pattern">', out)
        self.assertNotIn("<!-- pattern -->", out)

    def test_heading_ids(self) -> None:
        html, toc = _inject_heading_ids("<h2>One</h2><h3>Two</h3><h2>One</h2>")
        self.assertIn('id="one"', html)
        self.assertIn('id="two"', html)
        self.assertIn('id="one-1"', html)
        self.assertEqual([item.id for item in toc], ["one", "one-1"])


if __name__ == "__main__":
    unittest.main()
