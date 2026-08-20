# Process Review — Running Notes

Append-only log. Each entry marks one finding a review catches on its
first pass (spec-compliance, code-quality, or the final whole-branch
review), tagged `Catch`. `process-review` reads this log,
cross-references `git log`, and may surface `Miss`, `Friction`, or
`Gap` patterns across entries when it synthesizes a review file.

Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <one-line finding>`

<!-- entries below this line -->
- 2026-08-20 | Catch | Task 1 (pseudocode-during-planning) | Pseudocode section had no worked example, only abstract rules
- 2026-08-20 | Catch | Task 1 (pseudocode-during-planning) | Self-Review's Pseudocode check verified trigger presence only, not format or reason quality
- 2026-08-20 | Catch | Task 2 (pseudocode-during-planning) | Pseudocode context dispatch bullet gave no method for matching a task to its triggers
- 2026-08-20 | Catch | Task 2 (pseudocode-during-planning) | Pseudocode context bullet lacked the why-explanation and visibility requirement its Directory context sibling has
- 2026-08-20 | Catch | Final review (pseudocode-during-planning) | Multi-task-same-trigger attribution undefined -- a dispatch could fold another task's pseudocode into the wrong task's context
- 2026-08-20 | Catch | Final review (pseudocode-during-planning) | Both Task 1 and Task 2 needed a fix round for similar gaps (missing concrete guidance, missing parity with sibling content) traced to the plan's own drafted text, not implementer error -- future plans handing an implementer verbatim skill-file edits should self-check against the target file's own sibling conventions during Self-Review
