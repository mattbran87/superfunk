All seven self-review checks are done, with every numeric claim and quote re-verified against real command output. Here is what the review produced.

## Findings

**1. A third lineage exists, and it's the one that actually runs. (blocking)**

The spec's Context enumerates two copies of the skills — `plugin/skills/` and `~/.claude/skills/` — and Consequences builds its risk analysis on exactly that pair ("Two copies of three skills exist until superfunk installs globally"). A third exists at `C:\sf-bcv-plugins\arm1\skills\`, and it is where this session's `superfunk:brainstorming` loaded from.

It is not a copy of the repo. It holds 22 skills, including all three the spec proposes to "adopt," and it is not a git repository. Against `plugin/skills/brainstorming/SKILL.md` it already contains partial versions of two of the six decisions:

- Line 27 already carries a revised step 4 (confidence + project-specific evidence + dispatch a research skill) — the repo's is still bare.
- Line 148 already makes the `Alternatives Considered` branch reachable, with a short form of "the candidates, and the recommendation with its confidence and the named evidence behind it" — no do-nothing option, no flip factor.

Most consequentially, `C:\sf-bcv-plugins\arm1\.claude-plugin\plugin.json` already reads **`6.3.0`** — the exact version Decision 1 proposes bumping to and Falsifiable Criterion 8 asserts. Shipping this spec creates two different 6.3.0 releases with different content.

This falsifies three Context statements as written: "The plugin contains neither skill," "Superfunk installs nowhere today and reaches sessions only through disposable trials," and the two-lineage framing in Consequences. It also weakens Criteria 1–8, which all target `plugin/skills/` and would pass while the skills that actually load stay divergent. The direction of drift — whether arm1 is upstream of the repo or a parallel arm — is not determinable from the files, so this needs your decision rather than an inline fix.

**2. The spec violates its own Decision 4.** Decision 4 requires an `Alternatives Considered` section in "every spec that records a choice between approaches." This spec records at least three: copy the skills vs. move them, ship `adhd-research` vs. leave it at user level, and where the null option lives (`multi-lens-research` step 3 vs. a lens). It has no such section. The "This spec demonstrates the gap" paragraph justifies the omission, but only under the pre-change `:139` rule — under the arm1 wording already in force, and under the spec's own new rule, the section is required. As written, this spec becomes the first violation of the rule it introduces.

**3. `**Status:** Draft` is off-vocabulary.** The brainstorming skill permits `Proposed`, `Approved`, or `Superseded by <filename>`, and says never a free-text description. `Draft` is none of these. The other 43 specs read `Shipped`.

**4. Falsifiable Criterion 2 already passes.** `grep -rn adhd plugin/skills/` returns zero matches right now, before any implementation. The criterion cannot distinguish work done correctly from work not done at all; it needs conditioning on Criterion 1.

**5. Falsifiable Criterion 3 names a mechanism with no artifact.** It requires the reference check be "checked by script rather than by reading," but the spec creates no script and names no path — the Mechanisms, Not Goodwill shape the spec itself criticizes in step 4.

**6. Falsifiable Criterion 9 is under-specified.** The A/B trial names no prompt, no sample size (one run per arm, against a stochastic model), and — given finding 1 — no answer to which directory `--plugin-dir` points at.

## Checks that came back clean

Every numeric and citation claim verified against real output, not recall: 43 prior shipped specs with zero `## Alternatives Considered` headings (44 files, 43 `Shipped`, this one `Draft`); 19 plugin skills + 5 user skills = 24; `adhd-research` on exactly lines 10, 12, 17, 39, 77, 90 of `branching-research/SKILL.md`, splitting into positioning and provenance groups exactly as Decision 2 describes, with line 12 carrying the `vs. multi-lens-research` comparison; `6.2.0` in both repo manifests; and line cites `:27`, `:139`, `writing-plans:270-278`, `multi-lens-research:29`. Both quotations are exact: "confirmed failure mode from `adhd-research` testing" and "real evidence over vibes." Decision 2's claim that no other reference in the three files fails to resolve holds — the only backticked names are `adhd-research`, `calibrating-recommendations`, `multi-lens-research`, `dispatching-parallel-agents`, and `general-purpose`. `docs/architecture/` does not exist, confirming the Deferred item. Scope is a coherent single theme across five files.

## What I did not do

I made no edits. Findings 3, 4, and 5 are mechanical and I can fix them inline on your word. Findings 1 and 2 change the spec's premise — finding 1 in particular determines whether `plugin/skills/` is even the right target — so they need your call before I touch the file. No implementation plan written.
