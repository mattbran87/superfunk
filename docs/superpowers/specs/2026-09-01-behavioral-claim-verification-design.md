# Behavioral-Claim Verification — Design

**Date:** 2026-09-01
**Status:** Approved
**User-Facing:** Yes

## Context

`docs/patterns/check-the-record-before-adding-or-retiring-a-rule.md` shipped in
`54d16fe`, promoted from lessons `docs/lessons-learned.md:108` and `:124`. The
pattern states a procedure. No check points at it.

A measurement taken on 2026-09-01 across 66 plans: the 5 patterns cited from a
skill item appear in 20 plan citations, and every one of the 5 reaches at least
one plan. The 11 reachable only through `writing-plans` Self-Review item 7's
judgment lookup appear in 11 citations, and 6 of the 11 reach no plan at all.
The new pattern joins the second group.

### The failure the pattern documents

Two specs shipped a design on a false premise, and a live run falsified both:

- `2026-09-01-research-skill-adoption` ran a keyword probe across all 24 skill
  files, found zero matches, and concluded the model produces neither the
  null option nor the flip factor. The A/B trial found the flip factor in
  three of four arms, including both pre-change arms.
- `2026-09-01-convention-retirement` read three checks' titles and first
  sentences and concluded they overlapped. Two live trials examined all three
  against the shipped text and rejected every one.

Both authors gathered evidence about an artifact's **text** and drew a
conclusion about that artifact's **behavior**. The research-skill-adoption
probe ran correctly and returned a correct result; the inference from it
failed. A grep establishes an instruction's absence, never a behavior's
absence.

### Why item 6 hosts this

`plugin/skills/brainstorming/SKILL.md` Spec Self-Review item 6 already asks
whether the Context or Decision states a count about the existing codebase, and
requires the author to run the command and copy real output. A behavioral claim
asks the same question of the same sections. A count and a behavior differ only
in what the author runs to settle them.

Two changes shipped today, `c5c969d` and `5c2ea7c`, both folded a procedure
into a semantically adjacent step rather than adding a step. The Spec
Self-Review grew from four items to seven, and
`2026-09-01-convention-retirement-design.md` exists because the framework adds
checks and retires none.

### What this spec does not do

`process-review`'s Retirements section takes "one checkbox item per check or
gate this review proposes removing." It does not act on pattern files. Its
Zero-yield reason requires that no entry attributes a Catch to the check, which
holds trivially for every pattern, since nothing ever attributes a Catch to a
pattern. Routing patterns through Retirements would argue for removing all 17.
This spec proposes no pattern removals and treats the six unreferenced patterns
as situational reference material.

## Decision

### 1. Run a two-arm trial across two fixtures before any wording ships

**Fixtures.** Two superfunk trees, each rebuilt as a single-commit repository
so no later commit reveals the correction:

- **F1** — `aa08b7f`, the research-skill-adoption spec as written, before the
  A/B trial amended it. False premise: the model produces neither the null
  option nor the flip factor.
- **F2** — `e9f4f41`, the convention-retirement spec as written, before the
  trials corrected it. False premise: three named checks overlap, so a
  retirement pass finds work on its first run.

F1 carries the harder case. Its author ran a real command and got a real
result; only the inference failed. F2's author read titles. Report the two
separately and do not average them.

**Dispatch.** One prompt per fixture, identical across arms. The prompt states
that the agent just wrote the spec and asks it to run the Spec Self-Review. The
prompt never names a premise, never uses the words "assumption" or "behavior,"
and never suggests the spec contains an error.

**Arms.** Each arm changes item 6 and nothing else:

| Arm | Item 6 covers |
|---|---|
| 1 · Control | counts only, as it ships today |
| 2 · Widened | counts and behavioral claims, per Decision 2 |

**Detection criterion, recorded before the first run.**

- F1 detects when the output states that a keyword probe over skill files does
  not establish what the model produces without an instruction.
- F2 detects when the output states that check titles do not establish
  overlap, and names the record of what each check caught as the evidence that
  would.

An output that merely calls the Context "unverified" without naming the
evidence gap misses.

**Judge.** One fresh agent scores the four outputs unlabeled and shuffled, and
never learns which arm or fixture produced which.

**Decision rule, recorded before the first run.** Score each fixture
independently first, then combine. A fixture **favours the widening** when arm
2 detects on it and arm 1 misses on it. Every fixture lands in exactly one of
four per-fixture states, so the combination below covers all sixteen outcomes:

1. **No fixture favours the widening → ship nothing.** This covers arm 1
   detecting everywhere, arm 2 detecting nowhere, and both arms detecting on
   the same fixtures. Any of those shows the shipped wording already reaching
   the premise shape, or the widening failing to.
2. **At least one fixture favours the widening → ship Decision 2**, and name
   in the report which fixture favoured it and which did not.
3. **No fixture favours it AND arm 2 detects on no fixture at all** → beyond
   shipping nothing, record that item 6 hosts the wrong check, and reopen at
   `writing-plans`, whose Self-Review reads the spec against the plan.

