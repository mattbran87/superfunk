# Hazard Signal Words Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port ANSI Z535 signal words (DANGER/WARNING/CAUTION/NOTICE) for code comments and commit-message trailers, and wire `docs/code-standards.md` into the skill chain for the first time — per `docs/superpowers/specs/2026-08-21-hazard-signal-words-design.md`.

**Architecture:** Two content additions (`ai-code-guidelines.md`'s Hazard Signal Words section, `code-standards.md`'s commit-trailer rule), two broad wiring edits (implementer-prompt.md, task-reviewer-prompt.md), and two distributed wiring edits (writing-plans' File Structure, brainstorming's Documentation step).

**Tech Stack:** Markdown skill and doc files, no code, no test framework. Verification is grep checks plus two disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Modify:** `docs/ai-code-guidelines.md` — adds the "Hazard Signal Words" section.
- **Modify:** `docs/code-standards.md` — adds the commit-trailer rule to Git Conventions.
- **Modify:** `plugin/skills/subagent-driven-development/implementer-prompt.md` — extends the ai-code-guidelines.md read to also name code-standards.md.
- **Modify:** `plugin/skills/subagent-driven-development/task-reviewer-prompt.md` — extends the code-quality check to also check code-standards.md.
- **Modify:** `plugin/skills/writing-plans/SKILL.md` — adds a File Naming check to File Structure.
- **Modify:** `plugin/skills/brainstorming/SKILL.md` — adds a Spec File Conventions check to Documentation.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill and doc files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Add the Hazard Signal Words section to ai-code-guidelines.md

**Files:**
- Modify: `docs/ai-code-guidelines.md`

- [ ] **Step 1: Insert the new section after Why Comments**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
**AI:** Non-obvious constraints are exactly what Claude optimizes away. A magic number looks like a placeholder. An unusual conditional looks like a bug. A specific timeout looks arbitrary. Claude will "fix" these — and produce a correct-looking change that breaks a non-obvious invariant. A `// why:` comment makes the constraint visible in the context window. Claude reads it, understands that the pattern is intentional, and preserves it. Without the comment, the constraint is invisible.

---

## Signal Clarity
```

Replace with:
````
**AI:** Non-obvious constraints are exactly what Claude optimizes away. A magic number looks like a placeholder. An unusual conditional looks like a bug. A specific timeout looks arbitrary. Claude will "fix" these — and produce a correct-looking change that breaks a non-obvious invariant. A `// why:` comment makes the constraint visible in the context window. Claude reads it, understands that the pattern is intentional, and preserves it. Without the comment, the constraint is invisible.

---

## Hazard Signal Words

Mark a hazard inherent in the code — what breaks if a future caller
gets it wrong — with a fixed severity word: DANGER, WARNING, CAUTION,
or NOTICE. This answers a different question than a `why:` comment:
`why:` explains a non-obvious constraint; a hazard word flags what
happens if someone ignores the code that follows. A line can carry
both.

- **DANGER** — triggering this causes irreversible data loss or corruption
- **WARNING** — triggering this causes a serious but partially-recoverable problem
- **CAUTION** — non-obvious behavior that causes bugs if the reader doesn't know it
- **NOTICE** — important non-hazard context worth knowing

DANGER and WARNING go inline, directly at the hazardous line. CAUTION
and NOTICE go in the function or class's own documentation comment,
since they describe the unit as a whole rather than one exact line.

```python
def purge_records(user_id):
    # DANGER: a null user_id deletes every record in the table
    db.execute(f"DELETE FROM records WHERE user_id = {user_id}")
```

```python
def rebalance_shards():
    """
    CAUTION: must be called with the cluster lock held; concurrent calls corrupt shard state.
    """
    ...
```

**Engineering:** A hazard without a fixed severity word forces every reader to independently judge how bad the failure mode is. A consistent vocabulary makes severity legible at a glance, the same way a safety label does on physical equipment.

**AI:** Claude generates code near a hazardous line without knowing the blast radius of getting it wrong, unless the hazard is marked. A DANGER-level comment at the exact point of risk gives Claude a concrete signal to preserve the guard it protects, instead of "simplifying" it away.

---

## Signal Clarity
````

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^## Hazard Signal Words" docs/ai-code-guidelines.md
grep -n "DANGER and WARNING go inline" docs/ai-code-guidelines.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add docs/ai-code-guidelines.md
git commit -m "feat: add the Hazard Signal Words section to ai-code-guidelines.md

Ports ANSI Z535 signal words (DANGER/WARNING/CAUTION/NOTICE) for
code comments, kept separate from why: comments -- a hazard word
flags what breaks if misused, a why: comment explains why the code
looks unusual. A line can carry both.

Part of docs/superpowers/specs/2026-08-21-hazard-signal-words-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Add the commit-trailer rule to code-standards.md

