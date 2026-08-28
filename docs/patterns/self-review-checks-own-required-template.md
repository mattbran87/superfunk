# A Self-Review needs a check verifying the document matches its own required template

When a skill's own instructions define a required document structure — a header template, a mandatory field, a required section — that skill's Self-Review needs an explicit item checking the produced document against that structure.

## Context

A skill can accumulate many Self-Review items checking content quality (spec coverage, placeholder scans, cross-section consistency, worked-example currency) while never checking the one thing closest to home: does the document this skill just produced actually match the skill's own stated required shape? A required section can sit in the skill's own instructions, unenforced, for a long time — every use of the skill omits it, and nothing catches the omission, because the checks that exist all look outward (at the spec, at sibling files, at other documents) rather than inward (at the document's own conformance to its own template).

## Pattern

When designing or auditing a Self-Review checklist, add one item asking: does the produced document match every required element its own generating skill's instructions define (a required header, a mandatory field, a required section)? This is different from content-quality checks — it verifies structural compliance, not correctness of what's written.

## Example

- `writing-plans/SKILL.md`'s required Plan Document Header has included a `## Global Constraints` section since before this fork existed. Every plan written across an entire session omitted it, because the skill's 9-item Self-Review checked spec coverage, placeholders, type consistency, pseudocode, sibling parity, rule restatement, lessons-learned, cross-section consistency, and worked-example currency — but never checked the plan's own header against the template the same skill's own instructions require. The gap surfaced only by accident.

## Originating lessons

- "A required template section survives unenforced when the tool that writes documents never checks its own output against its own template" (2026-08-28-documentation)
