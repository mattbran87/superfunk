# Writing-Plans Self-Review Checks — Design

**Date:** 2026-08-20
**Status:** Shipped

## Context

The first real process review (`docs/superpowers/process-reviews/review-after-2026-08-20-lessons-and-patterns-design.md`) found two Recommendations. Both trace to real fix rounds this session already paid for. One Miss recurred across two specs: a new instruction, added next to an existing sibling instruction in the same target file, repeatedly failed to mirror that sibling's established shape (a why-explanation, a visibility clause). One Gap named a Pattern this session just promoted (`docs/patterns/cross-check-shared-rule-restatements.md`) with no plan-writing check behind it yet — the Pattern records the rule, but nothing in `writing-plans` applies it before a plan ships.

This spec closes both gaps the same way: two new items in `writing-plans`' existing Self-Review section, run by the plan-writer before finalizing a plan, the same way its current four items already work.

## Decision

- **New Self-Review item 5 — Sibling-pattern parity.** When a plan adds a new instruction next to an existing sibling instruction in the same target file, confirm the new instruction mirrors the sibling's established shape (a why-explanation, a visibility clause) before finalizing the plan.
- **New Self-Review item 6 — Cross-file rule restatement.** When a plan restates the same source rule in more than one target file, read every restatement side by side. Confirm they describe the same underlying logic — the same conditions, the same structure — not just similar wording.
- Both items sit in `writing-plans/SKILL.md`'s Self-Review section, after the existing item 4 (Pseudocode coverage), matching that section's own numbered-checklist format exactly.

## Falsifiable Criteria

This spec adds two self-review checklist questions, not executable behavior — a plan-writer applies them by reading and judgment, the same way the existing four items work. No disposable trial applies; the falsifiable test stays direct: grep `writing-plans/SKILL.md` for both new item numbers, and confirm their wording matches this spec exactly.

## Consequences

Every future plan's Self-Review pass gains two more questions to run through. Both work as judgment calls, like the section's existing items — they add reading time, not a new pause or a new file. A plan that never adds a sibling instruction, or never restates a rule across files, answers both quickly with "not applicable" and moves on.

## Deferred

- Retroactively re-checking already-shipped plans against these two new items — this spec applies forward only, from the next plan `writing-plans` produces.
