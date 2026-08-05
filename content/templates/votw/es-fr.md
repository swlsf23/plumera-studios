<!--
LLM PROMPT: Spanish Verb of the Week (for French speakers)
=========================================================
You are drafting a Plumera Studios Spanish Verb of the Week article for
French-speaking learners. Fill this Markdown template. Do not invent a
different structure.

INPUT (filled by the human before or with this prompt)
- Spanish verb / infinitive:
- CEFR level:
- Author:
- Date (YYYY-MM-DD):
- Any focus notes (optional):

OUTPUT RULES
1. Return a complete Markdown file ready to save as
   content/fr/apprendre-espagnol/votw/{slug}.md
2. Keep every ## heading exactly as written below and in this order.
   Do not rename, reorder, or add top-level ## sections. Registre et usage is
   the one optional section and may be deleted (see its note).
   Headings in this template are in French and must stay in French.
3. Set the H1 to the Spanish verb lemma only (e.g. Tomar).
4. Fill YAML frontmatter: title, description, slug, target, locale, level,
   author, date. Set target: apprendre-espagnol and locale: fr.
   title is the full document <title>, not just the verb:
   "Verbe espagnol de la semaine : Tomar". The builder uses it as-is.
   Keep draft: true unless the human asks to publish.
5. slug must be a URL-safe form of the infinitive, with the level as a suffix
   (e.g. votw-tomar-a1). frontmatter level is the source of truth. The suffix
   only keeps two articles about the same verb apart (tomar-a1, tomar-b2).
6. Write all learner-facing prose in French. description and body must be
   French. Do not write the article in Spanish or English.
7. Address the reader as vous, matching the other French-locale pages.
8. For example pairs, use Markdown tables with columns Espagnol | Français.
   The language being taught goes in the left column. Prefer 2-4 rows.
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
17. Sentence case for all headings. A heading that is a Spanish expression keeps
    its own capitalization.
18. Follow the STYLE GUIDE comment below (audience, voice, writing, examples,
    translation, pedagogy, L1 interference). This file is for French-speaking
    learners only. Do not write for English speakers or mix audiences.
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
  stem changes and any irregular preterite.
- Examples: natural, level-appropriate, accurate Spanish with French glosses.
- Erreurs fréquentes: typical for French speakers learning Spanish (see L1).
- Résumé: reinforce the core idea without restating every gloss.

Fill the template that follows (frontmatter, then body).
-->

<!--
STYLE GUIDE: Spanish VOTW for French speakers (es-fr)
====================================================
Pair: target=es, locale=fr. Do not reuse English-audience or Spanish-audience
guidance.

Audience
- Native French speakers learning Spanish.
- They will recognize Romance patterns, which helps and misleads in equal
  measure. Do not assume advanced grammar study.
