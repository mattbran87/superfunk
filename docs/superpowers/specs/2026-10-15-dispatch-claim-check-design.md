# Dispatch Claim Check — Design

**Date:** 2026-10-15
**Status:** Shipped
**User-Facing:** Yes

## Context

Two ArcGISProMCP findings target `subagent-driven-development`'s dispatch step (`docs/superpowers/process-reviews/external-project-arcgispromcp-findings.md`):

- **A4 — nothing confirms the controller's own dispatch claims against the tree.** SDD Step 1 (`plugin/skills/subagent-driven-development/SKILL.md:208-276`) builds a dispatch from five parts. Part (2), the task brief, comes from the plan word for word. Parts (1), (3), and (4) come from the controller, and no step checks them. On one ArcGISProMCP branch, 2 of 9 dispatches carried false controller claims: a type the controller wrote and then deleted, a wrong tool count, and a wrong home for a test file. The findings file calls this "the thinnest evidence base of the four".
- **A10 — nothing names where each part of a brief came from.** An implementer cannot tell which lines came from the plan and which from the controller, so it cannot calibrate its trust. On ArcGISProMCP's `arcade` branch, 5 implementers corrected the brief they received, and all 5 were right. Each correction followed an instruction in the brief to check citations against the source rather than against the brief.

Superfunk's own record holds almost no evidence for either finding. A search of `docs/superpowers/process-reviews/notes.md` finds one dispatch-related Catch (`:43`), and it describes a different failure: pseudocode folded into the wrong task. One related instance came up on 2026-10-15. A final-review fix brief stated a wrong expected count, and the fix agent reported the mismatch rather than force the check to pass. That instance sat in a fix dispatch, which this change does not reach (see Out of Scope).

The implementer template already separates the two sources. In `plugin/skills/subagent-driven-development/implementer-prompt.md`, the "Task Description" section points at the brief, and the "Context" section holds the controller's own text. No sentence tells the implementer that nothing checked the Context text.

## Decisions

1. **The implementer checks the controller's text, not the controller (option B).** Human-partner decision. A controller that checks its own memory shares the blind spots that produced the error. The implementer reads the tree anyway, and ArcGISProMCP's 5 correct corrections came from this kind of instruction.
2. **The controller keeps its own text inside Context.** Otherwise a controller claim placed elsewhere in the dispatch escapes the check.
3. **No trial. A watchlist entry tracks the change.** Human-partner decision. Superfunk cannot tell yet whether its implementers already behave this way without the sentence. The watch entry decides whether a trial runs later.

## Design

### 1. Implementer-side check

In `plugin/skills/subagent-driven-development/implementer-prompt.md`, directly under the `## Context` section's placeholder line (`[Scene-setting: where this fits, dependencies, architectural context]`), add this paragraph, indented to match the template:

> The controller wrote this section, not the plan. It may carry a claim from memory of earlier tasks: a type or file that exists, a count, a line number, a commit. Check each such claim against the tree before you rely on it. If one does not match, say so in your report rather than build around it.

### 2. Controller-side placement

In `plugin/skills/subagent-driven-development/SKILL.md` Step 1, in the "Task brief" bullet, directly after "(5) the report-file path and report contract.", add:

> Put parts (1), (3), and (4) under the template's Context heading. The implementer checks that section's claims against the tree, so a claim you place anywhere else skips that check.

The fix round also rewrote the sentence that follows it in Step 1. It now reads: "Exact values the plan states (numbers, magic strings, signatures, test cases) appear only in the brief, except a value your part (4) resolution selects. A value from an earlier task's run, such as a commit or a measured count, goes under Context." The old sentence said exact values appear only in the brief, which a plan written before any task ran cannot satisfy for a value from that run.

### 3. Watchlist entry

Append to `docs/superpowers/process-reviews/watchlist.md`:

```markdown
- **dispatch-claim-check** (added 2026-10-15, dispatch-claim-check)
  - Watching: the implementer-prompt sentence that tells an implementer to check the controller's Context claims against the tree.
  - Trigger: a review or an outcomes entry finds a false controller claim in an implementer dispatch built from `implementer-prompt.md`, which the implementer built on without reporting it.
  - Action when tripped: trial-gate the sentence per `docs/patterns/ab-test-live-trials-for-behavior-change.md`, or rewrite it.
```

