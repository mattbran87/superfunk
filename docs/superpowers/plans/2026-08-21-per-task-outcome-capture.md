# Per-Task Outcome Capture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every completed task a durable, git-tracked outcome note — what shipped, what diverged from the plan, what to follow up on — that survives after the plan's ephemeral workspace and report files are deleted, and wire it into `process-review` as a second evidence source. Per `docs/superpowers/specs/2026-08-21-per-task-outcome-capture-design.md`.

**Architecture:** One content addition to the implementer's status contract (a required Outcome field), one controller-side wiring edit (create/append/commit `docs/superpowers/plans/<plan-basename>-outcomes.md` at task completion), and one `process-review` wiring edit (read each shipped spec's outcomes file, fold real signal into the existing Misses/Recommendations/Gaps sections).

**Tech Stack:** Markdown skill files, no code, no test framework. Verification is grep checks plus disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Modify:** `plugin/skills/subagent-driven-development/implementer-prompt.md` — adds the required Outcome field to the short status-return contract.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds outcomes-file creation/append/commit instructions to the "Complete the task" step.
- **Modify:** `plugin/skills/process-review/SKILL.md` — adds a companion step reading each shipped spec's outcomes file, and folds outcomes-derived signal into Misses/Recommendations/Gaps.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Require an Outcome field in the implementer's status report

**Files:**
- Modify: `plugin/skills/subagent-driven-development/implementer-prompt.md`

- [ ] **Step 1: Insert the Outcome field into the short status-return contract**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
    Then report back with ONLY (under 15 lines — the detail lives in the
    report file):
    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - Commits created (short SHA + subject)
    - One-line test summary (e.g. "14/14 passing, output pristine")
    - Your concerns, if any
    - The report file path
```

Replace with:
```
    Then report back with ONLY (under 15 lines — the detail lives in the
    report file):
    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - Commits created (short SHA + subject)
    - One-line test summary (e.g. "14/14 passing, output pristine")
    - **Outcome (2-3 sentences):** What shipped, what diverged from the
      task brief, what to follow up on. State plainly when nothing
      diverged — e.g. "Shipped as planned; no divergence, no follow-ups."
    - Your concerns, if any
    - The report file path
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Outcome (2-3 sentences)" plugin/skills/subagent-driven-development/implementer-prompt.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/implementer-prompt.md
git commit -m "feat: require an Outcome field in the implementer status report

Every task and every fix round now reports 2-3 sentences on what
shipped, what diverged from the task brief, and what to follow up
on -- captured while the implementer's own memory of the task is
freshest, before its report file is deleted at Finish.

Part of docs/superpowers/specs/2026-08-21-per-task-outcome-capture-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Wire the outcomes file into "Complete the task"

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Insert the outcomes-file instructions after the ledger completion line**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
### 5. Complete the task

When the review comes back clean — or every open finding is parked with a
ruling at the cap — append the completion line to the ledger in the same
message as your other bookkeeping:

- `Task <N>: complete (commits <base7>..<head7>, review clean)`
- `Task <N>: complete (commits <base7>..<head7>, <K> parked)` after a
  tripped breaker

Then mark the todo complete and move on. Never move to the next task while
the review has open Critical/Important issues that are neither fixed nor
parked-with-ruling at the cap.
```

Replace with:
````
### 5. Complete the task

When the review comes back clean — or every open finding is parked with a
ruling at the cap — append the completion line to the ledger in the same
message as your other bookkeeping:

- `Task <N>: complete (commits <base7>..<head7>, review clean)`
- `Task <N>: complete (commits <base7>..<head7>, <K> parked)` after a
  tripped breaker

Also record this task's Outcome field — from the implementer's most
recent status report, the final round's if the task went through the
fix loop — in `docs/superpowers/plans/<plan-basename>-outcomes.md`
(`<plan-basename>` is PLAN_FILE's filename with `.md` removed, the
same value `scripts/sdd-workspace` derives). If this is the plan's
first completed task, create the file first with this header:

```markdown
# Outcomes — <plan filename>

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
```

Then append the entry itself:

```markdown
## Task <N>: <task name>
<the Outcome field's exact text>
```

Commit the outcomes file yourself, directly, in its own small commit —
this is controller bookkeeping, the same kind `process-reviews/tracker.md`
and `docs/lessons-learned.md` already get at Finish, just running once
per task here:

```bash
git add docs/superpowers/plans/<plan-basename>-outcomes.md
git commit -m "docs: record Task <N> outcome for <plan-basename>"
```

Then mark the todo complete and move on. Never move to the next task while
the review has open Critical/Important issues that are neither fixed nor
parked-with-ruling at the cap.
````

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Also record this task's Outcome field" plugin/skills/subagent-driven-development/SKILL.md
grep -n "docs: record Task" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat: create/append/commit the per-plan outcomes file at task completion

Complete the task now writes each task's Outcome field into
docs/superpowers/plans/<plan-basename>-outcomes.md and commits it
directly -- the same controller-bookkeeping pattern tracker.md and
lessons-learned.md already use at Finish, just running per task.

Part of docs/superpowers/specs/2026-08-21-per-task-outcome-capture-design.md."
```

