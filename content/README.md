# Content source

Markdown sources for the Plumera site. **This tree is the copy source of truth** for content pages. The Python builder (`python -m tools.content_builder` / `npm run build:site`) emits full HTML into `dist/`.

There is no React/SPA path for these pages in production or local site preview.

## Layout

```text
content/
  {locale}/              # explanatory / UI language
    core/                # no target language, site-wide pages
      updates.md
      privacy.md
      cefr.md
      index.md           # optional reference text only, NOT built
    {target}/            # language being taught
      votw/
      conjugation/
  templates/             # authoring prompts, not published pages
```

- **`locale`**: language of the explanation / UI (`en`, `es`, `fr`, …)
- **`core`**: site pages for that locale, with no target language (same filenames across locales, and body copy is not assumed 1:1)
- **`{target}`**: language being taught, one folder per language, holding every series for it (`votw/`, and whatever comes later)

The second level is therefore either `core` or a language code, and nothing else.

Grouping by target rather than by series keeps one language in one place: adding a language is a new folder, not a new subfolder inside every series.

Example: English explanation of French VOTW → `content/en/fr/votw/…` with `locale: en` and `target: fr`.

## Build rules

- Landings are **not** emitted from Markdown. `public/{locale}/index.html` is copied as-is.
- All other pages (for now) should have a Markdown file here and are emitted as full HTML documents (title, description, canonical baked in).
- Emitted URLs are directory indexes with trailing slashes (e.g. `/en/updates/` → `updates/index.html`), so plain static hosting matches local and production.
- No hreflang alternate tags. Canonicals are self-referencing only.

## Frontmatter

VOTW (and similar learn pages) use YAML frontmatter (`title`, `description`, `date`, `slug`, `target`, `locale`, …).

Keep `slug` equal to the filename stem (e.g. `votw-prendre-a1.md` → `slug: votw-prendre-a1`). The builder prefers `slug` for the URL and warns if it does not match the filename.

Optional `related` is a list of sidebar cards (`title`, `href`, optional `meta`) for the “You might also like” block.

Set `draft: true` to keep a page out of `dist/` and sitemaps until it is ready.

Core pages may use a plain first-line eyebrow/title, then a `#` heading, then body Markdown. Optional YAML frontmatter is also supported.

## Chrome / locales

Nav and footer labels for emitted pages live in `tools/content_builder/chrome.py`. If a locale is missing there, the builder falls back to English and prints a warning.