**Files:**
- Modify: `docs/code-standards.md`

- [ ] **Step 1: Insert the new bullet and example into Git Conventions**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
- `[Rule]` Never commit build artifacts, secrets, or generated files — `.superfunk/tracking.db` and `.superfunk/__pycache__/` are real, already-gitignored examples of exactly this
```

Replace with:
````
- `[Rule]` Never commit build artifacts, secrets, or generated files — `.superfunk/tracking.db` and `.superfunk/__pycache__/` are real, already-gitignored examples of exactly this
- `[Rule]` A commit may carry one severity trailer, present only when it applies: `DANGER:` (irreversible once merged — a destructive migration, deleted data, rewritten shared history), `WARNING:` (hard to reverse or affects production/shared systems — a breaking API change, a default changed for all environments), `CAUTION:` (reversible but has a real blast radius — a large refactor, a major dependency upgrade), or `NOTICE:` (worth flagging, no risk — a deprecation heads-up, follow-up work still needed). Composes with the type/scope header the same way `BREAKING CHANGE:` does in Conventional Commits.

```
Reduce default request timeout from 30s to 5s

Aligns client timeout with the upstream service's actual p99 latency.

WARNING: Lowers the default timeout for all callers; may increase retry
rate for slow-network clients until they set an explicit override.
```
````

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "A commit may carry one severity trailer" docs/code-standards.md
grep -n "Aligns client timeout with the upstream" docs/code-standards.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add docs/code-standards.md
git commit -m "feat: add the commit severity-trailer rule to Git Conventions

Ports ANSI Z535 signal words for commit messages -- a footer
trailer, present only when it applies, composing with Conventional
Commits the same way BREAKING CHANGE: already does.

Part of docs/superpowers/specs/2026-08-21-hazard-signal-words-design.md."
```

Stage only this one file.

---

## Task 3: Wire code-standards.md into the implementer dispatch

**Files:**
- Modify: `plugin/skills/subagent-driven-development/implementer-prompt.md`

- [ ] **Step 1: Extend the ai-code-guidelines.md read**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point.

Find:
```
    Also read `docs/ai-code-guidelines.md` before writing any code — it
    holds this project's code conventions (naming, control flow, dead
    code, side effects, comments, tests) and applies to everything you
    write in this task.
```

Replace with:
```
    Also read `docs/ai-code-guidelines.md` and `docs/code-standards.md`
    before writing any code — together they hold this project's code
    conventions (naming, control flow, dead code, side effects,
    comments, tests) and file/commit conventions (file naming, git
    message format), and apply to everything you write and commit in
    this task.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "docs/ai-code-guidelines.md\` and \`docs/code-standards.md\`" plugin/skills/subagent-driven-development/implementer-prompt.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/implementer-prompt.md
git commit -m "feat: read code-standards.md alongside ai-code-guidelines.md before writing code

Closes a real gap found while designing hazard signal words:
code-standards.md was never wired into the skill chain at all, so
its existing Git Conventions rule was goodwill-only. The implementer
now reads both before writing or committing anything.

Part of docs/superpowers/specs/2026-08-21-hazard-signal-words-design.md."
```

Stage only this one file.

---

## Task 4: Wire code-standards.md into the code-quality review

**Files:**
- Modify: `plugin/skills/subagent-driven-development/task-reviewer-prompt.md`

- [ ] **Step 1: Extend the Project conventions check**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point.

Find:
```
    **Project conventions:**
    - Read `docs/ai-code-guidelines.md` and check whether the diff
      follows it — in particular: naming, explicit-over-implicit, flat
      control flow, dead code, side-effect isolation, why-comments,
      signal clarity, behavioral test naming.
    - A violation is a Code Quality finding like any other, cited by
      file:line.
```

Replace with:
```
    **Project conventions:**
    - Read `docs/ai-code-guidelines.md` and check whether the diff
      follows it — in particular: naming, explicit-over-implicit, flat
      control flow, dead code, side-effect isolation, why-comments,
      hazard signal words, signal clarity, behavioral test naming.
    - Read `docs/code-standards.md` and check whether the diff and its
      commit messages follow it — in particular: file naming, commit
      message format, and the severity-trailer rule for risky changes.
    - A violation is a Code Quality finding like any other, cited by
      file:line.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Read \`docs/code-standards.md\` and check whether the diff" plugin/skills/subagent-driven-development/task-reviewer-prompt.md
grep -n "hazard signal words" plugin/skills/subagent-driven-development/task-reviewer-prompt.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/task-reviewer-prompt.md
git commit -m "feat: check diffs and commits against code-standards.md in code-quality review

The review package already includes the commit list, so this was
checkable and unchecked. Also adds hazard signal words to the
existing ai-code-guidelines.md check list.

Part of docs/superpowers/specs/2026-08-21-hazard-signal-words-design.md."
```

