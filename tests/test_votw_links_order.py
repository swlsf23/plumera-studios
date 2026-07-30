"""VOTW series index lists lessons newest publish date first."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.content_builder.parse import votw_links


def _write_votw(votw: Path, *, stem: str, title: str, date: str, draft: bool = False) -> None:
    draft_line = "true" if draft else "false"
    (votw / f"{stem}.md").write_text(
        "---\n"
        f'title: "French Verb of the Week: {title} | Plumera"\n'
        f"slug: {stem}\n"
        "target: learn-french\n"
        "locale: en\n"
        "level: A1\n"
        f"date: {date}\n"
        f"draft: {draft_line}\n"
        "---\n\n"
        f"# {title}\n\n"
        "Body.\n",
        encoding="utf-8",
    )


class VotwLinksOrderTests(unittest.TestCase):
    def test_votw_links_newest_date_first_not_filename_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            (votw / "index.md").write_text(
                "---\ntitle: Series\ndraft: false\n---\n\n# Series\n",
                encoding="utf-8",
            )
            # Filename order would put prendre before tenir; dates reverse that.
            _write_votw(votw, stem="votw-prendre-a1", title="Prendre", date="2026-07-20")
            _write_votw(votw, stem="votw-tenir-a1", title="Tenir", date="2026-07-28")

            links = votw_links(root, "en", "learn-french")

        self.assertEqual([link["title"] for link in links], ["Tenir", "Prendre"])
        self.assertEqual(
            [link["href"] for link in links],
            [
                "/en/learn-french/votw/votw-tenir-a1/",
                "/en/learn-french/votw/votw-prendre-a1/",
            ],
        )

    def test_votw_links_skips_drafts_unless_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            _write_votw(votw, stem="votw-prendre-a1", title="Prendre", date="2026-07-20")
            _write_votw(
                votw,
                stem="votw-tenir-a1",
                title="Tenir",
                date="2026-07-28",
                draft=True,
            )

            published = votw_links(root, "en", "learn-french")
            with_drafts = votw_links(
                root, "en", "learn-french", include_drafts=True
            )

        self.assertEqual([link["title"] for link in published], ["Prendre"])
        self.assertEqual([link["title"] for link in with_drafts], ["Tenir", "Prendre"])


if __name__ == "__main__":
    unittest.main()
