import { useEffect, useRef } from 'react';
import headerHtml from '../generated/content-header.html?raw';

/**
 * Renders the shared site header from src/generated/content-header.html
 * (emitted by python -m tools.content_builder from partials/content_header.html).
 */
export default function ContentHeader() {
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = wrapRef.current;
    if (!root) return;
    const btn = root.querySelector<HTMLButtonElement>('[data-menu-toggle]');
    const nav = root.querySelector<HTMLElement>('[data-mobile-nav]');
    if (!btn || !nav) return;

    const openIcon =
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"></path></svg>';
    const closeIcon =
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"></path></svg>';

    const onClick = () => {
      const open = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.innerHTML = open ? closeIcon : openIcon;
    };

    btn.addEventListener('click', onClick);
    return () => btn.removeEventListener('click', onClick);
  }, []);

  return (
    <div
      ref={wrapRef}
      className="content-header-root"
      dangerouslySetInnerHTML={{ __html: headerHtml }}
    />
  );
}
