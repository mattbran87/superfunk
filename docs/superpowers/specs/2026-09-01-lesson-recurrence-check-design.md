# Lesson Recurrence Check — Design

**Date:** 2026-09-01
**Status:** Shipped (the trial reached decision-rule branch 2; the promotion step carries the tested wording)
**User-Facing:** Yes

## Context

`plugin/skills/subagent-driven-development/SKILL.md:607-608` already carries a
recurrence rule:

> "A Lesson promotes to a Pattern when it answers that question yes, or when
> the same failure mode recurs a second time — whichever comes first."

The rule missed a recurrence that happened one day apart.

`docs/lessons-learned.md:108` and `:124` describe one failure. Each entry
closes with "single occurrence" and defers promotion. Their titles share
nothing:

- ":108 — An added instruction can suppress a behavior the model already
  produced"
- ":124 — Candidates asserted to justify a design can fail the design's own
  first test"

Their **Rule:** sentences converge:

- ":108 — before adding an instruction to make a model do X, check whether it
  already does X without one"
- ":124 — check those claims against the record of what those artifacts did —
  not just against their text"

Both entries record one act: the author needed to know what something does,
gathered evidence about what a file says, and treated the second as settling
the first. Entry 108 grepped 24 skill files. Entry 124 read check titles and
first sentences.

### Why the existing rule missed it

The rule names a condition and no procedure. To apply it, the writer must hold
every prior entry's failure mode in mind and compare the new one against all of
them, across a file that now runs 343 lines. Each entry also writes its own
recurrence condition in the vocabulary of its own instance, so ":124" cannot
satisfy ":108"'s stated condition and the reverse also fails.

### Three measured instances of the same shape, all from 2026-09-01

| Judgment item | Measured outcome |
|---|---|
| `brainstorming` Spec Self-Review item 2, before today's change | Two arms of a controlled trial missed a contradiction fifteen lines wide. The procedural arm caught it. |
| `writing-plans` Self-Review item 7 | The catch log at `docs/superpowers/process-reviews/notes.md` holds 97 entries. None names item 7 as the mechanism that caught something. |
| `subagent-driven-development` SKILL.md:607-608 | Missed a recurrence that arrived one day later. |

`2026-09-01-spec-rule-membership-check-design.md` shipped the first of these
after a three-arm trial. The same repair applies here: name a trigger, a
mechanical act, and a place to look.

## Decision

### 1. Run a two-arm trial before any wording ships

**Fixture.** `docs/lessons-learned.md` at commit `fbcec90`, which holds entry
108 and not entry 124. Rebuild the repository as a single-commit tree at that
state, so no later commit reveals how the promotion decision went.

**Dispatch.** One prompt, identical across both arms. The prompt supplies the
convention-retirement finding as raw material and asks the agent to complete
the Lessons-learned capture step, including its promotion note. The prompt
never mentions entry 108, never uses the word "recurrence," and never states
that a prior entry relates to this one.

**Arms.** Each arm changes `subagent-driven-development/SKILL.md:607-608` and
nothing else:

| Arm | The promotion step carries |
|---|---|
| 1 · Control | the wording that ships today |
| 2 · Procedure | plus the enumeration in Decision 2 |

**Detection criterion, recorded before the first run.** An arm detects when its
output names entry 108 as describing the same failure mode as the new entry,
and promotes on that basis. An arm that promotes for a different reason, or
that files the new entry as a single occurrence, misses.

**Judge.** One fresh agent scores both outputs unlabeled and shuffled, and
never learns which arm produced which.

**Decision rule, recorded before the first run.** Read in order, stop at the
first match:

1. Arm 1 detects → ship nothing. The shipped wording already does the work.
2. Arm 2 detects and arm 1 misses → ship Decision 2.
3. Neither detects → the promotion step hosts the wrong check. Reopen at
   `process-review`, which reads the whole lessons file already.

### 2. Ship the enumeration into the promotion step

Replace the recurrence clause with a procedure that enumerates rather than
recalls:

```markdown
Before writing the promotion note, list every existing `**Rule:**` sentence in
`docs/lessons-learned.md`, and state for each whether it names the same act as
this Lesson's Rule sentence — what the author gathered, and what the author
concluded from it. Compare Rule sentences, not titles: two entries describing
one failure often carry titles that share no words, because a title names the
instance and a Rule names the mechanism. A match promotes both entries to one
Pattern, whatever either entry's own promotion note says.
```

The enumeration bounds the work. `docs/lessons-learned.md` holds 28 Rule
sentences at this spec's HEAD, and 25 at the trial fixture's commit — both
counts measured, not estimated. The writer reads a fixed list instead of
recalling an open-ended one. The irreducible judgment shrinks to one question
per entry.

## Alternatives Considered

**Candidates.**

1. **Enumerate every Rule sentence at promotion time** — the recommendation.
2. **Merge entries 108 and 124 by hand.** Cheap, and it closes this instance.
3. **Ship nothing.** Accept that recurrence surfaces when someone notices.

**Recommendation:** candidate 1, gated by the trial in Decision 1.
**Confidence:** high on the diagnosis. Medium on the wording.

**Evidence behind it.** Three judgment items measured on 2026-09-01, each
carrying a real check and each failing to produce a finding: item 2 in a
controlled trial, item 7 across 97 catch-log entries, and the promotion rule
against entries 108 and 124. One procedural replacement already ran a
three-arm trial and detected what two weaker wordings missed.

**Steelman of candidate 2, the strongest rejected alternative.** The merge
costs one edit and closes a real gap today, while the procedure costs a trial
and a wording change that may fail. Against it: a hand-merge repairs one pair
and leaves the mechanism that produced the pair untouched, so entry 125 and
entry 140 repeat it. This spec treats the pair as a symptom.

