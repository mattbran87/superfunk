# Doc-Timing Fix and Mutation Check — Design

**Date:** 2026-08-30
**Status:** Shipped
**User-Facing:** No

## Context

An external real-world trial (`docs/superpowers/process-reviews/external-trial-bookmark-cli-findings.md`) ran the superfunk plugin through three full pipeline cycles against a genuine Python CLI project, then synthesized findings independently, cross-validated by the trial project's own `process-review` output. Two findings stand out as the highest-leverage fixes available, named as such by both the external report and the trial's internal review:

**D6 — documentation bookkeeping happens after the final review, guaranteeing a whole-branch reviewer sees stale docs.** `subagent-driven-development`'s Finish step runs `check_docs.py` only after the final whole-branch review already passed clean. For any `User-Facing: Yes` spec, this ordering structurally guarantees the final reviewer inspects a branch whose docs contradict its own code, every time — the check that would catch the mismatch hasn't run yet. This reproduced once in the trial: cycle 2 shipped with the README still stating a feature didn't exist. The trial's own project recorded the empirically-discovered fix in its `docs/lessons-learned.md`: "User-facing docs must ship in the task that ships the surface." That fix belongs in the skill, not in each project's own lessons file.

**G2/M2 — mutation testing has no home.** Across all three trial specs, four tests passed against structurally broken implementations — a capacity check that restated its own arithmetic, a scheduling test suite that couldn't distinguish a correct implementation from a starving one, an "opened" check using containment instead of equality, and a cleanup call whose removal left every test green. Every one of these got caught, but only because an individual reviewer personally chose to revert code and watch a test go red — no template asks for this. The trial's own process-review named this the single highest-leverage fix available: a test that cannot fail looks identical to a passing one until someone deliberately breaks the code underneath it.

## Decision

**`writing-plans/SKILL.md` gains a new section, `User-Facing Documentation Timing`,** placed after `Task Right-Sizing` and before `Bite-Sized Task Granularity`:

```markdown
## User-Facing Documentation Timing

If the spec carries `User-Facing: Yes`, the task whose deliverable adds
or changes that user-facing surface must include its own step running
`python plugin/skills/documentation/scripts/check_docs.py <spec-file>
<task-base-sha> <task-head-sha>` and, if it reports `ACTION_NEEDED`,
drafting the README/CHANGELOG update — in that same task, committed
alongside the surface it documents. Never defer this to a separate later
task or to Finish: a reviewer who reaches the final whole-branch review
before the docs exist reviews a branch that contradicts its own README
by construction.
```

**`writing-plans/SKILL.md`'s Self-Review gains item 12**, appended after item 11:

```markdown
**12. User-facing documentation timing:** If the spec carries
`User-Facing: Yes`, does the task shipping the user-facing surface
include its own documentation step, per the section above? A plan that
defers this to a separate task or relies on Finish to catch it repeats
the same class of gap this item exists to close.
```

**`subagent-driven-development/SKILL.md`'s documentation check moves from Finish to immediately before the final reviewer dispatch**, becoming a backstop rather than the first and only check. The `## Final Review` section gains this opening paragraph, before its existing first paragraph:

```markdown
Before dispatching the final reviewer, check whether this plan traces to
a design spec (named in the plan's Goal line or a task's commit trailer,
e.g. "Part of docs/superpowers/specs/..."). If it does, run `python
plugin/skills/documentation/scripts/check_docs.py <spec-file>
<merge-base-sha> <head-sha>`. `NOT_APPLICABLE` or `ALREADY_UPDATED`:
continue to dispatch below — the feature task already handled this, per
writing-plans' User-Facing Documentation Timing requirement.
`ACTION_NEEDED`: invoke superfunk:documentation's Step 2 to draft the
README/CHANGELOG update from the printed spec content, commit it, and
only then dispatch the final reviewer. No design spec: skip this check
entirely. Running this before the final reviewer sees the branch means a
gap the plan's own task missed still gets caught before the most
expensive review runs, not after.
```

