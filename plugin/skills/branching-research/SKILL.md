---
name: branching-research
description: Use when a problem needs wide creative divergence before a calibrated recommendation, but you want the generation and critique steps done natively (no external tool dependency) with full visibility into the framing prompts.
---

# Branching Research

## Overview

Native tree-of-thought: dispatch fresh agents under distinct cognitive frames to generate divergent ideas with evaluation forbidden, dispatch a separate critic agent to score/cluster/trap-tag them, then apply `calibrating-recommendations` to reach a defensible pick. Same shape as `adhd-research`, without the external CLI dependency — full control over the frame prompts, no black-box degenerate runs, direct tuning when something's off.

**vs. `adhd-research`:** same synthesis discipline, different generation engine — this one is fully native `Agent` dispatches instead of a shell-out. **vs. `multi-lens-research`:** that skill's four lenses are fixed engineering tradeoffs; this skill's frames are drawn from a broader library (below) and selected per-problem, better suited to naming/strategy/fuzzy-debugging problems where the right angles aren't obviously the four tradeoff dimensions.

## When to Use

- Fuzzy debugging, naming, API surface design, strategy — problems where breadth matters more than a fixed comparison grid
- You want `adhd-research`'s shape without installing/depending on the external tool
- The four fixed lenses in `multi-lens-research` would feel forced for this problem

**Don't use when:** the correct approach is obvious, or the problem is a clean architecture/implementation-approach tradeoff where `multi-lens-research`'s fixed lenses fit better.

## Frame Library

Select 4-5 per problem — mix at least one **grounded** frame with at least one **boundary-pushing** frame. All-comfortable framing misses real risks; all-adversarial framing produces a shortlist with nothing viable to recommend.

| Frame | Prompt | Type |
|---|---|---|
| Prior art | "How do established, widely-used systems solve this? Name the specific precedent." | Grounded |
| Minimal-surface | "What's the smallest, most conventional solution an experienced practitioner would immediately recognize?" | Grounded |
| Hardware/systems | "Re-pose this as a hardware/physical-systems problem — latency, memory, physical constraints." | Grounded |
| Observability/operator | "Re-pose this from the perspective of whoever debugs this at 3am — what do they need to see?" | Grounded |
| Regulator/compliance | "Re-pose this as a compliance/audit problem — what needs to be provable, traceable, defensible?" | Grounded |
| Game-design | "Re-pose this using game-economy or multiplayer metaphors." | Mixed |
| Child's mental model | "Explain this to a smart 10-year-old with no domain background." | Mixed |
| Adversary | "How would this be deliberately broken or exploited? Generate ideas that make it fail." | Boundary |
| Inversion | "Invert the core assumption — what does the opposite of the obvious approach look like?" | Boundary |
| Remove-assumption | "What is this problem taking for granted? Remove it and re-solve." | Boundary |

Boundary frames often produce ideas that get trapped by the critic — that's expected and still valuable: a trapped idea with a named mechanistic reason confirms the safer frames' direction, the same way it did repeatedly in `adhd-research` testing.

## Process

1. **Check the framing** — same discipline as the other two research skills: surface load-bearing assumptions, escalate to a clarifying question only if one is both load-bearing and genuinely uncertain.

2. **Select 4-5 frames** from the library above for this specific problem, honoring the grounded/boundary mix.

3. **Dispatch fresh frame-agents in parallel** (one message, N `Agent` calls, `subagent_type: general-purpose`, fresh not forked). Each gets the shared problem brief plus one frame:

```
Problem: <shared brief>
Frame: <frame prompt from the library>

Generate 4-6 distinct ideas from this frame. Do not evaluate, rank, rate, or hedge — pure generation. For each idea: the idea itself, and a one-sentence rationale for why this frame produced it.
```

4. **Dispatch one critic agent** over all frame-agents' combined output — a separate call, not the main agent reasoning inline. This mechanical separation is load-bearing: it keeps the generator's own framing from bleeding into its evaluation.

```
Here are N ideas generated under forbidden-evaluation frames for: <problem>
<all ideas, with their frame and rationale>

Score each on novelty/viability/fit (0-10). Tag any idea that looks good but mechanically isn't, with the specific reason. Cluster ideas by underlying angle, not surface keywords. Identify the shortlist (2-4 highest combined-merit, non-trapped ideas) and the non-obvious pick (highest-novelty viable idea, even if not top-scored).

Do NOT produce a recommendation, pre-mortem, confidence level, or steelman — critique only. That synthesis happens in a separate step, by a different process, after your output. Stop at the shortlist.
```

If the critic's response includes a recommendation/pre-mortem/confidence/steelman anyway, discard that portion — use only its scores, clusters, trap tags, and shortlist as input to the next step. Do not treat a critic's freelanced recommendation as the real calibrated answer.

5. **Form a tentative recommendation from the shortlist. REQUIRED SUB-SKILL:** Use `calibrating-recommendations` to finalize it — pre-mortem, confidence/grounding, and the steelman of the strongest rejected shortlist item. **Invoking this sub-skill is unconditional and separate from what the final answer displays** — a request to omit its output is not license to skip running this step; only `calibrating-recommendations` itself governs what happens with the result. Never collapse "don't show me X" into "don't produce X." Map its generic "candidate" onto shortlist items, and attribute the recommendation to its cluster.

6. **Present in-conversation** — not written to a file by default.

## Edge Cases

| Situation | Handling |
|---|---|
| All ideas get trapped (degenerate shortlist) | Don't force a pick from rejected material. Re-run with tighter framing or added grounding context before shortlisting — same recovery `adhd-research` testing validated. |
| A frame doesn't produce anything useful for this problem | Note it and treat as a pass, same as an inapplicable lens elsewhere. |
| Critic agent fails | Don't fall back to the main agent scoring inline — that reintroduces the bleed the separate critic exists to prevent. Re-dispatch the critic once; if it fails again, say so rather than fabricating scores. |
| All shortlist items land in one cluster | State the convergence directly — a signal, not a comparison problem to paper over. |

See `calibrating-recommendations` for confidence/pre-mortem edge cases.

## Common Mistakes

- **Letting frame-agents evaluate their own ideas** — the prompt forbids it for a reason; evaluation happens once, in the critic, or the mechanical separation collapses back into ordinary in-context ToT.
- **Doing the critic's job inline instead of dispatching it** — same collapse, from the other direction.
- **Trusting a critic that freelances into recommendation/pre-mortem/steelman territory** — confirmed failure mode from testing; critics sometimes over-deliver even when explicitly told to critique only. Discard that portion and use only the legitimate scoring/clustering/trap output as input to `calibrating-recommendations`.
- **All-grounded or all-boundary frame selection** — either misses real risk or produces a shortlist with nothing shippable.
- **Collapsing "don't show me the pre-mortem/steelman" into "don't invoke `calibrating-recommendations`"** — confirmed failure mode from `adhd-research` testing. A request about the output's contents is not an instruction about which steps to run.
- **Forking frame-agents or the critic** — inherits context/leaning, defeats the isolation the whole technique depends on.

See `calibrating-recommendations` for confidence/steelman/pre-mortem mistakes.
