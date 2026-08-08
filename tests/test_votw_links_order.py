"""VOTW series index lists hubs / flat one-offs newest publish date first."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.content_builder.parse import recent_target_links, votw_links


def _write_md(
    path: Path,
    *,
    title: str,
    slug: str,
    date: str,
    draft: bool = False,
    level: str = "A1",
) -> None:
    draft_line = "true" if draft else "false"
    level_line = f"level: {level}\n" if level else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f'title: "{title} | Plumera"\n'
        f"slug: {slug}\n"
        "target: learn-french\n"
        "locale: en\n"
        f"{level_line}"
        f"date: {date}\n"
        f"draft: {draft_line}\n"
        "---\n\n"
        f"# {title}\n\n"
        "Body.\n",
        encoding="utf-8",
    )


def _write_votw(votw: Path, *, stem: str, title: str, date: str, draft: bool = False) -> None:
    _write_md(
        votw / f"{stem}.md",
        title=title,
        slug=stem,
        date=date,
        draft=draft,
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
            _write_votw(votw, stem="votw-tenir-a2", title="Tenir", date="2026-07-28")

            links = votw_links(root, "en", "learn-french")

        self.assertEqual([link["title"] for link in links], ["Tenir", "Prendre"])
        self.assertEqual(
            [link["href"] for link in links],
            [
                "/en/learn-french/votw/votw-tenir-a2/",
                "/en/learn-french/votw/votw-prendre-a1/",
            ],
        )

    def test_votw_links_equal_dates_break_ties_by_title_then_href(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            # Same date: (date, title, href) reversed → title Z→A, then href.
            _write_votw(votw, stem="votw-prendre-a1", title="Prendre", date="2026-07-22")
            _write_votw(votw, stem="votw-tenir-a2", title="Tenir", date="2026-07-22")

            links = votw_links(root, "en", "learn-french")

        self.assertEqual([link["title"] for link in links], ["Tenir", "Prendre"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            # Same date + title: href breaks the tie deterministically.
            _write_votw(votw, stem="votw-alpha-a1", title="Same", date="2026-07-22")
            _write_votw(votw, stem="votw-beta-a1", title="Same", date="2026-07-22")

            links = votw_links(root, "en", "learn-french")

        self.assertEqual(
            [link["href"] for link in links],
            [
                "/en/learn-french/votw/votw-beta-a1/",
                "/en/learn-french/votw/votw-alpha-a1/",
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
                stem="votw-tenir-a2",
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

    def test_votw_links_lists_lemma_hub_not_nested_lessons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            _write_votw(votw, stem="votw-prendre-a1", title="Prendre", date="2026-07-20")
            faire = votw / "faire"
            _write_md(
                faire / "votw-faire-index.md",
                title="Learn faire",
                slug="votw-faire-index",
                date="2026-07-31",
                level="",
            )
            _write_md(
                faire / "votw-faire-basics-a2.md",
                title="How to use faire",
                slug="votw-faire-basics-a2",
                date="2026-07-31",
                level="A2",
            )
            _write_md(
                faire / "votw-faire-expressions-a2.md",
                title="Expressions with faire",
                slug="votw-faire-expressions-a2",
                date="2026-07-31",
                level="A2",
            )

            links = votw_links(root, "en", "learn-french")

        self.assertEqual(
            [link["href"] for link in links],
            [
                "/en/learn-french/votw/faire/votw-faire-index/",
                "/en/learn-french/votw/votw-prendre-a1/",
            ],
        )
        self.assertEqual([link["title"] for link in links], ["Learn faire", "Prendre"])

    def test_votw_links_falls_back_to_nested_lessons_without_hub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            etre = votw / "etre"
            _write_md(
                etre / "votw-etre-basics-a1.md",
                title="How to use être",
                slug="votw-etre-basics-a1",
                date="2026-07-08",
                level="A1",
            )
            _write_md(
                etre / "votw-etre-expressions-a2.md",
                title="Expressions and common errors with être",
                slug="votw-etre-expressions-a2",
                date="2026-07-11",
                level="A2",
            )

            links = votw_links(root, "en", "learn-french")

        self.assertEqual(
            [link["href"] for link in links],
            [
                "/en/learn-french/votw/etre/votw-etre-expressions-a2/",
                "/en/learn-french/votw/etre/votw-etre-basics-a1/",
            ],
        )

    def test_votw_links_ignores_non_lesson_and_non_canonical_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            faire = votw / "faire"
            _write_md(
                faire / "votw-faire-basics-a2.md",
                title="How to use faire",
                slug="votw-faire-basics-a2",
                date="2026-07-31",
                level="A2",
            )
            # Auxiliary notes and a non-canonical *-index must not surface.
            (faire / "notes.md").write_text("# Notes\n", encoding="utf-8")
            _write_md(
                faire / "draft-index.md",
                title="Wrong index",
                slug="draft-index",
                date="2026-08-01",
                level="",
            )

            links = votw_links(root, "en", "learn-french")

        self.assertEqual(
            [link["href"] for link in links],
            ["/en/learn-french/votw/faire/votw-faire-basics-a2/"],
        )

    def test_votw_links_draft_hub_falls_back_to_nested_lessons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            faire = votw / "faire"
            _write_md(
                faire / "votw-faire-index.md",
                title="Learn faire",
                slug="votw-faire-index",
                date="2026-07-31",
                level="",
                draft=True,
            )
            _write_md(
                faire / "votw-faire-basics-a2.md",
                title="How to use faire",
                slug="votw-faire-basics-a2",
                date="2026-07-31",
                level="A2",
            )

            published = votw_links(root, "en", "learn-french")
            with_drafts = votw_links(
                root, "en", "learn-french", include_drafts=True
            )

        self.assertEqual(
            [link["href"] for link in published],
            ["/en/learn-french/votw/faire/votw-faire-basics-a2/"],
        )
        self.assertEqual(
            [link["href"] for link in with_drafts],
            ["/en/learn-french/votw/faire/votw-faire-index/"],
        )

    def test_votw_links_hub_date_controls_series_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            _write_votw(votw, stem="votw-prendre-a1", title="Prendre", date="2026-07-20")
            faire = votw / "faire"
            _write_md(
                faire / "votw-faire-index.md",
                title="Learn faire",
                slug="votw-faire-index",
                date="2026-07-01",
                level="",
            )
            _write_md(
                faire / "votw-faire-basics-a2.md",
                title="How to use faire",
                slug="votw-faire-basics-a2",
                date="2026-07-31",
                level="A2",
            )

            links = votw_links(root, "en", "learn-french")

        # Hub is older than its nested lesson; series still uses hub date only.
        self.assertEqual(
            [link["href"] for link in links],
            [
                "/en/learn-french/votw/votw-prendre-a1/",
                "/en/learn-french/votw/faire/votw-faire-index/",
            ],
        )

    def test_recent_target_links_still_lists_nested_lessons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            votw = root / "en" / "learn-french" / "votw"
            votw.mkdir(parents=True)
            faire = votw / "faire"
            _write_md(
                faire / "votw-faire-index.md",
                title="Learn faire",
                slug="votw-faire-index",
                date="2026-07-31",
                level="",
            )
            _write_md(
                faire / "votw-faire-basics-a2.md",
                title="How to use faire",
                slug="votw-faire-basics-a2",
                date="2026-07-31",
                level="A2",
            )
            _write_md(
                faire / "votw-faire-expressions-a2.md",
                title="Expressions with faire",
                slug="votw-faire-expressions-a2",
                date="2026-07-30",
                level="A2",
            )

            links = recent_target_links(root, "en", "learn-french")

        hrefs = [link["href"] for link in links]
        self.assertEqual(
            hrefs,
            [
                "/en/learn-french/votw/faire/votw-faire-basics-a2/",
                "/en/learn-french/votw/faire/votw-faire-expressions-a2/",
            ],
        )
        self.assertNotIn("/en/learn-french/votw/faire/votw-faire-index/", hrefs)


if __name__ == "__main__":
    unittest.main()

