import { useMemo } from 'react';
import { Link, useParams } from 'react-router-dom';
import ContentHeader from '../components/ContentHeader';
import Flashcard from '../components/Flashcard';
import SiteFooter from '../components/SiteFooter';
import { getDeck } from '../practice/loadDeck';
import { useStudySession } from '../practice/useStudySession';
import type { Deck } from '../practice/types';

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

  return <PracticeSession key={deck.verb} deck={deck} />;
}

function PracticeSession({ deck }: { deck: Deck }) {
  const session = useStudySession(deck, { enabled: true });
  const conjugationCount = deck.cards.filter((c) => c.type === 'conjugation').length;
  const expressionCount = deck.cards.filter((c) => c.type === 'expression').length;
  const related = deck.related?.length
    ? deck.related
    : [
        {
          href: deck.lessonHref,
          title: deck.verb,
          meta: 'Verb of the Week lesson',
        },
      ];
  const about =
    deck.about ??
    "Practice the conjugations and expressions featured in this week's Verb of the Week article.";

  return (
    <div className="page practice-app">
      <ContentHeader />

      <main className="practice-shell">
        <section className="workspace">
          <header className="page-heading">
            <div className="page-heading__meta">
              <p className="page-heading__eyebrow">Practice</p>
              {deck.level ? (
                <span className="page-heading__level">
                  <span className="page-heading__level-prefix">Level</span>
                  <a className="page-heading__level-badge" href="/en/cefr/">
                    {deck.level}
                  </a>
                </span>
              ) : null}
            </div>
            <h1>
              <em>{deck.verb}</em>
            </h1>
            <p className="page-summary">
              Browse the deck with the arrow keys. Know / don&apos;t know comes next.
            </p>
          </header>

          {session.card ? (
            <Flashcard
              card={session.card}
              index={session.index}
              total={session.total}
              face={session.face}
              mode={session.mode}
              pass={session.pass}
              showingLang={session.showingLang}
              promptText={session.promptText}
              answerText={session.answerText}
              progressPct={session.progressPct}
              canPrev={session.canPrev}
              canNext={session.canNext}
              onPrev={session.prevCard}
              onNext={session.nextCard}
              onFlipUp={session.flipUp}
              onFlipDown={session.flipDown}
              onModeChange={session.setStudyMode}
            />
          ) : null}
        </section>

        <aside className="sidebar">
          <section className="panel definition-panel">
            <p className="eyebrow">Definition</p>
            <p className="sidebar-verb">
              <em>{deck.verb}</em>
            </p>
            <p className="sidebar-level">{deck.level}</p>
            <p className="sidebar-gloss">{deck.gloss}</p>
          </section>

          <section className="panel about-panel">
            <p className="eyebrow">About this deck</p>
            <p className="sidebar-about">{about}</p>
            <ul className="sidebar-deck-stats">
              <li>
                <strong>{conjugationCount}</strong>
                <span>conjugations</span>
              </li>
              <li>
                <strong>{expressionCount}</strong>
                <span>expressions</span>
              </li>
            </ul>
          </section>

          <section className="panel progress-panel">
            <p className="eyebrow">Deck position</p>
            <div className="progress-overview progress-overview--solo">
              <div
                className="progress-ring"
                style={{ ['--value' as string]: session.progressPct }}
                aria-hidden="true"
              >
                <span>{session.progressPct}%</span>
              </div>
              <div>
                <strong>
                  {session.index + 1} of {session.total}
                </strong>
                <span>current card</span>
              </div>
            </div>
          </section>

          <section className="panel related-panel">
            <p className="eyebrow">Related</p>
            <nav className="related-links" aria-label="Related pages">
              {related.map((item) => (
                <a key={item.href} href={item.href}>
                  {item.title === deck.verb ? <em>{item.title}</em> : item.title}
                  {item.meta ? <span>{item.meta}</span> : null}
                </a>
              ))}
            </nav>
          </section>
        </aside>
      </main>

      <SiteFooter />
    </div>
  );
}
