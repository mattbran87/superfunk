# External trial 2 — `taskq` — findings

**Plugin under test:** `superfunk` v6.2.0, loaded via `--plugin-dir`, with every
marketplace/user *plugin* disabled through `--settings` (verified: the child
session exposed exactly 19 `superfunk:` skills and zero `superpowers:` ids).

**Test project:** `C:\sf-taskq-trial` — `taskq`, a Python in-memory task queue
with an append-only JSONL state file, a worker pool, a retry engine, a
read-only CLI, and crash recovery.

**Method:** 44 driven turns against a single child session, run headless from a
bash harness. I played the human partner throughout. Every turn was captured
from the session `.jsonl` rather than from `claude -p` output — see
*Methodology* below.

**Date:** 2026-08-31 / 2026-09-01.

**Predecessor:** `external-trial-bookmark-cli-findings.md`. That trial found and
closed D1–D10. This trial's remit was to find *new* mistakes and to exercise the
paths that trial's own report listed as never reached.

---

## 1. Executive summary

Fifteen findings (F1–F15) and fifteen verified positives (P1–P15).

**The headline finding is F15**, and it did not exist as a hypothesis before the
trial: **every adversarial pass in `subagent-driven-development` sits downstream
of the brief, and the brief is where the defects have been.** Across specs 3 and
4, nine defects traced to a plan or spec and **zero** traced to an implementer
misreading one. The two most severe defects in the whole trial — both capable of
destroying data — were invisible to four independent task reviews and a plan
self-review, and were caught only by the whole-branch review. The mechanism is
structural, not a lapse: a task reviewer reads the brief to learn what correct
looks like, then checks the diff against it, so when the brief *is* the defect
the reviewer calibrates against the bug and correctly reports a match.

**The second finding of note is F4**, which the first trial predicted but could
not test: `executing-plans` is a bare execution loop. A spec executed inline
gets no code review and none of SDD's Finish bookkeeping, so it is invisible to
the process-review mechanism entirely. `writing-plans` offers it as a peer menu
choice without saying so.

**A structural pattern connects F4, F5, F6, F8 and F11:** reachability in this
framework is a function of *being named in another skill's control flow*, not of
a matching `description:` field. Four skills — `requesting-code-review`,
`receiving-code-review`, `systematic-debugging` and `dispatching-parallel-agents`
— each failed to fire at the exact moment their own description matched.

**On the D1–D10 fixes and the December-2026 rebrand: no regressions.** The D4
worktree-ignore, D5 checkpoint-priority and D7 conditional per-section gate
fixes all held against a second, different codebase, and I probed the last two
deliberately (P1, P9). The newly-shipped mutation check (Tier-2 R2) was the
single most valuable addition — it caught spec 1's headline invariant test
passing with **zero jobs executed** (P6).

---

## 2. What was built

`taskq`, 143 commits, **189 tests passing**, ruff clean.

- **`src/taskq/`** — `job.py`, `errors.py`, `_locking.py`, `state.py`,
  `ready.py`, `retry.py`, `clock.py`, `pool.py`, `queue.py`, `audit.py`,
  `adopt.py` (~2,700 lines) with ~3,500 lines of tests.
- **`src/taskq/cli/`** — `main.py`, `format.py`, `commands/{status,list,show,audit}.py`.
- Docs: 4 specs, 4 plans + 3 outcome ledgers, `docs/architecture/`
  (`project-definition.md`, `concept-index.md`), `docs/lessons-learned.md`,
  4 promoted patterns, 16 tracked bugs, `CLAUDE.md` +
  `docs/ai-code-guidelines.md`.

Design substance mattered here, because several findings only surface on work
with real invariants: an append-only JSONL log, a conservation invariant (every
`submitted` id gets exactly one terminal record), OS advisory file locking with
per-run tokens, an injectable clock, two-phase drain-with-deadline `close()`,
and — in spec 4 — adoption of a dead run's queued work.

**Four full pipeline cycles shipped**, all merged to `master`:

| # | Spec | Executed via | Finished via |
|---|---|---|---|
| 1 | `taskq-foundation-design` | subagent-driven-development | option 1 (merge) |
| 2 | `taskq-pool-and-retry-design` | **executing-plans (inline)** | **option 2 (PR)**, then merged |
| 3 | `taskq-cli-design` | subagent-driven-development | option 1 (merge) |
| 4 | `taskq-adoptable-records-design` | subagent-driven-development | option 1 (merge) |

Plus one **abandoned** throwaway spike (`spike-watch`) and **one process
review** at the 3-spec threshold.

---

## 3. Coverage against the targeted gaps

| Target | Reached? | Note |
|---|---|---|
| `executing-plans` | **Yes** | Spec 2, chosen for a realistic reason (a rate limit mid-SDD run). Produced F4, the second-biggest finding. |
| `project-definition` | **Yes** | Turns 21–23, lightweight arc42 tier. Clean pass (P8). |
| `concept-index` | **Yes** | Turn 29 — but only because I asked by name. That *is* F9. |
| `dispatching-parallel-agents` | **No** | Never invoked, including on a turn posing its exact decision question (F8) and a turn where the parallelism question was explicitly delegated (P13). The *answers* were correct both times. |
| `systematic-debugging` | **Yes, twice** | Once by failing to fire on the textbook case (F6), once by performing excellently after I named the need (P7). |
| `finishing-a-development-branch` PR path | **Yes** | Spec 2, against a bare local `origin` (F7). |
| `finishing-a-development-branch` abandon path | **Yes** | Turns 33–34. Passed cleanly and better than its text requires (P10). |
| CLAUDE.md scaffold offer | **Yes** | Accepted with real answers — and it produced F1. |
| Second process-review cycle | **No** | See below. |
| Hostile-input pass (item 13) | **Yes** | Ran substantively (P2). |
| Stale-workaround grep (item 14) | **Yes** | Correctly no-op'd once (P2), made a real catch once (P14). |
| Mutation check (Tier-2 R2) | **Yes** | Best-performing new item in the trial (P6). |
| Equality-not-containment note | **Partly** | See F14 — the *class* recurred twice despite the note. |
| D5 checkpoint priority / D7 conditional gate | **Yes, probed** | Both held (P1, P9). I tried to break them and did not. |

