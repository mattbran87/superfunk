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

### Writing a check for unverified numeric claims doesn't exempt the document writing it (2026-08-28-process-review-recommendations-batch-3)

This sub-project shipped three new Self-Review items specifically to catch predicted counts that never got run against real command output — closing a Miss from `documentation` and `superfunk-rebrand`. Building it, its own design spec and implementation plan hit the exact same failure shape three separate times before shipping: a predicted `grep -c "Finish:"` total assumed each new diagram node name contributes one matching line (wrong — reused node names span multiple edge lines), and a follow-up verification command's `-A 60` window assumed a diagram block's length without measuring it (wrong — the block spans 65 lines). All three got caught only by actually running the substitution and the command against real file content, not by any check that existed at the time — the mechanism being built didn't exist yet to catch its own construction. **Rule:** a document that specifies a check for a class of error doesn't inherit immunity from that same error while being written — apply the check's own discipline to the document shipping it, manually, before the mechanism exists to do it automatically.

**Tags:** none yet — tags deferred.

*No pattern promoted — this is a specific instance of the already-promoted `docs/patterns/validate-tools-against-real-project-data.md`-adjacent theme (verify before shipping, not after), recorded here since the target this time is a spec/plan's own numeric prose rather than a tool's runtime behavior; promote separately only if this exact self-referential shape (a mechanism-under-construction hitting the error it prevents) recurs.*

### The same self-referential blind spot recurred twice more, in two new shapes (2026-08-30-doc-timing-and-mutation-check)

The prior entry deferred promoting this theme to a Pattern, pending recurrence. It recurred twice in this sub-project alone: (1) a plan predicted `grep -c "User-Facing Documentation Timing"` would return 2, reasoning a new Self-Review item's text would repeat a section's exact heading phrase — it used different capitalization instead, so the real count was 1; (2) a plan's verification command used an anchored `grep -c "^## Mutation Check"` against a file that wraps its entire template in an indented code fence, so no heading ever sits at column 0 — the anchored pattern returned 0 matches every time, not a wrong count but a structurally guaranteed false negative. Both were caught by actually running the command against real file content before finalizing, not by assumption. **Rule:** verifying a plan's numeric or pattern-matching claims means running the exact command against the exact real content — not just checking the number "feels right," and not assuming a grep pattern that works on one file's structure works on another's (an anchored pattern is only as good as the assumption that the target text starts at column 0).

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/verify-plan-commands-against-real-content.md — this is the third and fourth instance of the same self-referential shape (documentation, batch-3 x3, this sub-project x2 — six total), past any reasonable threshold for "wait and see."*

### A search pattern can match a substring that's legitimately retained elsewhere (2026-08-30-rebrand-string-and-worktree-ignore)

A plan verifying a rebrand fix predicted `grep -c "superpowers"` on `session-start` would drop from 6 to 4 after fixing two lines. It only dropped to 5: the retained `using-superpowers` skill name is itself a substring match for "superpowers," including inside the now-correctly-fixed line's own `superfunk:using-superpowers` — so the bare substring count could never reach any clean target this fix controls. The actual fix was correct throughout; only the verification method was flawed. **Rule:** when a fix touches one occurrence of a string that's also a substring of something deliberately unchanged nearby, verify by checking the specific bad string's absence and the specific good string's presence — not by counting the shared substring, which can never isolate the two.

**Tags:** none yet — tags deferred.

*No pattern promoted — folded into the existing `docs/patterns/verify-plan-commands-against-real-content.md` as a further instance of "verify the exact command against real content," not a new distinct rule; added to that pattern's Example section.*

### A source document can change after you've already read it once (2026-08-30-pattern-template-and-convention-bootstrap)

Most of a design spec got written from an earlier read of the external trial findings report, treating its original D2/D3 finding ("the files don't exist anywhere," "the framework invented a format") as settled fact. The report carried a same-day correction, embedded in the same file, retracting both claims — the files exist in this dev repo, and nothing got improvised. The correction only surfaced because a tangential numeric claim ("25+ commits") got checked against the source text as part of routine verification, and reading enough context around the real number to fix it meant reading the correction too. Without that unrelated check, the spec would have shipped a fix for a finding that no longer described reality. **Rule:** a source document already read once, especially a living report another process might revise, needs a fresh full read immediately before building a second artifact from it — not a recall of what it said the first time.

**Tags:** none yet — tags deferred.

