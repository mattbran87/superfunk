# Research Skill Adoption — Design

**Date:** 2026-09-01
**Status:** Draft
**User-Facing:** Yes

## Context

`plugin/skills/brainstorming/SKILL.md:139` instructs the agent to capture an
`Alternatives Considered` section when `multi-lens-research` or
`branching-research` ran for a decision, and to skip the section otherwise.
The plugin contains neither skill. Both live only in `~/.claude/skills/`,
outside this repository. Anyone who installs superfunk elsewhere therefore
takes the skip branch on every spec.

A count across `docs/superpowers/specs/` confirms the effect: zero of 43
shipped specs contain an `## Alternatives Considered` heading. The branch has
never fired once in the project's history, including on this machine.

The instruction that survives — step 4 of the brainstorming checklist,
"Propose 2-3 approaches — with trade-offs and your recommendation"
(`SKILL.md:27`, restated at `:91-94`) — names no mechanism. It states an
outcome and relies on the agent to reach it. `docs/principles.md` calls this
shape out directly under Mechanisms, Not Goodwill. Step 4 therefore carries
the thinnest discipline of any step in a heavily-gated pipeline.

### Origin of the two added mechanisms

A review of the nine skills in `github.com/AminBlg/LeCunSkills` compared each
against all 19 plugin skills, the 5 user-level skills, `docs/principles.md`,
and `docs/ai-code-guidelines.md`. Six of the nine duplicate existing coverage
or state it more weakly. A seventh, `lecun-first-principles`, contributed the
deferred item at the end of this document. Two mechanisms survived into this
design. A keyword probe across all 24 skill files, plus the two docs above,
returns zero matches for either:

1. **The null option.** No skill asks what happens if the project ships
   nothing for this decision. `multi-lens-research` dispatches four lenses,
   and each lens must propose an approach; none may return "defer." A
   pipeline that converts conversations into specs pulls structurally toward
   action, and nothing currently pushes back.
2. **Ranking sensitivity.** No skill asks which factor, if it moved, would
   reorder the candidates. `calibrating-recommendations` asks what would lower
   confidence in the chosen candidate. That question probes the pick. It does
   not probe how narrowly the pick won.

### Install state

`~/.claude/settings.json` enables `superpowers@claude-plugins-official`.
`~/.claude/plugins/config.json` lists no repositories. Superfunk installs
nowhere today and reaches sessions only through disposable trials. Moving the
three skills out of `~/.claude/skills/` would therefore remove them from every
project until superfunk installs. This spec copies them instead.

### This spec demonstrates the gap

The brainstorming session that produced this document proposed approaches
inline and never dispatched a research skill. Under the current `:139` rule,
this spec must skip its own `Alternatives Considered` section — the
forty-fourth consecutive spec to do so.

## Decision

### 1. Adopt three skills into the plugin

Copy three directories from `~/.claude/skills/` into `plugin/skills/`:

- `multi-lens-research`
- `branching-research`
- `calibrating-recommendations`

`plugin/.claude-plugin/plugin.json` and `marketplace.json` enumerate no
skills, so neither file needs a skill entry. Claude Code discovers
`skills/*/SKILL.md` automatically.

The plugin version moves from `6.2.0` to `6.3.0`. `plugin/.version-bump.json`
declares seven files that carry that version, and all seven change together:
`package.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`,
`.codex-plugin/plugin.json`, `.kimi-plugin/plugin.json`,
`.claude-plugin/marketplace.json`, and `gemini-extension.json`.
`plugin/scripts/bump-version.sh` exists to do this in one step, but it
requires `jq`, which this environment lacks, so the seven edits happen by
hand.

`adhd-research` stays at user level. It shells out to an external `adhd` CLI.
`branching-research` already exists as its portable equivalent, by its own
description. A plugin skill that depends on an uninstalled binary costs every
adopter a failed invocation.

After the copy, `plugin/skills/` holds the authoritative version of all three
files. The `~/.claude/skills/` copies keep working as mirrors. They get
deleted when superfunk installs globally.

### 2. Repair cross-references in the adopted copies

`branching-research/SKILL.md` names `adhd-research` on six lines. A plugin
reader cannot resolve that name. The six lines split into two groups and take
two different repairs.

**Positioning references (lines 10, 12, 17)** describe `branching-research` by
contrast with a skill the plugin omits. Reword each to describe what
`branching-research` does, with no comparison to `adhd-research`. Keep the
`vs. multi-lens-research` comparison on line 12 — that skill ships alongside.

**Provenance references (lines 39, 77, 90)** cite where a documented failure
mode came from, for example "confirmed failure mode from `adhd-research`
testing." `plugin/skills/process-review/SKILL.md` states the governing
principle: real evidence over vibes. Deleting these lines discards evidence.
Reword each to keep the provenance without the unresolvable name, for example
"confirmed in prior testing of this technique."

`multi-lens-research/SKILL.md:29` names `general-purpose`. That names an agent
type, not a skill, and needs no change. No other reference in the three files
fails to resolve against `plugin/skills/`.

### 3. Give brainstorming's step 4 a mechanism

Replace `plugin/skills/brainstorming/SKILL.md:27`:

```markdown
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
```

with:

```markdown
4. **Propose 2-3 approaches** — with trade-offs and your recommendation.
   Every proposal set meets three requirements:
   - Include a do-nothing/defer candidate. Name what happens if this
     design ships nothing.
   - State confidence, and name the project-specific evidence behind it.
   - Name the factor that, if it moved, would flip the ranking.
   For a decision with several defensible paths, dispatch
   `multi-lens-research` or `branching-research` instead of proposing
   inline.
```

Update the prose restatement at `:91-94` to carry the same three
requirements, so the checklist and the prose agree.

This adds no gate. The three requirements attach to a step the agent already
runs.

