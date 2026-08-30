# External trial: superfunk against a fresh Python project

**Date:** 2026-08-28 → 2026-08-30
**Plugin under test:** `C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin` @ v6.2.0
**Test project:** `C:\sf-bookmark-cli-trial` — `bm`, a bookmark-manager CLI in Python
**Method:** one continuous `claude -p --resume` conversation (session
`659f8ca6-433f-4f5e-b723-c07e3b724c9f`), driven turn-by-turn by an operator playing a
real user. 26 partner turns, ~6 hours of child-session wall clock.

The point of the trial was to find mistakes in the *framework*, not in `bm`. Bugs in `bm`
were expected and were routed through the project's own `docs/bugs/` as designed.

---

## Trial setup

Only `git init` was run before the first prompt. No CLAUDE.md, no `docs/`, no conventions,
no test runner — a genuinely zero-convention repo, starting with **zero commits** on
`master`. Everything below about bootstrap behavior is therefore real.

One deliberate intervention: the marketplace plugin `superpowers@claude-plugins-official`
was disabled in the child session via `--settings`, along with context-mode and three
others. Without this the fork's skills would have competed with a marketplace copy of the
same framework under a different prefix, and no finding could be attributed cleanly.
Verified in-session: the `Skill` tool exposed exactly the fork's 19 skills, all
`superfunk:`-prefixed, and no `superpowers:` namespace existed.

### Methodological trap — read this before trusting any future trial

`claude -p` prints **only the final assistant message of a turn.** Intermediate assistant
messages are written to the session transcript but never to stdout.

Two findings in the running log were logged against the framework and then had to be
withdrawn or downgraded once the transcript at
`~/.claude/projects/C--sf-bookmark-cli-trial/659f8ca6-….jsonl` was read directly. One
("performed a cleanup and never reported it") was **entirely** an artifact — the report
existed at transcript line 909 and `-p` simply didn't print it. Another was over-stated by
one occurrence.

Any re-run must capture every assistant text block per turn, not `-p`'s last message. The
harness used here was corrected mid-trial to do so.

---

## What got built, and how many cycles

| Cycle | Feature | Pipeline | Outcome |
|---|---|---|---|
| 1 | `bm` core — `add`/`list`/`search`/`tags`/`rm`/`open`, SQLite store, URL normalization, HTML title fetch with a wall-clock deadline | brainstorming → writing-plans → using-git-worktrees → subagent-driven-development (9 tasks) → finishing-a-development-branch | **Shipped**, merged to `master`, 132 tests |
| 2 | `bm retry` — sweep that re-fetches failed titles; per-host serial queues, concurrent across hosts, Ctrl-C-safe incremental commits | same chain, fully autonomous under blanket consent | **Shipped**, merged, 195 tests, 0.2.0 |
| 3 | `bm edit` — fix a wrong title/tags without losing the id; `--clear-title` as the captive-portal recovery path; + BUG-0001 and BUG-0010 fixes | same chain, interrupted mid-run by a rate limit and resumed | **Shipped**, merged, 248 tests, 0.3.0 |
| — | **`superfunk:process-review`** over all three shipped specs | triggered by SDD's Finish gate at 3 specs | **Ran clean**, `review-after-2026-08-29-edit-command-design.md`, tracker reset |

Cycle 3 was interrupted twice by account rate limits (session limit, then weekly limit). Both
are trial-environment events, not framework failures — but the *resume* behavior is a genuine
result and is recorded under *What worked*.

**Three specs reached `Shipped`, and the process-review gate fired correctly** at the
threshold, using the ask-don't-force pattern the skill specifies. It was run and completed.

