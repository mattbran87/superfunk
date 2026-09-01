I ran the seven Spec Self-Review checks against the real sources rather than from memory. `docs/code-standards.md` and `docs/principles.md` don't exist in this repo, so I applied the self-contained/testable criteria directly, per the skill's fallback.

## Self-review found 8 issues

**Substantive — three**

**1. The backward-compatibility claim is false for the new record type.** The Decision says "the frozen on-disk format stays readable by every shipped version." That holds for the two new *keys*, but `state_of()` **raises** `InvalidTransitionError` on an unknown `type` (`src/taskq/state.py:52`), and both `audit()` (`src/taskq/audit.py:153`) and `taskq show` call it unguarded over every record. A shipped v0.3.0 `taskq audit` pointed at a file containing one `adopted` record doesn't skip it — it errors out on the whole file. Consequences hedges this ("can learn one new type through `state_of()`"), but the Decision states the flat version.

**2. Falsifiable Criterion 12 cannot fail.** It specifies calling `StateWriter.running()` on an unknown id — which is `tests/test_state_writer.py:79`, `test_running_without_a_submitted_record_raises`, already shipped and green with zero adoption code in the tree. Delete the entire `adopted` mechanism and criterion 12 still passes, so it can't be mutation-verified as the spec requires. It also doesn't match the Decision's own stated enforcement ("a test asserts that *adopting* without writing the `adopted` record raises"), which is a different test.

**3. Criterion 15 is unsatisfiable as written.** `src/taskq/queue.py` is exactly 681 lines right now (measured, `wc -l`). The Decision requires edits *inside* that file: `submit()` must compute and pass `args=`/`kwargs=` at the `self._writer.submitted(...)` call (`queue.py:307-314`), and `__init__` must gain `adopt=False` plus the adoption call. "No more than 681 lines" leaves zero headroom for changes the same spec mandates.

**Ambiguity — three**

**4. "criterion 4" names two different things.** The qualification rules under "What adoption takes" are numbered 1–5, and Falsifiable Criteria are numbered 1–16. Consequences says "Such a job fails criterion 4 above" meaning qualification rule 4 (non-null args), but Falsifiable Criterion 4 (`adopt=False` changes nothing) is also above it. The Decision's "criteria 4 and 5 below" and "criteria 3, 4, or 5" refer to different lists two sections apart.

**5. Criterion 3 is true or false depending on reading.** `render_show` dumps `json.dumps(record, sort_keys=True)` for the whole record (`src/taskq/cli/format.py:66`), so adding `args`/`kwargs` **does** change the rendered line for a `submitted` record — new keys, and `args` sorts before `args_repr`. "`taskq show` renders it as before" passes on the value reading and fails on the line reading.

**6. Criterion 13's failure mode is an unbounded hang.** The spec presents "the test hangs rather than passing quietly" as the safeguard, but `pyproject.toml` sets only `testpaths` — no pytest timeout, no `pytest-timeout` dependency — and `time.sleep` is lint-banned, so a regression stalls CI instead of failing it. It's also underspecified how a module imported during `Queue.__init__` reaches the Queue under construction, and whether the expected failure is a `_lock` self-deadlock or a `StateFileLockedError` from constructing a second Queue on an already-locked path.

**Consistency / completeness — two**

**7. The null-args rationale is narrower than the rule.** The rule fires whenever `classify_retryability` returns `False`; the reason given is "serializing arguments that already failed `json.dumps` would raise." Criterion 2's lambda fails on the *callable* (`retry.py:91`), not the arguments — those serialize fine and get discarded anyway. The rule may still be right; the stated reason doesn't reach it.

**8. No `Alternatives Considered` section.** The skill requires one in every spec recording a choice between approaches, and this one records at least three (constructor flag vs. `queue.adopt()`, `adopted` record vs. a writer special case, keeping `args_repr` vs. collapsing it). The constructor-vs-method comparison lives in Open Questions without a confidence level or named evidence. Caveat: none of specs 1–3 has this section either, so this may be a house-style call rather than a defect.

## Checks that came back clean

Every quote verified against its source with a fresh read: `README.md:90` (line number and wording both exact), both `classify_retryability` docstring quotes (`retry.py:79`, `:83`), `.context.md`'s "always pick loud" (line 18), and `ai-code-guidelines.md` rule 3, "Do not call user code while you hold a lock." The Context section's two measured facts hold: `queue.py` greps clean for `StateReader`/`replay`, and `StateWriter.submitted()` takes no `args`/`kwargs` (`state.py:84-93`). The `ALLOWED_TRANSITIONS[None] = {QUEUED}` and empty-`_last_state`-per-instance mechanism is exactly as described. Bug 014's measured output block matches the spec's Context block verbatim, `audit ok: False` line included. No placeholders, no TBDs. Scope is one implementation plan's worth.

One near-miss worth recording: `JobAlreadyRunningError` doesn't exist in `errors.py`, but bug 007 line 17 proposes it by that name and `project-definition.md:81` uses it the same way — the citation is legitimate.

The skill's step 7 says to fix these inline, but findings 1, 2, 3, and 6 each need a decision from you rather than a mechanical edit — what criterion 12 should actually assert, where the `queue.py` line ceiling should sit, whether to state old-reader incompatibility as a Consequence or add a guard to `state_of()`, and how criterion 13 should fail loudly. Want me to apply the mechanical fixes (4, 5, 7, and the Decision's compat sentence) and bring the other four back with options?