*No pattern promoted — a single instance so far, and the underlying cause (an external document getting corrected after this session's first read) is closer to an environmental fluke than a recurring design flaw; revisit if it recurs.*

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

### A tool's passing fixture-based unit tests don't prove it works against a real project's actual paths and text (2026-08-28-superfunk-rebrand)

`check_docs.py` shipped with 10 passing unit tests covering all three
branches (`NOT_APPLICABLE`, `ALREADY_UPDATED`, `ACTION_NEEDED`),
including a real-git-fixture test for the diff-based check. Its first
invocation against this project's own real spec and branch — not a
fixture — returned the wrong branch and then crashed outright. Two
gaps the fixtures never exercised: the fixture's doc file sat at the
fixture root, so the exact-bare-filename match never got tested
against a path like this project's own `plugin/README.md`; and the
fixture's spec text used only ASCII, so printing it never exercised
Python's default Windows stdout encoding against the em dashes and
arrows this project's specs use throughout. **Rule:** before treating
a tool's fixture-based test suite as proof it works, run it at least
once against the real project's own actual file paths and real
prose — a fixture built for coverage of the tool's branches, not for
resemblance to the target environment's real structure and text,
can pass every test while still failing on first real contact.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/validate-tools-against-real-project-data.md*

### Follow this project's own outcomes-file mechanism when executing subagent-driven-development, or its own author misses it first (2026-08-24-review-recommendations-followup)

The per-task outcome capture mechanism shipped three days earlier in this session, wiring `subagent-driven-development`'s "Complete the task" step to require an Outcome field in every implementer report and to append it to a git-tracked outcomes file. Executing this sub-project's own plan, the controller dispatched implementers with custom prompts that never asked for an Outcome field and never created the outcomes file — missing the very mechanism this session had just built and reviewed. **Rule:** when dispatching an implementer subagent under `subagent-driven-development`, use `implementer-prompt.md`'s actual current Report Format section (which already names every required field) rather than reconstructing a report contract from memory or from an older mental model of the template — a mechanism this project ships into its own skill files applies to running this project's own skills, not only to the tasks those skills execute.

**Tags:** none yet — tags deferred.

*Pattern promoted retroactively after a second occurrence — see docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md*

### An explicit reminder does not stop controller-owned bookkeeping from being deferred; only a blocking gate does (2026-08-25-concept-index)

The controller received an explicit instruction at the start of this sub-project to follow the per-task outcome capture mechanism, specifically because it had missed the mechanism entirely one sub-project earlier. It missed it again: Tasks 1-3's outcomes entries were reconstructed after the fact, in one batched commit, from review history the entries claim came from the implementer's own real-time report — not genuinely captured per task, the way Tasks 4-6 correctly were once the controller noticed. The original Lesson's Rule (use the template's current Report Format instead of reconstructing from memory) does not explain this recurrence: the contract was known and named explicitly, and the step still got deferred. The shared root cause across both instances: outcomes capture is controller-owned bookkeeping with no downstream consumer that fails loudly if skipped — everything else the controller does (dispatching, review packages, task commits) has something that breaks visibly if missed; this doesn't, so it stays silently deferrable. **Rule:** for controller-owned bookkeeping with no loud downstream failure mode, do not rely on a reminder or an explicit instruction — require a mechanical, checkable gate before the next dependent action proceeds (e.g., confirm Task N's outcomes commit exists in git log before dispatching Task N+1's implementer). Visibility (stating a check as its own explicit line) is necessary but not sufficient on its own, as this same sub-project's own Finish-step design argued while the controller was concurrently failing to follow a different check that already met that visibility bar.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md*

### A trial confirming a trigger doesn't fire must not hand the agent its own answer (2026-08-25-concept-index)

Two Falsifiable Criteria in this session's specs verified a trigger's negative case — that it correctly does NOT fire — with a trial whose own dispatch prompt named the trigger paragraph and stated the answer directly: review-recommendations-followup's Falsifiable Criterion 2 told the agent which instruction governed the outcome, and concept-index's Falsifiable Criterion 3 told the agent outright that nothing crossed a boundary before asking it to confirm the trigger skipped. Both trials returned a "correctly skipped" result that proved only that the agent could read a scenario it had already been handed the answer to, not that the trigger logic itself would have discriminated a real non-crossing from a crossing on its own. **Rule:** a trial verifying a trigger correctly does NOT fire must present the negative case as a scenario only — never name the specific trigger paragraph or state the expected answer in the prompt — so the agent's own evaluation, not the prompt's coaching, produces the result.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/ab-test-live-trials-for-behavior-change.md*

