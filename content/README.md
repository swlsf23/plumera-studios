# Content source

Markdown sources for the Plumera site. **This tree is the copy source of truth** for content pages. The Python builder (`python -m tools.content_builder`) emits full HTML into `dist/`.

## Layout

```text
content/
  core/{locale}/     # UI locale — site-wide pages
    updates.md
    privacy.md
    index.md         # optional reference text only — NOT built
  learn/{target}/    # language being learned
    votd/            # vocabulary / verse of the day (and similar)
```

- **`core`** — depends only on interface language (`en`, `es`, `fr`; later `ar`, `pt`, …)
- **`learn`** — depends on the language someone is studying (independent of UI locale)

Example: French UI + Spanish learning → chrome for `fr`, materials from `learn/es/`.

## Build rules

- Landings are **not** emitted from Markdown. `public/{locale}/index.html` is copied as-is.
- All other pages (for now) should have a Markdown file here and are emitted as full HTML documents (title, description, canonical baked in).
- No hreflang alternate tags; canonicals are self-referencing only.

## Frontmatter

VOTD (and similar learn pages) use YAML frontmatter (`title`, `description`, `date`, `slug`, …).

Core pages may use a plain first-line eyebrow/title, then a `#` heading, then body Markdown. Optional YAML frontmatter is also supported.
