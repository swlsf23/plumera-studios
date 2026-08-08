"""DOM-based HTML post-process transforms."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.content_builder.html_transform import (
    _classify_votw_tables,
    _fragment,
    _inject_heading_ids,
    _md_to_html,
    _rewrite_local_images,
    _soup,
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

    def test_orphan_table_hint_left_in_place(self) -> None:
        html = "<p>Intro</p>\n<!-- table: forms -->\n<p>No table follows</p>"
        out = _classify_votw_tables(html)
        self.assertIn("<!-- table: forms -->", out)
        self.assertIn("<p>Intro</p>", out)
        self.assertIn("<p>No table follows</p>", out)

    def test_pattern_comment(self) -> None:
        out = _tag_grammar_patterns("<!-- pattern -->\n<p><em>avoir</em> + pp</p>")
        self.assertIn('<p class="grammar-pattern">', out)
        self.assertNotIn("<!-- pattern -->", out)

    def test_orphan_pattern_comment_left_in_place(self) -> None:
        html = "<p>Intro</p>\n<!-- pattern -->\n<table><tr><td>x</td></tr></table>"
        out = _tag_grammar_patterns(html)
        self.assertIn("<!-- pattern -->", out)
        self.assertIn("<p>Intro</p>", out)
        self.assertIn("<table>", out)

    def test_heading_ids(self) -> None:
        html, toc = _inject_heading_ids("<h2>One</h2><h3>Two</h3><h2>One</h2>")
        self.assertIn('id="one"', html)
        self.assertIn('id="two"', html)
        self.assertIn('id="one-1"', html)
        self.assertEqual([item.id for item in toc], ["one", "one-1"])

    def test_rewrite_local_images_preserves_markup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            locale = "en"
            img_dir = root / locale / "img"
            img_dir.mkdir(parents=True)
            (img_dir / "maison-etre.png").write_bytes(b"x")
            md_path = root / locale / "learn-french" / "articles" / "page.md"
            md_path.parent.mkdir(parents=True)
            md_path.write_text("# x\n", encoding="utf-8")

            html = (
                '<p>Before</p>\n'
                '<p><img alt="map" src="../../img/maison-etre.png" /></p>\n'
                '<p>After <em>keep</em></p>\n'
                '<p><img alt="abs" src="/en/img/other.png" /></p>\n'
                '<p><img alt="remote" src="https://example.com/x.png" /></p>'
            )
            out = _rewrite_local_images(html, md_path, locale)
            self.assertIn('src="/en/img/maison-etre.png"', out)
            self.assertIn("<p>Before</p>", out)
            self.assertIn("<p>After <em>keep</em></p>", out)
            self.assertIn('src="/en/img/other.png"', out)
            self.assertIn('src="https://example.com/x.png"', out)
            self.assertNotIn("../../img/", out)

    def test_representative_fragment_stable_under_reparse(self) -> None:
        """Markdown → DOM transforms stay structurally stable when re-serialized."""
        md = (
            "## Sense one\n\n"
            "A short lead.\n\n"
            "<!-- table: forms -->\n\n"
            "| Singular | Plural |\n"
            "| --- | --- |\n"
            "| je suis | nous sommes |\n\n"
            "<!-- pattern -->\n\n"
            "*être* + adjective\n\n"
            "### Detail\n\n"
            "More prose.\n"
        )
        html = _md_to_html(md)
        html = _classify_votw_tables(html)
        html = _tag_grammar_patterns(html)
        html, toc = _inject_heading_ids(html)

        self.assertIn("pair-table--forms", html)
        self.assertIn("grammar-pattern", html)
        self.assertNotIn("<!-- table: forms -->", html)
        self.assertNotIn("<!-- pattern -->", html)
        self.assertEqual([item.id for item in toc], ["sense-one"])

        # Re-parse the serialized fragment; key markers must survive unchanged.
        round_tripped = _fragment(_soup(html))
        soup = _soup(round_tripped)
        table = soup.find("table")
        self.assertIsNotNone(table)
        assert table is not None
        self.assertEqual(table.get("class"), ["pair-table", "pair-table--forms"])
        pattern = soup.find("p", class_="grammar-pattern")
        self.assertIsNotNone(pattern)
        h2 = soup.find("h2")
        self.assertIsNotNone(h2)
        assert h2 is not None
        self.assertEqual(h2.get("id"), "sense-one")

        # Transforms are idempotent on already-classified markup.
        again = _classify_votw_tables(round_tripped)
        again = _tag_grammar_patterns(again)
        again, toc2 = _inject_heading_ids(again)
        self.assertEqual([item.id for item in toc2], ["sense-one"])
        soup2 = _soup(again)
        table2 = soup2.find("table")
        self.assertIsNotNone(table2)
        assert table2 is not None
        self.assertEqual(table2.get("class"), ["pair-table", "pair-table--forms"])
        self.assertIsNotNone(soup2.find("p", class_="grammar-pattern"))


if __name__ == "__main__":
    unittest.main()