Stage only this one file.

---

## Task 3: Wire the outcomes file into process-review

**Files:**
- Modify: `plugin/skills/process-review/SKILL.md`

- [ ] **Step 1: Update the intro and Core principle to name the new evidence source**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
Read `docs/superpowers/process-reviews/notes.md` and recent git
history across the specs shipped since the last review. Synthesize
findings into a dated review file, and reset the tracker.

**Core principle:** real evidence over vibes — every Catch, Miss,
Friction, and Gap in the output traces to a logged note or a specific
commit, not to memory of how the work felt.
```

Replace with:
```
Read `docs/superpowers/process-reviews/notes.md`, each shipped spec's
plan outcomes file (if one exists), and recent git history across the
specs shipped since the last review. Synthesize findings into a dated
review file, and reset the tracker.

**Core principle:** real evidence over vibes — every Catch, Miss,
Friction, and Gap in the output traces to a logged note, an outcomes
entry, or a specific commit, not to memory of how the work felt.
```

- [ ] **Step 2: Update "When to Use" to name the new evidence source**

Find:
```
Reads `docs/superpowers/process-reviews/tracker.md` and
`docs/superpowers/process-reviews/notes.md`. Invoked by two callers,
never run standalone without one of these triggers:
```

Replace with:
```
Reads `docs/superpowers/process-reviews/tracker.md`,
`docs/superpowers/process-reviews/notes.md`, and each shipped spec's
plan outcomes file (if one exists). Invoked by two callers, never run
standalone without one of these triggers:
```

- [ ] **Step 3: Insert the companion step and update the synthesis step**

Find:
```
2. Read `docs/superpowers/process-reviews/notes.md`. Collect every
   entry dated after the tracker's last-review date (or every entry,
   if the tracker reads "none yet").
3. Cross-reference `git log --oneline` for each shipped spec's
   implementing commits (the spec name usually appears in a commit
   trailer, e.g. "Part of docs/superpowers/specs/..."). For any fix
   commit whose message names a defect with no matching notes.md
   entry, treat it as a Catch the running log missed, and include it.
4. Synthesize the collected Catches into the review's sections:
   - **Specs Reviewed** — list the "Specs shipped since" filenames
     from the tracker; these are the specs this review covers.
   - **Catches** — list each Catch entry, grouped by spec.
   - **Misses** — a Catch that recurs across 2 or more of the
     reviewed specs signals something upstream should catch it
     earlier. Name the pattern and which specs it recurred in.
   - **Friction** — a task or spec whose commit history shows 3 or
     more fix rounds, or any note that reads as procedural friction
     rather than a code defect.
   - **Gaps** — a convention repeatedly caught by the same reviewer,
     with no earlier check backing it up.
   - **Recommendations** — one checkbox item per Miss, Friction
     point, or Gap identified above. Each names a target file and the
     exact change, e.g. `- [ ] Add X check to docs/ai-code-guidelines.md`.
     A Catch alone, with no recurring pattern, needs no
     Recommendation — the review loop already handled it.
5. Write the review to
   `docs/superpowers/process-reviews/review-after-<last-spec-slug>.md`,
   where `<last-spec-slug>` is the filename (minus `.md`) of the most
   recently shipped spec in the "Specs shipped since" list.
6. Update `docs/superpowers/process-reviews/tracker.md`: set "Last
   review" to `<spec-filename> — <YYYY-MM-DD>` (e.g.
   `2026-08-19-process-review-design.md — 2026-08-19`), using this
   review's spec filename and today's date, and clear "Specs shipped
   since" to `(none)`.
7. Commit the review file and the tracker update together.
```

Replace with:
```
2. Read `docs/superpowers/process-reviews/notes.md`. Collect every
   entry dated after the tracker's last-review date (or every entry,
   if the tracker reads "none yet").
