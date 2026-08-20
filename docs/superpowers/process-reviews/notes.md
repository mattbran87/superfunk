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
- 2026-08-20 | Catch | Task 1 (checklist-construction) | Wording redundancy: "not once per split sub-checklist" repeated "split" already established one clause earlier
- 2026-08-20 | Catch | Task 2 (checklist-construction) | Per-section instruction said "phase" but two of six groups (Quality Checks, Deployment) don't say "Phase" in their own heading
- 2026-08-20 | Catch | Task 1, 2, 3 (checklist-construction) | Three separate code-quality findings misapplied a stated rule literally without checking source intent or existing shipped precedent first -- all three overridden after independent verification (the 5-9 cap read as a floor, a tagging comparison used a mismatched sibling, a "needs examples" finding ignored two already-shipped instances of the same open-ended pattern)
- 2026-08-20 | Catch | Final review (checklist-construction) | Falsifiable Criterion 2's literal grep pattern didn't match test-driven-development's past-tense "Checked" wording -- a false failure if re-run literally
- 2026-08-20 | Catch | Final review (checklist-construction) | The shipped "5-9 items" rule text itself reads ambiguously as a floor, the same ambiguity that caused a reviewer override earlier in this same sub-project
