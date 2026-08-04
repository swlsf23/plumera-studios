"""Serve dist/ with production-like Cache-Control (local Brave warm-cache testing).

  python -m tools.serve_site
  → http://127.0.0.1:4173
"""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


class DistHandler(SimpleHTTPRequestHandler):
    """Mirror deploy.yml cache classes: short HTML, long CSS/JS/fonts."""

    # Do not rely on host mimetypes for .woff2 (can be application/octet-stream).
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".woff2": "font/woff2",
    }

    def end_headers(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path.endswith(".html") or path.endswith("/"):
            self.send_header("Cache-Control", "public, max-age=300, must-revalidate")
        elif path.endswith(".woff2"):
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        elif path.endswith(".css") or path.endswith(".js"):
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "public, max-age=86400")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4173)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()
    if not DIST.is_dir():
        raise SystemExit(f"missing {DIST}; run: python -m tools.content_builder")

    handler = partial(DistHandler, directory=str(DIST))
    server = ThreadingHTTPServer((args.bind, args.port), handler)
    print(f"http://{args.bind}:{args.port}  (dist/ with deploy-like Cache-Control)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        server.server_close()


if __name__ == "__main__":
    main()
