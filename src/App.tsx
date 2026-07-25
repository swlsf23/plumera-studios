import { useEffect } from 'react';

/**
 * Placeholder shell for future interactive React apps.
 * Content pages are static HTML from the Python builder (`dist/`), not this SPA.
 */
export default function App() {
  useEffect(() => {
    try {
      window.location.replace('/en/');
    } catch (error) {
      // Can throw in sandboxed iframes; leave the user on a blank shell.
      console.error('Failed to redirect to landing:', error);
    }
  }, []);

  return null;
}
