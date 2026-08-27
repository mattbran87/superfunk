# Refresh a worked example every time the process it illustrates gains a step

When a plan adds a step to a multi-step process, check whether any worked example elsewhere in the same file demonstrates that process — and if it does, update the example too.

## Context

A skill file often includes an Example Workflow: a condensed, illustrative walkthrough showing what the real process looks like end to end. When a later plan adds a new step to that process (a new Finish-time check, a new bookkeeping requirement), nothing about that plan's own File Structure or task list points back at the illustrative example — the task only touches the section describing the new step itself. The example silently falls behind, one addition at a time, until it demonstrates a process significantly shorter than the real one.

## Pattern

When writing a plan task that adds a step to a documented multi-step process, add an explicit check: does any worked example in the same file (or a cross-referenced one) walk through this process? If so, does the task's own File Structure entry include updating that example, or does the plan need one more task to do so? Don't rely on File Structure's silence about the example section to mean nothing needs checking — silence there usually means no one looked, not that nothing changed.

## Example

- `subagent-driven-development/SKILL.md`'s Example Workflow section demonstrates the full plan-to-push flow. `per-task-outcome-capture` once found this example stale after adding an outcomes-file step and fixed it. Five more Finish-step additions since then — the spec-Status flip and tracker update, the Recommendation-checkbox step, the notes.md gate, and `bug-tracking`'s own ledger-scan step — each shipped without revisiting the example, since none of those plans' tasks touched the Example Workflow section directly. The example now demonstrates a Finish sequence six steps shorter than the real one.

## Originating lessons

- "A worked example illustrating a process goes stale every time that process gains a new step, and nothing re-checks it" (2026-08-27-bug-tracking)