Branch 3 refines branch 1 rather than competing with it; read branch 1 for the
shipping decision and branch 3 for where to look next.

An arm-1 detection on one fixture and not the other stays a real outcome: it
records that the shipped wording already reaches one premise shape. That
fixture simply contributes no evidence for the widening, and the other fixture
decides.

### 2. Widen item 6 to cover behavioral claims

```markdown
6. **Claim verification:** Does any Context or Decision section state a
specific count (occurrences, files, lines) about the existing codebase, or a
claim about what the system or the model already does — that no skill asks for
X, that two checks overlap, that nothing enforces Y? For a count, confirm you
ran the actual command and copied its real output, not an estimate. For a
behavioral claim, name the observation that established it: a Catch record in
notes.md, a control arm, a logged outcome. A grep over source text observes
text, and an absent instruction does not establish an absent behavior. See
docs/patterns/verify-plan-commands-against-real-content.md and
docs/patterns/check-the-record-before-adding-or-retiring-a-rule.md for the
specific failure shapes each has actually hit before — checking against a known
list beats re-discovering the same trap.
```

The item keeps its position and its existing count clause. The heading changes
from "Numeric-claim verification" to "Claim verification", because the item now
covers two claim types.

### 3. Leave the six unreferenced patterns alone

Write no check for them and remove none of them. A pattern reaches an author
through item 7 whether or not a check names it, and
`seed-trial-fixtures-with-real-docs.md` reached two plans by that route. This
spec rejects the premise that every pattern needs a covering check.

## Alternatives Considered

**Candidates.**

1. **Widen item 6** — the recommendation.
2. **Add an eighth Spec Self-Review item** dedicated to behavioral claims.
3. **Ship nothing.** The pattern reaches authors through item 7.

**Recommendation:** candidate 1, gated by the trial in Decision 1.
**Confidence:** high on the diagnosis. Medium on item 6 as the host.

**Evidence behind it.** Two specs shipped false behavioral premises within one
day, both falsified by the first trial that looked. Two trials run today showed
procedural wordings detecting what judgment wordings missed, once at 3 arms and
once at 2. The 5-of-5 versus 5-of-11 citation measurement separates
skill-cited patterns from judgment-reachable ones.

**Steelman of candidate 2, the strongest rejected alternative.** A dedicated
item states one job plainly, and a reader scanning seven headings finds
"Behavioral-claim verification" faster than a clause buried inside a count
check. Against it: the Spec Self-Review already grew from four items to seven,
and an eighth costs every spec a heading whether or not it applies. Item 6
already triggers on the same two sections, so the widening reuses a trigger
that fires rather than adding one that competes.

**Pre-mortem on candidate 1.** The widened item asks for "the observation that
established it." An author who names the keyword probe as that observation
satisfies the wording and repeats the F1 failure exactly. The clause "a grep
over source text observes text" exists to close that reading, and the trial
tests whether it does. Falsifiable Criterion 6 records the F1 result separately
for this reason.

## Falsifiable Criteria

1. Before any arm runs, each fixture holds its target tree and `git log
   --oneline` returns exactly one commit.
2. Neither fixture contains the commit that corrected its spec, checked with
   `git log --all` rather than by reading the working tree.
3. The two arms differ in exactly one file and one item; a recursive diff of
   the plugin copies reports one differing file.
4. No dispatch prompt contains the words "assumption", "premise", "behavior",
   or "unverified".
5. The recorded detection criteria and decision rule carry a commit timestamp
   earlier than the first arm's output file.
6. The trial report states F1 and F2 separately, gives detected or missed per
   arm per fixture, and quotes the sentence the judge scored.
7. After the trial, `plugin/skills/brainstorming/SKILL.md` holds exactly seven
   Spec Self-Review items, and item 6 matches the arm the decision rule
   selects, character for character.
8. A grep for `check-the-record-before-adding-or-retiring-a-rule` across
   `plugin/skills/` returns matches only inside `brainstorming/SKILL.md`.

## Consequences

Item 6 covers two claim types and keeps one trigger. A spec that states no
count and no behavioral claim pays nothing.

The pattern promoted in `54d16fe` gains a citing check, which moves it from the
judgment-reachable group into the skill-cited group. That change makes the
5-of-5 versus 5-of-11 measurement one entry less lopsided, and a later reader
can re-measure rather than assume the effect held.

Three of the four decision-rule branches ship either nothing or a recorded
partial result. This spec can retire itself.

An author who names a text probe as the establishing observation defeats the
check. The wording names that reading and rejects it, and the trial measures
whether the rejection lands. No wording forces an author to want the truth.

## Deferred

- **The six unreferenced patterns keep no covering check.** Decision 3 states
  the reasoning. Revisit if a later process review attributes a repeated miss
  to one of them specifically.
- **`writing-plans` Self-Review carries no equivalent widening.** Item 10
  covers numeric expectations in plan steps and takes no behavioral-claim
  clause here. A plan inherits its premises from the spec, so the spec-time
  check runs first. Revisit if the trial shows the spec-time check reaching
  only one of the two premise shapes.
