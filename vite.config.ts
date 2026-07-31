import { appendFileSync, cpSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { defineConfig, type Plugin, type Connect } from 'vite';
import react from '@vitejs/plugin-react';

/** Verbs that get a static directory shell so refresh works without SPA fallback. */
const VERB_SHELLS = ['prendre'] as const;

const HEADER_MARKER = '<!-- CONTENT_HEADER -->';
const GENERATED_HEADER = resolve(__dirname, 'src/generated/content-header.html');
const PUBLIC_DIR = resolve(__dirname, 'public');
const DATA_DIR = resolve(__dirname, 'data');
const LOCAL_EVENTS_FILE = resolve(__dirname, 'tmp/study-events.jsonl');

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

/** For `npm run dev:app`, serve site chrome + dataset audio from disk (no copies). */
function serveSiteChrome(): Plugin {
  return {
    name: 'serve-site-chrome',
    configureServer(server) {
      const chrome: Connect.NextHandleFunction = (req, res, next) => {
        const url = req.url ?? '';
        const pathOnly = url.split('?')[0] ?? url;

        if (pathOnly.startsWith('/css/') || pathOnly.startsWith('/js/')) {
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
          return;
        }

        if (pathOnly.startsWith('/data/') && pathOnly.endsWith('.mp3')) {
          const file = resolve(DATA_DIR, pathOnly.slice('/data/'.length));
          if (!file.startsWith(DATA_DIR) || !existsSync(file)) {
            next();
            return;
          }
          try {
            res.setHeader('Content-Type', 'audio/mpeg');
            res.end(readFileSync(file));
          } catch {
            next();
          }
          return;
        }

        next();
      };
      server.middlewares.use(chrome);

      server.middlewares.use((req, res, next) => {
        const pathOnly = (req.url ?? '').split('?')[0] ?? '';
        if (pathOnly !== '/__local/study-events') {
          next();
          return;
        }
        if (req.method === 'OPTIONS') {
          res.statusCode = 204;
          res.setHeader('Access-Control-Allow-Origin', '*');
          res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
          res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
          res.end();
          return;
        }
        if (req.method !== 'POST') {
          next();
          return;
        }
        const chunks: Buffer[] = [];
        req.on('data', (chunk) => chunks.push(Buffer.from(chunk)));
        req.on('end', () => {
          try {
            const raw = Buffer.concat(chunks).toString('utf8') || '{}';
            JSON.parse(raw);
            mkdirSync(resolve(__dirname, 'tmp'), { recursive: true });
            appendFileSync(LOCAL_EVENTS_FILE, `${raw.trim()}\n`, 'utf8');
            res.statusCode = 204;
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.end();
          } catch {
            res.statusCode = 400;
            res.end('Invalid JSON');
          }
        });
      });
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
