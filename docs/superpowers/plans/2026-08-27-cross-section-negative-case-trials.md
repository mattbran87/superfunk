# Cross-Section Negative-Case Trials Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Verify item 8 and the re-review carve-out correctly do NOT fire on a "trigger words" near-miss edit, per `docs/superpowers/specs/2026-08-27-cross-section-negative-case-trials-design.md`.

**Architecture:** Two disposable `--plugin-dir` trials, one per touchpoint, each dispatching a scenario-only prompt per `docs/patterns/ab-test-live-trials-for-behavior-change.md`'s Rule 2 — no code changes anticipated.

**Tech Stack:** No code, no test framework. Verification is entirely live-trial output plus direct re-reading of each dispatch prompt against Rule 2.

---

## File Structure

No files created or modified in this repository. Both tasks are verification-only, touching only disposable scratch fixtures outside this repo.

---

## Pseudocode

- **T1 — API call sites:** Skipped: this plan runs live trials only — no task calls an external or internal API.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reused code pattern.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape.
- **T4 — User-designated:** Skipped: the user didn't ask for pseudocode on any specific piece of this plan.

---

## Task 1: Negative-case trial for item 8 (Self-Review)

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a mock skill file holding real routing content plus an unrelated Style Notes section**

```bash
mkdir -p /c/sf-negative-case-selfreview-test/plugin/skills/mock-skill
cd /c/sf-negative-case-selfreview-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/mock-skill/routing.md <<'EOF'
# Routing Doc

## Apply Config

Applies configuration to the target system -- never run standalone;
always triggered by the setup wizard after Step 2 completes.

## Style Notes

Keep variable names in snake_case. Prefer explicit config keys over
positional arguments where practical.
EOF

git add -A
git commit -q -m "initial scratch fixture: mock-skill directory with routing.md (Apply Config + Style Notes)"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial with a scenario-only prompt — do not name the discriminating fact or state the expected answer**

```bash
cd /c/sf-negative-case-selfreview-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-negative-case-selfreview-test. Use the Skill tool to invoke writing-plans. You are drafting a plan with exactly one task: modify plugin/skills/mock-skill/routing.md's Style Notes section so it reads: 'Keep variable names in snake_case. Prefer explicit config keys over positional arguments where practical. Avoid trigger words like \"always\" or \"never\" in user-facing error messages; keep tone neutral.' Do not actually write the plan file to disk or make any edit to routing.md -- this is a dry run of the Self-Review step only. Run Self-Review item 8 (Cross-section mechanism consistency) against this one planned task. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether this planned edit's language triggers item 8's routing/trigger/lifecycle pattern, and explain your reasoning. SECTION 2/2: if it triggers, report what you checked and any contradiction found; if it does not trigger, explain specifically why the edited text doesn't match the pattern despite containing the word 'trigger.'" > /c/sf-negative-case-selfreview-test/trial.txt 2>&1
cat /c/sf-negative-case-selfreview-test/trial.txt
```

- [ ] **Step 3: Verify the trial**

Read `/c/sf-negative-case-selfreview-test/trial.txt`. Confirm SECTION 1/2 reports item 8's pattern does NOT trigger on this edit. Confirm SECTION 2/2 gives a specific, semantic reason — e.g. that "trigger" here describes wording to avoid in error messages, not an "if X exists, proceed to...", "triggered by...", or "never run standalone" mechanism claim — not a vacuous "no exact phrase match."

Then re-read the exact dispatch prompt used in Step 2 against `docs/patterns/ab-test-live-trials-for-behavior-change.md`'s Rule 2. Confirm it names item 8 (necessary so the agent knows what to run) but never states or implies whether this edit triggers it, and never explains why "trigger" here doesn't count — the agent had to determine and explain that itself.

If the trial reports item 8 DID trigger, or gives reasoning that amounts to "no keyword match found" without semantic explanation, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains — this would be a real defect in item 8's shipped trigger language, not a trial-design problem.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-negative-case-selfreview-test
```

No commit for this task.

---

## Task 2: Negative-case trial for the re-review carve-out

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a fixture plan and a fix diff making the same near-miss edit**

