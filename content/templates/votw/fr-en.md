<!--
LLM PROMPT: French Verb of the Week (for English speakers)
==========================================================
You are drafting a Plumera Studios French Verb of the Week article for
English-speaking learners. Fill this Markdown template. Do not invent a
different structure.

INPUT (filled by the human before or with this prompt)
- French verb / infinitive:
- CEFR level:
- Author:
- Date (YYYY-MM-DD):
- Any focus notes (optional):

OUTPUT RULES
1. Return a complete Markdown file ready to save as
   content/en/learn-french/votw/{slug}.md
2. Keep every ## heading exactly as written below and in this order.
   Do not rename, reorder, or add top-level ## sections. Register and usage is
   the one optional section and may be deleted (see its note).
3. Set the H1 to the French verb lemma only (e.g. Prendre).
4. Fill YAML frontmatter: title, description, slug, target, locale, level,
   author, date. Set target: learn-french and locale: en.
   title is the full document <title>, not just the verb:
   "French Verb of the Week: {Verb} | Plumera". The builder uses it as-is.
   Keep draft: true unless the human asks to publish.
5. slug must be a URL-safe form of the infinitive, with the level as a suffix
   (e.g. votw-prendre-a1). frontmatter level is the source of truth. The suffix
   only keeps two articles about the same verb apart (prendre-a1, prendre-b2).
6. Write all learner-facing prose in English.
7. For example pairs, use Markdown tables with columns French | English.
   The language being taught goes in the left column. Prefer 2-4 rows.
8. For the present-tense conjugation grid in Forms and grammar, put
   <!-- table: forms --> on the line immediately above a Singular | Plural
   table (see content/README.md). Example pairs stay French | English without
   that marker.
9. Put <!-- art: band --> on its own line after Other common constructions and
   before Expressions and idioms (slim decorative band; see content/README.md).
10. Order the senses under How to use by a principle you state in that section's
    opening line, so the reader knows what separates them.
11. Every ## section opens with at least one sentence before any ### heading.
    Two headings must never sit next to each other with nothing in between, and
    that sentence must carry information rather than announce the section.
12. Do not use bold labels (**Definition**, **Examples**, **Usage Notes**,
    **Meaning**, **Explanation**). The heading names the item, the prose
    explains it, the table shows it.
13. Each sense is a heading, a short guidance line, then a French | English
    table. After that table you may add a short contrast (prose and/or a second
    table) when two correct verbs mean different things. Do not put that contrast
    under Common mistakes.
14. Under Common mistakes, the explanation goes before the table.
15. Use Incorrect / Correct only for genuine errors. A sentence that is
    grammatical but says something the learner did not intend still counts, so
    false friends belong here. If both versions are correct and simply mean
    different things, that is a contrast, not a mistake: put it in the relevant
    sense instead.
16. Do not point forward at items the reader has not reached. "These two" and
    "the first two" need an antecedent, as in "two of the mistakes below".
17. Do not state a rule in Forms and grammar that Common mistakes also covers.
18. Sentence case for all headings. A heading that is a French expression keeps
    its own capitalization.
19. Follow the STYLE GUIDE comment below (audience, voice, writing, examples,
    translation, pedagogy, L1 interference). This file is for English-speaking
    learners only. Do not write for Spanish speakers or mix audiences.
20. Write clear learner-facing prose. No meta commentary, no "as an AI",
    no placeholder text like "TODO" or "fill in".
21. Before finishing, delete this LLM PROMPT comment, the STYLE GUIDE comment,
    the AUTHOR NOTES comment, and the SEO CHECKLIST comment from the output.
    The published file must start with the YAML frontmatter (---).
22. Do not wrap the answer in a code fence unless the human asks for one.

QUALITY BAR
- Introduction: about 100 to 200 words, why the verb matters, and the central
  idea that ties its uses together.
- Forms and grammar: only the mechanics the examples below rely on, plus the
  forms table marker and a short past-tense note when the lesson uses it.
- Examples: natural, level-appropriate, accurate French with English glosses.
- Common mistakes: typical for English speakers learning French (see L1).
- Before you go: reinforce the core idea without restating every gloss.

Fill the template that follows (frontmatter, then body).
-->

<!--
STYLE GUIDE: French VOTW for English speakers (fr-en)
====================================================
Pair: target=fr, locale=en. Do not reuse Spanish-audience guidance.

Audience
- Readers using English to learn French. Do not assume they are native English
  speakers; keep explanation English clear for advanced ESL readers too.
  See docs/style-guide.md.
- Explain concepts without assuming prior grammatical knowledge.
- Do not assume they know Spanish or other Romance languages.

Voice
- Write clear, natural English with a personal teaching voice. Not
  translated-sounding, not textbook English, not generic AI English. Prefer
  concrete scenes and short sentences over culture-bound idiom.
- Friendly. Confident. Curious. Teacher.
- Conversational but precise.
- Never patronizing.
- Prefer explanation over definition.
- Assume the reader is curious, not studying for an exam.
- Prefer "Notice that..." over "Remember that..."
- Prefer "French uses..." over "French is..."
- Do not exaggerate rules.
- Avoid saying "simply", "just", "always", or "never" unless literally true.

Writing
- Use active voice.
- Prefer short paragraphs.
- Avoid unnecessary grammar jargon. If you need a term, explain it in plain English.
- Introduce French terminology only when useful.
- Explain why something works, not just what it means.
- Avoid AI-slop tropes. No em dashes. No semicolons. Do not use
  "this is not X, it's Y" (or "not X but Y") contrast formulas.