Final state: `master` clean at `ccfc63a`, 89 commits, 248 tests, no leftover worktrees or
branches. Artifacts the framework produced unprompted on a zero-convention repo:
`docs/bugs/tracker.md` + 11 bug files, `docs/superpowers/{specs,plans}/` (3 specs, 3 plans,
3 outcomes ledgers), `docs/superpowers/process-reviews/` (tracker, 25-entry notes.md, and one
completed review), `docs/lessons-learned.md` (6 entries under 2 categories), `docs/patterns/`
(3 promoted patterns), `README.md`, a `CHANGELOG.md` with all three releases, and a
`pyproject.toml` with pytest configured and a `dev` extra.

---

## Findings

### D1 — `hooks/session-start` still injects the pre-rebrand skill name  *(rebrand miss, live)*

**Where:** `plugin/hooks/session-start`, line 27.

The bootstrap injected into **every** session reads:

```
<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n**Below is the full content of your
'superpowers:using-superpowers' skill - your introduction to using skills. …
```

Under the fork the skill resolves as `superfunk:using-superpowers`. `superpowers:` is not a
namespace that exists in a fork-only session.

**Why it's wrong:** the very first instruction block a session sees names a skill id that
cannot resolve. It happens not to break anything *only* because the hook inlines the skill
body rather than asking the model to invoke it — so nothing ever tries the bad name. Any
model that decides to re-read that skill by the quoted id gets a resolution failure. The
branding line "You have superpowers." is stale for the same reason.

**Confidence this is a miss, not a deliberate hold-back:** every live skill file *was*
rebranded correctly — e.g. `executing-plans/SKILL.md:14` says
`superfunk:subagent-driven-development`. Only the hook was left behind. A repo-wide grep for
`superpowers:[a-z-]+` returns hits in `hooks/session-start`, `.pi/extensions/superpowers.ts`,
and historical `docs/plans/**` (harmless), and nowhere in `skills/**/SKILL.md`.

**Note on paths:** `docs/superpowers/…` and `.superpowers/…` paths are used consistently
throughout and are *not* flagged here — they appear to be a deliberate retention.

---

### D2 / D3 — Skills reference repo-level docs that are not part of the distributed plugin

> **Corrected 2026-08-30.** An earlier draft of this report claimed `pattern-template.md` and
> `ai-code-guidelines.md` "do not exist anywhere" and that the framework "invented a format".
> Both claims were wrong. My search was scoped to `plugin/` only, and I did not compare the
> generated patterns against the real template. The corrected finding is narrower and its
> severity is lower. Details below.

**The files do exist** — at the superfunk *development repo* root, not inside `plugin/`:

- `superfunk/docs/patterns/pattern-template.md`
- `superfunk/docs/ai-code-guidelines.md`
- `superfunk/docs/code-standards.md`

**The defect is a distribution boundary, not a missing file.** The plugin is loaded via
`--plugin-dir <repo>/plugin`, so only `plugin/` ships. These paths are written relative to the
*current project*, so they resolve when superfunk develops itself and dangle for every
downstream project. Confirmed in the trial: the bookmark repo got `docs/lessons-learned.md`
and `docs/patterns/` created for it, but never an `ai-code-guidelines.md` or a
`code-standards.md`.

**The sharper half of this — unguarded reads.** The framework already knows how to degrade:
`brainstorming` says "No `docs/lessons-learned.md` yet: skip this check", and SDD's
concept-index step says "If the index file doesn't exist yet … skip". The
`ai-code-guidelines.md` references mostly carry **no such guard**. Most direct:
`subagent-driven-development/implementer-prompt.md:18` instructs every implementer subagent to
*"Also read `docs/ai-code-guidelines.md` and `docs/code-standards.md` before you begin"*, and
`task-reviewer-prompt.md:114` tells every task reviewer to read and check the diff against it.
In this trial that instruction was issued to ~20 subagents against files that did not exist.

