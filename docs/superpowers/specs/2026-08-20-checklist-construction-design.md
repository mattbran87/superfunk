# Checklist Construction — Failure-Log Wiring and Size Discipline — Design

**Date:** 2026-08-20
**Status:** Approved, not yet implemented

## Context

The user's own draft adapts Atul Gawande's *The Checklist Manifesto*, plus surgical, construction, and investing checklist practice. It proposes rules for how Claude builds and runs checklists: pick READ-DO or DO-CONFIRM deliberately, keep items to killer items only, source items from documented past failures, cap size at 5-9 items with splitting past that, and state pause points explicitly.

superfunk's `writing-skills` skill already holds a 27-item "Skill Creation Checklist," grouped into five named phases (RED, GREEN, REFACTOR, Quality Checks, Deployment). It instructs creating a todo for all 27 items at once, at task start — far past the draft's size cap. Item-by-item review found two GREEN-phase items that restate general good-writing advice rather than naming a specific, easy-to-skip miss.

superfunk already runs a failure-log mechanism the draft's own proposed `docs/checklist_failures.md` would duplicate: `docs/lessons-learned.md` and `docs/patterns/`, shipped earlier this session. Reusing it avoids two parallel logs with an unclear boundary between them.

This spec ports the draft's discipline in two parts. It writes the general rule into `docs/code-standards.md`, so future skill-writers apply it without re-deriving it. It applies the rule to `writing-skills`' checklist as the concrete proof case, and wires failure-log sourcing into every existing DO-CONFIRM checklist in the fork.

## Decision

- **New `docs/code-standards.md` section: "Checklist Construction."** States four rules, adapted from the user's draft:
  - Choose READ-DO (a fixed sequence, run in order) or DO-CONFIRM (do the work, then pause and confirm nothing got missed) deliberately, per checklist.
  - A checklist item exists to catch a step people easily skip. An item that restates the obvious earns no place on the list.
  - Cap a single checklist at 5-9 items. Past that, split into grouped sub-checklists by phase or component, each with its own pause point.
  - A DO-CONFIRM checklist checks `docs/lessons-learned.md` for entries relevant to its own domain, once per run, not once per split sub-checklist.
- **Trim `writing-skills`' GREEN phase.** Remove "Keywords throughout for search" and "Clear overview with core principle" — both restate general good-writing advice rather than naming a specific, easy-to-skip miss.
- **Split GREEN into two named sub-phases.** "GREEN Phase — Metadata" (name format, frontmatter fields, description wording, description person: 4 items) and "GREEN Phase — Content" (address RED's baseline failures, guidance-form match, the no-guidance-control micro-test, code/example format, re-test with the skill: 6 items).
- **Change the checklist's own instruction from all-at-once to per-phase.** "Create a todo for EACH checklist item below" becomes: at the start of each phase, create a todo only for that phase's items. Complete the phase's work. Confirm against that phase's list. Move to the next phase.
- **Add one lessons-learned check near the top of the whole checklist section**, run once before RED starts: check `docs/lessons-learned.md` for anything relevant to skill-authoring, and apply anything it flags.
- **Wire failure-log sourcing into the fork's other DO-CONFIRM checklists.** `writing-plans`' Self-Review and No Placeholders, and `test-driven-development`'s Verification Checklist each gain one new item: check `docs/lessons-learned.md` for any entry relevant to this checklist's domain, and apply anything it flags.

## Falsifiable Criteria

This spec changes checklist structure and prose, not executable behavior a `--plugin-dir` trial can exercise directly. The falsifiable test stays direct:

1. Grep `writing-skills/SKILL.md` for the six phase headers (RED, GREEN Phase — Metadata, GREEN Phase — Content, REFACTOR, Quality Checks, Deployment). Confirm each groups 9 or fewer items.
2. Grep `writing-skills/SKILL.md`, `writing-plans/SKILL.md`, and `test-driven-development/SKILL.md` for the phrase "check `docs/lessons-learned.md`." Confirm at least one match per file.
3. Confirm "Keywords throughout for search" and "Clear overview with core principle" no longer appear in `writing-skills/SKILL.md`.

## Consequences

`writing-skills`' checklist now runs as six shorter pause points, instead of one 27-item list created at task start. A skill-writer holds fewer items in mind at any one pause. The cost: six explicit stopping points instead of one.

Three other checklists each gain one more item, checking `docs/lessons-learned.md`. This grows each checklist by one item, still inside the 5-9 cap for all three.

Future skill-writers get a written rule to follow, instead of re-deriving checklist discipline from first principles each time a new skill needs one. The rule binds new work going forward. It doesn't retroactively audit every checklist already in the fork — only the three this spec directly touches.

## Deferred

- Auditing every other checklist in Superpowers against this rule — only `writing-skills`, `writing-plans`, and `test-driven-development` get touched here. Revisit if a future review finds a specific oversized or padded checklist elsewhere.
- The WHO Time-Out communication pattern from the user's draft — no strong existing precedent to hang it on in this codebase, per the earlier assessment. Not part of this pass.
- Wiring failure-log sourcing into READ-DO checklists — declined this pass. A fixed-order recipe doesn't fit the same "what do people forget" framing a DO-CONFIRM pass does.
