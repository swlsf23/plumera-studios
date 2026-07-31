# App datasets

Non-page data for interactive apps (flashcard decks, etc.). Not consumed by the Python content builder.

## Layout

```text
data/
  {locale}/           # UI / explanation language (en, es, fr, …)
    {target}/         # language being taught (learn-french, …)
      prendre.json    # deck meta + cards (en / fr / example)
```

Authoring may move to YAML+Markdown later; **JSON is the runtime contract** for now. The API can emit the same shape later.

Card fields: `en`, `fr`, optional `example` + `exampleTranslation`, plus `type` / `subject` / `id`.
Study direction (EN→FR, FR→EN, mixed, both passes) is chosen in the app session, not in the JSON.
