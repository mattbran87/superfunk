# Outcomes — 2026-09-01-research-skill-adoption.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Copy the three skills into the plugin and bump the version
Shipped, with two divergences that both traced to plan defects.

First, the plan contradicted itself: Global Constraints forbade touching any file outside `plugin/skills/` and `plugin/.claude-plugin/`, while Step 6 required drafting a README update when `check_docs.py` reports `ACTION_NEEDED`. The implementer hit the contradiction and escalated as `DONE_WITH_CONCERNS` rather than silently picking a side. Resolved by naming `plugin/README.md` in the constraint, since this repository holds no root `README.md`.

Second, `check_docs.py` returned `ACTION_NEEDED` against a nested README for the second recorded time. BUG-0001 has documented that root cause since 2026-08-28 and stays Open. The plan wrote a verification step around a check a known-open bug guarantees will fail, because the output was predicted rather than checked against the bug tracker. Recorded a second-occurrence note on BUG-0001; no duplicate filed.

The code quality review then found the version bump covered 2 of 7 files. `plugin/.version-bump.json` declares seven files carrying the plugin version; the spec and plan both said "both manifests," written from the two files the author knew rather than from the repo's own declared list. Fixed to all seven, and Criterion 8 now iterates that declaring file instead of naming paths from memory.

Byte-for-byte equality of the three copies was verified programmatically (`Buffer.equals`), not by visual diff.

## Task 2: Fit the adopted copies to the plugin
Shipped. Scope grew mid-task from "repair six `adhd-research` references" to also cover the `superfunk:` namespace prefix on both `REQUIRED SUB-SKILL` markers and `branching-research`'s description, both surfaced by Task 1's code quality review. All three share one root cause: the files were written for a user-level context where `adhd-research` exists, no plugin namespace applies, and a description could position against a sibling.

The positioning/provenance split held. The three provenance references kept their evidence claim ("prior testing of this technique") rather than being deleted, per `process-review`'s real-evidence-over-vibes principle. The namespace prefix was not over-applied: exactly 2 `superfunk:` occurrences, both in `REQUIRED SUB-SKILL` markers, with 10 bare backticked prose references left untouched.

One divergence: the plan predicted `grep -c` would return 6 for the namespace check; the real answer is 7. Two compounding errors — `writing-plans` carries three such markers, not two, and `writing-skills:283` is the house standard's own "✅ Good" example line, which matches any grep for the pattern it documents. The implementer ran the command, found the mismatch, and reported `DONE_WITH_CONCERNS` rather than accepting it.

## Task 3: Give brainstorming's step 4 a mechanism
Shipped, then partly withdrawn. All three requirements landed and verified, then Task 6's A/B trial falsified two of them. Only confidence grounding remains. See Task 6.

Executed inline rather than by subagent: the session hit its API limit and a dispatched reviewer died mid-run.

## Task 4: Add ranking sensitivity to calibrating-recommendations
Shipped, then fully withdrawn after Task 6's trial. `plugin/skills/calibrating-recommendations/SKILL.md` now sits byte-identical to its adopted source, confirmed by `diff`. Decision section 5 of the spec is marked NOT SHIPPED with the reasoning.

## Task 5: Add the null-option baseline to multi-lens-research
Shipped and kept, despite the trial falsifying the same idea on the inline path. The two paths differ structurally: `multi-lens-research`'s four lenses each must propose an approach, so no lens can supply a defer option, whereas the inline path showed the model volunteers restraint unprompted. This path was not itself trialed — an untested mechanism kept on a structural argument, which is a follow-up candidate, not a validated result.

## Task 6: Verify every criterion, and run the A/B trial
Criteria 1–8 all pass. Criterion 9 falsified two of three mechanisms and the spec was rewritten to say so.

Four arms across two scenarios. Arm A pinned to the pre-edit commit with all three adopted skills already present, so step 4 stayed the only difference. Prompts never named the behavior under test.

- **Confidence grounding — validated.** Absent from both pre-change arms, present in both post-change arms.
- **Flip factor — falsified.** Present in three of four arms, including two pre-change arms that produced it unprompted ("the ranking changes", "the strongest argument against my recommendation").
- **Null option — falsified.** In the scenario where deferring stayed defensible, the pre-change arm made "Measure before caching" its first approach *and* its recommendation, writing "180ms p50 may simply not be worth fixing." The post-change arm, carrying the instruction, offered three caching implementations and raised restraint only as a caveat around the set.

Trial 1 turned out to be incapable of testing the null option at all: its prompt said "treat this as fully specified," which forecloses "build nothing" before the agent starts. The first-pass read nearly recorded that as a property of the mechanism rather than of the scenario. Re-running with a fair scenario produced the real, opposite-signed finding.

**Follow-up:** the multi-lens null-option baseline (Task 5) ships untested. A trial exercising the fan-out path would either validate it or retire it the way the inline version was retired.
