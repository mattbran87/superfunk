# Pseudocode During Planning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port Casita's triggered pseudocode mechanism into `writing-plans`, positioned before task breakdown, and close the gap Casita never built by wiring the pseudocode into `subagent-driven-development`'s implementer dispatch — per `docs/superpowers/specs/2026-08-20-pseudocode-during-planning-design.md`.

**Architecture:** A new `## Pseudocode` step and section in `writing-plans/SKILL.md`, positioned right after File Structure and before task breakdown begins; a fourth Self-Review check; and one new dispatch bullet in `subagent-driven-development/SKILL.md`.

**Tech Stack:** Markdown skill files, no code, no test framework. Verification is grep checks plus two disposable `--plugin-dir` scratch trials, matching every other wiring change this session.

---

## File Structure

- **Modify:** `plugin/skills/writing-plans/SKILL.md` — adds a `## Pseudocode` section after File Structure, and a fourth Self-Review check.
- **Modify:** `plugin/skills/subagent-driven-development/SKILL.md` — adds a "Pseudocode context" bullet to "① Dispatch the implementer," alongside the existing "Directory context" bullet.

---

## Task 1: Add the Pseudocode step to writing-plans

**Files:**
- Modify: `plugin/skills/writing-plans/SKILL.md`

- [ ] **Step 1: Insert the Pseudocode section after File Structure**

Find:
```
This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Task Right-Sizing
```

Replace with:
```
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

No trigger silently omitted: every plan states T1 through T4, each
either populated or explicitly skipped.

## Task Right-Sizing
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "^## Pseudocode" plugin/skills/writing-plans/SKILL.md
grep -n "T1 — API call sites" plugin/skills/writing-plans/SKILL.md
```

Expected: one match each.

- [ ] **Step 3: Add the Self-Review coverage check**

Find:
```
**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

Replace with:
```
**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Pseudocode coverage:** Does the Pseudocode section state all four triggers (T1–T4), each either populated with real pseudocode or marked `Skipped: <reason>`? A trigger left out entirely is a plan failure, the same as a missing task for a spec requirement.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.
```

- [ ] **Step 4: Verify the Self-Review edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Pseudocode coverage" plugin/skills/writing-plans/SKILL.md
```

Expected: one match.

- [ ] **Step 5: Commit**

```bash
git add plugin/skills/writing-plans/SKILL.md
git commit -m "feat: add the Pseudocode step and self-review check to writing-plans

Evaluates T1-T4 (API call sites, handler/pattern reuse, DTO/schema
shape, user-designated) against File Structure's mapped files,
before task breakdown starts -- matching Casita's own placement,
adapted since writing-plans' task steps already require complete
code. Skip allowed with a reason; Self-Review now checks no trigger
was silently omitted.

Part of docs/superpowers/specs/2026-08-20-pseudocode-during-planning-design.md."
```

Stage only this one file — do not use `git add -A` or `git add .` (other unrelated untracked files exist in the working tree, e.g. `.idea/`).

---

## Task 2: Wire pseudocode into subagent-driven-development's implementer dispatch

**Files:**
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Add the Pseudocode context bullet**

Find:
```
- **Directory context:** before dispatching, list the directories this
  task touches — from the task brief's file structure — and read the
  `.context.md` for each one (per `docs/ai-code-guidelines.md`'s
  Per-Directory Context Files section). Fold a short summary of each
  into the dispatch's Context section, since the implementer never reads
  `.context.md` itself — it gets curated context, not raw file access to
  figure out on its own. A directory with no `.context.md` needs no
  mention in the dispatch, but note which directories you checked (in
  the dispatch's Context section or the ledger), so the check stays
  visible instead of quietly not happening.
- **Report file:** name the implementer's report file after the brief
```

Replace with:
```
- **Directory context:** before dispatching, list the directories this
  task touches — from the task brief's file structure — and read the
  `.context.md` for each one (per `docs/ai-code-guidelines.md`'s
  Per-Directory Context Files section). Fold a short summary of each
  into the dispatch's Context section, since the implementer never reads
  `.context.md` itself — it gets curated context, not raw file access to
  figure out on its own. A directory with no `.context.md` needs no
  mention in the dispatch, but note which directories you checked (in
  the dispatch's Context section or the ledger), so the check stays
  visible instead of quietly not happening.
- **Pseudocode context:** if the plan's Pseudocode section has a
  populated (non-`Skipped`) subsection for a trigger this task fires,
  fold that subsection into the dispatch's Context section. A task
  whose triggers are all `Skipped` needs no mention.
- **Report file:** name the implementer's report file after the brief
```

- [ ] **Step 2: Verify the edit landed correctly**

```bash
cd "C:\Users\marko\IdeaProjects\personal_products\superfunk"
grep -n "Pseudocode context" plugin/skills/subagent-driven-development/SKILL.md
```

Expected: one match.

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/subagent-driven-development/SKILL.md
git commit -m "feat: fold a task's populated pseudocode into its implementer dispatch

Closes the gap Casita's own spec 099 left unbuilt -- pseudocode
Planning wrote now actually reaches the implementer, instead of
being a write-only Planning-phase artifact nobody reads back.

