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
- Support **filtering** (only matching rows) and **sorting** (reorder the current set) without a React lesson reader.
- Ship a small static version now (~20 items) on an architecture that can move the list to a backend later (tens → hundreds → thousands).
- Complement the catalog later with **site search** (free text), sharing the same content pipeline and metadata.
- Keep SEO honest: catalog discovery pages are real HTML documents; each result opens a static content page.
- **Static delivery lock:** the catalog page loads as builder-emitted HTML. Client JS may filter/sort the in-page list and sync the query string, but must **not** patch `<title>`, meta description, or canonical. Clicks on results are normal full-page navigations to other static HTML URLs — no SPA/MPA shell, no client router, no fetch-and-replace of page documents.

## Non-goals

Explicitly out of scope unless a later PRD says otherwise — prevents feature drift.

| Out of scope | Notes |
|--------------|--------|
| React/SPA lesson or article reader | Results stay static HTML |
| Client-side title / meta / canonical patching on catalog (or results) | SEO fields are build-time only |
| Dynamically rendered article bodies | Builder-emitted pages only |
| Semantic / embedding ranking | Keyword + structured filters only |
| Personalization / “for you” ranking | No per-user catalogs |
| Typo tolerance / fuzzy search | Phase 3 is exact/token FTS unless separately scoped |
| Cross-locale blending | No mixing `/en/…` and `/fr/…` results on one page |
| Cross-target blending | Catalog is one `locale` + `target` at a time |
| Audience personas as a filter | Learner stage is **level** (CEFR), not a separate audience dim |
| Free-form / author-invented type strings | Controlled allow-list only (multi-value from that list is allowed) |
| Sharding / list virtualization in phase 1 | Not needed at ~20 items |
| Merging catalog and search into one UI | Complementary, not combined |
| Per-level static pages as a phase 1 requirement | Optional SEO add-on later |
| Client-only empty catalog shells | SEO risk; always ship a real HTML document |
| `topic` frontmatter / lemma tags | Prefer catalog text filter (title + summary); no inconsistent optional metadata |
| Landing/nav chrome expansion | Explicit product decision per PR; not implied by catalog ship |

## Concepts

| Concept | Role |
|---------|------|
| **Catalog** | Structured browse: filter (restrict) and sort (reorder) over a target’s listable pages. |
| **Search** | Free-text find. Complements catalog; does not replace it. |
| **Catalog index** | Builder-emitted structured list of card fields. Build-time source of truth for the catalog UI (and later Postgres load). |
| **Static result pages** | Existing content URLs under `dist/` — full HTML documents. |

**Scope:** one catalog per `locale` + `target` (e.g. English UI teaching French → `/en/learn-french/catalog/`).

## Filter vs sort (definitions)

These are different operations. Do not conflate them.

| Term | Meaning | Example |
|------|---------|---------|
| **Filter** | Show **only** entries that match a chosen characteristic. Everything else is hidden. | Only levels that include A1; only types that include verb; date on/within range |
| **Sort** | **Reorder** the current result set (after filters, or the full catalog if unfiltered). Does not hide rows. | Among visible rows: newest date first; or by primary level; or by primary type |

Same idea applies later to **search**: filters restrict which hits appear; sort orders those hits.

### How dimensions are used

| Dimension | Maps to | Filter? | Sort? | Phase 1 learner UI | Required on each entry | Notes |
|-----------|---------|---------|-------|--------------------|------------------------|--------|
| **Locale** | `locale` | — | — | Scope (URL) | yes | Separate locale sites |
| **Target** | `target` | — | — | Scope (URL) | yes | Language being taught |
| **Level** | `level` | yes | yes | **Filter** and **sort** | yes (list, ≥1) | CEFR codes; multi-value allowed |
| **Content type** | `type` | yes | yes | **Filter** and **sort** | yes (list, ≥1) | Controlled allow-list; multi-value allowed |
| **Text (contains)** | title + summary | yes | — | **Filter** (substring) | derived | Case-insensitive match on list title + `description`; not body |
| **Date / freshness** | `date` | yes | yes | **Filter** (day or range) and **sort** | yes (single) | One publish date per page |
| **Publish state** | `draft` | system | — | System only | n/a | Production index omits drafts |
| **Series / kind** | path / chrome | no | no | Display only | no | “VOTW” vs “Article” ≠ `type` |
| **Audience** | — | — | — | Out of scope | — | Use **level** |
| **Relevance** | search score | — | phase 3 | N/A until search | — | Search sort only |

### Multi-value `level` and `type`

Authors may set one value or a list:

```yaml
level: A1                 # or: [A1, A2]
type: verb                # or: [verb, grammar]
date: 2026-07-08          # always a single publish date
```

Index always normalizes to arrays for `level` and `type`:

