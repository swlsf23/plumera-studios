import { useEffect, useRef } from 'react';

/**
 * Same EN markup as public landings / content_page.html content-header.
 * Styles: /css/base.css + /css/content-header.css (loaded in index.html).
 */
export default function ContentHeader() {
  const btnRef = useRef<HTMLButtonElement>(null);
  const navRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const btn = btnRef.current;
    const nav = navRef.current;
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
    <header className="content-header">
      <a href="/en/" className="content-header__brand" aria-label="Plumera Studios home">
        Plumera Studios
      </a>

      <nav className="content-header__nav" aria-label="Primary navigation">
        <a href="/en/learn-french/votw/">Verb of the Week</a>
        <a href="/en/learn-french/whats-new/">What&apos;s new</a>
        <a href="/en/privacy/">Privacy</a>
        <details className="content-header__lang">
          <summary aria-label="Choose language" title="Choose language">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
              <circle cx="12" cy="12" r="9"></circle>
              <path d="M3 12h18"></path>
              <path d="M12 3a14 14 0 0 1 0 18"></path>
              <path d="M12 3a14 14 0 0 0 0 18"></path>
            </svg>
          </summary>
          <nav className="content-header__lang-menu" aria-label="Languages">
            <a href="/en/" lang="en" aria-current="true">
              English
            </a>
            <a href="/es/" lang="es">
              Español
            </a>
            <a href="/fr/" lang="fr">
              Français
            </a>
          </nav>
        </details>
      </nav>

      <div className="content-header__actions">
        <a
          className="content-header__subscribe"
          href="/en/contact/"
          title="Verb of the Week by email"
        >
          Subscribe
        </a>
        <button
          ref={btnRef}
          className="content-header__menu"
          type="button"
          aria-label="Menu"
          aria-expanded="false"
          data-menu-toggle
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 7h16M4 12h16M4 17h16"></path>
          </svg>
        </button>
      </div>

      <nav
        ref={navRef}
        className="content-header__mobile"
        aria-label="Mobile navigation"
        data-mobile-nav
      >
        <a href="/en/learn-french/votw/">Verb of the Week</a>
        <a href="/en/learn-french/whats-new/">What&apos;s new</a>
        <a href="/en/privacy/">Privacy</a>
        <a href="/en/" lang="en" aria-current="true">
          English
        </a>
        <a href="/es/" lang="es">
          Español
        </a>
        <a href="/fr/" lang="fr">
          Français
        </a>
      </nav>
    </header>
  );
}
