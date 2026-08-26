# Lessons Learned

Accumulated knowledge from completed plans. Captured at
`subagent-driven-development`'s Finish step for notable learnings —
specific enough to act on in a future session. Entries live under an
H2 category heading; the first Lesson on a new topic creates its own
heading.

## Workflow

### Cross-check a shared rule's restatements across every file a plan writes it into (2026-08-20-lessons-and-patterns-design)

When translating one design-spec rule into multiple target files within
the same plan (e.g. the same promotion rule written once for
`docs/code-standards.md` and again for `subagent-driven-development/SKILL.md`),
each restatement independently matched its own target file's needs but
diverged from the other's wording — the design spec itself states the
rule once, but paraphrasing it twice, in two separate plan tasks,
without comparing the two paraphrases to each other, let two different
framings of the same rule ship. Both needed a fix round to reconcile.
**Rule:** when a plan restates the same rule in more than one target
file, cross-check every restatement against every other restatement,
not just each one individually against the source spec.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/cross-check-shared-rule-restatements.md*

## Review

### Verify a code-quality finding against source intent and existing precedent before treating a literal rule-match as a defect (2026-08-20-checklist-construction)

Three separate code-quality reviews in this sub-project each flagged
something as a defect by applying a stated rule literally, without
first checking what the rule's source actually meant or whether the
identical pattern already shipped elsewhere without issue. None of
the three survived independent verification: a "5-9 item cap" read
as a floor when the source draft explicitly framed it as a ceiling;
a tagging-consistency complaint didn't hold once the compared
bullet's different context got read; a "needs concrete examples"
finding ignored two already-shipped instances of the identical
open-ended pattern. **Rule:** before treating a literal rule-match as
a real defect, check the rule's source intent and whether the same
pattern already shipped elsewhere without the same complaint — a
rule applied too literally, without that context, produces a false
positive as often as it catches a real gap.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/verify-against-precedent-before-flagging.md*

### When wiring a new reviewer check, verify the reviewer can actually see what it's asked to check (2026-08-21-hazard-signal-words)

A code-quality reviewer got a new instruction to check commit
messages for a severity trailer. The instruction shipped clean
through spec-compliance and its own code-quality review — but the
reviewer's actual data source, `scripts/review-package`, built its
"## Commits" section with `git log --oneline`, which truncates every
commit to its subject line. The trailer the reviewer was told to
check lives in the commit body. The check was unrunnable from day
one, and nothing caught this until a later review happened to trace
the data path instead of just reading the instruction's wording.
**Rule:** when wiring a new "check X" instruction into a reviewer,
confirm the reviewer's actual input (the diff, the review package,
whatever it reads) really contains X — a well-written instruction
pointing at data the reviewer never receives is a defect the
instruction's own wording won't reveal.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/verify-reviewer-can-see-what-it-checks.md*

## Testing

### A --plugin-dir trial fixture needs the real convention docs it's testing copied in, not just the scratch structure (2026-08-21-hazard-signal-words)

A live trial dispatched a scratch session to read `docs/ai-code-guidelines.md`
and `docs/code-standards.md` and apply their conventions — but the
scratch fixture never copied those files in, only a bare `README.md`.
The trial ran anyway and produced plausible-looking output (a hazard
comment, a commit trailer), but using generic conventions the AI
invented on its own, not the specific vocabulary the trial existed to
verify. The gap wasn't caught by the trial passing or failing — it
was caught by the AI itself reporting that the files it was told to
read didn't exist. This same requirement was already written down
once before, in an earlier sub-project's Testing section ("a
meaningful trial needs docs/ai-code-guidelines.md... copied into the
scratch fixture first"), and still got missed here. **Rule:** before
running any `--plugin-dir` trial that depends on a project convention
doc, copy that doc into the scratch fixture as part of building it —
check this explicitly, since a documented step already proved easy to
forget once.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/seed-trial-fixtures-with-real-docs.md*

### A --plugin-dir trial that tells the agent to hunt for a skill's own file breaks under a plugin name collision (2026-08-21-per-task-outcome-capture)

