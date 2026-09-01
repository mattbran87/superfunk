# Process Review — after 2026-09-01-convention-retirement-design.md

**Date:** 2026-09-01
**Window:** the three specs below, covering 21 commits since the 2026-08-30 review.

## Execution environment — read before weighing M1, M2, and G2

Superfunk never loaded as a plugin during this window. `~/.claude/plugins/config.json` reads `{"repositories": {}}`, and the session ran upstream `superpowers@claude-plugins-official` 5.1.0, whose `writing-plans` carries 3 Self-Review items to superfunk's 14, whose `brainstorming` carries 4 spec-review items to superfunk's 7, and which ships no `process-review` skill at all.

Superfunk's conventions therefore got applied by hand: its 14 Self-Review items, its Pseudocode triggers, its Global Constraints header, and this review's own procedure were all read from the repository's files and performed manually, by the same agent that wrote the documents under review.

Two consequences for the findings below:

- **M1, M2, and G2 report a check that a self-interested reader applied to its own work, not a skill that fired in fresh context.** The scope gap they identify belongs to the check's wording and holds regardless. The evidence that the check "did not catch" the failures is weaker than a live invocation would give, since the same agent authored both the plan and its review.
- **The trial findings are exempt.** Every `--plugin-dir` invocation pointed at this repository's plugin, so the research-skill-adoption A/B trial and both convention-retirement retirement runs exercised superfunk's real skills in fresh sessions. Those findings carry full weight.

## Specs Reviewed

- `2026-08-30-checkpoint-priority-and-conditional-gate-design.md`
- `2026-09-01-research-skill-adoption-design.md`
- `2026-09-01-convention-retirement-design.md`

## Catches

15 entries logged in this window.

**checkpoint-priority-and-conditional-gate (2)**
- Plan self-review: two verification commands anchored on a phrase living in the spec's own Context section rather than in the skill text the plan inserts. Both checks would have returned 0 regardless of correctness.
- Task 2: the fix for that catch failed too — the corrected phrase spans a markdown line wrap, so no single-line grep matches it.

**research-skill-adoption (7)**
- Task 1: the plan's Global Constraints forbade touching files the plan's own Step 6 required editing. The implementer escalated rather than picking a side.
- Task 1: `check_docs.py` returned `ACTION_NEEDED` against a nested README for the second recorded time; BUG-0001 documents the cause and stays Open.
- Task 1 code quality review: the version bump covered 2 of the 7 files `.version-bump.json` declares.
- Task 1 code quality review: `bump-version.sh --check` cannot run here at all, since `jq` never got installed. The drift-detection tool built to prevent the finding above has therefore never executed in this environment.
- Task 2: a predicted grep count of 6 against a real answer of 7, from a miscounted baseline plus a self-documenting example line.
- Task 6 A/B trial: two of three added mechanisms falsified.
- Task 6 trial design: the first trial's prompt foreclosed the behavior it existed to test.

**convention-retirement (6)**
- Task 2: a verification anchor spanning a line wrap, in the very text the plan prescribed inserting.
- Task 3: a predicted count of 2 against a real answer of 3, undercounting the plan's own insertion.
- Task 3: the structural root cause behind all predicted-count failures, recorded.
- Task 5 trial run 1: the fixture leaked the answer via the design spec's own Context.
- Task 5 trial run 2: the leak survived the scrub through the fixture's git history.
- Task 5 trial: all three subsumption candidates the spec asserted failed examination against shipped text.

## Misses

**M1 — Predicted verification counts fail across every spec in this window.** Five instances across all three specs: two in checkpoint-priority, one in research-skill-adoption, two in convention-retirement. Five distinct sub-varieties, no two alike:

- an anchor quoting the spec instead of the target file
- a phrase spanning a markdown line wrap
- a bare substring over-matching a longer name
- a miscounted baseline, compounded by a self-documenting example line
- an undercount of the author's own drafted insertion

`writing-plans` Self-Review item 10 exists to catch exactly this class, and caught none of them. Every one surfaced when an implementer ran the command.

**M2 — The line-wrap variety recurred after one catch, one log entry, and one fix.** checkpoint-priority hit it on 2026-08-31 and recorded it. convention-retirement hit the identical shape on 2026-09-01, in a plan written after that entry existed. Logging a failure did not prevent its repeat, because nothing converts a `notes.md` entry into a check that runs.

**M3 — Trials that could not test what they existed to test.** research-skill-adoption's first A/B trial used a prompt saying "treat this as fully specified." That framing forecloses the do-nothing option the trial existed to detect. convention-retirement's trial fixture then leaked its own answer twice — first through a copied spec, then through git history. Three occurrences across two specs. In every case the trial or its re-run surfaced the defect, never the plan's Self-Review.

