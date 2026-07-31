/**
 * Retired. The site header is injected into the flashcard HTML shell
 * (`index.html` ← `partials/content_header.html`) — same path as content/landings.
 * Do not render a React header.
 */
export default function ContentHeader(): never {
  throw new Error(
    'ContentHeader removed: use the builder-injected header in index.html.',
  );
}
