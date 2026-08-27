# Bug Tracking — Design

**Date:** 2026-08-27
**Status:** Shipped

## Context

Superfunk has no process for tracking bugs, in three concrete ways:

1. **Deferred findings disappear.** `subagent-driven-development`'s task-level fix loop and final whole-branch review both record real-but-deferred findings as "parked" or "deferred minor" lines in `<workspace>/progress.md` (the ledger) — a file scoped to `.superpowers/sdd/<plan-basename>/`, git-ignored, and deleted by Finish's own last step (`rm -rf <workspace>` — "the git history is the record now"). The ledger text itself never enters git history; only the commit SHAs it references do. A finding real enough to survive adjudication as "park it, ruling: real and deferred" currently has no durable home once the workspace goes away.
2. **No process exists for reporting a bug found after a sub-project ships.** A human or a later session with nowhere to record a newly-discovered defect against already-shipped work.
3. **No severity/priority triage mechanism exists** — even a recorded finding has no structured way to signal urgency or track its resolution state over time.

This needs to work as a framework-level skill: the same shape every project adopting superfunk gets, operating on that project's own repository — the same pattern `writing-plans` and `brainstorming` already use (they save to the invoking project's `docs/superpowers/plans/` and `docs/superpowers/specs/`, not superfunk's own). Superfunk dogfoods this same skill on itself.

The user explicitly does not want a single-platform-specific design: some projects use GitHub Issues, others (including the user's own work) use Jira. The schema and process need to stay platform-agnostic at their foundation, transferable to whatever external tracker a project's team actually uses — without building that transfer mechanism now, before any concrete need names which platform to target.

## Decision

**A new skill, `bug-tracking`,** owns the schema, numbering, and file-creation process in one place, so both callers below follow identical logic rather than each restating it independently (the exact "same rule stated twice, drifts apart" failure shape this project has fixed repeatedly elsewhere).

**File structure**, created in the invoking project's own repository:

- `docs/bugs/tracker.md` — an index table (columns: ID, Title, Severity, Status, link), giving the at-a-glance triage view Gap 3 names, the same role `docs/superpowers/process-reviews/tracker.md` already plays for process reviews.
- `docs/bugs/BUG-<NNNN>-<slug>.md` — one file per bug, mutable in place as its status changes (not an append-only log, since a bug follows a lifecycle, not a stream of events).

**Numbering:** the next ID counts existing `docs/bugs/BUG-*.md` files and adds 1, zero-padded to 4 digits — deterministic and git-checkable, with no separate counter file to drift out of sync with the files it counts.

**Schema**, reusing this project's existing Critical/Important/Minor severity vocabulary rather than inventing a second one for bugs specifically:

```markdown
# BUG-0001: <short title>

**Severity:** Critical | Important | Minor
**Status:** Open | Triaged | In Progress | Fixed | Won't Fix
**Origin:** <how it surfaced>
**External ID:** (blank until synced to an external tracker)

## Description

## Reproduction
(if applicable)

## Resolution
(filled in when Status becomes Fixed or Won't Fix — what changed, commit SHA)
```

`External ID` stays blank and unused by this spec — the placeholder a future sync mechanism would populate, not something this spec builds. Keeping it in the schema now makes the design "platform-agnostic at the foundation": any external tracker's issue key fits this one field without a schema change.

**Two callers, one mechanism:**

1. **On-demand reporting.** A human or a session invokes `bug-tracking` directly to record a bug found any time — post-ship, mid-development, wherever. `Origin` reads `Reported <YYYY-MM-DD> by <name or session>`.
2. **Finish-time auto-ledger.** `subagent-driven-development`'s Finish section gains a step, inserted immediately before "Then delete this plan's workspace": read the ledger (`<workspace>/progress.md`) for any `parked` line whose ruling calls the finding real (not "reviewer is wrong" / contestable rulings, which resolve as correctly-not-a-bug), and for each, invoke `bug-tracking` to create a durable entry before the workspace — and the ledger text with it — gets deleted. `Origin` reads `Deferred finding, <ledger line> (plan: <plan-slug>)`.

## Falsifiable Criteria

1. A direct read-through of the shipped `plugin/skills/bug-tracking/SKILL.md` confirms the schema, numbering rule, and file/tracker structure match the Decision block above.
2. A direct read-through of the shipped `subagent-driven-development/SKILL.md` confirms the new Finish-time step exists, sits immediately before the workspace-deletion step, and correctly distinguishes a real-and-deferred parked ruling from a contestable "reviewer is wrong" one.
3. A disposable `--plugin-dir` trial invokes `bug-tracking` directly against a fixture project with no `docs/bugs/` directory yet, reporting one bug. Confirms `docs/bugs/tracker.md` and `docs/bugs/BUG-0001-<slug>.md` both get created with the correct schema and a matching tracker row.
4. A second trial seeds a fixture project with one existing bug (`BUG-0001`) and a fixture plan whose ledger has one real-and-deferred parked finding. Running the Finish-time step correctly creates `BUG-0002` (not colliding with the existing `BUG-0001`) with `Origin` naming the ledger finding and the plan-slug, before the workspace deletion step runs.

## Consequences

Every sub-project's Finish step gains one more check: reading the ledger for real-and-deferred parked findings. Cost stays low — most sub-projects finish with an empty or contestable-only parked list, matching this project's own history this session (nearly every recent sub-project's final review came back clean or with Minors already fixed, not parked).

A project adopting superfunk gets a working, platform-agnostic bug tracker from day one, with a clear seam (`External ID`) for connecting it to whatever tool that project's team actually uses — without superfunk having picked that tool for them.

## Deferred

- Any sync/export mechanism to Jira, GitHub Issues, Linear, or any other external tracker — the schema shapes for it, but no sync code exists yet. Revisit once a concrete project names the specific platform it wants to connect.
- Any dashboard or UI beyond the plain `tracker.md` table.
- A "contestable" parked ruling (reviewer wrong, code stands) does not become a bug — only "real and deferred" rulings do. If evidence later shows contestable rulings sometimes hide real bugs missed at adjudication time, revisit.
- **Found during this sub-project's final review, but pre-existing and out of scope to fix here:** `subagent-driven-development/SKILL.md`'s Example Workflow (its worked-example walkthrough near the file's end) never depicts any of Finish's bookkeeping steps — not the spec Status flip, the tracker update, the Recommendation-checkbox check, the notes.md gate, the Lessons-learned capture, the concept-index step, or now the bug-tracking step. It jumps straight from "Final reviewer: All requirements met" to workspace deletion. This predates bug-tracking — none of the five prior Finish additions updated it either — so a proper fix means refreshing the whole worked example in one pass, not patching in one more missing line. Revisit as its own small sub-project.
