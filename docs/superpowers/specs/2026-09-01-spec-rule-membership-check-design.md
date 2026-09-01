# Spec-Time Rule-Membership Check — Design

**Date:** 2026-09-01
**Status:** Approved
**User-Facing:** Yes

## Context

The second external trial of superfunk produced finding F15
(`docs/superpowers/process-reviews/external-trial-taskq-findings.md:139`).
Across specs 3 and 4 of that trial, nine defects traced to a plan or a spec.
None traced to an implementer misreading a brief.

The trial's Critical demonstrates the shape. Spec 4's qualification rule 1
listed `queued` among the states adoption may take. The retry engine also
writes `queued` while a job waits out its backoff. A run killed mid-backoff
therefore left a job whose last record read `queued`, and adoption
reconstructed that job with `attempt` at 0. Measured end to end: a callable
declaring `max_attempts=3` ran five times, three of them duplicating side
effects.

### What each gate produced

The trial transcript `0e1e9ab8` records the sequence:

1. **Line 3060** — the spec self-review ran. Its own summary named E-Prime,
   quote verification, and number verification. Those come from items 6 and 7.
2. **Line 3092** — the same message committed the spec as `75d66d3` and
   described the rule's intent correctly: "recover work that provably never
   started."
3. **`75d66d3` line 168** enumerates `submitted`, `queued`, and one further
   state. **Line 183** states "provably never started." Fifteen lines separate
   the two.
4. **Line 3165** — the plan self-review, minutes later, reported its findings.
   Every one traced to item 10 or item 14. That message states a count of four
   and then enumerates five, so this spec cites no count from it.

Item 2 of the Spec Self-Review already asks: "Do any sections contradict each
other?" It produced no finding on a contradiction fifteen lines wide, in a
session where the procedural items reported findings at every step.

### The distinction the evidence draws

Procedural items fire. Judgment items do not.

Items 6, 7, 10, and 14 each name a trigger, a procedure, and a place to look.
Item 2 names a question only. `docs/principles.md` calls this shape out under
Mechanisms, Not Goodwill.

A general "treat the brief as a suspect" mandate therefore cannot close F15.
Its equivalent already ships, already runs, and already missed this defect.

### Why the list shape carries the hazard

Prose states intent. A list states membership. A list gains a wrong member
silently, because a reader checks the sentence around the list and not each
member against it.

The value `queued` carries two producers: the submit path and the retry
engine. Only the first satisfies "provably never started." Naming the
producers of each member surfaces the conflict by grep rather than by
judgment.

### Scope of the contradiction

Three of the five contradicting passages lived outside the spec — `.context.md`,
`state.py`'s docstring, and the README. The trial's own report names all five.
The spec-internal pair alone (line 168 against line 183) suffices to detect the
defect, so a spec-internal check closes the Critical without a cross-document
sweep. A cross-document grep strengthens the check and does not carry it.

## Decision

### 1. Run a three-arm trial before any wording ships

No edit lands until the trial reports. The trial answers one question: does a
procedural rule-membership check detect what a general mandate misses?

**Fixture.** The taskq repository at commit `75d66d3`, the exact tree the spec
self-review approved. Rebuild it as a fresh `git init` holding that tree and no
later commits. Later commits contain the fix, and `git show <sha>:<path>`
stays readable to any agent that inspects history — the leak path
`docs/lessons-learned.md:116` records. Keep `.context.md`, the README, and
`state.py` as they stood, per
`docs/patterns/seed-trial-fixtures-with-real-docs.md`.

**Dispatch.** One prompt, identical across all three arms. The prompt states
that the agent just wrote the spec and asks it to run the Spec Self-Review. The
prompt never mentions a defect, never names an item, and never uses the word
`queued`.

**Arms.** Each arm changes item 2 of `plugin/skills/brainstorming/SKILL.md`
and changes nothing else:

| Arm | Item 2 carries |
|---|---|
| 1 · Control | the wording that ships today |
| 2 · Mandate | plus "name anything in this document that reads as wrong, unverified, or self-defeating" |
| 3 · Procedure | plus the rule-membership procedure in Decision 2 |

Arm 1 reproduces a known result. Run it anyway. The original session carried a
full sub-project's context, and the baseline needs the same conditions as the
other two arms.

**Detection criterion, recorded before the first run.** An arm detects when its
output states that rule 1 admits `queued` and that the same document requires
work that provably never started — or, equivalently, that the retry engine
writes `queued` as a second producer. No weaker output counts as a detection.

**Judge.** One fresh agent receives the three outputs unlabeled and shuffled,
plus the criterion above, and returns one yes/no per output. The judge never
learns which arm produced which output.

**Decision rule, recorded before the first run.** Read the branches in order
and stop at the first one that matches. The order matters: an arm-1 detection
dominates every other result, because it shows the shipped wording already does
the work.

1. Arm 1 detects → ship nothing, whatever arms 2 and 3 return. The model
   already does this, and shipping anyway repeats the failure
   `docs/lessons-learned.md:108` records.
2. Arms 2 and 3 both detect → ship the mandate wording. The procedure costs
   more and earns no slot.
3. Arm 3 detects alone → ship Decision 2.
4. Arm 2 detects alone → ship the mandate wording, and record that the
   procedure lost to a shorter instruction.
5. No arm detects → the spec-time home fails. Reopen the question at
   `writing-plans` and at the whole-branch review.

The five branches cover all eight combinations of three binary results. This
spec's own proposed check found that gap: the first draft enumerated four
branches and left "arm 2 detects, arm 3 misses" with no member.

### 2. Ship the winning wording into item 2, and nowhere else

Fold the procedure into item 2. Do not add an eighth item. The Spec
Self-Review grew from four items to seven, and
`2026-09-01-convention-retirement-design.md` exists because the framework adds
checks and retires none.

