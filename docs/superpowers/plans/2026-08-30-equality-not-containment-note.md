# Equality-Not-Containment Note Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a closing sentence to `task-reviewer-prompt.md`'s Mutation Check flagging string comparisons using `in` (containment) where the plan or spec states an equality property.

**Architecture:** One sentence appended to one existing paragraph in one existing skill file, followed by one disposable `--plugin-dir` trial confirming the addition fires correctly. No code, no tests in the software sense — verification is direct read-back and live trial behavior.

**Tech Stack:** Markdown, disposable trial.

## Global Constraints

- The added sentence must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criterion 1).
- No file outside `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` gets modified.

---

## File Structure

Directory touched: `plugin/skills/subagent-driven-development/`. Checked for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`).

This plan creates no new files — the only edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` — append the equality-not-containment sentence to the Mutation Check section

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; the edit adds Markdown prose describing a reviewer instruction.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Add the equality-not-containment sentence

**Files:**
- Modify: `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the amended Mutation Check instruction every future task review follows. Task 2's live trial depends on this task's exact wording.

- [ ] **Step 1: Confirm the current closing sentence's exact text**

Run: `grep -n "pure smoke test, for example" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: one match, at line 89 (confirmed via direct read this session).

- [ ] **Step 2: Append the new sentence**

Change:
```markdown
    Skip this check only for a test with no clear guarded line to revert (a
    pure smoke test, for example) and say so.

    ## Part 1: Spec Compliance
```
To:
```markdown
    Skip this check only for a test with no clear guarded line to revert (a
    pure smoke test, for example) and say so. A related trap: a test
    comparing two strings with `in` (substring containment) instead of
    `==` can look like it asserts equality while accepting anything one
    string contains the other — if a comparison the plan or spec treats
    as an equality guarantee uses `in`, flag it even if its own mutation
    check passes, since containment can stay true across a mutation that
    breaks the equality the test actually meant to pin.

    ## Part 1: Spec Compliance
```

- [ ] **Step 3: Verify the addition landed**

Run: `grep -c "containment" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: `2` — the added text uses the word twice ("substring containment" and "since containment can stay true"), counted directly against the drafted text before finalizing this check, not assumed to appear once.

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/subagent-driven-development/task-reviewer-prompt.md
git commit -m "feat(skills): add equality-not-containment note to task-reviewer-prompt's Mutation Check"
```

---

### Task 2: Live trial and final verification

**Files:**
- No files modified — this task only verifies Task 1.

**Interfaces:**
- Consumes: the finished state of the file Task 1 touched.
- Produces: pass/fail evidence for the design spec's Falsifiable Criteria. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criterion 1 — the added sentence**

Run: `grep -A7 "pure smoke test, for example" plugin/skills/subagent-driven-development/task-reviewer-prompt.md`
Expected: text matching the Decision block's addition exactly.

- [ ] **Step 2: Build the containment-vs-equality fixture**

Set up a disposable fixture: a small module with a function claimed to satisfy an equality property (e.g., "the normalized URL displayed to the user equals the URL `open` navigates to"), and a test asserting this via `in` rather than `==`, where the actual values differ but one is a genuine prefix of the other (matching the trial's own `opened[0] in listing` shape).

Run:
```bash
claude -p --plugin-dir plugin --dangerously-skip-permissions "Follow the superfunk:subagent-driven-development skill's task-reviewer-prompt.md template's Mutation Check section directly (read the actual current text, don't rely on memory) to review this diff: [paste the fixture's function and test]. The spec states: 'the displayed URL must equal the URL open() navigates to.'" --add-dir <fixture-path>
```

Expected: the response flags the `in`-based comparison as failing to actually verify the stated equality property, citing the specific sentence in the Mutation Check that names this trap — independent of whether a direct-line mutation of the guarded code happens to also go red.

- [ ] **Step 3: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1 covers the spec's Decision (the added sentence). Task 2 covers the spec's Falsifiable Criteria. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** N/A — this task appends a sentence to an existing paragraph rather than adding a new sibling instruction alongside an existing one; no comparable adjacent instruction to mirror.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into Task 1's Step 2 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md`, `docs/patterns/verify-plan-commands-against-real-content.md`, and `docs/patterns/re-verify-quotes-against-source-before-citing.md` before writing this plan — this plan's own numeric claim (the `1` count) got verified against a real file baseline, and this plan quotes nothing from an external source beyond what the design spec's own self-review already verified fresh.

**8. Cross-section mechanism consistency:** Task 1 edits the Mutation Check section of `task-reviewer-prompt.md`, which the Output Format section's `### Mutation Check` subsection also references. Grepped the full file for every other mention of "containment," "equality," and "Mutation Check" beyond the paragraph being changed to confirm no other passage needs updating — found only the Output Format subsection, which already describes reporting mutated tests generically (file:line, reverted line, red/green) and doesn't need a specific containment callout to remain accurate. This plan traces to a design spec; this sentence documents that check per item 8's own instruction.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — this appends a sentence to an existing check without changing its step sequence. No worked example needs a currency check.

**10. Verified numeric expectations:** The `Expected:` count in this plan (Task 1 Step 3's `1`) was confirmed by running the actual grep against real file content before being written into this plan — not estimated.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

**12. User-facing documentation timing:** This spec carries `User-Facing: No` — this item doesn't apply.

**13. Hostile-input pass:** N/A — this plan's own tasks contain no code blocks implementing runtime logic; the edit is Markdown/documentation content, not a function processing external input.

**14. Stale-workaround grep:** N/A — this plan doesn't remove any limitation from superfunk itself; it adds a new reviewer check. No prior limitation's workaround text exists to search for.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-equality-not-containment-note.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
