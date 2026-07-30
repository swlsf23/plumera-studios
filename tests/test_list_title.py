"""List labels prefer body H1 over document title."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import frontmatter

from tools.content_builder.parse import (
    _list_title_from_post,
    _plain_list_title,
    recent_target_links,
)


class ListTitleTests(unittest.TestCase):
    def test_plain_list_title_strips_emphasis(self) -> None:
        self.assertEqual(
            _plain_list_title("Idioms with *prendre*"),
            "Idioms with prendre",
        )

    def test_list_title_prefers_h1(self) -> None:
        post = frontmatter.loads(
            '---\ntitle: "Long document title | Plumera"\n---\n\n'
            "# Idioms and fixed expressions with *prendre*\n\nBody.\n"
        )
        self.assertEqual(
            _list_title_from_post(post, "fallback"),
            "Idioms and fixed expressions with prendre",
        )

    def test_recent_target_links_articles_use_h1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            articles = root / "en" / "learn-french" / "articles"
            articles.mkdir(parents=True)
            (articles / "verb-prendre-b1.md").write_text(
                '---\n'
                'title: "Prendre (French): idioms and fixed expressions | Plumera"\n'
                "slug: verb-prendre-b1\n"
                "target: learn-french\n"
                "locale: en\n"
                "level: B1\n"
                "date: 2026-07-28\n"
                "draft: false\n"
                "---\n\n"
                "# Idioms and fixed expressions with *prendre*\n\n"
                "Body.\n",
                encoding="utf-8",
            )
            links = recent_target_links(root, "en", "learn-french")
        self.assertEqual(len(links), 1)
        self.assertEqual(
            links[0]["title"],
            "Idioms and fixed expressions with prendre",
        )


if __name__ == "__main__":
    unittest.main()
