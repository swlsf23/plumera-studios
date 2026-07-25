# Content source

Markdown sources for the Plumera site. **This tree is the copy source of truth** for content pages. The Python builder (`python -m tools.content_builder` / `npm run build:site`) emits full HTML into `dist/`.

There is no React/SPA path for these pages in production or local site preview.

## Layout

```text
content/
  {locale}/              # explanatory / UI language
    core/                # site-wide pages (same filenames across locales)
      updates.md
      privacy.md
      cefr.md
      index.md           # optional reference text only — NOT built
    learn/               # learning materials
      votw/
  templates/             # authoring prompts — not published pages
```

- **`locale`** — language of the explanation / UI (`en`, `es`, `fr`, …)
- **`core`** — site pages for that locale (same filenames across locales; body copy is not assumed 1:1)
- **`learn`** — learning materials written for that locale’s audience
- **`target`** (frontmatter on learn pages) — language being taught (e.g. French verbs → `target: fr`), not a folder

Example: English explanation of French VOTW → `content/en/learn/votw/…` with `locale: en` and `target: fr`.

## Build rules

- Landings are **not** emitted from Markdown. `public/{locale}/index.html` is copied as-is.
- All other pages (for now) should have a Markdown file here and are emitted as full HTML documents (title, description, canonical baked in).
- Emitted URLs are directory indexes with trailing slashes (e.g. `/en/updates/` → `updates/index.html`), so plain static hosting matches local and production.
- No hreflang alternate tags; canonicals are self-referencing only.

## Frontmatter

VOTW (and similar learn pages) use YAML frontmatter (`title`, `description`, `date`, `slug`, `target`, `locale`, …).

Keep `slug` equal to the filename stem (e.g. `votw-prendre-a1.md` → `slug: votw-prendre-a1`). The builder prefers `slug` for the URL and warns if it does not match the filename.

Set `draft: true` to keep a page out of `dist/` and sitemaps until it is ready.

Core pages may use a plain first-line eyebrow/title, then a `#` heading, then body Markdown. Optional YAML frontmatter is also supported.

## Chrome / locales

Nav and footer labels for emitted pages live in `tools/content_builder/chrome.py`. If a locale is missing there, the builder falls back to English and prints a warning.
