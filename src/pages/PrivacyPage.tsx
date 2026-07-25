import { useMemo } from 'react';
import { AppShell } from '../components/layout/AppShell';
import { PageSidebar } from '../components/layout/PageSidebar';
import { useActiveSection } from '../hooks/useActiveSection';
import { useDocumentMeta } from '../hooks/useDocumentMeta';
import { privacy, type PrivacyBlock } from '../i18n/privacy';
import type { Locale } from '../i18n/types';
import { privacyPath } from '../lib/paths';

type Props = {
  locale: Locale;
};

function renderBlock(block: PrivacyBlock, index: number) {
  if (block.type === 'p') {
    const email = 'hello@plumerastudios.com';
    if (block.text.includes(email)) {
      const [before, after] = block.text.split(email);
      return (
        <p key={index}>
          {before}
          <a href={`mailto:${email}`}>{email}</a>
          {after}
        </p>
      );
    }
    return <p key={index}>{block.text}</p>;
  }

  if (block.type === 'h3') {
    return <h3 key={index}>{block.text}</h3>;
  }

  return (
    <ul key={index} className="plain-list">
      {block.items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

export function PrivacyPage({ locale }: Props) {
  const copy = privacy[locale];
  useDocumentMeta(locale, copy.title, copy.metaDescription, privacyPath(locale));

  const sections = useMemo(
    () => copy.sections.map((section) => ({ id: section.id, label: section.title })),
    [copy.sections],
  );
  const activeSection = useActiveSection(sections.map((section) => section.id));

  return (
    <AppShell
      locale={locale}
      active="privacy"
      sidebar={<PageSidebar locale={locale} sections={sections} activeSection={activeSection} />}
    >
      <header className="article-header">
        <p className="eyebrow">{copy.eyebrow}</p>
        <h1>{copy.heading}</h1>
        <p className="dek">{copy.summary}</p>
        <p className="meta-line">{copy.effectiveDate}</p>
      </header>

      <article className="article-body legal-body">
        {copy.sections.map((section) => (
          <section key={section.id} id={section.id} className="article-section">
            <h2>{section.title}</h2>
            {section.blocks.map(renderBlock)}
          </section>
        ))}
      </article>
    </AppShell>
  );
}
