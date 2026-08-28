# Documentation — Design

**Date:** 2026-08-28
**Status:** Shipped
**User-Facing:** No

## Context

`superfunk` needs a framework-level documentation process — the same shape as `bug-tracking`: a skill any project adopting superfunk uses, operating on its own repository, not something specific to superfunk itself. Three gaps motivate this, found the same way `bug-tracking`'s three gaps got named:

1. **Docs drift from what actually shipped.** Nothing touches a project's README or CHANGELOG when a user-facing change ships — the same staleness shape `docs/patterns/refresh-worked-examples-when-their-process-changes.md` already names for internal worked examples, applied here to a project's external-facing docs.
2. **No initial doc scaffold** for a project starting with none.
3. **No connection between internal specs and external docs.** A design spec already captures WHY and HOW; nothing translates that into the WHAT a user-facing doc needs to say. A project ends up re-deriving doc content from scratch even though the spec that motivated the change already has it.

**Research before designing from scratch:** a live web survey of existing tools found real solutions for Gap 1 (DeepDocs, README-Sync, Mintlify's AI workflows — all watch code diffs and draft doc updates via PR) and for CHANGELOG automation specifically (semantic-release, release-please, Changesets — all mature, widely used). None fit this framework's platform-agnostic, git-native default: the Gap-1 tools run as hosted SaaS requiring a GitHub account connection, and the CHANGELOG tools assume either npm or a specific git forge's PR flow. Gap 3 came back genuinely unaddressed — every "AI keeps docs in sync" tool works from a code diff (via AST parsing), not from an already-written structured document like a design spec's Context/Decision/Consequences. One pattern from Changesets deserves borrowing without adopting the tool itself: a small structured record per pending change, consumed later to generate a changelog — closely resembling what a design spec's own Consequences section already provides.

**Architecture discussion resolved four points before this spec:**

- **No Claude-Code-specific hook.** `scripts/review-package` and `scripts/sdd-workspace` already prove the pattern this session used successfully five separate times today (the notes.md gate, the Finish bookkeeping gate, `bug-tracking`'s ledger scan): a skill's own prose instructs the agent to run a script and gate on its output. This stays portable across any harness that can run a shell command, unlike a Claude-Code-native `PostToolUse` hook, which only benefits one specific harness.
- **The CLI tool stays strictly deterministic** — extraction, diffing, reporting only. No LLM call, no credentials to manage. Drafting the actual doc prose stays the invoking agent's job.
- **A project's user-facing-ness gets decided explicitly, during brainstorming** — a new `User-Facing: Yes | No` spec field — rather than inferred from spec content at Finish time. This matches this session's own repeated lesson: a gate needs a git-checkable precondition, not a last-second judgment call.
- **Fully synchronous for v1.** No background dispatch, no pending-draft tracking. The agent drafts README/CHANGELOG content directly during Finish, the same way every other Finish-time mechanism built this session works. Async drafting stays explicitly deferred until the synchronous version proves itself — matching how `bug-tracking` deferred external-tracker sync the same way.

## Decision

**`brainstorming/SKILL.md` gains a new required spec field**, added immediately after the existing `Status` line requirement:

```
- Give it a `User-Facing:` field: `Yes` or `No` — decided during
  brainstorming, not inferred later. `Yes` means a project's README
  or CHANGELOG needs updating once this ships;
  superpowers:documentation's Finish-time check reads this field to
  decide whether to fire.
```

**A new skill, `documentation`,** ships two entry points, mirroring `bug-tracking`'s shape:

- **Step 1 — Bootstrap (on-demand):** invoked by a human or a session for a project with no `README.md`/`CHANGELOG.md` yet. Pure prose, no script — scaffolds both files from a minimal template, the same way `bug-tracking`'s own Step 1 needed no script either.
- **Step 2 — Finish-time drafting:** triggered by `subagent-driven-development`'s Finish step. Runs `plugin/skills/documentation/scripts/check_docs.py <spec_file> <base_sha> <head_sha>` and branches on its output (see below). If `ACTION_NEEDED`, drafts the README and/or CHANGELOG update directly from the script's extracted spec content, then commits.

**The CLI tool, `check_docs.py`:**

1. Reads the spec file's `**User-Facing:**` field. Missing or `No`: prints `NOT_APPLICABLE: <reason>`, exits 0.
2. `Yes`: runs `git diff --name-only <base_sha> <head_sha>`. `README.md` or `CHANGELOG.md` present: prints `ALREADY_UPDATED: <files>`, exits 0.
3. Otherwise: parses the spec's `## Context`, `## Decision`, and `## Consequences` sections (split on `##` headers) and prints them under an `ACTION_NEEDED` banner, one section per labeled block. Exits 1.

The tool takes no position on what the doc update should say — it hands the drafting agent exactly the spec content needed, pre-extracted, so the agent doesn't re-parse the spec itself.

**`subagent-driven-development/SKILL.md`'s Finish section gains one more paragraph**, positioned alongside the existing `bug-tracking` ledger-scan step (both run as pre-workspace-deletion checks): invoke `check_docs.py` as described above, act on `ACTION_NEEDED`, skip cleanly on `NOT_APPLICABLE` or `ALREADY_UPDATED`.

**Applying `writing-plans`' own item 9 (Worked-example currency) to this addition**: this adds a step to Finish's documented sequence, and the Example Workflow refreshed one sub-project ago now demonstrates that sequence. The implementation plan for this spec needs its own task updating the Example Workflow's bracket-line sequence to include the new documentation check — closing the loop item 9 exists to close, on the very next Finish addition after it shipped.

## Falsifiable Criteria

1. A direct read-through of the shipped `brainstorming/SKILL.md` confirms the `User-Facing:` field requirement exists, worded identically to the Decision block above.
2. `plugin/skills/documentation/scripts/check_docs.py` has real unit tests (built via `test-driven-development`) covering all three branches: missing/No field, Yes-with-docs-already-updated, and Yes-with-ACTION_NEEDED including correct section extraction.
3. A direct read-through of the shipped `documentation/SKILL.md` confirms both steps match this Decision block.
4. A direct read-through of the shipped `subagent-driven-development/SKILL.md` confirms the new Finish paragraph invokes the script correctly and the Example Workflow's bracket-line sequence includes it.
5. A disposable `--plugin-dir` trial builds a fixture project with a user-facing spec whose commit range never touched README/CHANGELOG. Running the Finish-time step correctly reports `ACTION_NEEDED`, drafts real content into both files from the spec's own Context/Decision/Consequences, and commits.
6. A second trial builds the same fixture shape with a non-user-facing spec (`User-Facing: No`). Running the Finish-time step correctly reports `NOT_APPLICABLE` and makes no edit.

## Consequences

Every sub-project whose spec carries a `User-Facing: Yes` marking gains one more Finish-time check and, when it fires, a real README/CHANGELOG update drafted from the spec's own content — closing Gap 3 directly, since the draft comes from already-written spec prose rather than starting blank.

This ships the first real code (not markdown instructions) in this framework, with real unit tests — a precedent for any future skill that needs actual programmatic logic rather than prose an agent follows.

A project with no design-spec pipeline at all (using only `bug-tracking`-style ad hoc work) never triggers Step 2 — nothing traces back to a spec with a `User-Facing` field to read.

## Deferred

- Background/async drafting and the pending-draft tracking it would need — revisit once the synchronous version proves itself.
- Doc types beyond README and CHANGELOG (API reference, architecture docs, getting-started guides) — no evidence yet a specific project needs automated drafting for these.
- Any sync to a hosted doc-site generator (Docusaurus, Starlight, Mintlify, etc.) — a project's own choice if it wants a doc site; this skill's job stops at producing good markdown content.
- A Claude-Code-native hook as an additional, faster-feedback trigger layer on top of the Finish-time check — revisit only if the Finish-time check proves insufficient in practice.
