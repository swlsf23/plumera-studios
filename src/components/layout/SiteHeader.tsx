import { Menu, Search, X } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { chrome } from '../../i18n/chrome';
import type { Locale } from '../../i18n/types';
import { landingPath, privacyPath, updatesPath, votdPath } from '../../lib/paths';
import { LanguageSelector } from './LanguageSelector';
import { PlumeraMark } from './PlumeraMark';

type Props = {
  locale: Locale;
  active?: 'votd' | 'updates' | 'privacy';
};

export function SiteHeader({ locale, active }: Props) {
  const [open, setOpen] = useState(false);
  const copy = chrome[locale];

  const links = [
    { key: 'home' as const, label: copy.home, href: landingPath(locale), external: true },
    { key: 'votd' as const, label: copy.votd, href: votdPath(locale), external: false },
    { key: 'updates' as const, label: copy.updates, href: updatesPath(locale), external: false },
    { key: 'privacy' as const, label: copy.privacy, href: privacyPath(locale), external: false },
  ];

  return (
    <header className="site-header">
      <a href={landingPath(locale)} className="brand-link" aria-label={copy.brandHome}>
        <PlumeraMark />
      </a>

      <nav className="desktop-nav" aria-label="Primary navigation">
        {links.map((link) =>
          link.external ? (
            <a key={link.key} href={link.href}>
              {link.label}
            </a>
          ) : (
            <Link key={link.key} className={active === link.key ? 'active' : ''} to={link.href}>
              {link.label}
            </Link>
          ),
        )}
      </nav>

      <div className="header-actions">
        <LanguageSelector locale={locale} placement="header" />
        <button className="icon-button" aria-label={copy.search} type="button">
          <Search size={21} strokeWidth={1.7} />
        </button>
        <Link className="outline-button" to={updatesPath(locale)}>
          {copy.subscribe}
        </Link>
        <button
          className="menu-button"
          aria-label={copy.toggleNav}
          aria-expanded={open}
          type="button"
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {open && (
        <nav className="mobile-nav" aria-label="Mobile navigation">
          {links.map((link) =>
            link.external ? (
              <a key={link.key} href={link.href} onClick={() => setOpen(false)}>
                {link.label}
              </a>
            ) : (
              <Link
                key={link.key}
                className={active === link.key ? 'active' : ''}
                to={link.href}
                onClick={() => setOpen(false)}
              >
                {link.label}
              </Link>
            ),
          )}
        </nav>
      )}
    </header>
  );
}
