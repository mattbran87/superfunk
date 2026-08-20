# Process Review — Running Notes

Append-only log. Each entry marks one finding a review catches on its
first pass (spec-compliance, code-quality, or the final whole-branch
review), tagged `Catch`. `process-review` reads this log,
cross-references `git log`, and may surface `Miss`, `Friction`, or
`Gap` patterns across entries when it synthesizes a review file.

Format: `- <YYYY-MM-DD> | Catch | <task/spec label> | <one-line finding>`

<!-- entries below this line -->
- 2026-08-19 | Catch | Task 2 (process-review) | Process-review skill's Step 4 dropped the design spec's required Specs Reviewed section, and Self-Review only checked trigger presence, not format/reason quality (git log 437d959, missed by the running log since it predates this mechanism's own existence)
- 2026-08-19 | Catch | Final review (process-review) | Design spec's Falsifiable Criteria and the plan both retained a stale "five sections" count after the Decision section was corrected to six (git log 04fbdcf, missed by the running log since it predates this mechanism's own existence)
- 2026-08-20 | Catch | Task 1 (pseudocode-during-planning) | Pseudocode section had no worked example, only abstract rules
- 2026-08-20 | Catch | Task 1 (pseudocode-during-planning) | Self-Review's Pseudocode check verified trigger presence only, not format or reason quality
- 2026-08-20 | Catch | Task 2 (pseudocode-during-planning) | Pseudocode context dispatch bullet gave no method for matching a task to its triggers
- 2026-08-20 | Catch | Task 2 (pseudocode-during-planning) | Pseudocode context bullet lacked the why-explanation and visibility requirement its Directory context sibling has
- 2026-08-20 | Catch | Final review (pseudocode-during-planning) | Multi-task-same-trigger attribution undefined -- a dispatch could fold another task's pseudocode into the wrong task's context
- 2026-08-20 | Catch | Final review (pseudocode-during-planning) | Both Task 1 and Task 2 needed a fix round for similar gaps (missing concrete guidance, missing parity with sibling content) traced to the plan's own drafted text, not implementer error -- future plans handing an implementer verbatim skill-file edits should self-check against the target file's own sibling conventions during Self-Review
- 2026-08-20 | Catch | Task 2 (lessons-and-patterns) | Promotion-rule bullet dropped "that applies across many future situations" from the design spec's exact phrasing
- 2026-08-20 | Catch | Task 3 (lessons-and-patterns) | <spec-slug> had no fallback for the no-design-spec Finish branch
- 2026-08-20 | Catch | Task 3 (lessons-and-patterns) | Promotion-rule framing drifted from code-standards.md's independent-OR structure
- 2026-08-20 | Catch | Task 4 (lessons-and-patterns) | Lessons/patterns reading bullet had no visibility clause, unlike its .context.md sibling
- 2026-08-20 | Catch | Final review (lessons-and-patterns) | Three fix rounds traced to the plan restating the same design-spec rule in two different tasks without cross-checking the restatements against each other
