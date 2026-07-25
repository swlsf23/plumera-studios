import type { Locale } from '../i18n/types';

export function landingPath(locale: Locale) {
  return `/${locale}/index.html`;
}

export function updatesPath(locale: Locale) {
  return `/${locale}/updates.html`;
}

export function privacyPath(locale: Locale) {
  return `/${locale}/privacy.html`;
}

export function votdPath(locale: Locale, slug = 'thoughtful-content') {
  return `/${locale}/votd/${slug}`;
}
