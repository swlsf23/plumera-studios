import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  emitCardGraded,
  emitKey,
  emitPlayedAudio,
  emitStudyEvent,
  newSessionId,
  setActiveStudySession,
} from './events';
import { loadStudySession, saveStudySession } from './sessionStorage';
import { STUDY_DEFAULTS } from './studyDefaults';
import {
  answerLang,
  promptLang,
  textForLang,
  type CardFace,
  type CardLang,
  type Deck,
  type StudyDirection,
  type StudyMode,
} from './types';

/*
  Queued for revisit after trying the loop:
  - Grade only after seeing the answer, or anytime? (temp: anytime)
  - Exact keys? (3 = don’t know, 4 = know; ←/→ still browse queue)
  - Persist queue across mode change? (temp: mode change resets queue)
  - Both-mode pass refill details / bar denom? (temp: refill pass 2; goal = 2× deck)
*/

function randomDirections(count: number): StudyDirection[] {
  return Array.from({ length: count }, () => (Math.random() < 0.5 ? 'en-fr' : 'fr-en'));
}

function fullQueue(count: number): number[] {
  return Array.from({ length: count }, (_, i) => i);
}

export function useStudySession(deck: Deck, { enabled }: { enabled: boolean }) {
  const total = deck.cards.length;
  const verb = deck.verb;

  const restored = useMemo(() => loadStudySession(verb, total), [verb, total]);
  const sessionIdRef = useRef(newSessionId());
  const startedModeRef = useRef<StudyMode>(restored?.mode ?? STUDY_DEFAULTS.defaultMode);
  const startedEmitted = useRef(false);

  const [queue, setQueue] = useState<number[]>(() => restored?.queue ?? fullQueue(total));
  const [queuePos, setQueuePos] = useState(() => restored?.queuePos ?? 0);
  const [cleared, setCleared] = useState(() => restored?.cleared ?? 0);
  const [done, setDone] = useState(() => restored?.done ?? false);
  const [face, setFace] = useState<CardFace>(() => restored?.face ?? 'prompt');
  const [mode, setMode] = useState<StudyMode>(
    () => restored?.mode ?? STUDY_DEFAULTS.defaultMode,
  );
  /** Pass 1 = EN→FR, pass 2 = FR→EN (both mode only). */
  const [pass, setPass] = useState<1 | 2>(() => restored?.pass ?? 1);
  const [mixedDirections, setMixedDirections] = useState<StudyDirection[]>(
    () => restored?.mixedDirections ?? randomDirections(total),
  );
  /** Face to restore when leaving the example via E. */
  const [returnFace, setReturnFace] = useState<'prompt' | 'answer'>(
    () => restored?.returnFace ?? 'prompt',
  );

  useEffect(() => {
    saveStudySession({
      verb,
      queue,
      queuePos,
      cleared,
      done,
      face,
      mode,
      pass,
      mixedDirections,
      returnFace,
    });
  }, [
    verb,
    queue,
    queuePos,
    cleared,
    done,
    face,
    mode,
    pass,
    mixedDirections,
    returnFace,
  ]);

  const index = queue.length > 0 ? (queue[queuePos] ?? 0) : 0;
  const card = !done && queue.length > 0 ? (deck.cards[index] ?? null) : null;
  const hasExample = Boolean(card?.example?.trim());

  const sessionGoal = mode === 'both' ? total * 2 : total;
  // Both mode: pass 1 still has a full second pass ahead, so count that too.
  const remaining =
    mode === 'both' && pass === 1 ? queue.length + total : queue.length;

  const knowPct = useMemo(() => {
    if (sessionGoal === 0) return 0;
    return Math.round((cleared / sessionGoal) * 100);
  }, [cleared, sessionGoal]);

  const queuePct = useMemo(() => {
    if (sessionGoal === 0) return 0;
    return Math.round((remaining / sessionGoal) * 100);
  }, [remaining, sessionGoal]);

  const direction: StudyDirection = useMemo(() => {
    if (mode === 'en-fr') return 'en-fr';
    if (mode === 'fr-en') return 'fr-en';
    if (mode === 'both') return pass === 1 ? 'en-fr' : 'fr-en';
    return mixedDirections[index] ?? 'en-fr';
  }, [index, mixedDirections, mode, pass]);

  const showingLang: CardLang | 'example' = useMemo(() => {
    if (face === 'example') return 'example';
    if (face === 'prompt') return promptLang(direction);
    return answerLang(direction);
  }, [direction, face]);

  const promptText = card ? textForLang(card, promptLang(direction)) : '';
  const answerText = card ? textForLang(card, answerLang(direction)) : '';

  useEffect(() => {
    setActiveStudySession({
      session_id: sessionIdRef.current,
      verb,
      locale: deck.locale,
      target: deck.target,
      started_mode: startedModeRef.current,
      mode,
      pass,
      face,
      direction,
      card,
    });
    return () => setActiveStudySession(null);
  }, [verb, deck.locale, deck.target, mode, pass, face, direction, card]);

  useEffect(() => {
    if (!enabled || startedEmitted.current) return;
    startedEmitted.current = true;
    emitStudyEvent('session_started', {
      defaults: { ...STUDY_DEFAULTS },
      restored: Boolean(restored),
      card_count: total,
    });
  }, [enabled, restored, total]);

  const resetFace = useCallback(() => {
    setFace('prompt');
    setReturnFace('prompt');
  }, []);

  const prevCard = useCallback(() => {
    if (done || queue.length === 0) return;
    if (queuePos > 0) {
      setQueuePos(queuePos - 1);
      resetFace();
    }
  }, [done, queue.length, queuePos, resetFace]);

  const nextCard = useCallback(() => {
    if (done || queue.length === 0) return;
    if (queuePos < queue.length - 1) {
      setQueuePos(queuePos + 1);
      resetFace();
    }
  }, [done, queue.length, queuePos, resetFace]);

  const canPrev = !done && queuePos > 0;
  const canNext = !done && queuePos < queue.length - 1;

  const markKnow = useCallback(() => {
    if (done || queue.length === 0) return;
    if (card) emitCardGraded('know', card, direction);

    const nextQueue = queue.filter((_, i) => i !== queuePos);
    const nextCleared = cleared + 1;

    if (nextQueue.length === 0) {
      if (mode === 'both' && pass === 1) {
        setPass(2);
        setQueue(fullQueue(total));
        setQueuePos(0);
        setCleared(nextCleared);
        resetFace();
        return;
      }
      setQueue([]);
      setQueuePos(0);
      setCleared(nextCleared);
      setDone(true);
      emitStudyEvent('session_completed', {
        cleared: nextCleared,
        session_goal: mode === 'both' ? total * 2 : total,
      });
      return;
    }

    setQueue(nextQueue);
    setQueuePos(Math.min(queuePos, nextQueue.length - 1));
    setCleared(nextCleared);
    resetFace();
  }, [card, cleared, direction, done, mode, pass, queue, queuePos, resetFace, total]);

  const markDontKnow = useCallback(() => {
    if (done || queue.length === 0) return;
    if (card) emitCardGraded('dont_know', card, direction);

    if (queue.length <= 1) {
      // Single card left: send to back is a no-op positionally; still reset face.
      resetFace();
      return;
    }

    const current = queue[queuePos];
    if (current === undefined) return;
    const without = queue.filter((_, i) => i !== queuePos);
    const nextQueue = [...without, current];
    // Stay at queuePos → card that was next; wrap if we removed the last item.
    const nextPos = queuePos >= nextQueue.length ? 0 : queuePos;
    setQueue(nextQueue);
    setQueuePos(nextPos);
    resetFace();
  }, [card, direction, done, queue, queuePos, resetFace]);

  const restartSession = useCallback(() => {
    sessionIdRef.current = newSessionId();
    startedModeRef.current = mode;
    setQueue(fullQueue(total));
    setQueuePos(0);
    setCleared(0);
    setDone(false);
    setPass(1);
    if (mode === 'mixed') {
      setMixedDirections(randomDirections(total));
    }
    resetFace();
    emitStudyEvent('session_started', {
      defaults: { ...STUDY_DEFAULTS },
      restored: false,
      restarted: true,
      card_count: total,
      mode,
    });
  }, [mode, resetFace, total]);

  /** ↑ / ↓ cycle prompt ↔ answer only (wrap). Example is not in this cycle. */
  const flipDown = useCallback(() => {
    if (done) return;
    if (face === 'example') {
      setFace('answer');
      setReturnFace('answer');
      return;
    }
    const next = face === 'prompt' ? 'answer' : 'prompt';
    setFace(next);
    setReturnFace(next);
  }, [done, face]);

  const flipUp = useCallback(() => {
    if (done) return;
    if (face === 'example') {
      setFace('prompt');
      setReturnFace('prompt');
      return;
    }
    const next = face === 'answer' ? 'prompt' : 'answer';
    setFace(next);
    setReturnFace(next);
  }, [done, face]);

  /** E toggles example; restores the prior prompt/answer side. */
  const jumpExample = useCallback(() => {
    if (done || !hasExample) return;
    if (face === 'example') {
      setFace(returnFace);
      return;
    }
    if (face === 'prompt' || face === 'answer') {
      setReturnFace(face);
    }
    setFace('example');
  }, [done, face, hasExample, returnFace]);

  /** Temp: mode change resets the queue. Revisit later. */
  const setStudyMode = useCallback(
    (next: StudyMode) => {
      const previous = mode;
      setMode(next);
      startedModeRef.current = next;
      sessionIdRef.current = newSessionId();
      setQueue(fullQueue(total));
      setQueuePos(0);
      setCleared(0);
      setDone(false);
      if (next === 'mixed') {
        setMixedDirections(randomDirections(total));
      }
      setPass(1);
      resetFace();
      emitStudyEvent('mode_changed', { from: previous, to: next });
      emitStudyEvent('session_started', {
        defaults: { ...STUDY_DEFAULTS },
        restored: false,
        mode_reset: true,
        card_count: total,
        mode: next,
      });
    },
    [mode, resetFace, total],
  );

  const trackPlayedAudio = useCallback(
    (audioUrl: string | null) => {
      emitPlayedAudio(card, audioUrl);
    },
    [card],
  );

  useEffect(() => {
    if (!enabled) return;

    const onKeyDown = (event: KeyboardEvent) => {
      // Leave browser shortcuts alone (⌘←/→ history, etc.).
      if (event.metaKey || event.ctrlKey || event.altKey) return;

      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === 'INPUT' ||
          target.tagName === 'TEXTAREA' ||
          target.isContentEditable)
      ) {
        return;
      }

      switch (event.key) {
        case ' ':
        case 'Spacebar':
          event.preventDefault();
          emitKey('Space');
          flipDown();
          break;
        case 'ArrowUp':
          event.preventDefault();
          emitKey('ArrowUp');
          flipUp();
          break;
        case 'ArrowDown':
          event.preventDefault();
          emitKey('ArrowDown');
          flipDown();
          break;
        case 'ArrowLeft':
          event.preventDefault();
          emitKey('ArrowLeft');
          prevCard();
          break;
        case 'ArrowRight':
          event.preventDefault();
          emitKey('ArrowRight');
          nextCard();
          break;
        case 'e':
        case 'E':
          event.preventDefault();
          emitKey('e');
          jumpExample();
          break;
        case '3':
          event.preventDefault();
          emitKey('3');
          markDontKnow();
          break;
        case '4':
          event.preventDefault();
          emitKey('4');
          markKnow();
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [
    enabled,
    flipDown,
    flipUp,
    jumpExample,
    markDontKnow,
    markKnow,
    nextCard,
    prevCard,
  ]);

  return {
    card,
    index,
    total,
    face,
    mode,
    pass,
    direction,
    showingLang,
    promptText,
    answerText,
    hasExample,
    done,
    cleared,
    remaining,
    sessionGoal,
    knowPct,
    queuePct,
    canPrev,
    canNext,
    prevCard,
    nextCard,
    flipUp,
    flipDown,
    jumpExample,
    markKnow,
    markDontKnow,
    restartSession,
    setStudyMode,
    trackPlayedAudio,
  };
}
