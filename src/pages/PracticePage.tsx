import { useMemo } from 'react';
import { Link, useParams } from 'react-router-dom';
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
      <>
        <main className="practice-missing">
          <h1>Deck not found</h1>
          <p>
            No flashcard deck for <em>{verb || 'unknown'}</em> yet.
          </p>
          <Link to="/prendre/">Practice prendre</Link>
        </main>
        <SiteFooter />
      </>
    );
  }

  return <PracticeSession key={deck.verb} deck={deck} />;
}

function PracticeSession({ deck }: { deck: Deck }) {
  const session = useStudySession(deck, { enabled: true });
  const related = deck.related?.length
    ? deck.related
    : [
        {
          href: deck.lessonHref,
          title: deck.verb,
          meta: 'Verb of the Week lesson',
        },
      ];

  return (
    <>
      <main className="practice-shell">
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

        <section className="related-band">
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
      </main>

      <SiteFooter />
    </>
  );
}
