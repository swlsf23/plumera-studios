# Content source

Markdown sources for the Plumera site. Two axes:

```text
content/
  core/{locale}/     # UI locale — site-wide pages (landing, updates, privacy)
  learn/{target}/    # language being learned
    votd/            # vocabulary / verse of the day (and similar)
```

- **`core`** — depends only on interface language (`en`, `es`, `fr`; later `ar`, `pt`, …)
- **`learn`** — depends on the language someone is studying (independent of UI locale)

Example: French UI + Spanish learning → chrome from `core/fr/`, materials from `learn/es/`.

The Vite app still uses `src/i18n/` at runtime until a content builder wires these files into templates.
