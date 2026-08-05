# Filterable content catalog — PRD

Browse and narrow learning content by structured fields, with a path to API-backed scale and site search. Lesson and article URLs remain static HTML forever.

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
- Support filter/sort without a React lesson reader.
- Ship a small static version now (~20 items) on an architecture that can move the list to a backend later (tens → hundreds → thousands).
- Complement the catalog later with **site search** (free text), sharing the same content pipeline and metadata.
- Keep SEO honest: catalog discovery pages are real HTML documents; each result opens a static content page.

## Non-goals

Explicitly out of scope unless a later PRD says otherwise — prevents feature drift.

| Out of scope | Notes |
|--------------|--------|
| React/SPA lesson or article reader | Results stay static HTML |
| Dynamically rendered article bodies | Builder-emitted pages only |
| Semantic / embedding ranking | Keyword + structured filters only |
| Personalization / “for you” ranking | No per-user catalogs |
| Typo tolerance / fuzzy search | Phase 3 is exact/token FTS unless separately scoped |
| Cross-locale blending | No mixing `/en/…` and `/fr/…` results on one page |
| Cross-target blending | Catalog is one `locale` + `target` at a time |
| Audience personas as a filter | Learner stage is **level** (CEFR), not a separate audience dim |
| Multi-type tags / free-form tag clouds | Single controlled `type` |
| Sharding / list virtualization in phase 1 | Not needed at ~20 items |
| Merging catalog and search into one UI | Complementary, not combined |
| Per-level static pages as a phase 1 requirement | Optional SEO add-on later |
| Client-only empty catalog shells | SEO risk; always ship a real HTML document |

## Concepts

| Concept | Role |
|---------|------|
| **Catalog** | Structured browse: filter and sort over a target’s listable pages. |
| **Search** | Free-text find. Complements catalog; does not replace it. |
| **Catalog index** | Builder-emitted structured list of card fields. Build-time source of truth for the catalog UI (and later Postgres load). |
| **Static result pages** | Existing content URLs under `dist/` — full HTML documents. |

**Scope:** one catalog per `locale` + `target` (e.g. English UI teaching French → `/en/learn-french/…`).

## What “filterable” means

A catalog is **filterable** when the learner can narrow the visible set using **canonical dimensions** below. Dimensions are either:

- **UI filter** — control on the catalog page,
- **Sort** — order of the list,
- **Scope** — fixed by which catalog URL you are on,
- **System** — applied at index build / API load (not a learner control),
- **Deferred** — in the data contract for later UI, not phase 1 controls.

### Canonical dimensions

| Dimension | Maps to | Phase 1 learner UI | Required on each entry | Notes |
|-----------|---------|--------------------|------------------------|--------|
| **Locale** | `locale` | Scope (URL) | yes | Separate locale sites; no hreflang blending |
| **Target** | `target` | Scope (URL) | yes | Language being taught |
| **Level** | `level` | **Filter** (required) | yes | CEFR: `A1` … `C2` (exact code; no ranges in v1) |
| **Content type** | `type` | **Filter** (required) | yes | Controlled: start `verb` \| `grammar` |
| **Topic** | `topic` | Deferred (optional field) | no | e.g. verb lemma; group/filter later |
| **Freshness** | `date` | **Sort** (required); date-range filter deferred | yes | ISO date in index; locale-formatted label optional in UI |
| **Publish state** | `draft` | System only | n/a | Production index omits drafts; not a learner filter |
| **Series / kind** | path / chrome | Display only | no | “VOTW” vs “Article” label ≠ `type` taxonomy |
| **Audience** | — | Out of scope | — | Use **level**, not a separate audience field |

Phase 1 UI minimum: **filter level**, **filter type**, **sort by date** (newest / oldest). Optional: sync to `?level=&type=&sort=`.

## Data contract (v1)

### Ownership and source of truth

| Concern | Owner | Source of truth |
|---------|-------|-----------------|
| Entry schema (field names, types, requiredness) | **MSEO** (builder) with CONT review on semantic fields | This PRD + builder validation; versioned as `schemaVersion` in the index |
| Taxonomy values (`type`, allowed `level` codes) | **CONT** (governance); MSEO enforces in CI/builder | CONT-32 vocabulary + authoring docs; builder rejects unknown values once locked |
| Page metadata on Markdown | **CONT** (authors) | Frontmatter on each listable page |
| Catalog / search index artifacts in `dist/` | **MSEO** (content builder) | Generated at site build from Markdown |
| Postgres load + API (phase 2+) | **MSEO** (site/API) | Loaded from builder JSON (or equivalent publish artifact) |
| Reindex cadence | **MSEO** | Same as site publish (see Operational SLOs) |
| Quality checks for missing metadata | **MSEO** CI (fail or warn per policy); **CONT** fixes content | Builder/tests; CONT-32 backfill |

Markdown under `content/` remains the authoring source of truth. The catalog index is the **derived** contract for UI and API — not a second place authors edit by hand.

