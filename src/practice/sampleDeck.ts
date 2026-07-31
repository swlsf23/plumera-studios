import type { Deck } from './types';

/** Hand sample for /app/flashcard/prendre until data/ TSVs are wired. */
export const prendreDeck: Deck = {
  verb: 'prendre',
  gloss: 'to take',
  level: 'A1',
  lessonHref: '/en/learn-french/votw/votw-prendre-a1/',
  cards: [
    {
      id: 'prendre-je',
      type: 'conjugation',
      subject: 'je',
      prompt: 'How do you conjugate prendre for “je”?',
      answer: 'prends',
      example: 'Je prends mon sac.',
      translation: "I'm taking my bag.",
    },
    {
      id: 'prendre-tu',
      type: 'conjugation',
      subject: 'tu',
      prompt: 'How do you conjugate prendre for “tu”?',
      answer: 'prends',
      example: 'Prends ton téléphone.',
      translation: 'Take your phone.',
    },
    {
      id: 'prendre-il',
      type: 'conjugation',
      subject: 'il / elle / on',
      prompt: 'How do you conjugate prendre for “il / elle / on”?',
      answer: 'prend',
      example: 'Elle prend un livre.',
      translation: 'She takes a book.',
    },
    {
      id: 'prendre-nous',
      type: 'conjugation',
      subject: 'nous',
      prompt: 'How do you conjugate prendre for “nous”?',
      answer: 'prenons',
      example: 'Nous prenons le train.',
      translation: 'We take the train.',
    },
    {
      id: 'prendre-vous',
      type: 'conjugation',
      subject: 'vous',
      prompt: 'How do you conjugate prendre for “vous”?',
      answer: 'prenez',
      example: 'Vous prenez un café ?',
      translation: 'Are you having a coffee?',
    },
    {
      id: 'prendre-ils',
      type: 'conjugation',
      subject: 'ils / elles',
      prompt: 'How do you conjugate prendre for “ils / elles”?',
      answer: 'prennent',
      example: 'Ils prennent le bus.',
      translation: 'They take the bus.',
    },
    {
      id: 'prendre-bus',
      type: 'expression',
      prompt: 'How do you say “to take the bus” in French?',
      answer: 'prendre le bus',
      example: "J'ai pris le bus.",
      translation: 'I took the bus. / I went by bus.',
    },
    {
      id: 'prendre-froid',
      type: 'expression',
      prompt: 'What does prendre froid mean?',
      answer: 'to catch a chill / to get cold',
      example: 'Mets ton manteau, tu vas prendre froid.',
      translation: "Put on your coat or you'll catch a chill.",
    },
  ],
};

export function getDeck(verb: string): Deck | null {
  const key = verb.toLowerCase().replace(/\/$/, '');
  if (key === 'prendre') return prendreDeck;
  return null;
}
