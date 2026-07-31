import type { StudyMode } from './types';

/** Local / future-prod defaults for a new study session. */
export const STUDY_DEFAULTS = {
  /** Mode when no sessionStorage restore is present. */
  defaultMode: 'mixed' as StudyMode,
  source: 'flashcard-local' as const,
  schemaVersion: 1,
};
