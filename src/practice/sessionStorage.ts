import type { CardFace, StudyDirection, StudyMode } from './types';

const STORAGE_PREFIX = 'plumera.flashcard.session.v2:';

const MODES: StudyMode[] = ['mixed', 'en-fr', 'fr-en', 'both'];
const FACES: CardFace[] = ['prompt', 'answer', 'example'];
const DIRECTIONS: StudyDirection[] = ['en-fr', 'fr-en'];

export interface StoredStudySession {
  verb: string;
  /** Remaining card indices (deck order positions), front of queue first. */
  queue: number[];
  /** Index into `queue` for the card currently shown. */
  queuePos: number;
  /** Cards cleared with Know this session (accumulates across both-mode passes). */
  cleared: number;
  done: boolean;
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

function isValidQueue(queue: unknown, cardCount: number): queue is number[] {
  if (!Array.isArray(queue)) return false;
  if (queue.length > cardCount) return false;
  const seen = new Set<number>();
  for (const item of queue) {
    if (typeof item !== 'number' || item < 0 || item >= cardCount || seen.has(item)) {
      return false;
    }
    seen.add(item);
  }
  return true;
}

export function loadStudySession(verb: string, cardCount: number): StoredStudySession | null {
  if (typeof sessionStorage === 'undefined' || cardCount <= 0) return null;
  try {
    const raw = sessionStorage.getItem(storageKey(verb));
    if (!raw) return null;
    const data = JSON.parse(raw) as Partial<StoredStudySession>;
    if (data.verb !== verb) return null;
    if (!data.mode || !MODES.includes(data.mode)) return null;
    if (data.pass !== 1 && data.pass !== 2) return null;
    if (!data.face || !FACES.includes(data.face)) return null;
    if (data.returnFace !== 'prompt' && data.returnFace !== 'answer') return null;
    if (typeof data.cleared !== 'number' || data.cleared < 0) return null;
    if (typeof data.done !== 'boolean') return null;
    if (!isValidQueue(data.queue, cardCount)) return null;
    if (
      typeof data.queuePos !== 'number' ||
      data.queuePos < 0 ||
      (data.queue.length > 0 && data.queuePos >= data.queue.length) ||
      (data.queue.length === 0 && data.queuePos !== 0)
    ) {
      return null;
    }
    if (
      !Array.isArray(data.mixedDirections) ||
      data.mixedDirections.length !== cardCount ||
      !data.mixedDirections.every(isDirection)
    ) {
      return null;
    }
    return {
      verb,
      queue: data.queue,
      queuePos: data.queuePos,
      cleared: data.cleared,
      done: data.done,
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