### The one gap I did not close, and why

**`process-review`'s second-review path was not reached.** The tracker resets to
`(none)` after a review; reaching a second review needs three *more* shipped
specs, i.e. seven total. At the end of the trial the tracker reads one
(spec 4). Reaching seven was not achievable in this session — cycle 4 alone took
ten turns and hit two account rate limits — and the user capped the trial at four
specs.

So **C-D remains an untested hypothesis**, and I state it as such: reading the
skill, `process-review` has no step that opens the prior `review-after-*.md` and
checks off Recommendations that later specs closed. Only `brainstorming` surfaces
open Recommendations, and it surfaces them for *deferral*, not for closure —
observed live at turn 35, where it correctly reported nine open `- [ ]`
Recommendations and offered to defer them as a batch. On that evidence
Recommendations accumulate and are never mechanically retired, but **this is
inference from the skill text plus one turn, not an observed second review.**
It is the first thing a third trial should do, and it can be reached cheaply by
seeding a project with a prior review file rather than by shipping seven specs.

---

## 4. Findings

Ordered by importance, not by discovery order. Each is stated so it can be acted
on without re-running the trial.

### F15 — Every adversarial pass sits downstream of the brief; the brief is where the defects are

**Severity: high. Genuine, structural, and cheap to fix.**

Across specs 3 and 4, **nine** findings traced to a plan or spec rather than to
an implementation, and **none** traced to an implementer misreading a brief.
Every implementer transcribed faithfully and every reviewer said so explicitly.

| Defect | Origin | Caught by |
|---|---|---|
| Substring import guard missed `from taskq import cli` | plan's test code | task review |
| "Stays under the 681-line ratchet" | plan's constraints | implementer, at runtime |
| README guard asserted `"JSON"`, already present in the section | plan's test code | task review |
| `adopted` test never asserted the record's type | plan's test code | implementer |
| AST walk ignored `node.level` (relative imports) | plan's test code | task review |
| Criterion 14's guard could not fail | plan + spec wording | **whole-branch review** |
| Adoption call outside the lock-release guard | plan's instruction | **whole-branch review** |
| **`queued` listed as an adoptable state** | **spec's qualification rule 1** | **whole-branch review** |
| `project-definition.md` stale in three places | plan's file list | post-merge |

**The Critical, in detail** — because it is the clearest demonstration.
Spec 4's qualification rule 1 listed `queued` among the states adoption may
take. But `queued` is also what the **retry engine** writes while a job waits out
its backoff. A run killed mid-backoff therefore leaves a job whose last record is
`queued`; adoption takes it and reconstructs the `Job` with `attempt` at its
dataclass default of `0`. Measured end to end:

```
side effects after adoption: 3
[('submitted',None), ('running',1), ('queued',2), ('running',2), ('queued',3),
 ('adopted',0),      ('running',1), ('queued',2), ('running',2), ('queued',3),
 ('running',3),      ('terminal',3)]
```

Five executions of a callable declared `max_attempts=3`, three of them
duplicating side effects the state file cannot rule out — the exact hazard the
spec cites when refusing `running` jobs. And every crash-and-adopt cycle grants
another full budget, so *"a job must not retry forever"* stops being bounded by
the file at all.

**Why the gates missed it.** Rule 1 contradicted **five** other passages in the
same two documents: the spec's own "provably never started", its own Open
Question 3, `.context.md`, `state.py`'s docstring, and the README. The
specification was internally inconsistent *before any code existed*. Four
independent task reviews and a plan self-review all read rule 1, saw `queued`
listed, saw `queued` accepted, and agreed. That is the correct output of their
method: `task-reviewer-prompt.md` checks the diff against the brief, which is
structurally incapable of finding a brief that is wrong.

The plan's Self-Review has the mirror-image blind spot: it verifies what is
*checkable* — counts, filenames, command output, and it caught three wrong ones
in a single pass here — and never asks whether a *rule* is right, because a rule
has nothing to run.

**Of five adversarial passes, four inherit the brief as ground truth.** Only the
whole-branch review is positioned to ask whether the specification itself is
wrong, and **both defects capable of destroying data waited for it.**

**Suggested fix (not implemented — trial scope forbade it).** The task reviewer
already reads the brief. Give it an explicit mandate to treat the brief as a
suspect, not only as the standard — e.g. *"Name anything in this brief that is
wrong, unverified, or self-defeating, independently of whether the
implementation matches it."* The project under test independently derived a
sharper version and promoted it to
`docs/patterns/review-the-brief-against-its-own-intent.md`: treat **enumerated
lists** as the dangerous shape, because prose states intent and lists state
membership, and *a list gains a wrong member silently.* One question would have
caught the Critical: *rule 1 admits `queued`; the same document says "provably
never started"; what does a `queued` record mean?*

