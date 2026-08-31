# Checkpoint Priority and Conditional Gate — Design

**Date:** 2026-08-30
**Status:** Shipped
**User-Facing:** No

## Context

The external bookmark-cli trial's D5 and D7 findings, the last two unaddressed from the whole trial, both concern conversational behavior the trial itself flagged as the least certain to hold, since neither names a mechanical check — both shape what the agent says in a turn, not what a script verifies.

**D5 — a skill-mandated checkpoint consumes the whole turn, dropping direct user questions.** At the end of brainstorming, the spec Self-Review reported "three genuine ambiguities" and listed two. The user asked to name the third. Two consecutive turns — one running `writing-plans`, one firing SDD's worktree consent gate — produced checkpoint output with no acknowledgment of the question at all, verified against the full transcript, not just `-p`'s last-message output. Only a third, explicitly-flagged ask got answered. The framework's own later diagnosis (trial transcript line 304): "my first two answers were buried under gate output." `using-superpowers`' current "User Instructions" section states that user instructions take precedence over skills, but says nothing about a question arriving *inside the same message* as an approval — the gap D5 actually hit.

**D5's contributing defect** — the Self-Review step that miscounted its own findings ("three" stated, two listed) created the ambiguity the user then had to chase across three turns. A self-review whose summary doesn't get checked against its own body produces exactly this kind of confusion.

**D7 — brainstorming's per-section gate is unconditional, so blanket consent decays.** After giving blanket consent twice (turns 19 and 21), turn 23's response still closed with "Does this look right? If so I'll write the spec, then take it through plan, worktree, execution and merge without stopping" — the same question a third time. The trial itself names the partial defense: that same message surfaced a genuinely new decision (widening a bug fix's scope), and pausing for *that* specific decision made sense. The defect is narrower than "always stop" or "never stop" — the gate doesn't distinguish "I need a ruling on something new" from "the template says to check in," so it asks unconditionally even when nothing new has come up.

## Decision

**`using-superpowers/SKILL.md`'s "User Instructions" section gains one paragraph**, appended after the existing paragraph:

```markdown
## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.

If the user's message carries a question or request alongside an
approval or consent, answer or address it in the same response —
before or alongside any mandated checkpoint or gate output. A
checkpoint's own template text is not a reason to drop something else
the user just asked; a pending question outranks emitting the
checkpoint verbatim.
```

**`brainstorming/SKILL.md`'s Spec Self-Review gains one closing sentence**, inserted before the existing "Fix any issues inline" line:

```markdown
docs/patterns/re-verify-quotes-against-source-before-citing.md for
the specific failure shapes a plausible-looking citation has actually
hit before.

Before reporting these findings to the user, verify any count you're
about to state (e.g., "three ambiguities") actually matches the list
you give right after it — a count that overstates or understates its
own list creates the exact gap this step exists to close, and it's
what the user will ask about first if it's wrong.

Fix any issues inline. No need to re-review — just fix and move on.
```

**`brainstorming/SKILL.md`'s per-section gate bullet becomes conditional**, changing from:

```markdown
- Ask after each section whether it looks right so far
```

to:

```markdown
- Ask after each section whether it looks right so far — unless the
  user already gave blanket consent covering this stage, or the
  section only restates a decision the user made explicitly earlier.
  In either case, state the section and continue without re-asking.
  If the section introduces a decision the user hasn't made yet, ask
  about that specific new decision even under blanket consent —
  consent covers decisions already settled, not ones that haven't
  come up.
```

## Falsifiable Criteria

1. A direct read-through of `using-superpowers/SKILL.md`'s "User Instructions" section confirms the new paragraph exists, worded identically to the Decision block above.
2. A direct read-through of `brainstorming/SKILL.md`'s Spec Self-Review confirms the new sentence exists, worded identically to the Decision block above, positioned before "Fix any issues inline."
3. A direct read-through of `brainstorming/SKILL.md`'s per-section gate bullet confirms it matches the Decision block's conditional wording exactly.
4. A disposable `--plugin-dir` trial drives a multi-turn session where the user's message combines an approval with an unrelated question, immediately followed by a turn that would otherwise fire a mandated checkpoint (a worktree consent gate or an execution-options prompt). The response answers the question in that same turn, not just the checkpoint.
5. A second disposable trial gives blanket consent covering a multi-stage chain, then continues into a section that introduces no new decision. The response states the section and continues without re-asking "does this look right." A third trial section that does introduce a new decision still gets a targeted question about that decision specifically.

## Consequences

A future session holding a pending user question no longer risks losing it under two consecutive turns of mandated checkpoint output — closing the exact gap that made the trial's own operator ask the same question three times before getting an answer. A future session under blanket consent stops re-asking settled ground while still surfacing genuinely new decisions as they arise, closing the gap that made three consecutive approvals of the same chain read as the tool not listening.

Both fixes touch conversational behavior rather than a scripted check, so verification relies on live-trial behavior rather than a deterministic grep — the trial's own framing of these two findings as "the least certain to hold" stays true after this fix ships; a live trial confirms the mechanism fires in the tested scenario, not that it holds universally across every future conversation shape.

## Deferred

- None — this closes the last two findings from the external bookmark-cli trial's full list.
