import { useEffect } from 'react';
import type { Locale } from '../i18n/types';
import { absoluteUrl } from '../lib/site';

export function useDocumentMeta(
  locale: Locale,
  title: string,
  description: string,
  canonicalPath: string,
) {
  useEffect(() => {
    document.title = title;
    document.documentElement.lang = locale;

    let meta = document.querySelector('meta[name="description"]');
    if (!meta) {
      meta = document.createElement('meta');
      meta.setAttribute('name', 'description');
      document.head.appendChild(meta);
    }
    meta.setAttribute('content', description);

    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      document.head.appendChild(canonical);
    }
    canonical.setAttribute('href', absoluteUrl(canonicalPath));
  }, [locale, title, description, canonicalPath]);
}
