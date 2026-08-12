# Human-in-the-Loop Review Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a required step to `finishing-a-development-branch` that asks, once per feature, whether the user wants to review completed work themselves before the merge/PR/keep/discard menu appears.

**Architecture:** One new step ("Offer Human Review") inserted between the existing "Determine Base Branch" and "Present Options" steps in `plugin/skills/finishing-a-development-branch/SKILL.md`, shifting the three steps after it down by one and updating their internal `(Step N)` cross-references. No other file changes — this is a single-skill, single-file edit.

**Tech Stack:** Markdown skill file (no code, no test framework). Verification happens via disposable `--plugin-dir` scratch trials, per the design's Testing section — not automated tests, since there's no code to unit-test.

---

## File Structure

- **Modify:** `plugin/skills/finishing-a-development-branch/SKILL.md` — the only file this plan touches. All edits are inside this one file: the Overview's core-principle line, the Step 2 table/comment, a new Step 4 section, renumbering three subsequent `## Step N` headings, two inline `(Step N)` cross-references inside the (renumbered) Execute Choice section, and one new row in the Common Rationalizations table.

---

## Task 1: Add the Offer Human Review step to `finishing-a-development-branch`

**Files:**
- Modify: `plugin/skills/finishing-a-development-branch/SKILL.md`

- [ ] **Step 1: Update the Overview's core-principle line**

Find:
```
**Core principle:** Verify tests → Detect environment → Present options → Execute choice → Clean up.
```

Replace with:
```
**Core principle:** Verify tests → Detect environment → Offer review → Present options → Execute choice → Clean up.
```

- [ ] **Step 2: Update Step 2's comment and table to point at the renumbered Cleanup step**

Find:
```
# Capture now, while still inside the workspace — Step 5 changes directory
# before cleanup (Step 6) needs this value
```

Replace with:
```
# Capture now, while still inside the workspace — Step 6 changes directory
# before cleanup (Step 7) needs this value
```

Then find:
```
| `GIT_DIR != GIT_COMMON`, named branch | Standard 3 options | Provenance-based (see Step 6) |
```

Replace with:
```
| `GIT_DIR != GIT_COMMON`, named branch | Standard 3 options | Provenance-based (see Step 7) |
```

- [ ] **Step 3: Insert the new Step 4 and renumber "Present Options" to Step 5**

Find:
````
## Step 4: Present Options
````

Replace with:
````
## Step 4: Offer Human Review

Ask before presenting the menu: "Would you like to review the changes
yourself before deciding what to do next?"

**If no:** continue to Step 5, unchanged.

**If yes:**

```bash
git diff --stat <base-branch>...HEAD
```

Show that output. If a `spec.md` or plan doc exists for this work,
point to its Requirements section too — this puts what changed next to
what the work needed to do. Offer the full diff
(`git diff <base-branch>...HEAD`) if your human partner wants to see
it. Wait for explicit confirmation the changes look right before
continuing to Step 5.

## Step 5: Present Options
````

- [ ] **Step 4: Renumber "Execute Choice" to Step 6 and fix its two internal Step-6 references**

Find:
```
## Step 5: Execute Choice
```

Replace with:
```
## Step 6: Execute Choice
```

Then find:
```
Once the merged result is green: clean up the worktree (Step 6), then
delete the branch:
```

Replace with:
```
Once the merged result is green: clean up the worktree (Step 7), then
delete the branch:
```

Then find:
```
Then clean up the worktree (Step 6) and force-delete the branch:
```

Replace with:
```
Then clean up the worktree (Step 7) and force-delete the branch:
```

- [ ] **Step 5: Renumber "Cleanup Workspace" to Step 7**

Find:
```
## Step 6: Cleanup Workspace
```

Replace with:
```
## Step 7: Cleanup Workspace
```

- [ ] **Step 6: Add a Common Rationalizations row for skipping the new step**

Find:
```
| "The push was rejected — force-push will fix it" | A rejected push means the remote moved. Investigate; force-push only on your human partner's explicit request. |
```

Replace with:
```
| "The push was rejected — force-push will fix it" | A rejected push means the remote moved. Investigate; force-push only on your human partner's explicit request. |
| "They'll obviously want to skip review, no need to ask" | Ask anyway — the checkpoint costs one question, and skipping it removes your human partner's only whole-feature check. |
```

- [ ] **Step 7: Verify the file has exactly one occurrence of each step number, in order**

Run:
```bash
grep -n "^## Step" "plugin/skills/finishing-a-development-branch/SKILL.md"
```

Expected output (7 lines, one per step, in this order):
```
14:## Step 1: Verify Tests
28:## Step 2: Detect Environment
46:## Step 3: Determine Base Branch
53:## Step 4: Offer Human Review
<blank-adjusted>:## Step 5: Present Options
<blank-adjusted>:## Step 6: Execute Choice
<blank-adjusted>:## Step 7: Cleanup Workspace
```

(Exact line numbers after Step 4 will shift from the new content — confirm ordering and uniqueness, not exact numbers.)

Also run:
```bash
grep -n "Step 6\|Step 5" "plugin/skills/finishing-a-development-branch/SKILL.md"
```

Expected: every remaining `Step 6` reference means "Execute Choice," every remaining `Step 5` reference means "Present Options," and the only `(Step 7)` references are the two inside the (now) Step 6 section pointing at Cleanup Workspace. No reference should still point at the old numbering (e.g. no leftover "clean up the worktree (Step 6)" — that must now read "(Step 7)").

- [ ] **Step 8: Commit**

