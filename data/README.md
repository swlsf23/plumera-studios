# App datasets

Non-page data for interactive apps (flashcard decks, etc.). Not consumed by the Python content builder.

## Layout

```text
data/
  {locale}/           # UI / explanation language (en, es, fr, …)
    {target}/         # language being taught (learn-french, …)
      prendre.tsv     # example: one deck file per verb (later)
```

v1 of the flashcard app uses an in-module sample deck. Loading from these files comes next; the API will eventually replace or feed the same shape.