**This does not mean the independent reviewers are wasted** — P6 and the fix
waves show them catching real implementation defects. It means the **ratio is
off**: several adversarial passes on the code, zero on the document the code is
derived from.

### F4 — `executing-plans` is a bare execution loop: no review, and none of SDD's Finish bookkeeping

**Severity: high. Genuine defect. The path the first trial never took.**

`executing-plans/SKILL.md` is 65 lines: load plan → execute tasks → *"After all
tasks complete and verified: use superfunk:finishing-a-development-branch."*
There is no review step and no Finish step. `writing-plans`' Execution Handoff
presents the two options as peers — "Subagent-Driven (recommended)" vs "Inline
Execution … batch execution with checkpoints" — and nothing in that menu says the
second drops the entire verification and bookkeeping layer.

Measured on the branch at the end of spec 2 (8 tasks, 11 commits, 106 tests, all
inline), against what spec 1 produced under SDD:

| Finish artifact | SDD (spec 1) | executing-plans (spec 2) |
|---|---|---|
| Independent task reviews | 7, each mutation-checked | **none** |
| Whole-branch review | yes — found the cycle's Critical | **none** |
| Spec `Status` → `Shipped` | yes | **no — still `Approved`** |
| `process-reviews/tracker.md` append | yes | **no** |
| `process-reviews/notes.md` entries | 25+ | **zero** |
| `plans/<plan>-outcomes.md` | yes | **not created** |
| `docs/lessons-learned.md` | 2 entries + 1 promoted pattern | **unchanged** |
| `docs/bugs/` for deferred findings | 6 | **zero, despite 4 real defects found** |
| workspace ledger (`progress.md`) | yes | **none — no resume story** |
| concept-index maintenance check | yes | **none** |

The four defects the inline run found — an `on_event` re-entrant deadlock, a
`close()`-vs-pool deadlock, a `KeyboardInterrupt` hanging `close()` forever, and
a plan defect where one `_closed` flag served two purposes — were all found by
its own tests going red, and **none were recorded anywhere.** Under SDD each
would have become a `Catch` line that `process-review` later consumes. Inline
execution is therefore not merely less-reviewed: it is **invisible to the
process-review mechanism.** Ship three specs inline and `brainstorming`'s
review-due check still reads "none".

The model named the *review* half of the gap unprompted and accurately. It did
not notice the bookkeeping half. Even after I asked for a whole-branch review
(turn 16) and it found a Critical plus five Importants, `notes.md` gained
**zero** entries for spec 2.

**Why this is a defect rather than "inline is the cheap option":**
`executing-plans`' own note says to prefer SDD *when subagents are available* —
i.e. it is positioned as a degraded fallback for platforms without them — yet
`writing-plans` offers it as a normal menu choice on a platform that has them. I
chose it for a realistic reason (a rate limit) and silently opted out of the spec
lifecycle.

**Fix shape:** either (a) give `executing-plans` its own Finish section reusing
SDD's — Status flip, tracker append, outcomes ledger, lessons capture,
bug-tracking, concept-index check — plus a `requesting-code-review` step before
it; or (b) if the omission is deliberate, say so in `writing-plans`' Execution
Handoff so the user chooses knowingly.

### F9 — `concept-index` cannot bootstrap on a downstream project, and two of its three unit types don't exist there

**Severity: medium-high. Three separate defects, all confirmed live.**

1. **No automatic first build.** Step 1 says a full build "is the only case a
   human invokes this skill directly for". SDD's Finish says *"If the index file
   doesn't exist yet … skip this step — do not run a full rebuild here."* Each
   is reasonable alone; together the index **cannot come into existence** unless
   a human already knows the skill exists and asks by name. Across three full
   cycles it never appeared and was never mentioned. The child session, when I
   finally asked: *"it was never going to bootstrap itself, I hit that skip at
   Finish, and I didn't mention the skill existed."*
2. **Two of three unit types are superfunk's own repo shape.** "Skill" is
   `plugin/skills/<name>/`; "Feature" is `specs/<module>/<feature>/`. On `taskq`
   both are zero, measured. Only the Directory rule applies, yielding ~7 coarse
   rows — thinner than the module-level answer a user asking "where does X live"
   wants. This is the D2/D3 distribution-boundary problem in a new place.
3. **A format mismatch between the framework's own writer and its own reader.**
   `concept-index` derives a Directory row's Description from the directory's
   `.context.md` **`**Purpose:**` line.** Both `.context.md` files this
   project's own SDD cycles generated write **`## Purpose` as a heading.** So
   every `.context.md` the framework produces is unreadable by the framework's
   own index skill, which then falls back to "ask the user for a one-line
   description" — turning an automated build into an interrogation. Nothing in
   the plugin specifies the `.context.md` template, which is why the two halves
   disagree.

### F6 — `systematic-debugging` did not fire on the textbook case, and the Iron Law broke in the exact shape the skill describes

**Severity: medium-high. Genuine, and the cost was measured.**

An intermittent failure appeared in `test_conservation_under_the_pool_with_retries`
— the test proving the user's headline invariant. The skill's description is
*"Use when encountering any bug, test failure, or unexpected behavior, **before
proposing fixes**"*; its Iron Law is *"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION
FIRST."* The only `Skill` call that turn was `finishing-a-development-branch`.

Sequence: (1) a hypothesis stated as a conclusion with **no assertion text and
no traceback captured**; (2) a code fix applied on that hypothesis; (3) *"My fix
made it worse — 6/12 versus roughly 1/11 before. **I was guessing at the cause
instead of diagnosing it.**"*; (4) revert, then finally capture the real
assertion; (5) filed as a bug "explicitly not diagnosed".