```json
"level": ["A1", "A2"],
"type": ["verb", "grammar"]
```

**Filter semantics:** a filter value matches if it is **included** in the entry’s list (e.g. level filter `A1` matches `[A1, A2]`).

**Sort semantics:** use the **primary** value = first element of the list. Authors put the main level/type first.

**Cross-dimension filters** combine with AND (level includes A1 **and** type includes verb **and** date in range).

### `type` allow-list (locked)

| Value | Use for |
|-------|---------|
| `verb` | Verb meanings, forms, patterns, expressions (VOTW and verb-focused articles) |
| `grammar` | Structures, tenses, contrasts, system explainers |
| `conjugation` | Conjugation / paradigm series |
| `vocabulary` | Word sets, false friends, lexicon explainers |
| `pronunciation` | Sound, liaison, stress, standalone pronunciation pages |
| `guide` | Locale-wide reference (CEFR, exams, and similar `core/` pages) |

Locale `core/` pages opt into every target catalog for that locale with `catalog: true` plus the usual `level` / `type` / `date` fields.

Do **not** invent synonyms (`expressions`, `idioms`, `tense`) — use multi-type (`verb` + `grammar`) and/or the catalog text filter instead. Series identity stays in `kind`, not `type`.

Builder rejects unknown `type` / `level` values on listable pages.

### Dynamic filter facets

The filter UI lists **only values that exist** on at least one entry in **this** catalog index (after draft filtering).

- If no page is tagged `pronunciation`, do not show a pronunciation type control.
- If the index only has A1/A2/B1, do not show B2–C2 level controls.
- The schema allow-list may be larger than the visible facet list; authors can still tag new values, and the UI grows when those pages appear.

### Phase 1 UI (complete — no partial ship)

Phase 1 is not a prototype with missing controls. What ships must fully work.

- **Filters:**
  - **Contains** — free-text substring over **title + summary** (`description`); case-insensitive; not body. Empty = no text restriction.
  - **Level** — one value or “all”; match = level list includes value.
  - **Type** — one value or “all”; match = type list includes value.
  - **Date** — “all”; **one field only** = that exact day; **both fields** = inclusive range (`dateFrom` / `dateTo`).
  - Facet options for level/type are **data-driven** (see above).
  - Empty-state copy when nothing matches.
- **Sort:** date, level, or type, each with a defined direction. Default: **date newest first** (`date-desc`).
  - Level order for sort: A1 → C2 (and reverse).
  - Type order for sort: allow-list order (`verb`, `grammar`, `conjugation`, `vocabulary`, `pronunciation`, `guide`).
- **Query sync:** `?q=&level=&type=&sort=&date=&dateFrom=&dateTo=` so views are shareable.
- Filters apply first (AND across dimensions); sort applies to whatever remains. Sort never changes membership.

**Before site search (phase 3):** catalog text filter is enough for “find être / passé composé in this target.” Full-body / site-wide search comes later.

Deferred on purpose: body text in catalog filter, search relevance ranking, multi-select facet chips (one level + one type at a time is enough for phase 1).

## Data contract (v1)

### Ownership and source of truth

| Concern | Owner | Source of truth |
|---------|-------|-----------------|
| Entry schema (field names, types, requiredness) | **MSEO** (builder) with CONT review on semantic fields | This PRD + builder validation; versioned as `schemaVersion` in the index |
| Taxonomy values (`type`, allowed `level` codes) | **CONT** (governance); MSEO enforces in CI/builder | This PRD allow-list + authoring docs; builder rejects unknown values |
| Page metadata on Markdown | **CONT** (authors) | Frontmatter on each listable page |
| Catalog / search index artifacts in `dist/` | **MSEO** (content builder) | Generated at site build from Markdown |
| Postgres load + API (phase 2+) | **MSEO** (site/API) | Loaded from builder JSON (or equivalent publish artifact) |
| Reindex cadence | **MSEO** | Same as site publish (see Operational SLOs) |
| Quality checks for missing metadata | **MSEO** CI (fail build); **CONT** fixes content | Builder/tests; CONT-32 backfill |

Markdown under `content/` remains the authoring source of truth. The catalog index is the **derived** contract for UI and API — not a second place authors edit by hand.

### Record shape

Paths (locked):