### Record shape

Index file (conceptual path): `dist/{locale}/{target}/catalog/index.json` (exact path locked in MSEO-26).

Top-level:

```json
{
  "schemaVersion": 1,
  "locale": "en",
  "target": "learn-french",
  "generatedAt": "2026-08-05T18:00:00Z",
  "entries": [ /* CatalogEntry */ ]
}
```

`CatalogEntry` example:

```json
{
  "id": "en/learn-french/votw/etre/votw-etre-basics-a1",
  "title": "Être - basics",
  "href": "/en/learn-french/votw/etre/votw-etre-basics-a1/",
  "date": "2026-07-08",
  "level": "A1",
  "type": "verb",
  "topic": "être",
  "summary": "How French uses être for identity, location, and description at A1.",
  "kind": "Verb of the Week"
}
```

| Field | Required | Type | Notes |
|-------|----------|------|--------|
| `id` | yes | string | Stable opaque id (path-derived is fine) |
| `title` | yes | string | List label (body H1 / existing list-title rules) |
| `href` | yes | string | Absolute-path URL to static HTML |
| `date` | yes | string | `YYYY-MM-DD` for sort |
| `level` | yes | string | CEFR code |
| `type` | yes | string | Controlled vocabulary |
| `topic` | no | string | Lemma / subject |
| `summary` | no | string | Short blurb (often from `description`) |
| `kind` | no | string | Series chrome label for display |

### Forward compatibility (phase migration)

- Phase 1 HTML list, phase 2 API responses, and phase 3 search hits that expose catalog cards **must** be supersets of this v1 entry shape for shared fields.
- Additive changes only within `schemaVersion: 1` (new optional fields OK). Breaking renames/removals bump `schemaVersion` and require an explicit migration note in MSEO.
- API list endpoints (phase 2) should return the same field names/types for a card as the static JSON entry (plus pagination envelope). Do not invent a parallel DTO that renames `type` → `contentType` without a versioned mapping.
- Search (phase 3) may add search-only fields (`snippet`, `score`) alongside the catalog card fields; it must not require a second tagging model for `level` / `type`.

### Frontmatter: `type`

- Controlled set to start: `verb` | `grammar` (expand only when a real series needs it; CONT owns the decision).
- May default `type: verb` for everything under `votw/`; require explicit `type` on `articles/` and future series.
- Do not overload path-inferred “kind” as the filter taxonomy.

### Builder pipeline

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
| Entry fields and meanings (`schemaVersion`) | How many rows ship in the first HTML response |
| One catalog URL per target | Inlined list vs API-fetched pages |
| Index shape (compact cards, not full bodies) | Single JSON file vs sharded files / DB |
| Results → static HTML | Search engine / Postgres FTS details |

## Operational SLOs

These are **expected** SLOs for planning; tune numbers when CI/deploy reality is measured.

### Freshness / invalidation

| Phase | How the index updates | Expected freshness | Failure behavior |
|-------|----------------------|--------------------|------------------|
| **1** | Regenerated on every production site build/deploy (same ritual as `dist/`) | Catalog index and catalog HTML match the Markdown that shipped in that deploy. Target: **available on the live site within one successful Deploy after merge to `main`** (same as any other static page; no separate catalog CDN purge story). | Failed build/deploy → previous `dist/` remains live (stale but consistent). No partial catalog publish. |
| **2** | Builder JSON → Postgres load as part of publish (or immediately after deploy) | API data matches the just-shipped index within **same deploy window**; target **≤ 15 minutes** after successful static deploy unless a slower batch job is explicitly chosen. | If DB load fails: serve last-good DB snapshot; alert. Catalog page default HTML slice (from static build) still works for SEO/basic browse. Document degraded mode (filters may be stale vs static). |
| **3** | Search index JSON → Postgres with catalog load or twin job | Same freshness target as phase 2 for indexed docs. | Last-good search index; prefer empty/error UI over silently searching a broken schema. |

There is **no** requirement for sub-minute reindex on every author save. Authoring uses drafts + merge + deploy; the catalog is as fresh as the site release.

### Availability (phase 2+)

| Surface | Expectation |
|---------|-------------|
| Static catalog URL / default HTML slice | Same as site static hosting (CloudFront/`dist/`) |
| Catalog / search API | Design for high availability once shipped; exact % TBD with hosting. Soft launch may tolerate brief errors if the static default slice remains usable. |

### Quality checks (missing metadata)

- Builder **warns** during CONT-32 transition if `type` / `level` / `date` missing on listable pages.
- After vocabulary lock: builder/CI **fails** the build (or fails a dedicated check) when a non-draft listable page lacks required catalog fields or uses an unknown `type`/`level`.
- Unknown or invalid entries must not silently appear in the production index with empty filters.

## Success metrics by phase

Qualitative bar still applies: authoring stays frontmatter + Markdown; result URLs stay static; no retag for phase 2/3.

### Phase 1 — static catalog

