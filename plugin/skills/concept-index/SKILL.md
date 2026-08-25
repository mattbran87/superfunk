---
name: concept-index
description: Use when a codebase needs a fast concept-to-file lookup, especially as it grows past what directory structure alone makes navigable. Maintains docs/architecture/concept-index.md, a table mapping every skill, feature-tracking feature, and significant directory to its location and a one-line description.
---

# Concept Index

## Overview

Maintains `docs/architecture/concept-index.md`: a single git-tracked markdown table mapping three kinds of existing structural units — Skills, Features, and significant Directories — to their location and a one-line description. The index lets an agent find "where does X live" without searching, the same way a `.context.md` file gives an agent a directory's purpose without inferring it from file contents.

Two entry points exist: a full build (this skill, invoked directly, for a codebase with no index yet) and incremental maintenance (`subagent-driven-development`'s Finish step, triggered when a plan adds, renames, moves, or removes an indexed unit — see that skill's Finish section, not this one, for the trigger logic).

## Concept Units

A concept unit is one of:

- **Skill** — a directory at `plugin/skills/<name>/` containing a `SKILL.md`. Described by that file's own frontmatter `description:` field.
- **Feature** — a directory at `specs/<module>/<feature>/` (the `feature-tracking` pipeline), excluding `specs/_template/`. Described by its `spec.md`'s `#` heading and Requirements section.
- **Directory** — any directory meeting `docs/ai-code-guidelines.md`'s Per-Directory Context Files section's significant-directory threshold: "any directory with 3 or more non-generated files, or any top-level directory whose purpose is not evident from its name alone," excluding `.git/`, `node_modules/`, `__pycache__/`, `dist/`, `build/`. Described by its own `.context.md`'s `**Purpose:**` line, if one exists.

Never index `docs/superpowers/specs/` or `docs/superpowers/plans/` — that pipeline records this framework's own meta-development history (designing this project's own skills), not a downstream project's domain concepts.

## Process

### Step 1: Check for an existing index

Look for `docs/architecture/concept-index.md`. If it exists, this run is incremental maintenance — proceed to Step 3, and add/update/remove only the rows the current change calls for; never rebuild the whole table from scratch on top of an existing one. If it doesn't exist, proceed to Step 2.

### Step 2: Full build

Scan the codebase for every concept unit:

1. Every `plugin/skills/<name>/` directory containing a `SKILL.md`.
2. Every `specs/<module>/<feature>/` directory two levels under `specs/`, excluding `specs/_template/`.
3. Every directory meeting the significant-directory threshold from the Concept Units section above.

For each unit, derive its Description:

- **Skill:** read the `SKILL.md` frontmatter `description:` field directly. If it opens with "Use when...", trim that framing and keep the sentence(s) describing what the skill actually does or maintains.
- **Feature:** read the `spec.md`'s `#` heading (the feature name) and its Requirements section's first line, if populated. If Requirements is still the template's HTML-comment placeholder, use the heading alone.
- **Directory:** read the `.context.md`'s `**Purpose:**` line, if the file exists. If a Directory-type unit has no `.context.md`, ask the user for a one-line description rather than guessing one.

Write the table to `docs/architecture/concept-index.md`, with this exact header and column order:

```markdown
# Concept Index

| Concept | Type | Location | Description |
|---|---|---|---|
```

Sort rows alphabetically by Concept. Commit the file.

### Step 3: Incremental maintenance

Triggered by `subagent-driven-development`'s Finish step — never run this step standalone; it needs a specific plan's File Structure section as input, not a fresh codebase scan. Given that plan's File Structure section:

1. A new `plugin/skills/<name>/`, `specs/<module>/<feature>/`, or newly-significant directory: add one row, deriving its Description the same way Step 2 does for that unit type.
2. A renamed or moved unit: update its existing row's Concept name and/or Location — do not add a duplicate row.
3. A deleted unit: remove its row entirely.
4. No File Structure entry crosses any of these three boundaries: make no change to the index.

Commit the index change in its own small commit, separate from the plan's other Finish-step bookkeeping commits.

## Updating an Existing Index by Hand

A user may edit `docs/architecture/concept-index.md` directly (correcting a description, reordering rows). Never overwrite a hand-edited row without confirming with the user first — the same living-document discipline `project-definition` applies to its own generated sections.
