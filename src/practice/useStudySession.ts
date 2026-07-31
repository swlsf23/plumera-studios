import { useCallback, useMemo, useState } from 'react';
import type { CardFace, Deck, Grade } from './types';

export function useStudySession(deck: Deck) {
  const total = deck.cards.length;
  const [index, setIndex] = useState(0);
  const [face, setFace] = useState<CardFace>('prompt');
  const [knowCount, setKnowCount] = useState(0);
  const [dontKnowCount, setDontKnowCount] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [finished, setFinished] = useState(false);

  const card = deck.cards[index] ?? null;

  const progressPct = useMemo(() => {
    if (total === 0) return 0;
    return Math.round((completed / total) * 100);
  }, [completed, total]);

  const reveal = useCallback(() => {
    setFace('answer');
  }, []);

  const goTo = useCallback(
    (nextIndex: number) => {
      const clamped = Math.max(0, Math.min(nextIndex, total - 1));
      setIndex(clamped);
      setFace('prompt');
      setFinished(false);
    },
    [total],
  );

  const back = useCallback(() => {
    if (face === 'answer') {
      setFace('prompt');
      return;
    }
    if (index > 0) goTo(index - 1);
  }, [face, goTo, index]);

  const grade = useCallback(
    (result: Grade) => {
      if (face !== 'answer' || finished) return;
      if (result === 'know') setKnowCount((n) => n + 1);
      else setDontKnowCount((n) => n + 1);
      setCompleted((n) => Math.min(total, n + 1));

      if (index >= total - 1) {
        setFinished(true);
        return;
      }
      goTo(index + 1);
    },
    [face, finished, goTo, index, total],
  );

  return {
    card,
    index,
    total,
    face,
    knowCount,
    dontKnowCount,
    completed,
    progressPct,
    finished,
    reveal,
    grade,
    back,
  };
}
