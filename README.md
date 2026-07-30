# Plumera Studios

Monorepo for the Plumera website: static multilingual landings, Markdown content sources, a Python content builder, and a reserved Vite/React scaffold for future interactive apps.

## Language split

| Stack | Owns |
|---|---|
| **Python** (`.venv`) | Content builder, sitemaps, future APIs (e.g. Corpus) |
| **TypeScript / React** (npm) | Interactive apps only, **not** content pages |

## What gets deployed

**`dist/` is the site.** Build it once, then deploy that folder as-is (S3 + CloudFront in production). Local preview serves the same `dist/` with a plain static file server, with no special rewrite layer.

CI runs on every PR/`main` push. Production deploys on version tags (`v*`). See [docs/deploy.md](docs/deploy.md) ([MSEO-10](https://plumerastudios.atlassian.net/browse/MSEO-10)).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

npm run build:site    # → dist/  (same artifact as production)
npm run serve:site    # http://localhost:4173 serves dist/
```

Pages with `draft: true` are left out. To build them locally for review:

```bash
python3 -m tools.content_builder --drafts
```

Or `npm run dev` (= build + serve) at [http://localhost:4173](http://localhost:4173).

Useful URLs (same paths in prod: directory indexes, trailing slashes):

- [http://localhost:4173/](http://localhost:4173/) — root entry (EN / FR / ES → locale sites)
- [http://localhost:4173/en/](http://localhost:4173/en/)
- [http://localhost:4173/en/contact/](http://localhost:4173/en/contact/)
- [http://localhost:4173/en/privacy/](http://localhost:4173/en/privacy/)

View Source on content URLs: title, description, and canonical are in the HTML file.

## React scaffold (future apps)

```bash
npm run dev:app
```

Placeholder only. Not used for content pages.

## Structure

```text
content/                  # Markdown source of truth (except landings)
public/                   # Landings + static assets (copied into dist/)
tools/content_builder/    # Python MD → full HTML (extend/debug here)
dist/                     # Deployable site output (gitignored)
src/                      # Reserved for future interactive React apps
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
