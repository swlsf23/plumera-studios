import type { Deck } from './types';

/** Hand sample for /app/flashcard/tenir until data/ TSVs are wired. */
export const tenirDeck: Deck = {
  verb: 'tenir',
  gloss: 'to hold, to keep',
  level: 'A1',
  lessonHref: '/en/learn-french/votw/votw-tenir-a1/',
  cards: [
    {
      id: 'tenir-je',
      type: 'conjugation',
      subject: 'je',
      prompt: 'How do you conjugate tenir for “je”?',
      answer: 'tiens',
      example: 'Je tiens le livre dans ma main.',
      translation: 'I hold the book in my hand.',
    },
    {
      id: 'tenir-tu',
      type: 'conjugation',
      subject: 'tu',
      prompt: 'How do you conjugate tenir for “tu”?',
      answer: 'tiens',
      example: 'Tu tiens la porte ?',
      translation: 'Are you holding the door?',
    },
    {
      id: 'tenir-il',
      type: 'conjugation',
      subject: 'il / elle / on',
      prompt: 'How do you conjugate tenir for “il / elle / on”?',
      answer: 'tient',
      example: 'Elle tient son sac.',
      translation: 'She is holding her bag.',
    },
    {
      id: 'tenir-nous',
      type: 'conjugation',
      subject: 'nous',
      prompt: 'How do you conjugate tenir for “nous”?',
      answer: 'tenons',
      example: 'Nous tenons les clés.',
      translation: 'We are holding the keys.',
    },
    {
      id: 'tenir-vous',
      type: 'conjugation',
      subject: 'vous',
      prompt: 'How do you conjugate tenir for “vous”?',
      answer: 'tenez',
      example: 'Vous tenez le micro.',
      translation: 'You are holding the microphone.',
    },
    {
      id: 'tenir-ils',
      type: 'conjugation',
      subject: 'ils / elles',
      prompt: 'How do you conjugate tenir for “ils / elles”?',
      answer: 'tiennent',
      example: 'Ils tiennent la corde.',
      translation: 'They are holding the rope.',
    },
    {
      id: 'tenir-a',
      type: 'expression',
      prompt: 'What does tenir à mean?',
      answer: 'to care about / to be attached to',
      example: 'Je tiens à mon indépendance.',
      translation: 'I care about my independence.',
    },
    {
      id: 'tenir-debout',
      type: 'expression',
      prompt: 'What does tenir debout mean?',
      answer: 'to stand / to hold up (literally or figuratively)',
      example: 'Cette excuse ne tient pas debout.',
      translation: 'That excuse does not hold up.',
    },
  ],
};

export function getDeck(verb: string): Deck | null {
  if (verb.toLowerCase() === 'tenir') return tenirDeck;
  return null;
}
