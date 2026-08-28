# Refresh Example Workflow — Design

**Date:** 2026-08-27
**Status:** Approved

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-27-bug-tracking-design.md` left two open Recommendations: refresh `subagent-driven-development/SKILL.md`'s Example Workflow section, and add a check preventing the same staleness from recurring a seventh time. The final review that surfaced this named six Finish additions the example never absorbed — the spec Status flip, tracker update, Recommendation-checkbox step, notes.md gate, Lessons-learned capture, concept-index step, and bug-tracking's ledger scan — jumping straight from "Final reviewer: All requirements met" to workspace deletion. Re-reading the example while brainstorming this spec found a third, deeper instance of the same shape: Task 2's fix round shows no bracket line for the fix-loop's own notes.md logging requirement (append findings before the first fix dispatch), a gap one level below the Finish-sequence gap the process review named.

`docs/patterns/refresh-worked-examples-when-their-process-changes.md`, promoted from this same review period, already states the prospective rule this spec's second half implements: a plan adding a step to a documented multi-step process should check whether a worked example elsewhere in the same file demonstrates that process, and update it if so.

## Decision

**Two content additions to `subagent-driven-development/SKILL.md`'s Example Workflow:**

1. A fix-loop notes.md bracket line, inserted before Task 2's fix-round dispatch:

```
[notes.md: append Task 2 findings — Missing progress reporting; Magic number (100)]
```

2. The Finish sequence, replacing the bare workspace-deletion line with bracket lines showing the real, current sequence — including skip cases, which illustrate what "correctly not applicable" looks like alongside what "fires" looks like:

```
[Finish: spec Status Approved -> Shipped, committed]
[Finish: appended feature-plan-design.md to tracker.md's Specs shipped since]
[Finish: no Recommendation to check off -- this plan didn't trace to a process review]
[Finish: notes.md gate -- Task 2's fix round already logged above, check passes]
[Finish: captured a Lesson in lessons-learned.md; no pattern promoted, one instance so far]
[Finish: no concept-index entry needed -- no skill/feature/significant directory created]
[Finish: no real-and-deferred parked findings -- bug-tracking step skipped]
```

**A new Self-Review item in `writing-plans/SKILL.md`**, item 9, scoped generically to any documented multi-step process and any worked example — not hardcoded to `subagent-driven-development` specifically, matching how item 8 also generalized rather than naming one file:

```
**9. Worked-example currency:** Does any task add, remove, or reorder a
step in a documented multi-step process (e.g., Finish's bookkeeping
sequence, the fix loop)? If so, check whether a worked example
elsewhere in the same file demonstrates that process. If it does,
update it to reflect the change.
```

## Falsifiable Criteria

1. A direct read-through of the shipped `subagent-driven-development/SKILL.md` confirms the Example Workflow shows both the fix-loop notes.md bracket line and the full Finish-sequence bracket lines, worded identically to the Decision block above.
2. A direct read-through of the shipped `writing-plans/SKILL.md` confirms item 9 exists, worded identically to the Decision block above.
3. A disposable `--plugin-dir` trial builds a fixture skill file containing both a documented multi-step process and a worked example demonstrating it. A fixture plan task adds a new step to that process without touching the worked example. Running Self-Review item 9 against this plan catches the omission and reports that the worked example needs updating.

## Consequences

A reader of `subagent-driven-development/SKILL.md`'s Example Workflow now sees the actual Finish sequence this project runs today, including how a skip case reads, not a six-additions-old snapshot.

Every plan whose tasks touch a documented multi-step process gains one more Self-Review check — low-frequency, since most plans don't add or remove a step in an already-documented process; most tasks change unrelated content.

## Deferred

- **Found during this sub-project's own final review:** `subagent-driven-development/SKILL.md`'s process diagram (the dot digraph near the top of the file) also stops at workspace deletion, never depicting any of Finish's bookkeeping steps — the same staleness shape this sub-project fixed in the prose Example Workflow, in a third location within the same file. Left out of this sub-project's scope, since a diagram counts as a different kind of illustration than the prose walkthrough this spec's Decision names. Revisit as its own small follow-up; item 9's wording ("a worked example... e.g., an 'Example Workflow' section") already reads broadly enough to cover a diagram too, needing no wording change — only the diagram content itself needs the fix.