- Do not assume they know English. Never use English as a teaching bridge.

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
- Prefer "L'espagnol utilise..." over "L'espagnol est..."
- Do not exaggerate rules.
- Avoid "simplement", "juste", "toujours", or "jamais" unless literally true.
- Use typographic apostrophes ('), and the space French requires before a colon,
  question mark, or exclamation mark.
- Avoid AI-slop tropes. No em dashes. No semicolons.

Writing
- Use active voice.
- Prefer short paragraphs.
- Familiar school terms (subjonctif, prétérit, complément) are fine when they
  help, but a French term and its Spanish counterpart do not always cover the
  same ground. Say when they diverge.
- Explain why something works, not just what it means.
- Avoid AI-slop tropes. Do not use "ce n'est pas X, c'est Y" contrast formulas.

Examples
- Use natural, contemporary Spanish.
- Avoid textbook-only examples where possible.
- Prefer examples someone might actually hear or say.
- Where peninsular and Latin American usage differ, say so instead of presenting
  one as correct. Note vosotros and ustedes when the verb's forms make it
  relevant.

Translation
- Translate naturally into French.
- Don't force word-for-word translations unless illustrating a point.

Pedagogy
- Build from concrete meanings to abstract or idiomatic ones.
- Highlight patterns rather than isolated facts.
- Shared Romance roots are a real advantage here, so spend the space on where
  Spanish diverges from French rather than on where it agrees.
- Never use English (or another L3) as a bridge.

L1 interference (French → Spanish)
- Anticipate faux amis, which are dense between these two languages.
- Watch ser and estar, which French covers with être alone.
- Watch the past: the Spanish pretérito and imperfecto split what French often
  handles with the passé composé and imparfait, but not along the same line.
- Watch the subjunctive, which survives in ordinary Spanish where French has
  retreated to fixed phrases.
- Watch gustar-type verbs, where the thing liked is the subject.
- Watch por and para against pour, and the personal a, which French has no
  equivalent for.
- In Erreurs fréquentes, focus on errors French speakers typically make, not
  Anglophone transfer errors.
-->

---
title:          # <title> complet, p. ex. "Verbe espagnol de la semaine : Tomar | Plumera"
description:    # Méta-description en une phrase (français)
slug:           # votw-{verbe}-{niveau}, p. ex. votw-tomar-a1
target: apprendre-espagnol      # Langue enseignée
locale: fr      # Langue de l'explication (audience)
level:          # CECR : A1 | A2 | B1 | B2 | C1 | C2, ou une plage comme A1, A2
type: verb      # verb | grammar | conjugation | vocabulary | pronunciation | guide (list ok)
author:
date:           # AAAA-MM-JJ
draft: true
related:        # Cartes « Vous aimerez aussi » (optionnel)
  - href:       # Chemin du site, p. ex. /fr/apprendre-espagnol/votw/
    title:      # Remplacement optionnel. Omettre pour utiliser le H1 de la page cible
    meta:       # Sous-titre optionnel (p. ex. date)
---

<!--
  AUTHOR NOTES (delete this comment block before publishing)

  - Template: Spanish VOTW for French speakers (es-fr)
  - Copy to content/fr/apprendre-espagnol/votw/{slug}.md
  - Keep every ## heading below as written and in this order. Registre et usage
    is optional and may be deleted.
  - Replace the H1 with the verb (same as title).
  - Add as many senses, expressions, and mistakes as the verb needs. Delete the
    spare blocks.
  - Every ## opens with a sentence before any ###. No stacked headings, and no
    filler sentence either: it has to say something.
  - Example pairs use | Espagnol | Français | tables, Spanish on the left.
  - Link CECR level codes in body copy to /fr/cefr/ (e.g. [A1](/fr/cefr/)).
    Do not put Markdown links in YAML frontmatter.
  - Voice and pedagogy: see STYLE GUIDE comment above (French audience).
  - To generate a draft with an LLM: paste this whole file and complete the
    INPUT fields in the LLM PROMPT comment at the top of the file.
-->

# Verbe

Paragraphes d'introduction (environ 100 à 200 mots). Pourquoi ce verbe vaut la
peine, et l'idée qui relie ses emplois. N'énumérez pas toutes les traductions.
La proximité avec le français est une aide et un piège : dites lequel des deux
domine pour ce verbe.

## Formes et grammaire

La mécanique nécessaire pour construire une phrase correcte : diphtongaison et
changements de radical, prétérit irrégulier, participe passé, pronominalisation.
Limitez-vous à ce que les exemples ci-dessous utilisent vraiment.

## Comment utiliser {verbe}

Commencez par le critère qui ordonne les emplois ci-dessous, pour que le lecteur
sache ce qui les distingue avant de tomber sur trois titres à la suite.

### Premier emploi, avec un titre court et descriptif

Une ligne d'orientation : ce que couvre cet emploi, ou là où l'espagnol s'écarte
du français.

| Espagnol | Français |
|----------|----------|
| | |
| | |

### Deuxième emploi

Une ligne d'orientation.

| Espagnol | Français |
|----------|----------|
| | |
| | |

### Troisième emploi

Une ligne d'orientation.

| Espagnol | Français |
|----------|----------|
| | |
| | |

<!-- Quand deux verbes sont corrects mais ne disent pas la même chose, mettez la
     comparaison ici, dans l'emploi concerné, avec un tableau de deux lignes et
     un paragraphe qui explique la différence. Ce n'est pas une erreur. -->

## Constructions courantes

Une phrase pour présenter les combinaisons. Préférez les collocations où
l'espagnol et le français divergent à celles qui se traduisent sans surprise.

| Espagnol | Français |
|----------|----------|
| | |
| | |

Un mot de conclusion sur la ligne la moins prévisible pour un francophone.

## Expressions et idiomes

Une phrase sur ce qui sépare ces tournures des emplois ci-dessus.

### expresión española

Glose brève.

| Espagnol | Français |
|----------|----------|
| | |

### deuxième expression

Glose brève.

| Espagnol | Français |
|----------|----------|
| | |

## Registre et usage

FACULTATIF, et plus difficile à écrire qu'il n'y paraît. À garder seulement s'il
y a quelque chose de concret à dire : un emploi formel, vieilli, propre à une
région, ou qui sonnerait faux dans une conversation ordinaire. C'est aussi ici
que se règlent les écarts entre l'Espagne et l'Amérique latine, quand ils portent
sur ce verbe. Supprimez toute la section si la réponse honnête est que le verbe
est neutre partout.

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
