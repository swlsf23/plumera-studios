import { Link } from 'react-router-dom';
import { relatedVotd } from '../../data/related';
import { socialLinks } from '../../data/social';
import { chrome } from '../../i18n/chrome';
import type { Locale } from '../../i18n/types';
import { votdPath } from '../../lib/paths';
import { OnThisPageNav, type TocSection } from './OnThisPageNav';

type Props = {
  locale: Locale;
  sections: TocSection[];
  activeSection: string;
};

export function PageSidebar({ locale, sections, activeSection }: Props) {
  const copy = chrome[locale];

  return (
    <aside className="sidebar">
      <OnThisPageNav locale={locale} sections={sections} activeSection={activeSection} />

      <div className="sidebar-block related-block">
        <h2>{copy.relatedVotd}</h2>
        <div className="mini-card-list">
          {relatedVotd.map((item) => (
            <Link key={item.title} to={votdPath(locale)} className="mini-card">
              <h3>{item.title}</h3>
              <p>{item.date} · {item.read}</p>
            </Link>
          ))}
        </div>
      </div>

      <div id="newsletter" className="sidebar-block newsletter-block">
        <h2>{copy.followUs}</h2>
        <nav className="social-links" aria-label={copy.followUs}>
          {socialLinks.map((item) => (
            <a
              key={item.id}
              href={item.href}
              target="_blank"
              rel="noopener noreferrer"
            >
              {item.label}
            </a>
          ))}
        </nav>
      </div>
    </aside>
  );
}