Phase 1 of the skill would have prevented every step. The model reached the
skill's own conclusion by paying for it: one harmful fix, a 6× worse failure
rate, and a bug filed undiagnosed. Once invoked (after I named the failure and
refused another guess) it performed excellently — see P7.

**Why it is a framework finding.** Nothing in `executing-plans`,
`finishing-a-development-branch`, or the `writing-plans` handoff routes a
mid-execution test failure to `systematic-debugging`. Step 1 of
`finishing-a-development-branch` — *"If tests fail, report the failures and
stop"* — has no pointer to it either. On the SDD path an implementer or reviewer
subagent hitting a failure is similarly unrouted. The skill is reachable only by
the controller spontaneously remembering it, at the exact moment ("I can see the
cause") when it feels least necessary.

### F5 — `requesting-code-review` and `receiving-code-review` were never invoked, including when the user asked for a code review in so many words

**Severity: medium.**

Turn 16's prompt was *"do the cheap version: one whole-branch review at the end
… Run the review, deal with whatever it finds."* That turn contains **zero
`Skill` calls.** The review was a hand-rolled `Agent` dispatch; the findings were
acted on with no `receiving-code-review` invocation.
`requesting-code-review`'s own description names three conditions all true
simultaneously — completing tasks, implementing a major feature, before merging.

The output was excellent regardless, so the harm is not this run's quality. The
harm is that whatever those skills contain — checklists, escalation rules, the
"verify before agreeing" discipline — was not applied and cannot be relied on.
**Note the contrast:** on the SDD path the review prompts are *files SDD hands to
the reviewer*, so they run whether or not the skill is invoked. Off that path
nothing pulls them in.

### F13 — `writing-plans` Self-Review item 10 checks the numbers it enumerates, not the numbers it asserts

**Severity: medium. Genuine and narrow — a scope widening, not a rewrite.**

Item 10 fired well on spec 4's plan: it corrected three wrong claims about
existing test files (a count of 9 vs 8, two non-existent imports) and stated
per-task test deltas.

In the **same document**, Global Constraints asserted that this work "adds one
small method and one constructor argument" and would stay under spec 3's
`queue.py` line ratchet of 681. Nobody ran that number. Task 1 blew it
immediately (681 → 688), and the arithmetic afterwards was `688 + 39 = 727` for
Task 4 — **a figure derivable from the plan's own line counts before any code
was written.**

Item 10's scope in practice is *counts of things the plan enumerates*, not
*budgets the plan promises to stay inside*. A predicted line count, runtime,
binary size and test count are the same class of claim; only one gets checked.

Two aggravations: the blown budget made the codebase self-contradictory (the
implementer raised the ratchet to 688, so the test's own failure message cited a
`project-definition.md` that still said 681); and the ratchet was blown **by a
comment the plan itself dictated** — 5 of 7 added lines were prose, 2 were
executable — which is verbatim the failure the user had predicted one turn
earlier when rejecting a line-count criterion.

### F14 — Two guards in a row passed while failing to discriminate, and nothing names the class

**Severity: medium.**

- Spec 3: a `--help` output-width guard that did not fire at the width CI runs.
- Spec 4 Task 1: a README guard asserting `"JSON" in section`, chosen
  *deliberately* as a "distinctive noun" to avoid pinning wording — but
  `README.md:94` already contains "JSON-serializable" in that same section, so
  **deleting the bullet the guard exists to protect leaves it green.**

The shared failure mode is nameable: *asserting on a token the surrounding text
already supplies.* The mutation check found the second one, so the machinery
works — but it works per-task, from scratch, on whoever happens to be reviewing.
Nothing in `writing-plans`' Self-Review or `task-reviewer-prompt.md` names this
class, so each occurrence costs a fresh discovery. Two in four specs in one small
project suggests it is common enough to name — e.g. *"for every assertion that a
document contains a token, delete the thing it protects and confirm the
assertion fails."* (The project under test independently promoted this to
`docs/patterns/assert-on-a-token-the-context-cannot-supply.md`.)

Note this is adjacent to, but not the same as, the existing equality-not-
containment (`in` vs `==`) note: the note is about the *operator*, this is about
the *operand*.

### F12 — `brainstorming` has no convergence budget: four turns, four new questions, zero documents

**Severity: medium. Genuine friction with a cheap fix.**

Spec 4 was pitched as "one command", with the user saying in the same message
*"I don't want a forty-minute design conversation about a `retry` verb — keep it
proportionate to the size of the thing."* Turns 35, 36, 37 and 38 each ended with
a fresh decision request and **no design document on disk**. The user said "Go
ahead and write the spec" and, a turn later, "Go." Neither produced a spec.

**The nuance cuts both ways.** Every individual stop was justified — one of them
(F-list P12) found the agreed design unbuildable and saved a week. But the skill
has no notion of how much design a piece of work is worth, and no mechanism that
converts *"the user has answered everything I asked"* or an explicit *"write it
now"* into an artifact. The one-question-at-a-time discipline is a good property
and it is **unbounded**: each answered question licenses the next.

The failure mode is not bad design — the design was good. It is that a user who
granted "keep it proportionate" and twice said "go" spent **four turns making
decisions about an artifact that did not exist**, so none of those decisions were
reviewable as a whole, and a session limit or compaction at any point would have
lost all of it.

