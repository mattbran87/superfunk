# Convention Retirement — Design

**Date:** 2026-09-01
**Status:** Shipped (Context corrected and Criteria 7-8 amended after the trials)
**User-Facing:** No

## Context

`process-review` generates rules and never retires them. All five of its
output sections — Catches, Misses, Friction, Gaps, Recommendations — add.
A probe across all 24 skill files, plus `docs/principles.md` and
`docs/ai-code-guidelines.md`, finds no mechanism that retires a process rule,
check, gate, or skill. The closest existing mechanism,
`writing-plans/SKILL.md:270-278`, retires stale codebase text after a
capability lands, which solves a different problem.

Measurements confirm the one-way ratchet. Every measurement point rises, and
none falls:

- Total instruction volume across `plugin/skills/*/SKILL.md` grew from 19,031
  words on 2026-08-08 to 30,959 words on 2026-09-01 — 63% in 24 days,
  monotonically increasing on every day that recorded a change.
- Skill count grew from 14 to 22 over the same period.
- `writing-plans`' Self-Review grew from 3 items to 14 across eight separate
  increases and zero decreases: 3, 4, 6, 7, 8, 9, 11, 12, 14.

### The attribution gap

`notes.md` records where a Catch happened, not which check found it. Its
label field holds a phase — "Final review" appears 29 times, "Task 1" 13
times, "Plan self-review" 7 times. Only 18 of its 88 entries name a specific
numbered check. The framework therefore cannot answer "has item 7 ever caught
anything," which forecloses any retirement rule that depends on a check's
yield.

### Subsumption candidates — examined and rejected after the trials

**Corrected after implementation.** This section originally asserted that
three overlaps exist among shipped checks today, and used that claim to argue
a retirement pass would have work on its first run. Two live trials examined
all three against the shipped text and rejected every one, with citations
this spec's author then verified:

- Items 5, 6, 8, and 9 share a theme but not a trigger or an action.
  `notes.md` 2026-08-27 records that "item 8's own grep scope (same file plus
  design spec only) would not have caught this instance," so item 8 does not
  reach item 9's territory.
- Item 11 covers a gap items 1 and 2 never reached. `notes.md` 2026-08-28
  records that the missing Global Constraints header went undetected across
  every plan that session because the Self-Review "has no item checking a
  plan's own header against its own required template." Item 11 exists
  because of that gap. Its "same class of gap" wording makes an analogy about
  severity, not a coverage claim.
- Item 10 and `brainstorming` item 6 fire on different artifacts at different
  phases — item 6 on a spec's claims about the existing codebase, item 10 on
  a plan's `Expected:` values. Retiring either leaves its own document
  unchecked.

The three claims as originally written follow, kept for the record:

1. `writing-plans` items 5, 6, 8, and 9 all check one theme — whether an edit
   stays consistent with related content elsewhere. Sibling-pattern parity,
   rule-restatement accuracy, cross-section mechanism consistency, and
   worked-example currency plausibly compress to two checks.
2. `writing-plans` item 11 annexes the territory of items 1 and 2. Its own
   text calls a missing header section "the same class of gap as a missing
   task for a spec requirement," which describes item 1, while item 2 already
   scans for incompleteness.
3. `writing-plans` item 10 and `brainstorming` item 6 maintain the same
   numeric-verification discipline in two places.

### Origin

A review of `github.com/AminBlg/LeCunSkills` rejected eight of its nine
skills. The ninth, `lecun-first-principles`, contributed its assumption-autopsy
step, which asks what evidence supports a belief as against what merely
repeats tradition. Applied to a framework that accumulates its own conventions
at high velocity, that question becomes: does this check still earn its slot?
`2026-09-01-research-skill-adoption-design.md` deferred this work to its own
spec.

## Decision

### 1. `notes.md` gains a check-attribution field

The entry format grows from four fields to five:

```
- <YYYY-MM-DD> | Catch | <task/spec label> | <check that caught it> | <finding>
```

The fourth field names the specific check that produced the Catch — for
example `writing-plans item 10`, `brainstorming item 6`, or `SDD spec-review`.
When no check produced it, the field reads exactly `none — found ad hoc`.

That literal value carries weight. Most Catches so far trace to no specific
check. A format offering no legitimate way to say "nothing caught this"
pressures a writer to fabricate attribution, which produces worse data than
no attribution at all.

