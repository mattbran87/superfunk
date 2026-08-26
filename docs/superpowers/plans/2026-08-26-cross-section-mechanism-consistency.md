# Cross-Section Mechanism Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the third open Recommendation from `docs/superpowers/process-reviews/review-after-2026-08-25-concept-index-design.md` — per `docs/superpowers/specs/2026-08-26-cross-section-mechanism-consistency-design.md`.

**Architecture:** One shared language-pattern trigger (routing/trigger/lifecycle phrasing) applied at two points: a new Self-Review item in `writing-plans/SKILL.md` for a plan's original tasks, and a scope carve-out in `re-review-prompt.md` for fix-round dispatches.

**Tech Stack:** Markdown skill/prompt files, no code, no test framework. Verification is direct read-throughs plus disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Modify:** `plugin/skills/writing-plans/SKILL.md` — adds Self-Review item 8.
- **Modify:** `plugin/skills/subagent-driven-development/re-review-prompt.md` — adds the scope carve-out to "New Breakage in the Fix Diff."

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan edits markdown skill/prompt files only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Add Self-Review item 8 to writing-plans

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Insert item 8 after item 7**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking.

Find:
```
**7. Lessons-learned check:** Check `docs/lessons-learned.md` for any entry relevant to this plan's domain. Apply anything it flags.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

Replace with:
```
**7. Lessons-learned check:** Check `docs/lessons-learned.md` for any entry relevant to this plan's domain. Apply anything it flags.

**8. Cross-section mechanism consistency:** Does any task edit content
describing a routing, trigger, or lifecycle mechanism — language like
"if X exists, proceed to...", "triggered by...", "never run
standalone," or a cross-reference like "see Y, below"? If so, grep
the same target file — and the design spec, if it also describes this
mechanism — for every other mention of the key terms involved, and
read each hit. Confirm the edit doesn't leave any of them
contradicting the new content.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Cross-section mechanism consistency" plugin/skills/writing-plans/SKILL.md
grep -n "the design spec, if it also describes this" plugin/skills/writing-plans/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat(skills): add Cross-section mechanism consistency to Self-Review

Recurred repeatedly this session (per-task-outcome-capture's
worked-example contradiction, concept-index's three fix rounds
chasing one distinction across four sections, this review period's
own Decision-vs-Criterion contradiction). A language-pattern trigger
(routing/trigger/lifecycle phrasing) makes recognition mechanical
rather than aspirational.

Part of docs/superpowers/specs/2026-08-26-cross-section-mechanism-consistency-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Add the scope carve-out to re-review-prompt.md

**Files:**
- Modify: `plugin/skills/subagent-driven-development/re-review-prompt.md`

- [ ] **Step 1: Insert the carve-out into "New Breakage in the Fix Diff"**

**Important:** read the file first with the Read tool to confirm the exact current text at the edit point — do not assume the Find block below is byte-identical without checking. This section sits inside the prompt template's outer fence (a `` ``` `` code block) — your Find/Replace targets only the prose lines shown below, not the fence markers themselves.

Find:
```
    ### New Breakage in the Fix Diff

    Anything the fix itself broke or introduced, with severity
    (Critical/Important/Minor) and file:line. "None" if clean.

    ### Out-of-Scope Observations
```

Replace with:
```
    ### New Breakage in the Fix Diff

    Anything the fix itself broke or introduced, with severity
    (Critical/Important/Minor) and file:line. "None" if clean.

    If the fix diff changes content describing a routing, trigger, or
    lifecycle mechanism (language like "if X exists, proceed to...",
    "triggered by...", "never run standalone," or a cross-reference like
    "see Y, below"), this is the one case where you must look outside the
    diff: grep the rest of the touched file — and the design spec, if the
    plan's Goal line names one — for every other mention of the same key
    terms, and read each hit. A contradiction there is New Breakage, not
    an Out-of-Scope Observation, since the fix itself caused it even
    though the contradicted text sits outside the literal diff.

    ### Out-of-Scope Observations
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "this is the one case where you must look outside" plugin/skills/subagent-driven-development/re-review-prompt.md
grep -n "since the fix itself caused it even" plugin/skills/subagent-driven-development/re-review-prompt.md
```

Expected: one match each.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/re-review-prompt.md
git commit -m "feat(skills): carve out cross-section checks in re-review's scope discipline

Most real recurrences of the cross-section contradiction failure
shape happened in fix-round dispatches, which never pass through
writing-plans' Self-Review at all. Extending the re-reviewer's
existing New Breakage check -- rather than adding new controller
self-discipline -- reaches the dispatched case using a mechanism
that already runs after every fix round.

Part of docs/superpowers/specs/2026-08-26-cross-section-mechanism-consistency-design.md."
```

Stage only this one file.

---

## Task 3: Verify Self-Review item 8 with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a target file containing a real routing/trigger contradiction risk**

```bash
mkdir -p /c/sf-cross-section-selfreview-test/docs/superpowers/plans
cd /c/sf-cross-section-selfreview-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

mkdir -p target-skill
cat > target-skill/routing.md <<'EOF'
# Routing Doc

## Step 1: Entry check

Look for the config file. If it exists, proceed to Step 3. If it
doesn't exist, proceed to Step 2.

## Step 2: First-time setup

Runs only when no config file exists yet.

## Step 3: Apply config

Triggered only when Step 1 finds an existing config file -- never
run standalone.
EOF

git add -A
git commit -q -m "initial scratch fixture: routing doc with Step 1/2/3 cross-references"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial exercising Self-Review item 8 against a plan whose task introduces a contradiction**

