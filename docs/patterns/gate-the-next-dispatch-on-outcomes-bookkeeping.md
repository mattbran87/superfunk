# Gate the next dispatch on controller-owned bookkeeping that has no loud downstream failure

Do not rely on a reminder or an explicit instruction to make the controller perform bookkeeping with no loud downstream failure mode. Require a mechanical, checkable gate before the next dependent action proceeds.

## Context

Some steps in `subagent-driven-development`'s process are controller-owned bookkeeping: nothing an implementer or reviewer subagent does depends on them completing correctly, and skipping them produces no error, no failed test, no blocked review. Per-task outcome capture (creating and committing `docs/superpowers/plans/<plan-basename>-outcomes.md` after each task) is exactly this kind of step. Task dispatch works fine without it. The controller gets no signal that anything is missing until someone reads the file later and finds it empty, stale, or reconstructed after the fact.

Stating the check as "its own explicit visible line" in a skill file is necessary but has already been shown insufficient on its own — the same controller missed the mechanism a second time, in the very sub-project whose own design argued that explicit visibility prevents exactly this failure mode, after receiving a direct instruction naming the mechanism at the start of the session.

## Pattern

For controller-owned bookkeeping with no downstream consumer that fails loudly if skipped:

1. Identify a mechanically checkable precondition that proves the bookkeeping happened — not "did you remember," but a fact you can grep or `git log` for (a specific file exists, a specific commit exists, a specific line was appended).
2. Make that precondition a blocking gate on the next dependent action, not a reminder before it. For per-task outcomes: do not dispatch Task N+1's implementer until `git log --oneline -1 -- docs/superpowers/plans/<plan-basename>-outcomes.md` shows a commit whose content matches Task N's completion.
3. If the precondition fails, stop and perform the missed bookkeeping before proceeding — don't let the gap accumulate into a batch to reconstruct later, which produces a plausible-looking but fabricated record (an "Outcome" entry describing information the implementer's own report never contained).
4. Prefer this gate pattern over adding more reminder text, more explicit instructions, or restating the mechanism's importance — none of those changed behavior the second time either.

## Example

- A design spec explicitly named the risk of a Finish-step mechanism getting missed if not stated as its own visible line, and built its own new mechanism (concept-index maintenance) with that visibility in mind. In the same sub-project, executing that very plan, the controller — despite an explicit start-of-session instruction citing the exact prior failure — again deferred a different mechanism (per-task outcomes) for three tasks before noticing and reconstructing the missing entries after the fact from review history, not from real-time implementer reports. Visibility of the instruction did not prevent the recurrence; only noticing after the fact did.

## Originating lessons

- "Follow this project's own outcomes-file mechanism when executing subagent-driven-development, or its own author misses it first" (2026-08-24-review-recommendations-followup)
- "An explicit reminder does not stop controller-owned bookkeeping from being deferred; only a blocking gate does" (2026-08-25-concept-index)
