import { Mail } from 'lucide-react';
import { useMemo } from 'react';
import { AppShell } from '../components/layout/AppShell';
import { PageSidebar } from '../components/layout/PageSidebar';
import { useActiveSection } from '../hooks/useActiveSection';
import { useDocumentMeta } from '../hooks/useDocumentMeta';
import { updates } from '../i18n/updates';
import type { Locale } from '../i18n/types';
import { updatesPath } from '../lib/paths';

type Props = {
  locale: Locale;
};

export function UpdatesPage({ locale }: Props) {
  const copy = updates[locale];
  useDocumentMeta(locale, copy.title, copy.metaDescription, updatesPath(locale));

  const sections = useMemo(
    () => [
      { id: 'signup', label: copy.signupTitle },
      { id: 'receive', label: copy.receiveTitle },
      { id: 'promise', label: copy.promiseTitle },
    ],
    [copy.promiseTitle, copy.receiveTitle, copy.signupTitle],
  );
  const activeSection = useActiveSection(sections.map((section) => section.id));

  return (
    <AppShell
      locale={locale}
      active="updates"
      sidebar={<PageSidebar locale={locale} sections={sections} activeSection={activeSection} />}
    >
      <header className="article-header">
        <p className="eyebrow">{copy.eyebrow}</p>
        <h1>
          {copy.heading}
          <br />
          {copy.headingAccent}
        </h1>
        <p className="dek">{copy.intro}</p>
      </header>

      <div className="simple-panels">
        <article id="signup" className="content-panel">
          <div className="content-panel__icon" aria-hidden="true">
            <Mail size={25} strokeWidth={1.55} />
          </div>
          <h2>{copy.signupTitle}</h2>
          <p>
            {copy.signupBeforeSubject} <strong>{copy.signupSubject}</strong> {copy.signupAfterSubject}
          </p>
          <p className="email-address" aria-label={copy.emailAria}>
            hello <span>[{copy.emailAt}]</span> plumerastudios <span>[{copy.emailDot}]</span> com
          </p>
          <p>{copy.signupNote}</p>
        </article>

        <article id="receive" className="content-panel">
          <h2>{copy.receiveTitle}</h2>
          <ul className="plain-list">
            {copy.receiveItems.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article id="promise" className="content-panel">
          <h2>{copy.promiseTitle}</h2>
          {copy.promiseBody.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </article>
      </div>
    </AppShell>
  );
}
