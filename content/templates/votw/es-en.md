<!--
LLM PROMPT: Spanish Verb of the Week (for English speakers)
===========================================================
You are drafting a Plumera Studios Spanish Verb of the Week article for
English-speaking learners. Fill this Markdown template. Do not invent a
different structure.

INPUT (filled by the human before or with this prompt)
- Spanish verb / infinitive:
- CEFR level:
- Author:
- Date (YYYY-MM-DD):
- Any focus notes (optional):

OUTPUT RULES
1. Return a complete Markdown file ready to save as
   content/en/es/votw/{slug}.md
2. Keep every ## heading exactly as written below and in this order.
   Do not rename, reorder, or add top-level ## sections. Register and usage is
   the one optional section and may be deleted (see its note).
3. Set the H1 to the Spanish verb lemma only (e.g. Tomar).
4. Fill YAML frontmatter: title, description, slug, target, locale, level,
   author, date. Set target: es and locale: en.
   title is the full document <title>, not just the verb:
   "Spanish Verb of the Week: Tomar". The builder uses it as-is.
   Keep draft: true unless the human asks to publish.
5. slug must be a URL-safe form of the infinitive, with the level as a suffix
   (e.g. votw-tomar-a1). frontmatter level is the source of truth. The suffix
   only keeps two articles about the same verb apart (tomar-a1, tomar-b2).
6. Write all learner-facing prose in English.
7. For example pairs, use Markdown tables with columns Spanish | English.
   The language being taught goes in the left column. Prefer 2-4 rows.
8. Order the senses under How to use by a principle you state in that section's
   opening line, so the reader knows what separates them.
9. Every ## section opens with at least one sentence before any ### heading.
   Two headings must never sit next to each other with nothing in between, and
   that sentence must carry information rather than announce the section.
10. Do not use bold labels (**Definition**, **Examples**, **Usage Notes**,
    **Meaning**, **Explanation**). The heading names the item, the prose
    explains it, the table shows it.
11. Each sense is a heading, one line of guidance, then a table. Nothing else.
12. Under Common mistakes, the explanation goes before the table.
13. Use Incorrect / Correct only for genuine errors. A sentence that is
    grammatical but says something the learner did not intend still counts, so
    false friends belong here. If both versions are correct and simply mean
    different things, that is a contrast, not a mistake: put it in the relevant
    sense as a two-row comparison instead.
14. Do not point forward at items the reader has not reached. "These two" and
    "the first two" need an antecedent, as in "two of the mistakes below".
15. Do not state a rule in Forms and grammar that Common mistakes also covers.
16. Sentence case for all headings. A heading that is a Spanish expression keeps
    its own capitalization.
17. Follow the STYLE GUIDE comment below (audience, voice, writing, examples,
    translation, pedagogy, L1 interference). This file is for English-speaking
    learners only. Do not write for French speakers or mix audiences.
18. Write clear learner-facing prose. No meta commentary, no "as an AI",
    no placeholder text like "TODO" or "fill in".
19. Before finishing, delete this LLM PROMPT comment, the STYLE GUIDE comment,
    the AUTHOR NOTES comment, and the SEO CHECKLIST comment from the output.
    The published file must start with the YAML frontmatter (---).
20. Do not wrap the answer in a code fence unless the human asks for one.

QUALITY BAR
- Introduction: about 100 to 200 words, why the verb matters, and the central
  idea that ties its uses together.
- Forms and grammar: only the mechanics the examples below rely on, including
  stem changes and any irregular preterite.
- Examples: natural, level-appropriate, accurate Spanish with English glosses.
- Common mistakes: typical for English speakers learning Spanish (see L1).
- Summary: reinforce the core idea without restating every gloss.

Fill the template that follows (frontmatter, then body).
-->

<!--
STYLE GUIDE: Spanish VOTW for English speakers (es-en)
=====================================================
Pair: target=es, locale=en. Do not reuse French-audience or Spanish-audience
guidance.

Audience
- Native English speakers learning Spanish.
- Explain concepts without assuming prior grammatical knowledge.
- Do not assume they know French or other Romance languages.

Voice
- Write like a native English speaker: natural idiom, rhythm, and word choice.
  Not translated-sounding, not textbook English, not generic AI English.
- Friendly. Confident. Curious. Teacher.
- Conversational but precise.
- Never patronizing.
- Prefer explanation over definition.
- Assume the reader is curious, not studying for an exam.
- Prefer "Notice that..." over "Remember that..."
- Prefer "Spanish uses..." over "Spanish is..."
- Do not exaggerate rules.
- Avoid saying "simply", "just", "always", or "never" unless literally true.

Writing
- Use active voice.
- Prefer short paragraphs.
- Avoid unnecessary grammar jargon. If you need a term, explain it in plain
  English. Subjunctive and preterite need a plain-English gloss the first time.