A live trial's prompt told a simulated implementer to locate and read
`implementer-prompt.md` on its own. It reported the file didn't exist
and improvised the task from scratch instead — its status report had
no Outcome field at all. The fork under test and the globally-cached
`superpowers` plugin share the same plugin name on disk, so a broad
file search had no principled way to prefer one over the other, and
resolved to the wrong copy. A direct diagnostic proved the fork's
content loads correctly: when told to use the Skill tool first and
then resolve a referenced sibling file "using whatever path resolution
you would naturally use," the agent opened the fork's own copy every
time, quoting content that only exists there. **Rule:** a
`--plugin-dir` trial that needs an agent to see a skill's own file
(not just a project doc already copied into the fixture) must tell it
to invoke the Skill tool first and resolve any referenced file
relative to the skill it just loaded — never tell it to Glob or
broadly search the filesystem, which has no way to prefer the fork
under test over an identically-named globally-installed plugin.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/resolve-skill-files-via-skill-tool-not-glob.md*

### A live trial priming a false belief needs a true A/B control to show an instruction actually changed behavior (2026-08-24-review-recommendations-followup)

A live trial claimed to verify that a new reviewer instruction ("re-read the cited doc before citing it") prevented a false finding: it primed the reviewer with a wrong claim about a doc's rule, and the reviewer correctly caught and rejected it. But the trial's own dispatch prompt coached the exact behavior under test ("follow the reviewer template's instructions about re-reading," "quote the exact current text ... read fresh from disk"), and the pre-edit template already told the reviewer to check the relevant topic. A genuine two-arm run — the same fixture, a coaching-free prompt, dispatched once against the plugin before the edit and once after — found both arms independently caught the planted error; the pre-edit reviewer did this unprompted. The instruction demonstrably added no detectable value in this scenario, something the original trial's "pass" could never have revealed, since it was structurally incapable of failing. **Rule:** a live trial meant to prove a new instruction changes behavior (not just that the instruction reads correctly and gets followed) needs a real control — the same fixture and a coaching-free prompt, run once against the pre-edit plugin and once against the post-edit plugin. A trial whose own dispatch prompt tells the agent to perform the behavior under test cannot fail, and a "pass" against that kind of prompt proves nothing about the instruction's actual effect.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/ab-test-live-trials-for-behavior-change.md*

### Follow this project's own outcomes-file mechanism when executing subagent-driven-development, or its own author misses it first (2026-08-24-review-recommendations-followup)

The per-task outcome capture mechanism shipped three days earlier in this session, wiring `subagent-driven-development`'s "Complete the task" step to require an Outcome field in every implementer report and to append it to a git-tracked outcomes file. Executing this sub-project's own plan, the controller dispatched implementers with custom prompts that never asked for an Outcome field and never created the outcomes file — missing the very mechanism this session had just built and reviewed. **Rule:** when dispatching an implementer subagent under `subagent-driven-development`, use `implementer-prompt.md`'s actual current Report Format section (which already names every required field) rather than reconstructing a report contract from memory or from an older mental model of the template — a mechanism this project ships into its own skill files applies to running this project's own skills, not only to the tasks those skills execute.

**Tags:** none yet — tags deferred.

*Pattern promoted retroactively after a second occurrence — see docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md*

### An explicit reminder does not stop controller-owned bookkeeping from being deferred; only a blocking gate does (2026-08-25-concept-index)

The controller received an explicit instruction at the start of this sub-project to follow the per-task outcome capture mechanism, specifically because it had missed the mechanism entirely one sub-project earlier. It missed it again: Tasks 1-3's outcomes entries were reconstructed after the fact, in one batched commit, from review history the entries claim came from the implementer's own real-time report — not genuinely captured per task, the way Tasks 4-6 correctly were once the controller noticed. The original Lesson's Rule (use the template's current Report Format instead of reconstructing from memory) does not explain this recurrence: the contract was known and named explicitly, and the step still got deferred. The shared root cause across both instances: outcomes capture is controller-owned bookkeeping with no downstream consumer that fails loudly if skipped — everything else the controller does (dispatching, review packages, task commits) has something that breaks visibly if missed; this doesn't, so it stays silently deferrable. **Rule:** for controller-owned bookkeeping with no loud downstream failure mode, do not rely on a reminder or an explicit instruction — require a mechanical, checkable gate before the next dependent action proceeds (e.g., confirm Task N's outcomes commit exists in git log before dispatching Task N+1's implementer). Visibility (stating a check as its own explicit line) is necessary but not sufficient on its own, as this same sub-project's own Finish-step design argued while the controller was concurrently failing to follow a different check that already met that visibility bar.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md*