`notes.md`'s header gains this format line, replacing the current one.

**No backfill.** The 88 existing entries keep four fields. `process-review`
reads both shapes and treats a four-field entry as carrying no attribution.
Reconstructing which check caught a finding from weeks ago means inventing
attribution from memory — the failure this project recorded five times during
the sub-project that produced this spec.

### 2. `process-review` gains a Retirements section

The section follows Recommendations in the review file, and uses the same
`- [ ]` checkbox form, so a human decides each removal. Removal stays
advisory because a wrongly-removed check produces silence, while a
wrongly-added check produces visible friction — the two errors differ in how
easily anyone notices them.

Each entry names the check, the proposed action, and exactly one reason drawn
from this fixed set:

- **Subsumed** — another check already covers this. The entry names that
  check.
- **Superseded** — the mechanism this check guards changed. The entry names
  what changed.
- **Vacuous** — this check's precondition never holds in this project. The
  entry names the precondition.
- **Zero-yield** — no `notes.md` entry attributes a Catch to this check
  across the last 3 reviews, and the check existed at the start of that
  window. The entry states both facts.

The fixed set does real work. An open-ended reason like "seems unnecessary"
lets any check get argued away, which converts a retirement mechanism into a
tool for deleting whatever the reviewer finds inconvenient.

**Zero-yield threshold: 3 reviews.** This mirrors the existing
3-specs-per-review trigger, so a check accumulates roughly 9 specs of
exposure before anyone may claim zero yield. A check that entered the corpus
partway through the window does not qualify, since its absence from earlier
entries proves nothing.

### 3. Recommendations name what they replace

`process-review`'s Recommendations step gains one rule: a Recommendation that
adds a check or a gate names either the check it replaces, or states `net new
load` followed by a one-line justification. No Recommendation adds a check
silently.

This attacks accumulation at its source, where section 2 removes what already
accumulated. Neither substitutes for the other.

### 4. Enforcement

Per `docs/principles.md`'s Mechanisms, Not Goodwill, each decision names what
checks it:

- The `notes.md` field: a five-field format makes a missing attribution
  visible to `grep`, since a four-field entry written after this ships stands
  out against the documented format.
- The Retirements section: `process-review`'s existing "No Placeholders"
  rule extends to cover it, so every reason names a real check, a real
  mechanism change, or a real precondition.
- The Recommendations rule: a Recommendation carrying neither a replaced
  check nor a `net new load` line counts as a review defect, the same class
  as a Recommendation with no target file.

## Falsifiable Criteria

1. `docs/superpowers/process-reviews/notes.md`'s header states the
   five-field format, and names `none — found ad hoc` as the value for a
   Catch that no check produced.
2. A direct read of `plugin/skills/process-review/SKILL.md` confirms a
   Retirements section that lists exactly the four reasons in Decision
   section 2, and states the 3-review zero-yield threshold.
3. A direct read confirms `process-review` reads both four-field and
   five-field `notes.md` entries, and treats a four-field entry as carrying
   no attribution.
4. A direct read confirms the Recommendations step requires either a named
   replaced check or a `net new load` line.
5. The 88 pre-existing `notes.md` entries stay unmodified. `git diff` over
   `notes.md` shows only added lines and the header format line.
6. **A disposable `--plugin-dir` trial runs `process-review` against a
   fixture holding this repository's real `notes.md`, tracker, and skill
   files. The run produces a Retirements section naming at least one real
   check with a reason from the fixed set.**
7. **Every Retirement the trial proposes survives independent checking.** A
   second agent, given only the proposed Retirement and the files, confirms
   the named subsumption, supersession, or vacuity actually holds. A run that
   proposes deleting a check whose stated overlap does not survive checking
   falsifies this design, which then does not ship. This criterion, not
   criterion 6, carries the risk: a section that confidently proposes
   deleting checks on invented overlap damages the framework faster than no
   retirement mechanism at all.

   **RESULT: untested.** Both trial runs proposed zero Retirements, so no
   proposal existed to check. The runs did the opposite of the feared
   failure — they examined six candidates across the two runs and rejected
   every one against real shipped text, rather than reaching for a removal.
   That gives no evidence about how the section behaves when it does propose
   one. This criterion stays open until a review proposes a Retirement.
