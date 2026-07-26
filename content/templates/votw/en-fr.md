<!--
LLM PROMPT: English Verb of the Week (for French speakers)
=========================================================
You are drafting a Plumera Studios English Verb of the Week article for
French-speaking learners. Fill this Markdown template. Do not invent a
different structure.

INPUT (filled by the human before or with this prompt)
- English verb / infinitive:
- CEFR level:
- Author:
- Date (YYYY-MM-DD):
- Any focus notes (optional):

OUTPUT RULES
1. Return a complete Markdown file ready to save as
   content/fr/en/votw/{slug}.md
2. Keep every ## heading exactly as written below and in this order.
   Do not rename, reorder, or add top-level ## sections. Registre et usage is
   the one optional section and may be deleted (see its note).
   Headings in this template are in French and must stay in French.
3. Set the H1 to the English verb (same string as title in frontmatter), in the
   form "To take".
4. Fill YAML frontmatter: title, description, slug, target, locale, level,
   author, date. Set target: en and locale: fr.
   Keep draft: true unless the human asks to publish.
5. slug must be a URL-safe form of the verb, with the level as a suffix
   (e.g. votw-take-a2). frontmatter level is the source of truth. The suffix only
   keeps two articles about the same verb apart (take-a2, take-b2).
6. Write all learner-facing prose in French. description and body must be
   French. Do not write the article in English.
7. Address the reader as vous, matching the other French-locale pages.
8. For example pairs, use Markdown tables with columns Anglais | Français.
   The language being taught goes in the left column. Prefer 2–4 rows.
9. Order the senses under Comment utiliser by a principle you state in that
   section's opening line, so the reader knows what separates them.
10. Every ## section opens with at least one sentence before any ### heading.
    Two headings must never sit next to each other with nothing in between, and
    that sentence must carry information rather than announce the section.
11. Do not use bold labels (**Définition**, **Exemples**, **Notes d'usage**,
    **Sens**, **Explication**). The heading names the item, the prose explains
    it, the table shows it.
12. Each sense is a heading, one line of guidance, then a table. Nothing else.
13. Under Erreurs fréquentes, the explanation goes before the table.
14. Use Incorrect / Correct only for genuine errors. A sentence that is
    grammatical but says something the learner did not intend still counts, so
    faux amis belong here. If both versions are correct and simply mean
    different things, that is a contrast, not a mistake: put it in the relevant
    sense as a two-row comparison instead.
15. Do not point forward at items the reader has not reached. "Ces deux" and
    "les deux premières" need an antecedent, as in "deux des erreurs ci-dessous".
16. Do not state a rule in Formes et grammaire that Erreurs fréquentes also
    covers.
17. Sentence case for all headings. A heading that is an English expression keeps
    its own capitalization.
18. Follow the STYLE GUIDE comment below (audience, voice, writing, examples,
    translation, pedagogy, L1 interference). This file is for French-speaking
    learners only. Do not write for Spanish speakers or mix audiences.
19. Write clear learner-facing prose. No meta commentary, no "as an AI",
    no placeholder text like "TODO" or "à compléter".
20. Before finishing, delete this LLM PROMPT comment, the STYLE GUIDE comment,
    the AUTHOR NOTES comment, and the SEO CHECKLIST comment from the output.
    The published file must start with the YAML frontmatter (---).
21. Do not wrap the answer in a code fence unless the human asks for one.

QUALITY BAR
- Introduction: about 100 to 200 words, why the verb matters, and the central
  idea that ties its uses together.
- Formes et grammaire: only the mechanics the examples below rely on, including
  the preterite and past participle for irregular verbs.
- Examples: natural, level-appropriate, accurate English with French glosses.
- Erreurs fréquentes: typical for French speakers learning English (see L1).
- Résumé: reinforce the core idea without restating every gloss.

Fill the template that follows (frontmatter, then body).
-->

