# Brainstorm — Superpowers Fork

**Date:** 2026-08-08
**Stage:** 0 — Brainstorm

## Prior Art Reviewed

Casita split `framework/` (the shipped source of truth) from root `.claude/` (a synced, installed copy), with a sync script and a rule against hand-editing both. That rule did not hold: sessions edited the root copy directly, since that copy drove their actual behavior, and drift crept in anyway.

The current `superpowers` plugin (MIT-licensed, hosted at `github.com/obra/superpowers`) installs globally and drives this very session. It ships 14 skills, plus hooks, scripts, and tests, entirely separate from the `superfunk` repo this session edits.

That separation — this session's own skills live outside `superfunk` entirely — points to the fix Casita's sync script lacked. Make the active plugin structurally unreachable from the repo under development; a rule against touching it does not suffice.

## Approaches Considered

### Approach A

Fork `obra/superpowers` on GitHub with full history, preserving a path to pull upstream fixes later. Import the fork into `superfunk` via `git subtree add`. This avoids root-level collisions (`README.md`, `CLAUDE.md`, `LICENSE`, and `docs/` exist in both repos) and keeps a clean `git subtree pull` path for future syncs.

Development rule: sessions working in `superfunk` always run on the globally-installed `superpowers` plugin, never on `superfunk`'s own in-progress skill files. Reworked skills sit in the repo as inert source until a trial installs them somewhere else.

Testing rule: validating a reworked skill means installing that in-progress build into a separate, disposable local project. This reuses the Workflow Validation Process's existing synthetic-test-project and sandboxed-real-project trial environments — a new skill trial doesn't need a new environment concept, just an instance of one.

### Approach B

Approach B uses the same development and testing rules as Approach A, but imports via `git merge --allow-unrelated-histories` at the repo root instead of subtree. Every root-level filename collision (`README.md`, `CLAUDE.md`, `LICENSE`, `docs/`) needs manual conflict resolution during the initial merge. Each future upstream sync repeats that resolution from scratch, unlike subtree's incremental pull.

## Anti-Pattern Check

- Phase gate ceremony: this decision adds no phase gate.
- Dedicated SME or agent: this decision introduces no SME or agent.
- Shared live/dev instruction files: both approaches satisfy this equally by design — `superfunk` sessions run on the globally-installed plugin, never on the in-repo fork source, and trials only happen in separate, disposable projects.

## Recommendation

Approach A. Subtree import gives the same development and testing isolation as Approach B, with less merge risk now and a cleaner update path later.

## Rejected Approaches

Approach B: the full unrelated-histories merge carries the same isolation benefits as Approach A but with more upfront conflict-resolution risk and no incremental upstream-sync path.

A fully separate fork repo, referenced from `superfunk` rather than merged into it: rejected earlier in this conversation — `superfunk` itself becomes the fork, unifying the framework's process docs and its tool implementation in one repo.
