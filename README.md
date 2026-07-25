# Plumera Studios

Monorepo for the Plumera website: static multilingual landings, React content pages, and Markdown sources.

## Local development

```bash
npm install
npm run dev
```

Open:

- Landing: [http://localhost:5173/en/index.html](http://localhost:5173/en/index.html)
- Updates: [http://localhost:5173/en/updates.html](http://localhost:5173/en/updates.html)
- Privacy: [http://localhost:5173/en/privacy.html](http://localhost:5173/en/privacy.html)
- VOTD: [http://localhost:5173/en/votd/thoughtful-content](http://localhost:5173/en/votd/thoughtful-content)

Spanish and French use the same paths under `/es/` and `/fr/`.

## Production build

```bash
npm run build
npm run preview
```

## Structure

```text
content/
  core/{locale}/          # UI locale — landing, updates, privacy
  learn/{target}/votd/    # language being learned — VOTD content
public/
  {en,es,fr}/index.html   # static landings
  css/                    # landing + header styles
src/                      # Vite React app (Updates, Privacy, VOTD)
  i18n/                   # runtime copy (until content builder lands)
  data/                   # small app constants (related links, social URLs)
  pages/
  components/
```

See [content/README.md](content/README.md) for content conventions.
