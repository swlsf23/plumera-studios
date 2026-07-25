export const SITE_ORIGIN = 'https://plumerastudios.com';

/** Build an absolute production URL from a site path (e.g. `/en/privacy.html`). */
export function absoluteUrl(path: string) {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return `${SITE_ORIGIN}${normalized}`;
}