### 4. Bookkeeping

At Finish, change the findings file's "In progress" line for A4 and A10 (in its "Superfunk response — 2026-10-15" section) to record what shipped, with the commit and version.

## Falsifiable Criteria

1. The implementer-prompt paragraph appears exactly once, between the `## Context` heading and the `## Before You Begin` heading.
2. The SDD placement sentence appears exactly once, inside Step 1's "Task brief" bullet.
3. `watchlist.md` holds 8 entries, and `dispatch-claim-check` carries Watching, Trigger, and Action fields.
4. The spec's quotes of both sentences match the shipped text word for word, apart from line wraps.
5. At Finish, the findings file's response section records A4 and A10 as shipped.

## Out of Scope

- A controller-side check before dispatch (option A). The human partner rejected it, and the watch entry can bring it back.
- Checks on the brief itself. The brief comes from the plan, and `writing-plans`' Self-Review owns plan errors.
- `executing-plans`. It dispatches no implementer, so it has no Context section to label.
- An A/B trial (Decision 3).
- Fix dispatches and reviewer dispatches. The fix loop's resume message, a round 4–5 fresh implementer, the Final Review's fix subagent, and every reviewer dispatch carry controller claims too, but none of them uses the implementer template's Context section, so the claim check does not reach them. Two instances already sit in that gap: the 2026-10-15 fix brief's wrong expected count, and a 2026-10-16 reviewer dispatch for this batch's own Task 1 that named a "Placeholders section" `implementer-prompt.md` does not have. The reviewer reported that claim as vacuous rather than build on it.

## Consequences

- An implementer now treats the controller's Context text as claims to check. That adds tree reads at the start of each task, sized to how many claims the controller wrote.
- The implementer catches a false controller claim during implementation, not before dispatch. If the implementer builds on the claim anyway, the task review remains the next backstop.
- The placement rule depends on the controller following it. Nothing checks mechanically that every controller claim sits under Context.
- The sentence names four kinds of claim. A controller claim of another kind, such as a design decision from an earlier task, still reaches the implementer as Context text, but the sentence does not name it as a claim to check.

## Alternatives Considered

| Decision | Candidates | Chosen | Confidence and evidence |
|---|---|---|---|
| Where the check sits | A. controller checks before dispatch; B. implementer checks the controller's text; C. both | B | Medium. ArcGISProMCP's 5 correct implementer corrections came from this kind of instruction, and `implementer-prompt.md` already separates the brief from the controller's Context. |
| Trial | A. ship and watch; B. trial-gate; C. defer | A | Medium-low. The behavior shows up in ArcGISProMCP's record and in one 2026-10-15 instance, both without a control arm. |

## RESULT

Shipped on `master`, 2026-10-16, in one task plus one fix round and one final-review fix wave.

- `93db97b`: the implementer-prompt claim-check paragraph, the SDD placement sentence, the `dispatch-claim-check` watchlist entry, and the v6.9.0 release note.
- `d30bcb3` (fix round 1): SDD Step 1's exact-values rule now covers only values the plan states. A value from an earlier task's run goes under Context.
- `2c2f688` (final-review fix wave): a part (4) resolution may name a plan value. Out of Scope now names fix and reviewer dispatches. The watch trigger now covers implementer dispatches built from the template only.

Criteria 1–4 hold. Criterion 4 names two quoted sentences. The fix wave added a third quote, of the exact-values sentence, in Design §2. At Finish a whitespace-normalized search found that sentence once in SDD and once in this spec, so all three quotes match the shipped text.

**Evidence status.** The Alternatives row for the trial still cites the 2026-10-15 fix-brief instance. That instance sat in a fix dispatch, outside this change. So the ship-and-watch decision rests on ArcGISProMCP's record alone. The `dispatch-claim-check` watch entry carries the open question.

**One live instance during this batch.** The controller's own reviewer dispatch for Task 1 named a "Placeholders section" that `implementer-prompt.md` lacks. The reviewer reported it rather than build on it. That case also sits outside the change: Out of Scope names it.