### Building a gate against a failure mode doesn't stop you from committing that failure mode while building it (2026-08-26-process-review-recommendations-batch-2)

This sub-project shipped a mechanical gate specifically to catch notes.md logging being deferred — the grep-and-commit check in `subagent-driven-development/SKILL.md`'s Complete-the-task step. In the same sub-project's own execution, Task 3's fix-round notes.md entry landed eight minutes after Task 3 was marked complete, batched together with Task 4's own finding instead of committed on its own — the exact failure shape the new gate exists to prevent. A final whole-branch review's timestamp analysis caught it; the gate itself did not, because the gate was not yet built when Task 3 ran. Separately, the same review observed that a gate whose precondition is checkable only from the controller's own recollection (e.g., "confirm X before continuing") will keep needing sharper enforcement, while a gate whose precondition is a fact in git history (a specific commit exists) is closer to self-enforcing and doesn't need a gate of its own. **Rule:** verify a new gate's own real-world adherence with git timestamps before trusting it shipped correctly, and prefer a gate whose precondition is a checkable git fact over one that asks the controller to "confirm" or "check" from memory.

**Tags:** none yet — tags deferred.

*No pattern promoted for the git-checkable-preconditions half of this Rule — folded directly into `docs/patterns/gate-the-next-dispatch-on-outcomes-bookkeeping.md`'s existing numbered list instead of a new Pattern file. The verify-with-timestamps half stays a Lesson only, not yet promoted: one instance so far, revisit if it recurs.*

### A newly-shipped cross-section check doesn't apply itself to the fixes that ship it (2026-08-26-cross-section-mechanism-consistency)

