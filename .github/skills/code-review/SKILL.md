---
name: code-review
description: >
  Strict code review for the Python content site builder. Use when reviewing
  PRs or diffs for correctness, build integrity, security, tests, or regressions
  in tools/content_builder, templates, sitemaps, URL helpers, or generated site
  output.
---

# Code Review

## Purpose

Perform strict, thorough automated code reviews for this repository.

The repository is a Python-based content site builder. Reviews should identify
meaningful problems in correctness, reliability, architecture, maintainability,
performance, security, testing, and compatibility.

Prioritize real, actionable issues over stylistic preferences or speculative
concerns.

## Repo Constraints

Flag PRs that violate site invariants:

- Do not rewrite content delivery as a React SPA or client-route content pages
- Do not set title, meta description, or canonical at runtime for content pages
- Do not emit landing `index.html` from Markdown; landings stay hand-authored under `public/`
- Do not add hreflang or canonicalize one locale to another
- Do not change user-facing copy (Markdown under `content/`, landing HTML text,
  chrome/nav/footer strings, template labels) unless the PR explicitly asks for it
- Prefer Python tooling for content build; do not introduce an npm/Vite content toolchain
- `dist/` is the deployable site; local preview must serve that same static tree

## Review Priorities

### Correctness

Check for:

- Incorrect logic and assumptions
- Edge cases
- Incorrect error handling
- Unexpected side effects
- Incorrect filesystem or path handling
- Broken content parsing or transformation
- Incorrect template rendering
- Incorrect URL generation
- Metadata corruption or loss
- Incorrect build or incremental-build behavior

Pay particular attention to bugs that could silently generate incorrect site
output.

### Reliability

Check behavior when encountering:

- Missing files
- Malformed content
- Invalid configuration
- Unexpected input
- Encoding problems
- Filesystem failures
- Partial build failures

Flag nondeterministic behavior, fragile ordering assumptions, race conditions,
and environment-dependent behavior.

### Design and Architecture

Look for:

- Poor separation of responsibilities
- Excessive coupling
- Leaky abstractions
- Duplicated logic
- Unnecessary global state
- Excessively complex functions or modules
- Behavior implemented at the wrong abstraction layer

Prefer simple, composable designs with clear interfaces.

### Maintainability

Flag meaningful instances of:

- Confusing naming
- Excessive nesting
- Hidden side effects
- Dead or duplicated code
- Magic values
- Unnecessary complexity
- Difficult-to-understand control flow

Do not report purely stylistic preferences.

### Python

Check for Python-specific problems including:

- Mutable default arguments
- Overly broad exception handling
- Incorrect context-manager usage
- Resource leaks
- Problematic import patterns
- Incorrect iterator or generator behavior
- Misleading or incorrect type annotations
- Unnecessary reimplementation of standard-library functionality

Prefer idiomatic Python when it improves correctness or maintainability.

### Performance

Look for meaningful performance problems such as:

- Repeated filesystem access
- Repeated parsing or rendering
- Unnecessary rebuild work
- Accidental quadratic behavior
- Work performed for every page when it could be scoped more narrowly
- Excessive allocations or conversions

Pay particular attention to operations that scale with the number of pages,
assets, templates, links, or files.

Do not suggest insignificant micro-optimizations.

### Security

Check for:

- Path traversal
- Unsafe file writes
- Command injection
- Unsafe subprocess usage
- Unsafe deserialization
- Template or HTML injection
- Improper escaping
- Secret exposure
- Unsafe temporary-file handling
- Unvalidated filesystem paths or external input

### Build and Content Integrity

Consider:

- Full builds
- Incremental builds
- Clean builds
- Repeated builds
- File deletion
- File renaming
- Cache invalidation
- Dependency tracking
- Stale generated output
- Deterministic output

Look for situations where content, metadata, links, files, or generated output
could be lost, duplicated, corrupted, skipped, or become stale.

### Compatibility

Look for unintended breaking changes to:

- Existing content
- Configuration
- Templates
- Plugins
- CLI behavior
- Python APIs
- Generated output
- Filesystem layout

### Tests

Check whether changed behavior is adequately tested.

Pay particular attention to:

- New behavior
- Bug fixes
- Regression cases
- Edge cases
- Failure paths

Flag tests that are brittle, misleading, nondeterministic, excessively mocked,
or unable to catch the behavior they claim to test.

Do not demand tests for trivial changes where they provide little value.

## Review Rules

Only report issues that are meaningful and actionable.

Do not:

- Invent hypothetical problems unsupported by the code
- Report cosmetic style preferences
- Request refactoring merely because another design is possible
- Flood the review with low-value nitpicks
- Repeat multiple symptoms caused by the same root problem
- Assume code is broken without identifying a concrete failure mode

Before reporting an issue, consider whether surrounding code, validation,
tests, or repository invariants already address it.

When uncertain, clearly state the assumption required for the issue to occur.

## Findings

For each finding provide:

**Severity:** Critical | High | Medium | Low

**Problem:** A concise description.

**Location:** Relevant file and line or code region.

**Impact:** Explain why the problem matters and give a concrete failure mode.

**Recommendation:** Explain how it should be corrected.

Severity definitions:

- **Critical** — security vulnerability, data loss, arbitrary code execution,
  destructive behavior, or similarly catastrophic defect.
- **High** — clear correctness bug, major regression, broken build, corrupted
  output, or serious security/reliability problem.
- **Medium** — genuine reliability, maintainability, performance, compatibility,
  or edge-case defect.
- **Low** — small but legitimate problem with limited impact. Use sparingly.

## Verdict

Finish with exactly one verdict:

- `APPROVE` — no meaningful issues found.
- `COMMENT` — only non-blocking issues found.
- `REQUEST CHANGES` — at least one issue should be fixed before merge.

Prioritize precision over quantity. Three genuine findings are more useful than
twenty speculative or cosmetic comments.
