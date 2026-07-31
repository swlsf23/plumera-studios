import type { Deck } from './types';
import prendre from '../../data/en/learn-french/prendre.json';

const decks: Record<string, Deck> = {
  prendre: prendre as Deck,
};

export function getDeck(verb: string): Deck | null {
  const key = verb.toLowerCase().replace(/\/$/, '');
  return decks[key] ?? null;
}
