# Filterable content catalog — PRD

Browse and narrow learning content by structured fields (level, type, date), with a path to API-backed scale and site search. Lesson and article URLs remain static HTML forever.

## Jira

| Project | Key | Summary |
|---------|-----|---------|
| Content | [CONT-31](https://plumerastudios.atlassian.net/browse/CONT-31) | Epic — authoring & metadata |
| Content | [CONT-32](https://plumerastudios.atlassian.net/browse/CONT-32) | Define `type` vocabulary + backfill existing pages |
| MSEO | [MSEO-25](https://plumerastudios.atlassian.net/browse/MSEO-25) | Epic — catalog & site search |
| MSEO | [MSEO-26](https://plumerastudios.atlassian.net/browse/MSEO-26) | Phase 1 — static filterable catalog + index JSON |
| MSEO | [MSEO-27](https://plumerastudios.atlassian.net/browse/MSEO-27) | Phase 2 — API-backed catalog (Postgres) |
| MSEO | [MSEO-28](https://plumerastudios.atlassian.net/browse/MSEO-28) | Phase 3 — site search (JSON → Postgres) |

CONT-31 relates to MSEO-25. CONT-32 blocks MSEO-26 (metadata before catalog ship).

## Goals

- Give learners one place per locale + target to explore all listable content.
- Support filter/sort by **level**, **type**, and **date** without a React lesson reader.
- Ship a small static version now (~20 items) on an architecture that can move the list to a backend later (tens → hundreds → thousands).
- Complement the catalog later with **site search** (free text), sharing the same content pipeline and metadata.
- Keep SEO honest: catalog discovery pages are real HTML documents; each result opens a static content page.

## Non-goals

- React/SPA as the lesson or article reader.
- Replacing static lesson HTML with dynamically rendered article bodies.
- Sharding, virtualized lists, or search infrastructure in phase 1.
- Merging catalog browse and search into one undifferentiated UI.
- Per-level static index pages as a requirement for phase 1 (optional later for SEO).

## Concepts

| Concept | Role |
|---------|------|
| **Catalog** | Structured browse: filter by level/type, sort by date. |
| **Search** | Free-text find (title, verb, body excerpts). Complements catalog; does not replace it. |
| **Catalog index** | Builder-emitted structured list of card fields. Source of truth for catalog UI (and later Postgres load). |
| **Static result pages** | Existing content URLs under `dist/` — full HTML documents. |

**Scope:** one catalog per `locale` + `target` (e.g. English UI teaching French → `/en/learn-french/…`).

## Shared foundations (all phases)

Lock these in phase 1 so later work changes **delivery**, not the product model.

### Entry contract

Every listable page contributes:

| Field | Required | Notes |
|-------|----------|--------|
| `title` | yes | List label (body H1 / existing list-title rules) |
| `href` | yes | Static content URL |
| `date` | yes | Frontmatter `date`; used for sort |
| `level` | yes | CEFR code (`A1`, `A2`, …) |
| `type` | yes | Controlled vocabulary (see below) |
| `topic` | optional | e.g. verb lemma (`être`) for finer grouping later |
| `summary` | optional | Short blurb (e.g. from `description`) |

### New frontmatter: `type`

- Controlled set to start: at least `verb` | `grammar` (expand only when a real series needs it).
- May default `type: verb` for everything under `votw/`; require explicit `type` on `articles/` and future series.
- Do not overload path-inferred “kind” (VOTW vs Article chrome labels) as the filter taxonomy.

### Builder artifact

```text
Markdown (content/)
  → parse / validate catalog fields
  → catalog index (JSON) per locale + target
  → catalog page (phase 1: embed list from index)
  → lesson / article HTML (unchanged)
```

Draft rules match the rest of the site: production index omits `draft: true`; `--drafts` includes drafts.

### Stable vs replaceable

| Stable | Allowed to change later |
|--------|-------------------------|
| Entry fields and meanings | How many rows ship in the first HTML response |
| One catalog URL per target | Inlined list vs API-fetched pages |
| Index shape (compact cards, not full bodies) | Single JSON file vs sharded files / DB |
| Results → static HTML | Search engine / Postgres FTS details |

**Success criterion for scale:** growing from ~20 to thousands of items changes **how the catalog page loads and paints rows**, without changing URLs, filter meanings, or how authors tag pages.

## Phase 1 — Static filterable catalog (~20 items)

**When:** now.

**Ship:**

- One generated catalog page per target that has listable content (start with `en/learn-french`).
- Builder always emits the **catalog index JSON** and builds the page list **from that index** (one code path).
- Page UI: filter by level and type; sort by date (newest/oldest; title optional).
- Optional shareable query string: `?level=A1&type=verb`.
- Reuse existing content-list presentation where it fits; filters sit above the list.
- ~20 rows inlined in HTML is acceptable.

**SEO (phase 1):**

- Full HTML document (title, description, self-canonical).
- Full default list in the HTML response.
- Include in sitemaps like other content pages.
- Internal links (nav, landing, CEFR / level badge) are a product choice at implementation time — do not expand chrome without an explicit decision.

**Open choices before build:**

1. URL slug: `catalog` vs `browse` vs other.
2. Exact `type` vocabulary.
3. Authored intro Markdown vs fully generated chrome copy.
4. Which locales/targets get a catalog in the first slice.

**Done when:**

- Catalog works for the agreed target(s).
- Index JSON is in `dist/`.
- Filters/sort work; cards open static pages.
- Drafts excluded from production index.
- Tests cover index contents and draft exclusion.

## Phase 2 — API-backed catalog (~50–75 items)

**When:** list size makes a full inlined HTML list a load-time problem.

**Ship:**

- Same catalog URL and filter/sort semantics.
- Thin page shell loads quickly; list region filled from a **backend** (Python API).
- API serves filtered, sorted, paginated card data from **Postgres** (populated from the same catalog index the builder emits, or an equivalent publish step).
- Click-through still goes to **static HTML** on the same origin.

**SEO (phase 2):**

- Keep a real HTML document at the catalog URL (title, description, canonical).
- Embed or server-render a **default slice** (e.g. newest N) so crawlers do not see an empty shell.
- Filtered query views may stay client-driven; do not depend on thousands of filter URLs for SEO.
- Individual lessons/articles remain the primary SEO surface; catalog is discovery.

**Done when:**

- Catalog stays responsive at 75+ items.
- Pagination or load-more works without shipping the full catalog as HTML for UX.

## Phase 3 — Site search (~50 items)

**When:** free-text discovery matters; can land near the same scale as phase 2.

**Ship:**

- Builder generates a **search index JSON** (catalog fields + text worth searching: title, H1, summary/description, selected body as needed).
- Load that JSON into **Postgres** (full-text or equivalent).
- Search UI (site chrome and/or catalog page) calls the API; results link to the same static HTML pages.
- Catalog = structured browse; search = free text. Shared store where useful (`level` / `type` as optional search facets later).

### Suggested dependency order

1. Catalog index JSON + static catalog page (phase 1).
2. Postgres + load pipeline for catalog rows (and search text when ready) + API.
3. Point catalog UI at API (phase 2).
4. Search endpoint + UI (phase 3).

Phase 2 and 3 both want Postgres/API around the same content size; either can lead once the shared store exists. Prefer not inventing a second incompatible metadata model for search.

## Relationship to existing site

- **What’s-new / VOTW series lists:** remain series- or recency-specific; catalog is the cross-series browse surface for a target.
- **CEFR page:** explainer; may link into the catalog with a level filter later.
- **Level badge on content pages:** today links to CEFR; may deep-link to catalog `?level=…` later.
- **Corpus / APIs:** README already anticipates Python APIs; catalog/search backend fits that lane — not the content-builder’s static emit of lesson HTML.

## Out of scope until explicitly planned

- Arabic / additional locales beyond whatever phase 1 names.
- Client-only empty catalog shells with no default HTML slice (SEO risk).
- Multi-type tags / free-form tag clouds.
- Per-level static pages (`/a1/`, `/a2/`) — optional SEO add-on on top of the same index.

## Success metrics (lightweight)

- Learners can open one URL and narrow to their level and content type.
- Authoring cost stays “frontmatter + Markdown”; no parallel CMS for the catalog.
- Moving to API/search does not require retagging content or changing result URLs.
