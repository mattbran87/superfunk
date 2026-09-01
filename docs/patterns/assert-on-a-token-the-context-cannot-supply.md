# Assert on a Token the Context Cannot Supply

A containment assertion (`"X" in output`) that stays green after deleting
the thing it guards, because the surrounding content already supplies `X`
some other way.

## Context

A guard checks that a document, output, or diff contains some specific
word or flag, chosen to avoid pinning exact wording. This applies whenever
a plan or reviewer writes a "contains" assertion instead of an equality
assertion.

## Pattern

For every assertion that content contains a chosen token, check whether
that token — or a superstring/synonym of it — already appears elsewhere in
the same content before the guarded change ships. If it does, the
assertion cannot discriminate the guarded change from its absence; either
pick a token that appears nowhere else, or assert on the specific location
(a line number, a section) instead of a bare substring search.

## Example

A README guard asserted `"JSON" in section`, chosen as a "distinctive
noun" to avoid pinning wording. The same section already contained
`"JSON-serializable"` one line above the bullet the guard existed to
protect — deleting that bullet left the assertion green, because the
neighboring word alone satisfied it.

## Originating lessons

- "Non-discriminating containment guards" (taskq-trial-batch1-mechanical-fixes)