Examples
- Use natural, contemporary French.
- Avoid textbook-only examples where possible.
- Prefer examples someone might actually hear or say.

Translation
- Translate naturally into English.
- Don't force word-for-word translations unless illustrating a point.

Pedagogy
- Build from concrete meanings to abstract or idiomatic ones.
- Highlight patterns rather than isolated facts.
- Compare with English only when it aids understanding.
- Never use Spanish (or another L3) as a bridge.

L1 interference (English → French)
- Anticipate calques from English (especially phrasal-verb habits).
- Watch overuse of être where French prefers another verb or construction.
- Address false friends that trip English speakers when relevant to this verb.
- In Common mistakes, focus on errors English speakers typically make, not
  Hispanophone transfer errors.
-->

---
title:          # Full <title>, e.g. "Prendre: Everyday Uses (A1 French) | Plumera Studios"
description:    # One-sentence meta description (English)
slug:           # votw-{verb}-{level}, e.g. votw-prendre-a1
target: learn-french      # Language taught
locale: en      # Language of the explanation (audience)
level:          # CEFR: A1 | A2 | B1 | B2 | C1 | C2, or a range like A1, A2
author:
date:           # YYYY-MM-DD
draft: true
related:        # Sidebar "You might also like" cards (optional)
  - href:       # Site path, e.g. /en/learn-french/votw/ or /en/learn-french/votw/votw-autre-a1/
    title:      # Optional override; omit to use the target page H1
    meta:       # Optional subtitle (e.g. date)
---

<!--
  AUTHOR NOTES (delete this comment block before publishing)

  - Template: French VOTW for English speakers (fr-en)
  - Copy to content/en/learn-french/votw/{slug}.md
  - Keep every ## heading below as written and in this order. Register and usage
    is optional and may be deleted.
  - Replace the H1 with the verb lemma only (e.g. Prendre), not the full title.
  - Add as many senses, expressions, and mistakes as the verb needs. Delete the
    spare blocks.
  - Every ## opens with a sentence before any ###. No stacked headings, and no
    filler sentence either: it has to say something.
  - Present grid: <!-- table: forms --> then | Singular | Plural |.
  - Example pairs: | French | English |, French on the left.
  - Keep <!-- art: band --> between Other common constructions and Expressions.
  - Link CEFR level codes in body copy to /en/cefr/ (e.g. [A1](/en/cefr/)).
    Do not put Markdown links in YAML frontmatter.
  - Voice and pedagogy: see STYLE GUIDE comment above (English audience, not ES).
  - To generate a draft with an LLM: paste this whole file and complete the
    INPUT fields in the LLM PROMPT comment at the top of the file.
-->

# Verb

Introductory paragraphs (about 100-200 words). Why the verb is worth learning,
and the idea that ties its uses together. Do not list every translation.

## Forms and grammar

Open with why the forms matter (irregular stem, shared family, a habit that
keeps sentences correct). Then the present grid:

<!-- table: forms -->

| Singular | Plural |
|----------|--------|
| | |
| | |
| | |

A short note on what to notice in the grid (sound alike, stem split, family
verbs). Add past tense with *avoir* / *être* and the participle only if the
examples below use it, as a French | English table.

## How to use {verb}

Open with the principle that orders the senses below, so the reader knows what
separates them rather than meeting three headings cold.

### First sense, as a short descriptive heading

One line of guidance: what this use covers, or where French parts company with
English.

| French | English |
|--------|---------|
| | |
| | |

### Second sense

One line of guidance.

| French | English |
|--------|---------|
| | |
| | |

### Third sense

One line of guidance.

| French | English |
|--------|---------|
| | |
| | |

<!-- Optional: after a sense table, add a short contrast when two correct verbs
     mean different things (prose + French | English table). Not a mistake. -->

## Other common constructions

One sentence introducing combinations that fall outside the senses above.
Prefer collocations where French and English diverge.

| French | English |
|--------|---------|
| | |
| | |

A closing note on whichever row is least predictable for an English speaker.

<!-- art: band -->

## Expressions and idioms

One sentence on what sets these apart from the senses above (fixed phrases;
learn the whole unit).

### french expression

Short gloss.

| French | English |
|--------|---------|
| | |

### second expression

Short gloss.

| French | English |
|--------|---------|
| | |

## Register and usage

OPTIONAL, and harder to write than it looks. Keep it only if there is something
concrete to say: a use that is formal, dated, regional, or that would sound
wrong in ordinary conversation. Delete the whole section if the honest answer is
that the verb is neutral everywhere. Do not pad it.

## Common mistakes

One sentence characterizing the errors below and what they have in common, so
"the first" and "the other" have something to refer to.

### First mistake, as a short descriptive heading

The explanation, before the table, so the reader knows what to look for.

| Incorrect | Correct |
|-----------|---------|
| | |

### Second mistake

The explanation.

| Incorrect | Correct |
|-----------|---------|
| | |

## Related verbs

Verbs learners confuse with this one, or that cover part of its ground, each
with a short gloss:

- verb: short gloss
- verb: short gloss
- verb: short gloss

Call out the one that causes the most trouble in a blockquote, then optional
examples:

> *Verb* is the one to watch. …

| French | English |
|--------|---------|
| | |

## Before you go

One or two sentences reinforcing the central idea, with the level linked
(e.g. [A1](/en/cefr/)). Do not recap the glosses.

<!--
  SEO CHECKLIST (delete before publishing)

  - Primary keyword:
  - Secondary keywords:
  - Suggested page title:
  - Suggested meta description:
  - Suggested URL:
  - Image alt text:
  - Schema FAQ opportunities:
  - Internal links added:
  - External references checked:
-->
