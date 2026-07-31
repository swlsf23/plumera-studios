import type { CardFace, Flashcard as FlashcardData, Grade } from '../practice/types';

interface FlashcardProps {
  card: FlashcardData;
  index: number;
  total: number;
  face: CardFace;
  progressPct: number;
  onReveal: () => void;
  onGrade: (grade: Grade) => void;
  onBack: () => void;
}

function typeLabel(type: FlashcardData['type']): string {
  return type === 'conjugation' ? 'Conjugation' : 'Expression';
}

export default function Flashcard({
  card,
  index,
  total,
  face,
  progressPct,
  onReveal,
  onGrade,
  onBack,
}: FlashcardProps) {
  return (
    <section className="flashcard" aria-live="polite">
      <div className="card-meta">
        <span>
          Card {index + 1} of {total}
        </span>
        <div className="meta-progress">
          <span className="meta-progress__bar" aria-hidden="true">
            <span style={{ width: `${progressPct}%` }} />
          </span>
          <span>{progressPct}%</span>
        </div>
        <span className="card-type">{typeLabel(card.type)}</span>
      </div>

      {face === 'prompt' ? (
        <div className="card-content">
          {card.subject ? (
            <div className="subject-label">
              <span className="round-icon round-icon--small" aria-hidden="true">
                ◇
              </span>
              <span>{card.subject}</span>
            </div>
          ) : null}
          <p className="card-kicker">Prompt</p>
          <h2>{card.prompt}</h2>
          <button className="reveal-button" type="button" onClick={onReveal}>
            <span className="reveal-symbol" aria-hidden="true">
              ⌁
            </span>
            <span>Tap to reveal answer</span>
          </button>
        </div>
      ) : (
        <div className="answer-content">
          {card.subject ? <span className="answer-subject">{card.subject}</span> : null}
          <h2>
            <em>{card.answer}</em>
          </h2>
          {card.example ? (
            <div className="example">
              <span>Example</span>
              <p>{card.example}</p>
              {card.translation ? <p className="translation">( {card.translation} )</p> : null}
            </div>
          ) : null}
        </div>
      )}

      <div className="card-actions">
        <button className="button button--icon" type="button" onClick={onBack} aria-label="Previous">
          ←
        </button>
        {face === 'prompt' ? (
          <>
            <button className="button button--outline" type="button" disabled>
              × &nbsp; I don&apos;t know
            </button>
            <button className="button button--solid" type="button" disabled>
              ✓ &nbsp; I know this
            </button>
          </>
        ) : (
          <>
            <button
              className="button button--outline"
              type="button"
              onClick={() => onGrade('dontKnow')}
            >
              × &nbsp; I don&apos;t know
            </button>
            <button
              className="button button--solid"
              type="button"
              onClick={() => onGrade('know')}
            >
              ✓ &nbsp; I know this
            </button>
          </>
        )}
      </div>
    </section>
  );
}
