# Plumera site CSS

Runtime stylesheets for the static site under `public/css/`. Snapshots in `docs/snapshots/` are archival only — not source of truth and not served.

## Architecture (current)

Four runtime files. Do not add more without a strong reason.

| File | Owns |
| --- | --- |
| `base.css` | Design tokens (`:root`), reset, `.page` shell, shared footer / language selector, `.content-header`, domain-root (`.root-page`) |
| `content.css` | Content pages from the Python builder (`.content-page*`) |
| `landing.css` | Classic FR/ES locale landings (`.landing-classic`) |
| `landing-home.css` | English locale home (`.landing-home`) |

### Hard import order (sources)

1. `base.css` first  
2. At most one page sheet second  

Never author a page sheet that assumes it loads before `base.css`.

### What the browser loads

The builder concatenates sources into **one** stylesheet per surface in `dist/css/`:

| Surface | Live link | Sources |
| --- | --- | --- |
| Domain root `/` | `site-root.css` | `base.css` |
| EN home | `site-landing-home.css` | `base.css` + `landing-home.css` |
| FR / ES home | `site-landing.css` | `base.css` + `landing.css` |
| Content pages | `site-content.css` | `base.css` + `content.css` |

UI type is self-hosted Inter (`public/fonts/InterVariable.woff2`), registered as CSS family **`Plumera Sans`** (not `Inter`) so extension `@font-face` rules named Inter cannot hijack the stack. Metric-matched `Plumera Sans Fallback` (local Arial + size-adjust) and `@font-face` live in the inline `<head>` only — not repeated in `base.css`. `font-display: swap`. No font preload. No Google Fonts on live pages. Font URL carries `?v=` (bump with the file); see `docs/deploy.md` for Cache-Control.

Bump `?v=` on every live CSS link you change in the same commit so caches do not mix old and new sheets.

### `base.css` section order

Keep this order; do not interleave:

1. Tokens / reset / shell (`:root`, `*`, `html`, `body`, `.page`, `.content-column`)
2. Shared footer + language selector (and their media queries)
3. Content header (and its media queries)
4. Root page (`.root-page` and descendants; and their media queries)

### Page-root scoping

Page sheets must not use bare element selectors. Rules live under a page root class:

- `.content-page` — builder content pages  
- `.landing-classic` — classic FR/ES landings  
- `.landing-home` — EN home  
- `.root-page` — domain root locale cards (in `base.css`)

Prefer descendant selectors (`.content-page .page-grid`), not child combinators, unless a child combinator is required for correctness.

### Tokens today

**Global semantic palette** — only in `base.css` `:root`:

`--paper`, `--paper-deep`, `--ink`, `--ink-deep`, `--blue`, `--blue-deep`, `--green`, `--sand`, `--sand-soft`, `--muted`, `--surround`, `--line-mid`, `--line-on-dark`, `--icon-light`, plus layout/type: `--max`, `--content-max`, `--page-gutter`, `--page-top`, `--body-size`, `--body-leading`.

**Existing page-root overrides** (intentional themes; not locale skins):

- `.content-page` — content wash / ink / accent deltas  
- `.content-header` — `--blue-soft`, `--line` (and any header-local needs)  
- `.root-page` — `--muted`, `--line`, `--accent`  
- `.landing-home` — parallel `--landing-*` palette (debt; see limitations below)  
- `.landing-classic` — `--hero-spread` (layout behavior, not color)

Chrome and page sheets should consume `var(--…)` semantic tokens so a `:root` edit can retheme the default site.

## How to create a new skin

Skins are **CSS variable reassignment only**. No new layout rules, no new stylesheets, no forked page sheets per locale.

You are not required to ship skins with the architecture refactor; follow this recipe when you do.

### 1. Choose scope

| Goal | Where to set variables |
| --- | --- |
| Whole site default | `:root` in `base.css` |
| UI locale (EN / FR / ES / PT…) | `html[data-locale="{locale}"]` |
| Content language (target) | `.page[data-target="{target-slug}"]` |
| Target under one locale | `html[data-locale="{locale}"] .page[data-target="{target-slug}"]` |

