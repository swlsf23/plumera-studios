"""Strict frontmatter validation (draft / slug / date / target)."""

from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from tools.content_builder.build import build
from tools.content_builder.catalog import build_catalog_entries, iso_date_string
from tools.content_builder.frontmatter_validate import (
    parse_draft,
    resolve_slug,
    validate_iso_date,
    validate_slug,
    validate_target,
)
from tools.content_builder.parse import (
    _frontmatter_sort_date,
    is_draft,
    parse_article_page,
    parse_votw_page,
)


def _write_md(path: Path, frontmatter: str, body: str = "# Title\n\nBody.\n") -> Path:
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    return path


class ParseDraftTests(unittest.TestCase):
    def test_absent_and_bool(self) -> None:
        self.assertFalse(parse_draft(None))
        self.assertFalse(parse_draft(False))
        self.assertTrue(parse_draft(True))

    def test_string_false_hard_fails(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_draft("false", source="x.md")
        self.assertIn("draft must be a YAML boolean", str(ctx.exception))
        self.assertIn("x.md", str(ctx.exception))

    def test_string_true_and_other_types_hard_fail(self) -> None:
        for value in ("true", "yes", 0, 1, "0"):
            with self.assertRaises(ValueError):
                parse_draft(value)


class ValidateSlugTests(unittest.TestCase):
    def test_valid_matches_stem(self) -> None:
        self.assertEqual(
            validate_slug("votw-prendre-a1", stem="votw-prendre-a1", source="s"),
            "votw-prendre-a1",
        )

    def test_path_traversal_and_slash(self) -> None:
        with self.assertRaises(ValueError):
            validate_slug("../x", stem="../x", source="s")
        with self.assertRaises(ValueError):
            validate_slug("a/b", stem="a/b", source="s")

    def test_slug_must_equal_stem(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            validate_slug("other", stem="votw-prendre-a1", source="s")
        self.assertIn("!= filename stem", str(ctx.exception))

    def test_resolve_defaults_to_stem(self) -> None:
        self.assertEqual(
            resolve_slug({}, stem="cefr", source="s"),
            "cefr",
        )


class ValidateDateTests(unittest.TestCase):
    def test_real_iso_date(self) -> None:
        self.assertEqual(validate_iso_date("2026-07-28"), date(2026, 7, 28))
        self.assertEqual(iso_date_string("2026-07-28"), "2026-07-28")

    def test_invalid_calendar_hard_fails(self) -> None:
        with self.assertRaises(ValueError):
            validate_iso_date("2026-13-40")
        with self.assertRaises(ValueError):
            iso_date_string("2026-13-40", source="page.md")

    def test_missing_empty(self) -> None:
        self.assertEqual(iso_date_string(None), "")
        self.assertEqual(iso_date_string(""), "")

    def test_wrong_type_is_not_missing(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            validate_iso_date(0, source="page.md")
        msg = str(ctx.exception)
        self.assertIn("page.md", msg)
        self.assertIn("must be a YAML date or ISO string", msg)
        self.assertNotIn("missing date", msg)

    def test_sort_date_rejects_fake_iso(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            _frontmatter_sort_date("2026-13-40", source="en/learn-french/votw/x.md")
        self.assertIn("en/learn-french/votw/x.md", str(ctx.exception))


class ValidateTargetTests(unittest.TestCase):
    def test_match_and_absent_ok(self) -> None:
        validate_target(None, folder="learn-french", source="s")
        validate_target("learn-french", folder="learn-french", source="s")

    def test_mismatch_hard_fails(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            validate_target("apprendre-anglais", folder="learn-french", source="s")
        self.assertIn("!= folder", str(ctx.exception))


class EmitPathIntegrationTests(unittest.TestCase):
    def test_string_draft_false_fails_is_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_md(
                Path(tmp) / "votw-sample-a1.md",
                'title: "Sample"\n'
                "slug: votw-sample-a1\n"
                "target: learn-french\n"
                'draft: "false"\n',
            )
            with self.assertRaises(ValueError) as ctx:
                is_draft(path)
            self.assertIn("YAML boolean", str(ctx.exception))

    def test_slug_neq_stem_fails_parse(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_md(
                Path(tmp) / "votw-sample-a1.md",
                'title: "Sample"\n'
                "slug: other-slug\n"
                "target: learn-french\n"
                "draft: false\n",
            )
            with self.assertRaises(ValueError) as ctx:
                parse_votw_page(path, "en", "learn-french")
            self.assertIn("!= filename stem", str(ctx.exception))

    def test_target_mismatch_fails_parse(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_md(
                Path(tmp) / "verb-sample.md",
                'title: "Sample"\n'
                "slug: verb-sample\n"
                "target: apprendre-anglais\n"
                "draft: false\n",
            )
            with self.assertRaises(ValueError) as ctx:
                parse_article_page(path, "en", "learn-french")
            self.assertIn("!= folder", str(ctx.exception))

    def test_string_draft_false_fails_build(self) -> None:
        """Bad draft typing must fail catalog prevalidation before wiping dist."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "content"
            path = root / "en" / "learn-french" / "votw" / "votw-sample-a1.md"
            path.parent.mkdir(parents=True)
            _write_md(
                path,
                'title: "Sample"\n'
                "slug: votw-sample-a1\n"
                "target: learn-french\n"
                "level: A1\n"
                "type: verb\n"
                "date: 2026-07-28\n"
                'draft: "false"\n',
            )
            with self.assertRaises(ValueError) as ctx:
                build_catalog_entries(root, "en", "learn-french")
            self.assertIn("YAML boolean", str(ctx.exception))

            dist = Path(tmp) / "dist"
            dist.mkdir()
            sentinel = dist / "keep-me.txt"
            sentinel.write_text("previous-build", encoding="utf-8")
            with mock.patch("tools.content_builder.build.CONTENT", root):
                self.assertEqual(build(dist), 1)
            self.assertTrue(sentinel.is_file())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "previous-build")


if __name__ == "__main__":
    unittest.main()