**Probe result, which is the actionable part.** On turn 39 I named the *pattern*
in character. The spec was written that same turn — 341 lines, 16 falsifiable
criteria, **three Open Questions recorded in the document rather than asked**,
and three decisions explicitly made rather than escalated. The behaviour is fully
available; nothing in the skill reaches for it, and converging four turns earlier
would have cost nothing. Two plain "go"s did not trigger it; only a user who
diagnosed the loop could open the escape hatch.

**Fix shape:** a convergence check — after N rounds, or on an explicit
instruction to proceed, the default flips to "write the document with remaining
questions recorded in it" rather than "ask again".

### F1 — `brainstorming`'s scaffold offer: made late, then executed with zero of its three questions asked

**Severity: medium-low. Well mitigated in practice.**

The offer was not made as its own ask during "Understanding the idea". It
appeared as a parenthetical at the end of the context report — *"(Happy to
scaffold a starter `CLAUDE.md` + conventions doc from a couple of questions once
we've settled the design — say the word, otherwise I'll skip it.)"* — deferred
past where the skill places it, and easy to miss. I had to pull it forward.

On acceptance the skill says to ask up to three questions, one at a time.
**Zero were asked.** Both files were written and committed in one shot, with the
after-the-fact report: *"I skipped the usual 'what conventions do you already
follow' question — the repo was empty… That means I picked defaults you should
veto if they're wrong: ruff, hatchling, src layout, 88-char lines, type hints on
everything public."*

Only question 1 carries a skip condition in the skill text. Question 3 —
build/test commands and architecture notes — is precisely the one an empty repo
*cannot* answer by observation, so an empty repo argues for asking it. The result
is five tooling decisions committed into a file every implementer and reviewer
subagent is later told to obey, which the user never made. The disclosure with an
explicit veto invitation is good mitigation and is why this is a rough edge
rather than a serious defect.

**Fix shape:** give questions 2 and 3 their own skip conditions, or state that an
empty repo makes question 3 mandatory.

### F3 — `finishing-a-development-branch` Step 7 misclassifies the worktree its own sibling skill created

**Severity: medium-low. Two distinct defects; recurred in cycle 4.**

Step 7 branches on the worktree path: *"If `WORKTREE_PATH` is under
`.worktrees/` or `worktrees/`: Superpowers created this worktree — we own
cleanup"* → `git worktree remove`. *"Otherwise: the host environment owns this
workspace."* But `using-git-worktrees` prefers the harness's native
`EnterWorktree`, which puts worktrees at **`.claude/worktrees/<name>`**. The model
read that as not matching and took the *Otherwise* branch, saying so explicitly.

What followed: `ExitWorktree {action:"remove"}` refused with a data-loss warning
(*"Worktree has 39 commits… Confirm with the user, then re-invoke with
`discard_changes: true`"* — the native tool counts commits, not merge status, so
a fully-merged branch trips it); the model verified `git branch --merged master`
first, then re-invoked with a flag whose name asserts the opposite of what was
happening; that still left the directory, so it fell back to
`git worktree remove --force` anyway — executing the branch Step 7 told it not to
take.

**(a)** The path test does not recognise the path superfunk's own preferred
mechanism produces, so the "we own cleanup" branch is effectively dead code on
Claude Code. **(b)** Routing to `ExitWorktree` forces `discard_changes: true` on
merged work — exactly the input a cautious operator should refuse. The model
navigated both correctly *only because* it independently checked
`git branch --merged`; the skill does not tell it to.

**Recurrence:** in both SDD cycles a leftover directory remained
(`.claude/worktrees/taskq-foundation`, then `.claude/worktrees/spec4-adopt`),
undeletable with `Device or resource busy` from a handle the session itself
holds. Reported honestly both times rather than forced. Windows-specific, but
the framework has no guidance for it.

### F2 — SDD's Finish ran its second half and skipped its first half (cycle 1 only)

**Severity: medium in cycle 1. Did not recur — see the addendum for the durable
part.**

Finish's order is: (1) flip the spec's `Status` to `Shipped`; (2) append to
`process-reviews/tracker.md` and offer `process-review` at 3; (3) check off
Recommendations; (4) **verify** those three landed with `grep -c` — *"A 0 means
that action never happened — do it now, before starting the Lessons-learned
capture below"*; (5) lessons + patterns; (6) concept-index; (7) bug-tracking;
(8) delete workspace; (9) hand off.

In cycle 1, steps 5, 7 and 8 ran; steps 1, 2 and 4 did not. The spec still read
`Status: Approved` and `tracker.md` **did not exist**. The self-check in step 4,
which exists precisely to catch this, never ran. The model's stated reasoning:
*"Spec Status is now Approved, not Shipped — that flips on merge, which is yours
to call."*

**The ambiguity is in Finish's own justification sentence:** *"the only point in
this process where the work is both reviewed and **merged**, so it is the right
moment to record it."* In SDD's vocabulary "merged" means the fix wave's commits
are on the branch; a reader can equally read it as "merged to the base branch",
which has not happened yet. Under that second reading the step *cannot* run at
Finish — so the model deferred it, and deferred the verification block with it.

**Consequence:** the tracker is what `process-review` counts and what
`brainstorming`'s review-due check reads. With no tracker file, the counter never
starts.

**F2 did not recur in cycle 4** — verified by commit order: the Status flip and
tracker append landed on the branch *before* the merge commit, exactly where
Finish places them. So the cycle-1 behaviour was one reading of an ambiguity, not
a deterministic defect. **The sentence is unchanged, though**, and the addendum
below is the durable part.

