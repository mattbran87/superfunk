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
