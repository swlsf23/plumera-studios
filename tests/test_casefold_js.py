"""Keep catalog search folding aligned with Python str.casefold()."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.content_builder.build import build
from tools.content_builder.casefold_js import (
    casefold_mapping,
    render_casefold_js,
    write_casefold_js,
)


class CasefoldJsTests(unittest.TestCase):
    def test_python_casefold_samples(self) -> None:
        samples = {
            "ß": "ss",
            "ẞ": "ss",
            "Straße": "strasse",
            "STRASSE": "strasse",
            "İ": "i̇",
            "Σ": "σ",
            "ς": "σ",
            "être": "être",
            "ÊTRE": "être",
            "АБВ": "абв",
            "日本語": "日本語",
        }
        for raw, expected in samples.items():
            with self.subTest(raw=raw):
                self.assertEqual(raw.casefold(), expected)

    def test_mapping_covers_sharp_s(self) -> None:
        mapping = casefold_mapping()
        self.assertEqual(mapping[ord("ß")], "ss")
        self.assertEqual(mapping[ord("ẞ")], "ss")

    def test_render_includes_runtime_helper(self) -> None:
        src = render_casefold_js()
        self.assertIn("global.PlumeraCaseFold", src)
        self.assertIn(f'{ord("ß")}:"ss"', src)

    def test_write_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unicode-casefold.js"
            write_casefold_js(path)
            self.assertEqual(path.read_text(encoding="utf-8"), render_casefold_js())

    def test_build_emits_casefold_matching_this_python(self) -> None:
        """dist helper must come from the same interpreter that folds search blobs."""
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            self.assertEqual(build(dist), 0)
            emitted = dist / "js" / "unicode-casefold.js"
            self.assertTrue(emitted.is_file())
            self.assertEqual(emitted.read_text(encoding="utf-8"), render_casefold_js())
            # Catalog page loads the helper next to catalog.js.
            html = (dist / "en" / "learn-french" / "catalog" / "index.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("/js/unicode-casefold.js", html)


class CasefoldJsEvalTests(unittest.TestCase):
    """Optional Node check when available (CI images usually have it)."""

    def test_node_helper_matches_python_samples(self) -> None:
        import shutil
        import subprocess

        if not shutil.which("node"):
            self.skipTest("node not available")
        samples = {
            "ß": "ss",
            "ẞ": "ss",
            "Straße": "strasse",
            "STRASSE": "strasse",
            "İ": "i̇",
            "Σ": "σ",
            "ς": "σ",
            "être": "être",
            "ÊTRE": "être",
            "АБВ": "абв",
            "日本語": "日本語",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unicode-casefold.js"
            write_casefold_js(path)
            script = (
                f"const fs=require('fs');eval(fs.readFileSync({json.dumps(str(path))},'utf8'));"
                f"const samples={json.dumps(samples, ensure_ascii=False)};"
                "for (const [raw, expected] of Object.entries(samples)) {"
                "  const got = PlumeraCaseFold(raw);"
                "  if (got !== expected) {"
                "    console.error(JSON.stringify({raw, got, expected}));"
                "    process.exit(1);"
                "  }"
                "}"
            )
            proc = subprocess.run(
                ["node", "-e", script],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)


if __name__ == "__main__":
    unittest.main()
