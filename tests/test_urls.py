"""Table-driven tests for pure URL / dist-path assembly."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.content_builder.urls import (
    article_url,
    catalog_url,
    core_url,
    dist_path_for_url,
    votw_flat_url,
    votw_lesson_url,
    votw_nested_url,
    votw_series_url,
    whats_new_url,
)


class UrlAssemblyTests(unittest.TestCase):
    def test_page_kinds(self) -> None:
        cases = [
            (core_url("en", "cefr"), "/en/cefr/"),
            (votw_series_url("en", "learn-french"), "/en/learn-french/votw/"),
            (
                votw_flat_url("en", "learn-french", "votw-prendre-a1"),
                "/en/learn-french/votw/votw-prendre-a1/",
            ),
            (
                votw_nested_url("en", "learn-french", "etre", "votw-etre-basics-a1"),
                "/en/learn-french/votw/etre/votw-etre-basics-a1/",
            ),
            (
                article_url("en", "learn-french", "verb-prendre-b1"),
                "/en/learn-french/articles/verb-prendre-b1/",
            ),
            (whats_new_url("en", "learn-french"), "/en/learn-french/whats-new/"),
            (catalog_url("en", "learn-french"), "/en/learn-french/catalog/"),
        ]
        for got, want in cases:
            with self.subTest(want=want):
                self.assertEqual(got, want)

    def test_votw_lesson_url_flat_and_nested(self) -> None:
        self.assertEqual(
            votw_lesson_url("fr", "apprendre-anglais", "votw-take-a2"),
            "/fr/apprendre-anglais/votw/votw-take-a2/",
        )
        self.assertEqual(
            votw_lesson_url(
                "en", "learn-french", "votw-faire-index", lemma="faire"
            ),
            "/en/learn-french/votw/faire/votw-faire-index/",
        )

    def test_dist_path_for_url(self) -> None:
        dist = Path("/tmp/dist")
        cases = [
            ("/", dist / "index.html"),
            ("/en/cefr/", dist / "en" / "cefr" / "index.html"),
            (
                "/en/learn-french/votw/",
                dist / "en" / "learn-french" / "votw" / "index.html",
            ),
            (
                "/en/learn-french/votw/etre/votw-etre-basics-a1/",
                dist
                / "en"
                / "learn-french"
                / "votw"
                / "etre"
                / "votw-etre-basics-a1"
                / "index.html",
            ),
            (
                "/en/learn-french/articles/verb-prendre-b1/",
                dist
                / "en"
                / "learn-french"
                / "articles"
                / "verb-prendre-b1"
                / "index.html",
            ),
            (
                "/en/learn-french/catalog/",
                dist / "en" / "learn-french" / "catalog" / "index.html",
            ),
        ]
        for url, want in cases:
            with self.subTest(url=url):
                self.assertEqual(dist_path_for_url(dist, url), want)

    def test_dist_path_for_url_rejects_unsafe(self) -> None:
        dist = Path("/tmp/dist")
        bad = [
            "en/cefr/",
            "/en/cefr",
            "/en/../etc/",
            "/en/./cefr/",
            "/en//cefr/",
            "/en/cefr/?x=1/",
            "/en/cefr/#frag/",
            "/en\\cefr/",
            "",
        ]
        for url in bad:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    dist_path_for_url(dist, url)


if __name__ == "__main__":
    unittest.main()