This sub-project shipped a check (writing-plans Self-Review item 8, and a re-review carve-out) specifically to catch a fix to one part of a document leaving another part describing the same mechanism contradicted. The sub-project's own final whole-branch review found its shipped carve-out did exactly that: `re-review-prompt.md`'s own Scope section, and a sibling line in `subagent-driven-development/SKILL.md`, both stayed unqualified after the carve-out shipped an exception to them. A first fix wave reconciled one contradicting line per file — then a scoped re-review of that fix wave found a second, same-shape contradiction still standing in each of the same two files (the Red Flags table's "go to the ledger, not the loop," and the prompt's own opening "nothing else"). Both new items 8 and the carve-out apply automatically inside the workflows they instrument (a plan's Self-Review, a dispatched re-review) — but the controller's own hand-edits during a final-review fix wave sit outside both workflows, so nothing prompted the controller to run the same grep-and-read discipline against its own diff. **Rule:** when hand-fixing content that describes a routing, trigger, or lifecycle mechanism — including fixes to the cross-section check's own shipped text — deliberately re-apply the check's own grep-and-read step to the fix itself, and expect the first pass to close only the one contradiction that prompted it; budget for a re-review round to catch what it missed.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/self-apply-cross-section-check-to-hand-fixes.md*

### A Deferred item that survives two consecutive sub-projects on the same mechanism needs an explicit decision, not a third deferral (2026-08-27-cross-section-sibling-scope)

The design spec for `cross-section-mechanism-consistency` deferred trial coverage for the negative (correctly-does-not-fire) case, reasoning the cost asymmetry favored testing the positive cases first. This sub-project — extending the same two mechanisms one clause further — deferred the identical gap again, for the identical reasoning, without noting the gap had already survived one full extension untouched. Applying the self-apply-cross-section-check-to-hand-fixes Pattern worked cleanly this time (the final review found no self-referential contradiction), which shows a Deferred item can coexist with an otherwise-clean sub-project indefinitely: nothing about "the mechanism works" forces anyone to revisit what it still doesn't test. **Rule:** when a Deferred item from one spec still applies, unresolved, to a second spec extending the same mechanism, treat the recurrence itself as the trigger — either resolve it now or record an explicit reason it stays deferred a further time, rather than re-copying the same bullet forward silently.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/escalate-deferred-items-on-second-recurrence.md*

### When subagent dispatch is unavailable, the review discipline still applies directly (2026-08-27-finish-bookkeeping-gate)

This session's Agent-tool subagent spawn limit (200 of 200) was reached mid-execution, before Task 1 could be dispatched to an implementer subagent. Rather than skip the two-stage spec-compliance and code-quality review subagent-driven-development normally requires, the controller performed both checks directly: comparing the shipped diff word-for-word against the design spec's Decision block, and independently grepping sibling files for any restatement needing reconciliation, exactly as a dispatched reviewer's prompt would have instructed. Both live trials still ran normally, since `claude -p --plugin-dir` invocations are separate CLI processes, not Agent-tool subagents, and don't draw from the same budget. **Rule:** subagent dispatch is a delivery mechanism for the review discipline, not the discipline itself — when dispatch is unavailable, perform the same explicit, evidence-based checks directly rather than treating their absence as license to skip review.

**Tags:** none yet — tags deferred.

*No pattern promoted — one instance so far, and the underlying constraint (a session-level spawn limit) is infrastructure, not a recurring design flaw; revisit if it recurs.*

### A gate's precondition can be silently unmet without the gate ever noticing (2026-08-27-cross-section-negative-case-trials)

The Finish bookkeeping gate (shipped one sub-project earlier) checks off a process-review Recommendation by finding a `review-after-*.md` reference in a spec's Context section. This sub-project's own design spec, closing the review's second Recommendation, first cited only the two intermediate specs that had deferred the gap — never the review file itself, since the citation felt redundant while writing the Context section by hand. The gate would have silently reported "no review file named: skip this step," treating an uncited Recommendation exactly like a spec with none to close, rather than flagging a likely-missing citation. Caught only because the controller re-read the spec once more before running Finish, not because any check forced the read. **Rule:** a mechanical gate that keys off a specific citation existing is only as reliable as the discipline that puts the citation there in the first place — when a spec closes a process-review Recommendation, verify its Context literally names the `review-after-*.md` file, not just the intermediate specs the gap traveled through, before trusting the gate to catch it later.

**Tags:** none yet — tags deferred.

*No pattern promoted — this is a specific instance of the already-promoted `docs/patterns/self-apply-cross-section-check-to-hand-fixes.md`-adjacent theme (a mechanism's blind spot found in its own use), recorded in `2026-08-27-finish-bookkeeping-gate-design.md`'s Deferred section for now; promote only if a future spec repeats the same missing-citation shape.*

### A worked example illustrating a process goes stale every time that process gains a new step, and nothing re-checks it (2026-08-27-bug-tracking)

`subagent-driven-development/SKILL.md`'s Example Workflow section walks through the whole plan-to-push flow, including a Finish segment ending "Final reviewer: All requirements met... [Delete this plan's workspace]." `per-task-outcome-capture` once found and fixed this same example going stale after adding the outcomes-file step. Since then, five more additions to Finish — the spec-Status flip and tracker update, the Recommendation-checkbox step, the notes.md gate, and now this sub-project's bug-tracking step — each shipped without anyone revisiting the example, because no task in any of those plans touched the Example Workflow section itself, and nothing prompts a check of illustrative prose when the process it illustrates changes. **Rule:** a worked example demonstrating a multi-step process needs its own explicit check whenever a plan adds a step to that process — not just a check that the new step's own instructions are self-consistent, but a check that any worked example elsewhere in the same file still shows the real sequence. A plan task that adds a Finish step should ask "does the Example Workflow need updating too?" as its own line item, not assume File Structure's silence about that section means nothing to check.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/refresh-worked-examples-when-their-process-changes.md — this is the sixth instance of the same shape (one fix, then five more additions that never revisited it), past any reasonable threshold for "wait and see."*

### A required template section survives unenforced when the tool that writes documents never checks its own output against its own template (2026-08-28-documentation)

`writing-plans/SKILL.md`'s required Plan Document Header has included a `## Global Constraints` section since before this fork existed. Every plan written this entire session omitted it — dozens of plans, across every sub-project — because `writing-plans`' own 9-item Self-Review checks spec coverage, placeholders, type consistency, pseudocode, sibling parity, rule restatement, lessons-learned, cross-section consistency, and worked-example currency, but never checks a plan's own header against the template the skill itself requires. The omission surfaced only by accident, while re-reading the header template for an unrelated reason during this sub-project's own plan self-review. **Rule:** when a skill's own instructions define a required document structure (a header template, a required field, a mandatory section), that skill's Self-Review needs an explicit item checking the produced document against that structure — the same way item 8 checks cross-section consistency and item 9 checks worked-example currency, but for the document's own required shape rather than its content.

**Tags:** none yet — tags deferred.

*Pattern promoted — see docs/patterns/self-review-checks-own-required-template.md — the rule applies broadly (any skill defining a required structure needs this check), independent of whether this specific gap ever recurs.*
