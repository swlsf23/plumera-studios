"""Keep public/js/unicode-casefold.js aligned with Python str.casefold()."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.content_builder.casefold_js import (
    DEFAULT_OUT,
    casefold_mapping,
    render_casefold_js,
    write_casefold_js,
)


class CasefoldJsTests(unittest.TestCase):
    def test_committed_file_matches_generator(self) -> None:
        committed = DEFAULT_OUT.read_text(encoding="utf-8")
        self.assertEqual(committed, render_casefold_js())

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

    def test_write_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unicode-casefold.js"
            write_casefold_js(path)
            self.assertEqual(path.read_text(encoding="utf-8"), render_casefold_js())


if __name__ == "__main__":
    unittest.main()
