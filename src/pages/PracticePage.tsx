import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import ContentHeader from '../components/ContentHeader';
import Flashcard from '../components/Flashcard';
import SiteFooter from '../components/SiteFooter';
import { getDeck } from '../practice/sampleDeck';
import { useStudySession } from '../practice/useStudySession';

type PracticeTab = 'flashcards' | 'about' | 'definition';

export default function PracticePage() {
  const { verb = '' } = useParams();
  const deck = useMemo(() => getDeck(verb), [verb]);

  if (!deck) {
    return (
      <div className="page practice-app">
        <ContentHeader />
        <main className="practice-missing">
          <h1>Deck not found</h1>
          <p>
            No flashcard deck for <em>{verb || 'unknown'}</em> yet.
          </p>
          <Link to="/prendre/">Practice prendre</Link>
        </main>
        <SiteFooter />
      </div>
    );
  }

  return <PracticeSession deck={deck} />;
}

function PracticeSession({ deck }: { deck: NonNullable<ReturnType<typeof getDeck>> }) {
  const session = useStudySession(deck);
  const [tab, setTab] = useState<PracticeTab>('flashcards');
  const conjugationCount = deck.cards.filter((c) => c.type === 'conjugation').length;
  const expressionCount = deck.cards.filter((c) => c.type === 'expression').length;

  return (
    <div className="page practice-app">
      <ContentHeader />

      <main className="practice-shell">
        <aside className="sidebar">
          <section className="panel progress-panel">
            <p className="eyebrow">Practice progress</p>
            <div className="progress-overview">
              <div
                className="progress-ring"
                style={{ ['--value' as string]: session.progressPct }}
                aria-hidden="true"
              >
                <span>{session.progressPct}%</span>
              </div>
              <div>
                <strong>
                  {session.completed} of {session.total}
                </strong>
                <span>cards completed</span>
              </div>
            </div>
            <div className="score-grid">
              <div className="score">
                <span className="score__icon score__icon--correct" aria-hidden="true">
                  ✓
                </span>
                <div>
                  <strong>{session.knowCount}</strong>
                  <span>Correct</span>
                </div>
              </div>
              <div className="score">
                <span className="score__icon score__icon--incorrect" aria-hidden="true">
                  ×
                </span>
                <div>
                  <strong>{session.dontKnowCount}</strong>
                  <span>Incorrect</span>
                </div>
              </div>
            </div>
          </section>

          <section className="panel related-panel">
            <p className="eyebrow">Related</p>
            <nav className="related-links" aria-label="Related pages">
              <a href={deck.lessonHref}>
                <em>{deck.verb}</em>
                <span>Verb of the Week lesson</span>
              </a>
              <a href="/en/learn-french/votw/">
                Verb of the Week
                <span>Series index</span>
              </a>
            </nav>
          </section>

          <section className="panel tip-panel">
            <div className="tip-heading">
              <span aria-hidden="true">⌁</span>
              <p className="eyebrow">Tip</p>
            </div>
            <p>Focus on accuracy, not speed. Review any cards you miss at the end.</p>
          </section>
        </aside>

        <section className="workspace">
          <header className="page-heading">
            <h1>
              Practice: <em>{deck.verb}</em>
            </h1>
            <p>Practice the conjugations and expressions from this week&apos;s verb.</p>
          </header>

          <nav className="tabs" aria-label="Practice sections">
            <button
              className={tab === 'flashcards' ? 'tab is-active' : 'tab'}
              type="button"
              onClick={() => setTab('flashcards')}
            >
              Flashcards
            </button>
            <button
              className={tab === 'about' ? 'tab is-active' : 'tab'}
              type="button"
              onClick={() => setTab('about')}
            >
              About this deck
            </button>
            <button
              className={tab === 'definition' ? 'tab is-active' : 'tab'}
              type="button"
              onClick={() => setTab('definition')}
            >
              Definition
            </button>
          </nav>

          {tab === 'flashcards' ? (
            <>
              {session.finished || !session.card ? (
                <section className="flashcard flashcard--done">
                  <div className="card-content">
                    <p className="card-kicker">Session complete</p>
                    <h2>Nice work</h2>
                    <p className="done-copy">
                      You graded {session.completed} of {session.total} cards this session. Progress
                      is not saved yet — refresh or leave and it resets.
                    </p>
                  </div>
                </section>
              ) : (
                <Flashcard
                  card={session.card}
                  index={session.index}
                  total={session.total}
                  face={session.face}
                  progressPct={session.progressPct}
                  onReveal={session.reveal}
                  onGrade={session.grade}
                  onBack={session.back}
                />
              )}

              <section className="session-summary">
                <div className="session-intro">
                  <span className="trophy" aria-hidden="true">
                    ⌁
                  </span>
                  <div>
                    <strong>Session progress</strong>
                    <span>
                      {session.completed} of {session.total} cards completed
                    </span>
                  </div>
                </div>
                <div className="session-score">
                  <div className="score">
                    <span className="score__icon score__icon--correct" aria-hidden="true">
                      ✓
                    </span>
                    <div>
                      <strong>{session.knowCount}</strong>
                      <span>Correct</span>
                    </div>
                  </div>
                  <div className="score">
                    <span className="score__icon score__icon--incorrect" aria-hidden="true">
                      ×
                    </span>
                    <div>
                      <strong>{session.dontKnowCount}</strong>
                      <span>Incorrect</span>
                    </div>
                  </div>
                </div>
                <button className="button button--sand-outline" type="button" disabled>
                  Review missed cards
                </button>
              </section>
            </>
          ) : null}

          {tab === 'about' ? (
            <section className="tab-panel">
              <h2>About this deck</h2>
              <p>
                Practice the conjugations and expressions featured in this week&apos;s Verb of the
                Week article.
              </p>
              <div className="deck-summary-grid">
                <div className="deck-summary-item">
                  <span className="round-icon round-icon--large" aria-hidden="true">
                    ◇
                  </span>
                  <div>
                    <strong>Conjugations ({conjugationCount})</strong>
                    <p>
                      Practice the forms of <em>{deck.verb}</em> for the subjects in this deck.
                    </p>
                  </div>
                </div>
                <div className="deck-summary-item">
                  <span className="round-icon round-icon--large" aria-hidden="true">
                    ●
                  </span>
                  <div>
                    <strong>Expressions ({expressionCount})</strong>
                    <p>Learn key expressions and their meanings.</p>
                  </div>
                </div>
              </div>
            </section>
          ) : null}

          {tab === 'definition' ? (
            <section className="tab-panel">
              <h2>
                <em>{deck.verb}</em>
              </h2>
              <p className="definition-level">{deck.level}</p>
              <p className="definition-gloss">{deck.gloss}</p>
            </section>
          ) : null}
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}
