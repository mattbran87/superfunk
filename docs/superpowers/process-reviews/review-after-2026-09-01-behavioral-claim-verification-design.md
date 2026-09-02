# Process Review — after 2026-09-01-behavioral-claim-verification-design

**Date:** 2026-09-01
**Window:** since review-after-2026-09-01-convention-retirement-design (same day)

## Specs Reviewed

1. `2026-09-01-taskq-trial-batch1-mechanical-fixes-design.md`
2. `2026-09-01-spec-rule-membership-check-design.md`
3. `2026-09-01-lesson-recurrence-check-design.md`
4. `2026-09-01-behavioral-claim-verification-design.md`

Specs 2–4 shipped inline — no implementation plan, no SDD dispatch, no
outcomes file. Their trials and self-reviews served as the implementation.
Absence of outcomes files for them counts as expected under the skill's own
step 3, but the *reason* for the absence is itself a finding (see Misses M4,
Gaps G2).

## Catches

**taskq-trial-batch1-mechanical-fixes** (logged in notes.md; outcomes file read):

- notes 2026-09-01 (Task 1) | `none — found ad hoc` | F1 verification grep
  returned 0 against a correctly-shipped edit — phrase wraps across two lines.
  Third logged occurrence of the line-wrap anchor shape.
- notes 2026-09-01 (Task 2) | `none — found ad hoc` | Same failure, second
  task in a row; the outcomes entry explicitly asks to prioritize the
  standing candidate fix "in a near-term batch rather than continuing to
  absorb per-task cost."
- Outcomes, Task 3: after two wrap catches, the task used short same-line
  anchors from the start and passed first run — the fix works when applied;
  nothing yet makes plans apply it.

**spec-rule-membership-check** (no notes entries; recovered from commits per step 4):

- Commit `83fd4dd` (spec self-review): a cited count ("caught four defects")
  contradicted its own source, whose message states four and enumerates five.
  The spec now cites no count from that source.
- Commit `83fd4dd` (self-applied item-2 procedure): the spec's own
  decision-rule list enumerated four branches and omitted the "arm 2 detects
  alone" member — a missing-member defect in the spec proposing the
  missing-member check. Caught before the trial ran.

**lesson-recurrence-check** (no notes entries; recovered from commits):

- Commit `5c2ea7c`: Falsifiable Criteria 7 and 8 cannot both hold (cost
  sentence required vs. character-for-character match with the tested arm).
  Found after the trial; criterion 7 recorded as failed rather than reworded.
  The author did not run the just-shipped rule-membership check over this
  spec's own criteria list — the check existed and went un-self-applied.
- Commit `5c2ea7c`: the trial's enumeration arm compared 17 of 25 Rule
  sentences — an undercount recorded as an execution defect, not rounded
  into a pass.
- Commit `470c2e7` (re-test): the author's fixture-selection premise —
  that history had picked the wrong neighbouring pattern — was falsified by
  the enumeration arm, which examined the asserted better match and ruled it
  out with a reason. The premise was itself a two-Rule comparison done by
  reading. Second undercount also recorded (16 of 17).

**behavioral-claim-verification** (no notes entries; recovered from commits):

- Commit `2aa0d8d` (self-applied item-2 procedure): the decision rule's first
  draft left "arm 1 detects on one fixture while arm 2 detects on both" with
  no covering branch — the same missing-member shape as `83fd4dd`, in the
  next spec written.
- Commit `62950d7`: run 1's detection criteria named one specific sentence
  per fixture, which measured which claim an agent chose to examine rather
  than whether the mechanism worked — the pattern's Rule 3 shape, committed
  by the pattern's own user. Run recorded inconclusive.
- Commit `62950d7`: the blind judge returned `A: YES` on a sentence
  addressing a different claim than the criterion named. Caught only by
  reading the judge's quoted evidence against the criterion's wording; a
  bare-verdict judge prompt would have shipped it. Now Rule 4 of
  `ab-test-live-trials-for-behavior-change.md` (commit `eecbe81`).
- Trials (all three): arms read their `--plugin-dir` harness directory as
  project state; one control arm built a blocking finding on it. Symmetric,
  so no verdict biased. Now the third rule of
  `seed-trial-fixtures-with-real-docs.md` (commit `eecbe81`).

**Session-wide, caught by end-of-session review rather than any gate**
(commits `bc442a5`, `fa58dfb`, `eecbe81`):

- Three skill files changed across three specs with no version bump in any
  of the seven declared files, until a user-prompted review found it.
- The tracker's "Specs shipped since" list sat at 1 while four specs had
  shipped — the 3-entry review trigger was already exceeded and suppressed.
- Zero notes.md entries written for specs 2–4; every catch above survived
  only in commit messages and spec RESULT sections.

## Misses

- **M1 — Decision-rule missing-member, 2 of the reviewed specs**
  (`83fd4dd`, `2aa0d8d`). Same defect, same day, second occurrence written
  after the first was documented. Both caught by deliberately self-applying
  the new item-2 rule-membership procedure — post-hoc, not at drafting time.
  Upstream fix exists and is cheap: pre-register decision rules as per-unit
  states combined exhaustively, instead of enumerating example branches. See
  Recommendation R2.
