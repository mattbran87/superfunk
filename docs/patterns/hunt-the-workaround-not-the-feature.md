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
