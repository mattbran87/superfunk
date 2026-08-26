# Cross-Section Mechanism Consistency — Design

**Date:** 2026-08-26
**Status:** Approved

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-25-concept-index-design.md` left a third open Recommendation: a plan editing one part of a document that describes a mechanism spanning multiple sections needs a check confirming the edit doesn't leave another section contradicting it. The review named this "the single most repeated failure shape in this review period," with no check behind it.

Three real recurrences ground this spec:

- `per-task-outcome-capture`: a fix's own worked-example update contradicted the same commit's own scoping rule.
- `concept-index`: Task 1 needed three consecutive fix rounds chasing one interactive/unattended distinction across Step 1, Step 2, Step 3, and the Hand-editing section of a single skill file — each fix correct in isolation, each leaving a different section out of sync. The final review then needed two more fix rounds for the same shape.
- `process-review-recommendations-batch-2`: the design spec's own Decision bullet and its Falsifiable Criterion 4 contradicted each other after only the criterion got corrected — discovered while executing the very sub-project meant to close out this review period.

Tracing the actual origin of each recurrence shows the Recommendation's literal scope (a `writing-plans` Self-Review item) covers only part of the evidence. `writing-plans`' Self-Review runs once, on a plan's original tasks, before dispatch begins. Most real recurrences happened during fix-round dispatches instead — controller-composed, mid-execution, never passing through `writing-plans` at all: `concept-index`'s Task 1 rounds 2-3, both of its final-review fix waves, and the `process-review-recommendations-batch-2` Criterion 4 fix. A `writing-plans`-only check would miss the majority of the actual problem.

Tracing who performed each fix further narrows the design: some recurrences came from dispatched implementer subagents; others came from the controller fixing directly. `re-review-prompt.md` already runs after every dispatched fix round specifically to catch problems the fix itself introduced — extending its existing checklist reaches the dispatched case without relying on the controller's own self-discipline, the exact gap that produced this Recommendation in the first place.

## Decision

- **`writing-plans/SKILL.md` gains a new Self-Review item 8**, distinct from item 5 (sibling-instruction shape matching) and item 6 (source-rule fidelity) — this concerns a document's own internal sections agreeing with each other after an edit, not an external source or a neighboring instruction's shape:

  ```
  **8. Cross-section mechanism consistency:** Does any task edit content
  describing a routing, trigger, or lifecycle mechanism — language like
  "if X exists, proceed to...", "triggered by...", "never run
  standalone," or a cross-reference like "see Y, below"? If so, grep
  the same target file — and the design spec, if it also describes this
  mechanism — for every other mention of the key terms involved, and
  read each hit. Confirm the edit doesn't leave any of them
  contradicting the new content.
  ```

  The language-pattern trigger makes recognition concrete rather than aspirational: a plan-writer doesn't need to judge whether an edit counts as "cross-cutting" in the abstract — they check whether the edited text itself contains routing/trigger/lifecycle phrasing, a mechanically checkable signal.

- **`re-review-prompt.md`'s "New Breakage in the Fix Diff" section gains a carve-out** to its existing scope discipline ("Do NOT re-review code the fix did not touch"):

  ```
  If the fix diff changes content describing a routing, trigger, or
  lifecycle mechanism (language like "if X exists, proceed to...",
  "triggered by...", "never run standalone," or a cross-reference like
  "see Y, below"), this is the one case where you must look outside the
  diff: grep the rest of the touched file — and the design spec, if the
  plan's Goal line names one — for every other mention of the same key
  terms, and read each hit. A contradiction there is New Breakage, not
  an Out-of-Scope Observation, since the fix itself caused it even
  though the contradicted text sits outside the literal diff.
  ```

  Classifying the finding as New Breakage (not Out-of-Scope) matters mechanically: Out-of-Scope Observations never extend the fix loop; New Breakage does. A contradiction the fix itself introduced belongs in the loop, not ledgered as a someday-maybe.

Both edits share the identical trigger language deliberately — one recognition rule, applied at the two points in the process where a mechanism-describing edit actually happens.

## Falsifiable Criteria

1. A direct read-through of the shipped `writing-plans/SKILL.md` confirms Self-Review item 8 exists with the exact language-pattern trigger and grep instruction.
2. A direct read-through of the shipped `re-review-prompt.md` confirms the carve-out sits in the "New Breakage in the Fix Diff" section, uses the same trigger language, and explicitly classifies a caught contradiction as New Breakage rather than Out-of-Scope.
3. A disposable `--plugin-dir` trial writes a fixture plan whose one task edits a file's routing/trigger language in a way that contradicts a separate, untouched section of the same file. Running Self-Review against that plan catches and flags it before dispatch.
4. A second trial simulates a fix round whose diff introduces the same kind of contradiction against untouched content in the same file. Dispatching the re-review catches it and reports it as New Breakage, not silently passed or misfiled as Out-of-Scope.

## Consequences

Every plan's Self-Review pass gains one more item; most plans carry no routing/trigger/lifecycle language, so the added cost stays near zero for a typical plan.

Every fix-round re-review gains a conditional exception to its scope discipline, narrowly triggered by the same language pattern — a fix with no cross-cutting language stays exactly as scoped as it does today.

## Deferred

- A proactive File Structure-time check (flagging cross-cutting mechanisms before drafting any task) — deferred in favor of the cheaper, evidence-matched Self-Review-plus-re-review pair; revisit if this recurs after both ship.
- Extending the same check to `task-reviewer-prompt.md`'s first-pass review (not just re-review) — no evidence yet that a first review, as opposed to a fix round, missed this failure shape; only fix rounds did.
