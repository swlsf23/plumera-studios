import { Link } from 'react-router-dom';
import { chrome } from '../../i18n/chrome';
import type { Locale } from '../../i18n/types';
import { landingPath, privacyPath, updatesPath, votdPath } from '../../lib/paths';
import { LanguageSelector } from './LanguageSelector';
import { PlumeraMark } from './PlumeraMark';

type Props = {
  locale: Locale;
};

export function SiteFooter({ locale }: Props) {
  const copy = chrome[locale];

  return (
    <footer className="site-footer">
      <div className="footer-brand">
        <a href={landingPath(locale)} aria-label={copy.brandHome}>
          <PlumeraMark compact />
        </a>
        <p>
          {copy.tagline.split('\n').map((line) => (
            <span key={line}>
              {line}
              <br />
            </span>
          ))}
        </p>
      </div>

      <div className="footer-column">
        <h3>{copy.explore}</h3>
        <a href={landingPath(locale)}>{copy.home}</a>
        <Link to={votdPath(locale)}>{copy.votd}</Link>
        <Link to={updatesPath(locale)}>{copy.updates}</Link>
        <Link to={privacyPath(locale)}>{copy.privacy}</Link>
      </div>

      <div className="footer-column">
        <h3>{copy.connect}</h3>
        <Link to={updatesPath(locale)}>{copy.newsletter}</Link>
        <a href="mailto:hello@plumerastudios.com">hello@plumerastudios.com</a>
        <LanguageSelector locale={locale} placement="footer" />
      </div>

      <div className="footer-column footer-column--copy">
        <p>{copy.copyright}</p>
      </div>
    </footer>
  );
}
