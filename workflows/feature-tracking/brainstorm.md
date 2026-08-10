# Brainstorm — Feature Tracking

**Date:** 2026-08-10
**Stage:** 0 — Brainstorm

## Prior Art Reviewed

Casita tracked features with one flat `specs/roadmap.md` file plus one `specs/NNN-feature-name/` directory per feature (`spec.md`, `tasks.md`, `decisions.md`, `notes.md`). The flat file became unwieldy as the feature list grew, and it never reflected the codebase's actual module structure. Superpowers ships no roadmap-equivalent at all.

The user sketched a first-principles alternative: organize by codebase module/package. Each module catalogs its Feature Bundles and their child Features; each Feature gets its own spec, and Tasks/Subtasks live inside that spec, not in the module-level catalog.

## Approaches Considered

Four fresh agents researched this problem independently, each through a different lens (Simplicity, Robustness, Minimal-change, Performance/scale). Full comparison lives in the conversation history; summary below.

### Approach A — Simplicity-first

Module dir > `roadmap.md` (Bundle as heading, not a file) > Casita's unchanged four-file feature dir. Status gets typed in two places (`roadmap.md` and `spec.md`), with no sync mechanism.

### Approach B — Robustness-first

Same shape, but status lives only in `spec.md` frontmatter. The catalog derives from that data; nothing authors it independently. Feature identity (an immutable ID) decouples from its module/location, so refactors don't break links.

### Approach C — Minimal-change-first

This nearly matches Approach A. It aims explicitly for the smallest diff from Casita's own pattern. A global `NNN` counter numbers features, to avoid per-module ID collisions.

### Approach D — Performance/scale-first

Same shape, but Bundles shard into real directories past a size threshold. A generated flat index, built by script from frontmatter, gives fast cross-cutting queries at scale. This approach requires new build tooling the project doesn't have yet.

All four independently rejected Bundle as its own file or directory. Bundle stays a heading or tag on Features, never a physical container. That convergence anchors the recommendation below.

## Anti-Pattern Check

- Phase gate ceremony: this design adds no phase gate.
- Dedicated SME or agent: this design introduces no SME or agent. The SQLite rebuild runs as a mechanical command, not a judgment-requiring agent.
- Shared live/dev instruction files: does not apply — this decision concerns tracking data, not the framework's own tooling.

## Recommendation

This recommendation combines elements from multiple approaches. A pre-mortem surfaced a specific gap during the conversation: Approaches A and C leave status to drift silently between `roadmap.md` and `spec.md`, exactly the failure Casita already suffered. The design below closes that gap, and a later refinement (proposed by the user) adds a generated SQLite index to answer completion-status queries without reintroducing that drift risk.

- **Module** — a directory mirroring a real codebase module/package: `specs/<module>/`.
- **`roadmap.md`** — hand-authored catalog per module. Bundles appear as `##` headings, purely organizational, carrying no status of their own. Features appear as links under their Bundle.
- **Feature** — a directory named with this repo's existing `YYYY-MM-DD-<slug>` convention (already used under `docs/superpowers/specs/` and `docs/superpowers/plans/`), reusing Casita's four files unchanged: `spec.md`, `tasks.md`, `decisions.md`, `notes.md`.
- **Status** — `spec.md`'s `Status:` line stays the single authoritative source. `roadmap.md` never carries a status column, so it cannot independently drift from it.
- **SQLite index** (`.superfunk/tracking.db`, gitignored, never committed) — a command walks every `spec.md`, extracts module/bundle/feature/status, and rebuilds the index. Queries like "is spec X complete" run against this index directly, instead of grepping markdown by hand.
- **Rebuild trigger** — an on-demand command for now. An automatic hook (rebuilding on every `spec.md` status change) stays a deferred enhancement, added once the manual version proves itself and once hook infrastructure exists to validate it properly.
- **Bundle**, confirmed with the user: purely organizational grouping, carrying no status or other independent state of its own.

## Rejected Approaches

Approach A / C as originally proposed both leave status to drift between two hand-typed copies with no structural protection. Making `spec.md` the sole authoritative source and dropping status from `roadmap.md` entirely supersedes both.

Approach D's generator, sharding, and archival machinery: premature to build now, since this project has zero build tooling today. The core idea — a generated, queryable index — survives in the recommendation, but as a lightweight SQLite command rather than Approach D's fuller flat-file-plus-archival system.

This design rejects SQLite as the source of truth, where status would live only in the database. That approach breaks the git-native, diffable, human-readable property every other artifact in this framework already has. It would also require every tool or agent to hold database access just to know a feature's state, instead of reading a file.
