# Per-Task Outcome Capture — Design

**Date:** 2026-08-21
**Status:** Approved

## Context

A comparison against `github.com/kaanozhan/Frame` — an external spec-driven agentic-development tool — surfaced a real gap in `subagent-driven-development`. Frame's agents append 2-3 sentences to a per-feature `outcome.md` after each task: what shipped, what diverged from the plan, what to follow up on. That narrative persists across sessions.

`subagent-driven-development`'s "Complete the task" step already appends a terse ledger line per task — commit range and review status. But the ledger lives in the plan's workspace (`.superpowers/sdd/<plan-basename>/`), and `Finish` deletes that workspace once the branch ships (`rm -rf <workspace>` — git history becomes the record). The implementer's full report file, which holds its own narrative of what it did and any doubts it raised, dies with the workspace too. Nothing durable captures the implementer's own account of intent versus reality — only two other things survive: the ledger's terse commit-range line, and whatever a reviewer happened to catch as a defect.

That leaves a specific kind of signal uncaptured: an implementer's own judgment call that diverged from the plan but drew no reviewer finding — a simplification chosen, an assumption made, scope deliberately left out. `process-review` already synthesizes Catches, Misses, Friction, and Gaps from reviewer-side evidence (`process-reviews/notes.md`, git log) — it has no implementer-side evidence to draw on at all.

This spec scopes to `docs/superpowers/plans/` — the pipeline every sub-project this session actually used. `specs/<module>/<feature>/notes.md` (the feature-tracking system's own freeform notes file) stays out of scope; it exists but sees little real use today.

## Decision

- **New file per plan: `docs/superpowers/plans/<plan-slug>-outcomes.md`.** Created on the first task's completion, with a header:

  ```markdown
  # Outcomes — <plan filename>

  One entry per completed task: what shipped, what diverged from the
  plan, what to follow up on — in the implementer's own words, captured
  before Finish deletes the plan's workspace (and its full report files).

  <!-- entries below this line -->
  ```

  Each task appends `## Task <N>: <task name>` followed by its outcome note.

- **`implementer-prompt.md`'s Report Format gains a required Outcome field**, part of the same short (under-15-line) status contract already returned after every task and every fix round:

  ```
  - **Outcome (2-3 sentences):** What shipped, what diverged from the
    task brief, what to follow up on. State plainly when nothing
    diverged — e.g. "Shipped as planned; no divergence, no follow-ups."
  ```

  Every task reports this field, including one that went exactly to plan — matching this project's existing bias toward mandatory-but-terse checks (the Pseudocode section's `Skipped, reason` pattern) over an optional field that quietly degrades into "always skip." If a report omits it, the controller treats it as a missing required field, the same way it already would a missing Status or commit list, and asks the implementer to supply it before marking the task complete.

  A task that goes through fix rounds resends this field on every round's reply, since the contract already gets resent verbatim each round. The controller appends only the field's final value — the one reported at the round where the task actually completes — to the outcomes file. It reflects the task's whole journey, not just the first attempt.

- **`subagent-driven-development/SKILL.md`'s "Complete the task" step gains one instruction**, run alongside the existing ledger completion line: append the task's Outcome field to `docs/superpowers/plans/<plan-slug>-outcomes.md` as `## Task <N>: <task name>`, creating the file with its header the first time a task writes an entry.

  Git tracks the outcomes file; the ledger stays git-ignored, per its existing workspace-scratch status. The controller commits the outcomes file itself, directly, right after each append — the same pattern it already uses for other git-tracked bookkeeping (`process-reviews/tracker.md`, `lessons-learned.md`) at `Finish`, just running once per task instead of once per plan. This avoids adding a foreign-file instruction to every implementer dispatch prompt, which this project's own dispatch guidance already discourages (a dispatch describes one task, not accumulated session state).

- **`process-review/SKILL.md`'s Step 2 gains a companion step.** For each spec in the tracker's "Specs shipped since" list, derive its plan's slug by stripping `-design` from the spec's filename, then read `docs/superpowers/plans/<slug>-outcomes.md` if it exists — a spec shipped before this mechanism existed has no outcomes file, and that absence never counts as an error. Collect every entry reporting a real divergence or follow-up; skip terse "shipped as planned" entries, which carry no signal.

  Step 4's synthesis folds these into the existing four sections, adding no new section:
  - A divergence recurring across 2 or more reviewed specs joins **Misses**, the same recurrence threshold already applied to Catches.
  - A follow-up naming a concrete file and change joins **Recommendations** directly.
  - A follow-up too vague to act on yet joins **Gaps**, as a candidate needing more definition.
  - A one-off divergence with no recurrence and no concrete follow-up needs no mention, the same as a one-off Catch today.

## Falsifiable Criteria

1. A disposable `--plugin-dir` trial, seeded with a real 2-task plan (per this project's `seed-trial-fixtures-with-real-docs` pattern), runs `subagent-driven-development` end to end. Both implementer reports carry the required Outcome field. `docs/superpowers/plans/<slug>-outcomes.md` exists after Task 1 with the exact header format above, and gains a second `## Task 2:` entry after Task 2.
2. In the same trial, the task that ships exactly as planned still produces a non-empty entry ("Shipped as planned; no divergence, no follow-ups"), not a skipped one.
3. The outcomes file's git history shows one controller commit per task, immediately after each append — never left uncommitted at `Finish`.
4. A direct read-through (or trial) of the updated `process-review` confirms it derives a plan slug from a spec filename correctly, reads that plan's outcomes file, and tolerates a missing outcomes file without erroring.

## Consequences

Every task's status report grows by one required field, and every task completion writes one more file operation plus one more controller-made commit, for the outcomes file.

`process-review` gains a second evidence source. Its four output sections stay the same shape — outcomes-derived signal joins the same Misses/Recommendations/Gaps categories reviewer-derived signal already feeds, rather than growing the report format.

An outcomes file exists only for plans built after this mechanism ships. Every earlier plan's implementer narrative already died with its workspace — this spec does not recover it.

## Deferred

- `specs/<module>/<feature>/notes.md` (feature-tracking's own freeform notes file) — out of scope; revisit only if that pipeline sees real use.
- A dedicated "Divergences" section in `process-review`'s output — deferred until outcomes files exist and have real content to show whether the existing four sections hold up or need a fifth.
- Recovering or backfilling outcomes for plans shipped before this mechanism existed — not possible; Finish already deleted their report files.
