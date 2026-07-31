import { useEffect, useId, useRef, useState } from 'react';
import type {
  CardFace,
  Flashcard as FlashcardData,
  StudyMode,
} from '../practice/types';

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
  { key: 'E', action: 'Show or hide the example' },
  { key: '↑', action: 'Cycle front ↔ back' },
  { key: '↓', action: 'Cycle front ↔ back' },
  { key: '←', action: 'Previous card' },
  { key: '→', action: 'Next card' },
];

interface FlashcardProps {
  card: FlashcardData;
  index: number;
  total: number;
  face: CardFace;
  mode: StudyMode;
  pass: 1 | 2;
  showingLang: 'en' | 'fr' | 'example';
  promptText: string;
  answerText: string;
  progressPct: number;
  canPrev: boolean;
  canNext: boolean;
  onPrev: () => void;
  onNext: () => void;
  onFlipUp: () => void;
  onFlipDown: () => void;
  onModeChange: (mode: StudyMode) => void;
}

function modeLabel(mode: StudyMode): string {
  return MODES.find((item) => item.id === mode)?.label ?? 'Mixed';
}

type OpenMenu = 'mode' | 'help' | null;

export default function Flashcard({
  card,
  index,
  total,
  face,
  mode,
  pass,
  showingLang,
  promptText,
  answerText,
  progressPct,
  canPrev,
  canNext,
  onPrev,
  onNext,
  onFlipUp,
  onFlipDown,
  onModeChange,
}: FlashcardProps) {
  const [openMenu, setOpenMenu] = useState<OpenMenu>(null);
  const controlsRef = useRef<HTMLDivElement>(null);
  const modeMenuId = useId();
  const helpMenuId = useId();

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

  return (
    <section className="flashcard" aria-live="polite">
      <div className="card-meta">
        <span>
          Card {index + 1} of {total}
          {mode === 'both' ? ` · Pass ${pass}` : ''}
        </span>
        <div className="meta-progress">
          <span className="meta-progress__bar" aria-hidden="true">
            <span style={{ width: `${progressPct}%` }} />
          </span>
          <span>{progressPct}%</span>
        </div>

        <div className="meta-controls" ref={controlsRef}>
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
                <p className="meta-popover__title">Navigation</p>
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
      </div>

      <div className="card-actions card-actions--browse">
        <button
          className="button button--icon"
          type="button"
          onClick={onPrev}
          disabled={!canPrev}
          aria-label="Previous card"
        >
          ←
        </button>
        <button
          className="button button--outline"
          type="button"
          onClick={onFlipDown}
          aria-label="Cycle faces down"
        >
          ↓ Flip
        </button>
        <button
          className="button button--outline"
          type="button"
          onClick={onFlipUp}
          aria-label="Cycle faces up"
        >
          ↑ Flip
        </button>
        <button
          className="button button--icon"
          type="button"
          onClick={onNext}
          disabled={!canNext}
          aria-label="Next card"
        >
          →
        </button>
      </div>
    </section>
  );
}