Stage only this one file.

---

## Task 5: Wire File Naming into writing-plans' File Structure step

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Add the File Naming check**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point.

Find:
```
- Attempt to read the `.context.md` for each directory before mapping its role in the plan; skip if none exists — it holds the directory's purpose, key design decisions, and what to be careful about (per `docs/ai-code-guidelines.md`'s Per-Directory Context Files section). Note which directories you checked in the plan's File Structure section, so the check stays visible instead of silently not happening.
- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
```

Replace with:
```
- Attempt to read the `.context.md` for each directory before mapping its role in the plan; skip if none exists — it holds the directory's purpose, key design decisions, and what to be careful about (per `docs/ai-code-guidelines.md`'s Per-Directory Context Files section). Note which directories you checked in the plan's File Structure section, so the check stays visible instead of silently not happening.
- Check every new file name against `docs/code-standards.md`'s File Naming section before it enters the plan — kebab-case for markdown and documentation files, the `YYYY-MM-DD-<slug>` convention for dated artifacts.
- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Check every new file name against" plugin/skills/writing-plans/SKILL.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat: check new file names against code-standards.md in File Structure

Distributed wiring, matching how Per-Directory Context Files got
wired to specific trigger points rather than folded only into a
broad read -- File Structure is the exact moment file names get
decided.

Part of docs/superpowers/specs/2026-08-21-hazard-signal-words-design.md."
```

Stage only this one file.

---

## Task 6: Wire Spec File Conventions into brainstorming's Documentation step

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

- [ ] **Step 1: Add the Spec File Conventions check**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point.

Find:
```
- Write the validated design (spec) to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - (User preferences for spec location override this default)
- Give it a `Status` line: `Proposed`, `Approved` (not yet implemented), or `Superseded by <filename>`. Never a free-text description — `subagent-driven-development`'s Finish step is what advances `Approved` to `Shipped` once the work actually ships.
```

Replace with:
```
- Write the validated design (spec) to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - (User preferences for spec location override this default)
- Check the written spec against `docs/code-standards.md`'s Spec File Conventions section before committing — self-contained (readable without external context beyond `CLAUDE.md`), testable acceptance criteria, a current `Status` line.
- Give it a `Status` line: `Proposed`, `Approved` (not yet implemented), or `Superseded by <filename>`. Never a free-text description — `subagent-driven-development`'s Finish step is what advances `Approved` to `Shipped` once the work actually ships.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Check the written spec against" plugin/skills/brainstorming/SKILL.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat: check the written spec against code-standards.md before committing

Distributed wiring, matching how Per-Directory Context Files got
wired to specific trigger points -- Documentation's Write-design-doc
step is the exact moment a spec file actually gets written.

Part of docs/superpowers/specs/2026-08-21-hazard-signal-words-design.md."
```

Stage only this one file.

---

## Task 7: Verify the hazard-comment and commit-trailer mechanism with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture**

```bash
mkdir -p /c/sf-hazard-words-test
cd /c/sf-hazard-words-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
echo "# Scratch repo for hazard-signal-words trial" > /c/sf-hazard-words-test/README.md
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising the implementer's hazard-marking behavior**

```bash
cd /c/sf-hazard-words-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-hazard-words-test. Assume you are the implementer subagent from the subagent-driven-development skill, dispatched for this task: write a Python function purge_user(user_id) in user_admin.py that deletes every record for user_id from a records table -- if user_id is None or empty, this deletes every record in the entire table, which is unrecoverable. Also make the retry timeout for this module configurable, defaulting from 30s to 5s, in a follow-up commit -- this is a breaking change for any caller relying on the old default. Follow the implementer-prompt.md instructions exactly, including reading docs/ai-code-guidelines.md and docs/code-standards.md before writing any code, and commit both changes as separate commits with correct conventions. Report back in exactly 3 numbered sections with literal headers: SECTION 1/3: quote the exact hazard comment you wrote in user_admin.py, read fresh from disk. SECTION 2/3: quote the exact commit message (including any trailer) for the purge_user commit, read fresh from git log. SECTION 3/3: quote the exact commit message (including any trailer) for the timeout-default commit, read fresh from git log." > /c/sf-hazard-words-test/trial.txt 2>&1
cat /c/sf-hazard-words-test/trial.txt
```

- [ ] **Step 3: Verify the hazard comment and commit trailers independently**

Read `/c/sf-hazard-words-test/trial.txt`, and independently read the files and git log it should have touched:

```bash
cat /c/sf-hazard-words-test/user_admin.py
echo "---"
cd /c/sf-hazard-words-test && git log --format="%H%n%B%n---"
```

Confirm:
1. `user_admin.py` carries a `# DANGER:` comment inline at the deletion line, describing the null/empty `user_id` hazard.
2. The `purge_user` commit's message carries a `DANGER:` trailer (the operation itself is irreversible once merged and run).
3. The timeout-default commit's message carries a `WARNING:` trailer (a breaking default change affecting all callers).

