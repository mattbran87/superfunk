# Cross-Section Sibling Scope Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Widen Self-Review item 8 and the re-review carve-out to grep sibling files in the same `plugin/skills/<name>/` directory, per `docs/superpowers/specs/2026-08-27-cross-section-sibling-scope-design.md`.

**Architecture:** Both mechanisms already share one grep-scope clause ("the same target file... and the design spec"). This plan adds one more clause to each, identically worded, so the two touchpoints stay in lockstep: "every other file in the same `plugin/skills/<name>/` directory if the target file lives in one."

**Tech Stack:** Markdown skill/prompt files, no code, no test framework. Verification is direct read-throughs plus disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Modify:** `plugin/skills/writing-plans/SKILL.md` — widens Self-Review item 8's grep scope.
- **Modify:** `plugin/skills/subagent-driven-development/re-review-prompt.md` — widens the carve-out's grep scope identically.

No other file in either skill's directory (`plugin/skills/writing-plans/plan-document-reviewer-prompt.md`, `plugin/skills/subagent-driven-development/{implementer-prompt.md,task-reviewer-prompt.md,SKILL.md}`) restates either grep-scope clause — confirmed by grep before writing this plan — so no other file needs a matching edit.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill/prompt files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Widen Self-Review item 8's grep scope

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Insert the sibling-directory clause into item 8**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
**8. Cross-section mechanism consistency:** Does any task edit content
describing a routing, trigger, or lifecycle mechanism — language like
"if X exists, proceed to...", "triggered by...", "never run
standalone," or a cross-reference like "see Y, below"? If so, grep
the same target file — and the design spec, if it also describes this
mechanism — for every other mention of the key terms involved, and
read each hit. Confirm the edit doesn't leave any of them
contradicting the new content.
```

Replace with:
```
**8. Cross-section mechanism consistency:** Does any task edit content
describing a routing, trigger, or lifecycle mechanism — language like
"if X exists, proceed to...", "triggered by...", "never run
standalone," or a cross-reference like "see Y, below"? If so, grep
the same target file, every other file in the same
`plugin/skills/<name>/` directory if the target file lives in one,
and the design spec, if it also describes this mechanism — for every
other mention of the key terms involved, and read each hit. Confirm
the edit doesn't leave any of them contradicting the new content.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "every other file in the same" plugin/skills/writing-plans/SKILL.md
grep -n "directory if the target file lives in one" plugin/skills/writing-plans/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat(skills): widen item 8's grep scope to sibling skill-directory files

The final review of cross-section-mechanism-consistency found its
own carve-out edit needed a fix in a sibling file (SKILL.md) the
shipped scope (target file plus design spec) never reaches. Skill
directories top out at 11 files and mostly hold far fewer, so the
added grep cost stays negligible.

Part of docs/superpowers/specs/2026-08-27-cross-section-sibling-scope-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Widen the re-review carve-out's grep scope

**Files:**
- Modify: `plugin/skills/subagent-driven-development/re-review-prompt.md`

- [ ] **Step 1: Insert the sibling-directory clause into the carve-out**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking. This section sits inside the prompt template's outer fence (a `` ``` `` code block) — your Find/Replace targets only the prose lines shown below, not the fence markers themselves.

Find:
```
    If the fix diff changes content describing a routing, trigger, or
    lifecycle mechanism (language like "if X exists, proceed to...",
    "triggered by...", "never run standalone," or a cross-reference like
    "see Y, below"), this is the one case where you must look outside the
    diff: grep the rest of the touched file — and the design spec, if the
    plan's Goal line or a task's commit trailer names one — for every
    other mention of the same key terms, and read each hit. A
    contradiction there is New Breakage, not an Out-of-Scope Observation,
    since the fix itself caused it even though the contradicted text sits
    outside the literal diff.
```

