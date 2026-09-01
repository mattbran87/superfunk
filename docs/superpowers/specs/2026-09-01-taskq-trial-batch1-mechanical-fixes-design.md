# Taskq Trial Batch 1 — Mechanical Fixes — Design

**Status:** Shipped
**User-Facing:** No

## Context

The second external trial (`taskq`, a multi-module Python task queue,
`C:\sf-taskq-trial`) shipped four full pipeline cycles and produced
`docs/superpowers/process-reviews/external-trial-taskq-findings.md`: 15
findings (F1–F15) and 15 verified positives. The report's own triage table
splits the findings into three groups: cheap mechanical fixes, fixes that
need a small scoped decision, and one structural reachability question
(F5/F6/F8/F11 — skills that fire only when another skill's control flow
names them, not when their own `description:` matches).

This spec covers the first group only — 8 findings the report itself calls
"Trivial" or "Low" cost, each a wording or scope change confined to one or
two files, none touching the structural question. F15 (brief-as-suspect
mandate), F4 (`executing-plans`' missing Finish), F9.1/F9.2
(`concept-index` bootstrap and unit types), and F12 (`brainstorming`'s
convergence budget) each need their own small design and ship in later
batches.

## Decision

### F9.3 — `.context.md`'s `**Purpose:**` line and `## Purpose` heading disagree

`docs/ai-code-guidelines.md`'s Per-Directory Context Files section already
specifies the correct template — a `**Purpose:**` bold line — and
`concept-index/SKILL.md` reads exactly that line. But `brainstorming`'s
scaffold offer drafts a *downstream* project's own
`docs/ai-code-guidelines.md` from three interview answers, with nothing
telling it to carry this framework's own Format block over verbatim. Two
`.context.md` files the taskq trial's own SDD cycles generated used
`## Purpose` as a heading instead, so `concept-index` could not read either
one and fell back to asking the user for a description by hand.

`brainstorming/SKILL.md`'s scaffold-offer bullet (in "Understanding the
idea") gains one sentence, added after "Draft whichever file(s) were
missing from the answers, commit them, then continue.":

```markdown
If drafting `docs/ai-code-guidelines.md`, its Per-Directory Context Files
section must copy this project's own Format block verbatim (the
`**Purpose:**` bold line, not a `## Purpose` heading or any other
paraphrase) — this is the exact line `concept-index` parses, so the two
halves stay in sync by construction rather than by chance.
```

### F13 — Self-Review item 10 checks enumerated counts, not asserted budgets

Item 10 verifies a step's own `Expected:` count against a real command run,
but a plan's Global Constraints section can separately assert a numeric
budget (a line-count ceiling, a performance target) that nothing checks
against the plan's own task-level arithmetic. `taskq`'s spec 4 blew a
681-line ratchet by a margin derivable from the plan's own line counts
before any code existed, and item 10 did not catch it because the number
lived in Global Constraints, not a step's `Expected:` field.

`writing-plans/SKILL.md`'s item 10 gains one sentence at its end:

```markdown
This item's scope also covers any numeric budget the plan's Global
Constraints section states — a line-count ceiling, a performance target, a
size limit. Sum each task's own added or changed line counts against a
stated ceiling before finalizing the plan; a budget nobody checked against
the plan's own arithmetic counts as the same failure as an unchecked
`Expected:` value.
```

### F14 — a token-containment guard can pass while protecting nothing

A test asserting a document or output contains some specific token (a
word, a flag, a phrase) can stay green after the very thing it guards gets
deleted, if that token already appears elsewhere in the same content. Two
of `taskq`'s four specs hit this shape independently — a `--help`
width guard, and a README guard asserting `"JSON" in section` when
`"JSON-serializable"` already sat in the same section. Nothing in
`writing-plans` or `task-reviewer-prompt.md` names the class, so each
occurrence costs a fresh discovery; the mutation check catches it only
per-task, from scratch.

`task-reviewer-prompt.md`'s Mutation Check section gains one sentence,
appended after the existing equality-not-containment trap:

```markdown
A second related trap: an assertion that a document or output contains a
specific token can pass today only because something else in the same
content already supplies that token — deleting the exact thing the
assertion exists to protect then leaves it green. For any assertion of
this shape, check whether the asserted token already appears elsewhere in
the same content, independent of the mutation check above. See
docs/patterns/assert-on-a-token-the-context-cannot-supply.md.
```

A new pattern file, `docs/patterns/assert-on-a-token-the-context-cannot-supply.md`,
gets written at Finish time (this failure class recurred twice within one
trial, meeting the existing promotion bar of "recurs a second time"):

```markdown
# Assert on a Token the Context Cannot Supply

A containment assertion (`"X" in output`) that stays green after deleting
the thing it guards, because the surrounding content already supplies `X`
some other way.

## Context

A guard checks that a document, output, or diff contains some specific
word or flag, chosen to avoid pinning exact wording. This applies whenever
a plan or reviewer writes a "contains" assertion instead of an equality
assertion.

