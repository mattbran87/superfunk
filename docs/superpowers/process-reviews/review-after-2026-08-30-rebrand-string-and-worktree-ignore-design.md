# Process Review — after 2026-08-30-rebrand-string-and-worktree-ignore-design.md

**Date:** 2026-08-30

## Specs Reviewed

- 2026-08-28-process-review-recommendations-batch-3-design.md
- 2026-08-30-doc-timing-and-mutation-check-design.md
- 2026-08-30-rebrand-string-and-worktree-ignore-design.md

## Catches

**2026-08-28-process-review-recommendations-batch-3-design.md**
- Plan self-review: both the spec's Falsifiable Criterion 4 and the plan's Task 3/4 predicted a `grep -c "Finish:"` total of 10, assuming each new diagram node name contributes one matching line — testing the exact replacement text showed each name spans multiple lines (its own declaration plus every edge naming it), contributing 5 lines rather than 2, for a corrected total of 13.
- Task 4: the plan's own verification step used `grep -n "digraph process" -A 60 ... | grep "Finish:"`, expecting 5 matches, but returned only 2 — the digraph block spans 65 lines after Task 3's edit, so the 60-line window cut off before reaching the new nodes.

**2026-08-30-doc-timing-and-mutation-check-design.md**
- Plan self-review: Task 1 Step 4 predicted `grep -c "User-Facing Documentation Timing"` would return 2, assuming a new Self-Review item's text would repeat the section's exact capitalized heading — the item's actual text used different capitalization ("User-facing documentation timing"), a distinct case-sensitive string, so the real count was 1.
- Task 3: the verification used an anchored `grep -c "^## Mutation Check\|^### Mutation Check"` against a file that wraps its entire template in an indented code fence — no heading in that file ever sits at column 0, so the anchored pattern returned 0 regardless of whether the new section existed.

**2026-08-30-rebrand-string-and-worktree-ignore-design.md**
- Spec self-review: draft Falsifiable Criterion 1 claimed fixing one line would leave "no remaining superpowers string anywhere in the file," but a real grep found 6 total occurrences — three legitimately reference the unrenamed `using-superpowers` skill directory, one links to an upstream issue, and one (a plugin-identity comment) needed fixing but the draft never named it.
- Plan self-review: Task 2 Step 1's verification predicted a phrase would return two matches, but the same phrase also appears a third time in the same file's Common Rationalizations table.
- Task 1: the plan predicted a bare `grep -c "superpowers"` would drop from 6 to 4 after the fix, but it only dropped to 5 — the retained `using-superpowers` skill name is itself a substring match for "superpowers," including inside the newly-fixed line's own `superfunk:using-superpowers`, so a bare substring count could never reach a clean number the fix controls.

## Misses

### M1. A numeric or pattern-matching verification claim needed correction in every single reviewed spec — 7 occurrences across all 3 specs

Every one of the 7 Catches above shares the same shape: a plan or spec predicted what a `grep` command would return, and the real command returned something else. This isn't a code defect — it's the framework's own newest discipline (Self-Review items 6, 10, and 12, and `docs/patterns/verify-plan-commands-against-real-content.md`) working exactly as intended, catching itself in the act of being built and then immediately used. But a 100% recurrence rate across every spec this review covers says the underlying difficulty is real and not yet fully characterized: five genuinely distinct failure shapes appeared (line-vs-occurrence counting, a window too short for a block's real length, case-sensitivity assumed away, a phrase's other appearances in the same file ignored, and a substring legitimately retained elsewhere). Each one needed a separate moment of "wait, let me actually test this" that the Self-Review items' own text doesn't prompt for by name.

## Friction

### F1. Every reviewed spec's own writing process stopped at least once to fix a verification claim

Not a code-review fix round — a plan- or spec-authoring interruption, caught by the newly-shipped Self-Review items during the same sub-project that either shipped those items or immediately reused them. Zero of the three specs in this batch reached its own Self-Review clean on the first pass with respect to numeric claims.

## Gaps

### G1. Self-Review items 6, 10, and 12 say "verify" without naming the failure modes that make naive verification insufficient

`docs/patterns/verify-plan-commands-against-real-content.md` already catalogues five distinct ways a plausible-looking verification command fails (see Catches above), but none of writing-plans' items 10/12 or brainstorming's item 6 point to it directly — an author re-derives "verification is harder than it looks" from scratch each time, rather than checking their own command against a known list of traps.

## Recommendations

- [ ] Add a direct cross-reference from `writing-plans/SKILL.md`'s Self-Review items 10 and 12, and `brainstorming/SKILL.md`'s Spec Self-Review item 6, to `docs/patterns/verify-plan-commands-against-real-content.md` — naming it as the place to check known failure-mode categories (line-vs-occurrence counting, anchored patterns against indented/fenced content, case sensitivity, a phrase's other appearances in the same file, a substring legitimately retained elsewhere) before trusting a verification command's predicted output. Addresses G1.
- [ ] Revisit `2026-08-30-doc-timing-and-mutation-check-design.md`'s Deferred item — "Making the mutation check itself automatic/scripted... no evidence yet that manual execution proves insufficient" — against this review's own evidence: 7 manual-verification misses in one review period. A small script that takes a pattern and a file and reports the real count (or confirms a substitution's real effect) would remove the class of error this review's Catches all share, not just the mutation-check's own narrower case. Addresses M1 and F1 at the tooling level rather than the instruction level.
