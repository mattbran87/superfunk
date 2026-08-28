# Superfunk Rebrand Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand the plugin's manifests, live invocation prefixes, and README from upstream "Superpowers" identity to "Superfunk," while preserving fork attribution and the untouched MIT license.

**Architecture:** Direct field-level edits to 7 JSON/manifest files, a scripted bulk find/replace of the `superpowers:` skill-invocation prefix across 12 live-content files (verified by grep), and targeted edits to `plugin/README.md` adding a Requirements section, a fork-attribution note, and corrected harness install commands. No code, no tests in the software sense — every task verifies via direct read-back, `grep`, or `git diff`.

**Tech Stack:** JSON manifests, Markdown, `sed`/`grep` (Git Bash), a disposable `claude -p --plugin-dir` trial for final verification.

## Global Constraints

- Version numbers in all 7 manifest files stay at `6.2.0` — this rebrands identity, not a feature release (per spec Decision).
- `plugin/LICENSE` stays byte-for-byte unchanged — MIT terms require Jesse Vincent's 2025 copyright notice to persist (per spec Context).
- New identity values, applied only to the exact fields named per manifest below: name `superfunk`, displayName `Superfunk`, author name `Matthew Brandenburg`, author email `matt.bran87@gmail.com`, author url `https://github.com/mattbran87`, homepage/repository/websiteURL `https://github.com/mattbran87/superfunk`, developerName `Matthew Brandenburg` (per spec Decision).
- Free-text `description`/`longDescription`/`shortDescription`/`skillInstructions` fields, and any field holding a literal file path (`main`, `pi.extensions`, `composerIcon`, `logo`, `sessionStart.skill`), stay unchanged — this rebrands identity metadata only, not prose or file references (per spec Scope boundary).
- The `superpowers:` → `superfunk:` invocation-prefix rewrite applies only to live, instructional content: every file under `plugin/skills/`, plus `plugin/CLAUDE.md` and `plugin/.github/PULL_REQUEST_TEMPLATE.md` (per spec Decision, amended).
- `plugin/RELEASE-NOTES.md` and archived docs under `plugin/docs/plans/`, `plugin/docs/superpowers/plans/`, `plugin/docs/superpowers/specs/` keep their original `superpowers:` references, unchanged — historical record (per spec Decision, amended).
- `plugin/README.md` gains a `## Requirements` section stating Python 3 is needed for `check_docs.py`, and a fork-attribution note crediting Jesse Vincent and linking `https://github.com/obra/superpowers`, placed right after the title (per spec Decision).
- The `using-superpowers` skill's own directory/skill name stays unchanged (per spec Scope boundary).

---

## File Structure

Directories touched: `plugin/`, `plugin/.claude-plugin/`, `plugin/.cursor-plugin/`, `plugin/.codex-plugin/`, `plugin/.kimi-plugin/`, `plugin/skills/*` (10 subdirectories), `plugin/.github/`. Checked each for a `.context.md` file — none exist anywhere under `plugin/` (confirmed via `find plugin -iname ".context.md"`), so no directory context to read.

This plan creates no new files — every edit modifies an existing file — so `docs/code-standards.md`'s File Naming section doesn't apply.

**Manifests to modify (field-level edits only):**
- `plugin/.claude-plugin/plugin.json` — Claude Code's own plugin manifest
- `plugin/.claude-plugin/marketplace.json` — local dev marketplace wrapping the same plugin
- `plugin/package.json` — Pi package manifest
- `plugin/gemini-extension.json` — Gemini CLI extension manifest
- `plugin/.cursor-plugin/plugin.json` — Cursor manifest
- `plugin/.codex-plugin/plugin.json` — Codex manifest
- `plugin/.kimi-plugin/plugin.json` — Kimi Code manifest

**Live-content files to modify (prefix rewrite only, via scripted sed):**
- `plugin/skills/brainstorming/SKILL.md`
- `plugin/skills/executing-plans/SKILL.md`
- `plugin/skills/subagent-driven-development/SKILL.md`
- `plugin/skills/systematic-debugging/SKILL.md`
- `plugin/skills/test-driven-development/writing-good-tests.md`
- `plugin/skills/using-superpowers/SKILL.md`
- `plugin/skills/using-superpowers/references/gemini-tools.md`
- `plugin/skills/writing-plans/SKILL.md`
- `plugin/skills/writing-skills/SKILL.md`
- `plugin/skills/writing-skills/testing-skills-with-subagents.md`
- `plugin/CLAUDE.md`
- `plugin/.github/PULL_REQUEST_TEMPLATE.md`

**README to modify (mixed edits):**
- `plugin/README.md` — 11 harness install-command references, one new `## Requirements` section, one new attribution blockquote

