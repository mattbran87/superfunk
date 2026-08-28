# Superfunk Rebrand — Design

**Date:** 2026-08-28
**Status:** Approved
**User-Facing:** Yes

## Context

The fork's own plugin manifests, skill-invocation prefixes, and README install instructions still fully identify as upstream "Superpowers" — name `superpowers`, author Jesse Vincent, repository `obra/superpowers`, version `6.2.0` unchanged since the subtree import. Anyone installing this fork today would see the wrong project's identity, and following the README's install commands would install upstream (with none of superfunk's own additions: bug-tracking, documentation, concept-index, process-review, and dozens of others) rather than this fork.

Two findings shape the scope precisely:

- **Claude Code namespaces skills by the plugin's registered name, not each skill's own directory name** (e.g., `/content-ops:research` — `content-ops` names the plugin, `research` names the skill). This links the plugin's manifest name and every `superpowers:X` invocation-prefix reference together, not as independent choices — changing one without the other breaks skill resolution, pointing at a namespace that no longer exists (the same "Unknown skill" failure this session has already hit for other reasons).
- **The MIT license's copyright notice must stay intact** (`plugin/LICENSE`: "Copyright (c) 2025 Jesse Vincent") — the license's own terms require it "included in all copies or substantial portions of the Software." This file stays untouched regardless of everything else in this spec.

The user also wants the fork's origin visibly preserved somewhere a reader would find it, independent of the license requirement.

**Scope boundary:** this rebrands what's functionally load-bearing (manifest identity, invocation prefixes, install commands) and what's explicitly requested (Python requirement, fork attribution) — not a full narrative-prose rebrand. Deeper product-name prose (e.g., "you have superpowers," descriptive text throughout skill files) and the `using-superpowers` skill's own directory name stay unchanged, since the plugin-name-prefix fix alone resolves the functional concern, and a directory rename to the bootstrap skill carries much higher risk for no corresponding functional gain.

## Decision

**Seven manifest files** (`plugin/.claude-plugin/plugin.json`, `plugin/.claude-plugin/marketplace.json`, `plugin/package.json`, `plugin/gemini-extension.json`, `plugin/.cursor-plugin/plugin.json`, `plugin/.codex-plugin/plugin.json`, `plugin/.kimi-plugin/plugin.json`) get these field changes, wherever each field exists in that file:

- `name`: `superpowers` → `superfunk`
- `displayName` / `interface.displayName` (where present): `Superpowers` → `Superfunk`
- `author.name`: `Jesse Vincent` → `Matthew Brandenburg`
- `author.email`: `jesse@fsck.com` → `matt.bran87@gmail.com`
- `author.url` (codex only): `https://github.com/obra` → `https://github.com/mattbran87`
- `homepage`, `repository`, `websiteURL` (wherever present): `https://github.com/obra/superpowers` → `https://github.com/mattbran87/superfunk`
- `interface.developerName` (codex/kimi): `Jesse Vincent` → `Matthew Brandenburg`

Version numbers stay unchanged (`6.2.0`) — this rebrands identity, not a feature release.

**Every `superpowers:` skill-invocation prefix in live, instructional content** becomes `superfunk:`, applied as one mechanical bulk operation with full verification rather than individual edits. "Live, instructional content" means files an agent actually reads and acts on at runtime: every file under `plugin/skills/`, plus `plugin/CLAUDE.md` and `plugin/.github/PULL_REQUEST_TEMPLATE.md` (both give contributors and agents literal skill-invocation guidance for this fork).

**Historical records keep their original `superpowers:` references, unchanged**: `plugin/RELEASE-NOTES.md`'s past changelog entries, and archived design docs under `plugin/docs/plans/`, `plugin/docs/superpowers/plans/`, and `plugin/docs/superpowers/specs/` — all predating this fork, each describing what shipped under the Superpowers name at the time it happened. Rewriting these would misstate history rather than correct it.

**`plugin/README.md`'s 11 harness-specific Installation sections** (Claude Code, Antigravity, Codex App, Codex CLI, Cursor, Factory Droid, Gemini CLI, GitHub Copilot CLI, Kimi Code, OpenCode, Pi) get their literal marketplace/plugin/repository references updated from `obra/superpowers*` to `mattbran87/superfunk*` wherever an install command names a specific repo or plugin identifier. Surrounding narrative prose in each section stays as-is.

**A new attribution note**, placed immediately after `plugin/README.md`'s title, before the Quickstart section:

```markdown
> **Superfunk** is a fork of [Superpowers](https://github.com/obra/superpowers)
> by Jesse Vincent, customized for this project's own workflow. See
> [LICENSE](LICENSE) for the original copyright.
```

`plugin/LICENSE` itself stays completely unchanged — the MIT copyright notice for Jesse Vincent (2025) persists exactly as-is, satisfying the license's own terms independent of this attribution note.

**A new `## Requirements` section** in `plugin/README.md`, placed before Installation:

```markdown
## Requirements

- Python 3, for the `documentation` skill's Finish-time check
  (`check_docs.py`). No other skill in this library needs it.
```

## Falsifiable Criteria

1. A direct read-through of all seven manifest files confirms every field named in the Decision block matches the new values, and no file still names `superpowers`, Jesse Vincent, or `obra/superpowers` in any of those specific fields.
2. `grep -rl "superpowers:" plugin/skills/ plugin/CLAUDE.md plugin/.github/PULL_REQUEST_TEMPLATE.md` returns no files (the invocation prefix fully replaced in live content). A separate check confirms `plugin/RELEASE-NOTES.md` and the archived docs under `plugin/docs/` still contain their original `superpowers:` references, unchanged.
3. A direct read-through of `plugin/README.md` confirms the attribution note and Requirements section exist as specified, and all 11 harness Installation sections' literal repo/plugin references point at `mattbran87/superfunk` rather than `obra/superpowers*`.
4. `plugin/LICENSE` stays byte-for-byte unchanged from before this spec — confirmed by diffing against the pre-change version.
5. A disposable `--plugin-dir` trial against the renamed plugin confirms a skill resolves and invokes correctly under the new `superfunk:` prefix (e.g., dispatching a session that follows an instruction referencing `superfunk:writing-plans` or another renamed cross-reference, confirming it doesn't fail as an unknown skill).

## Consequences

Anyone installing this fork from today forward sees accurate identity, correct install instructions, and a clear, visible statement of its origin — closing the gap between what the manifests claimed and what this fork actually provides.

This counts as the most user-facing change made this session — literally the plugin's own name and installation instructions — so it also becomes the first sub-project to genuinely exercise the newly-shipped `documentation` skill's Finish-time check on a real (not fixture) case. `check_docs.py` doesn't recognize `plugin/RELEASE-NOTES.md` (this project's own established changelog file) as equivalent to `CHANGELOG.md` — a real gap the tool's first genuine use surfaces, to document and handle directly at Finish time rather than let it silently misfire.

## Deferred

- Full narrative-prose rebrand (every mention of "Superpowers" as a described concept, not just the manifest/prefix identity) — no evidence yet this matters beyond the functional and explicitly-requested scope above.
- Renaming the `using-superpowers` skill's own directory/name — the plugin-name-prefix fix alone resolves the functional concern; a rename here risks the bootstrap mechanism every session depends on, for no corresponding gain.
- Recognizing `RELEASE-NOTES.md` (or other equivalent changelog filenames) as equivalent to `CHANGELOG.md` in `check_docs.py` — a real gap surfaced by this very sub-project's own Finish step; revisit once this instance gets handled, if it recurs on a different project.
- Bumping the manifests' version number — this spec rebrands identity, not features; a version bump waits for a separate, later decision.