Replace with:
```
    If the fix diff changes content describing a routing, trigger, or
    lifecycle mechanism (language like "if X exists, proceed to...",
    "triggered by...", "never run standalone," or a cross-reference like
    "see Y, below"), this is the one case where you must look outside the
    diff: grep the rest of the touched file, every other file in the
    same `plugin/skills/<name>/` directory if the touched file lives in
    one, and the design spec, if the plan's Goal line or a task's
    commit trailer names one — for every other mention of the same key
    terms, and read each hit. A contradiction there is New Breakage,
    not an Out-of-Scope Observation, since the fix itself caused it
    even though the contradicted text sits outside the literal diff.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "every other file in the" plugin/skills/subagent-driven-development/re-review-prompt.md
grep -n "directory if the touched file lives in" plugin/skills/subagent-driven-development/re-review-prompt.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/re-review-prompt.md
git commit -m "feat(skills): widen the carve-out's grep scope to sibling skill-directory files

Preserves the deliberate parity with item 8 (same clause, identically
worded) established when the carve-out first shipped.

Part of docs/superpowers/specs/2026-08-27-cross-section-sibling-scope-design.md."
```

Stage only this one file.

---

## Task 3: Verify item 8's sibling-directory scope with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a two-file mock skill directory — the edit lands in one file, the contradiction lives only in the untouched sibling**

```bash
mkdir -p /c/sf-cross-section-sibling-selfreview-test/plugin/skills/mock-skill
cd /c/sf-cross-section-sibling-selfreview-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/mock-skill/routing.md <<'EOF'
# Routing Doc

## Apply Config

Applies configuration to the target system -- never run standalone;
always triggered by the setup wizard after Step 2 completes.
EOF

cat > plugin/skills/mock-skill/SKILL.md <<'EOF'
# Mock Skill

## Overview

This skill wraps routing.md's Apply Config step, which only runs
when triggered by the setup wizard -- it never runs standalone.
EOF

git add -A
git commit -q -m "initial scratch fixture: mock-skill directory with routing.md and sibling SKILL.md"
echo "FIXTURE READY"
```

Note: `routing.md` alone has no other section mentioning "standalone" — a same-file-only grep finds nothing wrong after the edit below. Only `SKILL.md`, the sibling, contradicts it. This isolates the sibling-directory widening from item 8's already-verified same-file behavior.

- [ ] **Step 2: Run an isolated trial exercising item 8 against a plan whose task introduces a contradiction only in the sibling file**

```bash
cd /c/sf-cross-section-sibling-selfreview-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-cross-section-sibling-selfreview-test. Use the Skill tool to invoke writing-plans. You are drafting a plan with exactly one task: modify plugin/skills/mock-skill/routing.md's Apply Config section so it reads 'Applies configuration to the target system -- can also run standalone for manual reapplication; always triggered by the setup wizard after Step 2 completes.' Do not actually write the plan file to disk or make any edit to plugin/skills/mock-skill/routing.md -- this is a dry run of the Self-Review step only. Run Self-Review item 8 (Cross-section mechanism consistency) against this one planned task. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether the planned edit's language triggered item 8's routing/trigger/lifecycle pattern, and whether you checked any file in the same plugin/skills/mock-skill/ directory besides routing.md itself. SECTION 2/2: quote the exact contradiction you found (if any), citing the specific file and text that disagrees." > /c/sf-cross-section-sibling-selfreview-test/trial.txt 2>&1
cat /c/sf-cross-section-sibling-selfreview-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-cross-section-sibling-selfreview-test/trial.txt`. Confirm SECTION 1/2 reports the edit's "never run standalone" / "can also run standalone" language triggered item 8's pattern, and explicitly reports checking `SKILL.md` in the same directory. Confirm SECTION 2/2 correctly identifies `SKILL.md`'s "it never runs standalone" line as the contradiction — not a false report of "no contradiction found" (which would mean the trial only checked `routing.md` itself, the exact failure this widening exists to close).

If the trial reports item 8 didn't trigger, reports no contradiction found, or shows no evidence of checking `SKILL.md`, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-cross-section-sibling-selfreview-test
```

No commit for this task.

---

## Task 4: Verify the carve-out's sibling-directory scope with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a fixture plan, a two-file mock skill directory, and a fix diff that contradicts the untouched sibling**

```bash
mkdir -p /c/sf-cross-section-sibling-rereview-test/plugin/skills/mock-skill
mkdir -p /c/sf-cross-section-sibling-rereview-test/docs/superpowers/plans
cd /c/sf-cross-section-sibling-rereview-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/mock-skill/routing.md <<'EOF'
# Routing Doc

