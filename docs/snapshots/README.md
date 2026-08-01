# EN home snapshots

Frozen reference copies of the English locale home — not served by the site.

| Folder | What it is | Git tag |
| --- | --- | --- |
| `en-home-production-2026-07-23/` | Classic EN landing as deployed from `plumera-site` / `plumera-studios-site` | `snapshot/en-home-production` |
| `en-home-proposal-2026-07-29/` | Homepage proposal layout (bubbles + What’s new + feature cards + Featured) | `snapshot/en-home-proposal` |

Each folder holds the page HTML and its landing stylesheet for historical reference. Do not edit snapshot CSS for live styling — `public/css/` is the source of truth.

Live pages load `/css/base.css` (tokens, chrome, root) plus at most one page sheet (`landing.css`, `landing-home.css`, or `content.css`). See [`public/css/README.md`](../../public/css/README.md).
