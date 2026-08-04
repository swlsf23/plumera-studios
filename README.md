# Plumera Studios

Website repo for Plumera: Markdown content, a Python content builder, and static landings/lessons. When Practice ships, a React app will live under `/app/practice` on the same domain (parallel to the static site, not wrapping it).

## Architecture

The **static site** and **React apps** exist in parallel on one origin. React does **not** wrap the content site.

| Layer | Role |
|---|---|
| **Python** (`.venv`) | Content builder, sitemaps, future APIs (e.g. Corpus) |
| **TypeScript / React** | Future app surfaces only (e.g. Practice at `/app/practice`) — not in this repo until wired |

**Content pages** (landings, VOTW, articles, core pages, …) are prebuilt static HTML. Title, description, and canonical are baked into each file. Do **not** rewrite those at runtime on content URLs.

**Practice** (and later apps) will live under `/app/…` as React. Product code lives in [`plumera-flashcard`](https://github.com/swlsf23/plumera-flashcard) and will be consumed here as a GitHub package — not reimplemented in this repo. Content CTAs and site nav will link into `/app/practice` (optional pack in the URL); everything else stays static HTML.

Today the shipped site is **100% static** (`dist/` from the content builder). There is no Vite/React toolchain in this repo until that app surface is added.

## What gets deployed

**`dist/`** is the site. Build it once, then deploy that folder as-is (S3 + CloudFront in production). Local preview serves the same `dist/` with a plain static file server.

CI runs on every PR/`main` push. Production deploys on version tags (`v*`). See [docs/deploy.md](docs/deploy.md) ([MSEO-10](https://plumerastudios.atlassian.net/browse/MSEO-10)).

Content voice and editorial rules: [docs/style-guide.md](docs/style-guide.md).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

npm run build:site    # → dist/  (wrapper around the Python builder)
npm run serve:site    # http://localhost:4173 serves dist/
```

`package.json` scripts call Python only; there are no npm dependencies.

Pages with `draft: true` are left out. To build them locally for review:

```bash
python3 -m tools.content_builder --drafts
```

Or `npm run dev` (= build + serve `dist/`) at [http://localhost:4173](http://localhost:4173).

Useful URLs (directory indexes, trailing slashes):

- [http://localhost:4173/](http://localhost:4173/) — root entry (EN / FR / ES → locale sites)
- [http://localhost:4173/en/](http://localhost:4173/en/)
- [http://localhost:4173/en/contact/](http://localhost:4173/en/contact/)
- [http://localhost:4173/en/privacy/](http://localhost:4173/en/privacy/)

View Source on content URLs: title, description, and canonical are in the HTML file.

## Structure

```text
content/                  # Markdown source of truth (except landings)
public/                   # Landings + static assets (copied into dist/)
tools/content_builder/    # Python MD → full HTML (extend/debug here)
dist/                     # Deployable site output (gitignored)
```

### Python content builder

Source: [`tools/content_builder/`](tools/content_builder/).

| Module | Role |
|---|---|
| `build.py` | Orchestrates copy of `public/`, page emit, sitemaps |
| `parse.py` | Markdown/frontmatter → page model |
| `chrome.py` | Localized nav/footer strings |
| `templates/content_page.html` | Full HTML document template |
| `sitemaps.py` | Root + per-locale sitemaps from `dist/` |

To extend (new page types, chrome strings, templates), change that package and re-run `npm run build:site`.

See [content/README.md](content/README.md) for content conventions.