- **M2 — Version-file drift, second window in a row.** notes 2026-09-01
  (research-skill-adoption, prior window) records five of seven files left
  at 6.2.0; this window repeated the class at seven of seven until `bc442a5`.
  The declared guard, `plugin/scripts/bump-version.sh --check`, has never
  run successfully on this machine (notes 2026-09-01: `jq` not installed —
  dies at line 46). A guard that cannot execute equals no guard; second
  recurrence escalates it past "known issue." See Recommendation R3.
- **M3 — Line-wrap verification anchors, fourth and fifth logged
  occurrences** (notes 118, 119), after the candidate fix was proposed
  (notes 113), re-confirmed (118), and explicitly requested for
  prioritization (119 and the outcomes file). The fix has now been deferred
  past the threshold `escalate-deferred-items-on-second-recurrence.md`
  names. See Recommendation R1.
- **M4 — Real-time bookkeeping bypassed across 3 of the reviewed specs.**
  Specs 2–4 shipped through a path (spec → trial → ship, no plan, no SDD)
  that owns none of the Finish gates: no notes.md entries, no tracker
  append, no version bump, no lessons capture until a user-prompted
  end-of-session review performed all four by hand. Lesson 25 ("the review
  discipline still applies directly") is goodwill, and this window measured
  what goodwill produces: the gates ran only when a human asked. See
  Recommendation R4 and Gap G2.

## Friction

- **F1 — The behavioral-claim trial ran twice.** Run 1 (4 dispatches + 1
  judge) was discarded for a mis-specified criterion and a mis-scored
  verdict; a class-level criterion was registered (`192c30a`) and the trial
  re-ran fresh. The re-run was the correct call — but the cost was one full
  trial cycle, and both defects were foreseeable from the pattern's own
  Rules 2–3. Converted to Rule 4 and a lesson; no further action beyond R2.
- **F2 — Inline implementation under a spawn limit.** All seven
  taskq-batch1 tasks report "implemented directly (subagent spawn limit
  still exhausted)." The work shipped correctly, and per-task review
  discipline held, but the plan was written for dispatch and executed by
  hand seven times. Recorded as friction; no recommendation — the limit is
  environmental, not process.

## Gaps

- **G1 — The F2 premise shape remains uncovered.** The widened item 6
  reaches "an absent instruction does not establish an absent behavior" but
  failed both runs on "two checks' titles do not establish overlap"
  (`208ddd2` RESULT). No current check covers title-based overlap claims.
  Candidate needing more definition — the convention-retirement spec's
  Retirements reason set partially covers it at review time, but nothing
  covers it at spec-writing time. No forced recommendation.
- **G2 — The plan-less shipping path has no owner.** Specs 2–4 followed
  spec → trial → ship. `subagent-driven-development` owns Finish for
  dispatched plans; `executing-plans` owns inline plan execution; nothing
  owns a spec whose implementation *is* its trial. R4 covers the
  executing-plans half; the plan-less half stays an open gap — naming a
  concrete home for it needs its own design conversation, not a checkbox
  here.
- **G3 — Attribution coverage for this window: effectively zero.** Of the
  window's catches, 2 carry `none — found ad hoc`, 0 name a specific check,
  and roughly a dozen were never logged at all (recovered from commits).
  Zero-yield retirement analysis is unusable on this data, and will stay
  unusable while M4 stands.

## Recommendations

- [ ] **R1** — Add the drafted-insertion check to `writing-plans` Self-Review
  item 10 (`plugin/skills/writing-plans/SKILL.md`): before finalizing a
  plan, write each task's drafted insertion text to a scratch file and run
  the task's own verification grep against that file — a baseline-only run
  cannot catch a wrap, a duplicate, or an undercount that exists only in
  text not yet inserted. Net new load — five logged occurrences across
  three sub-projects, candidate fix proposed twice, explicitly requested by
  the latest outcomes file.
- [ ] **R2** — Add one sentence to
  `docs/patterns/ab-test-live-trials-for-behavior-change.md` Rule 1:
  pre-register the decision rule by scoring each arm/fixture independently
  and combining the per-unit states exhaustively — enumerate the outcome
  space, never example branches. Net new load — the missing-branch defect
  recurred in both same-day specs (M1), caught only by post-hoc
  self-application.
- [ ] **R3** — Remove the `jq` dependency from
  `plugin/scripts/bump-version.sh` (port the JSON reads to python or node,
  both present on this machine) so `--check` can actually run here. Names
  the check it replaces: the script's own currently-unrunnable `--check`
  mode. Second-window recurrence of the exact drift it exists to prevent
  (M2).
- [ ] **R4** — Add a Finish bookkeeping section to
  `plugin/skills/executing-plans/SKILL.md` mirroring SDD's list (notes.md
  gate, tracker append, version bump when `plugin/skills/` changed, lessons
  capture, spec Status flip), so the inline path carries the same gates as
  the dispatched path. Net new load — 3 of 4 reviewed specs shipped with
  zero real-time bookkeeping (M4).

## Retirements

Attribution coverage this window: 0 entries name a check, 2 read
`none — found ad hoc`, and roughly a dozen catches were never logged
(recovered from git per step 4). Unattributed entries dominate completely,
which makes Zero-yield unusable on this window's data — this section
therefore proposes no removals the data cannot support.

None.
