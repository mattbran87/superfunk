# Continuous Improvement — Process Review — Design

**Date:** 2026-08-19
**Status:** Approved, not yet implemented

## Context

Casita runs continuous improvement on four related mechanisms: Process Review, Lessons, Patterns, and Group Retrospectives. Process Review runs periodically and produces evidence-based findings. Lessons capture per-spec retrospective facts. Patterns hold promoted, reusable rules. Group Retrospectives reflect at the project-delivery level. This spec ports the first mechanism only: Process Review.

Casita triggers a review after every 3 completed Standard or Full-cycle specs. Each spec captures Process Notes (Catches, Misses, Friction, Gaps) inline in its `notes.md` during Implementation and Testing. The review produces a file. That file's Recommendations block the next roadmap group until each gets an action or an explicit deferral. Real evidence backs this pattern. Three shipped review files exist in Casita's history. Recommendations R1 and R2 from one review shipped as a real follow-up fix — the loop from review to change closed in practice, not just on paper.

superfunk's design specs (`docs/superpowers/specs/`) carry no per-spec companion notes file. Reconstructing review input purely from `git log` has a real gap. This project's git conventions already require a fix commit to name what a review caught, so `git log` captures Catches reliably. It loses Friction and Gaps that never produce a commit: a redirect mid-brainstorm, or a live trial that needed multiple attempts to get its methodology right. Those exist only in conversation. Conversation compacts away. `docs/principles.md`'s Artifacts Over Memory principle names this failure mode directly: work that depends on session memory to stay correct breaks the next time context compacts.

## Decision

- **A running log, not a per-spec file.** `docs/superpowers/process-reviews/notes.md` holds one append-only line per entry. Each entry carries a tag (`Catch`, `Miss`, `Friction`, or `Gap`), a date, the spec or task it relates to, and a one-line description. A single running log fits superfunk's spec-level granularity better than Casita's per-spec `notes.md` — superfunk tracks work at the spec level, not the per-feature level Casita's `notes.md` served. It also needs no new file per design spec.

- **The logging trigger.** `plugin/skills/subagent-driven-development/SKILL.md`'s review loop already runs three reviews: spec-compliance, code-quality, and — after all tasks complete — a holistic review across the whole diff. Any of the three can return issues and trigger a fix round. Add an instruction: when a review returns issues instead of approving outright on the first pass, append one line to `docs/superpowers/process-reviews/notes.md` before starting the fix round. This ties logging to a concrete, already-occurring pipeline event — a review finding something wrong the first time. It replaces an open-ended judgment call ("does this count as loggable?") with a fixed trigger Claude doesn't have to remember to apply.

- **The tracker.** `docs/superpowers/process-reviews/tracker.md` records the last review's spec filename and date, plus the list of design specs shipped since. `plugin/skills/subagent-driven-development/SKILL.md`'s Finish step appends the just-shipped spec's filename to this list, immediately after it updates that spec's `Status` to `Shipped`.

- **Trigger point A — Finish step.** When the "shipped since" list reaches 3 entries, the Finish step offers to run `process-review` immediately. This matches the ask-don't-force pattern the human-in-the-loop review checkpoint already uses. The user can run it now, or defer it.

- **Trigger point B — brainstorming's "Explore project context" step.** This step checks the tracker before a new sub-project's design begins. Two independent conditions can trigger it: a review due (3+ specs shipped since last review, never run), or an open Recommendation in the last review file (an unchecked `- [ ]` item). Surface both, if both apply. Ask the user to act on each, or explicitly defer it, before continuing. A deferred Recommendation gets its `(deferred: <reason>)` note beside the item in the review file (see Recommendation lifecycle, below) — a deferred review-due check gets its note in the tracker instead, since it has no per-item home of its own.

- **The review procedure — a new skill, `plugin/skills/process-review/SKILL.md`.** Both trigger points invoke this shared procedure instead of duplicating it:
  1. Read `docs/superpowers/process-reviews/notes.md`, filtered to entries dated after the tracker's last-review date.
  2. Cross-reference `git log` across the shipped specs' commits. This confirms each logged entry, and catches any Catch a fix-commit message names that the running log missed.
  3. Write `docs/superpowers/process-reviews/review-after-<last-spec-slug>.md`, with six sections: **Specs Reviewed**, **Catches**, **Misses**, **Friction**, **Gaps**, and **Recommendations**. Each Recommendation gets a checkbox item (`- [ ] ...`) naming a target file and the exact change.
  4. Update the tracker: write a new last-review entry, and clear the "shipped since" list.

- **Recommendation lifecycle.** A Recommendation stays open until someone checks its box. Checking happens two ways: making the named change (checked off in the same commit), or the user explicitly deferring it at brainstorming's gate. A deferral adds a `(deferred: <reason>)` note beside the item without checking the box. A deferred Recommendation keeps surfacing at every future gate until someone resolves it or removes it explicitly.

## Falsifiable Criteria

Same disposable `--plugin-dir` baseline-trial approach used for every other wiring change this session:

1. Build a scratch fixture with a pre-seeded `notes.md` (3 fake log entries) and no tracker file. Trigger `subagent-driven-development`'s Finish step for a 3rd shipped spec. Confirm it detects the threshold and offers to run `process-review`.
2. Using the same fixture, run `process-review` directly. Confirm it produces a review file with all five sections populated from the log entries. Confirm it updates the tracker.
3. Build a scratch fixture with a tracker that names a review overdue, plus a review file with one unchecked Recommendation. Trigger `brainstorming`'s "Explore project context" step. Confirm it surfaces both the overdue review and the open Recommendation, and waits for an explicit act-or-defer answer before continuing.

## Consequences

Every review loop that finds an issue on its first pass now writes one extra line to a running log. This adds a small, mechanical step to an already-occurring event, not a new judgment call.

Friction and gaps that never trigger a formal review still go uncaptured — a user redirect mid-conversation, for instance. This spec accepts that gap rather than logging every user correction. The chosen trigger ties logging to a concrete pipeline event, not an open-ended friction judgment.

`docs/superpowers/process-reviews/notes.md` grows without bound between reviews. Each review clears the reviewed window, so entries older than the last review stay historical — a future review does not re-read them.

The `process-review` skill assumes at least one prior shipped spec exists to review. The very first review, with no prior tracker entry, reviews from the beginning of `docs/superpowers/process-reviews/notes.md`'s history.

## Deferred

- Lessons, Patterns, and Group Retrospectives — the other three mechanisms in Casita's continuous-improvement system, not ported in this pass.
- Logging user-initiated redirects (corrections made mid-brainstorm or mid-execution, outside a formal review loop) — considered and explicitly declined for this pass; revisit if Friction/Gaps prove too sparse to produce useful reviews without them.
- A different cadence than every 3 shipped specs, if 3 proves too frequent or too sparse once evidence accumulates.