#### F2 addendum — the deferred bookkeeping got attached to one branch of the integration menu

At the `finishing-a-development-branch` menu the model wrote, verbatim:

> *"If you pick **1**, I'll also flip the spec's `Status` from `Approved` to
> `Shipped` and start `docs/superpowers/process-reviews/tracker.md` on the branch
> before merging."*

I picked 1 and it did exactly that. But the recovery was conditional on the
*merge* option. Options 2 (PR) and 3 (keep as-is) carried no such promise, and
`finishing-a-development-branch` says nothing about spec Status or the tracker on
any path. **F7 confirmed this live:** after a completed option-2 finish, spec 2
still read `Status: Approved`, the tracker still listed only spec 1, and no
outcomes file existed. A branch finished via PR ships without its bookkeeping —
which is the case a real team hits most often.

### F8 — `dispatching-parallel-agents` was never invoked, including when the user posed its exact decision question

**Severity: low, but it completes the pattern.**

Turn 27's prompt was in substance the skill's own decision tree: three tasks in
separate files consuming one shared input — *"Do they actually have to be
sequential? … If there's a real dependency I'm not seeing … say so and keep them
in order."* Skills invoked that turn: `subagent-driven-development` and
`using-git-worktrees`. Not `dispatching-parallel-agents`.

**The answer was correct** — it found all three tasks modify `format.py`,
`main.py`, `README.md` and `CHANGELOG.md`, which is exactly the skill's
"shared state — agents would interfere" branch. And at turn 40, handed the
parallelism question again and asked to "pick deliberately rather than default",
it *rejected the user's premise* with a correct structural argument (see P13) —
still without invoking the skill.

So the reasoning is present even when the skill is not, and this is the mildest
of the not-invoked findings. But it completes the pattern:
`dispatching-parallel-agents`, `requesting-code-review`, `receiving-code-review`
and `systematic-debugging` were each not invoked at the moment they applied, and
`systematic-debugging`, `project-definition` and `concept-index` ran only because
the user named the need. The skills that *did* fire reliably are exactly the ones
another skill hands off to by name: `brainstorming` → `writing-plans` →
SDD/`executing-plans` → `finishing-a-development-branch`, plus
`using-git-worktrees` which SDD requires.

**Reachability in this framework is a function of being named in another skill's
control flow, not of a matching `description:` field.** That is the single most
generalisable structural observation of the trial, and it is worth deciding
deliberately whether that is the intended design.

### F11 — The abandon path was reproduced from memory, not re-invoked

**Severity: low. Same class as F8; the outcome was correct.**

`grep "TOOL Skill"` across turns 33 and 34 returns nothing:
`finishing-a-development-branch` was not invoked for the abandon path. The
behaviour (menu semantics, the `discard` token, the manifest shape) came from the
model recalling the skill it had loaded earlier in the same session.

Weaker than F4/F5/F6/F8 — the skill genuinely *was* in context and the outcome was
right (see P10). But the discard path's specific steps, notably Step 7's cleanup
test, were never re-read, so this trial cannot distinguish "followed Step 7" from
"there was no worktree, so it did not matter" — which is in fact what happened.
In a fresh session, or one where the earlier Finish had been compacted away,
nothing in the framework would have pointed at the skill when the user said
"throw the work away".

### F7 — `finishing-a-development-branch`'s PR path degrades well but has no "no forge" branch

**Severity: low. One sentence of guidance would close it.**

Option 2, against a bare local `origin`. The skill says to *"create the pull
request with the forge's tooling — its CLI if one is available, or the creation
URL most forges print when you push."* Neither exists for a bare repo.

Observed behaviour was good: it stated the caveat *before* acting, did the half
that is real (`git push -u origin <branch>`, verified 17 ahead / 0 behind), then
**actually ran `gh pr create` to test rather than assuming** — getting *"none of
the git remotes configured for this repository point to a known GitHub host"* —
and reported that as evidence. It preserved the worktree per the option-2
contract and asked whether to commit the PR description as a file.

No defect in the outcome. The gap is that option 2 assumes a forge; a less careful
run could report "PR created" having only pushed.

### F10 — A skill file was read with the Read tool

**Severity: trivial, but it is a stated rule being broken.**

Turn 29 contains `Read …/plugin/skills/concept-index/SKILL.md`.
`using-superpowers` says, in bold: *"Never use the Read tool on skill files."*
Harmless here — it was answering a question *about* the skill rather than
executing it — but that instruction is what stops a model substituting a stale
read for an invocation.

---

## 5. Verified positives

These matter as much as the findings: they are the D1–D10 fixes and the new
Tier-2 items holding up against a second, different codebase, several of them
probed deliberately for failure.

- **P6 — the mutation check (Tier-2 R2) is earning its keep, hard.** Its best
  catch: *"Mutation 5: the headline invariant test passes when zero jobs execute,
  because `close()` abandons all 200 and `abandoned` satisfies the id-set
  assertion."* That is the spec's own falsifiable criterion 1 — the "no silent
  drops" proof the user demanded — being satisfied by a run in which nothing ran.
  It also caught that moving a user callable back under `Queue._lock` left the
  suite green, i.e. the deadlock just fixed had no regression test. Both were
  found because the prompt now *asks* for mutation. It held under pressure twice
  more in cycle 4: an implementer reported a non-firing mutation rather than
  manufacturing a red, and the reviewer then built two tests that did
  discriminate.
