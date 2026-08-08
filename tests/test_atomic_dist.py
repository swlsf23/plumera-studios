"""Atomic dist publish: failed builds must not clobber a previous good dist/."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.content_builder.build import _publish_dist, build


class PublishDistTests(unittest.TestCase):
    def test_backup_name_includes_staging_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dist = root / "dist"
            dist.mkdir()
            (dist / "old.txt").write_text("old", encoding="utf-8")
            staging = root / ".dist-staging-unique123"
            staging.mkdir()
            (staging / "new.txt").write_text("new", encoding="utf-8")
            _publish_dist(staging, dist)
            self.assertTrue((dist / "new.txt").is_file())
            self.assertFalse((dist / "old.txt").exists())
            leftovers = [
                p
                for p in root.iterdir()
                if p.name.startswith(".dist.bak-") or p.name.startswith(".dist-staging-")
            ]
            self.assertEqual(leftovers, [])

    def test_existing_backup_is_not_deleted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dist = root / "dist"
            dist.mkdir()
            (dist / "keep.txt").write_text("live", encoding="utf-8")
            staging = root / ".dist-staging-unique456"
            staging.mkdir()
            (staging / "new.txt").write_text("new", encoding="utf-8")
            backup = root / f".dist.bak-{staging.name}"
            backup.mkdir()
            marker = backup / "do-not-delete.txt"
            marker.write_text("safe", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                _publish_dist(staging, dist)
            self.assertTrue(marker.is_file())
            self.assertEqual(marker.read_text(encoding="utf-8"), "safe")
            self.assertTrue((dist / "keep.txt").is_file())
            self.assertTrue(staging.is_dir())


class AtomicDistTests(unittest.TestCase):
    def test_catalog_failure_leaves_previous_dist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            dist.mkdir()
            sentinel = dist / "keep-me.txt"
            sentinel.write_text("previous-build", encoding="utf-8")
            with mock.patch(
                "tools.content_builder.build.build_catalog_entries",
                side_effect=ValueError("catalog metadata errors:\n- x: missing level"),
            ):
                self.assertEqual(build(dist), 1)
            self.assertTrue(sentinel.is_file())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "previous-build")
            self.assertFalse((dist / "en").exists())
            # No abandoned staging dirs next to dist.
            leftovers = [
                p for p in Path(tmp).iterdir() if p.name.startswith(".dist-staging-")
            ]
            self.assertEqual(leftovers, [])

    def test_emit_failure_leaves_previous_dist(self) -> None:
        """Parse/emit errors after staging starts must not replace dist/."""
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            dist.mkdir()
            sentinel = dist / "keep-me.txt"
            sentinel.write_text("previous-build", encoding="utf-8")
            with mock.patch(
                "tools.content_builder.build.parse_core_page",
                side_effect=ValueError("boom: bad page"),
            ):
                self.assertEqual(build(dist), 1)
            self.assertTrue(sentinel.is_file())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "previous-build")
            self.assertFalse((dist / "en").exists())
            leftovers = [
                p for p in Path(tmp).iterdir() if p.name.startswith(".dist-staging-")
            ]
            self.assertEqual(leftovers, [])

    def test_success_replaces_previous_dist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            dist.mkdir()
            sentinel = dist / "keep-me.txt"
            sentinel.write_text("previous-build", encoding="utf-8")
            self.assertEqual(build(dist), 0)
            self.assertFalse(sentinel.exists())
            self.assertTrue((dist / "en" / "index.html").is_file())
            leftovers = [
                p
                for p in Path(tmp).iterdir()
                if p.name.startswith(".dist-staging-") or p.name.startswith(".dist.bak-")
            ]
            self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
