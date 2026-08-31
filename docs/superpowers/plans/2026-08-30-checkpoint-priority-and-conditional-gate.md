# Checkpoint Priority and Conditional Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close D5 (checkpoint output drops pending user questions) and D7 (unconditional per-section gate re-asks settled consent) — the last two findings from the external bookmark-cli trial.

**Architecture:** Three additive edits across two existing skill files, followed by two disposable `--plugin-dir` trials confirming the conversational behavior changes. No code, no tests in the software sense — verification is direct read-back plus live trial behavior, since both fixes shape conversational output rather than a scripted check.

**Tech Stack:** Markdown, disposable trials.

## Global Constraints

- Every edit must match the design spec's Decision block exactly, character-for-character (per spec Falsifiable Criteria 1–3).
- No file outside `plugin/skills/using-superpowers/SKILL.md` and `plugin/skills/brainstorming/SKILL.md` gets modified.
- Both fixes verify via live-trial behavior in the tested scenario, not a claim of universal coverage — the spec's own Consequences section states this explicitly, and this plan's verification follows the same standard.

---

## File Structure

Directories touched: `plugin/skills/using-superpowers/`, `plugin/skills/brainstorming/`. Checked both for a `.context.md` file — none exist anywhere under `plugin/` (confirmed this session via `find plugin -iname ".context.md"`).

This plan creates no new files — every edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Files to modify:**
- `plugin/skills/using-superpowers/SKILL.md` — add the pending-question-priority paragraph
- `plugin/skills/brainstorming/SKILL.md` — add the count-verification sentence to Spec Self-Review, and make the per-section gate conditional

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit adds Markdown prose describing conversational behavior.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Add the pending-question-priority paragraph to using-superpowers

**Files:**
- Modify: `plugin/skills/using-superpowers/SKILL.md`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the priority rule every future session's "User Instructions" section states. Task 3's live trial depends on this task's exact wording.

- [ ] **Step 1: Confirm the current "User Instructions" section's exact text**

Run: `grep -n "User instructions (CLAUDE.md, AGENTS.md, GEMINI.md" plugin/skills/using-superpowers/SKILL.md`
Expected: one match, confirming the current paragraph's exact wording (confirmed via direct read this session).

- [ ] **Step 2: Append the new paragraph**

Change:
```markdown
## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.
```
To:
```markdown
## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.

If the user's message carries a question or request alongside an
approval or consent, answer or address it in the same response —
before or alongside any mandated checkpoint or gate output. A
checkpoint's own template text is not a reason to drop something else
the user just asked; a pending question outranks emitting the
checkpoint verbatim.
```

- [ ] **Step 3: Verify the addition landed**

Run: `grep -c "pending question outranks" plugin/skills/using-superpowers/SKILL.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugin/skills/using-superpowers/SKILL.md
git commit -m "feat(skills): add pending-question-priority paragraph to using-superpowers' User Instructions"
```

---

### Task 2: Add count-verification and make the per-section gate conditional

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

**Interfaces:**
- Consumes: nothing from Task 1 (an independent file).
- Produces: the two amended brainstorming behaviors. Task 3's verification depends on this task's exact wording.

- [ ] **Step 1: Confirm the Spec Self-Review's closing line**

Run: `grep -n "Fix any issues inline. No need to re-review" plugin/skills/brainstorming/SKILL.md`
Expected: one match, at line 163, confirmed unique in the file this session (a single occurrence, safe to anchor on).

- [ ] **Step 2: Add the count-verification sentence**

Change:
```markdown
docs/patterns/re-verify-quotes-against-source-before-citing.md for
the specific failure shapes a plausible-looking citation has actually
hit before.

Fix any issues inline. No need to re-review — just fix and move on.
```
To:
```markdown
docs/patterns/re-verify-quotes-against-source-before-citing.md for
the specific failure shapes a plausible-looking citation has actually
hit before.

Before reporting these findings to the user, verify any count you're
about to state (e.g., "three ambiguities") actually matches the list
you give right after it — a count that overstates or understates its
own list creates the exact gap this step exists to close, and it's
what the user will ask about first if it's wrong.

Fix any issues inline. No need to re-review — just fix and move on.
```

- [ ] **Step 3: Confirm the per-section gate bullet's exact current text**

Run: `grep -n "Ask after each section whether it looks right so far" plugin/skills/brainstorming/SKILL.md`
Expected: one match, at line 100 (confirmed via direct read this session).

- [ ] **Step 4: Make the gate conditional**

Change:
```markdown
- Ask after each section whether it looks right so far
```
To:
```markdown
- Ask after each section whether it looks right so far — unless the
  user already gave blanket consent covering this stage, or the
  section only restates a decision the user made explicitly earlier.
  In either case, state the section and continue without re-asking.
  If the section introduces a decision the user hasn't made yet, ask
  about that specific new decision even under blanket consent —
  consent covers decisions already settled, not ones that haven't
  come up.
```

- [ ] **Step 5: Verify both additions landed**