### 4. Make the Alternatives Considered branch reachable

Replace the `:139` bullet with wording that gives the inline path its own
short form:

```markdown
- Capture an `Alternatives Considered` section in every spec that records a
  choice between approaches. If `multi-lens-research` or `branching-research`
  ran for this decision, capture the full comparison — the candidates, the
  recommendation, the steelmanned alternative. If only step 4's inline
  proposal ran, capture the short form — the candidates including the
  do-nothing option, the recommendation with its confidence, and the flip
  factor. Skip the section only when the design records no choice between
  approaches; an empty section repeats the placeholder problem the
  self-review below already bans.
```

### 5. Add ranking sensitivity to calibrating-recommendations

Add one line to the Medium/High recommendation output block in
`plugin/skills/calibrating-recommendations/SKILL.md`, after
`**What would lower it:**`:

```markdown
**What would flip the ranking:** <the single factor that, if it moved, would
reorder the candidates — distinct from what would lower confidence in the
pick, which asks how the recommendation fails on its own terms>
```

Add a matching entry to that skill's Common Mistakes list. That list uses
bullets, not a table, so the entry takes bullet form and goes after the final
`Logging a severe pre-mortem finding without reconsidering` bullet:

```markdown
- **Restating the pre-mortem as the flip factor** — the pre-mortem asks how the pick fails on its own terms; the flip factor asks how narrowly the pick won. A recommendation that wins by a wide margin on every factor says so plainly; one that wins on a single close call names that call.
```

The skill's existing contract governs this field like the others: it stays
required even when a request asks to omit it.

### 6. Add the null-option baseline to multi-lens-research

The four lenses each must propose an approach, so no lens can carry the null
option. Add it to step 3, Synthesize, instead:

```markdown
Include a do-nothing/defer baseline in the comparison, even though no lens
proposes one — what happens if the project ships nothing here. A baseline
that beats all four lens proposals means the fan-out found no approach worth
taking, and the honest output says so rather than picking the least-bad
proposal.
```

`branching-research` selects frames per-problem and can reach the null option
through its Inversion or Remove-assumption frames, so it takes no equivalent
change.

## Falsifiable Criteria

1. `plugin/skills/multi-lens-research/SKILL.md`,
   `plugin/skills/branching-research/SKILL.md`, and
   `plugin/skills/calibrating-recommendations/SKILL.md` all exist.
2. A grep for `adhd-research` across `plugin/skills/` returns zero matches.
3. Every backtick-quoted skill name in the three adopted files resolves to a
   directory under `plugin/skills/`, checked by script rather than by reading.
4. `plugin/skills/brainstorming/SKILL.md:27` matches the step 4 wording in
   Decision section 3 exactly, and the prose at `:91-94` carries the same
   three requirements.
5. The `Alternatives Considered` bullet matches the wording in Decision
   section 4 exactly.
6. `calibrating-recommendations/SKILL.md` contains the
   `**What would flip the ranking:**` line and the new Common Mistakes row,
   worded as Decision section 5 states.
7. `multi-lens-research/SKILL.md` step 3 contains the null-option baseline
   paragraph, worded as Decision section 6 states.
8. All seven files `plugin/.version-bump.json` declares read `6.3.0`,
   checked by iterating that file's own list rather than by naming files
   from memory.
9. Two disposable `--plugin-dir` trials run the same brainstorming prompt: one
   against the current step 4, one against the revised step 4. The revised run
   produces a do-nothing candidate and a named flip factor. The current run
   produces neither. A run that produces both under the current wording
   falsifies the change, which then does not ship.

## Consequences

Every superfunk installation gains the option-comparison discipline that
previously depended on two files outside the repository. The
`Alternatives Considered` section becomes reachable for the first time, on
both the fan-out path and the inline path. Step 4 stops relying on goodwill
and names three checkable requirements, which the spec self-review can verify
against the written spec.

Two mechanisms enter the framework that no existing skill supplies: a
do-nothing candidate in every proposal set, and a named flip factor on every
recommendation. Both cost roughly one line of output each and apply to every
brainstorm rather than to the rare fan-out.

Specs get longer. A design that records a choice between approaches now
carries an `Alternatives Considered` section that 43 prior specs omitted.

Two copies of three skills exist until superfunk installs globally. The
assumption that must hold: that install eventually happens, and the
`~/.claude/skills/` mirrors get deleted as part of it. If the install never
happens, the two lineages drift, and the mirrors go stale first, because
`plugin/skills/` holds the version this spec and later specs amend.

`adhd-research` keeps working at user level and keeps its own references to
the three adopted skills. Those references resolve on this machine. They fail
for anyone who installs superfunk without also holding `adhd-research`, which
matches the current state and worsens nothing.

## Deferred

- **A convention-retirement pass for `process-review`.** `process-review`
  generates rules and never retires them. All five of its output sections —
  Catches, Misses, Friction, Gaps, Recommendations — add. A probe across all
  24 skill files and the two docs above finds no mechanism that retires a
  process rule, check, gate, or skill. The closest existing mechanism,
  `writing-plans/SKILL.md:270-278`, retires stale codebase text after a
  capability lands, which solves a different problem.
  The `2026-08-30-checkpoint-priority-and-conditional-gate` spec made
  an existing gate conditional by hand, which shows the pressure arriving
  without a process to absorb it. This gets its own spec after this one
  ships.
- **Bootstrapping `docs/architecture/concept-index.md`.** The `concept-index`
  skill ships and describes a file that does not exist. Adopting three skills
  makes a natural moment to create it. Out of scope here.
- **Effort estimation in plans.** No superfunk skill estimates time or effort
  for a task. This spec treats that absence as deliberate for AI-executed
  plans rather than as a gap, and changes nothing.
