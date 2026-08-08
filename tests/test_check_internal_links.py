"""Relative and absolute internal link resolution for CI."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.ci.check_internal_links import (
    _exists_in_dist,
    _local_path_from_ref,
    _page_url_for_html,
)


class PageUrlTests(unittest.TestCase):
    def test_index_and_stub_bases(self) -> None:
        dist = Path("/tmp/dist")
        self.assertEqual(
            _page_url_for_html(dist / "index.html", dist),
            "/",
        )
        self.assertEqual(
            _page_url_for_html(dist / "en" / "learn-french" / "votw" / "index.html", dist),
            "/en/learn-french/votw/",
        )
        self.assertEqual(
            _page_url_for_html(dist / "en" / "contact.html", dist),
            "/en/contact.html",
        )


class LocalPathFromRefTests(unittest.TestCase):
    def test_root_relative_unchanged(self) -> None:
        self.assertEqual(
            _local_path_from_ref("/en/cefr/", page_url="/en/learn-french/votw/"),
            "/en/cefr/",
        )

    def test_relative_parent(self) -> None:
        self.assertEqual(
            _local_path_from_ref(
                "../whats-new/",
                page_url="/en/learn-french/votw/",
            ),
            "/en/learn-french/whats-new/",
        )

    def test_multi_segment_parent(self) -> None:
        # From …/votw/etre/lesson/: ../../ → …/votw/; ../../../../ → /en/.
        self.assertEqual(
            _local_path_from_ref(
                "../../",
                page_url="/en/learn-french/votw/etre/votw-etre-basics-a1/",
            ),
            "/en/learn-french/votw/",
        )
        self.assertEqual(
            _local_path_from_ref(
                "../../../../cefr/",
                page_url="/en/learn-french/votw/etre/votw-etre-basics-a1/",
            ),
            "/en/cefr/",
        )

    def test_fragment_only_is_ignored(self) -> None:
        self.assertIsNone(
            _local_path_from_ref("#section", page_url="/en/cefr/")
        )

    def test_relative_with_fragment_resolves_path(self) -> None:
        self.assertEqual(
            _local_path_from_ref(
                "../../cefr/#levels",
                page_url="/en/learn-french/votw/",
            ),
            "/en/cefr/",
        )

    def test_mailto_and_external_ignored(self) -> None:
        self.assertIsNone(
            _local_path_from_ref("mailto:hi@example.com", page_url="/en/")
        )
        self.assertIsNone(
            _local_path_from_ref("https://example.com/x", page_url="/en/")
        )
        self.assertIsNone(
            _local_path_from_ref("http://example.com/x", page_url="/en/")
        )

    def test_same_origin_absolute_checked(self) -> None:
        self.assertEqual(
            _local_path_from_ref(
                "https://plumerastudios.com/en/cefr/",
                page_url="/en/",
            ),
            "/en/cefr/",
        )


class ExistsInDistTests(unittest.TestCase):
    def test_trailing_slash_directory_requires_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp)
            page = dist / "en" / "cefr" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("<html></html>", encoding="utf-8")
            self.assertTrue(_exists_in_dist("/en/cefr/", dist=dist))
            self.assertTrue(_exists_in_dist("/en/cefr", dist=dist))
            self.assertFalse(_exists_in_dist("/en/missing/", dist=dist))

    def test_relative_resolution_finds_sibling_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp)
            (dist / "en" / "learn-french" / "votw").mkdir(parents=True)
            (dist / "en" / "learn-french" / "votw" / "index.html").write_text(
                "x", encoding="utf-8"
            )
            whats = dist / "en" / "learn-french" / "whats-new" / "index.html"
            whats.parent.mkdir(parents=True)
            whats.write_text("x", encoding="utf-8")

            page_url = _page_url_for_html(
                dist / "en" / "learn-french" / "votw" / "index.html", dist
            )
            path = _local_path_from_ref("../whats-new/", page_url=page_url)
            self.assertEqual(path, "/en/learn-french/whats-new/")
            self.assertTrue(_exists_in_dist(path, dist=dist))


if __name__ == "__main__":
    unittest.main()
