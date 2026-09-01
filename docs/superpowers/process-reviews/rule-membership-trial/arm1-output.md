I ran the Spec Self-Review's seven checks against the committed spec, verifying every citation and count against the actual sources rather than against what the spec said about them.

## What the seven checks produced

**Placeholders (1):** clean. No TBD, no TODO, no empty section.

**Numeric-claim verification (6) — one real defect.** Criterion 15 read "`queue.py` holds no more than 681 lines." `wc -l` says `src/taskq/queue.py` is **exactly 681 lines today**, so the criterion allowed zero growth — while the Decision requires `Queue.__init__` to gain an `adopt` keyword and a call into the new module. The criterion was unsatisfiable by the spec's own design. Raised the cap to 700 and said explicitly what the 19 lines are for.

**Quote and source-freshness verification (7):** all clean, which is worth stating since it was the check most likely to fail. Verified against source: `README.md:90` (the sentence does start there), `classify_retryability`'s "a tuple argument comes back as a list" (`retry.py:83`), `.context.md`'s "When you face a choice between the two, always pick loud" (line 17–18), concurrency rule 3 "Do not call user code while you hold a lock" (`ai-code-guidelines.md:35`), the `_lock -> _cond` nesting being load-bearing (`.context.md:59`), `ALLOWED_TRANSITIONS[None]` permitting only `QUEUED`, `submitted()` taking no `args`/`kwargs`, `queue.py` referencing neither `StateReader` nor `replay`, and the ruff `banned-api` entry. The Context section's measured output block matches bug 014's, which is its source.

**Internal consistency (2) — two defects.**
- The signature block declared `args: list[Any]` while the prose two paragraphs later says a non-retryable job writes `args: null`. Now `list[Any] | None`.
- The spec claimed "the frozen on-disk format stays readable by every shipped version." That is true of the two added keys and false of the `adopted` record type: `state_of()` **raises** `InvalidTransitionError` on an unknown type, and `audit.py` calls it on every record. A pre-spec-4 `taskq audit` or `show` pointed at a file containing an `adopted` record errors out. Scoped the claim to the keys and recorded the real consequence — the format is now versioned one-way.

**Ambiguity (4) — one defect.** Nothing said which `max_attempts` an adopted job runs under. `max_attempts` is a per-`submit()` argument recorded on the record (default 3), and the adopting `Queue` has its own `RetryPolicy` — two defensible readings. Picked one: the record's value wins, the adopting run's policy governs backoff only.

**Enforcement (5) — one gap.** The "adoption goes in a new module" decision existed *only* in criterion 15, never in the Decision section. Folded the rationale into the criterion. The new `max_attempts` rule got criterion 17 so it isn't enforced by goodwill either.

**Scope (3):** holds as one plan. `taskq retry`, bug 012 and bug 007 are already pushed out explicitly.

## One thing outside the seven checks

The spec had no `Alternatives Considered` section, which the skill requires of any spec recording a choice between approaches — and this one records three. Its Open Questions section was doing that job informally, listing settled decisions as if open. Added the section with the three real choices (opt-in vs. automatic, constructor flag vs. `queue.adopt()`, refusing vs. adopting `running` jobs), each with confidence and evidence, and trimmed the open question that had been absorbed to the part that is genuinely still open — how a caller learns the adoption count.

Six defects total: one unsatisfiable criterion, two internal contradictions, one ambiguity, one unenforced decision, one missing required section. Fixed inline and committed as `8f14506`.

Two notes on the skill itself: its self-review steps 6 and 7 point at `docs/patterns/verify-plan-commands-against-real-content.md` and `docs/patterns/re-verify-quotes-against-source-before-citing.md`, and neither exists — `docs/patterns/` holds only `measure-claims-before-writing-them-down.md` and `mutation-verify-load-bearing-tests.md`. I ran both checks from the step text directly. Also, per the skill this self-review is followed by the user-review gate, so: the spec is at `docs/superpowers/specs/2026-09-01-taskq-adoptable-records-design.md` — worth your read before anything downstream, particularly the `max_attempts` call, since I picked that reading rather than asking.
