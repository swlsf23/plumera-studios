import type { CardFace, StudyDirection, StudyMode } from './types';

const STORAGE_PREFIX = 'plumera.flashcard.session.v1:';

const MODES: StudyMode[] = ['mixed', 'en-fr', 'fr-en', 'both'];
const FACES: CardFace[] = ['prompt', 'answer', 'example'];
const DIRECTIONS: StudyDirection[] = ['en-fr', 'fr-en'];

export interface StoredStudySession {
  verb: string;
  index: number;
  face: CardFace;
  mode: StudyMode;
  pass: 1 | 2;
  mixedDirections: StudyDirection[];
  returnFace: 'prompt' | 'answer';
}

function storageKey(verb: string): string {
  return `${STORAGE_PREFIX}${verb}`;
}

function isDirection(value: unknown): value is StudyDirection {
  return typeof value === 'string' && DIRECTIONS.includes(value as StudyDirection);
}

export function loadStudySession(verb: string, cardCount: number): StoredStudySession | null {
  if (typeof sessionStorage === 'undefined' || cardCount <= 0) return null;
  try {
    const raw = sessionStorage.getItem(storageKey(verb));
    if (!raw) return null;
    const data = JSON.parse(raw) as Partial<StoredStudySession>;
    if (data.verb !== verb) return null;
    if (typeof data.index !== 'number' || data.index < 0 || data.index >= cardCount) {
      return null;
    }
    if (!data.mode || !MODES.includes(data.mode)) return null;
    if (data.pass !== 1 && data.pass !== 2) return null;
    if (!data.face || !FACES.includes(data.face)) return null;
    if (data.returnFace !== 'prompt' && data.returnFace !== 'answer') return null;
    if (
      !Array.isArray(data.mixedDirections) ||
      data.mixedDirections.length !== cardCount ||
      !data.mixedDirections.every(isDirection)
    ) {
      return null;
    }
    return {
      verb,
      index: data.index,
      face: data.face,
      mode: data.mode,
      pass: data.pass,
      mixedDirections: data.mixedDirections,
      returnFace: data.returnFace,
    };
  } catch {
    return null;
  }
}

export function saveStudySession(session: StoredStudySession): void {
  if (typeof sessionStorage === 'undefined') return;
  try {
    sessionStorage.setItem(storageKey(session.verb), JSON.stringify(session));
  } catch {
    // Quota / private mode — ignore; session still works in memory.
  }
}