3. For each spec in the "Specs shipped since" list, derive its plan's
   basename by stripping `-design` from the spec's filename (minus
   `.md`), then read
   `docs/superpowers/plans/<plan-basename>-outcomes.md` if it exists —
   a spec shipped before this mechanism existed has no outcomes file,
   and that absence never counts as an error. Collect every entry
   reporting a real divergence or follow-up; skip an entry that reads
   "shipped as planned" with no divergence or follow-up, since it
   carries no signal.
4. Cross-reference `git log --oneline` for each shipped spec's
   implementing commits (the spec name usually appears in a commit
   trailer, e.g. "Part of docs/superpowers/specs/..."). For any fix
   commit whose message names a defect with no matching notes.md
   entry, treat it as a Catch the running log missed, and include it.
5. Synthesize the collected Catches and outcomes entries into the
   review's sections:
   - **Specs Reviewed** — list the "Specs shipped since" filenames
     from the tracker; these are the specs this review covers.
   - **Catches** — list each Catch entry, grouped by spec.
   - **Misses** — a Catch that recurs across 2 or more of the
     reviewed specs signals something upstream should catch it
     earlier. Name the pattern and which specs it recurred in. An
     outcomes-reported divergence that recurs across 2 or more of the
     reviewed specs joins this section too, the same recurrence
     threshold.
   - **Friction** — a task or spec whose commit history shows 3 or
     more fix rounds, or any note that reads as procedural friction
     rather than a code defect.
   - **Gaps** — a convention repeatedly caught by the same reviewer,
     with no earlier check backing it up. An outcomes-reported
     follow-up too vague to act on yet joins this section too, as a
     candidate needing more definition.
   - **Recommendations** — one checkbox item per Miss, Friction
     point, or Gap identified above, plus one per outcomes-reported
     follow-up that names a concrete file and change. Each names a
     target file and the exact change, e.g. `- [ ] Add X check to
     docs/ai-code-guidelines.md`. A Catch or a one-off outcomes entry
     alone, with no recurring pattern and no concrete follow-up, needs
     no Recommendation — the review loop already handled it.
6. Write the review to
   `docs/superpowers/process-reviews/review-after-<last-spec-slug>.md`,
   where `<last-spec-slug>` is the filename (minus `.md`) of the most
   recently shipped spec in the "Specs shipped since" list.
7. Update `docs/superpowers/process-reviews/tracker.md`: set "Last
   review" to `<spec-filename> — <YYYY-MM-DD>` (e.g.
   `2026-08-19-process-review-design.md — 2026-08-19`), using this
   review's spec filename and today's date, and clear "Specs shipped
   since" to `(none)`.
8. Commit the review file and the tracker update together.
```

- [ ] **Step 4: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "derive its plan's" plugin/skills/process-review/SKILL.md
grep -n "^8\. Commit the review file" plugin/skills/process-review/SKILL.md
```

Expected: one match each.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/process-review/SKILL.md
git commit -m "feat: read outcomes files as a second evidence source in process-review

process-review now derives each shipped spec's plan-outcomes file
(stripping -design from the spec filename) and folds real
implementer-reported divergences and follow-ups into the existing
Misses/Recommendations/Gaps sections -- no new report section, a
second evidence source feeding the same four.

Part of docs/superpowers/specs/2026-08-21-per-task-outcome-capture-design.md."
```

Stage only this one file.

---

## Task 4: Verify the implementer's Outcome field with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture**

```bash
mkdir -p /c/sf-outcome-field-test
cd /c/sf-outcome-field-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
echo "# Scratch repo for per-task-outcome-capture trial" > /c/sf-outcome-field-test/README.md
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising the implementer's status-report format**

```bash
cd /c/sf-outcome-field-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-outcome-field-test. Assume you are the implementer subagent from the subagent-driven-development skill, dispatched for this task: create a file named hello.txt containing exactly the text 'hello'. Follow the implementer-prompt.md instructions exactly, including committing your work and producing the final short status report under Report Format. Report back in exactly 1 section with literal header SECTION 1/1: quote your exact short status report verbatim, exactly as you would send it to the controller." > /c/sf-outcome-field-test/trial.txt 2>&1
cat /c/sf-outcome-field-test/trial.txt
```

- [ ] **Step 3: Verify the Outcome field is present and correctly formed**

Read `/c/sf-outcome-field-test/trial.txt`. Confirm SECTION 1/1's quoted status report contains a bullet beginning `**Outcome`, and that bullet's text states plainly that the task shipped as planned with no divergence (since the trial task was trivial and unambiguous) — not a generic restatement of "what shipped" copied from elsewhere in the report, and not omitted.

