# Production release history

Chronological record of production publishes for [plumerastudios.com](https://plumerastudios.com). Newest first.

- **Current repo:** [`swlsf23/plumera-studios`](https://github.com/swlsf23/plumera-studios) — tag a `v*` release; Deploy workflow syncs `dist/` to S3 and invalidates CloudFront.
- **Early site repo:** [`swlsf23/plumera-studios-site`](https://github.com/swlsf23/plumera-studios-site) — no GitHub Release tags; production was manual `scripts/deploy.sh` after merges to `main` (July 2026).

Snapshot tags (`snapshot/…`) are not production releases and are omitted here.

## plumera-studios (tagged / CD)

| Date (UTC) | Tag | Summary | Release |
|------------|-----|---------|---------|
| 2026-08-06 | `v2026.08.05-SITE` | Filterable All lessons catalog (phase 1) | [Release](https://github.com/swlsf23/plumera-studios/releases/tag/v2026.08.05-SITE) |
| 2026-08-05 | `v2026.08.04-CNT` | Être/avoir VOTW cluster and passé composé | [Release](https://github.com/swlsf23/plumera-studios/releases/tag/v2026.08.04-CNT) |
| 2026-08-04 | `v2026.08.04-SITE` | CSS bundles, favicon, Plumera Sans font hardening | [Release](https://github.com/swlsf23/plumera-studios/releases/tag/v2026.08.04-SITE) |
| 2026-07-31 | `v2026.07.31-CNT` | Tenir VOTW, certification guide, prendre polish | [Release](https://github.com/swlsf23/plumera-studios/releases/tag/v2026.07.31-CNT) |
| 2026-07-31 | `v2026.07.30-UX` | UX and builder polish (no new lesson content) | [Release](https://github.com/swlsf23/plumera-studios/releases/tag/v2026.07.30-UX) |
| 2026-07-30 | `v2026.07.29` | First **automated** deploy from this repo (CI/CD MSEO-10). Site was already live from `plumera-studios-site`. Tag only — no GitHub Release notes object | [Tag](https://github.com/swlsf23/plumera-studios/releases/tag/v2026.07.29) · [Deploy run](https://github.com/swlsf23/plumera-studios/actions/runs/30510378885) |

## plumera-studios-site (site birth / pre-migration)

**Site birth date: 2026-07-22.**

Evidence: repo created `2026-07-22T11:58:18Z`; [PR #1](https://github.com/swlsf23/plumera-studios-site/pull/1) merged `2026-07-22T12:06:44Z` with the initial French landing, sitemap, and production `scripts/deploy.sh`. No GitHub Release/tag and no logged S3 sync timestamp, so the birth **day** is exact; the clock time of the first `deploy.sh` run is not in git.

No tags or GitHub Releases. Deploys were local/AWS via [`scripts/deploy.sh`](https://github.com/swlsf23/plumera-studios-site/blob/main/scripts/deploy.sh). Table dates are merge-to-`main` days.

| Date (UTC) | Tag | Summary | Link |
|------------|-----|---------|------|
| 2026-07-23 | — | Updates + Privacy (profile icon); core reorg; Umami restrict; source/deploy trees; ES/FR core; language nav | [PR #6](https://github.com/swlsf23/plumera-studios-site/pull/6) · [PR #18](https://github.com/swlsf23/plumera-studios-site/pull/18) … [PR #23](https://github.com/swlsf23/plumera-studios-site/pull/23) |
| 2026-07-22 | — | **Site birth** — French landing, deploy script, crawler/agent safeguards | [PR #1](https://github.com/swlsf23/plumera-studios-site/pull/1) · [PR #2](https://github.com/swlsf23/plumera-studios-site/pull/2) |

Ownership moved to **plumera-studios** (repo created 2026-07-25). First automated Deploy workflow run: **2026-07-30** (toolchain cutover, not launch).

## Maintaining this file

After each production publish:

1. Add a row under **plumera-studios** (date = release/publish UTC day, tag, short summary, release URL).
2. Prefer the GitHub Release link when notes exist; otherwise link the tag and/or Deploy workflow run.
