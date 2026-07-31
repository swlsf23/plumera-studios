import { useMemo } from 'react';
import { Link, useParams } from 'react-router-dom';
import Flashcard from '../components/Flashcard';
import SiteFooter from '../components/SiteFooter';
import { getDeck } from '../practice/loadDeck';
import { resolveAudioUrl } from '../practice/resolveAudioUrl';
import { useStudySession } from '../practice/useStudySession';
import type { Deck } from '../practice/types';

export default function PracticePage() {
  const { verb = '' } = useParams();
  const deck = useMemo(() => getDeck(verb), [verb]);

  if (!deck) {
    return (
      <>
        <main className="page-grid page-grid--lesson">
          <div className="content-column practice-missing">
            <h1>Deck not found</h1>
            <p>
              No flashcard deck for <em>{verb || 'unknown'}</em> yet.
            </p>
            <Link to="/prendre/">Practice prendre</Link>
          </div>
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
      <main className="page-grid page-grid--lesson">
        <div className="content-column practice-shell">
          <header className="page-heading article-header">
            <div className="page-heading__meta article-header__meta-row">
              <p className="page-heading__eyebrow">Practice</p>
              {deck.level ? (
                <span className="page-heading__level article-level">
                  <span className="page-heading__level-prefix article-level__prefix">
                    Level
                  </span>
                  <a className="page-heading__level-badge article-level__badge" href="/en/cefr/">
                    {deck.level}
                  </a>
                </span>
              ) : null}
            </div>
            <h1>
              <em>{deck.verb}</em>
            </h1>
            {deck.description ? (
              <p className="page-summary">{deck.description}</p>
            ) : null}
          </header>

          <Flashcard
            card={session.card}
            face={session.face}
            mode={session.mode}
            pass={session.pass}
            showingLang={session.showingLang}
            promptText={session.promptText}
            answerText={session.answerText}
            done={session.done}
            cleared={session.cleared}
            remaining={session.remaining}
            sessionGoal={session.sessionGoal}
            knowPct={session.knowPct}
            queuePct={session.queuePct}
            canPrev={session.canPrev}
            canNext={session.canNext}
            onPrev={session.prevCard}
            onNext={session.nextCard}
            onKnow={session.markKnow}
            onDontKnow={session.markDontKnow}
            onRestart={session.restartSession}
            onModeChange={session.setStudyMode}
            audioUrl={resolveAudioUrl(session.card?.audio, deck.locale, deck.target)}
            onPlayedAudio={() =>
              session.trackPlayedAudio(
                resolveAudioUrl(session.card?.audio, deck.locale, deck.target),
              )
            }
          />

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
        </div>
      </main>

      <SiteFooter />
    </>
  );
}
