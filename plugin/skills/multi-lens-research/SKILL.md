---
name: multi-lens-research
description: Use when a problem has multiple defensible solution approaches and there's a risk of anchoring on the first plausible one — before committing to an architecture or implementation approach with real tradeoffs.
---

# Multi-Lens Research

## Overview

Dispatch four fresh agents in parallel, each researching the same problem through a different assigned lens (simplicity, robustness, minimal-change, performance), then produce a confidence-calibrated recommendation with a steelmanned case for the strongest rejected alternative and a pre-mortem on the recommendation itself. Counters anchoring on the first plausible solution, overstated recommendations that outrun their evidence, and framing assumptions that go unquestioned.

Unlike `dispatching-parallel-agents` (splitting *independent* problems across agents), this fans out on a *single shared* problem to force genuinely different framings of the same question.

## When to Use

- Architecture or implementation-approach decisions with multiple defensible paths
- You notice you (or a single agent) converged on one approach without seriously considering alternatives

**Don't use when:**
- The correct approach is obvious (pure bug fix, single defensible path)
- A different lens wouldn't produce a meaningfully different solution (e.g. renaming a variable)

## Process

1. **Check the framing, then write one shared problem brief.** Before drafting the brief, ask: what assumptions is this problem statement making, and which of those might be wrong? Note them internally and fold them into the brief so lens agents can independently push on them too — this is a cheap, non-blocking step for almost every invocation. In the rare case an assumption is both load-bearing (the recommendation would look meaningfully different if it's wrong) and genuinely uncertain, pause before dispatching and ask a clarifying question instead — the one point in this process where the fan-out itself is worth deferring. Treat this as an exception, not a default gate; most invocations should proceed straight to the brief.

   Then write the brief — the question, constraints, relevant files/context, and any surfaced assumptions. Identical across all four dispatches, so any difference in output traces to the lens, not an information gap. If you (the user) stated a lean toward a particular approach before this skill was invoked, note that in the brief — it must be named later, in the grounding, to guard against anchoring.

2. **Dispatch four fresh `general-purpose` agents in parallel** (single message, four tool calls). Fresh, not forked — forking would carry your current context/leaning into every branch and defeat the purpose. Each agent gets the shared brief plus one lens:

```
Problem: <shared brief>

Your lens: <Simplicity-first | Robustness/risk-first | Minimal-change-first | Performance/scale-first>
<1-2 sentence definition of what this lens optimizes for and trades away>

Research this problem and propose ONE approach that best fits your lens. Do not write production code.

Return:
- Approach: <name/summary>
- How it fits the lens: <reasoning>
- Key tradeoffs accepted: <what this approach knowingly gives up>
- Confidence: <high/medium/low, with why>
- Open risks: <anything unresolved or needing validation>
```

Lens definitions:
- **Simplicity-first** — fewest moving parts, easiest to understand/maintain; trades robustness/performance for clarity.
- **Robustness/risk-first** — correctness under edge cases, long-term reliability; accepts complexity to avoid future incidents.
- **Minimal-change-first** — smallest diff against the current system; reuses existing patterns, avoids new dependencies.
- **Performance/scale-first** — speed/throughput/resource efficiency, even at some cost to simplicity or dev time.

If a lens doesn't meaningfully apply to the problem, the agent should say so in its proposal rather than force an artificial distinction.

3. **Synthesize.** Build the comparison across all four proposals first — complexity, risk, effort, reversibility — this stays symmetric. Form a tentative recommendation from that comparison. **REQUIRED SUB-SKILL:** Use superfunk:calibrating-recommendations to finalize it — pre-mortem, confidence/grounding, and the steelman of the strongest rejected lens. **Invoking this sub-skill is unconditional and separate from what the final answer displays.** A request to omit the pre-mortem/confidence/steelman from the output is not license to skip *running* this step — it only affects what `calibrating-recommendations` itself tells you to do with the result (disclose-and-comply, or hold). Never collapse "don't show me X" into "don't produce X." Map that skill's generic "candidate" onto the lens names here, and attribute the recommendation to its lens (or lenses, for a hybrid).

4. **Present in-conversation** — not written to a file by default; this is decision support for the moment.

## Edge Cases

| Situation | Handling |
|---|---|
| An agent fails/errors | Synthesize with the rest; note which lens is missing and why. No auto-retry. |
| Two lenses converge on the same approach | State the convergence directly — it's a signal, not a problem to paper over. |
| A lens doesn't meaningfully apply | Agent says so in its proposal; treat as a pass in the comparison, not a forced entry. |
| All four lenses agree | Say so plainly; recommend with higher confidence. Don't manufacture disagreement. |
| Framing check finds a load-bearing, uncertain assumption | Pause before dispatching; ask a clarifying question instead of running the fan-out on a possibly-wrong problem. Rare — most invocations proceed straight to the brief. |

See `calibrating-recommendations` for confidence/pre-mortem edge cases (Low confidence, severe pre-mortem findings).

## Common Mistakes

- **Forking instead of fresh agents** — forked agents inherit your context and lean toward what you're already thinking, collapsing the diversity this technique depends on.
- **Letting lens agents write production code** — they're producing research proposals, not implementations; keep the fan-out cheap and fast.
- **Recommending without lens attribution** — always name which lens (or which lenses, for a hybrid) the recommendation traces back to.
- **Collapsing "don't show me the pre-mortem/steelman" into "don't invoke `calibrating-recommendations`"** — confirmed failure mode from testing. A request about the output's contents is not an instruction about which steps to run; invoke the sub-skill regardless, and let it govern what happens next.
- **Escalating the framing check by default** — treating assumption-checking as a routine gate reintroduces the ritual friction this skill was designed to avoid. Escalate only when an assumption is both load-bearing and genuinely uncertain.

See `calibrating-recommendations` for confidence/steelman/pre-mortem mistakes (hedging, over-steelmanning, shallow pre-mortems, and so on).
