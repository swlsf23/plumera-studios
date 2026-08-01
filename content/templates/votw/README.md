# VOTW templates

Site-wide editorial bar (including English as explanation language for non-native readers): [docs/style-guide.md](../../../docs/style-guide.md).

Naming: `{target}-{locale}.md`

- **target**: language of the verb (taught)
- **locale**: language of the explanation (audience / UI)

| File | Verb language | For speakers of | Explanations in |
|------|---------------|-----------------|-----------------|
| `fr-en.md` | French | English | English |
| `fr-es.md` | French | Spanish | Spanish |
| `en-fr.md` | English | French | French |
| `en-es.md` | English | Spanish | Spanish |
| `es-en.md` | Spanish | English | English |
| `es-fr.md` | Spanish | French | French |

Templates are not built by the content builder. Copy into `content/{locale}/{target}/votw/{slug}.md` when drafting (e.g. French verbs for an English audience → `content/en/learn-french/votw/…`).

## Article shape

Matches published EN VOTW lessons (`votw-prendre-a1`, `votw-tenir-a2`). Every template carries the same sections in the same order, named in the locale's language:

1. H1 (verb lemma only) and introduction
2. Forms and grammar — include `<!-- table: forms -->` above the Singular | Plural present grid
3. How to use *verb*, with one `###` per sense (optional contrast after a sense when two correct verbs differ)
4. Other common constructions
5. `<!-- art: band -->` (builder decorative band; see [content/README.md](../../README.md))
6. Expressions and idioms
7. Register and usage. **Optional**, delete it unless there is something concrete to say
8. Common mistakes, with one `###` per mistake
9. Related verbs — bullets plus a blockquote for the one to watch
10. Before you go (not “Summary”). If a companion article exists, link it here after the core takeaway.

Rules that hold across pairs:

- Every `##` opens with a sentence before any `###`. No two headings in a row, and the sentence has to carry information rather than announce the section.
- Every `###` opens with a short meaning gloss (often a "To…" line, optional nuance) before the table. See [docs/style-guide.md](../../../docs/style-guide.md) (`###` section openers).
- No bold labels. The heading names the item, the prose explains it, the table shows it.
- The language being taught goes in the left column of every example table.
- Incorrect/Correct is for genuine errors, including a false friend that makes a grammatical sentence say the wrong thing. Two correct sentences that mean different things are a contrast, and belong in the relevant sense (not under Common mistakes).
- Title frontmatter is `… | Plumera` (full document `<title>`). H1 is the lemma only.

Level lives in frontmatter and is the source of truth. The level suffix in a filename only keeps two articles about the same verb apart (`votw-prendre-a1`, `votw-prendre-b2`).
