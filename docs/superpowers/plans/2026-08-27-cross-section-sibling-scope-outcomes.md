# Outcomes — 2026-08-27-cross-section-sibling-scope.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Widen Self-Review item 8's grep scope
Shipped as planned. Spec compliance confirmed exact text match. A code-quality review flagged the widened sentence's length (46 words) and its "if ... names one" construction as new STE violations; both overridden after independent verification found the identical patterns already shipped and approved in precedent (item 8's original 32-word sentence, the carve-out's identical "names one" construction) — fixing only this instance would also have broken parity with Task 2's identical, unedited clause. No fix round dispatched. No other divergence.

## Task 2: Widen the re-review carve-out's grep scope
Shipped as planned. Spec compliance confirmed exact text match. Code-quality review approved clean on first pass — explicitly applied verify-against-precedent-before-flagging itself and confirmed the same construction Task 1's review had flagged (then had overridden) is pre-existing house style, not a new defect. No fix round, no divergence.

## Task 3: Live trial for item 8's sibling-directory scope
Shipped as planned; the trial correctly triggered item 8's pattern, explicitly enumerated and checked the sibling file (not just the edited target file), and correctly cited the sibling's contradicting line. The trial also surfaced two unprompted secondary observations (the fixture's proposed edit was internally self-contradictory on its own "always" qualifier, and a real fix would need to touch the sibling file too) — noted as evidence of thorough engagement, not a fixture defect, since the trial's actual job (does the widened grep reach the sibling) was met regardless. No divergence, no follow-ups.

## Task 4: Live trial for the carve-out's sibling-directory scope
Shipped as planned; the trial correctly triggered the carve-out's pattern, explicitly enumerated and checked the sibling file, and filed the sibling contradiction as New Breakage (not Out-of-Scope), citing the exact contradicting line. Independently surfaced the same "always" self-contradiction Task 3's trial had also caught, in a completely separate fixture/session — corroborating evidence the fixture's design flaw is real and consistently detected, not a fluke of one trial. No divergence, no follow-ups.