If any of the three is missing, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the files and git log actually contain.

- [ ] **Step 4: Run a second trial confirming the reviewer catches a missing hazard marker**

```bash
cd /c/sf-hazard-words-test
git show HEAD~1:user_admin.py > /c/sf-hazard-words-test/user_admin_unmarked.py 2>/dev/null || cp user_admin.py /c/sf-hazard-words-test/user_admin_unmarked.py
sed -i '/# DANGER:/d' /c/sf-hazard-words-test/user_admin_unmarked.py
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-hazard-words-test. Assume you are the task reviewer subagent from the subagent-driven-development skill, reviewing a diff that adds this file, /c/sf-hazard-words-test/user_admin_unmarked.py, as user_admin.py -- a purge_user(user_id) function that deletes every record for user_id, with no hazard comment marking what happens if user_id is None or empty. Follow task-reviewer-prompt.md's Project conventions check exactly, reading docs/ai-code-guidelines.md as instructed. Report back in exactly 1 section with literal header SECTION 1/1: quote the exact Code Quality finding you would report for this file, citing docs/ai-code-guidelines.md by name, or state you found no issue." > /c/sf-hazard-words-test/trial2.txt 2>&1
cat /c/sf-hazard-words-test/trial2.txt
```

Confirm SECTION 1/1 reports a finding citing the missing DANGER-level hazard comment, naming `docs/ai-code-guidelines.md`. If it reports no issue, treat this as DONE_WITH_CONCERNS.

- [ ] **Step 5: Clean up**

```bash
rm -rf /c/sf-hazard-words-test
```

No commit for this task.

---

## Task 8: Verify the distributed wiring with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture**

```bash
mkdir -p /c/sf-distributed-wiring-test
cd /c/sf-distributed-wiring-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
echo "# Scratch repo for distributed-wiring trial" > /c/sf-distributed-wiring-test/README.md
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising writing-plans' File Naming check**

```bash
cd /c/sf-distributed-wiring-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-distributed-wiring-test. Assume a spec is already approved for this idea: add a new Python module. Use the writing-plans skill. In the File Structure section, your first instinct is to name the new file Add_The_New_Feature_Module.py (not kebab-case, not matching any existing convention). Follow the skill's File Structure step exactly, including the file-naming check against docs/code-standards.md. Stop immediately after finishing the File Structure section. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: quote the exact file name you settled on in File Structure, after running the check. SECTION 2/2: quote what the check against docs/code-standards.md's File Naming section told you, and whether it changed your original file-name instinct." > /c/sf-distributed-wiring-test/trial.txt 2>&1
cat /c/sf-distributed-wiring-test/trial.txt
```

- [ ] **Step 3: Verify the File Naming check fired**

Read `/c/sf-distributed-wiring-test/trial.txt`. Confirm SECTION 1/2's final file name follows `docs/code-standards.md`'s File Naming rules (kebab-case, e.g. `new-feature-module.py`, not the original `Add_The_New_Feature_Module.py`), and SECTION 2/2 shows the check actually caught and corrected the naming, not silently passing it through.

- [ ] **Step 4: Run an isolated trial exercising brainstorming's Spec File Conventions check**

```bash
cd /c/sf-distributed-wiring-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-distributed-wiring-test. Use the brainstorming skill for this idea: add a one-line helper function that returns the current year as an integer. Skip asking clarifying questions -- treat this as already fully specified. Go directly through presenting the design and then writing it to docs/superpowers/specs/2026-08-21-year-helper-design.md, following the skill's Documentation instructions exactly, including the check against docs/code-standards.md's Spec File Conventions section. Report back in exactly 1 section with literal header SECTION 1/1: state what the Spec File Conventions check told you, and quote the spec's actual Status line and acceptance-criteria section, read fresh from the file you wrote." > /c/sf-distributed-wiring-test/trial2.txt 2>&1
cat /c/sf-distributed-wiring-test/trial2.txt
```

- [ ] **Step 5: Verify the Spec File Conventions check fired**

Read `/c/sf-distributed-wiring-test/trial2.txt`, and independently read the file it should have written:

```bash
cat /c/sf-distributed-wiring-test/docs/superpowers/specs/2026-08-21-year-helper-design.md 2>/dev/null
```

Confirm the trial explicitly mentions running the check, and the written spec has a valid `Status` line and testable acceptance criteria, matching Spec File Conventions.

If either trial in this task shows the check silently skipped, treat this as DONE_WITH_CONCERNS and report exactly which check failed.

- [ ] **Step 6: Clean up**

```bash
rm -rf /c/sf-distributed-wiring-test
```

No commit for this task — it verifies Tasks 5 and 6 and touches no repository files.
