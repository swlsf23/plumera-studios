<!--
LLM PROMPT — French Verb of the Week (for Spanish speakers)
===========================================================
You are drafting a Plumera Studios French Verb of the Week article for
Spanish-speaking learners. Fill this Markdown template. Do not invent a
different structure.

INPUT (filled by the human before or with this prompt)
- French verb / infinitive:
- CEFR level:
- Author:
- Date (YYYY-MM-DD):
- Any focus notes (optional):

OUTPUT RULES
1. Return a complete Markdown file ready to save as
   content/learn/fr/votw/{slug}.md
   (UI locale for URLs may change later; for now follow the path above unless
   the human gives a different path.)
2. Keep every ## heading exactly as written below and in this order.
   Do not rename, reorder, add, or remove top-level ## sections.
   Headings in this template are in Spanish and must stay in Spanish.
3. Set the H1 to the French verb lemma (same string as title in frontmatter).
4. Fill YAML frontmatter: title, description, slug, target, locale, level,
   author, date. Set target: fr and locale: es.
   Keep draft: true unless the human asks to publish.
5. slug must be a URL-safe form of the infinitive (e.g. prendre, not Prendre).
6. Write all learner-facing prose in Spanish. description and body must be
   Spanish. Do not write the article in English.
7. For example pairs, use Markdown tables with columns Francés | Español.
   Prefer 2–4 rows per table.
8. Under Significados, order senses from most literal to most idiomatic.
   Use only as many ### Significado N / Expresión N / Error N blocks as needed;
   delete unused numbered blocks.
9. Follow the STYLE GUIDE comment below (audience, voice, writing, examples,
   translation, pedagogy, L1 interference). This file is for Spanish-speaking
   learners only. Do not write for English speakers or mix audiences.
10. Write clear learner-facing prose. No meta commentary, no "as an AI",
    no placeholder text like "TODO" or "rellenar".
11. Before finishing, delete this LLM PROMPT comment, the STYLE GUIDE comment,
    the AUTHOR NOTES comment, and the SEO CHECKLIST comment from the output.
    The published file must start with the YAML frontmatter (---).
12. Do not wrap the answer in a code fence unless the human asks for one.

QUALITY BAR
- Introduction: ~100–200 words; why the verb matters; one central idea.
- Concepto central: semantic idea that links meanings — not a gloss list.
- Examples: natural, level-appropriate, accurate French with Spanish glosses.
- Errores comunes: typical for Spanish speakers learning French (see L1).
- Resumen: reinforce the core idea; do not restate every gloss.

Fill the template that follows (frontmatter, then body).
-->

<!--
STYLE GUIDE — French VOTW for Spanish speakers (fr-es)
=====================================================
Pair: target=fr, locale=es. Do not reuse English-audience guidance.

Audience
- Native Spanish speakers learning French.
- They may recognize Romance patterns, but do not assume advanced grammar study.
- Do not assume they know English. Never use English as a teaching bridge.

Voice
- Write learner-facing prose like a native Spanish speaker: natural idiom,
  rhythm, and word choice. Not translated-from-English, not textbook Spanish,
  not generic AI Spanish.
- Friendly. Confident. Curious. Teacher.
- Conversational but precise.
- Never patronizing.
- Prefer explanation over definition.
- Assume the reader is curious, not studying for an exam.
- Prefer "Fíjate que..." / "Observa que..." over "Recuerda que..."
- Prefer "El francés usa..." over "El francés es..."
- Do not exaggerate rules.
- Avoid "simplemente", "solo", "siempre", or "nunca" unless literally true.

Writing
- Use active voice.
- Prefer short paragraphs.
- Prefer plain language. Familiar school terms (subjuntivo, complemento, etc.)
  are fine when they help, but explain briefly if a term might be rusty.
- Introduce French terminology only when useful.
- Explain why something works, not just what it means.
- Avoid AI-slop tropes. No em dashes (—). Avoid semicolons. Do not use
  "esto no es X, es Y" / "no X sino Y" contrast formulas.

Examples
- Use natural, contemporary French.
- Avoid textbook-only examples where possible.
- Prefer examples someone might actually hear or say.

Translation
- Translate naturally into Spanish.
- Don't force word-for-word translations unless illustrating a point.

