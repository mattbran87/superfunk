# Cross-Section Sibling Scope — Design

**Date:** 2026-08-27
**Status:** Shipped

## Context

The final whole-branch review of `cross-section-mechanism-consistency` found its own carve-out edit needing changes in two files under `plugin/skills/subagent-driven-development/`: the target file `re-review-prompt.md`, and a sibling file, `SKILL.md`, in the same directory. The shipped grep scope — the target file plus the design spec, if named — never reaches a sibling file. The controller fixed the sibling-file instance directly, by hand; the mechanism itself never caught it.

This design closes the Deferred item that named exactly this gap: "Widening item 8's and the carve-out's grep scope beyond the target file (plus its design spec) to sibling files in the same skill directory that describe the same mechanism." That item stayed deferred in the originating spec pending a real recurrence; this recurrence now grounds the fix.

## Decision

- **`writing-plans/SKILL.md`'s Self-Review item 8 widens** to include the target file's sibling directory when that directory sits under `plugin/skills/`:

  ```
  **8. Cross-section mechanism consistency:** Does any task edit content
  describing a routing, trigger, or lifecycle mechanism — language like
  "if X exists, proceed to...", "triggered by...", "never run
  standalone," or a cross-reference like "see Y, below"? If so, grep
  the same target file, every other file in the same
  `plugin/skills/<name>/` directory if the target file lives in one,
  and the design spec, if it also describes this mechanism — for every
  other mention of the key terms involved, and read each hit. Confirm
  the edit doesn't leave any of them contradicting the new content.
  ```

- **`re-review-prompt.md`'s carve-out widens identically**, preserving the parent design's deliberate parity between the two touchpoints:

  ```
  If the fix diff changes content describing a routing, trigger, or
  lifecycle mechanism (language like "if X exists, proceed to...",
  "triggered by...", "never run standalone," or a cross-reference like
  "see Y, below"), this is the one case where you must look outside the
  diff: grep the rest of the touched file, every other file in the same
  `plugin/skills/<name>/` directory if the touched file lives in one,
  and the design spec, if the plan's Goal line or a task's commit
  trailer names one — for every other mention of the same key terms,
  and read each hit. A contradiction there is New Breakage, not an
  Out-of-Scope Observation, since the fix itself caused it even though
  the contradicted text sits outside the literal diff.
  ```

- **Scope stays deliberately narrow to `plugin/skills/<name>/` directories**, not "any directory." Skill directories in this repo top out at 11 files and mostly hold 1-6, so the added grep cost stays negligible. A directory like `docs/` holds dozens of unrelated files with no evidence yet that a sibling-file check would help there — widening indiscriminately trades a real, cheap fix for an untested, potentially noisy one.

- **A `.context.md`-based trigger condition (tying the widening to the existing Per-Directory Context File convention instead of hardcoding a path pattern) does not replace the path-based rule.** No skill directory in this repo currently has a `.context.md` file, so that condition alone would not have caught the actual recurrence this design fixes.

## Falsifiable Criteria

1. A direct read-through of the shipped `writing-plans/SKILL.md` confirms item 8 names the `plugin/skills/<name>/` sibling-directory scope, worded identically to the Decision block above.
2. A direct read-through of the shipped `re-review-prompt.md` confirms the carve-out names the same sibling-directory scope, worded identically to the Decision block above.
3. A disposable `--plugin-dir` trial creates a fixture skill directory holding two files. A plan task edits file A's routing language in a way that contradicts file B, untouched, in the same directory. Running Self-Review against that plan catches the contradiction in file B before dispatch.
4. A second disposable `--plugin-dir` trial simulates a fix round whose diff edits file A's routing language, contradicting untouched file B in the same directory. Dispatching the re-review catches it and reports it as New Breakage.

## Consequences

Every plan's Self-Review item 8 gains one more grep target when the edited file lives under `plugin/skills/`: negligible added cost, since skill directories hold at most 11 files today and mostly hold far fewer.

Every carve-out-triggered re-review gains the identical additional grep target under the identical condition — the two touchpoints stay in lockstep, matching the parent design's explicit parity principle.

## Deferred

Carried forward, unaddressed by this narrow fix:

- A proactive File Structure-time check (flagging cross-cutting mechanisms before drafting any task).
- Extending the same check to `task-reviewer-prompt.md`'s first-pass review. That file's existing "cross-cutting changes are legitimate named risks" allowance (lock ordering, API contracts, shared mutable state) still never names the routing/trigger/lifecycle pattern specifically.
- Trial coverage for the negative (correctly-does-not-fire) case, a mechanism spanning more than two sections, and the "and the design spec" clause of either instruction. The negative case has now gone untested across two consecutive sub-projects in this line — worth promoting out of Deferred the next time this mechanism gets touched.
- Widening the sibling-directory scope beyond `plugin/skills/<name>/` to other directory kinds — revisit only if a recurrence shows up outside a skill directory.
- Whether "every other file in the same `plugin/skills/<name>/` directory" recurses into subdirectories (four skill directories have one, including `subagent-driven-development/scripts/`, the directory this whole fix originated from). No live contradiction exists in any subdirectory file today, and a naive recursive grep also risks false positives on unrelated code (e.g., a variable literally named `LIFECYCLE_CHECK_MS`). Left non-recursive, silently, in both shipped clauses — stays deferred pending a real recurrence rather than resolved here.
- The item 8 visibility gap the prior spec named (`2026-08-26-cross-section-mechanism-consistency-design.md`'s Deferred: item 8 produces no written artifact, matching Self-Review items 1-7's reminder shape rather than the File Structure step's visibility-clause convention) stays open — this sub-project widened what item 8 checks without changing that it stays silent about having checked it.
- `subagent-driven-development/SKILL.md`'s two abstract summaries of the carve-out (its Finish-adjacent description of the re-reviewer's job, and its Red Flags table entry) and `re-review-prompt.md`'s own `## Scope` cross-reference pointer needed no edit for this widening — all three stay scope-free by construction (each describes *that* a cross-section exception exists, never *how wide* it reaches), so widening what the exception covers changes nothing they assert. Recording this reasoning here since the prior sub-project's equivalent abstractions *did* need a hand-edit, and a future reader comparing the two would otherwise find the difference unexplained.