## Friction

**F1 — research-skill-adoption Task 1 took four commits to settle:**

- `3a602d5` implemented it
- `283dce7` fixed the plan contradiction it exposed
- `349b21c` fixed the version drift the review found
- `934ed5d` corrected the spec and plan scope

The task itself stayed small. The surrounding documents needed three corrective rounds.

**F2 — Subagent dispatch hit the session API limit mid-plan.** A dispatched reviewer died with no result, forcing a switch to inline execution for three tasks of research-skill-adoption. The work completed, but the two-stage review discipline degraded to self-review for those tasks.

## Gaps

**G1 — `notes.md` uses an unescaped `|` delimiter, and findings routinely contain pipes.** This review's own attribution tally miscounted a four-field entry as five-field, because that entry's text quotes `grep ... | grep -c ...`. Any tool splitting entries on `|` inherits the same error. The five-field format shipped this window, so the defect ships with a mechanism whose whole purpose depends on reading that fourth field accurately.

**G2 — Plan Self-Review cannot check text that does not exist yet.** Item 10 requires running verification commands against real content. Every plan in this window did so — against each file's pre-edit state, to establish baselines. A baseline run cannot detect a wrap, a duplicate, or an over-match living only in text the plan has not yet inserted. M1 and M2 both sit in that blind spot.

**G3 — BUG-0001 has cost two implementers time in five days and stays Open.** Neither occurrence produced a fix. An implementer with no knowledge of the first rediscovered the second from scratch.

**G4 — `jq` absent means `bump-version.sh --check` has never run.** The tool built to prevent version drift cannot execute in the environment where the drift occurred.

## Recommendations

- [ ] Add a Self-Review item to `plugin/skills/writing-plans/SKILL.md` requiring this: for each verification command the plan states, write the drafted insertion text to a scratch file and run that exact command against it before finalizing. A baseline run against the target file's pre-edit state does not satisfy the item. Addresses M1, M2, G2. **Replaces nothing; net new load** — item 10 stays, since it governs counts about existing content, while this covers counts about content nobody has written yet. The two do not overlap.
- [ ] Add one sentence to `plugin/skills/writing-plans/SKILL.md` item 10 pointing at the new item above, so a reader of item 10 learns that pre-edit baselines do not satisfy it. **Replaces nothing; net new load** — one cross-reference sentence, no new check.
- [ ] Change the entry format in `docs/superpowers/process-reviews/notes.md`'s header. State that a finding containing a literal `|` escapes it as `\|`, and that a reader splits on unescaped `|` only. Addresses G1. **Replaces nothing; net new load** — a format constraint, not a check.
- [ ] Fix BUG-0001 at `plugin/skills/documentation/scripts/check_docs.py:47`. Match any path whose basename equals `README.md` or `CHANGELOG.md`, rather than requiring an exact root-level match. Addresses G3. **Replaces nothing; net new load** — a code fix, no process check added.
- [ ] Add a `jq` presence check to `plugin/scripts/bump-version.sh`. It exits with a message naming the missing dependency, instead of dying at line 46 with `jq: command not found` and an unbound-variable error. Addresses G4. **Replaces nothing; net new load** — an error path, no process check added.

## Retirements

**Attribution coverage in this window: 6 of 15 entries carry a check field. Of those, 5 name a specific check and 1 reads `none — found ad hoc`. The remaining 9 carry no check field at all**, since they predate the five-field format, which shipped mid-window.

**Zero-yield does not apply this review, for two independent reasons.** First, 9 of 15 entries carry no attribution, so a check's absence from the log proves nothing about its yield. Second, the reason requires no attribution across the last 3 reviews, and the attribution field has existed for part of one. No removal gets proposed on Zero-yield grounds.

**Subsumed, Superseded, and Vacuous — examined, nothing proposed.**

That spec's own trials examined the three subsumption candidates `2026-09-01-convention-retirement-design.md`'s Context names, and rejected all three against shipped text, with citations since verified. Its Context now records the rejections. Nothing in this window's evidence disturbs them.

One candidate deserves explicit mention and explicit rejection. `writing-plans` item 10 produced zero catches across five failures it exists to prevent, which reads superficially like a Zero-yield case. It does not qualify as one. Item 10 never failed to fire — it fired and passed, because every count it checked held true of the pre-edit files. The defect sits in its scope, not its value, and the first Recommendation above narrows that scope rather than removing the item. **Retiring an under-powered check rather than a redundant one removes the discipline and keeps the gap.**

**None.**

No check or gate gets proposed for removal this review.