**Explicitly not modified:** `plugin/LICENSE`, `plugin/RELEASE-NOTES.md`, `plugin/docs/plans/**`, `plugin/docs/superpowers/plans/**`, `plugin/docs/superpowers/specs/**`.

## Pseudocode

- **T1 — API call sites:** Skipped: no task calls an external or internal API; every edit is a static JSON field value or Markdown text change.
- **T2 — Handler/pattern reuse:** Skipped: no task implements a handler, controller, or reusable code pattern; this rebrands identity strings and prefixes.
- **T3 — DTO/schema shape:** Skipped: no task defines or consumes a data shape; JSON manifests get literal field-value substitutions, not new structure.
- **T4 — User-designated:** Skipped: the user hasn't asked for pseudocode on any part of this work.

---

### Task 1: Rebrand Claude Code's manifest and dev marketplace

**Files:**
- Modify: `plugin/.claude-plugin/plugin.json`
- Modify: `plugin/.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: nothing from an earlier task (first task in this plan).
- Produces: the two files Claude Code itself reads to resolve the plugin's own identity and skill namespace (`superfunk`). Later tasks don't read these files' contents, but Task 6's live trial depends on this task's `name` field change to confirm skill resolution under the new namespace.

- [ ] **Step 1: Edit `plugin/.claude-plugin/plugin.json`**

Change:
```json
{
  "name": "superpowers",
  "description": "Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven techniques",
  "version": "6.2.0",
  "author": {
    "name": "Jesse Vincent",
    "email": "jesse@fsck.com"
  },
  "homepage": "https://github.com/obra/superpowers",
  "repository": "https://github.com/obra/superpowers",
  "license": "MIT",
```
To:
```json
{
  "name": "superfunk",
  "description": "Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven techniques",
  "version": "6.2.0",
  "author": {
    "name": "Matthew Brandenburg",
    "email": "matt.bran87@gmail.com"
  },
  "homepage": "https://github.com/mattbran87/superfunk",
  "repository": "https://github.com/mattbran87/superfunk",
  "license": "MIT",
```

- [ ] **Step 2: Edit `plugin/.claude-plugin/marketplace.json`**

Change:
```json
{
  "name": "superpowers-dev",
  "description": "Development marketplace for Superpowers core skills library",
  "owner": {
    "name": "Jesse Vincent",
    "email": "jesse@fsck.com"
  },
  "plugins": [
    {
      "name": "superpowers",
      "description": "Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven techniques",
      "version": "6.2.0",
      "source": "./",
      "author": {
        "name": "Jesse Vincent",
        "email": "jesse@fsck.com"
      }
    }
  ]
}
```
To:
```json
{
  "name": "superfunk-dev",
  "description": "Development marketplace for Superpowers core skills library",
  "owner": {
    "name": "Matthew Brandenburg",
    "email": "matt.bran87@gmail.com"
  },
  "plugins": [
    {
      "name": "superfunk",
      "description": "Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven techniques",
      "version": "6.2.0",
      "source": "./",
      "author": {
        "name": "Matthew Brandenburg",
        "email": "matt.bran87@gmail.com"
      }
    }
  ]
}
```

The top-level `name` field (`superpowers-dev` → `superfunk-dev`) isn't one of the spec's literally-quoted values, but it's the same `name` field the spec's Falsifiable Criterion 1 checks, and it still names "superpowers" — leaving it unchanged would contradict the criterion's intent. The `description` field's prose ("Superpowers core skills library") stays as-is: it isn't one of the itemized identity fields, matching the spec's narrative-prose exclusion.

- [ ] **Step 3: Validate both files parse as JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync('plugin/.claude-plugin/plugin.json'))" && node -e "JSON.parse(require('fs').readFileSync('plugin/.claude-plugin/marketplace.json'))" && echo VALID`
Expected: `VALID`

- [ ] **Step 4: Commit**

```bash
git add plugin/.claude-plugin/plugin.json plugin/.claude-plugin/marketplace.json
git commit -m "rebrand: update Claude Code plugin and dev marketplace identity to Superfunk"
```

---

### Task 2: Rebrand the Pi and Gemini CLI manifests

**Files:**
- Modify: `plugin/package.json`
- Modify: `plugin/gemini-extension.json`

**Interfaces:**
- Consumes: nothing from Task 1 (independent manifest).
- Produces: the `name` field Pi and Gemini CLI read to resolve the package/extension identity. No later task reads these files.

- [ ] **Step 1: Edit `plugin/package.json`**

Change:
```json
  "name": "superpowers",
```
To:
```json
  "name": "superfunk",
```

Leave `description`, `main`, and `pi.extensions` untouched — they hold prose or literal file paths (`.opencode/plugins/superpowers.js`, `./.pi/extensions/superpowers.ts`), not identity metadata, and no file in this plan gets renamed on disk.

- [ ] **Step 2: Edit `plugin/gemini-extension.json`**

Change:
```json
  "name": "superpowers",
```
To:
```json
  "name": "superfunk",
```

- [ ] **Step 3: Validate both files parse as JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync('plugin/package.json'))" && node -e "JSON.parse(require('fs').readFileSync('plugin/gemini-extension.json'))" && echo VALID`
Expected: `VALID`

- [ ] **Step 4: Commit**

```bash
git add plugin/package.json plugin/gemini-extension.json
git commit -m "rebrand: update Pi and Gemini CLI manifest identity to Superfunk"
```

---

### Task 3: Rebrand the Cursor, Codex, and Kimi Code manifests

**Files:**
- Modify: `plugin/.cursor-plugin/plugin.json`
- Modify: `plugin/.codex-plugin/plugin.json`
- Modify: `plugin/.kimi-plugin/plugin.json`

**Interfaces:**
- Consumes: nothing from Tasks 1–2 (independent manifests).
- Produces: the identity fields Cursor, Codex, and Kimi Code read to resolve plugin identity and display name. No later task reads these files.

- [ ] **Step 1: Edit `plugin/.cursor-plugin/plugin.json`**

Change:
```json
{
  "name": "superpowers",
  "displayName": "Superpowers",
  "description": "Core skills library: TDD, debugging, collaboration patterns, and proven techniques",
  "version": "6.2.0",
  "author": {
    "name": "Jesse Vincent",
    "email": "jesse@fsck.com"
  },
  "homepage": "https://github.com/obra/superpowers",
  "repository": "https://github.com/obra/superpowers",
  "license": "MIT",
```
To:
```json
{
  "name": "superfunk",
  "displayName": "Superfunk",
  "description": "Core skills library: TDD, debugging, collaboration patterns, and proven techniques",
  "version": "6.2.0",
  "author": {
    "name": "Matthew Brandenburg",
    "email": "matt.bran87@gmail.com"
  },
  "homepage": "https://github.com/mattbran87/superfunk",
  "repository": "https://github.com/mattbran87/superfunk",
  "license": "MIT",
```

- [ ] **Step 2: Edit `plugin/.codex-plugin/plugin.json`**

Change:
```json
{
  "name": "superpowers",
  "version": "6.2.0",
  "description": "An agentic skills framework & software development methodology that works: planning, TDD, debugging, and collaboration workflows.",
  "author": {
    "name": "Jesse Vincent",
    "email": "jesse@fsck.com",
    "url": "https://github.com/obra"
  },
  "homepage": "https://github.com/obra/superpowers",
  "repository": "https://github.com/obra/superpowers",
  "license": "MIT",
```
To:
```json
{
  "name": "superfunk",
  "version": "6.2.0",
  "description": "An agentic skills framework & software development methodology that works: planning, TDD, debugging, and collaboration workflows.",
  "author": {
    "name": "Matthew Brandenburg",
    "email": "matt.bran87@gmail.com",
    "url": "https://github.com/mattbran87"
  },
  "homepage": "https://github.com/mattbran87/superfunk",
  "repository": "https://github.com/mattbran87/superfunk",
  "license": "MIT",
```

Then, within the same file's `interface` block, change:
```json
  "interface": {
    "displayName": "Superpowers",
    "shortDescription": "Planning, TDD, debugging, and delivery workflows for coding agents",
    "longDescription": "Use Superpowers to guide agent work through brainstorming, implementation planning, test-driven development, systematic debugging, parallel execution, code review, and finish-the-branch workflows.",
    "developerName": "Jesse Vincent",
    "category": "Developer Tools",
    "capabilities": [
      "Interactive",
      "Read",
      "Write"
    ],
    "defaultPrompt": [
      "I've got an idea for something I'd like to build.",
      "Let's add a feature to this project."
    ],
    "websiteURL": "https://github.com/obra/superpowers",
```
To:
```json
  "interface": {
    "displayName": "Superfunk",
    "shortDescription": "Planning, TDD, debugging, and delivery workflows for coding agents",
    "longDescription": "Use Superpowers to guide agent work through brainstorming, implementation planning, test-driven development, systematic debugging, parallel execution, code review, and finish-the-branch workflows.",
    "developerName": "Matthew Brandenburg",
    "category": "Developer Tools",
    "capabilities": [
      "Interactive",
      "Read",
      "Write"
    ],
    "defaultPrompt": [
      "I've got an idea for something I'd like to build.",
      "Let's add a feature to this project."
    ],
    "websiteURL": "https://github.com/mattbran87/superfunk",
```

`longDescription`'s "Use Superpowers to guide..." prose and `composerIcon`'s `./assets/superpowers-small.svg` path stay unchanged — prose and a literal asset path, neither an itemized identity field nor a file this plan renames.

- [ ] **Step 3: Edit `plugin/.kimi-plugin/plugin.json`**

Change:
```json
{
  "name": "superpowers",
  "version": "6.2.0",
  "description": "An agentic skills framework and software development methodology.",
  "author": {
    "name": "Jesse Vincent",
    "email": "jesse@fsck.com"
  },
  "homepage": "https://github.com/obra/superpowers",
  "license": "MIT",
```
To:
```json
{
  "name": "superfunk",
  "version": "6.2.0",
  "description": "An agentic skills framework and software development methodology.",
  "author": {
    "name": "Matthew Brandenburg",
    "email": "matt.bran87@gmail.com"
  },
  "homepage": "https://github.com/mattbran87/superfunk",
  "license": "MIT",
```

Then, within the same file's `interface` block, change:
```json
  "interface": {
    "displayName": "Superpowers",
    "shortDescription": "Planning, TDD, debugging, and delivery workflows for coding agents",
    "longDescription": "Use Superpowers to guide agent work through brainstorming, implementation planning, test-driven development, systematic debugging, parallel execution, code review, and finish-the-branch workflows.",
    "developerName": "Jesse Vincent",
    "capabilities": [
      "Interactive",
      "Read",
      "Write"
    ],
    "websiteURL": "https://github.com/obra/superpowers"
  }
```
To:
```json
  "interface": {
    "displayName": "Superfunk",
    "shortDescription": "Planning, TDD, debugging, and delivery workflows for coding agents",
    "longDescription": "Use Superpowers to guide agent work through brainstorming, implementation planning, test-driven development, systematic debugging, parallel execution, code review, and finish-the-branch workflows.",
    "developerName": "Matthew Brandenburg",
    "capabilities": [
      "Interactive",
      "Read",
      "Write"
    ],
    "websiteURL": "https://github.com/mattbran87/superfunk"
  }
```

`sessionStart.skill: "using-superpowers"` and `skillInstructions`'s prose stay unchanged — the former names a skill directory this plan doesn't rename, the latter is instructional prose, not an itemized identity field.

- [ ] **Step 4: Validate all three files parse as JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync('plugin/.cursor-plugin/plugin.json'))" && node -e "JSON.parse(require('fs').readFileSync('plugin/.codex-plugin/plugin.json'))" && node -e "JSON.parse(require('fs').readFileSync('plugin/.kimi-plugin/plugin.json'))" && echo VALID`
Expected: `VALID`

