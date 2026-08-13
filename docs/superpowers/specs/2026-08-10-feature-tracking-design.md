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
- **Status** — `spec.md`'s `Status:` line stays the single authoritative source. `roadmap.md` never carries a status column. The vocabulary stays closed: `Planned`, `In Progress`, `Done`, `Deferred` (intentionally postponed, not abandoned), `Dropped` (abandoned) — the last two borrowed from Casita's real, proven usage. `Blocked` does not appear here; it exists only as the derived `blocked`/`blocked_reason` signal from Dependencies, avoiding two competing signals for the same concept. `rebuild_index.py` warns (non-blocking) on any Status outside this vocabulary. When a feature becomes `Done`, add a separate `**Completed:** YYYY-MM-DD` line — kept as its own field rather than embedded in the Status string, for reliable parsing; not yet indexed in SQLite.
- **SQLite index** (`.superfunk/tracking.db`, gitignored) — `.superfunk/rebuild_index.py` walks every `spec.md` and rebuilds the index from scratch. Queries answer "is X complete" directly.
- **Dependencies** — `spec.md`'s `Dependencies:` line names other features by title (not path), comma-separated, spanning every module — a dependency can live anywhere, or not be filed yet at all. The rebuild script resolves each title and derives `blocked`/`blocked_reason` per feature: a matched, `Done` dependency clears it; a matched, not-`Done` dependency blocks it and names the status; an unmatched title blocks it as "not filed yet"; a title matching more than one feature blocks it as ambiguous. Nothing gets manually typed as blocked — it derives from the same source of truth as everything else in the index.
- **Templates** — `specs/_template/` holds the scaffold: `spec.md`, `tasks.md`, `decisions.md`, `notes.md`, and `roadmap.md` for a brand-new module.
- **Generated status summary in `roadmap.md`** — `rebuild_index.py` patches a `## Status Summary` table into each module's `roadmap.md`, between `<!-- status:start -->` and `<!-- status:end -->` markers. The table lists every feature with its Bundle and Status, in the same order as the file's own hand-authored Bundle/link structure — not an arbitrary database order. The markers insert automatically, right after the H1, the first time the script runs against a `roadmap.md` that doesn't have them yet, so the mechanism also works retroactively on files created before this addition. The script never touches anything outside the markers. `spec.md`'s `Status:` line stays the single authoritative source; this table only mirrors it for scanning.
- **Multi-file scaling split (built)** — a module's `roadmap.md` passing roughly 150 lines gets flagged by `rebuild_index.py` with a non-blocking warning naming the module and pointing at `.superfunk/split_roadmap.py --module <module>`. That command performs the actual split, on request, not automatically: it turns `roadmap.md` into an index file (the H1, the generated Status Summary aggregated across every bundle file, and a new generated Bundles table — `Bundle | Features | Status | File`, marker-patched the same way the Status Summary already is) and moves each bundle into its own `specs/<module>/roadmap-<bundle-slug>.md`, holding that bundle's heading and feature links — the same shape the body of `roadmap.md` held before the split. `rebuild_index.py` and `add_feature.py` both became split-aware: a split module's status/count aggregation reads across every bundle file (self-healing a bundle file that exists on disk but isn't in the table yet), and filing a new feature writes into the correct bundle file instead of the index. This trigger and target shape scale down `claude-spec-framework`'s own real split: spec `115-roadmap-multifile-decomposition` split a 2,213-line flat, whole-project roadmap into an index plus per-group and per-category files once scanning it stopped working. `superfunk` already avoids that failure mode's root cause for one dimension — a module boundary already separates roadmaps — so 150 lines gives enough room for a module to grow before the same problem repeats at a smaller scale. See `docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md` for the full mechanics and `docs/superpowers/plans/2026-08-12-roadmap-multifile-split-automation.md` for the build and test record.

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
- **Resolved 2026-08-10:** dependency tracking and a closed status vocabulary, added after comparing this design against Casita's real, battle-tested roadmap format (`ArcGISProSDKMCP`, `ArcGISRuntimeMCP`, and `claude-spec-framework`'s own dogfooded roadmap). That comparison raised four questions, ranked by how foundational each is. Three are resolved: the ID scheme stays date-slug, not Casita's sequential numeric IDs (discussed and confirmed); dependency tracking is built; and the status vocabulary is now closed to five values, with `Blocked` removed in favor of the derived signal.
- **Resolved 2026-08-11:** the status-in-roadmap tradeoff, the fourth question from that same comparison. A `branching-research` pass generated 30 ideas across 5 frames and scored them; the calibrated recommendation leaned toward deferring the decision, since no real feature existed yet to test against and the AI agent stayed the sole status-checker all session. The user weighed the steelmanned case for building the generated block immediately, since validating it stays cheap while the project stays simple, and chose that path over the leaning recommendation. The generated status-summary block above implements it. Testing in disposable fixtures found and fixed two real defects before they reached the repo: a regex collision where `add_feature.py`'s instructional-comment stripper would have matched the new markers, and a double-blank-line artifact in the marker auto-insertion path.
- **Resolved 2026-08-11:** the multi-file scaling split, the fifth and final question from that comparison. `claude-spec-framework`'s real history — spec `115-roadmap-multifile-decomposition`, which split a 2,213-line flat roadmap into an index plus per-group and per-category files once it grew unwieldy — gave a proven pattern to scale down rather than design from scratch. `superfunk` documented the trigger (~150 lines per module's `roadmap.md`) and the target shape (an index file with a Bundles table, one `roadmap-<bundle-slug>.md` per bundle) above, deliberately without building the split logic yet, since no module in `specs/` approached the threshold at that point. This matched `claude-spec-framework`'s own deferral of its template guidance (decision D7) until the pattern proved out in practice. All five items from the ranked Casita-comparison list carried a resolution at that point.
- **Resolved 2026-08-12:** the multi-file scaling split's automation itself, once you asked to build it for real rather than leave it deferred. `.superfunk/split_roadmap.py`, plus split-awareness in `rebuild_index.py` and `add_feature.py`, now implement the design documented above. Three rounds of code-quality review across the three files, each followed by a real fix, closed real gaps before they shipped: silent data loss if `roadmap.md` held content outside the recognized grammar, a stalled split that could get stuck showing a placeholder status forever, an empty-slug bundle name, a common workflow (filing two features into one brand-new bundle before a rebuild) that the first version blocked outright, and a stale Bundles-table reference that crashed instead of failing cleanly. A final cross-file review, run after all three files' individual reviews passed, caught the last of those — confirming per-file review alone doesn't catch everything once multiple files interact, the same reason this project's review discipline always adds a final holistic pass. See `docs/superpowers/specs/2026-08-12-roadmap-multifile-split-automation-design.md` and `docs/superpowers/plans/2026-08-12-roadmap-multifile-split-automation.md`.

## Deferred (per the earlier scoping decisions)

Change tiers, phase gates with sign-off, and the deeper feature-scoping/brainstorm process (closer to Casita's `/brainstorm`) each get their own dedicated workflow, not bundled into this decision.