```bash
git add plugin/skills/finishing-a-development-branch/SKILL.md
git commit -m "feat: add human-in-the-loop review checkpoint to finishing-a-development-branch

Inserts a new Step 4 (Offer Human Review) between Determine Base
Branch and Present Options: ask once per feature whether the user
wants to review the diff themselves (file-stat + Requirements/plan
pointer, full diff on request) before the merge/PR/keep/discard menu
appears. Steps after it renumber from 4-6 to 5-7, with their internal
(Step N) cross-references updated to match.

Implements docs/superpowers/specs/2026-08-11-human-in-the-loop-review-design.md."
```

---

## Task 2: Verify the "no" path with a disposable scratch trial

**Files:** none (this task only runs commands; it modifies nothing in the repo)

- [ ] **Step 1: Set up a throwaway git repo with a completed feature branch**

```bash
mkdir -p /c/sf-review-checkpoint-test
cd /c/sf-review-checkpoint-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
echo "hello" > README.md
git add README.md
git commit -q -m "initial commit"
git checkout -q -b feature/add-greeting
echo "hello world" > README.md
git add README.md
git commit -q -m "feat: update greeting"
```

`-b main` pins the initial branch name explicitly, so this doesn't depend on the local git config's default branch name. Expected: no output beyond git's own quiet-mode silence; `git status` on this new repo shows a clean tree on branch `feature/add-greeting`.

- [ ] **Step 2: Run an isolated trial session answering "no"**

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-review-checkpoint-test, on branch feature/add-greeting, forked from main. All work is complete and tests pass (this toy repo has no test suite -- treat that as a passing/skippable check). Use the finishing-a-development-branch skill to wrap up this work. When the skill's Offer Human Review step asks whether to review the changes yourself, answer: no. After the skill presents its options menu, STOP -- do not select an option or run any git command beyond what is needed to reach and display that menu. Report back verbatim: the exact question asked (if any) at the review-checkpoint step, and the exact menu text you presented." > /c/sf-review-checkpoint-test/trial-no.txt 2>&1
cat /c/sf-review-checkpoint-test/trial-no.txt
```

Expected: the transcript shows the agent announcing the `finishing-a-development-branch` skill, running Step 1 (tests) and Step 2 (environment detection), asking the Step 3 base-branch question or inferring `main`, then at Step 4 either skipping straight past the review question (since the agent was told to answer "no") or explicitly stating it asked and got "no" — followed immediately by the standard 3-option menu (Merge back to main locally / Push and create a Pull Request / Keep the branch as-is), with no file-stat diff, no Requirements pointer, and no wait-for-confirmation language anywhere in the transcript.

- [ ] **Step 3: Confirm the "no" path matches today's unmodified behavior**

Read `/c/sf-review-checkpoint-test/trial-no.txt` and confirm two things explicitly:
1. The review question got asked (or the agent states it evaluated the "no" answer) before the menu appeared.
2. Nothing about a diff stat or Requirements pointer appears anywhere in the transcript — the "no" path must be indistinguishable from the pre-change skill except for the one extra question.

If either check fails, stop and re-examine Task 1's edit before continuing to Task 3.

---

## Task 3: Verify the "yes" path with a disposable scratch trial

**Files:** none (this task only runs commands; it modifies nothing in the repo)

- [ ] **Step 1: Reuse the same scratch repo from Task 2**

```bash
cd /c/sf-review-checkpoint-test
git status
```

Expected: still on branch `feature/add-greeting`, clean tree, same as Task 2 left it (Task 2's trial was instructed to stop before running any git command, so nothing should have changed).

- [ ] **Step 2: Run an isolated trial session answering "yes"**

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-review-checkpoint-test, on branch feature/add-greeting, forked from main. All work is complete and tests pass (this toy repo has no test suite -- treat that as a passing/skippable check). Use the finishing-a-development-branch skill to wrap up this work. When the skill's Offer Human Review step asks whether to review the changes yourself, answer: yes. Report back verbatim what the skill showed you at that point (the diff-stat output, and whether it mentioned a Requirements or plan-doc pointer -- there is no spec.md or plan doc in this repo, so confirm whether the skill still produced sensible output without one). Then confirm you waited for an explicit go-ahead before displaying the options menu -- state that go-ahead in your own reply, then show the menu. After presenting the menu, STOP -- do not select an option or run any further git commands." > /c/sf-review-checkpoint-test/trial-yes.txt 2>&1
cat /c/sf-review-checkpoint-test/trial-yes.txt
```

Expected: the transcript shows `git diff --stat main...feature/add-greeting` (or equivalent) output listing `README.md` as changed, an explicit statement that no `spec.md`/plan doc exists so no Requirements pointer got shown (graceful degradation, not an error or a stall), an explicit self-confirmation step before the menu, and then the same 3-option menu as Task 2.

- [ ] **Step 3: Confirm the "yes" path matches the design**

Read `/c/sf-review-checkpoint-test/trial-yes.txt` and confirm three things explicitly:
1. A file-stat-style diff summary appeared (not a full unified diff dump by default).
2. The agent handled the no-spec.md/no-plan-doc case without stalling or treating it as an error.
3. The menu appeared only after an explicit confirmation step, not immediately after the diff stat.

If any check fails, revise Task 1's Step 3 edit and re-run both Task 2 and Task 3 before proceeding.

- [ ] **Step 4: Clean up the scratch repo**

```bash
rm -rf /c/sf-review-checkpoint-test
```

Expected: directory no longer exists. This scratch fixture was disposable throughout — nothing here belongs in the superfunk repo.
