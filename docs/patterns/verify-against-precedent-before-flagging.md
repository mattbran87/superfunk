# Verify against source intent and existing precedent before flagging a literal rule-match as a defect

When a review finding cites a stated rule literally, check the rule's source intent and existing shipped precedent before treating the match as a real defect.

## Context

A review (spec-compliance, code-quality, or holistic) sometimes finds something that technically matches a stated rule's literal wording — a number outside a range, a tag that doesn't match a sibling's tag, a section missing detail another section has. Applied literally, each of these reads as a defect. But the rule itself often has a narrower intent than its literal wording suggests, and the same pattern may already exist elsewhere in the codebase without complaint.

## Pattern

Before treating a literal rule-match as a real defect:
1. Find the rule's original source (the draft, spec, or design doc that motivated it) and read what it actually says the rule exists for, not just its summary.
2. Search for the same pattern already shipped elsewhere in the codebase. If it exists and got approved, the finding is likely a misreading, not a defect.
3. Only escalate the finding as real once both checks come back empty-handed — no clarifying source intent, no existing accepted precedent.

## Example

- A code-quality review read `docs/code-standards.md`'s "5-9 item cap" as a floor-and-ceiling range and flagged a 4-item checklist group as non-compliant. The source draft's own text ("Keep a single checklist to 5-9 items — the limit of working memory... rather than inflating a single list past the point anyone can hold it in mind") frames it as ceiling-only. Two already-shipped sub-checklists (3 items, 2 items) confirmed the real, accepted practice.
- A separate review flagged one bullet's `[Rule]` tag as inconsistent with another bullet's `[Preference]` tag, based on both being "about making a decision." Reading each bullet's actual role (one a primary required decision, the other an explicit soft fallback "when the distinction feels unclear") showed they weren't the same kind of guidance at all.
- A third review asked for concrete examples in a lessons-learned-check instruction, without checking that the identical open-ended phrasing already shipped, approved, in two other files for the same category of check.

## Originating lessons

- "Verify a code-quality finding against source intent and existing precedent before treating a literal rule-match as a defect" (2026-08-20-checklist-construction)
