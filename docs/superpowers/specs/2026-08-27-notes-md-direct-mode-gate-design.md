# Notes.md Direct-Mode Gate — Design

**Date:** 2026-08-27
**Status:** Shipped

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-27-cross-section-recursion-boundary-design.md` named its only Recommendation: `notes.md` received zero real-time entries across three consecutive specs, despite genuine findings in two of them. The existing gate in `subagent-driven-development/SKILL.md`'s Complete-the-task step only fires "if this task's fix loop ran at least one round" — a condition scoped to the dispatched-implementer-then-reviewer cycle. All three specs the review covers ran through a different path: this session's Agent-tool subagent spawn limit forced the controller to implement and review every task directly, so no fix loop, in the structural sense the gate checks for, ever ran, even when real findings occurred (a Falsifiable Criterion scoping error and a missing citation, both in `cross-section-negative-case-trials`, both caught and fixed without a matching `notes.md` entry).

## Decision

The gate's trigger condition widens with an OR clause covering direct implementation:

```
If this task's fix loop ran at least one round, or if you implemented
and reviewed this task directly — without dispatching an implementer
subagent — and caught a real issue during that direct review, run
`grep -c "Task <N> (<plan-slug>)" docs/superpowers/process-reviews/notes.md`
to confirm at least one entry exists — a task whose review passed
clean on the first pass, dispatched or direct, never triggers this
check. If the grep returns 0, append one entry now for each finding
you caught, naming the specific finding (not "review findings
addressed" or "issues fixed"), using the findings you already have:
```

This does not encourage direct implementation as a routine alternative to dispatch — `subagent-driven-development/SKILL.md` already discourages controller self-fixing outside genuine exceptions (`"Controller fixes pollute your context and skip review. Resume the implementer."`). This closes the logging gap for when direct implementation happens anyway, for whatever reason, without normalizing it as an equally valid default.

The two real notes.md entries this exact gap already caused get backfilled: `cross-section-negative-case-trials`' Falsifiable Criterion 3 scoping catch (commit `461db45`) and its missing review-file citation catch (commit `ce978c4`), both currently undocumented in `notes.md` despite already appearing in the process review's own Catches section.

## Falsifiable Criteria

1. A direct read-through of the shipped `subagent-driven-development/SKILL.md` confirms the widened trigger condition exists, worded identically to the Decision block above.
2. `docs/superpowers/process-reviews/notes.md` contains an entry for each of the two backfilled catches, matching the established `- <YYYY-MM-DD> | Catch | Task <N> (<plan-slug>) | <finding>` format.
3. A disposable `--plugin-dir` trial dispatches a fresh session told it just implemented a task directly (no subagent dispatch, citing a spawn-limit scenario) and caught and fixed a real issue during that direct review. The session, following the widened Complete-the-task step, runs the grep and — finding it returns 0 — appends a notes.md entry before reporting the task complete.

## Consequences

Every task the controller implements directly, and where that direct review catches a real issue, now needs the same notes.md entry a dispatched fix loop already required — closing the exact gap this session's own recent history demonstrated, at negligible added cost (the same grep-and-append the existing gate already specifies).

A task implemented directly with no real finding (the common case when direct implementation happens at all) triggers nothing new, matching the existing gate's "clean on first pass" exemption.

## Deferred

- Nothing identified. This closes the single Recommendation from the originating review.
