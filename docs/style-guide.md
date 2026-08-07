# Plumera Studios content style guide

This guide defines the editorial voice, structure, and writing conventions for Plumera language-learning content.

The goal is to make Plumera clear, useful, engaging, and easy to navigate for learners at different levels.

Learner-facing copy on the site lives in Markdown under `content/` and in landing HTML prose. Pair-specific drafting notes still live in the VOTW templates.

Related:

- Per-pair voice and pedagogy: [`content/templates/votw/`](../content/templates/votw/) (see that [README](../content/templates/votw/README.md))
- CI banned characters: [`tools/ci/check_prohibited_chars.py`](../tools/ci/check_prohibited_chars.py) (also noted in [deploy.md](deploy.md))

## Voice

### Write to the learner

Use second person when explaining what the learner can do, recognize, or expect.

Prefer:

> You’ll use *faire* in many common weather expressions.

Over:

> French uses *faire* in many common weather expressions.

Prefer:

> You can use *faire* for actions you carry out and things you create.

Over:

> *Faire* covers actions that are carried out and things that are created.

Do not force second person into every sentence. Statements about French, English, grammar, or a particular expression can use whatever construction is clearest.

### Prefer active voice

Use active verbs and direct constructions.

Prefer:

> Learn the patterns instead.

Over:

> The patterns should be learned instead.

Prefer:

> Use *faire* in these expressions.

Over:

> *Faire* is used in these expressions.

Active voice should not become command-heavy technical writing. Use imperatives when they give the learner a useful action, not simply to make every sentence active.

### Use plain English

Write for an international audience. A reader of an English-language page may not be a native English speaker.

Avoid unnecessary idiomatic English, clever phrasing, and expressions that require cultural knowledge when simpler language works.

Prefer:

> common errors

Over:

> common slips

Prefer:

> After you learn...

Over:

> Once you've got the hang of...

Prefer *after* to *once* when describing a learning sequence. *After* is more explicit for readers who use English as an additional language. Rejecting an idiomatic phrase like "once you've got the hang of" is not enough on its own: use *after* as the default sequencing word even in plain constructions ("After you learn the basic uses…" not "Once you learn the basic uses…").

Clarity takes priority over personality.

### Keep languages grammatically separate

Avoid inserting conjugated French verbs into otherwise English sentences.

Avoid:

> You *fabriques* a table, but you *fais* a cake.

Prefer:

> You use *fabriquer* for something you manufacture or build. You use *faire* for broader everyday actions.

English-language pages can discuss French words and expressions freely, but the surrounding sentence should remain natural English.

### Make the reference language explicit when necessary

Do not assume every reader's native language is English.

When a translation relationship matters, identify English explicitly.

Prefer:

> *Faire* can mean "to do" or "to make" in English.

This also makes content easier to adapt if Plumera pages are later localized into other languages.

### Avoid unnecessary qualifiers

Remove words such as *often*, *especially*, *generally*, *usually*, or *really* when they merely soften the sentence.

Keep qualifiers when they make a statement more accurate.

Prefer:

> A direct English translation won't always help.

Over:

> A direct English translation often won't help.

The goal is precision, not absolute statements.

## Teaching style

### Teach patterns, not just translations

Do not treat French words as if they always have one English equivalent.

Show learners the patterns that determine meaning and usage.

For example:

> Don't try to translate *faire* with a single English verb.

Help learners move gradually from word-by-word translation toward recognizing French constructions directly.

### Explain why something matters

Do more than state a rule when a short explanation will help the learner understand or remember it.

For example:

> Unlike most French verbs, *faire* has a *vous* form ending in **-tes**.

But do not explain a point twice. If an example already makes the meaning obvious, additional explanation may not earn its space.

### Target the middle between lesson and reference

Every page should work both for someone reading it from beginning to end and for someone arriving from search at a specific section.

Each section should therefore make sense independently, but the page should still have momentum when read sequentially.

Avoid both extremes:

- encyclopedic explanations that interrupt the lesson
- explanations so brief that search visitors cannot understand the section independently

### Let complexity determine explanation length

Do not make every section the same length for visual consistency.

A transparent expression may need one sentence and examples. A difficult idiom may need an explanation of its figurative image.

Use as much explanation as the learner needs, then stop.

### Examples should teach

Examples should demonstrate the point immediately around them.

Avoid adding examples merely to increase quantity.

When an English translation has multiple natural possibilities, show useful alternatives when they help clarify the French meaning.

## CEFR and scope

### Respect the target level

Each page targets a CEFR level. Do not try to cover every meaning, construction, expression, and exception on one page.

Teach what belongs at the stated level and move more advanced material to the appropriate companion topic.

Higher-level pages can assume knowledge established in lower-level pages.

### Avoid unnecessary prerequisites

Pages belong to a learning path, but they should still work as search landing pages.

A learner arriving directly on an Expressions page should not be told that they must leave and read Basics first.

Instead, provide a useful backward link:

> For a refresher on the basic forms and uses, start with [Faire - basics](...).

