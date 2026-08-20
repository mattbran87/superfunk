---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `superpowers:using-git-worktrees` skill at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Attempt to read the `.context.md` for each directory before mapping its role in the plan; skip if none exists — it holds the directory's purpose, key design decisions, and what to be careful about (per `docs/ai-code-guidelines.md`'s Per-Directory Context Files section). Note which directories you checked in the plan's File Structure section, so the check stays visible instead of silently not happening.
- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Pseudocode

Before breaking the plan into tasks, evaluate the files and
responsibilities from File Structure against four triggers, unchanged
from Casita's own proven set:

- **T1 — API call sites:** a task calls an external or internal API
  with more than a trivial signature.
- **T2 — Handler/pattern reuse:** a task implements a handler,
  controller, or pattern this codebase already uses elsewhere, where
  the shape matters.
- **T3 — DTO/schema shape:** a task defines or consumes a data shape
  with more than one or two fields.
- **T4 — User-designated:** the user asked for pseudocode on a
  specific piece of this plan.

For each trigger that fires, write natural-language pseudocode in a
`## Pseudocode` section of the plan document: standard idioms
(`for each`, `if`, `return`), no language-specific syntax, no type
system, no library calls. A trigger that fires but adds no signal
beyond what File Structure already states gets
`Skipped: <one-line reason>` instead of forced content — an empty or
padded pseudocode block is the same placeholder problem "No
Placeholders" already bans.

If more than one task fires the same trigger, label each task's
pseudocode separately within that trigger's subsection — for example
`T1 — API call sites (Task 2):` and `T1 — API call sites (Task 4):`
as two distinct entries, not one combined block. An unlabeled entry
under a trigger that fires for more than one task leaves later
readers unable to tell which task it describes.

Example, for a task that calls an external weather API:

````
- **T1 — API call sites:**
  ```
  function get_weather(city):
      response = call OpenWeather /forecast/{city}
      return WeatherResponse with temperature, humidity, hourly forecasts from response
  ```
- **T2 — Handler/pattern reuse:** Skipped: no handler or controller pattern involved.
````

No trigger silently omitted: every plan states T1 through T4, each
either populated or explicitly skipped.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task
- A Pseudocode entry with no real content, or a `Skipped` reason that just restates the trigger name instead of saying why

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Pseudocode coverage:** Does the Pseudocode section state all four triggers (T1–T4), each either populated with real pseudocode or marked `Skipped: <reason>`? A trigger left out entirely is a plan failure, the same as a missing task for a spec requirement. For each populated trigger, confirm the pseudocode stays natural-language only — no real code, no type annotations, no library calls. For each `Skipped` trigger, confirm the reason names a real absence, not a restatement of the trigger's name.

**5. Sibling-pattern parity:** When a plan adds a new instruction next to an existing sibling instruction in the same target file, does it mirror that sibling's established shape (a why-explanation, a visibility clause)? If not, add what's missing.

**6. Cross-file rule restatement:** Does this plan restate the same source rule in more than one target file? If so, read every restatement side by side. Confirm they describe the same underlying logic — the same conditions, the same structure — not just similar wording.

**7. Lessons-learned check:** Check `docs/lessons-learned.md` for any entry relevant to this plan's domain. Apply anything it flags.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:executing-plans
- Batch execution with checkpoints for review