```bash
mkdir -p /c/sf-negative-case-rereview-test/plugin/skills/mock-skill
mkdir -p /c/sf-negative-case-rereview-test/docs/superpowers/plans
cd /c/sf-negative-case-rereview-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"

cat > plugin/skills/mock-skill/routing.md <<'EOF'
# Routing Doc

## Apply Config

Applies configuration to the target system -- never run standalone;
always triggered by the setup wizard after Step 2 completes.

## Style Notes

Keep variable names in snake_case. Prefer explicit config keys over
positional arguments where practical.
EOF

cat > docs/superpowers/plans/2026-08-27-negative-case-rereview-fixture-test.md <<'EOF'
# Negative Case Rereview Fixture Test Implementation Plan

**Goal:** A trivial one-task plan used only to exercise the re-review carve-out's negative case in a disposable trial.

**Architecture:** N/A.

**Tech Stack:** N/A.

---

## Task 1: Adjust the Style Notes wording

Modify plugin/skills/mock-skill/routing.md's Style Notes text slightly (cosmetic only).
EOF

git add -A
git commit -q -m "initial scratch fixture: routing doc, fixture plan (this is the review base)"

cat > plugin/skills/mock-skill/routing.md <<'EOF'
# Routing Doc

## Apply Config

Applies configuration to the target system -- never run standalone;
always triggered by the setup wizard after Step 2 completes.

## Style Notes

Keep variable names in snake_case. Prefer explicit config keys over
positional arguments where practical. Avoid trigger words like
"always" or "never" in user-facing error messages; keep tone neutral.
EOF

git add -A
git commit -q -m "fix: add trigger-word guidance to Style Notes (fixture fix commit)"
echo "FIXTURE READY"
```

- [ ] **Step 2: Verify the fixture's fix diff only touches Style Notes, leaving Apply Config (the real routing content) untouched**

```bash
cd /c/sf-negative-case-rereview-test && git diff HEAD~1..HEAD
```

Confirm the diff shows only the Style Notes section changing — Apply Config's routing/trigger content is untouched by this diff.

- [ ] **Step 3: Run an isolated trial with a scenario-only re-review prompt — do not name the discriminating fact or state the expected answer**

```bash
cd /c/sf-negative-case-rereview-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-negative-case-rereview-test. Use the Skill tool to invoke subagent-driven-development first, so you have its actual current instructions loaded. Note its reference to re-review-prompt.md as the re-review dispatch template, and open that referenced sibling file using whatever path resolution you would naturally use for a skill's own referenced files (do not use Glob or a broad filesystem search). Follow re-review-prompt.md's instructions to re-review this fix: the diff from HEAD~1 to HEAD in plugin/skills/mock-skill/routing.md, which added a sentence to the Style Notes section. The plan this fix belongs to is docs/superpowers/plans/2026-08-27-negative-case-rereview-fixture-test.md. Follow the New Breakage in the Fix Diff section's instructions exactly, including its cross-section check. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: state whether this fix diff's language triggers the routing/trigger/lifecycle pattern requiring you to look outside the diff, and explain your reasoning. SECTION 2/2: report your New Breakage in the Fix Diff finding (or confirm it is 'None' if the cross-section check doesn't apply); if the pattern doesn't trigger, explain specifically why the edited text doesn't match it despite containing the word 'trigger.'" > /c/sf-negative-case-rereview-test/trial.txt 2>&1
cat /c/sf-negative-case-rereview-test/trial.txt
```

- [ ] **Step 4: Verify the trial**

Read `/c/sf-negative-case-rereview-test/trial.txt`. Confirm SECTION 1/2 reports the pattern does NOT trigger, and SECTION 2/2 reports New Breakage as "None" (for the cross-section-check dimension specifically) with a specific, semantic reason — not a vacuous "no exact phrase match."

Then re-read the exact dispatch prompt used in Step 3 against `docs/patterns/ab-test-live-trials-for-behavior-change.md`'s Rule 2. Confirm it names the carve-out's mechanism (via "the New Breakage in the Fix Diff section's instructions... including its cross-section check") but never states or implies whether this diff triggers it, and never explains why "trigger" here doesn't count.

If the trial reports the pattern DID trigger, or gives reasoning that amounts to "no keyword match found" without semantic explanation, treat this as DONE_WITH_CONCERNS and report exactly what the trial output contains — this would be a real defect in the carve-out's shipped trigger language, not a trial-design problem.

- [ ] **Step 5: Clean up**

```bash
rm -rf /c/sf-negative-case-rereview-test
```

No commit for this task.
