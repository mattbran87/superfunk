# Enumerate lists to their structural end, not to a line range or an expectation

An enumeration bounded by anything other than the structure's own terminator undercounts silently, and the undercount reads as a complete result.

## Context

Any task that claims to have examined every member of something: a rule-membership check over a spec's lists, a mirror of another document's step list, a Rule-sentence comparison during lesson promotion, a trial arm comparing entries across files. The failure shape recurs because partial reads look identical to complete ones — nothing in a 17-member output announces that the source held 25.

## Pattern

1. Before enumerating, name the structure's own terminator: the section's closing heading, the file's end, the list's final delimiter. "Read lines 556–639" or "read until the members I expected appear" does not bound an enumeration — the structure does.
2. Produce an independent mechanical count of candidate members (a grep count, a delimiter count) and reconcile it against the enumeration's own count before using the result. A mismatch means the enumeration is incomplete, whatever it looks like.
3. Watch the line-wrap trap specifically: members that sit mid-paragraph defeat line-anchored extraction. Join paragraphs (or search wrap-insensitively) before counting.
4. Treat "I already enumerated this once" as no exemption — a second enumeration of the same list bounded the same wrong way misses the same members, plus different ones.

## Example

- One spec enumerated SDD's Finish section three times while designing a mirror of it. The first read (a line range) missed concept-index; the second, "full" read missed the bug-tracking sweep, workspace deletion, and the finishing-skill invocation, because it stopped at the previous read's end. Only reading to the section's structural end (`## Common Rationalizations`) produced the true nine-member list — the spec's "complete" enumeration was wrong twice in a row.
- The same batch's Finish step extracted Rule sentences with a single-line grep and got 23; the file's own `**Rule:**` line count said 30. The seven missing rules wrapped before their first period. The count reconciliation caught it before the comparison ran on a short list.
- Two earlier trial arms compared 17 of 25 and 16 of 17 Rule sentences and recorded the undercounts as execution defects — same shape, recorded before this pattern existed.

## Originating lessons

- "An enumeration bounded by a line range or an expectation undercounts silently" (2026-09-02-process-review-batch-r1-r4)