**Pre-mortem on candidate 1.** The enumeration grows with the file. At 28 Rule
sentences the writer reads a bounded list. At two hundred the step turns
costly, and a writer under pressure skims rather than enumerates. Falsifiable
Criterion 7 records this limit rather than claiming the procedure scales. The
file gained 3 Rule sentences between the fixture's commit and this spec, so a
later reader can measure the growth rate rather than guess it.

## Falsifiable Criteria

1. Before either arm runs, a fresh repository holds the `fbcec90` tree, and
   `git log --oneline` inside it returns exactly one commit.
2. The fixture's `docs/lessons-learned.md` contains entry 108 and contains no
   entry naming convention-retirement's asserted candidates.
3. The two arm prompts match byte for byte; the arms differ only in the plugin
   directory each one loads.
4. Neither the dispatch prompt nor either arm's promotion step contains the
   string `recurrence` alongside a reference to entry 108.
5. Commit `83fd4dd`'s successor recording this criterion carries a timestamp
   earlier than the first arm's output file.
6. The trial report states, for each arm, detected or missed, and quotes the
   sentence the judge scored.
7. The shipped promotion step states the enumeration's cost in its own words,
   so a later reader sees the scaling limit without reading this spec.
8. `subagent-driven-development/SKILL.md` carries the wording of the arm the
   decision rule selects, character for character.

### RESULT — the trial ran on 2026-09-01 and reached branch 2

Commit `8a50b47` recorded the criterion and the decision rule before either arm
ran. The two plugin copies differed in one file at one line. A leak probe over
the shared prompt returned no match for `recurrence`, `recurs`, `entry 108`,
`added instruction`, `already produced`, `promote both`, or `same failure`.

| Arm | The promotion step carried | Verdict |
|---|---|---|
| 1 · Control | the wording that shipped before today | **missed** |
| 2 · Procedure | plus the enumeration | **detected** |

A separate agent scored both outputs unlabeled and shuffled.

**Arm 1 promoted, and still missed.** That result matters more than a refusal
to promote would. Arm 1 wrote a new standalone Pattern,
`verify-overlap-claims-before-proposing-removal.md`, and justified it on the
prospective-rule test: "the rule applies to any argument for removal." It
checked two nearby *patterns* before writing a new file, and never compared
against the *lessons*. Entry 108 went unnamed.

So the control arm does not fail by filing a single occurrence. It fails by
minting a third near-duplicate, which grows the very pile that makes the next
comparison harder.

**Arm 2 named entry 108, promoted both, and amended entry 108's own note.** It
produced the better abstraction as well. Arm 1's pattern covers removal
arguments only. Arm 2's, `check-the-record-before-adding-or-retiring-a-rule`,
covers both directions and states why they share one mechanism: each gathers a
shipped instruction's function from text rather than from evidence of its
behavior, then edits the instruction set on that basis — one adding, one
retiring — and a live run falsified both.

**Arm 2 undercounted, and the procedure still worked.** It reported comparing
against "all 17 existing ones." The fixture holds 25 Rule sentences, measured
from `git show fbcec90:docs/lessons-learned.md`. The enumeration reached 17 of
25 and found the match anyway. This spec records that as a real execution
defect rather than rounding it into a clean pass. A partial enumeration that
happens to contain the matching entry proves less than an exhaustive one.

**Scale caveat.** One fixture, one model, one prompt, one run per arm. This
shows the enumeration found a link the shipped wording missed in this scenario.
It does not measure how often either outcome repeats.

**Fixture note.** Both arms appended their own entry to the fixture's
`docs/lessons-learned.md`, so each arm's working copy holds 26 Rule sentences
afterward. The pristine count of 25 comes from git, not from the post-run
tree.

**Criterion 7 fails, and criteria 7 and 8 contradict each other.** Criterion 7
requires the shipped step to state the enumeration's scaling cost in its own
words. Criterion 8 requires the shipped step to match the tested arm character
for character. Arm 2 carried no cost sentence, so no wording satisfies both.

Criterion 8 wins. Shipping a string no arm ran repeats the failure this whole
sub-project exists to stop, and a missing cost sentence costs a later reader one
lookup. Criterion 7 therefore stands as **failed**, not as satisfied by a
convenient reading.

This spec's own Falsifiable Criteria formed an enumerated list holding two
members that cannot both hold. The rule-membership check shipped in `c5c969d`
covers exactly that shape, and this author did not run it over this document's
criteria list. Recorded here rather than quietly repaired.

## Consequences

The promotion step gains a bounded read of one file and no new checklist item.

A Lesson that repeats an earlier failure promotes on the first repeat rather
than waiting for a reader to notice the resemblance. Entries 108 and 124
promote together when this ships, through the mechanism rather than by hand.

The step costs more on every sub-project, including the many where no
recurrence exists. That cost buys a promotion decision that no longer depends
on recall.

Three of the four decision-rule branches ship either nothing or a different
home. This spec can retire itself.

## Deferred

- **Four patterns that no check covers.** `resolve-skill-files-via-skill-tool-not-glob.md`,
  `self-apply-cross-section-check-to-hand-fixes.md`,
  `validate-tools-against-real-project-data.md`, and
  `verify-reviewer-can-see-what-it-checks.md` appear in none of 66 plans, and a
  probe across `plugin/skills/` finds no check covering any of them. They differ
  from the recurrence gap: nothing routes to them because nothing asks their
  question. `process-review`'s Retirements section exists to decide cases like
  these, and both of its trials proposed zero candidates. Feed these four to it
  rather than deciding by hand. Whether that mechanism handles them stays an
  untested prediction.
- **`escalate-deferred-items-on-second-recurrence.md` has no covering check
  either.** This spec's procedure covers lessons. Deferred items in specs take a
  separate route and stay out of scope here.