| KPI | Target |
|-----|--------|
| **Index coverage** | 100% of non-draft listable pages for the shipped target(s) appear in the catalog index with required fields |
| **Metadata completeness** | 100% of those entries have non-empty `level`, `type`, `date`, `title`, `href` |
| **Filter correctness** | Manual/automated checks: each level/type control shows only matching rows; “all” shows full index |
| **Draft exclusion** | 0 drafts in production index / production catalog HTML |
| **Result integrity** | 100% of catalog `href`s resolve to emitted static HTML in `dist/` (internal link check) |
| **Page weight (sanity)** | Full inlined list acceptable at ≤ ~50 entries; revisit phase 2 trigger if HTML list payload becomes a measured LCP problem |

### Phase 2 — API catalog

| KPI | Target |
|-----|--------|
| **Query latency** | p95 catalog list API **≤ 300 ms** server-side for typical filter combos at ~100 rows (tune with real hosting) |
| **Freshness** | API reflects shipped index within the phase 2 freshness SLO above |
| **Pagination** | No full-catalog HTML dump required for UX; default page size documented |
| **SEO shell** | Catalog URL returns real HTML with a non-empty default slice (crawl/render mismatch = fail) |
| **Degraded mode** | Documented behavior when API is down; static slice still available |

### Phase 3 — site search

| KPI | Target |
|-----|--------|
| **Zero-result rate** | Track; investigate if sustained **> 30%** of searches on common teaching terms after tuning (baseline first month, then set a tighter goal) |
| **CTR from results** | Track click-through to static pages; no hard launch gate — use to tune ranking/snippets |
| **Index coverage** | Same listable set as catalog (+ search text fields); drafts excluded in production |
| **Query latency** | p95 search API **≤ 400 ms** at initial corpus size (tune later) |
| **Contract reuse** | Search hits expose v1 catalog card fields for shared UI components |

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
2. Exact `type` vocabulary (CONT-32).
3. Authored intro Markdown vs fully generated chrome copy.
4. Which locales/targets get a catalog in the first slice.

**Done when:**

- Phase 1 KPIs met for agreed target(s).
- Index JSON is in `dist/`; page rendered from index.
- Filters/sort work; cards open static pages.
- Tests cover index contents, draft exclusion, and required fields.

## Phase 2 — API-backed catalog (~50–75 items)

**When:** list size makes a full inlined HTML list a load-time problem (see phase 1 page-weight sanity KPI).

**Ship:**

- Same catalog URL and filter/sort semantics; same v1 card fields in API responses.
- Thin page shell loads quickly; list region filled from a **backend** (Python API).
- API serves filtered, sorted, paginated card data from **Postgres** (populated from the same catalog index the builder emits, or an equivalent publish step).
- Click-through still goes to **static HTML** on the same origin.

**SEO (phase 2):**

- Keep a real HTML document at the catalog URL (title, description, canonical).
- Embed or server-render a **default slice** (e.g. newest N) so crawlers do not see an empty shell.
- Filtered query views may stay client-driven; do not depend on thousands of filter URLs for SEO.
- Individual lessons/articles remain the primary SEO surface; catalog is discovery.

**Done when:** phase 2 KPIs met.

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

**Done when:** phase 3 KPIs met (with baselines collected in the first month where targets are track-then-tighten).

## Relationship to existing site

- **What’s-new / VOTW series lists:** remain series- or recency-specific; catalog is the cross-series browse surface for a target.
- **CEFR page:** explainer; may link into the catalog with a level filter later.
- **Level badge on content pages:** today links to CEFR; may deep-link to catalog `?level=…` later.
- **Corpus / APIs:** README already anticipates Python APIs; catalog/search backend fits that lane — not the content-builder’s static emit of lesson HTML.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Taxonomy inconsistency** (`type` / level drift across pages) | Broken filters; empty or misleading facets | CONT owns vocabulary; builder rejects unknown values after lock; CONT-32 backfill |
| **Missing metadata** | Entries dropped or unfilterable | Warn → fail CI; coverage KPI 100% |
| **Stale index** (especially phase 2+ DB vs `dist/`) | Learners see old set; SEO slice disagrees with API | Same-deploy load; freshness SLO; degraded-mode docs; alert on load failure |
| **Crawl / render mismatch** | Catalog URL empty or thin for bots, rich for JS | Always ship real HTML + default slice; phase 2 SEO acceptance |
| **Contract drift** (HTML vs JSON vs API field names) | Duplicate DTOs; costly phase 2 rewrite | Single v1 card shape; `schemaVersion`; additive-only rule |
| **Scope creep** (semantic search, personalization, cross-locale) | Delays catalog | Non-goals table; separate PRD to reopen |

## Out of scope until explicitly planned

- Additional locales/targets beyond whatever phase 1 names.
- Date-range / freshness **filter** UI (sort is in phase 1; range filter later).
- `topic` as a learner-facing filter.
- Per-level static pages (`/a1/`, `/a2/`) — optional SEO add-on on top of the same index.
