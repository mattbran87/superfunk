# Spec Self-Review — `2026-09-01-taskq-adoptable-records-design.md`

Four findings. One blocks implementation.

---

## 1. BLOCKING — the qualification list admits a member that violates its own stated intent

*(step 2, rule-membership check)*

The spec's stated intent, in its own words:

> "This spec draws the line at work that **provably never started**."

The rule that implements it (Decision → *What adoption takes*, criterion 1):

> "Its last record puts it in `QUEUED` — a `submitted`, `queued`, or `adopted` record."

Grepping every producer of each member:

| Member | Producer | Started? |
|---|---|---|
| `submitted` | `Queue.submit()` — `queue.py:284` | never started ✓ |
| `adopted` | this spec, `attempt: 0` | never started ✓ |
| **`queued`** | **`queue.py:634`, the retry path** | **already ran N attempts ✗** |

`queued` has exactly one producer, and it is inside the failure handler:

```python
if retrying:
    job.state = JobState.QUEUED
    self._writer.queued(job_id, attempt=job.attempt + 1, delay=delay)
```

`StateWriter.queued`'s docstring (`state.py:109`) confirms it: *"Record the retry engine returning a job to the queue."* A `queued` record is only ever written after an attempt executed and raised.

**This is reachable, and it's the common crash shape.** Run submits a job → attempt 1 raises → `queued` written with a backoff delay → process killed during the backoff window. Last record is `queued`. It passes all five qualification criteria (the earlier `submitted` record still carries `args`/`kwargs`/`retryable`), so adoption takes it.

Four consequences:

- **`attempt: 0` records a false fact.** The job reached attempt N.
- **`taskq status`/`show` report the wrong number.** `audit.py:155-157` keeps the attempt from the most recent record carrying an int — the `adopted` record's `0` overwrites the real count.
- **The retry budget resets.** `retry.py:63` is `if attempt >= max_attempts: return False`. An adopted job restarts at 0, so it gets `max_attempts` fresh attempts on every adoption. Crash-and-adopt in a loop retries without bound — CLAUDE.md's "a job must not retry forever."
- **The backoff is discarded.** The `queued` record carries `delay`; `queue.py:640` honours it via `not_before=`. The spec's adoption publishes to the `ReadyQueue` with no such qualifier, so the job re-runs immediately.

It also contradicts the spec's own Open Question 3, which treats this as hypothetical:

> "If a later spec **relaxes that** and adopts jobs mid-backoff, the field gains meaning and the criteria above need revisiting."

Criterion 1 already relaxed it. And nothing catches this: criteria 8–11 test refusals for `running`, missing args, unresolvable `func`, and `retryable: false`. No criterion exercises a `queued`-last job in either direction — so whichever behaviour ships, it ships untested. That's the wrong-member-added-silently hazard exactly.

Two ways out, your call: drop `queued` from criterion 1 (matches the stated intent, matches `attempt: 0`, smallest change), or admit it deliberately — then `adopted` must carry the real attempt number and the recorded `delay`, and Open Question 3 needs resolving now rather than deferring.

## 2. Forward-compatibility overclaim on the new record type

*(step 2, internal consistency)*

Decision says the format change is safe because readers ignore unknown keys — true for `args`/`kwargs`. Consequences then extends the claim to the new record type:

> "every shipped reader ignores unknown keys **and can learn one new type through `state_of()`**"

An *already-shipped* reader cannot. `state.py:52` raises on an unrecognized type, and `audit()`'s own docstring documents the blast radius: *"Raise `InvalidTransitionError` when a record's `type` field is not one of the types `state_of()` recognizes."* A spec-3 `taskq` binary pointed at a file containing `adopted` records crashes rather than degrading. Adding keys is backward-compatible; adding a record type is a breaking format change for older readers. Consequences should say so.

## 3. Nonexistent error class — fixed inline

Scope named `bug 007's JobAlreadyRunningError`. No such class exists (`errors.py` defines `TaskqError`, `StateFileLockedError`, `StateFileCorruptError`, `InvalidTransitionError`, `JobNotFoundError`). Bug 007 is about `cancel()` raising `JobNotFoundError` where its docstring promises `InvalidTransitionError`. Corrected in the file.

## 4. "one criterion per rule" doesn't hold

*(step 5, enforcement check)*

> "criteria 8 through 11 below each supply one disqualifying record and assert it survives un-adopted, **one criterion per rule**."

Five rules, four criteria: 8→rule 1, 9→rule 4, 10→rule 5, 11→rule 3. Rule 2 has none. The spec justifies that separately ("true by construction rather than by check"), so the gap is real but defensible — the sentence just overstates coverage. Left as-is pending finding 1, which changes this list.

---

**Verified clean:** no placeholders or TBDs; scope holds for a single plan; `README.md:90` quoted exactly; `.context.md`'s "always pick loud" quoted exactly (line 18); `classify_retryability`'s "a tuple argument comes back as a list" quoted exactly (`retry.py:83`); `ai-code-guidelines.md` concurrency rule 3 is "Do not call user code while you hold a lock" as cited; `queue.py` is **681** lines, so criterion 15's threshold is a real no-growth tripwire; `queue.py` references neither `StateReader` nor `replay`, confirming the Context claim; bugs 006 and 012 described accurately.
