# Plumera Studios

Monorepo for the Plumera website: static multilingual landings, Markdown content sources, a Python content builder, and a Vite/React app for interactive work.

## Language split

| Stack | Owns |
|---|---|
| **Python** (`.venv`) | Content builder, sitemaps, future APIs (e.g. Corpus) |
| **TypeScript / React** (npm) | Interactive apps only — not production content pages |

## Production site (Python)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m tools.content_builder
```

Output is `dist/`:

- Landings and assets **copied** from `public/`
- Content pages **emitted** from `content/` (updates, privacy, votd, …)
- `index.md` is **not** built — landings stay hand-authored HTML

Preview the static output with any static server, for example:

```bash
npx --yes serve dist
```

## React app (prototype / future apps)

```bash
npm install
npm run dev
```

The SPA still serves Updates/Privacy/VOTD from `src/` for local prototyping. Production content URLs come from the Python builder.

## Structure

```text
content/
  core/{locale}/          # UI locale — updates, privacy (+ optional index.md reference)
  learn/{target}/votd/    # language being learned — VOTD Markdown
public/
  {en,es,fr}/index.html   # static landings (copied, not emitted)
  css/                    # landing + content styles
tools/content_builder/    # Python MD → full HTML
src/                      # Vite React app (interactive / prototype)
```

See [content/README.md](content/README.md) for content conventions.