**What did NOT happen — correcting the earlier claim.** The three promoted patterns in the
trial repo match the real template *exactly* — `# Title`, `## Context`, `## Pattern`,
`## Example`, `## Originating lessons`, three for three. Nothing was improvised. Notably, that
structure is documented **nowhere in `plugin/`** (a search for "Originating lessons" across
the plugin returns zero hits), so the correct output came from the model's own prior knowledge
rather than from anything the framework supplied. Correct by luck is not the same as correct
by construction, but the observed harm here is zero.

**Revised severity:** low. Real, cheap to fix, but no damage observed.

**Fix shape:** make the references self-contained rather than path-dependent — inline the four
pattern section names at the point of use, and guard the guideline reads with the same "skip
if absent" phrasing the other checks already use. Shipping copies of these docs into `plugin/`
is the alternative, and is a design decision rather than a repair.

---

### D4 — The worktree is created *inside* the repo it is supposed to isolate, and nothing ignores it

`superfunk:using-git-worktrees` prefers the harness's native `EnterWorktree`, which placed
the worktree at:

```
C:/sf-bookmark-cli-trial/.claude/worktrees/bookmark-cli
```

— nested inside the main checkout's own working tree. Two harms were **observed**, not
theorized:

1. **A second source tree plus site-packages inside the repo.** The worktree acquired its
   own `.venv/` (pytest, pluggy, iniconfig, colorama, an editable install of `bm`). A
   recursive listing from the repo root walked ~54 KB of vendored library paths. Anything
   that globs from the project root — packaging, linting, a naive `pytest`, a security
   scanner — sees two copies of the source.
2. **`master` left permanently dirty.** After cycle 1's merge, `git status` on `master`
   reported `?? .claude/`, which it had not before. Claude Code's `.git/info/exclude` covers
   `.claude/settings.local.json` but not the directory. The merged branch's own `.gitignore`
   did not cover it either. The repo sat one `git add -A` away from committing an entire
   second checkout and a virtualenv.

Neither `using-git-worktrees` nor `finishing-a-development-branch` added an ignore rule. The
fix only happened because the operator, playing the user, noticed `?? .claude/` and asked for
it. When asked, the framework fixed it correctly and verified with a probe file
(commit `5e06727`, rule `.claude/worktrees/`) — but a user who doesn't read `git status`
carefully never gets that.

**Fix shape:** whichever skill creates the worktree should ensure `.claude/worktrees/` (or
whatever path it chose) is ignored, at creation time, before any work lands.

---

### D5 — A skill-mandated checkpoint consumes the whole turn, dropping direct user questions

**Sequence.** At the end of brainstorming, the spec Self-Review reported "three genuine
ambiguities" and then listed two. As the user I asked what the third was — the only
non-approval content in my next message.

- **Turn 10** (`writing-plans` ran): no answer anywhere in the turn's transcript. The output
  is plan-writing results ending in the plan's own execution-options prompt.