## Pattern

For every assertion that content contains a chosen token, check whether
that token — or a superstring/synonym of it — already appears elsewhere in
the same content before the guarded change ships. If it does, the
assertion cannot discriminate the guarded change from its absence; either
pick a token that appears nowhere else, or assert on the specific location
(a line number, a section) instead of a bare substring search.

## Example

A README guard asserted `"JSON" in section`, chosen as a "distinctive
noun" to avoid pinning wording. The same section already contained
`"JSON-serializable"` one line above the bullet the guard existed to
protect — deleting that bullet left the assertion green, because the
neighboring word alone satisfied it.

## Originating lessons

- "Non-discriminating containment guards" (taskq-trial-batch1-mechanical-fixes)
```

### F1 — scaffold-offer questions 2 and 3 have no skip conditions

Only question 1 (language/stack) carries a stated skip condition ("skip if
already evident from existing files"). On an empty repo, observation
cannot answer question 3 (build/test commands, architecture notes), yet
nothing in the skill flags that gap — the taskq trial
scaffolded both files in one shot, asking zero of the three questions, and
disclosed afterward that it had picked five tooling defaults the user
never chose.

`brainstorming/SKILL.md`'s scaffold-offer bullet's question list changes
from:

```markdown
ask up to three questions, one at a time: the project's language/stack
(skip if already evident from existing files), any coding conventions
already followed informally, and anything future sessions should know
upfront (build/test commands, architecture notes).
```

to:

```markdown
ask up to three questions, one at a time: the project's language/stack
(skip if already evident from existing files), any coding conventions
already followed informally (skip if a linter or formatter config already
establishes them observably), and anything future sessions should know
upfront — build/test commands, architecture notes (ask this one outright
on a new or near-empty repo; observation cannot substitute for it there).
```

### F3a — Step 7's cleanup-ownership test misses the native tool's own path

`using-git-worktrees` prefers a harness's native worktree tool
(`EnterWorktree` or equivalent) when one exists, and defers to it entirely
for placement — its own manual-fallback table only ever checks
`.worktrees/` or `worktrees/`. Claude Code's native tool places worktrees
at `.claude/worktrees/<name>`, a path `finishing-a-development-branch`'s
Step 7 does not recognize, so it takes the "host environment owns this
workspace" branch for a worktree the framework itself directed into
existence.

`finishing-a-development-branch/SKILL.md`'s Step 7 changes from:

```markdown
**If `WORKTREE_PATH` is under `.worktrees/` or `worktrees/`:** Superpowers
created this worktree — we own cleanup:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```
```

to:

