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
      whats-new.md       # optional: recent pages for this target
      votw/              # Verb of the Week series (+ optional index.md)
      articles/          # standalone pages (not a series index)
      conjugation/       # future series
  templates/             # authoring prompts, not published pages
```

- **`locale`**: language of the explanation / UI (`en`, `es`, `fr`, …)
- **`core`**: site pages for that locale, with no target language (same filenames across locales, and body copy is not assumed 1:1)
- **`{target}`**: language being taught, one folder per language, holding every series for it (`votw/`, `articles/`, and whatever comes later)
- **`articles/`**: one-off explainers for that target; emitted at `/{locale}/{target}/articles/{slug}/`. Not listed on the VOTW index. Default eyebrow is “Article” (override with frontmatter `eyebrow`).
- **`whats-new.md`**: optional page at `/{locale}/{target}/whats-new/`. Intro copy is authored; the builder appends a newest-first list of that target’s VOTW lessons and articles (draft filtering matches the build).

**CEFR on links (site standard):** when the builder generates a link to a page that declares `level` in frontmatter (related cards, what’s-new list, VOTW index cards), it appends the level to the link label as `Title · A1`. Authors do not need to put the level in the related `title` by hand.

**Document `<title>`:** the template emits `Plumera | {title}` unless frontmatter `title` already starts with `Plumera |` or `Plumera Studios |`.

The second level is therefore either `core` or a language code, and nothing else.

Grouping by target rather than by series keeps one language in one place: adding a language is a new folder, not a new subfolder inside every series.

Example: English explanation of French VOTW → `content/en/fr/votw/…` with `locale: en` and `target: fr`.

## Build rules

- Landings are **not** emitted from Markdown. `public/{locale}/index.html` is copied as-is.
- All other pages (for now) should have a Markdown file here and are emitted as full HTML documents (title, description, canonical baked in).
- Emitted URLs are directory indexes with trailing slashes (e.g. `/en/updates/` → `updates/index.html`), so plain static hosting matches local and production.
- No hreflang alternate tags. Canonicals are self-referencing only.

## Content page template

Every emitted content page uses one layout (not landings): short **eyebrow**, **H1**, **dek** as a lede, slim decorative **hero** band, article body, then an end band with optional **You might also like** cards and **Follow us**.

Author that shape in Markdown + YAML. Do not add a right-rail “On this page” TOC for content pages.

## Frontmatter

Prefer YAML frontmatter on content pages (`title`, `description`, `eyebrow`, `related`, and for VOTW also `date`, `slug`, `target`, `locale`, `level`, …).

Keep `slug` equal to the filename stem (e.g. `votw-prendre-a1.md` → `slug: votw-prendre-a1`). The builder prefers `slug` for the URL and warns if it does not match the filename.

Optional `related` is a list of end-band cards for “You might also like”. Each item needs `href`. Omit `title` to use the target page’s H1 (recommended). Set `title` only to override that label. Optional `meta` is a short secondary line. When the target declares `level`, the builder appends it as `Title · A1`.

Draft pages are indexed for those H1 labels even when not emitted. A production build warns if a related `href` points at a draft URL (label works; the link is not in `dist/` without `--drafts`).

Optional `eyebrow` is the short label above the H1 (e.g. `Levels`, `News`, `Series`).

Set `draft: true` to keep a page out of `dist/` and sitemaps until it is ready.

## Chrome / locales

Nav and footer labels for emitted pages live in `tools/content_builder/chrome.py`. If a locale is missing there, the builder falls back to English and prints a warning.
