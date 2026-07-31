import { cpSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/** Verbs that get a static directory shell so refresh works without SPA fallback. */
const VERB_SHELLS = ['tenir'] as const;

export default defineConfig({
  base: '/app/flashcard/',
  plugins: [
    react(),
    {
      name: 'flashcard-verb-shells',
      closeBundle() {
        const out = resolve(__dirname, 'dist/app/flashcard');
        for (const verb of VERB_SHELLS) {
          const dir = resolve(out, verb);
          mkdirSync(dir, { recursive: true });
          cpSync(resolve(out, 'index.html'), resolve(dir, 'index.html'));
        }
      },
    },
  ],
  build: {
    outDir: 'dist/app/flashcard',
    emptyOutDir: true,
    // Site CSS/assets already live at dist/ root from the content builder.
    copyPublicDir: false,
  },
});
