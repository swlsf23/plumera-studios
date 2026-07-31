import { useEffect, useId, useRef, useState } from 'react';
import { emitKey } from '../practice/events';
import type {
  CardFace,
  Flashcard as FlashcardData,
  StudyMode,
} from '../practice/types';
import AudioButton, { type AudioButtonHandle } from './AudioButton';

const MODES: { id: StudyMode; label: string; description: string }[] = [
  {
    id: 'mixed',
    label: 'Mixed',
    description: 'Each card picks a direction at random for this session.',
  },
  {
    id: 'en-fr',
    label: 'EN → FR',
    description: 'English prompt, French answer. Practice producing French.',
  },
  {
    id: 'fr-en',
    label: 'FR → EN',
    description: 'French prompt, English answer. Practice recognition.',
  },
  {
    id: 'both',
    label: 'Both passes',
    description: 'Go through the deck EN → FR, then again FR → EN.',
  },
];

const NAV_KEYS: { key: string; action: string }[] = [
  { key: '3', action: 'Don’t know — keep in queue, next card' },
  { key: '4', action: 'Know — clear from queue, next card' },
  { key: 'Space', action: 'Flip front ↔ back' },
  { key: 'a', action: 'Play French audio' },
  { key: 'E', action: 'Show or hide the example' },
  { key: '↑', action: 'Cycle front ↔ back' },
  { key: '↓', action: 'Cycle front ↔ back' },
  { key: '←', action: 'Previous card in queue' },
  { key: '→', action: 'Next card in queue' },
];


interface FlashcardProps {
  card: FlashcardData | null;
  face: CardFace;
  mode: StudyMode;
  pass: 1 | 2;
  showingLang: 'en' | 'fr' | 'example';
  promptText: string;
  answerText: string;
  done: boolean;
  cleared: number;
  remaining: number;
  sessionGoal: number;
  knowPct: number;
  queuePct: number;
  canPrev: boolean;
  canNext: boolean;
  onPrev: () => void;
  onNext: () => void;
  onKnow: () => void;
  onDontKnow: () => void;
  onRestart: () => void;
  onModeChange: (mode: StudyMode) => void;
  /** Resolved site URL for French-face audio, if any. */
  audioUrl?: string | null;
  onPlayedAudio?: () => void;
}

function modeLabel(mode: StudyMode): string {
  return MODES.find((item) => item.id === mode)?.label ?? 'Mixed';
}

type OpenMenu = 'mode' | 'help' | null;