### Build explicit learning paths

Related pages are not merely collections of internal links. Verb clusters form learning paths.

For example:

> Basics → Expressions and common errors → Advanced

Use the end of a topic to point learners toward the next logical step.

Related-content components such as "You might like" serve discovery. In-body next-step links serve learning progression.

If the site layout changes, reconsider this division rather than duplicating navigation unnecessarily.

## Verb-cluster architecture

A verb cluster may eventually contain:

- core usage
- expressions and common errors
- advanced usage
- idioms
- conjugation
- practice

Not every verb needs every topic immediately.

### Core usage topics

Use a reader-facing title rather than exposing the internal "Basics" classification.

Preferred pattern:

> How to use *[verb]*

HTML title:

> How to use [verb] (A2 French) | Plumera Studios

The internal slug or content architecture may still use `basics`.

### A2 expressions topics

Use a standard reader-facing H1 that describes the purpose of the page rather than an internal content label such as "Faire - expressions":

> # Expressions and common errors with *[verb]*

Examples:

> # Expressions and common errors with *faire*
>
> # Expressions and common errors with *prendre*
>
> # Expressions and common errors with *tenir*

Use a consistent H2 structure across verbs:

> ## Common expressions
>
> ## Usage patterns
>
> ## Common errors

**Common expressions** covers useful fixed combinations and lexical expressions.

**Usage patterns** covers larger productive constructions that learners can recognize and reuse.

**Common errors** covers mistakes directly associated with the target verb and the material taught on the page.

Do not create an "Idioms" section merely because some expressions are not translated word for word.

### Idioms

Use *idiom* in the stricter sense: a figurative expression whose overall meaning cannot reliably be determined from the individual words.

For example:

> *faire tout un fromage de quelque chose*

is appropriate for idiom content.

By contrast:

> *faire attention à*

is better treated as a common expression.

Idioms can have their own topic when a verb has enough useful material to justify one.

Possible pattern:

> [Verb] - idioms (B1-B2 French)

Do not pad an idioms page to reach an arbitrary number of expressions. Curate for frequency, usefulness, and learner level.

## Introductions

### Give the learner a reason to continue

The opening should quickly establish why the topic matters.

Avoid opening with dictionary-style definitions when a learner-centered explanation is possible.

For example:

> *Faire* can mean "to do" or "to make" in English. But you’ll use it for much more than that.

The introduction should establish the central problem or idea that the rest of the page will solve.

### Keep introductions focused

Do not preview every section mechanically.

Avoid positional language such as:

> The three uses below...

Prefer language that describes the content itself:

> You’ll use *faire* in several everyday situations, from doing or making something to talking about the weather and activities.

## Headings

### Use headings for meaning, not keyword repetition

H2 headings should identify the purpose of the section.

Prefer:

> ## Common expressions
>
> ## Usage patterns
>
> ## Common errors

Over:

> ## Common expressions with faire
>
> ## Usage patterns with faire
>
> ## Common errors with faire

The page title, H1, URL, body copy, and examples already establish the target verb. Do not repeat it mechanically in every heading for SEO.

### Avoid consecutive headings when context helps

An H2 followed immediately by an H3 is not inherently wrong on the web, but a short introductory sentence is useful when it explains what the section contains or how the subsections relate.

Do not add filler solely to prevent two headings from appearing together.

### Avoid positional navigation

Do not use *above* and *below* when referring to content. Those words depend on page layout.

Prefer semantic references to sections, examples, or topics.

*Next* is appropriate when it identifies the next step in a learning path. It describes pedagogical sequence, not physical position on the page.

## Tables

### Use tables for comparisons and examples

Tables work well for:

- conjugation forms
- French/English example pairs
- incorrect/correct comparisons
- related-verb comparisons

### Introduce tables consistently

Use a colon when the preceding sentence directly introduces the contents of the table.

For example:

> You can use *faire* for actions you carry out and things you create:

If the preceding sentence stands independently and the table merely provides additional illustration, use a period.

Parallel sections performing the same function should use the same construction.

### Related verbs

The Related verbs section should teach semantic boundaries, not function as a thesaurus.

A useful table structure is:

| Verb | English | When to use it |
| ---- | ------- | -------------- |

Choose a small number of neighboring verbs that learners are genuinely likely to confuse with the target verb.

Explain enough for the learner to understand why they might choose one verb instead of another.

Until a related verb has its own Plumera topic, the Related verbs section can carry slightly more explanation. Later, that explanation can become a concise summary plus an internal link.

### Table layout

- Do **not** put two tables back to back. Separate them with a short teaching sentence, a note, or a subsection heading.
- A gloss or list table followed immediately by an example table still counts as two in a row. Bridge them.
- Incorrect / Correct tables are for genuine errors (including false friends). Two correct sentences that mean different things are a contrast, not a mistake.

## French typography and terminology

Italicize French words and expressions when discussing them as linguistic items in English prose.

For example:

> *faire*
>
> *faire attention à*
>
> *vous faites*

