export type CardType = 'conjugation' | 'expression';

export type CardFace = 'prompt' | 'answer';

export type Grade = 'know' | 'dontKnow';

export interface Flashcard {
  id: string;
  type: CardType;
  /** Short label above the prompt (e.g. subject pronoun). */
  subject?: string;
  prompt: string;
  answer: string;
  example?: string;
  translation?: string;
}

export interface Deck {
  verb: string;
  gloss: string;
  level: string;
  lessonHref: string;
  cards: Flashcard[];
}
