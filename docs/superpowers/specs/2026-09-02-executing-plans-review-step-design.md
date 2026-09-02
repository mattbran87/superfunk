# Executing-Plans Review Step — Design

**Status:** Approved
**User-Facing:** No

## Context

The second external trial's F4 finding
(`docs/superpowers/process-reviews/external-trial-taskq-findings.md`)
named two gaps in `superfunk:executing-plans`: no Finish bookkeeping, and
no review step. A parallel session's process-review independently
surfaced the same bookkeeping gap as Miss M4 and shipped it as
Recommendation R4 — `executing-plans/SKILL.md` now carries an eight-item
Step 3 ("Finish Bookkeeping") mirroring `subagent-driven-development`'s
Finish section: notes.md gate, spec Status flip, tracker append,
Recommendation checkbox, a verification pass, lessons capture, a version
bump, and a concept-index check.

Two pieces of F4's original finding remain unaddressed by R4:

1. **No review step.** Step 1's own point 3 still only asks the
   executing session to "Review critically - identify any questions or
   concerns about the plan" before starting — a one-time, pre-execution
   read, not a review of the finished branch. Nothing between Step 2
   (Execute Tasks) and Step 3 (Finish Bookkeeping) inspects the actual
   diff the tasks produced. `subagent-driven-development` dispatches a
   task reviewer after every task and a whole-branch reviewer at the
   end; `executing-plans` dispatches neither.
2. **No bug-tracking step.** R4's Step 3 has no equivalent of Finish's
   bug-tracking step, which files real-and-deferred parked findings to
   `docs/bugs/` before the workspace disappears. The original trial
   measured this concretely: SDD produced 6 filed bugs from its review
   loops; `executing-plans` produced zero, despite the inline run finding
   4 real defects of its own during the trial.

