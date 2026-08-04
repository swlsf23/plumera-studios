"""Playwright smoke: key pages' computed font-family includes Plumera Sans.

Covers EN home, one classic landing (FR), and one content page.
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

# path → CSS selector for a primary text node on that surface
PAGES: tuple[tuple[str, str, Path], ...] = (
    ("/en/", ".landing-home .hero h1", DIST / "en" / "index.html"),
    ("/fr/", ".landing-classic .hero h1", DIST / "fr" / "index.html"),
    (
        "/en/privacy/",
        ".content-page .article-header h1",
        DIST / "en" / "privacy" / "index.html",
    ),
)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def main() -> int:
    missing = [str(p.relative_to(ROOT)) for _, _, p in PAGES if not p.is_file()]
    if missing:
        print(
            "missing build outputs; run: python -m tools.content_builder\n  "
            + "\n  ".join(missing),
            file=sys.stderr,
        )
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

        failures: list[str] = []
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # Umami is third-party analytics; do not wait on it for networkidle.
            page.route("**/cloud.umami.is/**", lambda route: route.abort())
            for path, selector, _ in PAGES:
                url = f"http://127.0.0.1:{port}{path}"
                page.goto(url, wait_until="load")
                page.wait_for_function("() => document.fonts.status === 'loaded'")
                family = page.evaluate(
                    """(sel) => {
                      const el = document.querySelector(sel);
                      if (!el) return '';
                      return getComputedStyle(el).fontFamily;
                    }""",
                    selector,
                )
                if "Plumera Sans" not in family:
                    failures.append(
                        f"{path} ({selector}): expected Plumera Sans; got {family!r}"
                    )
                else:
                    print(f"ok {path}: {family}")
            browser.close()

        if failures:
            print("Font render check failed:", file=sys.stderr)
            for line in failures:
                print(f"  {line}", file=sys.stderr)
            return 1

        print("Font render check ok")
        return 0
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    raise SystemExit(main())
