# Cross-check a shared rule's restatements across every file a plan writes it into

When a plan restates the same source-of-truth rule into more than one target file, compare every restatement against every other restatement, not just each one individually against the source.

## Context

A plan sometimes needs to write the same underlying rule into multiple files — a design spec's rule, stated once in prose, might need to land in a reference doc and a skill file, each in its own natural phrasing. Each restatement can independently match the source spec's intent while still drifting from each other, since nothing checks the restatements against one another.

## Pattern

When a plan task restates a rule already stated in another task of the same plan, read both restatements side by side before finalizing either one. Confirm they describe the same underlying logic (same conditions, same structure — e.g. both frame two conditions as independent OR-branches, not one as a tiebreaker scoped to the other's ambiguous case), not just similar wording.

## Example

- `docs/code-standards.md`'s "Lessons vs. Patterns" section and `subagent-driven-development/SKILL.md`'s Finish-step paragraph both state the same Lesson-to-Pattern promotion rule. The plan wrote each independently from the design spec's single source bullet, and the two ended up structurally different (one framed the recurrence tiebreaker as scoped to an ambiguous primary answer; the other framed it as an independent OR-condition). A code-quality review caught the drift only when it happened to check the two files side by side.

## Originating lessons

- "Cross-check a shared rule's restatements across every file a plan writes it into" (2026-08-20-lessons-and-patterns-design)
