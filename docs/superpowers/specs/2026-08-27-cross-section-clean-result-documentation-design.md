# Cross-Section Clean-Result Documentation — Design

**Date:** 2026-08-27
**Status:** Approved

## Context

The process review `docs/superpowers/process-reviews/review-after-2026-08-27-cross-section-sibling-scope-design.md` named its fourth Recommendation: when a plan's own dog-fooding of item 8 finds a sibling file needing no change, the design spec should document why — this reasoning has twice landed only reactively, after a final review asked for it. `cross-section-sibling-scope`'s own Deferred section shows the clearest instance: the spec never recorded why `subagent-driven-development/SKILL.md`'s two abstract carve-out summaries and `re-review-prompt.md`'s own Scope pointer needed no edit that time, unlike the predecessor sub-project where the equivalent abstraction did need one.

This gap traces specifically to item 8 (`writing-plans/SKILL.md`) — a plan-writer's own dog-fooding, checking siblings while drafting tasks. The re-review carve-out has no equivalent moment: a fix round never has an active design spec to write reasoning into, so this spec stays scoped to item 8 only, not extended to the carve-out for forced parity.

## Decision

Item 8 gains one more sentence, continuing the same check rather than adding a new item:

```
**8. Cross-section mechanism consistency:** Does any task edit content
describing a routing, trigger, or lifecycle mechanism — language like
"if X exists, proceed to...", "triggered by...", "never run
standalone," or a cross-reference like "see Y, below"? If so, grep
the same target file, every other file in the same
`plugin/skills/<name>/` directory (top-level files only, not
subdirectories) if the target file lives in one, and the design spec,
if it also describes this mechanism — for every other mention of the
key terms involved, and read each hit. Confirm the edit doesn't leave
any of them contradicting the new content. If none of them
contradict, and this plan traces to a design spec, add one sentence
to that spec's Deferred or Consequences section explaining why the
checked file(s) needed no change.
```

The new sentence fires only when item 8 both triggers (rare — most plans carry no routing/trigger/lifecycle language) and finds a clean result (rarer still — most triggers in this project's history found a real contradiction needing a fix). This keeps the added cost low without leaving the clean case silent the way it stayed twice before.

## Falsifiable Criteria

1. A direct read-through of the shipped `writing-plans/SKILL.md` confirms item 8's new sentence exists, worded identically to the Decision block above.
2. A disposable `--plugin-dir` trial builds a fixture with a target file and an untouched sibling that, together, trigger item 8 but produce no contradiction (the sibling genuinely doesn't need a change). Running Self-Review against a fixture plan naming a fixture design spec confirms the agent adds a one-sentence explanation to that spec's Deferred or Consequences section, unprompted.

## Consequences

Every plan whose item 8 triggers and finds a clean result gains one required sentence in its design spec — a narrow, low-frequency cost, since both conditions (trigger, then clean) rarely coincide.

Plans where item 8 never triggers, or where it triggers and finds a real contradiction (already required to get fixed), see no change.

## Deferred

- Extending an equivalent requirement to the re-review carve-out — no design spec actively drafts during a fix round, so "document in the spec's Deferred section" doesn't have an analogous moment there. Revisit only if a future recurrence shows a fix-round-time clean result going undocumented in a way that matters.
