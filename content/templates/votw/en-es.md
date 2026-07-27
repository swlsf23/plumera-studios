<!--
LLM PROMPT: English Verb of the Week (for Spanish speakers)
==========================================================
You are drafting a Plumera Studios English Verb of the Week article for
Spanish-speaking learners. Fill this Markdown template. Do not invent a
different structure.

INPUT (filled by the human before or with this prompt)
- English verb / infinitive:
- CEFR level:
- Author:
- Date (YYYY-MM-DD):
- Any focus notes (optional):

OUTPUT RULES
1. Return a complete Markdown file ready to save as
   content/es/en/votw/{slug}.md
2. Keep every ## heading exactly as written below and in this order.
   Do not rename, reorder, or add top-level ## sections. Registro y uso is the
   one optional section and may be deleted (see its note).
   Headings in this template are in Spanish and must stay in Spanish.
3. Set the H1 to the English verb only, in the form "To take".
4. Fill YAML frontmatter: title, description, slug, target, locale, level,
   author, date. Set target: en and locale: es.
   title is the full document <title>, not just the verb:
   "Verbo inglés de la semana: To take". The builder uses it as-is.
   Keep draft: true unless the human asks to publish.
5. slug must be a URL-safe form of the verb, with the level as a suffix
   (e.g. votw-take-a2). frontmatter level is the source of truth. The suffix only
   keeps two articles about the same verb apart (take-a2, take-b2).
6. Write all learner-facing prose in Spanish. description and body must be
   Spanish. Do not write the article in English.
7. For example pairs, use Markdown tables with columns Inglés | Español.
   The language being taught goes in the left column. Prefer 2–4 rows.
8. Order the senses under Cómo se usa by a principle you state in that section's
   opening line, so the reader knows what separates them.
9. Every ## section opens with at least one sentence before any ### heading.
   Two headings must never sit next to each other with nothing in between, and
   that sentence must carry information rather than announce the section.
10. Do not use bold labels (**Definición**, **Ejemplos**, **Notas de uso**,
    **Significado**, **Explicación**). The heading names the item, the prose
    explains it, the table shows it.
11. Each sense is a heading, one line of guidance, then a table. Nothing else.
12. Under Errores comunes, the explanation goes before the table.
13. Use Incorrecto / Correcto only for genuine errors. A sentence that is
    grammatical but says something the learner did not intend still counts, so
    falsos amigos belong here. If both versions are correct and simply mean
    different things, that is a contrast, not a mistake: put it in the relevant
    sense as a two-row comparison instead.
14. Do not point forward at items the reader has not reached. "Estos dos" and
    "los dos primeros" need an antecedent, as in "dos de los errores siguientes".
15. Do not state a rule in Formas y gramática that Errores comunes also covers.
16. Sentence case for all headings. A heading that is an English expression keeps
    its own capitalization.
17. Follow the STYLE GUIDE comment below (audience, voice, writing, examples,
    translation, pedagogy, L1 interference). This file is for Spanish-speaking
    learners only. Do not write for French speakers or mix audiences.
18. Write clear learner-facing prose. No meta commentary, no "as an AI",
    no placeholder text like "TODO" or "rellenar".
19. Before finishing, delete this LLM PROMPT comment, the STYLE GUIDE comment,
    the AUTHOR NOTES comment, and the SEO CHECKLIST comment from the output.
    The published file must start with the YAML frontmatter (---).
20. Do not wrap the answer in a code fence unless the human asks for one.

QUALITY BAR
- Introduction: about 100 to 200 words, why the verb matters, and the central
  idea that ties its uses together.
- Formas y gramática: only the mechanics the examples below rely on, including
  the preterite and past participle for irregular verbs.
- Examples: natural, level-appropriate, accurate English with Spanish glosses.
- Errores comunes: typical for Spanish speakers learning English (see L1).
- Resumen: reinforce the core idea without restating every gloss.

Fill the template that follows (frontmatter, then body).
-->