## Apply Config

Applies configuration to the target system -- never run standalone;
always triggered by the setup wizard after Step 2 completes.
EOF

cat > plugin/skills/mock-skill/SKILL.md <<'EOF'
# Mock Skill

## Overview

This skill wraps routing.md's Apply Config step, which only runs
when triggered by the setup wizard -- it never runs standalone.
EOF

cat > docs/superpowers/plans/2026-08-27-sibling-rereview-fixture-test.md <<'EOF'
# Sibling Rereview Fixture Test Implementation Plan

**Goal:** A trivial one-task plan used only to exercise the re-review carve-out's sibling-directory scope in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Adjust Apply Config's wording

Modify plugin/skills/mock-skill/routing.md's Apply Config text slightly (cosmetic only).
EOF

git add -A
git commit -q -m "initial scratch fixture: mock-skill directory, fixture plan (this is the review base)"

cat > plugin/skills/mock-skill/routing.md <<'EOF'
# Routing Doc

## Apply Config

Applies configuration to the target system -- can also run
standalone for manual reapplication; always triggered by the setup
wizard after Step 2 completes.
EOF

git add -A
git commit -q -m "fix: allow Apply Config to run standalone for manual reapplication (fixture fix commit)"
echo "FIXTURE READY"
```

- [ ] **Step 2: Verify the fixture's fix diff only touches `routing.md`, leaving the sibling `SKILL.md` untouched and now contradicted**

```bash
cd /c/sf-cross-section-sibling-rereview-test && git diff HEAD~1..HEAD
```

Confirm the diff shows only `routing.md` changing. `SKILL.md`, in the same directory, still claims "it never runs standalone" and remains untouched — now contradicted by `routing.md`'s new "can also run standalone" claim.

- [ ] **Step 3: Run an isolated trial exercising the re-review carve-out**

```bash
cd /c/sf-cross-section-sibling-rereview-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-cross-section-sibling-rereview-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current instructions loaded. Note its reference to re-review-prompt.md as the re-review dispatch template, and open that referenced sibling file using whatever path resolution you would naturally use for a skill's own referenced files (do not use Glob or a broad filesystem search). Follow re-review-prompt.md's instructions to re-review this fix: the diff from HEAD~1 to HEAD in plugin/skills/mock-skill/routing.md, which changed the Apply Config wording to allow standalone runs. The plan this fix belongs to is docs/superpowers/plans/2026-08-27-sibling-rereview-fixture-test.md. Follow the New Breakage in the Fix Diff section's instructions exactly, including its cross-section check. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether the fix diff's language triggered the routing/trigger/lifecycle pattern requiring you to look outside the diff, and whether you checked any file in the same plugin/skills/mock-skill/ directory besides routing.md itself. SECTION 2/2: quote the exact New Breakage finding you reported, citing the specific sibling file (SKILL.md) and text that now contradicts the edit." > /c/sf-cross-section-sibling-rereview-test/trial.txt 2>&1
cat /c/sf-cross-section-sibling-rereview-test/trial.txt
```

- [ ] **Step 4: Verify the trial**

Read `/c/sf-cross-section-sibling-rereview-test/trial.txt`. Confirm SECTION 1/2 reports the fix diff's "never run standalone" → "can also run standalone" change triggered the pattern, and explicitly reports checking `SKILL.md` in the same directory. Confirm SECTION 2/2 reports the contradiction as **New Breakage** (not an Out-of-Scope Observation), citing `SKILL.md`'s "it never runs standalone" line.

If the trial reports the pattern didn't trigger, reports no contradiction, shows no evidence of checking `SKILL.md`, or misfiles the finding as an Out-of-Scope Observation instead of New Breakage, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains.

- [ ] **Step 5: Clean up**

```bash
rm -rf /c/sf-cross-section-sibling-rereview-test
```

No commit for this task.
