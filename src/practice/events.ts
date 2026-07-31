import { STUDY_DEFAULTS } from './studyDefaults';
import type { CardFace, Flashcard, StudyDirection, StudyMode } from './types';

export type StudyEventType =
  | 'session_started'
  | 'session_completed'
  | 'mode_changed'
  | 'card_graded'
  | 'played_audio'
  | 'key';

export type StudyGrade = 'know' | 'dont_know';

export interface VocabItem {
  card_id: string;
  type: Flashcard['type'];
  subject?: string;
  en: string;
  fr: string;
}

export interface StudySessionContext {
  session_id: string;
  verb: string;
  locale?: string;
  target?: string;
  started_mode: StudyMode;
  mode: StudyMode;
  pass: 1 | 2;
  face: CardFace;
  direction: StudyDirection;
  card: Flashcard | null;
}

type EventBody = Record<string, unknown>;

let active: StudySessionContext | null = null;

const LOCAL_EVENTS_PATH = '/__local/study-events';

export function setActiveStudySession(ctx: StudySessionContext | null): void {
  active = ctx;
}

export function newSessionId(): string {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return crypto.randomUUID();
  }
  return `sess_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
}

export function vocabFromCard(card: Flashcard | null | undefined): VocabItem | null {
  if (!card) return null;
  return {
    card_id: card.id,
    type: card.type,
    ...(card.subject ? { subject: card.subject } : {}),
    en: card.en,
    fr: card.fr,
  };
}

function envelope(type: StudyEventType, body: EventBody): EventBody {
  const base: EventBody = {
    type,
    ts: new Date().toISOString(),
    schema_version: STUDY_DEFAULTS.schemaVersion,
    source: STUDY_DEFAULTS.source,
  };
  if (!active) return { ...base, ...body };
  return {
    ...base,
    session_id: active.session_id,
    verb: active.verb,
    locale: active.locale,
    target: active.target,
    started_mode: active.started_mode,
    mode: active.mode,
    pass: active.pass,
    face: active.face,
    direction: active.direction,
    ...body,
  };
}

/** Fire-and-forget local sink (dev/serve). No-op if the endpoint is missing. */
export function emitStudyEvent(type: StudyEventType, body: EventBody = {}): void {
  const event = envelope(type, body);
  if (typeof fetch === 'undefined') return;
  void fetch(LOCAL_EVENTS_PATH, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(event),
  }).catch(() => {
    /* local sink optional */
  });
}

export function emitKey(key: string, extra: EventBody = {}): void {
  const vocab = vocabFromCard(active?.card);
  emitStudyEvent('key', {
    key,
    ...(vocab ? { vocab } : {}),
    ...extra,
  });
}

export function emitCardGraded(grade: StudyGrade, card: Flashcard, direction: StudyDirection): void {
  const vocab = vocabFromCard(card);
  if (!vocab) return;
  emitStudyEvent('card_graded', { grade, direction, vocab });
}

export function emitPlayedAudio(card: Flashcard | null, audioUrl: string | null): void {
  const vocab = vocabFromCard(card);
  emitStudyEvent('played_audio', {
    audio: audioUrl,
    ...(vocab ? { vocab } : {}),
  });
}