<!--
STYLE GUIDE: English VOTW for French speakers (en-fr)
====================================================
Pair: target=en, locale=fr. Do not reuse English-audience or Spanish-audience
guidance.

Audience
- Native French speakers learning English.
- Explain concepts without assuming advanced grammar study.
- Do not assume they know Spanish or any other third language.

Voice
- Write learner-facing prose like a native French speaker: natural idiom,
  rhythm, and word choice. Not translated-from-English, not textbook French,
  not generic AI French.
- Friendly. Confident. Curious. Teacher.
- Conversational but precise.
- Never patronizing.
- Address the reader as vous throughout the prose. Example sentences may use tu
  where that is what a French speaker would actually say.
- Prefer explanation over definition.
- Assume the reader is curious, not studying for an exam.
- Prefer "Remarquez que..." over "N'oubliez pas que..."
- Prefer "L'anglais utilise..." over "L'anglais est..."
- Do not exaggerate rules.
- Avoid "simplement", "juste", "toujours", or "jamais" unless literally true.
- Use typographic apostrophes ('), and the space French requires before a colon,
  question mark, or exclamation mark.
- Avoid AI-slop tropes. No em dashes. No semicolons.

Writing
- Use active voice.
- Prefer short paragraphs.
- Familiar school terms (prétérit, participe passé, complément) are fine when
  they help. Explain an English grammar term the first time it appears.
- Explain why something works, not just what it means.
- Avoid AI-slop tropes. Do not use "ce n'est pas X, c'est Y" contrast formulas.

Examples
- Use natural, contemporary English.
- Avoid textbook-only examples where possible.
- Prefer examples someone might actually hear or say.
- When British and American usage differ, say so instead of presenting one as
  correct.

Translation
- Translate naturally into French.
- Don't force word-for-word translations unless illustrating a point.

Pedagogy
- Build from concrete meanings to abstract or idiomatic ones.
- Highlight patterns rather than isolated facts.
- Where English collapses a distinction French makes, or splits one French
  merges, say so plainly. That asymmetry is usually the most useful thing in
  the article.
- Never use Spanish (or another L3) as a bridge.
- Phrasal verbs have no French counterpart to hang them on. Scope them out of
  A1 and A2 articles rather than covering four of twenty.

L1 interference (French → English)
- Anticipate calques from French, especially verb + noun collocations where
  English prefers have, make, or catch.
- Watch the present: French has one present tense, English chooses between the
  simple and the continuous.
- Watch the past: j'ai fait resembles the present perfect, so a named past time
  (yesterday, last week) draws the wrong tense.
- Address faux amis when relevant to this verb.
- In Erreurs fréquentes, focus on errors French speakers typically make, not
  Hispanophone transfer errors.
-->

---
title:          # Verbe anglais, p. ex. To take
description:    # Méta-description en une phrase (français)
slug:           # votw-{verbe}-{niveau}, p. ex. votw-take-a2
target: en      # Langue enseignée
locale: fr      # Langue de l'explication (audience)
level:          # CECR : A1 | A2 | B1 | B2 | C1 | C2, ou une plage comme A1, A2
author:
date:           # AAAA-MM-JJ
draft: true
---

<!--
  AUTHOR NOTES (delete this comment block before publishing)

  - Template: English VOTW for French speakers (en-fr)
  - Copy to content/fr/en/votw/{slug}.md
  - Keep every ## heading below as written and in this order. Registre et usage
    is optional and may be deleted.
  - Replace the H1 with the verb (same as title).
  - Add as many senses, expressions, and mistakes as the verb needs. Delete the
    spare blocks.
  - Every ## opens with a sentence before any ###. No stacked headings, and no
    filler sentence either: it has to say something.
  - Example pairs use | Anglais | Français | tables, English on the left.
  - Link CECR level codes in body copy to /fr/cefr/ (e.g. [A1](/fr/cefr/)).
    Do not put Markdown links in YAML frontmatter.
  - Voice and pedagogy: see STYLE GUIDE comment above (French audience).
  - To generate a draft with an LLM: paste this whole file and complete the
    INPUT fields in the LLM PROMPT comment at the top of the file.
-->

# To verb

Paragraphes d'introduction (environ 100 à 200 mots). Pourquoi ce verbe vaut la
peine, et l'idée qui relie ses emplois. N'énumérez pas toutes les traductions.
Si l'anglais et le français découpent le sens différemment, annoncez-le ici.

## Formes et grammaire

La mécanique nécessaire pour construire une phrase correcte : formes
irrégulières, prétérit et participe passé, particularités de conjugaison,
présent simple contre présent continu si le verbe s'y prête. Limitez-vous à ce
que les exemples ci-dessous utilisent vraiment.

## Comment utiliser {verbe}

Commencez par le critère qui ordonne les emplois ci-dessous, pour que le lecteur
sache ce qui les distingue avant de tomber sur trois titres à la suite.

### Premier emploi, avec un titre court et descriptif

Une ligne d'orientation : ce que couvre cet emploi, ou là où l'anglais s'écarte
du français.

| Anglais | Français |
|---------|----------|
| | |
| | |

### Deuxième emploi

Une ligne d'orientation.

| Anglais | Français |
|---------|----------|
| | |
| | |

### Troisième emploi

Une ligne d'orientation.

| Anglais | Français |
|---------|----------|
| | |
| | |

<!-- Quand deux verbes sont corrects mais ne disent pas la même chose, mettez la
     comparaison ici, dans l'emploi concerné, avec un tableau de deux lignes et
     un paragraphe qui explique la différence. Ce n'est pas une erreur. -->

## Constructions courantes

Une phrase pour présenter les combinaisons. Préférez les collocations où
l'anglais et le français divergent à celles qui se traduisent sans surprise.

| Anglais | Français |
|---------|----------|
| | |
| | |

Un mot de conclusion sur la ligne la moins prévisible pour un francophone.

## Expressions et idiomes

Une phrase sur ce qui sépare ces tournures des emplois ci-dessus.

### english expression

Glose brève.

| Anglais | Français |
|---------|----------|
| | |

### deuxième expression

Glose brève.

| Anglais | Français |
|---------|----------|
| | |

## Registre et usage

FACULTATIF, et plus difficile à écrire qu'il n'y paraît. À garder seulement s'il
y a quelque chose de concret à dire : un emploi formel, vieilli, régional, ou qui
sonnerait faux dans une conversation ordinaire. Supprimez toute la section si la
réponse honnête est que le verbe est neutre partout. Ne la remplissez pas pour
la remplir.

## Erreurs fréquentes

Une phrase qui caractérise les erreurs ci-dessous et ce qu'elles ont en commun,
pour que « la première » et « l'autre » aient un antécédent.

### Première erreur, avec un titre court et descriptif

L'explication, avant le tableau, pour que le lecteur sache quoi regarder.

| Incorrect | Correct |
|-----------|---------|
| | |

### Deuxième erreur

L'explication.

| Incorrect | Correct |
|-----------|---------|
| | |

## Verbes voisins

Les verbes que les apprenants confondent avec celui-ci, ou qui couvrent une
partie de son terrain, chacun avec une glose brève :

-
-
-

Un mot sur celui qui pose le plus de problèmes aux francophones.

## Résumé

Une ou deux phrases qui renforcent l'idée centrale, avec le niveau en lien
(p. ex. [A1](/fr/cefr/)). Ne reprenez pas les gloses.

<!--
  SEO CHECKLIST (delete before publishing)

  - Mot-clé principal :
  - Mots-clés secondaires :
  - Titre de page suggéré :
  - Méta-description suggérée :
  - URL suggérée :
  - Texte alternatif d'image :
  - Occasions de FAQ (schema) :
  - Liens internes ajoutés :
  - Références externes vérifiées :
-->