- Index: `dist/{locale}/{target}/catalog/index.json`
- Page: `dist/{locale}/{target}/catalog/index.html` → URL `/{locale}/{target}/catalog/`

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
  "level": ["A1"],
  "type": ["verb"],
  "summary": "How French uses être for identity, location, and description at A1.",
  "kind": "Verb of the Week"
}
```

| Field | Required | Type | Notes |
|-------|----------|------|--------|
| `id` | yes | string | Stable opaque id (path-derived is fine) |
| `title` | yes | string | List label (body H1 / existing list-title rules) |
| `href` | yes | string | Absolute-path URL to static HTML |
| `date` | yes | string | `YYYY-MM-DD` (single publish date) |
| `level` | yes | string[] | ≥1 CEFR codes; primary = `[0]` |
| `type` | yes | string[] | ≥1 allow-listed types; primary = `[0]` |
| `summary` | no | string | Short blurb (from `description`); used by text filter |
| `kind` | no | string | Series chrome label for display |

Allowed CEFR codes: `A1`, `A2`, `B1`, `B2`, `C1`, `C2`.

### Forward compatibility (phase migration)

- Phase 1 HTML list, phase 2 API responses, and phase 3 search hits that expose catalog cards **must** be supersets of this v1 entry shape for shared fields.
- `level` and `type` are **always arrays** in the index/API (even for a single value).
- Additive changes only within `schemaVersion: 1` (new optional fields OK). Breaking renames/removals bump `schemaVersion` and require an explicit migration note in MSEO.
- API list endpoints (phase 2) should return the same field names/types for a card as the static JSON entry (plus pagination envelope).
- Search (phase 3) may add search-only fields (`snippet`, `score`) alongside the catalog card fields; it must not require a second tagging model for `level` / `type`.

### Frontmatter defaults

- `votw/`: may default `type: verb` when omitted (still prefer explicit frontmatter).
- `articles/` and other series: require explicit `type`.
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
| One catalog URL per target (`/catalog/`) | Inlined list vs API-fetched pages |
| Index shape (compact cards, not full bodies) | Single JSON file vs sharded files / DB |
| Results → static HTML | Search engine / Postgres FTS details |

## Operational SLOs

These are **expected** SLOs for planning; tune numbers when CI/deploy reality is measured.

### Freshness / invalidation

| Phase | How the index updates | Expected freshness | Failure behavior |
|-------|----------------------|--------------------|------------------|
| **1** | Regenerated on every production site build/deploy (same ritual as `dist/`) | Catalog index and catalog HTML match the Markdown that shipped in that deploy. Target: **available on the live site within one successful Deploy after merge to `main`**. | Failed build/deploy → previous `dist/` remains live (stale but consistent). No partial catalog publish. |
| **2** | Builder JSON → Postgres load as part of publish (or immediately after deploy) | API data matches the just-shipped index within **same deploy window**; target **≤ 15 minutes** after successful static deploy unless a slower batch job is explicitly chosen. | If DB load fails: serve last-good DB snapshot; alert. Catalog page default HTML slice still works. |
| **3** | Search index JSON → Postgres with catalog load or twin job | Same freshness target as phase 2 for indexed docs. | Last-good search index; prefer empty/error UI over silently searching a broken schema. |

There is **no** requirement for sub-minute reindex on every author save. Authoring uses drafts + merge + deploy; the catalog is as fresh as the site release.

### Availability (phase 2+)

| Surface | Expectation |
|---------|-------------|
| Static catalog URL / default HTML slice | Same as site static hosting (CloudFront/`dist/`) |
| Catalog / search API | Design for high availability once shipped; exact % TBD with hosting. |

### Quality checks (missing metadata)

- Builder/CI **fails** the build when a non-draft listable page lacks required catalog fields or uses an unknown `type`/`level`.
- Unknown or invalid entries must not silently appear in the production index with empty filters.

## Success metrics by phase

Qualitative bar still applies: authoring stays frontmatter + Markdown; result URLs stay static; no retag for phase 2/3.

### Phase 1 — static catalog

| KPI | Target |
|-----|--------|
| **Index coverage** | 100% of non-draft listable pages for the shipped target(s) appear in the catalog index with required fields |
| **Metadata completeness** | 100% of those entries have non-empty `level[]`, `type[]`, `date`, `title`, `href` |
| **Filter correctness** | Contains/level/type/date filters show **only** matching rows; empty/all shows the unfiltered index |
| **Facet correctness** | Level/type controls list only values present in the index |
| **Sort correctness** | Date, level, and type sort keys each reorder the current (filtered) set without changing membership; default `date-desc` |
| **Draft exclusion** | 0 drafts in production index / production catalog HTML |
| **Result integrity** | 100% of catalog `href`s resolve to emitted static HTML in `dist/` |
| **Page weight (sanity)** | Full inlined list acceptable at ≤ ~50 entries; revisit phase 2 if LCP suffers |

### Phase 2 — API catalog

| KPI | Target |
|-----|--------|
| **Query latency** | p95 catalog list API **≤ 300 ms** server-side for typical filter combos at ~100 rows |
| **Freshness** | API reflects shipped index within the phase 2 freshness SLO above |
| **Pagination** | No full-catalog HTML dump required for UX |
| **SEO shell** | Catalog URL returns real HTML with a non-empty default slice |
| **Degraded mode** | Documented behavior when API is down; static slice still available |

### Phase 3 — site search

| KPI | Target |
|-----|--------|
| **Zero-result rate** | Track; investigate if sustained **> 30%** after tuning (baseline first month) |
| **CTR from results** | Track; use to tune ranking/snippets |
| **Index coverage** | Same listable set as catalog (+ search text); drafts excluded in production |
| **Query latency** | p95 search API **≤ 400 ms** at initial corpus size |
| **Contract reuse** | Search hits expose v1 catalog card fields for shared UI |

## Phase 1 — Static filterable catalog (~20 items)

**When:** now.

**Locked decisions**

| Choice | Decision |
|--------|----------|
| URL | `/{locale}/{target}/catalog/` |
| Index | `dist/{locale}/{target}/catalog/index.json` |
| First HTML catalog | `en/learn-french` (emit JSON for any target with listable pages that pass validation) |
| Page copy | Fully generated chrome strings + short fixed intro |
| Default sort | `date-desc` |
| Landing/nav links | Not in phase 1 unless explicitly added |

**Ship**

- Catalog index JSON + catalog HTML built from that index (one code path).
- Complete filter UI: contains (title+summary), level, type, date (day or range); dynamic level/type facets.
- Complete sort UI: date, level, type (all directions).
- Query string sync (`q`, level, type, sort, date).
- Reuse content-list presentation; controls above the list.
- Full list in HTML for SEO / no-JS; JS filters and sorts in place. Without JS, filter controls stay hidden and a noscript note explains that filtering needs JavaScript.
- Text filter uses Unicode case folding on both sides (Python `str.casefold()` in the index blob; matching JS helper generated at build time into `dist/js/unicode-casefold.js` from that same interpreter).
- Catalog `<title>` / description / canonical are emitted in HTML; result `href`s are ordinary links to static pages (no SPA navigation).
- Sitemap entry for the catalog URL.
- Backfill `type` / `level` / `date` on every listable page; authoring docs updated. No `topic` field.

**Done when:** phase 1 KPIs met; tests cover index, draft exclusion, required fields, filter/sort/date behavior.

## Phase 2 — API-backed catalog (~50–75 items)

**When:** list size makes a full inlined HTML list a load-time problem.

**Ship:** same URL and filter/sort/date semantics; thin page + Python API + Postgres loaded from the same index; clicks still open static HTML; real HTML document + default slice for SEO.

**Done when:** phase 2 KPIs met.

## Phase 3 — Site search (~50 items)

**When:** free-text discovery matters; can land near the same scale as phase 2.

**Ship:** search index JSON → Postgres; search UI complements catalog; same static result URLs; reuse catalog card fields.

### Suggested dependency order

1. Catalog index JSON + static catalog page (phase 1).
2. Postgres + load pipeline + API.
3. Point catalog UI at API (phase 2).
4. Search endpoint + UI (phase 3).

**Done when:** phase 3 KPIs met (with baselines where targets are track-then-tighten).

## Relationship to existing site

- **What’s-new / VOTW series lists:** remain series- or recency-specific; catalog is the cross-series browse surface for a target.
- **CEFR page:** explainer; may link into the catalog with a level filter later.
- **Level badge on content pages:** today links to CEFR; may deep-link to catalog `?level=…` later.
- **Corpus / APIs:** catalog/search backend fits the Python API lane — not the content-builder’s static emit of lesson HTML.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Taxonomy inconsistency** | Broken filters; empty or misleading facets | CONT owns allow-list; builder rejects unknown values; CONT-32 backfill |
| **Missing metadata** | Entries dropped or unfilterable | Fail CI; coverage KPI 100% |
| **Stale index** (phase 2+ DB vs `dist/`) | Learners see old set; SEO slice disagrees with API | Same-deploy load; freshness SLO; degraded-mode docs |
| **Crawl / render mismatch** | Catalog URL empty for bots | Always ship real HTML with full default list (phase 1) / default slice (phase 2) |
| **Contract drift** | Costly phase 2 rewrite | Single v1 card shape; arrays for level/type; `schemaVersion` |
| **Empty facet clutter** | Filters for types with zero pages | Dynamic facets from index only |
| **Scope creep** | Delays catalog | Non-goals table |

## Out of scope until explicitly planned

- Additional locale/target catalog **pages** beyond the first slice (JSON may still emit where valid).
- Catalog text filter over **body** (title+summary only until then).
- Multi-select level/type facet chips (one value per dimension in phase 1).
- Per-level static pages (`/a1/`, `/a2/`).
- Site-wide search (phase 3) — catalog `q` is not a substitute forever, but ships first.
