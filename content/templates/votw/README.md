# VOTW templates

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

Every template carries the same sections in the same order, named in the locale's language:

1. H1 and introduction
2. Forms and grammar
3. How to use *verb*, with one `###` per sense
4. Common constructions
5. Expressions and idioms
6. Register and usage. **Optional**, delete it unless there is something concrete to say
7. Common mistakes, with one `###` per mistake
8. Related verbs
9. Summary

Four rules hold across all six:

- Every `##` opens with a sentence before any `###`. No two headings in a row, and the sentence has to carry information rather than announce the section.
- No bold labels. The heading names the item, the prose explains it, the table shows it.
- The language being taught goes in the left column of every example table.
- Incorrect/Correct is for genuine errors, including a false friend that makes a grammatical sentence say the wrong thing. Two correct sentences that mean different things are a contrast, and belong in the relevant sense as a two-row comparison.

Level lives in frontmatter and is the source of truth. The level suffix in a filename only keeps two articles about the same verb apart (`votw-prendre-a1`, `votw-prendre-b2`).