Candidate wording for arm 3, and for the shipped version if arm 3 wins:

```markdown
2. **Internal consistency:** Do any sections contradict each other? Does the
   architecture match the feature descriptions? Then check rule membership:
   does any rule, criterion, or definition enumerate members — a list of
   states, conditions, cases, or allowed values it admits or refuses? For each
   such list:
   - Quote the rule's stated intent from this document's own words.
   - For each member, name every producer of that value. Grep this spec, the
     relevant `.context.md`, and the module's docstrings for the member's
     name, and read each hit.
   - A member with more than one producer carries the hazard. Confirm that
     every producer satisfies the stated intent.

   Prose states intent; a list states membership, and a list gains a wrong
   member silently.
```

### 3. Add no restatement elsewhere until the trial reports

`writing-plans`' Self-Review and `subagent-driven-development`'s
`task-reviewer-prompt.md` both stay unchanged. A task reviewer reads one task's
brief, and the Critical needed passages the brief never carried, so that file
cannot host the primary check. Self-Review item 6 exists to police restatements
across files; writing a rule into three files before the first one proves out
creates the drift that item polices.

## Alternatives Considered

**Candidates.**

1. **Spec-time procedural rule-membership check** — the recommendation.
2. **Adversarial reviewer subagent**, modeled on the `lecun-adversarial` skill:
   a fresh agent attacks the spec and plan through several named attacks.
3. **General "brief as suspect" mandate** in `task-reviewer-prompt.md`, as
   F15's own suggested fix states it.
4. **Ship nothing** — treat F15 as covered by the whole-branch review, which
   caught the Critical.

**Recommendation:** candidate 1, gated by the trial in Decision 1.
**Confidence:** high, on the diagnosis. Medium, on the wording.

**Evidence behind it.** Transcript `0e1e9ab8` line 3060 shows the spec
self-review ran on spec 4. Line 3092 shows it approved `75d66d3`, which holds
both halves of the contradiction fifteen lines apart. Line 3165 shows the same
agent, minutes later, reporting findings through items 10 and 14. That
contrast separates procedural items from judgment items within one session.

**Steelman of candidate 2, the strongest rejected alternative.** A fresh agent
does not inherit the author's blind spot, and a spec-time check depends on an
author who already missed the defect once. Against it: four independent task
reviewers, all fresh, all missed this Critical, because their mandate compared
a diff against a brief. Actor did not decide the outcome; mandate did. A
reviewer with the wrong mandate misses regardless of who runs it.

**Pre-mortem on candidate 1.** The check fails when a spec states a rule's
intent far from the list, or states it only in the conversation and never in
the file. The procedure then finds a list, finds producers, and finds no intent
to test them against. Falsifiable Criterion 6 records this limit rather than
claiming coverage the trial did not show.

## Falsifiable Criteria

1. A fresh git repository holds the `75d66d3` tree, and `git log --oneline`
   inside it returns exactly one commit.
2. `git log --all` inside the fixture returns no commit whose message or diff
   names the adoption fix.
3. The three arm prompts match byte for byte, apart from nothing at all — the
   arms differ only in the plugin directory each one loads.
4. Neither the dispatch prompt nor any arm's item 2 contains the string
   `queued`.
5. The recorded detection criterion and decision rule carry a commit timestamp
   earlier than the first arm's output file.
6. The trial report states, for each arm, detected or missed, and quotes the
   sentence the judge scored.
7. `plugin/skills/brainstorming/SKILL.md` gains no edit before criterion 6
   completes.
8. After the trial, `plugin/skills/brainstorming/SKILL.md` holds exactly seven
   Spec Self-Review items, and item 2 matches the arm the decision rule
   selects.
9. A grep for `rule membership` across `plugin/skills/writing-plans/` and
   `plugin/skills/subagent-driven-development/` returns zero matches.

## Consequences

The Spec Self-Review gains a procedure and no new item. A spec that enumerates
states, conditions, or allowed values costs one grep per list member.

Specs that enumerate nothing pay nothing. The check reads its trigger from the
document's own shape rather than from the author's judgment about risk.

The trial may retire this design before it ships. Three of the four decision-rule
branches ship either the mandate wording or nothing at all. That outcome
matches `docs/lessons-learned.md:108`, which records two requirements that
shipped and then withdrew because nobody measured the baseline first.

The check reaches only contradictions a reader can find inside one document.
The taskq Critical qualifies. A contradiction that lives entirely across files
still waits for the whole-branch review.

`lecun-adversarial` contributed the stance that a reviewer treats the brief as
a suspect. This design adopts the stance and rejects the mechanism, because the
evidence shows neither breadth of attack nor independence of actor decided the
outcome.

## Deferred

- **Promote two lessons into one pattern.**
  `docs/lessons-learned.md:108` and `:124` each close with "single occurrence"
  and each defer promotion pending a recurrence. Both describe one failure:
  evidence gathered from an artifact's text, and a claim made about that
  artifact's behavior. Entry 108 grepped 24 skill files and concluded the model
  produces no such behavior. Entry 124 read check titles and first sentences
  and concluded those checks overlap. The recurrence condition each entry names
  already holds. This needs its own decision, not a third deferral, per
  `docs/patterns/escalate-deferred-items-on-second-recurrence.md`.
- **A pre-build falsification arm for behavioral premises.** When a spec's
  justification rests on a claim about current behavior, the plan's first task
  could run the pre-change arm and falsify the claim before any edit lands.
  This addresses the failure class the item above names. Out of scope here.
- **Cross-document membership sweep.** The procedure greps `.context.md` and
  docstrings. It does not sweep every file a project holds. Widen it only if a
  later trial finds a Critical the spec-internal pair cannot reach.
