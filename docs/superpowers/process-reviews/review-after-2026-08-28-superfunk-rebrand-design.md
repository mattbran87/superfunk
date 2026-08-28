# Process Review — after 2026-08-28-superfunk-rebrand-design.md

**Date:** 2026-08-28

## Specs Reviewed

- 2026-08-27-refresh-example-workflow-design.md
- 2026-08-28-documentation-design.md
- 2026-08-28-superfunk-rebrand-design.md

## Catches

**2026-08-27-refresh-example-workflow-design.md**
- Task 2: the commit message for the new Self-Review item 9 misattributed its originating final review to "cross-section-mechanism-consistency" instead of the actual source, "bug-tracking" — caught immediately on self-review before pushing, fixed via `git commit --amend`.
- Final review: `subagent-driven-development/SKILL.md`'s process diagram (the dot digraph near the top of the file) also stops at workspace deletion, never depicting any of Finish's bookkeeping steps — the same staleness shape this sub-project just fixed in the prose Example Workflow, in a third location within the same file. Left out of this sub-project's own scope (a different kind of illustration than the one named in its Decision) and documented rather than fixed.

**2026-08-28-documentation-design.md**
- Plan self-review: `writing-plans/SKILL.md`'s required Plan Document Header has always included a `## Global Constraints` section (present since the original upstream import, predating this fork). Every plan written this entire session omitted it, undetected because `writing-plans`' own 9-item Self-Review has no item checking a plan's own header against its own required template. Fixed for this one plan; promoted to `docs/patterns/self-review-checks-own-required-template.md`.
- Task 1: the plan's Step 8 predicted "9/9" tests passing but the correct count was 10 — a miscount when end-to-end tests got added after the plan's git-fixture test step was drafted. Caught by actually running the tests, not a defect in the shipped code.

**2026-08-28-superfunk-rebrand-design.md**
- Plan self-review: the approved spec estimated "135 occurrences across 33 files" for the `superpowers:` prefix rewrite and called for "grep-and-replace across the whole plugin/ tree." The actual sweep found 116 occurrences across 29 files, roughly half in upstream's own historical changelog and archived pre-fork design docs, which a literal whole-tree rewrite would have misstated as current. Caught by running the real grep before building the plan's file list; the spec was amended and re-approved (scoped to live/instructional content only) before planning continued.
- Task 4: the plan's verification steps predicted "33" for `grep -rn ... | wc -l` and a `grep -rc` sum, but both commands count matching lines, not raw pattern occurrences — one line carries two `superpowers:` references, so 33 total occurrences land on 32 matching lines. Caught by running the actual command before editing; plan corrected in place.
- Task 6: the plan predicted `check_docs.py` would report `ALREADY_UPDATED` once the README got modified. Its first-ever real (non-fixture) invocation instead returned `ACTION_NEEDED` and separately crashed with a `UnicodeEncodeError`. Two real, previously undetected defects in code shipped earlier this session: an exact bare-filename match that never matches a nested `README.md` path, and a Windows stdout encoding that can't handle the em dashes and arrows nearly every spec in this project uses. Filed as BUG-0001 (Important) and BUG-0002 (Critical) rather than fixed inline, per explicit direction, since fixing a previously-shipped tool sat outside this sub-project's own scope. Promoted to `docs/patterns/validate-tools-against-real-project-data.md`.

## Misses

- **A plan's stated "Expected:" numeric value drifts from what a freshly-run command actually reports, and nothing in `writing-plans`' Self-Review catches the drift before execution.** Three instances across two of the three reviewed specs: documentation's Task 1 (predicted 9/9 tests, actual 10), and superfunk-rebrand's Task 4 (predicted 33 occurrences, actual 32 matching lines — a different counting method than assumed). Each got caught only because the actual command ran and its real output got read, not because a plan-writing check flagged the number as unverified.

## Friction

- **superfunk-rebrand's own plan and spec needed three separate in-flight corrections** (the spec's occurrence-count estimate, Task 4's line-vs-occurrence count, and Task 6's check_docs.py prediction) before the sub-project's Finish step — each individually minor and each caught immediately by running the real command rather than trusting the written prediction, but the concentration of three corrections in one sub-project reads as procedural friction: numeric claims kept entering spec and plan text without being freshly derived first.

## Gaps

- **`writing-plans`' Self-Review has no item verifying a plan's own header against the required Plan Document Header template.** Named as a Pattern after the Global Constraints omission (see Catches, documentation), but the underlying mechanism gap — no Self-Review item performs this check — remains unaddressed. This Gap entry exists to generate its own Recommendation rather than leave the Pattern as documentation-only.

## Recommendations

- [ ] Add a Self-Review item to `writing-plans/SKILL.md` requiring every step's stated `Expected:` numeric value to be confirmed by actually running the command during plan-writing, not estimated or carried over from an earlier draft — closes the Miss above (documentation Task 1, superfunk-rebrand Task 4).
- [ ] Add a step to `brainstorming/SKILL.md`'s spec-writing process (or its own Spec Self-Review) requiring any numeric claim about existing project state (occurrence counts, file counts, and similar) to be verified by running the actual command before committing it to the spec's Decision section — superfunk-rebrand's spec originally estimated "135 occurrences across 33 files" without running the real grep, later found to be 116 across 29.
- [ ] Add a Self-Review item to `writing-plans/SKILL.md` checking the plan's own document header against the required Plan Document Header template (Goal, Architecture, Tech Stack, Global Constraints) — closes the Gap above, per `docs/patterns/self-review-checks-own-required-template.md`'s own stated rule.
- [ ] Update `subagent-driven-development/SKILL.md`'s process diagram (the dot digraph near the top of the file) to depict Finish's bookkeeping steps, matching the fix `refresh-example-workflow` already applied to the prose Example Workflow — flagged in both `bug-tracking`'s and `refresh-example-workflow`'s final reviews without action yet.