<!--
STYLE GUIDE: English VOTW for Spanish speakers (en-es)
=====================================================
Pair: target=en, locale=es. Do not reuse English-audience or French-audience
guidance.

Audience
- Native Spanish speakers learning English.
- Explain concepts without assuming advanced grammar study.
- Do not assume they know French or any other third language.

Voice
- Write learner-facing prose like a native Spanish speaker: natural idiom,
  rhythm, and word choice. Not translated-from-English, not textbook Spanish,
  not generic AI Spanish.
- Friendly. Confident. Curious. Teacher.
- Conversational but precise.
- Never patronizing.
- Address the reader as tú.
- Prefer explanation over definition.
- Assume the reader is curious, not studying for an exam.
- Prefer "Fíjate que..." / "Observa que..." over "Recuerda que..."
- Prefer "El inglés usa..." over "El inglés es..."
- Do not exaggerate rules.
- Avoid "simplemente", "solo", "siempre", or "nunca" unless literally true.

Writing
- Use active voice.
- Prefer short paragraphs.
- Familiar school terms (sujeto, complemento, participio) are fine when they
  help. Explain an English grammar term the first time it appears.
- Explain why something works, not just what it means.
- Avoid AI-slop tropes. No em dashes. No semicolons. Do not use
  "esto no es X, es Y" / "no X sino Y" contrast formulas.

Examples
- Use natural, contemporary English.
- Avoid textbook-only examples where possible.
- Prefer examples someone might actually hear or say.
- When British and American usage differ, say so instead of presenting one as
  correct.

Translation
- Translate naturally into Spanish.
- Don't force word-for-word translations unless illustrating a point.
- Neutral Latin American Spanish unless the human asks otherwise.

Pedagogy
- Build from concrete meanings to abstract or idiomatic ones.
- Highlight patterns rather than isolated facts.
- Where English collapses a distinction Spanish makes, or splits one Spanish
  merges, say so plainly. That asymmetry is usually the most useful thing in
  the article.
- Never use French (or another L3) as a bridge.
- Phrasal verbs have no Spanish counterpart to hang them on. Scope them out of
  A1 and A2 articles rather than covering four of twenty.

L1 interference (Spanish → English)
- Anticipate calques from Spanish, especially verb + noun collocations where
  English prefers have, make, or take.
- Watch tener where English needs be: age, hunger, cold, fear.
- Watch the present: Spanish uses the simple present for what is happening now,
  English usually needs the continuous.
- Watch the past: he hecho resembles the present perfect, so a named past time
  (yesterday, last week) draws the wrong tense.
- Watch subject pronouns, which Spanish drops and English requires.
- Address falsos amigos when relevant to this verb.
- In Errores comunes, focus on errors Spanish speakers typically make, not
  francophone transfer errors.
-->

---
title:          # <title> completo, p. ej. "Verbo inglés de la semana: To take"
description:    # Meta descripción en una frase (español)
slug:           # votw-{verbo}-{nivel}, p. ej. votw-take-a2
target: en      # Idioma que se enseña
locale: es      # Idioma de la explicación (audiencia)
level:          # MCER: A1 | A2 | B1 | B2 | C1 | C2, o un rango como A1, A2
author:
date:           # AAAA-MM-DD
draft: true
related:        # Tarjetas "También te puede interesar" (opcional)
  - title:      # Título de la tarjeta
    meta:       # Subtítulo opcional (p. ej. fecha)
    href:       # Ruta del sitio, p. ej. /es/en/votw/
---

