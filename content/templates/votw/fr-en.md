<!--
LLM PROMPT — French Verb of the Week (for English speakers)
===========================================================
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
   content/en/fr/votw/{slug}.md
2. Keep every ## heading exactly as written below and in this order.
   Do not rename, reorder, add, or remove top-level ## sections.
3. Set the H1 to the French verb lemma (same string as title in frontmatter).
4. Fill YAML frontmatter: title, description, slug, target, locale, level,
   author, date. Set target: fr and locale: en.
   Keep draft: true unless the human asks to publish.
5. slug must be a URL-safe form of the infinitive (e.g. prendre, not Prendre).
6. Write all learner-facing prose in English.
7. For example pairs, use Markdown tables with columns French | English.
   Prefer 2–4 rows per table.
8. Under Meanings, order senses from most literal to most idiomatic.
   Use only as many ### Meaning N / Expression N / Mistake N blocks as needed;
   delete unused numbered blocks.
9. Follow the STYLE GUIDE comment below (audience, voice, writing, examples,
   translation, pedagogy, L1 interference). This file is for English-speaking
   learners only. Do not write for Spanish speakers or mix audiences.
10. Write clear learner-facing prose. No meta commentary, no "as an AI",
    no placeholder text like "TODO" or "fill in".
11. Before finishing, delete this LLM PROMPT comment, the STYLE GUIDE comment,
    the AUTHOR NOTES comment, and the SEO CHECKLIST comment from the output.
    The published file must start with the YAML frontmatter (---).
12. Do not wrap the answer in a code fence unless the human asks for one.

QUALITY BAR
- Introduction: ~100–200 words; why the verb matters; one central idea.
- Core Concept: semantic idea that links meanings — not a gloss list.
- Examples: natural, level-appropriate, accurate French with English glosses.
- Common Mistakes: typical for English speakers learning French (see L1).
- Summary: reinforce the core idea; do not restate every gloss.

Fill the template that follows (frontmatter, then body).
-->

<!--
STYLE GUIDE — French VOTW for English speakers (fr-en)
=====================================================
Pair: target=fr, locale=en. Do not reuse Spanish-audience guidance.

Audience
- Native English speakers learning French.
- Explain concepts without assuming prior grammatical knowledge.
- Do not assume they know Spanish or other Romance languages.

Voice
- Write like a native English speaker: natural idiom, rhythm, and word choice.
  Not translated-sounding, not textbook English, not generic AI English.
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
- Avoid AI-slop tropes. No em dashes (—). Avoid semicolons. Do not use
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
- In Common Mistakes, focus on errors English speakers typically make — not
  Hispanophone transfer errors.
-->

---
title:          # French verb lemma, e.g. Prendre
description:    # One-sentence meta description (English)
slug:           # Must match filename stem, e.g. prendre
target: fr      # Language taught
locale: en      # Language of the explanation (audience)
level:          # CEFR: A1 | A2 | B1 | B2 | C1 | C2
author:
date:           # YYYY-MM-DD
draft: true
---

<!--
  AUTHOR NOTES (delete this comment block before publishing)

  - Template: French VOTW for English speakers (fr-en)
  - Copy to content/en/fr/votw/{slug}.md
  - Keep every ## heading below exactly as written and in this order.
  - Replace the H1 with the verb (same as title).
  - Fill sections; remove unused Meaning / Expression / Mistake blocks.
  - Do not rename headings — the series TOC and future build checks rely on them.
  - Example pairs use | French | English | tables.
  - Link CEFR level codes in body copy to /en/cefr/ (e.g. [A1](/en/cefr/)).
    Do not put Markdown links in YAML frontmatter.
  - Voice and pedagogy: see STYLE GUIDE comment above (English audience, not ES).
  - To generate a draft with an LLM: paste this whole file and complete the
    INPUT fields in the LLM PROMPT comment at the top of the file.
-->

# Verb

Introductory paragraphs (about 100–200 words). Why the verb is worth learning.
Introduce the central idea without listing every translation.

## At a Glance

| Item | Value |
|------|-------|
| Infinitive | |
| Pronunciation | |
| CEFR | |
| Auxiliary | |
| Past Participle | |
| Core Meaning | |

## Core Concept

Explain the underlying semantic idea behind the verb. Prefer the concept that
links its meanings over a list of glosses.

## Meanings

<!-- Repeat ### Meaning N for each important sense, most literal → most idiomatic. -->

### Meaning 1

**Definition**

**Examples**

| French | English |
|--------|---------|
| | |
| | |

**Usage Notes**

### Meaning 2

**Definition**

**Examples**

| French | English |
|--------|---------|
| | |
| | |

**Usage Notes**

### Meaning 3

**Definition**

**Examples**

| French | English |
|--------|---------|
| | |
| | |

**Usage Notes**

## Common Constructions

Recurring grammatical patterns, for example:

- verb + noun
- verb + infinitive
- verb + de + infinitive
- verb + à + infinitive
- reflexive forms

Where a construction needs an example, use a table:

| French | English |
|--------|---------|
| | |

## Expressions and Idioms

<!-- Repeat ### Expression N for each item. Prefer meaning over literal translation. -->

### Expression 1

**Meaning**

**Example**

| French | English |
|--------|---------|
| | |

### Expression 2

**Meaning**

**Example**

| French | English |
|--------|---------|
| | |

## Register and Usage

Note whether usages are formal, informal, literary, conversational, regional, or dated.

## Common Mistakes

<!-- Mistakes English speakers commonly make when learning French. -->

### Mistake 1

| Incorrect | Correct |
|-----------|---------|
| | |

**Explanation**

### Mistake 2

| Incorrect | Correct |
|-----------|---------|
| | |

**Explanation**

## Related Verbs

Verbs learners confuse with this one, or that share similar meanings:

-
-
-

## Summary

Concise wrap-up of the verb’s core idea. Reinforce the semantic concept rather
than repeating individual translations.

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
