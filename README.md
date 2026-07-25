# Plumera Studios

Monorepo for the Plumera website: static multilingual landings, Markdown content sources, a Python content builder, and a reserved Vite/React scaffold for future interactive apps.

## Language split

| Stack | Owns |
|---|---|
| **Python** (`.venv`) | Content builder, sitemaps, future APIs (e.g. Corpus) |
| **TypeScript / React** (npm) | Interactive apps only — **not** content pages |

## Local site (static HTML)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

npm run dev
```

`npm run dev` builds `dist/` with the Python builder, then serves it at [http://localhost:4173](http://localhost:4173).

Useful URLs:

- Landing: [http://localhost:4173/en/index.html](http://localhost:4173/en/index.html)
- Updates: [http://localhost:4173/en/updates.html](http://localhost:4173/en/updates.html)
- Privacy: [http://localhost:4173/en/privacy.html](http://localhost:4173/en/privacy.html)
- VOTD: [http://localhost:4173/en/votd/thoughtful-content/](http://localhost:4173/en/votd/thoughtful-content/)

Or step by step:

```bash
npm run build:site    # python -m tools.content_builder → dist/
npm run preview:site  # serve dist/
```

View Source on content URLs: title, description, and canonical are in the HTML file.

## React scaffold (future apps)

```bash
npm run dev:app
```

This Vite app is a placeholder only. It does not deliver production content pages.

## Structure

```text
content/                  # Markdown source of truth (except landings)
public/                   # Landings + static assets (copied into dist/)
tools/content_builder/    # Python MD → full HTML
dist/                     # Deployable site output
src/                      # Reserved for future interactive React apps
```

See [content/README.md](content/README.md) for content conventions.
