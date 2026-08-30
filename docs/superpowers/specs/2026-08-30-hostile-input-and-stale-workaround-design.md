# Hostile-Input Pass and Stale-Workaround Grep — Design

**Date:** 2026-08-30
**Status:** Shipped
**User-Facing:** No

## Context

The external bookmark-cli trial's own internal process-review (`review-after-2026-08-29-edit-command-design.md`) names two Misses, each with an already-drafted Recommendation targeting `writing-plans/SKILL.md`'s Self-Review section.

**M1 — the plan, not the implementer, authored the defect, five times across two specs.** Catches 1–4 (bookmark-cli) and 11 (retry-sweep) all record the same shape: the plan's own code block never considered a specific input class, and an implementer transcribed the gap faithfully. Metacharacters in query text (`search()`'s unescaped `LIKE` pattern), a value that already exists (`cmd_add` fetching and discarding a title on a re-add), a discarded return value (`cmd_open` ignoring `webbrowser.open`'s result), and an already-running future that resists cancellation (`shutdown(cancel_futures=True)` against futures already in flight) — all five surfaced only after an implementer built the wrong thing and a reviewer read the diff, one stage later than a plan-time check could have caught them.

**D10/M3 — shipping a feature leaves behind the text describing its absence, twice across two specs.** After `bm retry` shipped, the README still listed "No retry for failed fetches" as a limitation. After `bm edit` shipped, `bm add --title` on an already-saved URL still printed "remove and re-add to change it" — actively directing users at the destructive operation `edit` existed to replace. Both got caught only at the final whole-branch review, the most expensive point in the pipeline. The trial's own process-review promoted this to `docs/patterns/hunt-the-workaround-not-the-feature.md` (not yet present in this repo — its actual content, read directly from the trial fixture, informs the Decision below): the fix isn't searching for the new feature's name, since limitation-era text never mentions a feature that didn't exist yet — it's searching for the *workaround's own distinctive words*, the phrase a user would have hit when the limitation still applied.

Both Recommendations target the same file and section, so this spec ships both together.

## Decision

**`writing-plans/SKILL.md`'s Self-Review gains item 13**, appended after the existing item 12:

```markdown
**13. Hostile-input pass:** For each code block a task specifies, name
the input class it does not handle — metacharacters in user-supplied
text, a value that already exists, a discarded return value, an
operation that cannot be cancelled, or any other input the block's
own logic doesn't account for. Either handle it in the plan, or
record it as an accepted limitation in the spec's Consequences
section. A code block with an unexamined input class counts as a plan
failure, the same as a missing test.
```

**`writing-plans/SKILL.md`'s Self-Review gains item 14**, appended after item 13:

```markdown
**14. Stale-workaround grep:** If any task removes a limitation (a
missing command, an unsupported case, a manual step), write down the
exact phrase the tool used to describe that limitation — the error
message, docstring, or README text a user would have hit. Grep the
codebase for that phrase's distinctive words — not the new feature's
name, which limitation-era text never mentions — per
docs/patterns/hunt-the-workaround-not-the-feature.md. List every hit
as a task requirement: each one either needs updating to reflect the
new capability, or needs removing if it no longer applies.
```

**`docs/patterns/hunt-the-workaround-not-the-feature.md` gets created in this repo**, adapted from the trial fixture's own version (Context, Pattern, and the two worked examples below, generalized from `bm`-specific detail to the general shape):

```markdown
# Hunt The Workaround, Not The Feature

When a change removes a limitation, the stale text sits wherever the
limitation forced a workaround — and none of it names the new feature.

## Context

A release removes a constraint: a missing command arrives, an
unsupported case becomes supported, a manual step gets automated. The
new surface gets documented carefully, because it's what the work was
about.

What doesn't get found is everything written around the absence. A
limitation propagates outward from the code that lacks it: error
messages that route users to a workaround, rationale comments
explaining why something was deferred, "Current limitations" lists,
test comments justifying an awkward workaround, prose describing the
old behavior sitting near prose describing the new. Searching for the
feature's name finds none of these — they predate it and talk about
its absence.

## Pattern

Before shipping, grep for the workaround the limitation forced — the
phrase users were told to do instead — not for the feature's name.
Write down the sentence the tool used to say when someone hit the
limitation. Search for its distinctive words. Every hit either turns
false the moment the feature ships, or needs to point at the new
path instead.

Check the same terms in: error strings, comments near the code that
enforced the limitation, the README's limitation list, and any test
whose comment explains a workaround.

A useful sharpening: the more helpful the old message was, the more
dangerous it becomes. A message that merely said "not supported" goes
inert once support arrives. A message that said "do X instead"
actively directs users at X — and if X causes harm, it keeps causing
harm after the safe path exists.

## Example

A bookmark-manager CLI shipped an `edit` command so a bookmark's title
could get fixed without losing its permanent id and tags. The final
review found `add --title` on an already-saved URL still printing
"already saved — --title ignored; remove and re-add to change it."
Correct when written; after `edit` shipped, it directed users at the
one operation that destroys the id and every tag — precisely the
damage the round existed to prevent. Grepping for `edit` would have
found none of the four stale references (two code comments, a test
comment, a README paragraph). Grepping for `re-add` — the workaround —
found all four.

The same failure happened one round earlier: after a retry command
shipped, a docstring still read "wired to no command yet" and the
README still listed the retry gap as a limitation — that instance
blocked a merge.

## Originating lessons

- "Removing a limitation means hunting the workaround it forced" (2026-08-30-hostile-input-and-stale-workaround)
```

## Falsifiable Criteria

1. A direct read-through of `writing-plans/SKILL.md`'s Self-Review confirms items 13 and 14 exist, worded identically to the Decision block above.
2. A direct read-through of `docs/patterns/hunt-the-workaround-not-the-feature.md` confirms it exists with the content above.
3. A disposable `--plugin-dir` trial constructs a fixture plan whose task code block leaves an unhandled input class (e.g., a search function with no metacharacter escaping). Applying item 13 during the plan's own Self-Review correctly names the unhandled input class and either adds handling or records it as an accepted Consequence.
4. A second disposable trial constructs a fixture where a task removes a limitation and a stale reference to the old workaround phrase still exists elsewhere in the fixture (an error message, a comment, a README line). Applying item 14 correctly greps for the workaround's distinctive words (not the new feature's name) and lists the stale hit as a task requirement.

## Consequences

A future plan whose code block doesn't account for a hostile or edge-case input gets caught during the plan's own Self-Review, before an implementer builds it and a reviewer reads the diff — closing the gap that let five defects across two specs ship one stage later than necessary. A future plan that removes a limitation gets checked for every place the limitation's own workaround text still lingers, closing the gap that twice let shipped features stay actively misdirected by stale guidance, once badly enough to block a merge.

## Deferred

- The remaining trial finding (D5/D7, checkpoint UX) — tracked separately for a follow-up sub-project.
- The mutation check's own equality-not-containment addendum (R5 in the trial's process-review, not yet shipped alongside the mutation check itself) — a small, independent loose end from the same source list, out of this spec's scope.