If the Outcome field is missing or empty, treat this as DONE_WITH_CONCERNS and report exactly what the status report contained instead.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-outcome-field-test
```

No commit for this task.

---

## Task 5: Verify the controller's outcomes-file wiring with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a minimal plan**

```bash
mkdir -p /c/sf-outcomes-wiring-test/docs/superpowers/plans
cd /c/sf-outcomes-wiring-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > docs/superpowers/plans/2026-08-21-fixture-test.md <<'EOF'
# Fixture Test Implementation Plan

**Goal:** A trivial two-task plan used only to exercise the outcomes-file wiring in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Create file A

Create a file named a.txt containing "a".

## Task 2: Create file B

Create a file named b.txt containing "b".
EOF
git add -A
git commit -q -m "initial scratch fixture with fixture plan"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run a trial simulating Task 1's completion**

```bash
cd /c/sf-outcomes-wiring-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-outcomes-wiring-test. Assume you are the controller running the subagent-driven-development skill on the plan at docs/superpowers/plans/2026-08-21-fixture-test.md. Task 1 (Create file A) just came back from review clean, with this exact final status report from the implementer: Status: DONE. Commits created: abc1234 feat: add a.txt. One-line test summary: n/a. Outcome (2-3 sentences): Shipped as planned; no divergence, no follow-ups. Your concerns: none. Report file path: n/a. Follow the Complete the task step exactly, including the outcomes-file instructions, for this completion. Report back in exactly 1 section with literal header SECTION 1/1: quote the exact full contents of docs/superpowers/plans/2026-08-21-fixture-test-outcomes.md after you finish, read fresh from disk." > /c/sf-outcomes-wiring-test/trial1.txt 2>&1
cat /c/sf-outcomes-wiring-test/trial1.txt
```

- [ ] **Step 3: Verify the outcomes file was created correctly**

Read `/c/sf-outcomes-wiring-test/trial1.txt`, and independently verify:

```bash
cat /c/sf-outcomes-wiring-test/docs/superpowers/plans/2026-08-21-fixture-test-outcomes.md
echo "---"
cd /c/sf-outcomes-wiring-test && git log --oneline
```

Confirm the file exists with the exact header specified in this plan's Task 2, a `## Task 1: Create file A` entry containing the reported Outcome text, and a separate git commit (not folded into any other commit) whose message matches the `docs: record Task 1 outcome for 2026-08-21-fixture-test` pattern.

- [ ] **Step 4: Run a second trial simulating Task 2's completion**

```bash
cd /c/sf-outcomes-wiring-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-outcomes-wiring-test. Assume you are the controller running the subagent-driven-development skill on the plan at docs/superpowers/plans/2026-08-21-fixture-test.md. Task 1's outcomes entry already exists in docs/superpowers/plans/2026-08-21-fixture-test-outcomes.md. Task 2 (Create file B) just came back from review clean, with this exact final status report from the implementer: Status: DONE. Commits created: def5678 feat: add b.txt. One-line test summary: n/a. Outcome (2-3 sentences): Diverged from the brief by also adding a short comment at the top of b.txt explaining its purpose, since the brief didn't say whether comments were wanted; no other follow-ups. Your concerns: none. Report file path: n/a. Follow the Complete the task step exactly, including the outcomes-file instructions, for this completion. Report back in exactly 1 section with literal header SECTION 1/1: quote the exact full contents of docs/superpowers/plans/2026-08-21-fixture-test-outcomes.md after you finish, read fresh from disk." > /c/sf-outcomes-wiring-test/trial2.txt 2>&1
cat /c/sf-outcomes-wiring-test/trial2.txt
```

- [ ] **Step 5: Verify the outcomes file was appended, not overwritten**

Read `/c/sf-outcomes-wiring-test/trial2.txt`, and independently verify:

```bash
cat /c/sf-outcomes-wiring-test/docs/superpowers/plans/2026-08-21-fixture-test-outcomes.md
echo "---"
cd /c/sf-outcomes-wiring-test && git log --oneline
```

Confirm the file still carries the header and the unchanged Task 1 entry, now followed by a `## Task 2: Create file B` entry containing the reported divergence text verbatim, and a second, separate commit for the Task 2 outcome (two outcomes commits total, distinct from the two fictional implementer commits named in the reports).