- **P15 — the whole-branch review is the load-bearing gate.** Both cross-cutting
  Criticals in this project (spec 1's and spec 4's) were invisible to every
  task-scoped review and found only by the whole-branch pass. Whatever is done
  about F15, this pass should not be made optional.
- **P1 / P9 — the D5 checkpoint-priority and D7 conditional per-section gate
  fixes held, in shapes they were not tested against.** I tried to break D7 with
  blanket consent plus a carve-out (*"present it all at once, **except** where
  something genuinely new to me comes up"*) — the response presented six sections
  with no "does this look right?" after any of them and ended with exactly two
  questions, both genuinely novel. No settled decision was re-asked, twice.
- **P4 / P12 — `writing-plans` and `brainstorming` run real disposable
  experiments rather than reasoning about the platform.** One found a genuine bug
  in the plan's own draft (a Windows mandatory byte-range lock would have made
  `audit()` fail exactly when a run held the lock) and disclosed that its *first*
  probe script was itself buggy. Another, told "go ahead and write the spec",
  opened with *"I need to check something I assumed and didn't verify"* and found
  three things that killed the agreed design — including that
  `README.md:90` and `classify_retryability`'s docstring both overclaimed that a
  later process could "reconstruct and re-run" a job. Note what it caught: a
  false capability claim shipped by **spec 1 of this same trial**, which had
  passed its own Self-Review, its subagent reviews, *and* process-review #1.
- **P11 — `brainstorming` held its ground under a plausible-but-wrong user
  argument, by experiment rather than assertion.** I pushed back with two real
  counter-cases and explicitly invited it to fold. It conceded the *argument*
  without hedging — *"my argument was weak"* — then appended a foreign
  `submitted` record to a live run's state file and let the pool run: the job
  never executed and `audit` returned `ok: False, unaccounted: [...]`. Same
  conclusion, different and correct reason. This is the shape the first trial
  wanted and did not get.
- **P10 — the abandon path behaved better than its own text requires.** It
  preserved the salvage *before* touching the branch; noticed unprompted that the
  harness it was preserving depended on the code about to be deleted and rewrote
  it to probe through `audit()` instead; produced the irreversibility manifest;
  volunteered the one thing not covered by the salvage and invited a correction;
  required the literal token `discard` and did **not** act on the plain-English
  "throw the work away" alone; then grepped for remnants afterwards.
- **P13 — the execution-mode choice was made by argument and overruled the
  user's premise.** It rejected my guess that the spec had "two independent
  halves" — *"adoption can't reconstruct anything without the args the format
  change adds; it's a strict chain"* — then chose SDD on a stronger ground (this
  is the first spec that *writes*, and it touches the conservation invariant),
  citing the project's own history as evidence and naming the cost honestly.
- **P14 — Self-Review item 14 (stale-workaround grep) made its first
  substantive catch**, and named *why* the technique works: *"limitation-era text
  never mentions the feature that removes it"*, so you grep the limitation's own
  wording. It found `README.md:398` documenting as permanent a limitation the
  spec removes. Item 13 (hostile input) also ran substantively, naming six code
  blocks with a specific unhandled input class each, split into handled vs
  explicitly accepted; and it correctly *no-op'd* once with a stated reason
  rather than fabricating a grep.
- **P7 — `systematic-debugging`, once invoked, performed extremely well.** A
  standalone repro that runs with pytest nowhere in the picture (4–5/40 before,
  0/100 after); causation proven **in both directions** by removing only the new
  term; a correction of my own premise (I had assumed randomised test order —
  `pytest-randomly` was not installed, so `-p no:randomly` had been a no-op); and
  it reported an experiment that *appeared to refute the correct hypothesis*
  (a 2 ms delay drove failures to zero because it slowed every claim enough to
  remove the race, i.e. it measured a different system) — the sort of thing most
  write-ups quietly drop.
- **P8 — `project-definition` worked cleanly on its stated use case.** It asked
  the tier question **without steering** (the skill forbids recommending a tier;
  it complied explicitly), derived the real import graph for the Building Block
  View and presented a draft for correction before writing, and correctly refused
  to settle a question that belonged to a spec.
- **P5 — the D4 worktree-ignore fix held.** A `.gitignore` containing
  `.claude/worktrees/` with a why-comment was committed on `master` **before any
  work landed**; `git status` stayed clean throughout. The exact harm D4
  documented did not recur.

---

## 6. Triage: what to fix, what to accept

**Genuine, fixable defects — worth acting on:**

| # | Finding | Rough cost |
|---|---|---|
| F15 | Every adversarial pass sits downstream of the brief | **Low** — one item in `task-reviewer-prompt.md` |
| F4 | `executing-plans` has no review and no Finish | Medium — a Finish section, or one honest sentence in the handoff menu |
| F9.3 | `.context.md` `**Purpose:**` vs `## Purpose` mismatch | **Trivial** — pick one and state the template |
| F9.1 | `concept-index` cannot bootstrap | Low — let Finish create it, or have `project-definition` offer it |
| F9.2 | Two of three unit types are superfunk's own repo shape | Medium — a distribution-boundary problem, same family as D2/D3 |
| F13 | Item 10 misses asserted budgets | **Trivial** — widen the wording to "any numeric claim, including budgets" |
| F14 | Non-discriminating guards | **Trivial** — one Self-Review item |
| F12 | `brainstorming` has no convergence budget | Low — a round cap, or honour an explicit "write it now" |
| F1 | Scaffold questions skipped | **Trivial** — per-question skip conditions |
| F3a | Step 7's path test misses `.claude/worktrees/` | **Trivial** — add the path |
| F7 | PR path has no "no forge" branch | **Trivial** — one sentence |
| F2 | Finish's "merged" is ambiguous | **Trivial** — say "on this branch" |
| F2a | Bookkeeping is absent from options 2 and 3 | Low — move it into `finishing-a-development-branch`, or state it on every path |
| F10 | A skill file was Read | None — behavioural, no fix available |

