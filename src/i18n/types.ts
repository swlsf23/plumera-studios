export type Locale = 'en' | 'es' | 'fr';

export const LOCALES: Locale[] = ['en', 'es', 'fr'];

export function isLocale(value: string | undefined): value is Locale {
  return value === 'en' || value === 'es' || value === 'fr';
}
