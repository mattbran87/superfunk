# Lessons and Patterns — Design

**Date:** 2026-08-20
**Status:** Shipped

## Context

Casita runs Lessons and Patterns as the last two pieces of its continuous-improvement system, alongside Process Review, already ported into superfunk. A Lesson captures one retrospective fact, tied to the spec that surfaced it. A Pattern promotes a recurring Lesson into a prospective, reusable rule.

Real evidence backs both mechanisms. `docs/lessons-learned.md` holds 144 entries across six categories. Two Lessons already promoted to real Pattern files. Each shows confirmed downstream reuse: a lesson from spec 046 applied directly in spec 047, without waiting for a reviewer to repeat the catch.

Casita captures a Lesson at Acceptance Wrap-Up, the last step of a spec's lifecycle. It reads `docs/lessons-learned.md` at Planning Setup, the first step of the next spec. superfunk has two close equivalents. `subagent-driven-development`'s Finish step already runs at the end of a plan — it updates a shipped spec's Status and the process-review tracker. `brainstorming`'s "Understanding the idea" step already runs at the start of a new one — it checks `.context.md` and the process-review tracker. This spec wires Lessons and Patterns into those same two points.

Casita's tag system exists to make 144 entries selectively readable. A tag earns its place once 3+ lessons share a theme. superfunk starts at zero entries, so this spec skips tags. A full read costs nothing at this scale.

Casita's own retrospectives name one open gap, repeated across multiple process reviews. A Lesson gets read at Planning time, but nothing enforces it mid-Implementation. Casita's own fix pattern — elevate a recurring lesson into a CLAUDE.md rule — never got automated in Casita itself. This spec leaves that gap open here too. It names the gap explicitly in Deferred, rather than inventing an unproven mechanism Casita's own battle-tested version never reached.

## Decision

- **`docs/lessons-learned.md`** — a new file. H1 title, a one-line intro, then entries grouped under H2 category headings. No fixed category list: the first Lesson on a new topic creates its own heading, matching how Casita's six categories grew from zero.
- **Entry format**, ported from Casita: `### <title> (<spec-slug>)` as an H3 heading, a prose paragraph ending in a **Rule:** sentence, then a promotion note.
- **`docs/patterns/`** — a new directory, seeded with `pattern-template.md`: H1, `## Context`, `## Pattern`, `## Example`, `## Originating lessons`. Matches Casita's own template exactly.
- **Capture point — `subagent-driven-development`'s Finish step.** After the existing Status and tracker steps, add: capture a notable learning in `docs/lessons-learned.md`, or record that nothing notable arose. "Nothing notable" counts as a complete answer — Casita's own real entries include several.
- **Promotion question, ported unchanged.** At capture time, ask: "Does this Lesson express a prospective rule that applies across many future situations?" Tiebreaker: two instances of the same failure mode justify a promotion, even if the question alone reads ambiguous. Casita's one real promotion needed only the tiebreaker — the question itself never came into play.
- **On promotion:** write `docs/patterns/<slug>.md` from the template. Add `*Pattern promoted — see docs/patterns/<slug>.md*` after the Lesson entry.
- **On no promotion:** add `*No pattern promoted — <one-line reason>.*` after the Lesson entry.
- **Consumption point — `brainstorming`'s "Understanding the idea" step.** Before clarifying questions begin, read `docs/lessons-learned.md` in full, and run `Glob docs/patterns/*.md`, reading any pattern file relevant to the idea's domain.
- **`docs/code-standards.md`** gains a "Lessons vs. Patterns" section. A Lesson answers what happened and what to watch for. A Pattern answers what future work should do. Secondary test: one specific fact tied to one context makes a Lesson. A rule that applies across many future situations makes a Pattern.
- **No relation to `workflows/anti-patterns.md`.** That file stays a narrow, workflow-brainstorm-only checklist. This mechanism stays general-purpose, sourced from any plan's Finish step. The two coexist without cross-reference.

## Falsifiable Criteria

Same disposable `--plugin-dir` baseline-trial approach used for every wiring change this session:

1. Build a scratch fixture with an empty `docs/lessons-learned.md` and no `docs/patterns/` directory. Run `subagent-driven-development`'s Finish step for a plan with a real, notable finding. Confirm it writes a correctly formatted Lesson entry. Confirm it asks the promotion question. Confirm it applies the tiebreaker correctly, given a second scratch entry that describes the same failure mode.
2. Using the same fixture, run `brainstorming`'s "Understanding the idea" step for a new idea. Confirm it reads `docs/lessons-learned.md` in full before any clarifying question. Confirm it globs `docs/patterns/` before any clarifying question too.

## Consequences

Every Finish now asks one more question. "Nothing notable" answers this cheaply, most of the time, matching Casita's real ratio.

`docs/lessons-learned.md` grows without bound. No pruning mechanism exists, matching Casita's own 144-entry file today.

Patterns stay rare by design. Casita promoted two Patterns from 144 Lessons — a low ratio, not a sign the mechanism underperforms.

The enforcement gap Casita's own retrospectives never closed stays open here too. A Lesson gets read at the start of a new plan, but nothing enforces it mid-Implementation. This spec accepts that gap rather than inventing an unproven fix.

## Deferred

- Tags — revisit once `docs/lessons-learned.md` grows large enough that a full read costs real time, matching Casita's own 3+-lessons-per-theme threshold.
- The Implementation-time enforcement gap — Casita's own retrospectives name this repeatedly and never close it. Revisit only if it causes a real, observed problem in superfunk, the same standard this project applies to every other deferred gap.
- Any migration of `workflows/anti-patterns.md` into this system — considered and declined. The two serve different scopes.
