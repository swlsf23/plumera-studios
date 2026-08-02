# Plumera content style guide

Learner-facing copy on the site (Markdown under `content/`, landing HTML prose). This file is the source of truth for shared editorial rules. Pair-specific drafting notes still live in the VOTW templates.

Related:

- Per-pair voice and pedagogy: `content/templates/votw/` (see that [README](../content/templates/votw/README.md))
- CI banned characters: `tools/ci/check_prohibited_chars.py` (also noted in [deploy.md](deploy.md))

## Audience (especially `locale: en`)

English on `/en/` is the **explanation language**, not a promise that readers are native English speakers. Many learners use English as a shared medium while learning French (or another target).

Balance a personal teaching voice with English that travels:

- Put personality in **rhythm and concreteness**, not in obscure idiom. A short list of real situations (suitcase, door, shop) beats a clever native-only turn of phrase.
- Prefer **transparent metaphors** over culture-bound ones. "Worth learning in depth," "notice the split," "that mix can feel confusing" travel well. Phrases like "reach for," "slippery," or heavy figurative English ask more of the reader.
- **One slightly literary verb per beat is fine** if the rest of the sentence is plain. Stacking writerly turns starts to feel like native-only prose (or AI).
- When in doubt, **say the meaning twice**: image or vivid verb first, then a plain clause ("Some uses are literal. Others are fixed phrases…").

Creative = concrete scenes, short sentences, clear teaching moves. Avoid = English idioms you would need to gloss for an advanced ESL reader.

Locale-pair templates may still say "for English speakers." Read that as **readers using English for the lesson**, not as native-speaker-only prose.

## Voice

- Friendly. Confident. Curious. Teacher.
- Conversational but precise. Never patronizing.
- Prefer explanation over definition.
- Assume the reader is curious, not studying for an exam.
- Prefer "Notice that…" over "Remember that…"
- Prefer "French uses…" over "French is…"
- Prefer "after" over "once" for sequencing ("After the house set feels steady…" not "Once the house set feels steady…").
- Do not exaggerate rules.
- Avoid "simply," "just," "always," or "never" unless literally true.
- Prefer active voice and short paragraphs.
- Avoid unnecessary grammar jargon. If you need a term, explain it in plain English.
- Explain why something works, not just what it means.
- Do not write Forms and grammar (or similar) like an API reference. Name the pattern, say why it matters for the learner, then show it.

## Anti-slop (enforced)

Treat these as AI tells. They are banned in shippable site copy:

- No em dashes (`—`, U+2014)
- No semicolons (`;`)
- Avoid "this is not X, it's Y" / "not X but Y" contrast formulas as a default rhetorical move

CI fails the build if `;` or `—` appear in locale Markdown or landing prose.

## Document `<title>` (EN French verbs)

Frontmatter `title` is the full document `<title>` (include the brand suffix). Prefer `| Plumera Studios`.

For English explanations of French verbs:

- **VOTW / everyday-uses lesson:** `{Verb}: Everyday Uses ({Level} French) | Plumera Studios`
  - Example: `Prendre: Everyday Uses (A1 French) | Plumera Studios`
- **B1 idioms companion:** `{Verb}: Idioms & Fixed Expressions ({Level} French) | Plumera Studios`
  - Example: `Prendre: Idioms & Fixed Expressions (B1 French) | Plumera Studios`

Rules:

- `{Level}` must match frontmatter `level`.
- H1 stays short (lemma for VOTW; idioms heading for companions). Series signal stays in the eyebrow.
- Do not put "Conjugation" in the VOTW title unless the page is actually a conjugation page.
- Other locale pairs may keep localized title shapes in their templates until those series get the same SEO pass.

## Series consistency vs variety

For Verb of the Week and similar series:

- **Same skeleton across lessons is fine** (section order, table shapes, a short bridge into the next section). Bridge lines may be nearly parallel from verb to verb.
- **Vary the openers.** A concrete catalog or colon-list beat is strong once or twice. Do not reuse the same intro shape on every VOTW.
- Keep Forms and grammar parallel in *design* (irregular lead-in → table → one teaching note → past tense) without copying dry reference wording.

## Companion links (VOTW)

When a Verb of the Week lesson has a companion article (idioms / fixed expressions), mention it in **Before you go** with a link, after the core takeaway. Also list it in frontmatter `related`. Do not rely on the Expressions section alone to point readers onward.

## `###` section openers

Every `###` (senses, expressions, common mistakes, and similar) opens with a short meaning gloss before the table or further teaching. Prefer a clear "To…" line, with an optional nuance:

- Good: "To start doing something, often suddenly or after a pause."
- Good: "To keep going when something is hard."
- Weak: "Used when…" with no meaning stated
- Weak: jumping straight to a table

Extra explanation can follow the gloss. The gloss itself should stand alone if the reader only skims headings and first lines. Apply this in new drafts and when revising published lessons.

## Tables

- Do **not** put two tables back to back. Separate them with a short teaching sentence, a note, or a subsection heading.
- A gloss or list table followed immediately by an example table still counts as two in a row. Bridge them.
- Incorrect / Correct tables are for genuine errors (including false friends). Two correct sentences that mean different things are a contrast, not a mistake.

## Examples and pedagogy

- Prefer examples someone might actually hear or say. Avoid textbook-only lines where possible.
- Build from concrete meanings to abstract or idiomatic ones.
- Highlight patterns rather than isolated facts.
- Compare with English only when it aids understanding.
- Never use a third language as a bridge between locale and target.

## What not to edit casually

Do not "improve" published or in-progress lesson wording unless the task asks for it. Voice is intentional; drive-by rewrites create drift.

## Voice ledger

Running list of Plumera teaching moves and distinctive explanations. Add entries when a phrasing or mental model is worth reusing across lessons.

- "French treats tangling or getting stuck as something that 'takes' itself into an object."
  Conceptual explanation rather than a translation. Helps learners see the event through a French lens.

- "The same shapes show up again and again."
  Encourages noticing recurring grammatical and lexical patterns instead of memorizing isolated idioms.

- "Recognizing the pattern matters more than forcing every line through the English verb 'take'."
  Broader teaching philosophy: prioritize French conceptual patterns over mapping every expression onto English.