Pedagogy
- Build from concrete meanings to abstract or idiomatic ones.
- Highlight patterns rather than isolated facts.
- Compare with Spanish only when it aids understanding.
- Never use English (or another L3) as a bridge.
- Shared Romance roots can help, but call out when French diverges from Spanish.

L1 interference (Spanish → French)
- Anticipate falsos amigos when relevant to this verb.
- Watch gender and agreement habits carried from Spanish nouns/adjectives.
- Watch false confidence with subjunctive or tense mapping from Spanish.
- Address ser/estar habits that do not map cleanly onto French.
- In Errores comunes, focus on errors Spanish speakers typically make — not
  Anglophone transfer errors.
-->

---
title:          # Lema del verbo francés, p. ej. Prendre
description:    # Meta descripción en una frase (español)
slug:           # Debe coincidir con el nombre del archivo, p. ej. prendre
target: fr      # Idioma que se enseña
locale: es      # Idioma de la explicación (audiencia)
level:          # MCER: A1 | A2 | B1 | B2 | C1 | C2
author:
date:           # AAAA-MM-DD
draft: true
---

<!--
  AUTHOR NOTES (delete this comment block before publishing)

  - Template: French VOTW for Spanish speakers (fr-es)
  - Copy to content/learn/fr/votw/{slug}.md (path may gain a locale segment later)
  - Keep every ## heading below exactly as written and in this order.
  - Replace the H1 with the verb (same as title).
  - Fill sections; remove unused Significado / Expresión / Error blocks.
  - Do not rename headings — this Spanish series depends on them.
  - Example pairs use | Francés | Español | tables.
  - Voice and pedagogy: see STYLE GUIDE comment above (Spanish audience, not EN).
  - To generate a draft with an LLM: paste this whole file and complete the
    INPUT fields in the LLM PROMPT comment at the top of the file.
-->

# Verbo

Párrafos introductorios (unas 100–200 palabras). Por qué vale la pena aprender
este verbo. Presenta la idea central sin enumerar todas las traducciones.

## De un vistazo

| Elemento | Valor |
|----------|-------|
| Infinitivo | |
| Pronunciación | |
| MCER | |
| Auxiliar | |
| Participio pasado | |
| Significado central | |

## Concepto central

Explica la idea semántica que une los significados del verbo. Prefiere el
concepto compartido a una lista de glosas.

## Significados

<!-- Repite ### Significado N para cada acepción importante, de lo más literal a lo más idiomático. -->

### Significado 1

**Definición**

**Ejemplos**

| Francés | Español |
|---------|---------|
| | |
| | |

**Notas de uso**

### Significado 2

**Definición**

**Ejemplos**

| Francés | Español |
|---------|---------|
| | |
| | |

**Notas de uso**

### Significado 3

**Definición**

**Ejemplos**

| Francés | Español |
|---------|---------|
| | |
| | |

**Notas de uso**

## Construcciones comunes

Patrones gramaticales frecuentes, por ejemplo:

- verbo + sustantivo
- verbo + infinitivo
- verbo + de + infinitivo
- verbo + à + infinitivo
- formas pronominales

Cuando una construcción necesite un ejemplo, usa una tabla:

| Francés | Español |
|---------|---------|
| | |

## Expresiones e idiotismos

<!-- Repite ### Expresión N. Prefiere explicar el sentido a traducir literalmente. -->

### Expresión 1

**Significado**

**Ejemplo**

| Francés | Español |
|---------|---------|
| | |

### Expresión 2

**Significado**

**Ejemplo**

| Francés | Español |
|---------|---------|
| | |

## Registro y uso

Indica si los usos son formales, informales, literarios, conversacionales,
regionales o anticuados.

## Errores comunes

<!-- Errores típicos de hispanohablantes que aprenden francés. -->

### Error 1

| Incorrecto | Correcto |
|------------|----------|
| | |

**Explicación**

### Error 2

| Incorrecto | Correcto |
|------------|----------|
| | |

**Explicación**

## Verbos relacionados

Verbos que los estudiantes confunden con este, o que comparten significados
parecidos:

-
-
-

## Resumen

Cierre breve de la idea central del verbo. Refuerza el concepto semántico;
no repitas todas las glosas.

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
