# Deploy (CI/CD)

Tracked as [MSEO-10](https://plumerastudios.atlassian.net/browse/MSEO-10).

## Publishing ritual

1. Author with `draft: true` while iterating.
2. Remove `draft: true` when the page should ship (that is the publish decision).
3. Merge to `main` (CI builds a production-shaped `dist/` with **no** `--drafts`).
4. Tag a release, e.g. `v2026.07.30` or `v1.2.0`.
5. The **Deploy** workflow builds again without drafts, syncs `dist/` to S3, and invalidates CloudFront.

Production must never pass `--drafts`.

## CI (every PR and push to `main`)

Workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

- `pip install -e .`
- Prohibited-character check (`;` and em dash `—` in shippable copy)
- `python -m tools.content_builder` (no drafts)
- Dist shape + draft exclusion checks
- Head-tag smoke on sample content pages
- Internal link check against `dist/`
- `python -m unittest discover -s tests`
- Local HTTP smoke on key URLs

Run the same checks locally:

```bash
source .venv/bin/activate
pip install -e .
python -m tools.ci.check_prohibited_chars
python -m tools.content_builder
python -m tools.ci.check_internal_links
python -m unittest discover -s tests -v
```

## CD (tags `v*` or manual `workflow_dispatch`)

Workflow: [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml)

Uses GitHub Environment **`production`** and OIDC to AWS (no long-lived access keys in the repo).

### Repository / environment variables

Set these on the `production` environment (Settings → Environments → production → Variables):

| Variable | Purpose |
| --- | --- |
| `AWS_ROLE_ARN` | IAM role ARN for `aws-actions/configure-aws-credentials` (OIDC trust to this repo) |
| `AWS_REGION` | e.g. `us-west-2` |
| `S3_BUCKET` | Marketing-site bucket that serves `plumerastudios.com` |
| `CLOUDFRONT_DISTRIBUTION_ID` | Distribution to invalidate after sync |

### IAM role trust (sketch)

Trust `token.actions.githubusercontent.com` for this repository, limited to the `production` environment (or `refs/tags/v*`). Attach permissions for `s3:ListBucket` / `s3:PutObject` / `s3:DeleteObject` on the site bucket and `cloudfront:CreateInvalidation` on the distribution.

### First deploy after setup

```bash
git checkout main
git pull
git tag vYYYY.MM.DD
git push origin vYYYY.MM.DD
```

Then confirm the Deploy workflow is green and spot-check View Source on `/`, `/en/`, and a content URL (title / description / canonical present in the HTML file).

## Notes

- `aws s3 sync --delete` removes objects that are no longer in `dist/`. An empty or broken build is guarded by the “Refuse empty or incomplete dist/” step.
- Interactive apps (e.g. `/app/flashcard/`) are included when `npm run build:site` runs Vite into `dist/app/…` after the content builder. Content pages remain full static HTML; apps are SPA shells under `/app/`.
- Hand-authored landings under `public/` are copied into `dist/` by the builder and deploy with everything else.
