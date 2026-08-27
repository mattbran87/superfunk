# Self-apply the cross-section check to your own hand-fixes

When you hand-fix content describing a routing, trigger, or lifecycle mechanism outside a workflow that runs the cross-section check automatically, run the check yourself against your own fix — and expect a second round to catch what the first missed.

## Context

`writing-plans`' Self-Review item 8 and `re-review-prompt.md`'s carve-out both apply the same grep-and-read discipline automatically: a plan-writer runs Self-Review on new tasks, and a dispatched re-reviewer runs the carve-out on a fix diff. Neither mechanism covers a controller's own hand-edits made outside those workflows — for example, fixes applied directly during a final whole-branch review. Nothing prompts the controller to re-apply the same discipline to itself, so a hand-fix to mechanism-describing content is exactly as likely to leave a sibling mention contradicted as any other edit to that content.

## Pattern

Before finalizing a hand-edit to content matching the cross-section trigger (language like "if X exists, proceed to...", "triggered by...", "never run standalone," or a cross-reference like "see Y, below"), grep the same file — and any sibling file or design spec that also describes the mechanism — for every other mention of the key terms, and read each hit. Do this even when the edit itself is a fix for a cross-section finding: fixing the one contradiction a reviewer named does not guarantee no other contradiction exists. Plan on a follow-up re-review round specifically to check for a second instance the first pass missed, rather than assuming one pass converges.

## Example

- `cross-section-mechanism-consistency`'s own final-review fix wave (commit `99ed48c`) reconciled `re-review-prompt.md`'s Scope section and one line of `subagent-driven-development/SKILL.md` with the newly-shipped carve-out. A scoped re-review of that fix wave then found a second unqualified diff-only statement still standing in each of the same two files — the Red Flags table's "go to the ledger, not the loop," and the prompt's own opening "nothing else" — closed only in a follow-up round (commit `3d75180`).

## Originating lessons

- "A newly-shipped cross-section check doesn't apply itself to the fixes that ship it" (2026-08-26-cross-section-mechanism-consistency)
