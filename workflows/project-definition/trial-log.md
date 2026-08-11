# Trial Log — Project Definition Skill

**Stage:** 4 — Trials + Trial Log

Append-only. Add a new entry per trial; do not edit past entries.

## Trial 1

<!-- Add one "## Trial N" heading per trial, incrementing N. Never edit a previous entry's fields. -->

**Date:** 2026-08-11
**Environment:** Synthetic test project (small fake codebase, three module-like directories: `auth`, `billing`, `api`)
**Driver:** Autonomous agent run
**Outcome:** An isolated `claude -p` session, given the skill and a fake project persona for interview answers, chose the lightweight tier and produced exactly one file at `docs/architecture/project-definition.md`, holding exactly the three specified sections in the specified order. Independent verification confirmed every module, file, and relationship described in the Building Block View matches the actual codebase, including an accurate, non-fabricated observation that `auth` and `billing` don't call each other yet in the current code. No modules got invented. Criteria 1 and 2 both pass.
**Friction:** `claude -p` runs single-shot, but the skill's interview steps assume a multi-turn conversation. The trial worked around this by supplying the fake project's goals and constraints up front in the prompt, instructing the agent to answer its own interview questions from that context rather than pausing to ask. This is a testing-methodology limitation, not a defect in the skill itself — a real interactive session would ask these questions turn by turn. Worth noting for future trials of this skill: a hands-on driver may be more faithful for any scenario specifically testing the interview *experience*, not just its output.

## Trial 2

**Date:** 2026-08-11
**Environment:** A completely empty directory, with only the Building Block View section (extracted from Trial 1's output) passed in the prompt text -- no codebase, no other section, no other context
**Driver:** Autonomous agent run
**Outcome:** This trial corresponds to Test Plan row 3 (module-assignment). Given a hypothetical feature request -- "add a refund processing feature that reverses a completed payment and updates the invoice status" -- the fresh session correctly named `src/billing`, reasoning that the feature touches both `payment.js` (money movement) and `invoice.js` (status), both already billing's stated responsibility. This matches what someone with full codebase knowledge would decide. Criterion 3 passes.
**Friction:** None. Reusing Trial 1's generated Building Block View for this trial, rather than generating a fresh one, kept the two trials cleanly separable while still testing a real generated document, not a hand-crafted one.

## Trial 3

**Date:** 2026-08-11
**Environment:** Fresh copy of the same synthetic codebase
**Driver:** Autonomous agent run
**Outcome:** This trial corresponds to Test Plan row 2 (full tier). An isolated session produced exactly 12 files under `docs/architecture/`, correctly named and numbered, matching the skill's specified section list exactly -- no extras, none missing. Content quality exceeded expectations: Architecture Decisions correctly detected that no `specs/<module>/<feature>/decisions.md` files exist anywhere in this test repo and said so explicitly, rather than fabricating decision history, then correctly captured only the project-level decisions actually given in the interview context. Building Block View independently identified a "Notable Absences" section -- no persistence layer, no product/order module despite the project's stated purpose, no middleware -- an accurate observation the skill was never explicitly told to make. Quality Requirements correctly synthesized the interview priorities into ranked goals with concrete, arc42-appropriate quality scenarios. Criteria 1 and 2 both pass, with stronger evidence than Trial 1 gave for the lightweight tier alone.
**Friction:** None found in the output. The trial itself took noticeably longer than the lightweight-tier trial (12 sections' worth of exploration and interview synthesis vs. 3), which is expected and not a defect, but worth noting for anyone running this skill for real: full arc42 generation is a genuinely long single session.

## Trial 4

**Date:** 2026-08-11
**Environment:** Synthetic test project with `docs/architecture/project-definition.md` already generated (from Trial 1), one section hand-edited before the skill ran again
**Driver:** Hands-on
**Outcome:** This trial corresponds to Test Plan row 4 (update mode). A distinctive line, marked as a human hand-edit, got added to the existing Constraints section: a claim about a legacy SOAP inventory integration that appears nowhere in the actual codebase. The skill got asked to update Constraints specifically. It re-explored the codebase, detected that the SOAP line matched no evidence in the source or the given interview context, and explicitly refused to overwrite it -- it printed the proposed replacement, named exactly what would change (the SOAP line dropping out), asked which of three options to take, and stated plainly that it had not modified the file yet. Independent verification (`grep` for the marker, checked the file's modification timestamp) confirmed the file was untouched. Criterion 4 passes.
**Friction:** None. This is the cleanest possible pass on this criterion -- the skill did exactly what Step 6 of `SKILL.md` specifies, and did it without any prompting beyond the trial's own instructions.