If either trial shows the header duplicated, the Task 1 entry overwritten, or both entries folded into one commit, treat this as DONE_WITH_CONCERNS and report exactly what the file and git log actually contain.

- [ ] **Step 6: Clean up**

```bash
rm -rf /c/sf-outcomes-wiring-test
```

No commit for this task.

---

## Task 6: Verify process-review's outcomes wiring with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a tracker, two shipped specs, and one outcomes file**

```bash
mkdir -p /c/sf-process-review-outcomes-test/docs/superpowers/process-reviews
mkdir -p /c/sf-process-review-outcomes-test/docs/superpowers/specs
mkdir -p /c/sf-process-review-outcomes-test/docs/superpowers/plans
cd /c/sf-process-review-outcomes-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > docs/superpowers/process-reviews/tracker.md <<'EOF'
# Process Review Tracker

**Last review:** none yet
**Specs shipped since:** 2026-08-21-fixture-alpha-design.md, 2026-08-21-fixture-beta-design.md
EOF

cat > docs/superpowers/process-reviews/notes.md <<'EOF'
# Process Review — Running Notes

<!-- entries below this line -->
EOF

cat > docs/superpowers/specs/2026-08-21-fixture-alpha-design.md <<'EOF'
# Fixture Alpha — Design

**Date:** 2026-08-21
**Status:** Shipped
EOF

cat > docs/superpowers/specs/2026-08-21-fixture-beta-design.md <<'EOF'
# Fixture Beta — Design

**Date:** 2026-08-21
**Status:** Shipped
EOF

cat > docs/superpowers/plans/2026-08-21-fixture-alpha-outcomes.md <<'EOF'
# Outcomes — 2026-08-21-fixture-alpha.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Add the fixture module
Shipped as planned; no divergence, no follow-ups.

## Task 2: Wire the fixture module into the loader
Diverged from the brief by adding a small retry wrapper the brief
didn't ask for, since the loader already retries everywhere else in
this file. Follow-up: consider adding a dedicated retry-wrapper test
in tests/loader/retry.test.js — none exists today.
EOF

git add -A
git commit -q -m "initial scratch fixture: tracker, two shipped specs, one outcomes file (beta has none)"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising process-review's outcomes read and synthesis**

```bash
cd /c/sf-process-review-outcomes-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-process-review-outcomes-test. Use the process-review skill, invoked as if subagent-driven-development's Finish step triggered it. Follow the skill's process exactly, including the step that reads each shipped spec's plan outcomes file. Note that docs/superpowers/specs/2026-08-21-fixture-beta-design.md has no matching outcomes file at all -- confirm this does not error the process. Report back in exactly 3 numbered sections with literal headers: SECTION 1/3: state the plan basename you derived for fixture-alpha and for fixture-beta, and whether you found an outcomes file for each. SECTION 2/3: quote the exact Task 2 follow-up text you collected from fixture-alpha's outcomes file. SECTION 3/3: after writing the review file, quote the exact Gaps or Recommendations bullet (whichever you produced) that resulted from that follow-up." > /c/sf-process-review-outcomes-test/trial.txt 2>&1
cat /c/sf-process-review-outcomes-test/trial.txt
```

- [ ] **Step 3: Verify the derivation, the read, and the synthesis independently**

Read `/c/sf-process-review-outcomes-test/trial.txt`, and independently read the review file it should have written:

```bash
ls /c/sf-process-review-outcomes-test/docs/superpowers/process-reviews/
cat /c/sf-process-review-outcomes-test/docs/superpowers/process-reviews/review-after-2026-08-21-fixture-beta-design.md 2>/dev/null
```

Confirm:
1. SECTION 1/3 derives `2026-08-21-fixture-alpha` and `2026-08-21-fixture-beta` correctly (stripping `-design`), reports finding fixture-alpha's outcomes file, and reports finding none for fixture-beta without treating that as an error.
2. SECTION 2/3 quotes the retry-wrapper follow-up from fixture-alpha's Task 2 entry.
3. The written review file exists and contains a Gaps or Recommendations bullet naming the retry-wrapper test follow-up — since it names a concrete file (`tests/loader/retry.test.js`) and a concrete change, confirm it landed in **Recommendations** specifically, as a checkbox item, not merely mentioned in Gaps.

If the review file treats fixture-beta's missing outcomes file as an error, drops the fixture-alpha follow-up entirely, or misplaces it (Gaps instead of Recommendations, or omitted), treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the trial output and the written review file actually contain.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-process-review-outcomes-test
```

No commit for this task.
