"""Playwright smoke: /en/ hero computed font-family includes Plumera Sans.

Requires: pip install -e '.[dev]' && playwright install chromium
Serves dist/ via tools.serve_site on an ephemeral port.
"""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
EN = DIST / "en" / "index.html"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def main() -> int:
    if not EN.is_file():
        print(f"missing {EN}; run: python -m tools.content_builder", file=sys.stderr)
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "playwright not installed; run: pip install -e '.[dev]'",
            file=sys.stderr,
        )
        return 1

    port = _free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "tools.serve_site", "--port", str(port), "--bind", "127.0.0.1"],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.time() + 10
        while time.time() < deadline:
            if server.poll() is not None:
                err = (server.stderr.read() or b"").decode("utf-8", errors="replace")
                print(f"serve_site exited early:\n{err}", file=sys.stderr)
                return 1
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.05)
        else:
            print("serve_site did not become ready", file=sys.stderr)
            return 1

        url = f"http://127.0.0.1:{port}/en/"
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.wait_for_function("() => document.fonts.status === 'loaded'")
            family = page.evaluate(
                """() => {
                  const el = document.querySelector('.landing-home .hero h1');
                  if (!el) return '';
                  return getComputedStyle(el).fontFamily;
                }"""
            )
            browser.close()

        if "Plumera Sans" not in family:
            print(
                f"expected computed font-family to include Plumera Sans; got: {family!r}",
                file=sys.stderr,
            )
            return 1

        print(f"Font render check ok: {family}")
        return 0
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    raise SystemExit(main())
