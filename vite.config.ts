import { cpSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { defineConfig, type Plugin, type Connect } from 'vite';
import react from '@vitejs/plugin-react';

/** Verbs that get a static directory shell so refresh works without SPA fallback. */
const VERB_SHELLS = ['prendre'] as const;

const HEADER_MARKER = '<!-- CONTENT_HEADER -->';
const GENERATED_HEADER = resolve(__dirname, 'src/generated/content-header.html');
const PUBLIC_DIR = resolve(__dirname, 'public');

/**
 * Inject the builder-emitted header fragment into the app HTML shell.
 * Source of truth remains partials/content_header.html (via --app-header-only / site build).
 */
function injectContentHeader(): Plugin {
  return {
    name: 'inject-content-header',
    transformIndexHtml: {
      order: 'pre',
      handler(html) {
        if (!html.includes(HEADER_MARKER)) return html;
        if (!existsSync(GENERATED_HEADER)) {
          throw new Error(
            `Missing ${GENERATED_HEADER}. Run: python3 -m tools.content_builder --app-header-only`,
          );
        }
        const header = readFileSync(GENERATED_HEADER, 'utf8').trim();
        return html.replace(HEADER_MARKER, header);
      },
    },
  };
}

/**
 * Keep site chrome at domain root (/css, /js). Vite's `base` would otherwise rewrite
 * those absolute URLs to /app/flashcard/css/... which does not exist.
 */
function keepSiteChromeRootPaths(): Plugin {
  return {
    name: 'keep-site-chrome-root-paths',
    transformIndexHtml: {
      order: 'post',
      handler(html) {
        return html
          .replaceAll('/app/flashcard/css/', '/css/')
          .replaceAll('/app/flashcard/js/', '/js/');
      },
    },
  };
}

/** For `npm run dev:app`, serve /css and /js from public/ like the static site. */
function serveSiteChrome(): Plugin {
  return {
    name: 'serve-site-chrome',
    configureServer(server) {
      const chrome: Connect.NextHandleFunction = (req, res, next) => {
        const url = req.url ?? '';
        if (!url.startsWith('/css/') && !url.startsWith('/js/')) {
          next();
          return;
        }
        const pathOnly = url.split('?')[0] ?? url;
        const file = resolve(PUBLIC_DIR, pathOnly.slice(1));
        if (!file.startsWith(PUBLIC_DIR) || !existsSync(file)) {
          next();
          return;
        }
        try {
          const body = readFileSync(file);
          if (file.endsWith('.css')) res.setHeader('Content-Type', 'text/css; charset=utf-8');
          else if (file.endsWith('.js'))
            res.setHeader('Content-Type', 'text/javascript; charset=utf-8');
          res.end(body);
        } catch {
          next();
        }
      };
      server.middlewares.use(chrome);
    },
  };
}

export default defineConfig({
  base: '/app/flashcard/',
  plugins: [
    react(),
    injectContentHeader(),
    keepSiteChromeRootPaths(),
    serveSiteChrome(),
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