The existing documentation-check paragraph in `## Finish` (currently reading `"If this plan traces to a design spec ... run check_docs.py ..."`) gets removed — the check now runs earlier and doesn't repeat at Finish.

**The process diagram (`digraph process`) gains one new node** between `"More tasks remain?"` resolving `no` and `"Dispatch final code reviewer..."`: `"Pre-final-review doc check: check_docs.py, draft if ACTION_NEEDED"`.

**The prose Example Workflow's bracket-line sequence moves the documentation bracket line** from its current position among the other Finish bookkeeping lines to immediately before the `"[Run review-package PLAN_FILE MERGE_BASE HEAD; dispatch final code-reviewer...]"` line — reflecting the new, earlier timing.

**`task-reviewer-prompt.md` gains a new `## Mutation Check` section**, placed after the existing `## Tests` section and before `## Part 1: Spec Compliance`:

```markdown
## Mutation Check

For each new test in this diff that asserts a load-bearing property — an
edge case, an invariant, a boundary condition, or any assertion the plan
or spec treats as a correctness guarantee, not a trivial "returns X"
check — revert the specific implementation line(s) the test claims to
guard, run that one test, confirm it fails (goes red), then restore the
code to its exact prior state. A test that stays green after reverting its
guarded line cannot actually catch the regression it claims to guard
against — report it as an Important finding, not a footnote. Skip this
check only for a test with no clear guarded line to revert (a pure smoke
test, for example) and say so.
```

**The Output Format section gains a new subsection**, between `### Strengths` and `### Issues`:

```markdown
### Mutation Check

For each load-bearing test mutated: file:line, the line reverted, and
whether the test went red (✅) or stayed green (❌ — filed as an
Important finding above).
```

## Falsifiable Criteria

1. A direct read-through of `writing-plans/SKILL.md` confirms the `User-Facing Documentation Timing` section and Self-Review item 12 exist, worded identically to the Decision block above.
2. A direct read-through of `subagent-driven-development/SKILL.md`'s `## Final Review` section confirms the new opening paragraph exists, and `## Finish` no longer contains a documentation-check paragraph.
3. A direct read-through of the `digraph process` block confirms the new pre-final-review documentation-check node exists in the correct position, and the prose Example Workflow's documentation bracket line appears before the final-reviewer-dispatch bracket line, not after it.
4. A direct read-through of `task-reviewer-prompt.md` confirms the `## Mutation Check` section and its `### Mutation Check` Output Format subsection exist, worded identically to the Decision block above.
5. A disposable `--plugin-dir` trial builds a fixture task with one test that would pass against a broken implementation (e.g., a boundary check using the wrong comparison operator). Dispatching a task reviewer against it correctly reports the test failing the mutation check as an Important finding.

## Consequences

A future `User-Facing: Yes` spec's docs land in the same commit as the feature they describe, closing the gap that let a real trial ship a feature invisible in its own README. The Finish-time check becomes a true backstop — still present, but no longer the first or only point of failure, and no longer running after the point where catching a gap costs the most.

A future task reviewer that finds a load-bearing test now has an explicit, named check for whether that test can actually fail — closing the gap that let four structurally-broken implementations pass their own test suites across one trial, each one only caught because a reviewer happened to think of it independently.

This adds real review cost: every task review that touches a load-bearing test now includes a revert-run-restore cycle per test, not just a read. Accepted because the trial's own evidence shows this exact pattern recurring at the most expensive possible point (final review, or not at all) without it.

## Deferred

- Making the mutation check itself automatic/scripted (a tool that reverts a named line and runs the test, rather than the reviewer doing this by hand) — no evidence yet that manual execution proves insufficient; revisit if reviewers skip this step in practice.
- The remaining findings from the same trial (D1-D5, D7-D10, and the hostile-input-pass and stale-workaround-grep Recommendations) — out of scope for this spec, tracked separately for follow-up sub-projects.
