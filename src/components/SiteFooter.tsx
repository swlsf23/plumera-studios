/**
 * Same EN markup as tools/content_builder/templates/content_page.html site-footer.
 * Styles: /css/base.css (.site-footer).
 */
export default function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="footer-primary">
        <details className="language-selector language-selector--footer">
          <summary aria-label="Choose language" title="Choose language">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
              <circle cx="12" cy="12" r="9"></circle>
              <path d="M3 12h18"></path>
              <path d="M12 3a14 14 0 0 1 0 18"></path>
              <path d="M12 3a14 14 0 0 0 0 18"></path>
            </svg>
          </summary>
          <nav className="language-menu" aria-label="Choose language">
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
        <div className="footer-links">
          <a className="footer-link" href="/en/contact/">
            Contact
          </a>
          <a className="footer-link" href="/en/privacy/">
            Privacy
          </a>
        </div>
      </div>
      <p className="footer-copy">© 2026 Plumera Studios</p>
    </footer>
  );
}