`executing-plans` documents itself as the platform-level fallback for
sessions without subagent access ("If subagents are available, use
`subagent-driven-development` instead"), but the trial itself chose it
for an unrelated, temporary reason — a rate limit mid-SDD run, not an
absence of subagents. A fix that always assumes no subagent access
misjudges that real case; a fix that always assumes subagent access
defeats the skill's stated purpose. The review step below detects which
condition holds and degrades accordingly.

## Decision

**A new step, "Step 2.5: Whole-Branch Review," gets inserted into
`plugin/skills/executing-plans/SKILL.md` between the current Step 2
("Execute Tasks") and Step 3 ("Finish Bookkeeping"):**

```markdown
### Step 2.5: Whole-Branch Review

After all tasks complete and verified, and before Step 3's bookkeeping,
review the whole branch — mirroring `subagent-driven-development`'s
Final Review, adapted for a session that may or may not have subagent
access:

1. **Documentation check:** If this plan traces to a design spec (named
   in the plan's Goal line or a task's commit trailer), run `python
   plugin/skills/documentation/scripts/check_docs.py <spec-file>
   <merge-base-sha> <head-sha>`. `NOT_APPLICABLE` or `ALREADY_UPDATED`:
   continue. `ACTION_NEEDED`: invoke superfunk:documentation's Step 2 to
   draft the README/CHANGELOG update and commit it before continuing. No
   design spec: skip this check.
2. **Attempt to dispatch a reviewer.** Try dispatching a subagent on the
   most capable available model, using superfunk:requesting-code-review's
   [code-reviewer.md](../requesting-code-review/code-reviewer.md), with
   `BASE_SHA` = the commit before Step 1 began and `HEAD_SHA` = the
   current commit.
3. **No subagent dispatch available:** perform the same review yourself,
   directly — read the full diff between those two commits and apply
   `code-reviewer.md`'s own rubric (plan alignment, code quality,
   architecture, testing, production readiness) and Output Format
   (Strengths, Issues by severity, Recommendations, Assessment) as your
   own direct assessment, not a dispatched subagent's report.
4. **Findings:** append one line per finding to
   `docs/superpowers/process-reviews/notes.md`
   (`- <YYYY-MM-DD> | Catch | Final review | <one-line finding>`), then
   fix all of them in one pass — not one fix per finding — and run
   exactly one scoped re-review of the fix diff (dispatched if possible,
   direct otherwise). Adjudicate any residual finding as
   `subagent-driven-development`'s Final Review does: park a contestable
   or non-load-bearing finding with a ruling, or stop and report to your
   human partner if it's load-bearing — with the same one-time exception
   for a regression the fix itself introduces (bounded to fire at most
   once, only for a defect the fix wave caused). There is no second fix
   wave for a finding the first wave simply failed to fix.
5. **Bug-tracking:** for each parked finding whose ruling calls it real
   rather than contestable, invoke superfunk:bug-tracking's Step 2 to
   record it in `docs/bugs/` before continuing — this is `executing-plans`'
   only opportunity to do so; nothing else in this skill preserves a
   deferred finding once the review above is done. No real-and-deferred
   parked findings: skip this step.

Only once this review is clean does Step 3 begin.
```

**Step 3's opening line changes** from "After all tasks complete and
verified, and before Step 4, perform..." to "After Step 2.5's review is
clean, and before Step 4, perform..." — so Step 3's own text states the
ordering unambiguously, not only the new step's placement.

## Alternatives Considered

**Always dispatch, never self-review** — rejected: `executing-plans`
exists specifically for sessions where dispatch can fail or never
exist; a design that always requires it contradicts the skill's own
stated purpose and leaves the no-subagent case exactly as unreviewed as
before this fix.

**Always self-review, never attempt dispatch** — rejected: the trial's
own invocation of `executing-plans` had subagents available (a temporary
rate limit, not a structural absence) — skipping dispatch unconditionally
would throw away review quality in the common case this skill actually
gets chosen for, per the trial.

**A lighter review (spot-check the diff, no formal rubric)** — rejected:
`code-reviewer.md` already exists and has proven itself as SDD's own
final reviewer template; reusing it exactly means `executing-plans`
produces the same shape of finding SDD does — comparable, not a lesser
tier of review because of which skill executed the plan.

## Consequences

`executing-plans` now reviews the branch it produces, closing the last
piece of F4 that R4 didn't reach. A plan executed inline with subagents
temporarily unavailable gets the same whole-branch review quality as one
executed via `subagent-driven-development`; a plan executed where
dispatch never existed as an option gets a rigorous direct review
instead of none. Real, deferred findings get a durable record in
`docs/bugs/` instead of disappearing with the session, closing the
trial's zero-bugs-filed measurement for this path.

This adds one more gate before `executing-plans` reaches Finish
bookkeeping — a plan with review findings takes longer to complete than
one that skipped review entirely. That trade holds intentionally: the
trial measured the previous zero-review path finding real defects on
its own tests, with nothing else catching or recording them.

## Falsifiable Criteria

1. A direct read-through of `executing-plans/SKILL.md` confirms Step 2.5
   exists between Step 2 and Step 3, worded identically to the Decision
   block above.
2. A direct read-through confirms Step 3's opening sentence now reads
   "After Step 2.5's review is clean, and before Step 4, perform..."
3. `grep -c "Step 2.5" plugin/skills/executing-plans/SKILL.md` returns at
   least 2 (the new heading plus Step 3's updated reference to it).
4. A disposable `--plugin-dir` trial executes a small plan via
   `executing-plans` with subagent dispatch available, and confirms a
   reviewer subagent gets dispatched, using `code-reviewer.md`'s template,
   before Step 3's bookkeeping runs.
5. A second disposable trial executes a small plan via `executing-plans`
   with subagent dispatch unavailable (or deliberately simulated as
   unavailable), and confirms the session performs the same review
   directly — producing Strengths/Issues/Assessment output — before Step
   3's bookkeeping runs.