- **Turn 11** (SDD's worktree consent gate fired): I re-asked with *"Answer that before you
  start executing."* The entire turn output is the worktree gate. Still no answer.
- **Turn 12**: asked a third time, explicitly flagging it as the third ask. **This time it
  was answered**, fully and correctly (the third item was the `fetch_attempts` increment
  rule; self-review made two spec edits covering three under-specified points, so the count
  was right and the earlier report merely under-listed).

**Verified against the full transcript, not `-p` output.** Turns 10 and 11 contain no
assistant text on the topic at all — genuinely dropped, twice.

**Why it's wrong.** `using-superpowers` states the priority order explicitly: *"User's
explicit instructions … highest priority."* A checkpoint template that emits only the
checkpoint inverts that. The framework itself later diagnosed the cause (transcript line
304): *"my first two answers were buried under gate output."*

**Fix shape:** a line in every gate/checkpoint template — "also address anything else the
user asked in this message" — or an explicit rule in `using-superpowers` that a pending user
question outranks emitting a checkpoint verbatim.

**Contributing defect:** the brainstorming Self-Review step reported a finding *count* it did
not substantiate in its own list. A self-review that miscounts its own output is a
self-review whose summary isn't being checked against its body.

---

### D6 — `subagent-driven-development`'s Finish does documentation bookkeeping *after* the final review, so the reviewer necessarily sees stale docs

This is the framework's own most consequential process defect, and the framework caught it
itself. Verbatim from the project's `docs/superpowers/process-reviews/notes.md`:

> `2026-08-29 | Miss | Final review (retry-sweep) |` the feature shipped with README still
> stating "No retry for failed fetches... no command is wired to it yet", no CHANGELOG entry,
> and version still 0.1.0. The spec was marked User-Facing: Yes and the PREVIOUS feature
> updated both files, so the mechanism exists and was simply not run. **Root cause: the
> documentation check fires at Finish, after the final review, so a whole-branch reviewer
> sees a branch whose docs contradict its code.**

Cycle 2's feature would have shipped invisible in its own README. The final review blocked the
merge and caught it — but only because that reviewer happened to look at docs; the ordering
guarantees a stale-docs branch reaches the review gate every time for a user-facing spec.

The framework recorded the lesson (`docs/lessons-learned.md`: "User-facing docs must ship in
the task that ships the surface") and cycle 3's plan applied it by moving README/CHANGELOG/
version-bump into the task that adds the surface. That's the right fix, discovered
empirically at the cost of one blocked merge — it belongs in the skill, not in each project's
lessons file.

---

### D7 — Brainstorming's per-section gate is unconditional, so blanket consent decays

By turn 23 I had given blanket consent covering spec → plan → worktree → execution → merge
**twice** (turns 19 and 21), and turn 23 itself said *"Section 2, then run the whole chain
through to merge."* The response still ended with *"Does this look right? If so I'll write
the spec, then take it through plan, worktree, execution and merge without stopping."*

**Partial defence, and it matters:** that same message surfaced a genuinely new decision —
widening the BUG-0001 fix so `list`/`search` also display the openable URL form, making
"display equals destination" true by construction rather than narrowing the gap to tracking
parameters. Stopping for *that* was correct.

The defect is that the gate is written as an unconditional "Does this look right?" and
doesn't distinguish "I need a ruling on something new" from "the template says to check in."
The user-visible effect is being asked for the same consent three times, which reads as the
tool not listening.

**Fix shape:** make the section gate conditional — ask when the section introduces a decision
the user hasn't made; otherwise state the section and continue.

---

### D8 — No CLAUDE.md is ever produced, across two complete pipeline cycles

After 25 turns, two shipped specs, 35+ commits, and a fully-populated `docs/` tree, the repo
root contains `README.md` and `CHANGELOG.md` and nothing else. No CLAUDE.md, no AGENTS.md,
no `.context.md` anywhere.

This is worth stating plainly because the framework *did* bootstrap almost everything else
unprompted, and because several skills begin by reading project conventions (`.context.md`,
`docs/lessons-learned.md`, `docs/patterns/*`) — every cycle opened with a context check that
found `.context.md: none exist`. The framework reads a convention layer it never writes.

`superfunk:project-definition` exists and was never invoked, on the one project where a fresh
project definition was maximally warranted.

**What did get established correctly:** a test runner. `pyproject.toml` carries
`[tool.pytest.ini_options] testpaths = ["tests"]`, an autouse `conftest.py` fixture that
points `BM_DB_PATH` at `tmp_path` for every test, and a `dev` extra pinning `pytest>=8`. No
CI config was created, which for a local-only trial project is defensible.

---

### D9 — `subagent-driven-development`'s "there is no second fix wave" has no branch for a regression the fix wave itself introduces

**Where:** `subagent-driven-development/SKILL.md`, Final Review section — *"There is no second
fix wave — residual load-bearing findings surface to your human partner when
finishing-a-development-branch presents the options."*

**What happened in cycle 3.** The single permitted fix wave introduced a new crash:
`for_opening` read `parts.port`, which raises on a malformed port. One typo'd URL stored a
poison row that made `bm list` exit 3 displaying *nothing* — every bookmark invisible. The
re-review *of that wave* caught it.

The rule left three options, all bad: merge a known crash that hides the user's entire
library; stop and ask the human to approve a one-line guard; or break the rule. The framework
broke the rule, did one extra scoped fix dispatch, and **declared it explicitly** with the
reasoning — which is the best available behavior, but it is still a rule violation forced by
the rule's own shape.

**Why the rule is right and the gap is narrow.** The cap exists to stop unbounded review-fix
cycles. A regression introduced *by* the wave and caught *by* its own single re-review is
bounded by construction. The distinction the skill is missing is between a finding the wave
**failed to fix** (stays parked — that's what the cap is for) and a regression the wave
**introduced** (needs exactly one scoped follow-up).

This trial's own process-review reached the same conclusion independently and filed it as
`G1`, with the amendment named against `subagent-driven-development/SKILL.md`.

---

### D10 — Shipping a feature leaves behind the text describing its absence (2 occurrences, 2 specs)

Distinct from D6 and worse, because D6 is about docs *lagging* and this is about docs
*actively misdirecting*.

- Cycle 2: `README.md` still said "No retry for failed fetches… no command is wired to it
  yet" for the feature the branch shipped.
- Cycle 3: `bm add --title` on an already-saved URL still printed **"remove and re-add to
  change it"** — pointing the user at the destructive operation that `bm edit` had just been
  built to replace, and that destroys the id and every tag.

Both were caught by the final whole-branch review, i.e. at the most expensive possible moment.
Nothing earlier in the pipeline looks for text that a new feature has just made false. The
trial's process-review promoted this to the pattern
`hunt-the-workaround-not-the-feature.md` and recommended a stale-workaround grep in
`writing-plans`' Self-Review.

---

## What worked — recorded so the defect list isn't read as a verdict

These are not padding; they are the evidence that the expensive parts of the process pay for
themselves.

**The review layers caught defects the plan itself authored.** From `notes.md`, all
plan-authored rather than implementer slips:

- `search()` interpolated user text into a `LIKE` pattern unescaped, so `_` and `%` acted as
  wildcards — `async_std` matched `asyncXstd`, `100%` matched `10099`.
- `cmd_add` decided title/fetch-status *before* checking whether the URL already existed, so
  re-adding a bookmark to tag it — the exact workflow the spec designates as the tagging path
  — performed a full network fetch and threw the result away.
- `cmd_open` discarded `webbrowser.open`'s return value, so `bm open` exited 0 having
  launched nothing in a headless session.
- `test_read_is_capped` asserted `8192 <= 65536` — the loop's own arithmetic against its own
  constant. Raising `MAX_BYTES` from 64 KB to 100 MB passed 113/113 tests.
- `shutdown(cancel_futures=True)` cancelled nothing, because one-future-per-host means every
  future is already running. An interrupted sweep printed its summary and kept fetching the
  whole backlog — measured 3.01s → 0.60s, 30/30 fetches → 6/30 after the fix.

**The Task 4 reviewer built four deliberately-broken implementations and ran the suite
against each**, discovering that all eight scheduling tests passed a structurally-wrong
implementation (per-bookmark futures with per-host locks — observably polite, starves
cross-host parallelism). That became the promoted pattern
`build-the-mutant-you-claim-to-reject.md`.

**Escalation discipline held.** When the Task 2 review found that `normalize()` trimmed
exactly one trailing slash — breaking the idempotence property the plan itself asserted — it
correctly identified that the fix contradicted the *spec text* rather than the
implementation, and stopped for a human ruling instead of silently choosing. Minor findings
in the same review were deferred to final review rather than looped on.

**Blanket consent was honored where the decision was genuinely already made.** Cycle 2 ran
spec → plan → worktree → ~100 minutes of subagent execution → final review → fix wave → merge
→ worktree cleanup on one message of consent, with zero redundant confirmations, stopping for
nothing that wasn't new. This is the direct counter-evidence to a "ritual confirmation loops"
reading of D7.

**Limitations were volunteered rather than buried.** Two examples: a hang-guard test that
"proves the fixed code terminates but cannot go red" on the regression it names (reverting
the fix hangs rather than fails, and `pytest-timeout` is excluded by the project's
zero-dependency constraint); and BUG-0010 parked rather than fixed because the process allows
one fix wave after final review and it was found by the re-review *of* that wave. Both were
stated with reasoning.

**The bookkeeping bootstrapped correctly on a zero-convention repo** — bug tracker, per-bug
files with reproductions, process-review tracker and notes, lessons-learned with categories,
pattern promotion, spec `Status:` flips, and `-outcomes.md` ledgers all appeared without being
asked for.

**Resume after a mid-execution kill worked, and worked for the right reason.** The rate limit
killed the session during Task 1's *review* dispatch — code committed, no completion line in
the ledger. On resume the framework re-ran the review rather than re-dispatching the
implementation, and said so: *"That's exactly what the ledger exists for; without it I'd have
had to guess."* The `<workspace>/progress.md` ledger did the job it's designed for, against a
failure mode nobody planned for.

**`process-review` fired at the right moment and produced a genuinely useful synthesis.**
SDD's Finish step counted three filenames in the tracker and offered the review (ask, not
force). Over 3 specs / 88 commits / 25 logged notes it produced 19 Catches, 3 Misses, 1
Friction, 3 Gaps, and 5 unchecked Recommendations targeting specific plugin files, then reset
the tracker and recorded itself. Its top finding is one no single cycle could have seen:

> Five of the nineteen Catches record the same thing in different words: *the plan's own text
> carried the defect.* The implementers transcribed correctly every time. In three of those
> five the **spec** was wrong, so the plan was faithful to a bad instruction.

and

> Four tests across all three specs could not fail. Every single one was found by *mutation* —
> and every one of those mutations happened because an individual reviewer chose to, not
> because any prompt asked.

It also declined to invent a Recommendation for `G3` (the suite can hang instead of failing;
`pytest-timeout` would fix it but is barred by the project's zero-dependency constraint),
recording it as a known limitation because it is a real conflict between two things the user
asked for. That restraint is the correct behavior and worth noting.

---

## Coverage gaps — things this trial did *not* exercise

Stated so nobody reads the absence of findings as a clean bill of health.

- **`superfunk:executing-plans` never ran** — SDD was available and worked every time, so the
  fallback path was never taken.
- **Never invoked at all:** `project-definition`, `concept-index`,
  `dispatching-parallel-agents`, `receiving-code-review`, `writing-skills`,
  `systematic-debugging` (no bug was debugged interactively; all were found by review).
- **`finishing-a-development-branch` was only exercised on its merge path.** The PR path and
  the abandon path were never taken, because the trial repo has no remote.
- **One trial-side event, not a framework defect:** the child session hit an account session
  limit and then a weekly limit mid-execution of cycle 3. It resumed correctly from the
  ledger — see *What worked*.
- **`process-review` ran once, on its first-ever trigger.** Its behavior on a *second* review
  (consuming a prior `review-after-*.md`, checking off Recommendations that later specs
  close) is untested — that path needs three more shipped specs.

---

## Triage

| # | Finding | Verdict |
|---|---|---|
| D1 | `hooks/session-start` injects `superpowers:using-superpowers` | **Genuine defect, trivial fix.** One string in one file. Rebrand miss. |
| D2/D3 | Skills reference repo-level docs not shipped in `plugin/` | **Genuine but low severity — downgraded on correction.** The files exist in the superfunk repo; they just aren't distributed, so the paths dangle downstream. Worst instance is unguarded: every implementer and task-reviewer subagent is told to read two files that don't exist. Zero observed harm — the patterns came out matching the real template exactly. Cheap to fix. |
| D4 | Worktree inside the repo, no ignore rule | **Genuine defect.** Two observed harms. The fix (ignore at creation time) is small and belongs in `using-git-worktrees`. |
| D5 | Checkpoint output drops direct user questions | **Genuine defect.** 2 of 3 asks dropped, verified against the transcript. Contradicts `using-superpowers`' own stated priority order. Needs a template line, not a redesign. |
| D6 | Docs bookkeeping happens after the final review | **Genuine defect, highest value to fix.** Structural ordering bug: for any user-facing spec, the whole-branch reviewer is guaranteed to see docs that contradict the code. The framework found it, fixed it *in one project's lessons file*, and the skill still has the old ordering. |
| D7 | Unconditional section gate re-asks settled consent | **Genuine but mild.** Partly defensible — the same turn raised a real new decision. Worth making the gate conditional. |
| D8 | No CLAUDE.md ever produced | **Genuine gap, judgment call on whether to fix.** The framework reads a convention layer it never writes, and `project-definition` never fires on the case that most warrants it. Arguably intentional restraint; flagged for a ruling rather than asserted as a bug. |
| D9 | "No second fix wave" has no branch for a regression the wave itself introduced | **Genuine defect.** Forced a rule violation to avoid merging a crash that hid the user's whole library. Independently found by the trial's own process-review as `G1`, with a narrow amendment already drafted. |
| D10 | Shipping a feature leaves the text describing its absence | **Genuine defect, 2 occurrences / 2 specs.** Worse than D6: cycle 3's stale text actively pointed the user at the destructive operation the new feature replaced. Caught only at the final review both times. |
| — | Brainstorming self-review reported "three" and listed two | **Genuine but minor**, and it is the proximate cause of D5's chain. A summary-vs-body consistency check would catch it. |
| — | Rate-limit interruptions | **Not a framework issue.** Trial-environment event. |
| — | Worktree-report-not-shown, "false claim about own output" | **Withdrawn — trial-harness artifact.** `claude -p` truncation, not framework behavior. Documented above so it isn't rediscovered. |

No finding here looks like a one-off fluke. D1–D4 are static — they are properties of files on
disk and will reproduce on any project. D5 and D7 reproduced across multiple turns and two
different skills. D6, D9 and D10 are structural, and each was independently diagnosed by the
framework's own process-review from evidence accumulated across all three specs.

**The single highest-leverage fix is not on this list.** It is the trial's own process-review
recommendation: move the **mutation check** into the task-reviewer template. Four tests across
three specs could not fail, every one was found by a reviewer choosing to mutate the
implementation, and no prompt ever asked for it. That is currently a convention with no home —
it works when a reviewer happens to reinvent it, at the most expensive gate. See `G2` and the
five unchecked Recommendations in
`C:\sf-bookmark-cli-trial\docs\superpowers\process-reviews\review-after-2026-08-29-edit-command-design.md`,
which name their target files in the superfunk plugin directly.

---

## Keep or discard `C:\sf-bookmark-cli-trial`?

**Keep it.** It is now a more valuable fixture than it was a test project.

Reasons:

1. **It holds a completed process-review with five unchecked Recommendations that name files
   in this plugin.** `review-after-2026-08-29-edit-command-design.md` is a real, evidence-backed
   work queue for the framework, derived from 88 commits it would be expensive to fabricate.
2. **It is the only fixture for the second-review path.** `process-review` has now run once,
   from a cold start. Its behavior when a *prior* review exists — consuming
   `review-after-*.md`, checking off Recommendations that later specs close, which
   `brainstorming` and SDD's Finish both depend on — is still untested. Three more shipped
   specs here would exercise it; a fresh project would need six.
3. **`notes.md` holds 25 real Catch/Miss/Friction/Gap entries** across three specs — exactly
   the input `process-review` consumes, and hard to synthesize convincingly.
4. **It is a live regression fixture for D1–D4 and D9–D10.** After fixing the missing template,
   the missing guidelines doc, the worktree placement, or the fix-wave rule, re-running one
   cycle here shows immediately whether the fix took.

Costs of keeping it are near zero: no remote, no CI, a few MB. The worktrees have been cleaned
up by `finishing-a-development-branch` each cycle; `master` is clean at `ccfc63a`.

Discard only if D6 is fixed by changing the SDD Finish ordering, since that would make a fresh
from-scratch run the more honest test of the new ordering. Everything else is better tested
here than on a new project.

---

## Fix order

Merged with the five Recommendations the trial's own process-review filed, since they overlap.

**Tier 1 — cheap, no judgment required, do together.**

1. **D4, worktree ignore rule** (`using-git-worktrees`). The only defect that can damage a
   user's repo. The precise bug: the `git check-ignore` safety verification exists *only* in
   Step 1b (the manual `git worktree add` fallback). Step 1a — the **preferred** native-tool
   path, and the one actually taken in all three cycles — has no ignore check at all.
2. **D1, rebrand string** (`hooks/session-start`). One string, plus a stale header comment.
3. **D2/D3, dangling doc references.** Inline the pattern section names; guard the guideline
   reads with the "skip if absent" phrasing already used elsewhere.

**Tier 2 — highest value in the list.** R2: move the **mutation check** into
`task-reviewer-prompt.md`. Four tests across three specs could not fail; every one was caught
because a reviewer chose to mutate, and no prompt ever asked. Fold in R5
(equality-not-containment) as part of the same edit.

**Tier 3 — one root cause, three symptoms.** D6 + D10 + R3: move the docs step out of `Finish`
into the task that ships the user-visible surface, and add the stale-workaround grep to
`writing-plans`' Self-Review. Low risk — cycle 3 already validated this by hand.

**Tier 4 — real, lower confidence or lower frequency.** R1 hostile-input pass (ship it
*separately* from R2, or you won't know which one worked); D9/G1 fix-wave amendment (drafted,
narrow, fired once); D5/D7 conversational gates (cheapest to attempt, least certain to hold —
these are model-behavior-shaped).

**Not a fix, needs a ruling.** D8 (no CLAUDE.md; is `project-definition` never firing a gap or
deliberate restraint?) and G3 (suite hangs instead of failing; a genuine zero-dependency
conflict the review correctly declined to paper over).

**Verification.** Re-run one cycle in `C:\sf-bookmark-cli-trial` — the only fixture where
D1–D4 and D9–D10 re-trigger.

---

## Appendix — where the evidence lives

- Full child-session transcript (every assistant message, including ones `-p` never printed):
  `~/.claude/projects/C--sf-bookmark-cli-trial/659f8ca6-433f-4f5e-b723-c07e3b724c9f.jsonl`
- Per-turn prompts and outputs: the trial scratchpad, `p01–p25.txt` / `o01–o25.txt`
  (and `o*.all.txt` from turn 18 onward, which contain all assistant blocks)
- The project's own process record: `C:\sf-bookmark-cli-trial\docs\superpowers\process-reviews\notes.md`
- **The process-review the framework produced about itself, with five actionable
  Recommendations naming files in this plugin:**
  `C:\sf-bookmark-cli-trial\docs\superpowers\process-reviews\review-after-2026-08-29-edit-command-design.md`
- The project's own bug record: `C:\sf-bookmark-cli-trial\docs\bugs\tracker.md`
- Promoted patterns: `C:\sf-bookmark-cli-trial\docs\patterns\` —
  `audit-deferrals-as-a-set.md`, `build-the-mutant-you-claim-to-reject.md`,
  `hunt-the-workaround-not-the-feature.md`

No files under `plugin/` or `docs/` were modified during the trial. This report is the only
thing written to the superfunk repo.