Part of docs/superpowers/specs/2026-08-20-pseudocode-during-planning-design.md."
```

Stage only this one file.

---

## Task 3: Verify writing-plans' Pseudocode step with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture**

```bash
mkdir -p /c/sf-pseudocode-test
cd /c/sf-pseudocode-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
echo "# Scratch repo for pseudocode trial" > /c/sf-pseudocode-test/README.md
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
```

- [ ] **Step 2: Run an isolated trial that exercises the Pseudocode step directly**

```bash
cd /c/sf-pseudocode-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-pseudocode-test. Assume a spec is already approved for this idea: Task A calls the external OpenWeather API's /forecast/{city} endpoint and returns a parsed WeatherResponse object with temperature, humidity, and a list of hourly forecasts. Task B adds a constant MAX_RETRIES = 3 to config.py -- no external call, no handler pattern, no schema shape, nothing user-designated. Use the writing-plans skill. Complete the File Structure section and the new Pseudocode section exactly as the skill describes. Stop immediately after finishing the Pseudocode section -- do not continue to Task Structure or write the rest of the plan. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: quote the exact Pseudocode section you wrote, verbatim, including all four trigger labels (T1-T4). SECTION 2/2: state which trigger(s) you populated with real pseudocode and which you marked Skipped, and why." > /c/sf-pseudocode-test/trial.txt 2>&1
cat /c/sf-pseudocode-test/trial.txt
```

- [ ] **Step 3: Verify the trigger behavior**

Read `/c/sf-pseudocode-test/trial.txt`. Confirm:

1. SECTION 1/2 states all four triggers (T1, T2, T3, T4) — none silently omitted.
2. T1 (API call sites) has real natural-language pseudocode describing Task A's OpenWeather call and WeatherResponse shape — not a `Skipped` line, and not language-specific syntax (no `def`, no type annotations, no library imports).
3. T2, T3, and T4 each read `Skipped: <reason>` — Task B has no handler pattern, no multi-field schema of its own being defined, and the trial gave no user-designation.

If any of the three is missing, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the trial actually output.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-pseudocode-test
```

No commit for this task.

---

## Task 4: Verify the implementer dispatch includes pseudocode with a live trial

**Files:** none (verification only; touches no repository files)

- [ ] **Step 1: Build a scratch fixture with a plan file containing a populated Pseudocode section**

````bash
mkdir -p /c/sf-pseudocode-dispatch-test/docs/superpowers/plans
cd /c/sf-pseudocode-dispatch-test
git init -q -b main
git config user.email "test@example.com"
git config user.name "Test"
cat > /c/sf-pseudocode-dispatch-test/docs/superpowers/plans/2026-01-01-weather-fetch.md <<'EOF'
# Weather Fetch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development.

**Goal:** Add a weather-fetch helper and a retry constant.

**Architecture:** Two independent files.

**Tech Stack:** Python.

## Global Constraints

None.

---

## Pseudocode

- **T1 — API call sites:**
  ```
  function get_weather(city):
      response = call OpenWeather /forecast/{city}
      return WeatherResponse with temperature, humidity, hourly forecasts from response
  ```
- **T2 — Handler/pattern reuse:** Skipped: no handler or controller pattern involved.
- **T3 — DTO/schema shape:** Skipped: WeatherResponse shape already covered under T1.
- **T4 — User-designated:** Skipped: no user-designated pseudocode requested.

## Task A: Weather fetch

**Files:**
- Create: `weather.py`

- [ ] **Step 1: Implement get_weather**

```python
def get_weather(city):
    return {"temperature": 0, "humidity": 0, "hourly": []}
```

- [ ] **Step 2: Commit**

```bash
git add weather.py
git commit -m "feat: add weather fetch"
```

## Task B: Retry constant

**Files:**
- Create: `config.py`

- [ ] **Step 1: Add the constant**

```python
MAX_RETRIES = 3
```

- [ ] **Step 2: Commit**

```bash
git add config.py
git commit -m "feat: add retry constant"
```
EOF
git add -A
git commit -q -m "initial scratch fixture"
echo "FIXTURE READY"
````

- [ ] **Step 2: Run an isolated trial that composes both dispatches**

```bash
cd /c/sf-pseudocode-dispatch-test && claude -p --plugin-dir "/c/Users/marko/IdeaProjects/personal_products/superfunk/plugin" --dangerously-skip-permissions --output-format text "You are in a git repository at /c/sf-pseudocode-dispatch-test. A plan exists at docs/superpowers/plans/2026-01-01-weather-fetch.md. Assume you are following the subagent-driven-development skill and about to dispatch the implementer for Task A, then separately for Task B. Do not actually dispatch any subagent -- just compose each dispatch prompt's Context section exactly as step '① Dispatch the implementer' describes, including its Pseudocode context bullet. Report back in exactly 2 numbered sections with literal headers: SECTION 1/2: quote the Context section you would send for Task A's dispatch, verbatim. SECTION 2/2: quote the Context section you would send for Task B's dispatch, verbatim." > /c/sf-pseudocode-dispatch-test/trial.txt 2>&1
cat /c/sf-pseudocode-dispatch-test/trial.txt
```

- [ ] **Step 3: Verify the dispatch behavior**

Read `/c/sf-pseudocode-dispatch-test/trial.txt`. Confirm:

1. SECTION 1/2 (Task A's dispatch) includes the T1 pseudocode (the `get_weather` function describing the OpenWeather call and WeatherResponse shape) in its Context.
2. SECTION 2/2 (Task B's dispatch) does not include any pseudocode content — Task B's own triggers are all `Skipped` in the plan.

If either check fails, treat this as DONE_WITH_CONCERNS and report exactly which check failed, quoting what the trial actually output.

- [ ] **Step 4: Clean up**

```bash
rm -rf /c/sf-pseudocode-dispatch-test
```

No commit for this task — it verifies Task 2 and touches no repository files.
