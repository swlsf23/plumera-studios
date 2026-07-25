/**
 * Placeholder shell for future interactive React apps.
 * Content pages are static HTML from the Python builder (`dist/`), not this SPA.
 */
export default function App() {
  if (typeof window !== 'undefined') {
    try {
      window.location.replace('/en/index.html');
    } catch (error) {
      console.error('Failed to redirect to landing:', error);
    }
  }
  return null;
}