- [ ] **Step 5: Commit**

```bash
git add plugin/.cursor-plugin/plugin.json plugin/.codex-plugin/plugin.json plugin/.kimi-plugin/plugin.json
git commit -m "rebrand: update Cursor, Codex, and Kimi Code manifest identity to Superfunk"
```

---

### Task 4: Rewrite the `superpowers:` invocation prefix in live content

**Files:**
- Modify: `plugin/skills/brainstorming/SKILL.md`
- Modify: `plugin/skills/executing-plans/SKILL.md`
- Modify: `plugin/skills/subagent-driven-development/SKILL.md`
- Modify: `plugin/skills/systematic-debugging/SKILL.md`
- Modify: `plugin/skills/test-driven-development/writing-good-tests.md`
- Modify: `plugin/skills/using-superpowers/SKILL.md`
- Modify: `plugin/skills/using-superpowers/references/gemini-tools.md`
- Modify: `plugin/skills/writing-plans/SKILL.md`
- Modify: `plugin/skills/writing-skills/SKILL.md`
- Modify: `plugin/skills/writing-skills/testing-skills-with-subagents.md`
- Modify: `plugin/CLAUDE.md`
- Modify: `plugin/.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Consumes: nothing from Tasks 1–3 (a text-content change, independent of manifest identity fields).
- Produces: every live skill-invocation cross-reference now reads `superfunk:<skillname>`, matching the plugin `name` Task 1 set. Task 6's live trial depends on this task to confirm a renamed cross-reference actually resolves.

- [ ] **Step 1: Confirm the exact occurrence count before editing**

Run: `grep -rn "superpowers:" plugin/skills/ plugin/CLAUDE.md plugin/.github/PULL_REQUEST_TEMPLATE.md | wc -l`
Expected: `33`

- [ ] **Step 2: Run the bulk replace across all 12 files**

Run:
```bash
sed -i 's/superpowers:/superfunk:/g' \
  plugin/skills/brainstorming/SKILL.md \
  plugin/skills/executing-plans/SKILL.md \
  plugin/skills/subagent-driven-development/SKILL.md \
  plugin/skills/systematic-debugging/SKILL.md \
  plugin/skills/test-driven-development/writing-good-tests.md \
  plugin/skills/using-superpowers/SKILL.md \
  plugin/skills/using-superpowers/references/gemini-tools.md \
  plugin/skills/writing-plans/SKILL.md \
  plugin/skills/writing-skills/SKILL.md \
  plugin/skills/writing-skills/testing-skills-with-subagents.md \
  plugin/CLAUDE.md \
  plugin/.github/PULL_REQUEST_TEMPLATE.md