<!--
  AUTHOR NOTES (delete this comment block before publishing)

  - Template: English VOTW for Spanish speakers (en-es)
  - Copy to content/es/en/votw/{slug}.md
  - Keep every ## heading below as written and in this order. Registro y uso is
    optional and may be deleted.
  - Replace the H1 with the verb (same as title).
  - Add as many senses, expressions, and mistakes as the verb needs. Delete the
    spare blocks.
  - Every ## opens with a sentence before any ###. No stacked headings, and no
    filler sentence either: it has to say something.
  - Example pairs use | Inglés | Español | tables, English on the left.
  - Link MCER level codes in body copy to /es/cefr/ (e.g. [A1](/es/cefr/)).
    Do not put Markdown links in YAML frontmatter.
  - Voice and pedagogy: see STYLE GUIDE comment above (Spanish audience).
  - To generate a draft with an LLM: paste this whole file and complete the
    INPUT fields in the LLM PROMPT comment at the top of the file.
-->

# To verb

Párrafos introductorios (unas 100–200 palabras). Por qué vale la pena aprender
este verbo y cuál es la idea que une sus usos. No enumeres todas las
traducciones. Si el inglés y el español reparten el sentido de otra manera,
anúncialo aquí.

## Formas y gramática

La mecánica que hace falta para construir una frase correcta: formas
irregulares, pasado y participio, presente simple frente a presente continuo si
el verbo lo pide. Limítate a lo que usan los ejemplos de abajo.

## Cómo se usa {verbo}

Empieza con el criterio que ordena los usos siguientes, para que el lector sepa
qué los distingue antes de encontrarse con tres títulos seguidos.

### Primer uso, con un título breve y descriptivo

Una línea de orientación: qué cubre este uso, o dónde el inglés se separa del
español.

| Inglés | Español |
|--------|---------|
| | |
| | |

### Segundo uso

Una línea de orientación.

| Inglés | Español |
|--------|---------|
| | |
| | |

### Tercer uso

Una línea de orientación.

| Inglés | Español |
|--------|---------|
| | |
| | |

<!-- Cuando dos verbos son correctos pero dicen cosas distintas, pon la
     comparación aquí, en el uso al que pertenece, con una tabla de dos filas y
     un párrafo que explique la diferencia. No es un error. -->

## Construcciones comunes

Una frase que presente las combinaciones. Prefiere las colocaciones donde el
inglés y el español divergen antes que las que se traducen sin sorpresa.

| Inglés | Español |
|--------|---------|
| | |
| | |

Un comentario final sobre la fila menos previsible para un hispanohablante.

## Expresiones e idiotismos

Una frase sobre qué separa estas expresiones de los usos anteriores.

### english expression

Glosa breve.

| Inglés | Español |
|--------|---------|
| | |

### segunda expresión

Glosa breve.

| Inglés | Español |
|--------|---------|
| | |

## Registro y uso

OPCIONAL, y más difícil de escribir de lo que parece. Consérvalo solo si hay algo
concreto que decir: un uso formal, anticuado, regional, o que sonaría raro en una
conversación normal. Borra la sección entera si la respuesta honesta es que el
verbo es neutro en todas partes. No la rellenes.

## Errores comunes

Una frase que caracterice los errores siguientes y lo que tienen en común, para
que "el primero" y "el otro" tengan a qué referirse.

### Primer error, con un título breve y descriptivo

La explicación, antes de la tabla, para que el lector sepa qué mirar.

| Incorrecto | Correcto |
|------------|----------|
| | |

### Segundo error

La explicación.

| Incorrecto | Correcto |
|------------|----------|
| | |

## Verbos relacionados

Verbos que los estudiantes confunden con este, o que cubren parte de su terreno,
cada uno con una glosa breve:

-
-
-

Un comentario sobre el que más problemas causa a los hispanohablantes.

## Resumen

Una o dos frases que refuercen la idea central, con el nivel enlazado
(p. ej. [A1](/es/cefr/)). No repitas las glosas.

<!--
  SEO CHECKLIST (delete before publishing)

  - Palabra clave principal:
  - Palabras clave secundarias:
  - Título de página sugerido:
  - Meta descripción sugerida:
  - URL sugerida:
  - Texto alt de imagen:
  - Oportunidades de FAQ (schema):
  - Enlaces internos añadidos:
  - Referencias externas comprobadas:
-->
