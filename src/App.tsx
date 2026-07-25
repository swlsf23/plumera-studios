/**
 * Placeholder shell for future interactive React apps.
 * Content pages are static HTML from the Python builder (`dist/`), not this SPA.
 */
export default function App() {
  if (typeof window !== 'undefined') {
    window.location.replace('/en/index.html');
  }
  return null;
}
