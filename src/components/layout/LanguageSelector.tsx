import { LOCALES, type Locale } from '../../i18n/types';
import { chrome } from '../../i18n/chrome';
import { landingPath } from '../../lib/paths';

const labels: Record<Locale, string> = {
  en: 'English',
  es: 'Español',
  fr: 'Français',
};

type Props = {
  locale: Locale;
  placement?: 'header' | 'footer';
};

export function LanguageSelector({ locale, placement = 'footer' }: Props) {
  const copy = chrome[locale];

  return (
    <details className={`language-selector language-selector--${placement}`}>
      <summary aria-label={copy.chooseLanguage} title={copy.chooseLanguage}>
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <circle cx="12" cy="12" r="9" />
          <path d="M3 12h18" />
          <path d="M12 3a14 14 0 0 1 0 18" />
          <path d="M12 3a14 14 0 0 0 0 18" />
        </svg>
      </summary>
      <nav className="language-menu" aria-label={copy.languages}>
        {LOCALES.map((item) => (
          <a
            key={item}
            href={landingPath(item)}
            lang={item}
            hrefLang={item}
            aria-current={item === locale ? 'true' : undefined}
          >
            {labels[item]}
          </a>
        ))}
      </nav>
    </details>
  );
}
