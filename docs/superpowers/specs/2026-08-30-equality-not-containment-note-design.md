# Equality-Not-Containment Note — Design

**Date:** 2026-08-30
**Status:** Approved
**User-Facing:** No

## Context

The trial's own internal process-review (`review-after-2026-08-29-edit-command-design.md`) names one Recommendation not yet shipped alongside the Mutation Check it amends: "Add an equality-not-containment note to the mutation check above: when a test compares two strings where one may be a prefix of the other, compare whole lines or use equality — `in` is the wrong operator for an equality property. Derived from the edit-command Miss at notes.md:26."

That Miss (`notes.md:26`, dated 2026-08-30) reads: "`test_list_displays_exactly_what_open_navigates_to` asserted `opened[0] in listing` — substring containment — and passed against the UNFIXED code, because the normalized URL is a prefix of the raw one. The test meant to pin the round's headline property (display equals destination) could not fail." The implementer caught this by reverting the fix and re-checking, not the reviewer — the exact gap the Mutation Check exists to close, in a shape the check's own current wording doesn't specifically flag: a test using `in` can look like it asserts equality while actually asserting something weaker, and stays green under a mutation that only breaks equality, not containment.

## Decision

**`task-reviewer-prompt.md`'s Mutation Check section gains one closing sentence**, appended to the existing paragraph:

```markdown
Skip this check only for a test with no clear guarded line to revert (a
pure smoke test, for example) and say so.
```

becomes:

```markdown
Skip this check only for a test with no clear guarded line to revert (a
pure smoke test, for example) and say so. A related trap: a test
comparing two strings with `in` (substring containment) instead of
`==` can look like it asserts equality while accepting anything one
string contains the other — if a comparison the plan or spec treats
as an equality guarantee uses `in`, flag it even if its own mutation
check passes, since containment can stay true across a mutation that
breaks the equality the test actually meant to pin.
```

## Falsifiable Criteria

1. A direct read-through of `task-reviewer-prompt.md`'s Mutation Check section confirms the added sentence exists, worded identically to the Decision block above.
2. A disposable `--plugin-dir` trial constructs a fixture test asserting `x in y` where the plan or spec states an equality property (e.g., "the displayed value equals the destination value"), with `x` a genuine prefix of `y`. Dispatching a task reviewer against it correctly flags the containment-vs-equality gap, independent of whether the test's own directly-guarded line passes a standard mutation check.

## Consequences

A future task reviewer checking a string-comparison test now has an explicit prompt to look past "does reverting the guarded line turn it red" and ask whether the comparison operator itself matches the property the test claims to pin — closing the exact gap that let a real trial's headline test stay green against unfixed code.

## Deferred

- The remaining trial finding (D5/D7, checkpoint UX) — tracked separately for a follow-up sub-project.