**Structural — needs a decision, not a patch:**

- **F5/F6/F8/F11 — skill reachability.** These are all one thing: skills fire
  when another skill names them, not when their `description:` matches. Patching
  them one at a time means adding a pointer to `systematic-debugging` from every
  place a test can fail, a pointer to `requesting-code-review` from every place
  work completes, and so on. That may be right, but it is a design decision about
  how the framework routes, not four small fixes. **Worth noting the one place it
  already works:** on the SDD path the review prompts are *files SDD hands to the
  subagent*, so they apply whether or not a skill is invoked. Generalising that
  mechanism — ship the content as a file the control flow passes along — is
  probably cheaper than adding cross-references everywhere.

**Inherent limitations, not defects:**

- F3b — `ExitWorktree` requiring `discard_changes: true` on merged work is a
  *harness* tool's behaviour, not the framework's. The framework can only
  document it.
- The Windows `Device or resource busy` leftover is an OS/handle artefact. The
  framework should probably say "report it, do not force it" — which is what
  happened anyway, twice.

**One-off flukes — recorded, not actionable:**

- F2's cycle-1 skip did not recur in cycle 4 under the same skill text. Treat the
  *ambiguous sentence* as the finding, not the incident.
- Five child-session rate limits are trial-environment events. The first trial hit
  them too. They cost a resume turn each and produced no findings.

---

## 7. Methodology

**The trap held, and it has a second-order form.** The first trial's report warns
that `claude -p` prints only the final assistant message per turn. That is true
and the harness captured every assistant text block from the session `.jsonl`
accordingly. Several findings — F5 and F6 in particular, which are both
statements about which `Skill` calls did *not* happen — are only visible in the
full trace.

**A new trap, worth adding to any future trial's setup notes.** On Windows,
invoking the CLI through `%APPDATA%\npm\claude.cmd` with a **multi-line** `-p`
prompt silently truncates the command line at the first newline, because the
`.cmd` wrapper forwards `%*` through `cmd.exe`. Every flag after the prompt —
`--plugin-dir`, `--settings`, `--output-format`, `--resume` — is dropped. The
symptom is that the child session loads the **marketplace**
`superpowers@claude-plugins-official` plugin (14 `superpowers:` skills) instead of
the fork's 19 `superfunk:` skills, i.e. **the trial silently tests the wrong
plugin.** Three sessions were burned this way and discarded. Fix: invoke
`.../@anthropic-ai/claude-code/bin/claude.exe` directly. Verify by asserting the
skill namespace, not by assuming the flag took.

Also: `--session-id <uuid>` is ignored (a fresh uuid is allocated) — read
`session_id` back from `--output-format json`. And the transcript **moves**
between `~/.claude/projects/C--<project>\` and `...--claude-worktrees-<name>\` as
the session changes cwd, so a transcript reader must search all of them.

**Trial-condition caveat.** The child session still sees the user's *personal*
skills in `~/.claude/skills` — only plugins can be disabled via `--settings`. One
of them, `writing-controlled-documents`, was invoked at turn 2 and shaped the
specs' prose (an "E-Prime scan" appears in every spec self-review). It is
additive rather than a competing namespace, so findings remain attributable to
superfunk — but the spec-*writing* behaviour observed here is superfunk plus that
skill, not superfunk alone.

---

## 8. Is `C:\sf-taskq-trial` worth keeping?

**Yes — keep it.** Specifically:

**It is the cheapest route to the one gap this trial missed.** A third trial can
reach `process-review`'s second-review path from this repo in a handful of turns:
the tracker already holds one spec since the last review, and there are two
specs' worth of real work queued and specified (`taskq retry`, and the
`queue.py` split that bug 015 waits on). Starting fresh would cost four cycles to
get back here.

**It is a regression corpus.** It now contains four shipped specs, one abandoned
spike, one process review, 16 tracked bugs, 4 promoted patterns, and a
`concept-index` and `project-definition` built by the framework itself. Re-running
`concept-index` against it after fixing F9.3 is a direct before/after test.

**It has live, specified, non-trivial work waiting**, which matters because
findings F13/F14/F15 all surfaced from *real* design pressure rather than from
toy tasks: bug 015 (adoption plus early `close()` destroys recoverability —
blocked on the `queue.py` split), bug 016 (`adopt_limit` bounds blast radius, not
cost), bug 006 (the POSIX `fcntl` branch has never executed — needs a Linux
machine or CI), and spec 5.

**Two caveats if it is reused.** The `.claude/worktrees/spec4-adopt` directory is
inert but undeletable until the holding process exits — clear it before the next
run. And `origin` points at `C:/sf-taskq-origin.git`, a local bare repo created
so the PR path could be exercised without publishing anything; a future trial
wanting the *real* forge behaviour of `finishing-a-development-branch` option 2
will need an actual remote.

**What a third trial should target**, in priority order: the second process-review
path (cheap from here, and the last untouched integration path); whether F15's
fix actually changes outcomes, measured by whether brief-origin defects still
reach the whole-branch review; and `concept-index` after F9.3, since a
`.context.md` template fix is testable in one turn against a repo that already
has two non-conforming files.
