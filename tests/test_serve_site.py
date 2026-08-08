"""Cache-Control classes on DistHandler (mirror deploy.yml)."""

from __future__ import annotations

import unittest
from http.server import SimpleHTTPRequestHandler
from unittest import mock

from tools.serve_site import DistHandler


class DistHandlerCacheTests(unittest.TestCase):
    def _cache_control(self, request_path: str) -> str:
        handler = DistHandler.__new__(DistHandler)
        handler.path = request_path
        headers: dict[str, str] = {}

        def send_header(keyword: str, value: str) -> None:
            headers[keyword] = value

        handler.send_header = send_header  # type: ignore[method-assign]
        with mock.patch.object(SimpleHTTPRequestHandler, "end_headers", lambda self: None):
            DistHandler.end_headers(handler)
        self.assertIn("Cache-Control", headers)
        return headers["Cache-Control"]

    def test_html_and_directory_are_short_revalidate(self) -> None:
        want = "public, max-age=300, must-revalidate"
        self.assertEqual(self._cache_control("/en/cefr/index.html"), want)
        self.assertEqual(self._cache_control("/en/cefr/"), want)

    def test_css_js_woff2_are_immutable_year(self) -> None:
        want = "public, max-age=31536000, immutable"
        self.assertEqual(self._cache_control("/css/base.css"), want)
        self.assertEqual(self._cache_control("/js/catalog.js"), want)
        self.assertEqual(self._cache_control("/fonts/InterVariable.woff2"), want)

    def test_other_assets_are_one_day(self) -> None:
        self.assertEqual(
            self._cache_control("/images/hero.png"),
            "public, max-age=86400",
        )

    def test_woff2_mime_override(self) -> None:
        self.assertEqual(DistHandler.extensions_map[".woff2"], "font/woff2")


if __name__ == "__main__":
    unittest.main()
