# Mechanisms Not Goodwill Wiring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one bullet to `plugin/skills/brainstorming/SKILL.md`'s "Presenting the design" section, per `docs/superpowers/specs/2026-08-13-mechanisms-not-goodwill-wiring-design.md`, so a design decision with no enforcement mechanism gets flagged as a gap instead of silently presented as settled.

**Architecture:** One text insertion into one existing markdown skill file — no code, no new files.

**Tech Stack:** Markdown skill file, no code, no test framework. Verification is a grep check plus one disposable `--plugin-dir` scratch trial.

---

## File Structure

- **Modify:** `plugin/skills/brainstorming/SKILL.md` — adds one bullet to the existing "Presenting the design" list.

---

## Task 1: Add the enforcement-check bullet to brainstorming

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`

- [ ] **Step 1: Add the bullet**

Find:
```
**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense
```

Replace with:
```
**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- For each design decision, name what actually checks or enforces it — a review step, a script, a derived value — not just what states it (per `docs/principles.md`'s Mechanisms, Not Goodwill). A decision with no enforcement mechanism is worth flagging as a gap, not silently presenting as settled.
- Be ready to go back and clarify if something doesn't make sense
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Mechanisms, Not Goodwill" plugin/skills/brainstorming/SKILL.md
```

Expected: one match, on the new bullet's line.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/brainstorming/SKILL.md
git commit -m "feat: wire Mechanisms Not Goodwill into brainstorming's design presentation

Adds a bullet to Presenting the design: name what actually checks or
enforces each decision, not just what states it, flagging a decision
with no enforcement mechanism as a gap rather than presenting it as
settled.

Part of docs/superpowers/specs/2026-08-13-mechanisms-not-goodwill-wiring-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Verify with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a design idea that includes one enforcement-free decision**

```bash
mkdir -p /c/sf-mng-wiring-test/docs
cd /c/sf-mng-wiring-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cp "C:\Users\marko\IdeaProjects\personal_products\superfunk\docs\principles.md" /c/sf-mng-wiring-test/docs/
git add -A
git commit -q -m "initial scratch fixture"
```

- [ ] **Step 2: Run an isolated trial that skips straight to design presentation**

```bash
claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-mng-wiring-test. Use the brainstorming skill for this idea: add a project convention that every API response must include a trace ID header, for debugging support requests. Skip asking clarifying questions -- treat these as already answered: this is a small internal API, trace IDs are UUIDv4 strings, the convention applies to every endpoint, and there is no existing request-logging middleware or schema validator in this project. Go directly to presenting the design in this same response. As part of presenting it, follow the skill's instruction to name what actually checks or enforces each decision. Format your response as exactly 2 numbered sections with literal headers: SECTION 1/2: the design decisions, one per line. SECTION 2/2: for the trace-ID-header decision specifically, quote verbatim whatever you wrote about what enforces it (or the absence of enforcement) -- do not paraphrase, quote your own exact words from the design. Stop after SECTION 2/2." > /c/sf-mng-wiring-test/trial.txt 2>&1
cat /c/sf-mng-wiring-test/trial.txt
```

- [ ] **Step 3: Verify the trial actually flagged the gap, not just presented the decision**

Read `/c/sf-mng-wiring-test/trial.txt`. Confirm:
1. The trace-ID-header decision appears in SECTION 1/2.
2. SECTION 2/2's quoted text explicitly names the absence of an enforcement mechanism (e.g., states no middleware, script, or review step currently checks for the header) rather than only restating the convention itself.
3. The quoted text reads as a genuine gap flag — language like "not currently enforced," "no check exists," or equivalent — not a bare restatement of the decision with no comment on enforcement.

If SECTION 2/2 only restates the decision without commenting on enforcement, treat this as DONE_WITH_CONCERNS — the wording in Task 1 may need to be stronger, not just present.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-mng-wiring-test
```

No commit for this task — it verifies Task 1 and touches no repository files.