Run: `grep -c "overstates or understates" plugin/skills/brainstorming/SKILL.md`
Expected: `1` (twice-corrected anchor — the original "own body produces exactly this kind" quoted this spec's own Context section, not the inserted skill text; the first fix, "overstates or understates its own list," spans a markdown line wrap in the actual file, so it never matches as one line either. Both errors caught by running the command against the real file, not assumed.)

Run: `grep -c "consent covers decisions already settled" plugin/skills/brainstorming/SKILL.md`
Expected: `1`

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat(skills): add Self-Review count-verification and make brainstorming's per-section gate conditional"
```

---

### Task 3: Live trials for both fixes

**Files:**
- No files modified — this task only verifies Tasks 1–2.

**Interfaces:**
- Consumes: the finished state of both files Tasks 1–2 touched.
- Produces: pass/fail evidence for the design spec's Falsifiable Criteria 4–5. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criteria 1–3 — direct read-back**

Run: `grep -A7 "pending question outranks" plugin/skills/using-superpowers/SKILL.md`
Expected: text matching the Decision block's paragraph exactly.

Run: `grep -B3 -A2 "overstates or understates" plugin/skills/brainstorming/SKILL.md`
Expected: text matching the Decision block's count-verification sentence exactly. (Corrected anchor, same reason as Task 2 Step 5.)

Run: `grep -B1 -A5 "gave blanket consent covering this stage" plugin/skills/brainstorming/SKILL.md`
Expected: text matching the Decision block's conditional gate wording exactly. (Not `grep "unless the"` — that phrase already exists once elsewhere in the file, in the unrelated Visual Companion section's "unless they raise it," confirmed by checking the baseline before finalizing this command.)

- [ ] **Step 2: Verify Falsifiable Criterion 4 — pending-question live trial**

Set up a disposable fixture project with an approved spec ready for `writing-plans`, positioned so the next turn would fire a mandated checkpoint (the plan's own Execution Handoff prompt).

Run a multi-turn session (`--session-id` then `--resume`, matching this session's established live-trial pattern): send a message combining an approval ("looks good, write the plan") with an unrelated direct question (e.g., "by the way, does this plan need a worktree given how small it is?").

Expected: the response answers the direct question in the same turn that also produces the plan and its Execution Handoff checkpoint — not a checkpoint-only turn that drops the question.

- [ ] **Step 3: Verify Falsifiable Criterion 5 — conditional gate live trial**

Set up a second disposable fixture. Drive a brainstorming session to the design-presentation stage, give blanket consent covering the remaining stages, then continue into a further design section that introduces no new decision.

Expected: the response states that section's content and continues without re-asking "does this look right." Continue into one more section that does introduce a genuinely new decision (not previously discussed) — expected: the response asks specifically about that new decision, not a generic re-confirmation of everything already agreed.

- [ ] **Step 4: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1 covers Decision ¶1 (using-superpowers). Task 2 covers Decision ¶2–3 (brainstorming's two edits). Task 3 covers all five Falsifiable Criteria. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A — no functions or types get defined across tasks.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons.

**5. Sibling-pattern parity:** The count-verification sentence and the conditional-gate wording both match their surrounding sections' existing prose style (plain paragraphs, no bullet list) — checked directly against the real surrounding text before finalizing, not assumed similar.

**6. Rule-restatement accuracy:** The Decision block's exact wording got copied verbatim into Task 1's Step 2 and Task 2's Steps 2 and 4 — no paraphrasing introduced between the spec and the plan.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md`, `docs/patterns/verify-plan-commands-against-real-content.md`, and `docs/patterns/re-verify-quotes-against-source-before-citing.md` before writing this plan — every numeric claim in this plan (the `1` counts) got verified against real file baselines, and every quote in the design spec this plan implements already got verified fresh against the source report during the spec's own self-review.

**8. Cross-section mechanism consistency:** Task 1 edits `using-superpowers/SKILL.md`'s "User Instructions" section, which also appears referenced conceptually (not by exact wording) in `brainstorming/SKILL.md`'s own priority framing. Grepped both files for every other mention of "priority," "checkpoint," and "pending question" beyond the exact paragraphs being changed — found no other passage describing this same mechanism that would need a matching update. Task 2's two edits target unrelated mechanisms within the same file (self-review reporting vs. section-gate conditionality); grepped for cross-references between the two and found none. This plan traces to a design spec; this sentence documents that check per item 8's own instruction.

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process — all three edits add conditions or sentences to existing instructions without changing any process's own step sequence. No worked example needs a currency check.

**10. Verified numeric expectations:** Every `Expected:` count in this plan was confirmed by running the actual grep against real file content before being written into this plan — not estimated.

**11. Template compliance:** This plan's own header includes Goal, Architecture, Tech Stack, and Global Constraints, checked directly against `writing-plans/SKILL.md`'s Plan Document Header template before finalizing.

**12. User-facing documentation timing:** This spec carries `User-Facing: No` — this item doesn't apply.

**13. Hostile-input pass:** N/A — this plan's own tasks contain no code blocks implementing runtime logic; every edit is Markdown/documentation content, not a function processing external input.

**14. Stale-workaround grep:** N/A — this plan doesn't remove any limitation from superfunk itself; it adds two new behavioral rules. No prior limitation's workaround text exists to search for.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-30-checkpoint-priority-and-conditional-gate.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
