import { chrome } from '../../i18n/chrome';
import type { Locale } from '../../i18n/types';

export type TocSection = {
  id: string;
  label: string;
};

type Props = {
  locale: Locale;
  sections: TocSection[];
  activeSection: string;
};

export function OnThisPageNav({ locale, sections, activeSection }: Props) {
  const copy = chrome[locale];

  return (
    <div className="sidebar-block">
      <h2>{copy.onThisPage}</h2>
      <nav className="toc" aria-label={copy.onThisPage}>
        {sections.map((section) => (
          <a
            key={section.id}
            className={activeSection === section.id ? 'active' : ''}
            href={`#${section.id}`}
          >
            {section.label}
          </a>
        ))}
      </nav>
    </div>
  );
}