```markdown
**If `WORKTREE_PATH` is under `.worktrees/`, `worktrees/`, or
`.claude/worktrees/`:** Superpowers created this worktree — we own
cleanup. If a native worktree-exit tool created it (the same one
`using-git-worktrees` used to enter it), try that tool first — it owns
placement and branching, so it is the matching way back out. Fall back to
the manual commands below only if no native exit tool exists, or it
fails:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```
```

### F7 — the PR path can report success without confirming a PR exists

Option 2 assumes a forge exists and says to create the PR "with the
forge's tooling," but never says to confirm the tooling actually
succeeded before reporting a PR back to the user. Against a bare local
`origin`, the taskq trial's own run behaved well by actually invoking
`gh pr create` and reporting its refusal — but nothing in the skill
requires that verification step, so a less careful run could report "PR
created" having only pushed.

`finishing-a-development-branch/SKILL.md`'s Option 2 section gains one
sentence, inserted before "Keep the worktree":

```markdown
Confirm the forge CLI actually created a PR — its exit status and printed
URL — before reporting one back to your human partner; a successful push
alone does not mean a PR exists. If the repository has no forge remote (a
bare or local-only `origin`), say so plainly and stop after the push.
```

### F2 — Finish's "merged" reads as "merged to the base branch"

`subagent-driven-development`'s Finish section opens with "When the final
whole-branch review is clean and its fixes are merged" — intended to mean
the fix wave's commits sit on the current branch, but readable as "merged
to the base branch," which has not happened yet at this point in the
process. Under the second reading, a run deferred the Status flip and the
tracker append entirely in one observed cycle (the taskq trial's cycle 1),
reasoning that Status "flips on merge, which is yours to call."

`subagent-driven-development/SKILL.md`'s Finish section's opening sentence
changes from:

```markdown
When the final whole-branch review is clean and its fixes are merged,
check whether this plan traces to a design spec
```

to:

```markdown
When the final whole-branch review is clean and its fix wave's commits sit
on this branch — not yet merged to the base branch, which
`finishing-a-development-branch` handles afterward — check whether this
plan traces to a design spec
```

### F2a — the bookkeeping's relationship to the 3 integration options goes unstated

`finishing-a-development-branch` never mentions spec Status or the
tracker on any of its 3 options — a reader could take that silence as a
gap in this skill, rather than as bookkeeping some other skill already
finished. The taskq trial's own live evidence for this gap (spec 2,
reached via Option 2) traces entirely to `executing-plans` skipping Finish
outright (F4, fixed in a later batch) — but the ambiguity this finding
names holds independent of that: nothing in `finishing-a-development-branch`
tells a reader that this bookkeeping already ran, or under what condition
it might not have.

`finishing-a-development-branch/SKILL.md`'s Overview section gains one
sentence, appended after the existing "Core principle" line:

```markdown
Spec-Status and process-review-tracker bookkeeping is the dispatching
skill's job (`subagent-driven-development`'s Finish section), and it runs
before this skill gets invoked — none of the 3 options below repeat it.
Arriving here from a path that skips that Finish step (a manual merge, or
`superfunk:executing-plans`, which has no Finish step of its own) means
that bookkeeping has not happened; flag this to your human partner rather
than assuming it already did.
```

## Alternatives Considered

**F14:** add only the inline sentence to `task-reviewer-prompt.md`, versus
also promoting a pattern file. Chose both — the failure class recurred
twice within one trial (the existing bar for promotion), and a pattern
file gives future specs a stable cross-reference the way
`verify-plan-commands-against-real-content.md` already does for a sibling
failure class.

**F2a:** duplicate the Status/tracker bookkeeping into all 3 of
`finishing-a-development-branch`'s options, versus stating the
responsibility boundary once in its Overview. Chose the latter — the
report itself offers both as viable ("move it into
finishing-a-development-branch, or state it on every path"), duplicating
multi-step bookkeeping logic into 3 places doubles the maintenance
surface for the exact kind of drift that already caused F2, and the actual
missing-bookkeeping case this finding's live evidence hit traces to
`executing-plans` lacking Finish altogether (F4) — a later batch's fix —
not a gap in this skill's own 3 options.

**F3a:** always run `git worktree remove` for a recognized path, versus
preferring a matching native exit tool first. Chose the latter, mirroring
`using-git-worktrees`' own "prefer native tools, fall back to manual"
rule for entry — a worktree the framework asked a native tool to create
should exit through that same tool's cleanup path when one exists, per
the trial's F3b observation that the harness's own `ExitWorktree` behavior
(refusing without `discard_changes: true`) warrants routing through
deliberately rather than bypassing by default.

## Consequences

`concept-index` reads a `.context.md` correctly on the first downstream
project it runs against with a scaffolded `docs/ai-code-guidelines.md`
(F9.3), instead of falling back to an interrogation. A plan that would
blow a stated line-count or performance budget gets caught during
Self-Review, before any task starts (F13). A reviewer checks one
additional failure shape during the Mutation Check, backed by a named
pattern file (F14). A scaffold offer against a near-empty repo asks the
one question observation cannot answer, instead of silently picking
defaults (F1). A worktree the framework created through a native tool
gets recognized and cleaned up through that same tool, instead of taking
the "not ours" branch by accident (F3a). A PR-path run states plainly when
no PR actually got created, instead of reporting success from a push alone
(F7). Finish's own bookkeeping sentence no longer reads as gated on a
merge to the base branch (F2), and a reader arriving at
`finishing-a-development-branch` from a Finish-skipping path knows to
flag missing bookkeeping instead of assuming a silent gap in this skill
(F2a).

None of these 8 fixes touch the structural reachability question
(F5/F6/F8/F11) or `executing-plans`' missing Finish step (F4) — those need
their own design and ship in later batches, per this spec's Context
section.

## Falsifiable Criteria

1. A direct read-through of `brainstorming/SKILL.md`'s scaffold-offer
   bullet confirms the new `.context.md` Format-block sentence and the
   reworded three-question list, both matching the Decision blocks above
   verbatim.
2. A direct read-through of `writing-plans/SKILL.md`'s Self-Review item 10
   confirms the new closing sentence, matching the Decision block above
   verbatim.
3. A direct read-through of `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`'s
   Mutation Check section confirms the new token-containment sentence,
   matching the Decision block above verbatim, and
   `docs/patterns/assert-on-a-token-the-context-cannot-supply.md` exists
   with the four required sections (Context, Pattern, Example,
   Originating lessons).
4. A direct read-through of `finishing-a-development-branch/SKILL.md`
   confirms: Step 7 recognizes `.claude/worktrees/` and states the
   native-tool-first preference; Option 2 contains the forge-confirmation
   sentence; the Overview contains the bookkeeping-responsibility
   sentence. All three match their Decision blocks verbatim.
5. A direct read-through of `subagent-driven-development/SKILL.md`'s
   Finish section confirms its opening sentence matches the Decision
   block above verbatim.
6. `grep -c "Format block verbatim" plugin/skills/brainstorming/SKILL.md`
   returns at least 1.
7. `grep -c "already supplies that token" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
   returns at least 1.