8. The trial's fixture receives no hint about the three subsumption candidates
   this spec's Context names. A run seeded with those candidates tests
   nothing, per `docs/patterns/ab-test-live-trials-for-behavior-change.md`
   Rule 2.

   **RESULT: passed in part, on the second attempt.** Run 1's fixture leaked
   the candidates: the build copied this spec into the fixture's specs
   directory, and its Context names all three. The run detected the
   contamination and disclosed it unprompted. Run 2 removed that spec, and
   the leak survived anyway by a second route — the fixture's git history
   still held run 1's committed review file, which the run retrieved with
   `git show` and again disclosed unprompted.

   Run 2 nonetheless demonstrated genuine independent discovery on a
   candidate no document named: `writing-plans` item 12, tested for Vacuous.
   The run grepped all 10 fixture specs, found exactly one carrying
   `User-Facing: Yes`, and rejected the vacuity claim on that evidence. It
   also tested items 13 and 14 for Zero-yield and rejected them on the
   check's-age half of the rule, both having shipped inside the window.

   Scrubbing a fixture means scrubbing its git history too, not only its
   working tree.

## Alternatives Considered

Step 4's inline proposal ran for this decision; no formal research skill
dispatched. Candidates:

- **A — Retirements section in `process-review`, plus the `notes.md`
  attribution field.** Reuses an existing trigger and an existing output
  shape.
- **B — A separate `retiring-conventions` skill on its own cadence.** Allows
  a deeper audit without diluting `process-review`, at the cost of a 23rd
  skill and a second trigger to maintain. Rejected: it answers an additive
  problem by adding, and skill count already grew 14 to 22 in 24 days.
- **C — Recommendations name what they replace.** Cheapest, and it stops
  accumulation at the source, but it governs only new additions and leaves
  the existing 14 items and the subsumption cluster untouched.
- **Do nothing.** The ratchet continues. Rejected because the measurements
  above show 24 days of monotonic growth with zero removals, and this
  session produced direct evidence that added instructions can suppress
  behavior a model already produced.

**Recommendation: A combined with C**, since they act at opposite ends —
C prevents accumulation, A removes what accumulated.

**Confidence: Medium.** Named evidence: `process-review` already reads
`notes.md`, outcomes files, and `git log`, and already emits five output
sections, so a sixth section reuses a proven shape in that file; its
3-specs-per-review trigger exists and currently sits at 2; and the three
subsumption candidates in Context give the immediate half real work on its
first run.

**What would lower it:** the zero-yield half ships unvalidated and stays that
way for at least 3 review cycles, since no attribution data exists yet.

## Consequences

`process-review` gains the ability to propose removal, which no mechanism in
the framework currently holds. Reviews stop acting as a one-way ratchet.

Every future `notes.md` entry costs one more field to write. That cost buys
per-check yield data, which no other source supplies.

The zero-yield reason produces no findings until 3 reviews accumulate
five-field entries. Until then, only Subsumed, Superseded, and Vacuous fire.
A reader who expects immediate yield-based retirement finds none, so the
Retirements section states its own attribution coverage on every run.

Retirement stays advisory. A reviewer who never ticks a Retirement checkbox
leaves the ratchet in place, and no mechanism here forces the tick. This
design accepts that, because automatic removal of a check nobody re-read
carries more risk than a Recommendation nobody actions.

The assumption that must hold: reviewers attribute Catches honestly rather
than defaulting every entry to `none — found ad hoc`. If that default
dominates, the yield data reads as though no check ever catches anything, and
zero-yield becomes a mechanism for retiring the entire corpus. The
Retirements section therefore reports the ratio of attributed to
unattributed entries in its window, so a degenerate default stays visible
instead of silently driving removals.

## Deferred

- **The three subsumption candidates named in Context.** Recorded there as
  observations, deliberately NOT supplied to the first Retirements run.
  Whether the section independently surfaces them measures whether it works.
- **Whole-skill retirement.** This design covers checks and gates only. Skill
  count grew 14 to 22, but removing a skill breaks cross-references across
  the plugin, which needs its own design.
- **`docs/patterns/` and `docs/lessons-learned.md` growth.** Both accumulate
  monotonically too. Both hold reference material read on demand rather than
  instructions that fire every run, so neither creates the ritual friction
  this spec targets.
- **Backfilling attribution onto the 88 existing entries.** Rejected rather
  than deferred; reconstructing it from memory would fabricate the data.