```bash
cd /c/sf-cross-section-selfreview-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-cross-section-selfreview-test. Use the Skill tool to invoke writing-plans. You are drafting a plan with exactly one task: modify target-skill/routing.md's Step 3 so it reads 'Triggered only when Step 1 finds an existing config file -- can also run standalone for manual reapplication.' Do not actually write the plan file to disk or make any edit to target-skill/routing.md -- this is a dry run of the Self-Review step only. Run Self-Review item 8 (Cross-section mechanism consistency) against this one planned task. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether the planned edit's language triggered item 8's routing/trigger/lifecycle pattern. SECTION 2/2: quote the exact contradiction you found (if any) after grepping target-skill/routing.md for the relevant terms, citing the specific other section that disagrees." > /c/sf-cross-section-selfreview-test/trial.txt 2>&1
cat /c/sf-cross-section-selfreview-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-cross-section-selfreview-test/trial.txt`. Confirm SECTION 1/2 reports the edit's "never run standalone" / "can also run standalone" language triggered item 8's pattern, and SECTION 2/2 correctly identifies the contradiction: the edited Step 3 would now allow standalone runs, but Step 1's routing logic still only ever reaches Step 3 by proceeding from Step 1 when a config file exists — the new "standalone" claim has no matching entry point anywhere else in the file.

If the trial reports item 8 didn't trigger, or reports no contradiction found, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-cross-section-selfreview-test
```

No commit for this task.

---

## Task 4: Verify the re-review carve-out with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a fixture plan, a routing doc, and a fix diff that introduces a contradiction**

```bash
mkdir -p /c/sf-cross-section-rereview-test/docs/superpowers/plans
mkdir -p /c/sf-cross-section-rereview-test/target-skill
cd /c/sf-cross-section-rereview-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > target-skill/routing.md <<'EOF'
# Routing Doc

## Step 1: Entry check

Look for the config file. If it exists, proceed to Step 3. If it
doesn't exist, proceed to Step 2.

## Step 2: First-time setup

Runs only when no config file exists yet.

## Step 3: Apply config

Triggered only when Step 1 finds an existing config file -- never
run standalone.
EOF

cat > docs/superpowers/plans/2026-08-26-rereview-fixture-test.md <<'EOF'
# Rereview Fixture Test Implementation Plan

**Goal:** A trivial one-task plan used only to exercise the re-review carve-out in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Adjust Step 3's wording

Modify target-skill/routing.md's Step 3 heading text slightly (cosmetic only).
EOF

git add -A
git commit -q -m "initial scratch fixture: routing doc, fixture plan (this is the review base)"

cat > target-skill/routing.md <<'EOF'
# Routing Doc

## Step 1: Entry check

Look for the config file. If it exists, proceed to Step 3. If it
doesn't exist, proceed to Step 2.

## Step 2: First-time setup

Runs only when no config file exists yet.

## Step 3: Apply config

Triggered only when Step 1 finds an existing config file -- can also
run standalone for manual reapplication.
EOF

git add -A
git commit -q -m "fix: allow Step 3 to run standalone for manual reapplication (fixture fix commit)"
echo "FIXTURE READY"
```

- [ ] **Step 2: Verify the fixture's fix diff actually only touches Step 3, leaving Step 1's contradiction unedited**

```bash
cd /c/sf-cross-section-rereview-test && git diff HEAD~1..HEAD -- target-skill/routing.md
```

Confirm the diff shows only Step 3's line changing — Step 1's routing logic (which only ever reaches Step 3 by proceeding from Step 1 when a config file exists) remains untouched, now contradicted by Step 3's new "can also run standalone" claim.

- [ ] **Step 3: Run an isolated trial exercising the re-review carve-out**

```bash
cd /c/sf-cross-section-rereview-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-cross-section-rereview-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current instructions loaded. Note its reference to re-review-prompt.md as the re-review dispatch template, and open that referenced sibling file using whatever path resolution you would naturally use for a skill's own referenced files (do not use Glob or a broad filesystem search). Follow re-review-prompt.md's instructions to re-review this fix: the diff from HEAD~1 to HEAD in target-skill/routing.md, which changed Step 3's wording to allow standalone runs. The plan this fix belongs to is docs/superpowers/plans/2026-08-26-rereview-fixture-test.md. Follow the New Breakage in the Fix Diff section's instructions exactly, including its cross-section check. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether the fix diff's language triggered the routing/trigger/lifecycle pattern requiring you to look outside the diff. SECTION 2/2: quote the exact New Breakage finding you reported, citing the specific other section (Step 1) that now contradicts Step 3's edit." > /c/sf-cross-section-rereview-test/trial.txt 2>&1
cat /c/sf-cross-section-rereview-test/trial.txt
```

- [ ] **Step 4: Verify the trial**

Read `/c/sf-cross-section-rereview-test/trial.txt`. Confirm SECTION 1/2 reports the fix diff's "never run standalone" → "can also run standalone" change triggered the pattern, and SECTION 2/2 reports the contradiction as **New Breakage** (not an Out-of-Scope Observation) — citing that Step 1's routing logic still has no entry point that would ever invoke Step 3 in a standalone way, contradicting Step 3's new claim.

If the trial reports the pattern didn't trigger, reports no contradiction, or misfiles the finding as an Out-of-Scope Observation instead of New Breakage, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains.

- [ ] **Step 5: Clean up**

```bash
rm -rf /c/sf-cross-section-rereview-test
```

No commit for this task.
