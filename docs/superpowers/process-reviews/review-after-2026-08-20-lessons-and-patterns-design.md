# Process Review — after 2026-08-20-lessons-and-patterns-design.md

**Date:** 2026-08-20

## Specs Reviewed

- 2026-08-19-process-review-design.md
- 2026-08-20-pseudocode-during-planning-design.md
- 2026-08-20-lessons-and-patterns-design.md

## Catches

**2026-08-19-process-review-design.md**
- Task 2: the `process-review` skill's own Step 4 dropped the design spec's required "Specs Reviewed" section, and its Self-Review check only verified trigger presence, not format or reason quality.
- Final review: the design spec's Falsifiable Criteria and the plan both retained a stale "five sections" count after the Decision section was corrected to six.

**2026-08-20-pseudocode-during-planning-design.md**
- Task 1: the Pseudocode section had no worked example, only abstract rules.
- Task 1: Self-Review's Pseudocode check verified trigger presence only, not format or reason quality.
- Task 2: the Pseudocode context dispatch bullet gave no method for matching a task to its triggers.
- Task 2: the Pseudocode context bullet lacked the why-explanation and visibility requirement its Directory context sibling has.
- Final review: multi-task-same-trigger attribution stayed undefined — a dispatch could fold another task's pseudocode into the wrong task's context.
- Final review: both Task 1 and Task 2 needed a fix round for similar gaps, traced to the plan's own drafted text, not implementer error.

**2026-08-20-lessons-and-patterns-design.md**
- Task 2: the promotion-rule bullet dropped "that applies across many future situations" from the design spec's exact phrasing.
- Task 3: `<spec-slug>` had no fallback for the no-design-spec Finish branch.
- Task 3: the promotion-rule framing drifted from `docs/code-standards.md`'s independent-OR structure.
- Task 4: the lessons/patterns reading bullet had no visibility clause, unlike its `.context.md` sibling.
- Final review: three fix rounds traced to the plan restating the same design-spec rule in two different tasks without cross-checking the restatements against each other.

## Misses

- **A new bullet added next to an existing sibling bullet repeatedly failed to mirror that sibling's established pattern** (why-explanation, visibility/note-what-you-checked clause). This recurred across two of the three reviewed specs: pseudocode-during-planning's Task 2 (missing Directory context's why/visibility shape) and lessons-and-patterns' Task 4 (missing `.context.md`'s visibility shape). Both needed a fix round to add what the sibling bullet already had. Nothing in `writing-plans` currently checks for this before a plan ships.

## Friction

- **lessons-and-patterns**: three of its four editing tasks (Task 2, Task 3, Task 4) needed one fix round each — a 75% fix-round rate across editing tasks in a single sub-project.
- **pseudocode-during-planning**: both editing tasks (Task 1, Task 2) needed a fix round, plus a third fix round at final-holistic-review stage — every editing task in this sub-project needed at least one round.
- Across both sub-projects, tasks that only created new files (seed-artifact tasks) needed zero fix rounds; tasks that wrote Find/Replace text into an existing fork skill file needed a fix round in 5 of 6 cases. This split is worth watching as a real signal, not yet as a proven cause.

## Gaps

- **No plan-writing check for sibling-pattern parity.** When a plan adds a new instruction next to an existing one in the same target file, nothing checks whether the new instruction mirrors the existing one's established shape before implementation starts — only code-quality review has caught this, every time it happened.
- **No plan-writing check for cross-file rule restatement.** When a plan writes the same underlying rule into more than one target file, nothing checks the restatements against each other before implementation starts — only a code-quality review that happened to compare both files caught this. A Pattern was promoted for this exact gap this session (`docs/patterns/cross-check-shared-rule-restatements.md`), but promoting a Pattern records the rule — it doesn't yet operationalize a check for it inside `writing-plans` itself.

## Recommendations

- [x] Add a check to `plugin/skills/writing-plans/SKILL.md`'s Self-Review section: when a plan adds a new instruction next to an existing sibling instruction in the same target file, confirm the new instruction mirrors the sibling's established shape (why-explanation, visibility clause) before finalizing the plan. (Shipped as Self-Review item 5, commit `7992e30`.)
- [x] Add a check to `plugin/skills/writing-plans/SKILL.md`'s Self-Review section: when a plan restates the same source rule into more than one target file, cross-check every restatement against every other restatement before finalizing — this directly operationalizes `docs/patterns/cross-check-shared-rule-restatements.md` as an actual plan-writing check, not only a recorded Lesson. (Shipped as Self-Review item 6, commit `7992e30`.)
