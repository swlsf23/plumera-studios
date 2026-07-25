import type { ReactNode } from 'react';
import type { Locale } from '../../i18n/types';
import { SiteFooter } from './SiteFooter';
import { SiteHeader } from './SiteHeader';

type Props = {
  locale: Locale;
  active?: 'votd' | 'updates' | 'privacy';
  sidebar: ReactNode;
  children: ReactNode;
};

export function AppShell({ locale, active, sidebar, children }: Props) {
  return (
    <div id="top" className="app-shell">
      <SiteHeader locale={locale} active={active} />
      <main className="page-grid">
        <div className="content-column">{children}</div>
        {sidebar}
      </main>
      <SiteFooter locale={locale} />
    </div>
  );
}
