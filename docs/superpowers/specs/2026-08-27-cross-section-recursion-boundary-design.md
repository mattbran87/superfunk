# Cross-Section Recursion Boundary — Design

**Date:** 2026-08-27
**Status:** Approved

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-27-cross-section-sibling-scope-design.md` named its third Recommendation: the sibling-directory clause in Self-Review item 8 and the re-review carve-out never states whether "every other file in the same `plugin/skills/<name>/` directory" recurses into subdirectories. `2026-08-27-cross-section-sibling-scope-design.md`'s own Deferred section already recorded the underlying evidence: four skill directories currently have a subdirectory (`subagent-driven-development/scripts/`, `brainstorming/scripts/`, `writing-skills/examples/`, `using-superpowers/references/`), none hold mechanism prose today, and a naive recursive grep risks false positives on unrelated code (e.g., a variable literally named `LIFECYCLE_CHECK_MS`). This spec resolves the ambiguity in the shipped text.

## Decision

Both clauses gain an identical parenthetical: `(top-level files only, not subdirectories)`, inserted immediately after "the same `plugin/skills/<name>/` directory."

Item 8 (`writing-plans/SKILL.md`):
```
If so, grep the same target file, every other file in the same
`plugin/skills/<name>/` directory (top-level files only, not
subdirectories) if the target file lives in one, and the design spec,
if it also describes this mechanism — for every other mention of the
key terms involved, and read each hit. Confirm the edit doesn't leave
any of them contradicting the new content.
```

The carve-out (`re-review-prompt.md`):
```
If the fix diff changes content describing a routing, trigger, or
lifecycle mechanism (language like "if X exists, proceed to...",
"triggered by...", "never run standalone," or a cross-reference like
"see Y, below"), this is the one case where you must look outside the
diff: grep the rest of the touched file, every other file in the same
`plugin/skills/<name>/` directory (top-level files only, not
subdirectories) if the touched file lives in one, and the design
spec, if the plan's Goal line or a task's commit trailer names one —
for every other mention of the same key terms, and read each hit. A
contradiction there is New Breakage, not an Out-of-Scope Observation,
since the fix itself caused it even though the contradicted text sits
outside the literal diff.
```

This wording clarifies scope rather than changing behavior: both mechanisms already only ever checked top-level files in practice (neither shipped trial nor real use exercised a subdirectory). The clarification closes the ambiguity the process review named, without altering what either mechanism actually does.

## Falsifiable Criteria

1. A direct read-through of the shipped `writing-plans/SKILL.md` confirms item 8's clause includes `(top-level files only, not subdirectories)`, worded identically to the Decision block above.
2. A direct read-through of the shipped `re-review-prompt.md` confirms the carve-out's clause includes the identical parenthetical.

No new live trial: this closes a documentation ambiguity rather than a behavior gap — both mechanisms' actual scope stays unchanged, leaving nothing new to exercise.

## Consequences

Every plan's Self-Review item 8 and every carve-out-triggered re-review read one more parenthetical — no change in what either check actually does or costs.

## Deferred

- Extending either check to recurse into subdirectories — revisit only if a real mechanism-describing contradiction surfaces in a skill directory's subdirectory (`scripts/`, `examples/`, `references/`), none of which currently hold any.
