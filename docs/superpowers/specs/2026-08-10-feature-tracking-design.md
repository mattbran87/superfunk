# Feature Tracking — Design

**Date:** 2026-08-10
**Status:** Shipped (validated via `workflows/feature-tracking/`)

## Context

`superfunk` needs Casita's roadmap equivalent, reworked around real codebase organization instead of one flat file. This spec covers the tracking structure, status handling, and feature intake — not the deeper feature-scoping conversation, which the existing brainstorming skill already covers.

This decision ran through the Workflow Validation Process. A four-lens exploration (`multi-lens-research`) and a user-proposed SQLite addition refined it further. See `workflows/feature-tracking/` for the full brainstorm, diagram, criteria, test plan, and trial log behind it.

## Decision

- **Module** — a directory mirroring a real codebase module/package: `specs/<module>/`.
- **`roadmap.md`** — hand-authored catalog per module. Bundles appear as `##` headings, purely organizational, carrying no status of their own. Features appear as links under their Bundle.
- **Feature** — a directory named with the `YYYY-MM-DD-<slug>` convention already used elsewhere in this repo, holding Casita's four files unchanged: `spec.md`, `tasks.md`, `decisions.md`, `notes.md`.
- **Status** — `spec.md`'s `Status:` line stays the single authoritative source. `roadmap.md` never carries a status column.
- **SQLite index** (`.superfunk/tracking.db`, gitignored) — `.superfunk/rebuild_index.py` walks every `spec.md` and rebuilds the index from scratch. Queries answer "is X complete" directly.
- **Dependencies** — `spec.md`'s `Dependencies:` line names other features by title (not path), comma-separated, spanning every module — a dependency can live anywhere, or not be filed yet at all. The rebuild script resolves each title and derives `blocked`/`blocked_reason` per feature: a matched, `Done` dependency clears it; a matched, not-`Done` dependency blocks it and names the status; an unmatched title blocks it as "not filed yet"; a title matching more than one feature blocks it as ambiguous. Nothing gets manually typed as blocked — it derives from the same source of truth as everything else in the index.
- **Templates** — `specs/_template/` holds the scaffold: `spec.md`, `tasks.md`, `decisions.md`, `notes.md`, and `roadmap.md` for a brand-new module.

## Feature Intake Procedure

`.superfunk/add_feature.py --module <module> --bundle <bundle> --feature "<Feature Name>" [--rebuild-index]` automates this procedure deterministically. A person or agent still decides which module and bundle a feature belongs to. The script then executes the mechanical part without improvising markdown. This closes the bug class Trial 2 found in the fully manual version (see Follow-ups).

The steps the script automates:

1. Pick the module: an existing `specs/<module>/` directory, or create one with a fresh `roadmap.md`.
2. Pick the Bundle: an existing heading, or a new one.
3. Create `specs/<module>/<YYYY-MM-DD-slug>/` from `specs/_template/`.
4. Set `spec.md`'s `Status:` line to `Planned`.
5. Add a link for the feature under its Bundle heading in `roadmap.md`, matching the format `[Feature Name](./<feature-dir>/)`. Remove the template's instructional comment once the module has its first bundle and feature.
6. Rebuild the SQLite index. This step stays optional at this stage, since a `Planned` feature carries no urgency — pass `--rebuild-index` to run it in the same step.

## Flow

```mermaid
flowchart TD
    subgraph Intake["Add a feature"]
        A1[Pick the module] --> A2{Module exists?}
        A2 -->|No| A3[Create specs/module/ + roadmap.md]
        A2 -->|Yes| A4[Pick the Bundle]
        A3 --> A4
        A4 --> A5{Bundle heading exists?}
        A5 -->|No| A6[Add ## Bundle heading]
        A5 -->|Yes| A7[Scaffold feature dir from template]
        A6 --> A7
        A7 --> A8[Set spec.md Status to Planned]
        A8 --> A9[Link feature under Bundle in roadmap.md]
    end

    subgraph Update["Update status"]
        B1[Edit spec.md Status line]
    end

    A9 --> D1
    B1 --> D1

    subgraph Query["Answer: is it complete?"]
        D1[Run the rebuild command] --> D2([Query .superfunk/tracking.db])
    end
```

## Falsifiable Criteria (validated)

1. **Intake correctness** — Passed (Trials 1-2). A fresh-module intake exposed two real defects (an inconsistent roadmap link format and a leftover instructional comment) that a pre-populated fixture had papered over. Fixed in `specs/_template/roadmap.md` and re-verified with a clean re-run.
2. **Index accuracy** — Passed (Trial 3). Every query matched its feature's actual `spec.md` Status line exactly, across 5 features spanning 2 modules, 3 bundles, and 4 status values, with zero mismatches.
3. **Git-nativeness preserved** — Passed (Trial 3). `.superfunk/tracking.db` never appeared as trackable in `git status`, confirmed as gitignored.

## Follow-ups Carried Forward (non-blocking)

- No defined home exists yet for a feature spanning multiple modules — flagged during the multi-lens exploration and in the Diagram's Notes, never resolved here.
- No fallback exists for a project not yet organized into modules, including `superfunk` itself today.
- Running the intake procedure via a non-interactive agent session needs write permissions granted up front. Otherwise it stalls on a prompt nobody can answer (Trial 1 finding).
- **Resolved 2026-08-10:** `.superfunk/add_feature.py` now automates the procedure deterministically. Five scenarios verified it before it landed: brand-new module, existing module plus existing bundle, existing module plus new bundle, `--rebuild-index` integration, and a duplicate-feature guard. It structurally eliminates the format-inconsistency bug class Trial 2 found, since the script — not an agent — produces the markdown.
- **Resolved 2026-08-10:** dependency tracking, added after comparing this design against Casita's real, battle-tested roadmap format (`ArcGISProSDKMCP`, `ArcGISRuntimeMCP`, and `claude-spec-framework`'s own dogfooded roadmap). That comparison raised four questions, ranked by how foundational each is. Two are resolved: the ID scheme stays date-slug, not Casita's sequential numeric IDs (discussed and confirmed), and dependency tracking (this entry) is now built. Two remain open for future discussion: the status-in-roadmap tradeoff (`roadmap.md` currently carries no status column, unlike Casita's scannable summary table) and the multi-file scaling split Casita's own roadmap eventually needed once it outgrew a single file.

## Deferred (per the earlier scoping decisions)

Change tiers, phase gates with sign-off, and the deeper feature-scoping/brainstorm process (closer to Casita's `/brainstorm`) each get their own dedicated workflow, not bundled into this decision.
