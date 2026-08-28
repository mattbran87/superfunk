# Process Review Recommendations, Batch 3 — Design

**Date:** 2026-08-28
**Status:** Approved
**User-Facing:** No

## Context

`docs/superpowers/process-reviews/review-after-2026-08-28-superfunk-rebrand-design.md` names four Recommendations, closing a Miss, a Gap, and a Friction note this review synthesized from `refresh-example-workflow`, `documentation`, and `superfunk-rebrand`'s combined Catches:

1. A plan's stated `Expected:` numeric value can drift from what a freshly-run command actually reports — `documentation`'s Task 1 predicted "9/9" tests but shipped 10, and `superfunk-rebrand`'s Task 4 predicted "33" occurrences but the actual grep counted 32 matching lines. Neither `writing-plans`' Self-Review nor any other check catches this drift before execution.
2. The same drift shape shows up one stage earlier too: `superfunk-rebrand`'s own approved spec estimated "135 occurrences across 33 files" without running the real grep, and a later grep measured 116 across 29 — a wrong number written directly into a Decision section.
3. `writing-plans`' Self-Review has no item checking a plan's own document header against the required Plan Document Header template — the gap `docs/patterns/self-review-checks-own-required-template.md` already names, still unaddressed at the mechanism level.
4. `subagent-driven-development/SKILL.md`'s process diagram (the dot digraph near the top of the file) stops at workspace deletion, never depicting Finish's bookkeeping sequence — flagged in both `bug-tracking`'s and `refresh-example-workflow`'s final reviews without action. `refresh-example-workflow` already fixed this exact staleness in the file's prose Example Workflow section; the diagram remains the one illustration in this file that never got the same treatment.

## Decision

**`writing-plans/SKILL.md`'s Self-Review gains two items**, appended after the existing item 9:

```markdown
**10. Verified numeric expectations:** For each step whose `Expected:`
value states a specific count (a test count, a grep match count, a
line count), confirm you ran the actual command during plan-writing
and copied its real output — not an estimate, and not carried over
from an earlier draft after other steps changed. An estimated count
nobody actually ran counts as a plan failure, the same as a
placeholder.

**11. Template compliance:** Does this plan's own document header
match every element the Plan Document Header section above requires
(Goal, Architecture, Tech Stack, Global Constraints)? A required
section silently missing from this plan's own header counts as the
same class of gap as a missing task for a spec requirement.
```

**`brainstorming/SKILL.md`'s Spec Self-Review gains one item**, appended after the existing item 5:

```markdown
6. **Numeric-claim verification:** Does any Context or Decision
section state a specific count (occurrences, files, lines) about the
existing codebase? If so, confirm you ran the actual command and
copied its real output — not an estimate — before finalizing the
spec.
```

**`subagent-driven-development/SKILL.md`'s process diagram** (the `digraph process` block) gets four new nodes inserted between the existing `"Final review clean: delete this plan's workspace"` node and the `"Use superfunk:finishing-a-development-branch"` node, replacing that combined node with a sequence matching the prose Example Workflow's own Finish bracket lines:

```dot
"Final review clean" [shape=box];
"Finish: spec Status flip, tracker update, Recommendation checkbox, notes.md gate" [shape=box];
"Finish: Lessons-learned, concept-index, bug-tracking, documentation check" [shape=box];
"Delete this plan's workspace" [shape=box];
"Use superfunk:finishing-a-development-branch" [shape=box style=filled fillcolor=lightgreen];

"Final findings? ONE fix dispatch, one scoped re-review, adjudicate residuals" -> "Final review clean";
"Final review clean" -> "Finish: spec Status flip, tracker update, Recommendation checkbox, notes.md gate";
"Finish: spec Status flip, tracker update, Recommendation checkbox, notes.md gate" -> "Finish: Lessons-learned, concept-index, bug-tracking, documentation check";
"Finish: Lessons-learned, concept-index, bug-tracking, documentation check" -> "Delete this plan's workspace";
"Delete this plan's workspace" -> "Use superfunk:finishing-a-development-branch";
```

This groups Finish's eight bookkeeping items into two boxes, matching this diagram's own existing convention of condensing multiple actions into one node (e.g. the existing `"Setup: worktree, ledger check, read plan, pre-flight review"` node already does this).

## Falsifiable Criteria

1. A direct read-through of `writing-plans/SKILL.md`'s Self-Review section confirms items 10 and 11 exist, worded identically to the Decision block above.
2. A direct read-through of `brainstorming/SKILL.md`'s Spec Self-Review section confirms item 6 exists, worded identically to the Decision block above.
3. A direct read-through of `subagent-driven-development/SKILL.md`'s `digraph process` block confirms the new node sequence exists exactly as specified, and the old combined `"Final review clean: delete this plan's workspace"` node no longer appears anywhere in the file.
4. `grep -c "Finish:" plugin/skills/subagent-driven-development/SKILL.md` returns 10 — the file's 8 existing prose Example Workflow `[Finish: ...]` bracket lines (confirmed via a direct grep before this spec's own numeric claims got finalized) plus the 2 new diagram nodes this spec adds.

## Consequences

A future plan whose verification step states a specific count without having run the command gets caught during that plan's own Self-Review, before execution starts — closing the exact drift `documentation` and `superfunk-rebrand` each hit independently. A future spec's Decision section carrying an unverified count gets caught one stage earlier, during brainstorming's own Spec Self-Review. A future plan whose header drops a required section (Global Constraints or otherwise) gets caught by the plan's own Self-Review rather than surfacing by accident, as it did for `documentation`. `subagent-driven-development/SKILL.md`'s process diagram now matches its own prose Example Workflow, closing the last of the three staleness spots named across `bug-tracking`'s and `refresh-example-workflow`'s final reviews.

These three new Self-Review items add a small amount of review overhead to every future spec and plan — a real ongoing cost, accepted because each closes a concrete, already-recurring failure shape rather than a hypothetical one.

## Deferred

- A programmatic check verifying a plan's `Expected:` values against real command output (rather than relying on the Self-Review item's manual re-check) — no evidence yet that manual re-checking proves insufficient; revisit if the drift recurs after this spec ships.
- Extending numeric-claim verification to other document types beyond specs and plans (process reviews, bug reports) — no evidence yet this class of drift affects those document types.
