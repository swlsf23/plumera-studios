import { useCallback, useEffect, useMemo, useState } from 'react';
import { loadStudySession, saveStudySession } from './sessionStorage';
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

function randomDirections(count: number): StudyDirection[] {
  return Array.from({ length: count }, () => (Math.random() < 0.5 ? 'en-fr' : 'fr-en'));
}

export function useStudySession(deck: Deck, { enabled }: { enabled: boolean }) {
  const total = deck.cards.length;
  const verb = deck.verb;

  const restored = useMemo(() => loadStudySession(verb, total), [verb, total]);

  const [index, setIndex] = useState(() => restored?.index ?? 0);
  const [face, setFace] = useState<CardFace>(() => restored?.face ?? 'prompt');
  const [mode, setMode] = useState<StudyMode>(() => restored?.mode ?? 'mixed');
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
      index,
      face,
      mode,
      pass,
      mixedDirections,
      returnFace,
    });
  }, [verb, index, face, mode, pass, mixedDirections, returnFace]);

  const card = deck.cards[index] ?? null;
  const hasExample = Boolean(card?.example?.trim());

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

  const progressPct = useMemo(() => {
    if (total === 0) return 0;
    if (mode === 'both') {
      const step = (pass - 1) * total + index + 1;
      return Math.round((step / (total * 2)) * 100);
    }
    return Math.round(((index + 1) / total) * 100);
  }, [index, mode, pass, total]);

  const resetFace = useCallback(() => {
    setFace('prompt');
    setReturnFace('prompt');
  }, []);

  const prevCard = useCallback(() => {
    if (mode === 'both' && pass === 2 && index === 0) {
      setPass(1);
      setIndex(total - 1);
      resetFace();
      return;
    }
    if (index > 0) {
      setIndex(index - 1);
      resetFace();
    }
  }, [index, mode, pass, resetFace, total]);

  const nextCard = useCallback(() => {
    if (mode === 'both' && pass === 1 && index >= total - 1) {
      setPass(2);
      setIndex(0);
      resetFace();
      return;
    }
    if (index < total - 1) {
      setIndex(index + 1);
      resetFace();
    }
  }, [index, mode, pass, resetFace, total]);

  const canPrev = index > 0 || (mode === 'both' && pass === 2);
  const canNext = index < total - 1 || (mode === 'both' && pass === 1 && total > 0);

  /** ↑ / ↓ cycle prompt ↔ answer only (wrap). Example is not in this cycle. */
  const flipDown = useCallback(() => {
    if (face === 'example') {
      setFace('answer');
      setReturnFace('answer');
      return;
    }
    const next = face === 'prompt' ? 'answer' : 'prompt';
    setFace(next);
    setReturnFace(next);
  }, [face]);

  const flipUp = useCallback(() => {
    if (face === 'example') {
      setFace('prompt');
      setReturnFace('prompt');
      return;
    }
    const next = face === 'answer' ? 'prompt' : 'answer';
    setFace(next);
    setReturnFace(next);
  }, [face]);

  /** E toggles example; restores the prior prompt/answer side. */
  const jumpExample = useCallback(() => {
    if (!hasExample) return;
    if (face === 'example') {
      setFace(returnFace);
      return;
    }
    if (face === 'prompt' || face === 'answer') {
      setReturnFace(face);
    }
    setFace('example');
  }, [face, hasExample, returnFace]);

  /** Stay on the same card; show prompt in the new mode. Feel it out from here. */
  const setStudyMode = useCallback(
    (next: StudyMode) => {
      setMode(next);
      if (next === 'mixed') {
        setMixedDirections(randomDirections(total));
      }
      if (next === 'both') {
        setPass(1);
      }
      resetFace();
    },
    [resetFace, total],
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
        case 'ArrowUp':
          event.preventDefault();
          flipUp();
          break;
        case 'ArrowDown':
          event.preventDefault();
          flipDown();
          break;
        case 'ArrowLeft':
          event.preventDefault();
          prevCard();
          break;
        case 'ArrowRight':
          event.preventDefault();
          nextCard();
          break;
        case 'e':
        case 'E':
          event.preventDefault();
          jumpExample();
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [enabled, flipDown, flipUp, jumpExample, nextCard, prevCard]);

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
    progressPct,
    canPrev,
    canNext,
    prevCard,
    nextCard,
    flipUp,
    flipDown,
    jumpExample,
    setStudyMode,
  };
}
