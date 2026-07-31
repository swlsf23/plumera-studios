"""Serve dist/ and append local study events to tmp/study-events.jsonl."""

from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
EVENTS_PATH = ROOT / "tmp" / "study-events.jsonl"


class SiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def do_POST(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] != "/__local/study-events":
            self.send_error(404, "Not found")
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
            if not isinstance(payload, dict):
                raise ValueError("expected object")
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self.send_error(400, "Invalid JSON")
            return

        EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with EVENTS_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] != "/__local/study-events":
            self.send_error(404, "Not found")
            return
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        if args and str(args[0]).startswith("POST"):
            super().log_message(format, *args)
            return
        # Keep static GETs quiet-ish; still show errors.
        if args and str(args[0]).startswith(("4", "5")):
            super().log_message(format, *args)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    if not DIST.is_dir():
        raise SystemExit(f"Missing {DIST}; build the site first.")
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((args.host, args.port), SiteHandler)
    print(f"http://{args.host}:{args.port}")
    print(f"study events → {EVENTS_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
