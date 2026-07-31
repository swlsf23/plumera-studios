export type CardType = 'conjugation' | 'expression';

/** Flip cycle is prompt ↔ answer only. Example is E, not part of the cycle. */
export type CardFace = 'prompt' | 'answer' | 'example';

/** Which language is shown first for the current card. */
export type StudyDirection = 'en-fr' | 'fr-en';

/**
 * In-loop study configuration (kept in sessionStorage for the tab).
 * - en-fr / fr-en: fixed direction
 * - mixed: each card picks a direction (stable while browsing)
 * - both: pass 1 EN→FR, then pass 2 FR→EN
 */
export type StudyMode = 'en-fr' | 'fr-en' | 'mixed' | 'both';

export type CardLang = 'en' | 'fr';

export interface RelatedLink {
  href: string;
  title: string;
  meta?: string;
}

export interface Flashcard {
  id: string;
  type: CardType;
  /** Short label (e.g. subject pronoun); optional metadata. */
  subject?: string;
  en: string;
  fr: string;
  example?: string;
  exampleTranslation?: string;
  /** Path relative to `data/{locale}/{target}/` (e.g. `prendre/prendre_je_prends.mp3`). */
  audio?: string;
}

export interface Deck {
  verb: string;
  gloss: string;
  level: string;
  locale?: string;
  target?: string;
  lessonHref: string;
  /** Short intro for the list being studied (not lesson/series chrome). */
  description?: string;
  related?: RelatedLink[];
  cards: Flashcard[];
}

export function promptLang(direction: StudyDirection): CardLang {
  return direction === 'en-fr' ? 'en' : 'fr';
}

export function answerLang(direction: StudyDirection): CardLang {
  return direction === 'en-fr' ? 'fr' : 'en';
}

export function textForLang(card: Flashcard, lang: CardLang): string {
  return lang === 'en' ? card.en : card.fr;
}
