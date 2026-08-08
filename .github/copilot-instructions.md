# Plumera Studios — Copilot instructions

This repository is a Python content site builder (`tools/content_builder`) that
emits full HTML into `dist/`. Source copy lives under `content/`.

## Pull request reviews

For every pull request code review, load and follow
`.github/skills/code-review/SKILL.md` (priorities, repo constraints, finding
format, and verdict). Prefer that skill over generic review style.

## Always-on site rules

- Content pages are full static HTML documents; do not introduce a React SPA or
  client router for content, and do not set title/description/canonical at runtime.
- Landings (`public/{locale}/index.html`) are hand-authored; do not emit them
  from Markdown.
- No hreflang; canonicals are self-referencing only.
- Do not change user-facing copy unless the change explicitly asks for it.
- Build and preview via the Python content builder and `dist/`; do not add an
  npm/Vite content toolchain.