Target slug matches the content folder (e.g. `learn-french`, `apprendre-anglais`).

### 2. Add markup hooks

Wire attributes where pages are authored or emitted (follow-up work if not present yet):

- **Landings** — `data-locale` on `<html>`; `data-target` on `.page` when the landing is about a taught language  
- **Content pages** — builder sets `data-locale` from the page locale and `data-target` from the target folder / frontmatter  
- **Domain root `/`** — locale entry only; omit `data-target` (or leave unset)

Example:

```html
<html lang="fr" data-locale="fr">
  …
  <div class="page content-page …" data-target="apprendre-anglais">
```

### 3. Add the skin block in `base.css`

Place locale/target skin blocks **immediately after `:root`** so one file remains the palette control surface.

```css
/* Locale skin: French UI */
html[data-locale="fr"] {
  --ink: #143b38;
  --paper: #f5f0e6;
  --sand: #b8954f;
  --blue: #a8bbc2;
  /* Reassign only semantic color tokens you need to change */
}

/* Target skin: learn-english under any locale */
.page[data-target="apprendre-anglais"] {
  --accent: #a67c2d;
}

/* Combined: English UI + learn-french target */
html[data-locale="en"] .page[data-target="learn-french"] {
  --blue: #6f8992;
}
```

### 4. Token checklist

When authoring a skin, consider these semantic color tokens from `:root`:

- `--paper`, `--paper-deep`
- `--ink`, `--ink-deep`
- `--blue`, `--blue-deep`
- `--green`, `--sand`, `--sand-soft`
- `--muted`, `--surround`
- `--line-mid`, `--line-on-dark`, `--icon-light`

Omit tokens you leave unchanged. Do not redefine spacing/type unless the skin intentionally changes them.

### 5. Cascade and verify

Intended cascade:

```text
:root                         → default Plumera palette
html[data-locale="…"]         → locale palette
.page[data-target="…"]        → target-within-locale palette
page-type roots               → layout / type deltas (prefer not full palette resets)
```

Smoke-test after adding a skin:

1. Domain root `/`  
2. Locale landing for that locale  
3. One content page under that locale (and target, if applicable)  

Bump `base.css` `?v=` when shipping a skin.

### 6. Current limitations (and interim workarounds)

**Content page / header mini-palettes**  
`.content-page` and `.content-header` still set local color variables. Those win over `html[data-locale]` for their subtrees. Until a follow-up thins those overrides to true page-type deltas, a locale skin that must reach content pages should also reassign under the page roots:

```css
html[data-locale="fr"] {
  --ink: #143b38;
  --paper: #f5f0e6;
}

html[data-locale="fr"] .content-page,
html[data-locale="fr"] .content-header {
  --ink: #143b38;
  --paper: #f5f0e6;
}
```

**EN home `--landing-*`**  
`.landing-home` uses a parallel `--landing-*` palette and does not yet follow shared semantics. Interim: reassign `--landing-*` in the same skin block for EN home, or land a cleanup that aliases `--landing-ink: var(--ink)` (etc.) first.

**Do not**

- Add a fifth CSS file for skins  
- Fork `content.css` / `landing.css` per locale  
- Expand new parallel token families (prefer shared semantics)

### Worked example (hypothetical)

Ship a slightly cooler French UI palette and a gold accent for `apprendre-anglais`:

1. Set `data-locale="fr"` on FR HTML (`public/fr/index.html` and FR content emits).  
2. Set `data-target="apprendre-anglais"` on those content `.page` roots.  
3. Append after `:root` in `base.css`:

```css
html[data-locale="fr"] {
  --ink: #123a42;
  --paper: #f2f4f1;
  --blue: #6e8f99;
  --sand: #a8925c;
}

html[data-locale="fr"] .content-page,
html[data-locale="fr"] .content-header {
  --ink: #123a42;
  --paper: #f2f4f1;
}

html[data-locale="fr"] .page[data-target="apprendre-anglais"] {
  --accent: #b89267;
}
```

4. Bump `base.css?v=…`, rebuild, check `/fr/`, a FR content page, and `/`.
