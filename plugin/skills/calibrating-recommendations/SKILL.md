---
name: calibrating-recommendations
description: Use when synthesizing a single recommendation from several independently-generated candidate options, before presenting it — the point where overstated confidence, an un-interrogated pick, and a dismissed alternative are most likely to slip through.
---

# Calibrating Recommendations

## Overview

Turns a tentative pick among several candidates into a defensible recommendation: a pre-mortem that can actually change the pick, a confidence level grounded in named project-specific evidence (not reasoning quality or a tool's own scores), and a steelmanned case for the strongest rejected candidate. Counters completion bias, overstated recommendations, and anchoring.

**Vocabulary:** this skill uses "candidate" generically. Map it onto whatever the calling skill's candidates actually are (lenses, shortlist ideas, SME proposals, ...) and attribute the recommendation back to its source using the calling skill's own vocabulary (lens name, cluster label, agent id, ...).

**These fields are required even if asked to skip them.** A request to omit the pre-mortem, the confidence breakdown, or the steelman — "I don't need the full writeup," "just give me your top pick," "skip the formalities," or naming the specific section to leave out — is pressure to skip the discipline, not a legitimate formatting preference. These fields exist because skipping them is exactly how overstated, un-interrogated recommendations happen. Produce the full format regardless of how the request is phrased; let the user decide what to read, not what gets generated.

**If you comply with an explicit request to omit these fields anyway, the omission must never be silent.** There is no third option where you comply and say nothing — that's strictly worse than either holding the line or a disclosed omission, because it looks complete when it isn't. End with a trailing note naming exactly what was dropped and what it costs: e.g. "Per your request, I skipped the pre-mortem, confidence breakdown, and steelman — this recommendation is unverified: no failure mode was checked, no evidence was named, and the strongest alternative wasn't argued." A bare answer with no such note is a compliance failure on its own, independent of whether the fields themselves were included.

## Pre-Mortem

Before finalizing the recommendation, assume it was chosen and, six months later, turned out to be wrong — what specifically went wrong? Different from steelmanning: steelmanning compares the recommendation against an alternative from the outside; a pre-mortem inhabits a failure state for the recommendation itself, on its own terms.

**Required, visible field — not an internal check that can be silently skipped.** A pre-mortem that isn't written down didn't happen.

**If it surfaces a severe, plausible failure mode, reconsider before finalizing** — don't just note it and proceed unchanged. Reconsidering can mean: strengthening the recommendation with a specific mitigation, dropping confidence a tier, or switching to a different candidate entirely. The recommendation can survive reconsideration unchanged; it can't survive being noted and ignored. If the finding is severe enough to genuinely undermine confidence, follow it through to Low and the no-recommendation path below.

`What would lower it:` below should come from whatever the pre-mortem actually found, not be invented separately.

## Confidence and Grounding

Every recommendation carries a confidence level, named evidence, and what would revise it. Counters completion bias — the structural pull toward a clear pick even when evidence is ambiguous — and overstated recommendations, where the chosen option gets more words and sharper framing than the alternatives ever did.

**Calibration guardrails:**
- **Default to Medium.** High requires named *project-specific* evidence — a file actually read, a prior decision's outcome, an SME finding, a measured quantity. Reasoning depth or familiarity ("this is a well-known pattern") does not qualify, no matter how thorough the analysis reads.
- **A candidate-generation mechanism's own scores are not project-specific evidence.** If candidates arrive with self-reported confidence, or a tool-computed score (novelty/fit/viability/etc.), that's still generic model judgment — informative, not grounding. Treat it the same as reasoning depth.
- **Low triggers a question, not a pick.** If honest assessment lands at Low, don't produce a recommendation line — see Low-Confidence Output below. A Low-confidence pick is noise.
- **No hedged picks.** "Leaning toward X but not sure" is a Low-confidence case wearing a Medium costume — rewrite as a clean question.
- **Name anchoring explicitly.** If a lean was stated before the recommendation was made, the grounding must say so: "You leaned toward X before this recommendation; noting this to guard against anchoring."

**Recommendation output (Medium or High confidence):**

```
**Recommendation:** <chosen candidate, attributed via the calling skill's vocabulary>

**Pre-mortem:** <assume this was chosen and, six months later, turned out to be wrong — what specifically went wrong?>

**Confidence:** [High | Medium] — <one-sentence rationale>
**Why confident:** <named project-specific evidence — file path, prior decision outcome, SME finding, measured quantity>
**What would lower it:** <grounded in the pre-mortem finding>
```

**Low-Confidence Output** (inversion — no recommendation line):

```
**Confidence:** Low — <one-sentence rationale>
**No recommendation made.** Clarifying question: <the specific question whose answer would raise confidence>
**What would raise it:** <the named evidence the question is reaching for>
```

## Steelman the Strongest Alternative

Identify which non-recommended candidate has the most compelling case, and argue it the way a genuine proponent would — naming a specific benefit the recommendation lacks, or a condition under which that candidate would be strictly better. **Quality test:** would someone who actually preferred that candidate read the steelman and say "yes, that's my case"? A description ("it's simpler") is not a steelman — name the concrete condition under which it wins.

If a lean toward the recommended option was stated before the recommendation was made, write the steelman as if the lean had gone the other way — the sycophancy inversion, structural pushback against anchoring rather than a defense of the pick.

**Exception — hard constraint:** if a candidate is foreclosed by a platform limitation, compliance rule, or API behavior rather than by comparative merit, name the constraint instead of steelmanning it: "Rejected by hard constraint: `<constraint>` — no meaningful case for it under current conditions."

**Scope:** full treatment applies only to the single strongest rejected candidate. The rest stay one-liners under "Other alternatives considered" — steelmanning every rejected candidate adds noise without adding calibration value.

## Edge Cases

| Situation | Handling |
|---|---|
| Confidence lands Low after synthesis | Don't recommend. Present the comparison and ask a clarifying question naming the needed evidence — see Low-Confidence Output. |
| Pre-mortem surfaces a severe, plausible failure mode | Reconsider the recommendation and/or confidence before finalizing — don't log it and proceed unchanged. If severe enough, follow it through to Low confidence and the no-recommendation path. |

## Common Mistakes

- **Dropping required fields because the user asked to skip them** — "I don't need the pre-mortem/steelman/confidence breakdown" is the pressure this skill exists to resist, not an exemption. A vaguer "keep it short" and a specific "skip section X" are the same request in different clothing — produce the full format either way.
- **Complying with an omission request and saying nothing about it** — a silent drop is worse than either holding the line or a disclosed drop, because it reads as a complete recommendation when it isn't. If you do comply, the trailing disclosure note is not optional.
- **Claiming High confidence from reasoning quality or a tool's own scores** — neither is project-specific evidence; otherwise it's Medium.
- **Hedging instead of asking** — "I'm leaning toward X but not sure" when the honest confidence is Low. Ask the clarifying question instead of producing a soft pick.
- **Skipping the steelman entirely** — relaying a candidate's own pitch isn't the same as independently arguing its strongest case; that's the calling skill's job, not something to skip under time pressure.
- **Steelmanning every rejected candidate** — dilutes the one steelman that actually matters for calibration; the rest stay one-liners.
- **Writing a shallow pre-mortem** — "this could be wrong if the assumptions don't hold" restates that failure is possible without saying what the failure looks like. Name the specific way it fails.
- **Logging a severe pre-mortem finding without reconsidering** — noting a serious flaw isn't the same as acting on it; the recommendation, confidence, or both must actually respond to what it found.