export default function Flashcard({
  card,
  face,
  mode,
  pass,
  showingLang,
  promptText,
  answerText,
  done,
  cleared,
  remaining,
  sessionGoal,
  knowPct,
  queuePct,
  canPrev,
  canNext,
  onPrev,
  onNext,
  onKnow,
  onDontKnow,
  onRestart,
  onModeChange,
  audioUrl: audioUrlProp = null,
  onPlayedAudio,
}: FlashcardProps) {
  const [openMenu, setOpenMenu] = useState<OpenMenu>(null);
  const controlsRef = useRef<HTMLDivElement>(null);
  const audioButtonRef = useRef<AudioButtonHandle>(null);
  const modeMenuId = useId();
  const helpMenuId = useId();

  const audioUrl = showingLang === 'fr' ? audioUrlProp : null;

  useEffect(() => {
    if (!openMenu) return;

    const onPointerDown = (event: MouseEvent) => {
      if (!controlsRef.current?.contains(event.target as Node)) {
        setOpenMenu(null);
      }
    };

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpenMenu(null);
    };

    document.addEventListener('mousedown', onPointerDown);
    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('mousedown', onPointerDown);
      document.removeEventListener('keydown', onKeyDown);
    };
  }, [openMenu]);

  useEffect(() => {
    if (!audioUrl) return;

    const onKeyDown = (event: KeyboardEvent) => {
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
      if (event.key !== 'a' && event.key !== 'A') return;
      event.preventDefault();
      emitKey('a');
      audioButtonRef.current?.play();
    };

    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [audioUrl]);

  return (
    <section className="flashcard" aria-live="polite">
      <div className="card-meta card-meta--queue">
        <div className="meta-progress meta-progress--dual" aria-label="Session progress">
          <div className="meta-progress__track">
            <span className="meta-progress__label">
              Know · {cleared}/{sessionGoal}
            </span>
            <span className="meta-progress__bar meta-progress__bar--know" aria-hidden="true">
              <span style={{ width: `${knowPct}%` }} />
            </span>
          </div>
          <div className="meta-progress__track">
            <span className="meta-progress__label">
              Queue · {remaining}/{sessionGoal}
            </span>
            <span className="meta-progress__bar meta-progress__bar--queue" aria-hidden="true">
              <span style={{ width: `${queuePct}%` }} />
            </span>
          </div>
        </div>

        <div className="meta-controls" ref={controlsRef}>
          {mode === 'both' && !done ? (
            <span className="card-pass">Pass {pass}</span>
          ) : null}
          <div className="meta-menu">
            <button
              type="button"
              className={openMenu === 'mode' ? 'card-type card-type--btn is-open' : 'card-type card-type--btn'}
              aria-haspopup="listbox"
              aria-expanded={openMenu === 'mode'}
              aria-controls={modeMenuId}
              onClick={() => setOpenMenu((current) => (current === 'mode' ? null : 'mode'))}
            >
              Mode · {modeLabel(mode)}
              <span className="card-type__chevron" aria-hidden="true">
                ▾
              </span>
            </button>
            {openMenu === 'mode' ? (
              <div
                id={modeMenuId}
                className="meta-popover"
                role="listbox"
                aria-label="Study mode"
              >
                {MODES.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    role="option"
                    aria-selected={mode === item.id}
                    className={mode === item.id ? 'meta-popover__option is-active' : 'meta-popover__option'}
                    onClick={() => {
                      onModeChange(item.id);
                      setOpenMenu(null);
                    }}
                  >
                    <span className="meta-popover__label">{item.label}</span>
                    <span className="meta-popover__desc">{item.description}</span>
                  </button>
                ))}
              </div>
            ) : null}
          </div>

          <div className="meta-menu">
            <button
              type="button"
              className={openMenu === 'help' ? 'card-help is-open' : 'card-help'}
              aria-label="Keyboard navigation"
              aria-haspopup="dialog"
              aria-expanded={openMenu === 'help'}
              aria-controls={helpMenuId}
              onClick={() => setOpenMenu((current) => (current === 'help' ? null : 'help'))}
            >
              ?
            </button>
            {openMenu === 'help' ? (
              <div id={helpMenuId} className="meta-popover meta-popover--help" role="dialog" aria-label="Navigation">
                <p className="meta-popover__title">Keys</p>
                <ul className="nav-keys nav-keys--compact">
                  {NAV_KEYS.map((item) => (
                    <li key={item.key}>
                      <kbd className="nav-keys__key">{item.key}</kbd>
                      <span>{item.action}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        </div>
      </div>

      {done ? (
        <div className="card-content card-content--summary">
          <h2>Session complete</h2>
          <p className="done-copy">
            You cleared {cleared} of {sessionGoal}
            {mode === 'both' ? ' (both passes)' : ''} cards.
          </p>
          <button className="button button--solid" type="button" onClick={onRestart}>
            Practice again
          </button>
        </div>
      ) : card ? (
        <div className={`card-content card-content--${showingLang}`}>
          {face === 'prompt' ? <h2>{promptText}</h2> : null}

          {face === 'answer' ? (
            <h2>
              <em>{answerText}</em>
            </h2>
          ) : null}

          {face === 'example' ? (
            <>
              <h2>{card.example}</h2>
              {card.exampleTranslation ? (
                <p className="translation">( {card.exampleTranslation} )</p>
              ) : null}
            </>
          ) : null}

          {audioUrl ? (
            <AudioButton
              ref={audioButtonRef}
              src={audioUrl}
              label={card.fr}
              onPlayed={onPlayedAudio}
            />
          ) : null}
        </div>
      ) : null}

      <div className="card-actions card-actions--grade">
        <button
          className="button button--icon"
          type="button"
          onClick={onPrev}
          disabled={done || !canPrev}
          aria-label="Previous card in queue"
        >
          ←
        </button>
        <button
          className="button button--dont-know"
          type="button"
          onClick={onDontKnow}
          disabled={done}
        >
          Don’t know
        </button>
        <button
          className="button button--know"
          type="button"
          onClick={onKnow}
          disabled={done}
        >
          Know
        </button>
        <button
          className="button button--icon"
          type="button"
          onClick={onNext}
          disabled={done || !canNext}
          aria-label="Next card in queue"
        >
          →
        </button>
      </div>
    </section>
  );
}