```

- [ ] **Step 3: Verify no `superpowers:` occurrence remains in these 12 files**

Run: `grep -rn "superpowers:" plugin/skills/ plugin/CLAUDE.md plugin/.github/PULL_REQUEST_TEMPLATE.md`
Expected: no output (exit code 1, no matches)

- [ ] **Step 4: Verify the replacement landed correctly**

Run: `grep -rc "superfunk:" plugin/skills/ plugin/CLAUDE.md plugin/.github/PULL_REQUEST_TEMPLATE.md | awk -F: '{sum+=$2} END {print sum}'`
Expected: `33`

- [ ] **Step 5: Verify historical files are untouched**

Run: `git diff --stat plugin/RELEASE-NOTES.md plugin/docs/`
Expected: no output (no changes to any file under these paths)

- [ ] **Step 6: Commit**

```bash
git add plugin/skills/ plugin/CLAUDE.md plugin/.github/PULL_REQUEST_TEMPLATE.md
git commit -m "rebrand: rewrite superpowers: invocation prefix to superfunk: in live content"
```

---

### Task 5: Update README — install commands, Requirements, attribution

**Files:**
- Modify: `plugin/README.md`

**Interfaces:**
- Consumes: nothing from Tasks 1–4 (README edits are independent text changes; they reference the new identity values Task 1 already established but don't read the JSON files programmatically).
- Produces: the finished README Task 6 reads to confirm every Falsifiable Criterion about it. This task's changes also make `README.md` appear in the branch's diff, which Task 6 relies on for `check_docs.py`'s `ALREADY_UPDATED` branch.

- [ ] **Step 1: Add the fork-attribution note**

Change:
```markdown
# Superpowers

Superpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them.


## Quickstart
```
To:
```markdown
# Superpowers

> **Superfunk** is a fork of [Superpowers](https://github.com/obra/superpowers)
> by Jesse Vincent, customized for this project's own workflow. See
> [LICENSE](LICENSE) for the original copyright.

Superpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them.


## Quickstart
```

- [ ] **Step 2: Add the Requirements section**

Change:
```markdown
## Installation

Installation differs by harness. If you use more than one, install Superpowers separately for each one.
```
To:
```markdown
## Requirements

- Python 3, for the `documentation` skill's Finish-time check
  (`check_docs.py`). No other skill in this library needs it.

## Installation

Installation differs by harness. If you use more than one, install Superfunk separately for each one.
```

- [ ] **Step 3: Update the Claude Code install section**

Change:
```markdown
### Claude Code

Superpowers is available via the [official Claude plugin marketplace](https://claude.com/plugins/superpowers)

#### Official Marketplace

- Install the plugin from Anthropic's official marketplace:

  ```bash
  /plugin install superpowers@claude-plugins-official
  ```

#### Superpowers Marketplace

The Superpowers marketplace provides Superpowers and some other related plugins for Claude Code.

- Register the marketplace:

  ```bash
  /plugin marketplace add obra/superpowers-marketplace
  ```

- Install the plugin from this marketplace:

  ```bash
  /plugin install superpowers@superpowers-marketplace
  ```
```
To:
```markdown
### Claude Code

- Register the marketplace from this fork:

  ```bash
  /plugin marketplace add mattbran87/superfunk
  ```

- Install the plugin from this marketplace:

  ```bash
  /plugin install superfunk@superfunk
  ```
```

This drops the "Official Marketplace" subsection along with it — that marketplace distributes upstream Superpowers, not this fork, and pointing at it would install the wrong plugin.

- [ ] **Step 4: Update the Antigravity section**

Change:
```markdown
### Antigravity

Install Superpowers as a plugin from this repository:

```bash
agy plugin install https://github.com/obra/superpowers
```

Antigravity runs the plugin's session-start hook, so Superpowers is active from
the first message. Reinstall with the same command to update.
```
To:
```markdown
### Antigravity

Install Superfunk as a plugin from this repository:

```bash
agy plugin install https://github.com/mattbran87/superfunk
```

Antigravity runs the plugin's session-start hook, so Superfunk is active from
the first message. Reinstall with the same command to update.
```

- [ ] **Step 5: Update the Codex App and Codex CLI sections**

Change:
```markdown
### Codex App

Superpowers is available via the [official Codex plugin marketplace](https://github.com/openai/plugins).

- In the Codex app, click on Plugins in the sidebar.
- You should see `Superpowers` in the Coding section.
- Click the `+` next to Superpowers and follow the prompts.

### Codex CLI

Superpowers is available via the [official Codex plugin marketplace](https://github.com/openai/plugins).

- Open the plugin search interface:

  ```bash
  /plugins
  ```

- Search for Superpowers:

  ```bash
  superpowers
  ```

- Select `Install Plugin`.
```
To:
```markdown
### Codex App

This fork isn't published to the official Codex plugin marketplace. Install
it directly from the repository instead:

```bash
codex plugin install https://github.com/mattbran87/superfunk
```

### Codex CLI

This fork isn't published to the official Codex plugin marketplace. Install
it directly from the repository instead:

```bash
codex plugin install https://github.com/mattbran87/superfunk
```
```

The upstream Codex App/CLI sections pointed at an official marketplace listing that only distributes upstream Superpowers, not this fork — there's no equivalent marketplace entry to point at, so both sections switch to a direct-repository install, matching the pattern the Antigravity and Pi sections already use.

- [ ] **Step 6: Update the Cursor section**

Change:
```markdown
### Cursor

- In Cursor Agent chat, install from marketplace:

  ```text
  /add-plugin superpowers
  ```

- Or search for "superpowers" in the plugin marketplace.
```
To:
```markdown
### Cursor

- In Cursor Agent chat, install from this repository:

  ```text
  /add-plugin https://github.com/mattbran87/superfunk
  ```
```

The upstream marketplace search step is dropped for the same reason as Codex App/CLI — the plugin marketplace entry named "superpowers" resolves to upstream, not this fork.

- [ ] **Step 7: Update the Factory Droid section**

Change:
```markdown
### Factory Droid

- Register the marketplace:

  ```bash
  droid plugin marketplace add https://github.com/obra/superpowers
  ```

- Install the plugin:

  ```bash
  droid plugin install superpowers@superpowers
  ```
```
To:
```markdown
### Factory Droid

- Register the marketplace:

  ```bash
  droid plugin marketplace add https://github.com/mattbran87/superfunk
  ```

- Install the plugin:

  ```bash
  droid plugin install superfunk@superfunk
  ```
```

- [ ] **Step 8: Update the Gemini CLI section**

Change:
```markdown
### Gemini CLI

- Install the extension:

  ```bash
  gemini extensions install https://github.com/obra/superpowers
  ```

- Update later:

  ```bash
  gemini extensions update superpowers
  ```
```
To:
```markdown
### Gemini CLI

- Install the extension:

  ```bash
  gemini extensions install https://github.com/mattbran87/superfunk
  ```

- Update later:

  ```bash
  gemini extensions update superfunk
  ```
```

- [ ] **Step 9: Update the GitHub Copilot CLI section**

Change:
```markdown
### GitHub Copilot CLI

- Register the marketplace:

  ```bash
  copilot plugin marketplace add obra/superpowers-marketplace
  ```

- Install the plugin:

  ```bash
  copilot plugin install superpowers@superpowers-marketplace
  ```
```
To:
```markdown
### GitHub Copilot CLI

- Register the marketplace:

  ```bash
  copilot plugin marketplace add mattbran87/superfunk
  ```

- Install the plugin:

  ```bash
  copilot plugin install superfunk@superfunk
  ```
```

- [ ] **Step 10: Update the Kimi Code section**

Change:
```markdown
### Kimi Code

Superpowers is available in Kimi Code's plugin marketplace.

- Open Kimi Code's plugin manager:

  ```text
  /plugins
  ```

- Go to `Marketplace` > `Superpowers` and install it.

- Or install directly from this repository:

  ```text
  /plugins install https://github.com/obra/superpowers
  ```

- Detailed docs: [docs/README.kimi.md](docs/README.kimi.md)
```
To:
```markdown
### Kimi Code

This fork isn't published to Kimi Code's plugin marketplace. Install it
directly from the repository instead:

```text
/plugins install https://github.com/mattbran87/superfunk
```

- Detailed docs: [docs/README.kimi.md](docs/README.kimi.md)
```

- [ ] **Step 11: Update the OpenCode section**

Change:
```markdown
### OpenCode

OpenCode uses its own plugin install; install Superpowers separately even if you
already use it in another harness.

- Tell OpenCode:

  ```
  Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
  ```

- Detailed docs: [docs/README.opencode.md](docs/README.opencode.md)
```
To:
```markdown
### OpenCode

OpenCode uses its own plugin install; install Superfunk separately even if you
already use it in another harness.

- Tell OpenCode:

  ```
  Fetch and follow instructions from https://raw.githubusercontent.com/mattbran87/superfunk/refs/heads/main/.opencode/INSTALL.md
  ```

- Detailed docs: [docs/README.opencode.md](docs/README.opencode.md)
```

- [ ] **Step 12: Update the Pi section**

Change:
```markdown
### Pi

Install Superpowers as a Pi package from this repository:

```bash
pi install git:github.com/obra/superpowers
```

For local development, run Pi with this checkout loaded as a temporary package:

```bash
pi -e /path/to/superpowers
```

The Pi package loads the Superpowers skills and a small extension that injects the `using-superpowers` bootstrap at session startup and again after compaction. Pi has native skills, so no compatibility `Skill` tool is required. Subagent and task-list tools remain optional Pi companion packages.
```
To:
```markdown
### Pi

Install Superfunk as a Pi package from this repository:

```bash
pi install git:github.com/mattbran87/superfunk
```

For local development, run Pi with this checkout loaded as a temporary package:

```bash
pi -e /path/to/superfunk
```

The Pi package loads the Superfunk skills and a small extension that injects the `using-superpowers` bootstrap at session startup and again after compaction. Pi has native skills, so no compatibility `Skill` tool is required. Subagent and task-list tools remain optional Pi companion packages.
```

The `using-superpowers` bootstrap name stays unchanged here too — same directory-name exclusion as everywhere else in this plan.

- [ ] **Step 13: Read the full file back and confirm no stray `obra/superpowers` or bare install-context "Superpowers" references remain in the 11 harness sections**

Run: `grep -n "obra/superpowers" plugin/README.md`
Expected: no output (all 11 sections now point at `mattbran87/superfunk`)

- [ ] **Step 14: Commit**

```bash
git add plugin/README.md
git commit -m "rebrand: update README install instructions, add Requirements and fork-attribution note"
```

---

### Task 6: Full verification sweep and live trial

**Files:**
- No files modified — this task only verifies Tasks 1–5.

**Interfaces:**
- Consumes: the finished state of every file Tasks 1–5 touched.
- Produces: pass/fail evidence for every Falsifiable Criterion in the design spec. Nothing later depends on this task.

- [ ] **Step 1: Verify Falsifiable Criterion 1 — manifest fields**

Run: `grep -n '"name"\|"displayName"\|"author"\|"homepage"\|"repository"\|"websiteURL"\|"developerName"' plugin/.claude-plugin/plugin.json plugin/.claude-plugin/marketplace.json plugin/package.json plugin/gemini-extension.json plugin/.cursor-plugin/plugin.json plugin/.codex-plugin/plugin.json plugin/.kimi-plugin/plugin.json`
Expected: every line shows `superfunk`, `Superfunk`, `Matthew Brandenburg`, `matt.bran87@gmail.com`, or `mattbran87` — no line shows `superpowers`, `Jesse Vincent`, or `obra`.

- [ ] **Step 2: Verify Falsifiable Criterion 2 — prefix rewrite scope**

Run: `grep -rl "superpowers:" plugin/skills/ plugin/CLAUDE.md plugin/.github/PULL_REQUEST_TEMPLATE.md; echo "exit: $?"`
Expected: `exit: 1` (no files matched)

Run: `grep -c "superpowers:" plugin/RELEASE-NOTES.md`
Expected: a nonzero count (historical references still present, unchanged)

- [ ] **Step 3: Verify Falsifiable Criterion 3 — README**

Run: `grep -n "fork of \[Superpowers\]\|## Requirements\|obra/superpowers" plugin/README.md`
Expected: shows the attribution line, shows the Requirements heading, and shows no `obra/superpowers` matches outside the attribution note's own link.

- [ ] **Step 4: Verify Falsifiable Criterion 4 — LICENSE untouched**

Run: `git diff --stat HEAD~5 -- plugin/LICENSE` (adjust the range to cover every commit made in this plan)
Expected: no output (zero changes)

- [ ] **Step 5: Verify Falsifiable Criterion 5 — live trial**

Run:
```bash
claude -p --plugin-dir plugin "Use the superfunk:writing-plans skill to explain, in one sentence, what its Global Constraints section is for. Do not do anything else." --dangerously-skip-permissions
```
Expected: the agent resolves `superfunk:writing-plans` without an "Unknown skill" error and answers the question, confirming the renamed namespace works end-to-end.

- [ ] **Step 6: Confirm the documentation skill's Finish-time check reports the expected outcome**

Run: `python plugin/skills/documentation/scripts/check_docs.py docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md <merge-base-sha> HEAD`

(Substitute `<merge-base-sha>` with this branch's actual merge-base against the base branch.)

Expected: `ALREADY_UPDATED: plugin/README.md` (exit 0) — Task 5 already modified README.md, so no further documentation drafting is needed at Finish.

- [ ] **Step 7: No commit** — this task only verifies; nothing here changes tracked files.

---

## Self-Review

**1. Spec coverage:** Task 1–3 cover all 7 manifest files' field changes (spec Decision ¶1–2). Task 4 covers the amended prefix-rewrite scope (spec Decision ¶3–4). Task 5 covers all 11 README harness sections, the Requirements section, and the attribution note (spec Decision ¶5–8). Task 6 covers all 5 Falsifiable Criteria plus the Consequences section's documentation-check expectation. No spec section lacks a task.

**2. Placeholder scan:** No TBD/TODO markers; every step shows the actual before/after content or an exact runnable command.

**3. Type consistency:** N/A in the code sense — no functions or types get defined across tasks. File paths and field names stay consistent between the File Structure list and each task's own Files block.

**4. Pseudocode coverage:** All four triggers (T1–T4) stated and skipped with real reasons — no task involves an API call, a handler/pattern, or a data shape, and the user didn't request pseudocode.

**5. Sibling-pattern parity:** Task 5's Codex App/CLI and Cursor rewrites (dropping a now-inapplicable official-marketplace pointer) mirror the shape the Antigravity and Pi sections already use (direct-repository install) — checked side by side while drafting Step 5 and Step 6.

**6. Rule-restatement accuracy:** The Global Constraints section's field list was checked word-for-word against the spec's Decision bullet list before being copied in — same fields, same old→new values, nothing narrowed or broadened.

**7. Lessons-learned check:** Consulted `docs/lessons-learned.md` and `docs/patterns/self-review-checks-own-required-template.md` before writing this plan — the header above includes the required `## Global Constraints` section, closing the exact gap that pattern describes.

**8. Cross-section mechanism consistency:** Task 4 edits `subagent-driven-development/SKILL.md`'s and `writing-plans/SKILL.md`'s `superpowers:X` cross-references. Grepped both files' full text and every other top-level file in their respective `plugin/skills/` directories, plus the design spec, for other mentions of the renamed prefix or the plugin's identity — no other passage describes the invocation-prefix mechanism itself (only individual invocation sites, all covered by the same sed pass), so nothing contradicts the change. This plan traces to the design spec; a sentence noting this check is added to the spec's Consequences section in the same commit as Task 4 (see Step 6 below, executed as part of this Self-Review, not a separate task).

**9. Worked-example currency:** No task adds, removes, or reorders a step in a documented multi-step process (Finish's bookkeeping sequence, the fix loop, or similar) — this plan only renames identity strings and a prefix, so no worked example needs a currency check.

- [ ] **Step (Self-Review item 8 follow-through): Add the cross-section-consistency note to the spec**

Change (in `docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md`, end of Consequences section):
```markdown
This is the most user-facing change made this session — literally the plugin's own name and installation instructions — so it also becomes the first sub-project to genuinely exercise the newly-shipped `documentation` skill's Finish-time check on a real (not fixture) case. `check_docs.py` doesn't recognize `plugin/RELEASE-NOTES.md` (this project's own established changelog file) as equivalent to `CHANGELOG.md` — a real gap the tool's first genuine use surfaces, to document and handle directly at Finish time rather than let it silently misfire.
```
To:
```markdown
This is the most user-facing change made this session — literally the plugin's own name and installation instructions — so it also becomes the first sub-project to genuinely exercise the newly-shipped `documentation` skill's Finish-time check on a real (not fixture) case. `check_docs.py` doesn't recognize `plugin/RELEASE-NOTES.md` (this project's own established changelog file) as equivalent to `CHANGELOG.md` — a real gap the tool's first genuine use surfaces, to document and handle directly at Finish time rather than let it silently misfire. In practice this sub-project's own README.md edit satisfies `check_docs.py`'s `ALREADY_UPDATED` branch directly, so the gap doesn't block this specific case (confirmed by Task 6, Step 6 of the implementation plan).

The implementation plan's Task 4 checked every other top-level file in `plugin/skills/subagent-driven-development/` and `plugin/skills/writing-plans/`, plus this spec, for other descriptions of the `superpowers:`/`superfunk:` invocation-prefix mechanism itself. None exist beyond the individual invocation sites the bulk rewrite already covers, so no cross-reference needed a separate fix.
```

```bash
git add docs/superpowers/specs/2026-08-28-superfunk-rebrand-design.md
git commit -m "docs: note cross-section consistency check for superfunk-rebrand plan"
```

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-28-superfunk-rebrand.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