- Introduce Spanish terminology only when useful.
- Explain why something works, not just what it means.
- Avoid AI-slop tropes. No em dashes. No semicolons. Do not use
  "this is not X, it's Y" (or "not X but Y") contrast formulas.

Examples
- Use natural, contemporary Spanish.
- Avoid textbook-only examples where possible.
- Prefer examples someone might actually hear or say.
- Where peninsular and Latin American usage differ, say so instead of presenting
  one as correct. Note vosotros and ustedes when the verb's forms make it
  relevant.

Translation
- Translate naturally into English.
- Don't force word-for-word translations unless illustrating a point.

Pedagogy
- Build from concrete meanings to abstract or idiomatic ones.
- Highlight patterns rather than isolated facts.
- Compare with English only when it aids understanding.
- Never use French (or another L3) as a bridge.

L1 interference (English → Spanish)
- Anticipate calques from English, especially phrasal-verb habits and verb +
  noun collocations.
- Watch ser and estar, which English covers with be alone.
- Watch the past: English has one simple past where Spanish chooses between the
  preterite and the imperfect.
- Watch the subjunctive, which is ordinary in Spanish and nearly gone in English.
- Watch gustar-type verbs, where the thing liked is the subject.
- Watch por and para, and the personal a, which English has no equivalent for.
- Address false friends that trip English speakers when relevant to this verb.
- In Common mistakes, focus on errors English speakers typically make, not
  francophone transfer errors.
-->

---
title:          # Full <title>, e.g. "Plumera | Spanish Verb of the Week: Tomar"
description:    # One-sentence meta description (English)
slug:           # votw-{verb}-{level}, e.g. votw-tomar-a1
target: es      # Language taught
locale: en      # Language of the explanation (audience)
level:          # CEFR: A1 | A2 | B1 | B2 | C1 | C2, or a range like A1, A2
author:
date:           # YYYY-MM-DD
draft: true
related:        # Sidebar "You might also like" cards (optional)
  - href:       # Site path, e.g. /en/es/votw/ or /en/es/votw/votw-otro-a1/
    title:      # Optional override; omit to use the target page H1
    meta:       # Optional subtitle (e.g. date)
---

<!--
  AUTHOR NOTES (delete this comment block before publishing)

  - Template: Spanish VOTW for English speakers (es-en)
  - Copy to content/en/es/votw/{slug}.md
  - Keep every ## heading below as written and in this order. Register and usage
    is optional and may be deleted.
  - Replace the H1 with the verb (same as title).
  - Add as many senses, expressions, and mistakes as the verb needs. Delete the
    spare blocks.
  - Every ## opens with a sentence before any ###. No stacked headings, and no
    filler sentence either: it has to say something.
  - Example pairs use | Spanish | English | tables, Spanish on the left.
  - Link CEFR level codes in body copy to /en/cefr/ (e.g. [A1](/en/cefr/)).
    Do not put Markdown links in YAML frontmatter.
  - Voice and pedagogy: see STYLE GUIDE comment above (English audience, not FR).
  - To generate a draft with an LLM: paste this whole file and complete the
    INPUT fields in the LLM PROMPT comment at the top of the file.
-->

# Verb

Introductory paragraphs (about 100-200 words). Why the verb is worth learning,
and the idea that ties its uses together. Do not list every translation.

## Forms and grammar

The mechanics a learner needs in order to build a correct sentence: stem
changes, an irregular preterite, the participle, reflexive forms, any
preposition habit. Keep to what the examples below actually rely on.

## How to use {verb}

Open with the principle that orders the senses below, so the reader knows what
separates them rather than meeting three headings cold.

### First sense, as a short descriptive heading

One line of guidance: what this use covers, or where Spanish parts company with
English.

| Spanish | English |
|---------|---------|
| | |
| | |

### Second sense

One line of guidance.

| Spanish | English |
|---------|---------|
| | |
| | |

### Third sense

One line of guidance.

| Spanish | English |
|---------|---------|
| | |
| | |

<!-- Where two verbs are both correct but say different things, put the
     comparison here, in the sense it belongs to, as a two-row table with a
     paragraph explaining the difference. It is not a mistake. -->

## Common constructions

One sentence introducing the combinations. Prefer collocations where Spanish and
English diverge over ones that translate predictably.

| Spanish | English |
|---------|---------|
| | |
| | |

A closing note on whichever row is least predictable for an English speaker.

## Expressions and idioms

One sentence on what sets these apart from the senses above.

### expresión española

Short gloss.

| Spanish | English |
|---------|---------|
| | |

### second expression

Short gloss.

| Spanish | English |
|---------|---------|
| | |

## Register and usage

OPTIONAL, and harder to write than it looks. Keep it only if there is something
concrete to say: a use that is formal, dated, regional, or that would sound
wrong in ordinary conversation. This is also where peninsular and Latin American
differences belong, when they bear on this verb. Delete the whole section if the
honest answer is that the verb is neutral everywhere.

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

-
-
-

A note on whichever one causes English speakers the most trouble.

## Summary

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