Use italics consistently in headings when the heading itself is a French expression:

> ### *faire la connaissance de*

Bold may be used to draw attention to a specific morphological feature:

> **-tes**

Do not over-format ordinary French example sentences inside tables when the table already identifies them as French.

## Metadata

### Titles

Titles should describe learner intent rather than expose internal taxonomy when possible.

Prefer:

> How to use faire (A2 French) | Plumera Studios

Over:

> Faire - basics (A2 French) | Plumera Studios

Keep title patterns consistent across equivalent topics.

Frontmatter `title` is the full document `<title>` (include the brand suffix). Prefer `| Plumera Studios`.

`{Level}` in titles must match frontmatter `level` (including multi-level bands when the builder supports them). H1 stays short. Series signal stays in the eyebrow. Do not put "Conjugation" in a VOTW title unless the page is actually a conjugation page.

### Descriptions

Use active verbs and tell the learner what they will gain.

Prefer:

> Learn the core meanings, grammar, and major usage patterns of the French verb faire.

Prefer:

> Learn useful expressions and common errors for the French verb faire.

Avoid passive descriptions or generic summaries.

## Before you go

The "Before you go" section should give the learner a useful takeaway, next step, or both.

Do not simply summarize the entire article.

A good takeaway reinforces the learning strategy:

> As you recognize more of these patterns, you'll rely less on translating *faire* word by word.

When the page belongs to an explicit learning path, add a short next-step sentence. *Next* is fine here because it names the pedagogical sequence, not a place on the page:

> Next, learn the fixed phrases and common errors in [Faire - expressions and common errors](...).

Do not duplicate a list of related links already presented immediately by the interface.

Future Practice and Conjugation topics can become natural action-oriented next steps from this section.

## SEO

Write for the learner first, while making the page's subject and search intent unmistakable.

Use the target verb naturally in:

- the HTML title
- H1
- introduction
- examples and explanations
- metadata description
- URL or content architecture where appropriate

Do not repeat the keyword mechanically in every H2.

Prefer titles and headings that correspond to genuine learner intent, such as:

> How to use faire

rather than internal editorial classifications such as:

> Faire - basics

Internal linking should reinforce semantic relationships between verb topics, related verbs, CEFR material, expressions, advanced constructions, idioms, conjugation, and practice.

## `###` section openers

Every `###` (senses, expressions, common mistakes, and similar) opens with a full sentence before the table or further teaching. Do not use bare "To…" gloss fragments ("To agree.").

- Good: "Use *être d'accord* to say that you agree with someone."
- Good: "Use *prendre* when you take a bus, a drink, or medicine."
- Weak: "To agree."
- Weak: jumping straight to a table

Extra explanation can follow that opener. The first sentence should still make sense if the reader only skims headings and lead-ins. Apply this in new drafts and when revising published lessons.

## Anti-slop (enforced)

Treat these as AI tells. They are banned in shippable site copy:

- No em dashes (`—`, U+2014)
- No semicolons (`;`)
- Avoid "this is not X, it's Y" / "not X but Y" contrast formulas as a default rhetorical move

CI fails the build if `;` or `—` appear in locale Markdown or landing prose.

## Editing principles

### Consistency is deliberate, not mechanical

Keep recurring structures, terminology, punctuation conventions, and learning paths consistent across equivalent pages.

Do not force sentences to have identical shapes merely because the pages share a template.

### Don't over-explain

After writing an explanation, ask:

> Does the next sentence teach the learner anything new?

If not, cut it.

### Don't under-explain for brevity

Concise content still needs to resolve the learner's likely question.

The goal is not the fewest words. The goal is the fewest words needed for a clear and useful explanation.

### Prefer precision over cleverness

If a sentence sounds memorable but takes extra effort to interpret, rewrite it.

An A2 learner should not need to decode the English before learning the French.

### Stop when the page is done

Do not keep polishing clear, accurate prose merely because another wording is possible.

Distinguish between:

- factual or grammatical errors
- style inconsistencies
- meaningful improvements
- optional editorial preferences

During final sanity checks, report only the category the editor requested.

### What not to edit casually

Do not "improve" published or in-progress lesson wording unless the task asks for it. Voice is intentional; drive-by rewrites create drift.

### Examples and language bridges

- Prefer examples someone might actually hear or say. Avoid textbook-only lines where possible.
- Build from concrete meanings to abstract or idiomatic ones.
- Never use a third language as a bridge between locale and target.

## Voice ledger

Running list of Plumera teaching moves and distinctive explanations. Add entries when a phrasing or mental model is worth reusing across lessons.

- "French treats tangling or getting stuck as something that 'takes' itself into an object."
  Conceptual explanation rather than a translation. Helps learners see the event through a French lens.

- "The same shapes show up again and again."
  Encourages noticing recurring grammatical and lexical patterns instead of memorizing isolated idioms.

- "Recognizing the pattern matters more than forcing every line through the English verb 'take'."
  Broader teaching philosophy: prioritize French conceptual patterns over mapping every expression onto English.
