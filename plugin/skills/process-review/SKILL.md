---
name: process-review
description: Use when a design-spec Status trigger or brainstorming gate signals a process review is due -- synthesizes recent Catches/Misses/Friction/Gaps into a review file with actionable Recommendations
---

# Process Review

Read `docs/superpowers/process-reviews/notes.md`, each shipped spec's
plan outcomes file (if one exists), and recent git history across the
specs shipped since the last review. Synthesize findings into a dated
review file, and reset the tracker.

**Core principle:** real evidence over vibes — every Catch, Miss,
Friction, and Gap in the output traces to a logged note, an outcomes
entry, or a specific commit, not to memory of how the work felt.

## When to Use

Reads `docs/superpowers/process-reviews/tracker.md`,
`docs/superpowers/process-reviews/notes.md`, and each shipped spec's
plan outcomes file (if one exists). Invoked by two callers, never run
standalone without one of these triggers:

- `subagent-driven-development`'s Finish step, when the tracker's
  "Specs shipped since" list reaches 3 entries.
- `brainstorming`'s "Understanding the idea" step, when the tracker
  shows a review overdue.

## The Process

1. Read `docs/superpowers/process-reviews/tracker.md`. Note the last
   review's spec filename and date (or "none yet"), and the "Specs
   shipped since" list — these are the specs this review covers.
2. Read `docs/superpowers/process-reviews/notes.md`. Collect every
   entry dated after the tracker's last-review date (or every entry,
   if the tracker reads "none yet"). An entry carries either four
   fields (date, Catch, label, finding) or five (date, Catch, label,
   check, finding). Read a four-field entry as carrying no
   attribution: it predates the attribution field, and nothing
   reconstructs which check found it. Read the literal value
   `none — found ad hoc` in a five-field entry the same way — a real
   record that no check produced that Catch, not a missing value.
3. For each spec in the "Specs shipped since" list, derive its plan's
   basename by stripping the trailing `-design` from the spec's
   filename (minus `.md`) — the trailing occurrence specifically,
   since some filenames contain "design" more than once (e.g.
   `2026-08-13-design-spec-template-quality-design.md`). Read
   `docs/superpowers/plans/<plan-basename>-outcomes.md` if it exists
   at that exact path. If it doesn't, fall back to matching
   `docs/superpowers/plans/*-outcomes.md` against the spec's own
   `YYYY-MM-DD` date prefix, to cover a plan whose filename doesn't
   share the spec's exact stem: a single match still counts as found;
   zero matches means no outcomes file exists for this spec (most
   commonly a spec shipped before this mechanism existed), and that
   absence never counts as an error; more than one match is a genuine
   ambiguity — name the candidate filenames in the review's Gaps
   section and skip reading any of them, rather than guessing. Collect
   every entry reporting a real divergence or follow-up from a file
   you did read; skip an entry that reads "shipped as planned" with no
   divergence or follow-up, since it carries no signal.
4. Cross-reference `git log --oneline` for each shipped spec's
   implementing commits (the spec name usually appears in a commit
   trailer, e.g. "Part of docs/superpowers/specs/..."). For any fix
   commit whose message names a defect with no matching notes.md
   entry, treat it as a Catch the running log missed, and include it.
5. Synthesize the collected Catches and outcomes entries into the
   review's sections:
   - **Specs Reviewed** — list the "Specs shipped since" filenames
     from the tracker; these are the specs this review covers.
   - **Catches** — list each Catch entry, grouped by spec.
   - **Misses** — a Catch that recurs across 2 or more of the
     reviewed specs signals something upstream should catch it
     earlier. Name the pattern and which specs it recurred in. An
     outcomes-reported divergence that recurs across 2 or more of the
     reviewed specs joins this section too, the same recurrence
     threshold.
   - **Friction** — a task or spec whose commit history shows 3 or
     more fix rounds, or any note that reads as procedural friction
     rather than a code defect.
   - **Gaps** — a convention repeatedly caught by the same reviewer,
     with no earlier check backing it up. An outcomes-reported
     follow-up too vague to act on yet joins this section too, as a
     candidate needing more definition.
   - **Recommendations** — one checkbox item per Miss, Friction
     point, or Gap identified above, plus one per outcomes-reported
     follow-up that names a concrete file and change. Each names a
     target file and the exact change, e.g. `- [ ] Add X check to
     docs/ai-code-guidelines.md`. A Catch or a one-off outcomes entry
     alone, with no recurring pattern and no concrete follow-up, needs
     no Recommendation — the review loop already handled it.
6. Write the review to
   `docs/superpowers/process-reviews/review-after-<last-spec-slug>.md`,
   where `<last-spec-slug>` is the filename (minus `.md`) of the most
   recently shipped spec in the "Specs shipped since" list.
7. Update `docs/superpowers/process-reviews/tracker.md`: set "Last
   review" to `<spec-filename> — <YYYY-MM-DD>` (e.g.
   `2026-08-19-process-review-design.md — 2026-08-19`), using this
   review's spec filename and today's date, and clear "Specs shipped
   since" to `(none)`.
8. Commit the review file and the tracker update together.

## No Placeholders

Every Recommendation names a real target file and a real, specific
change — never "improve X" or "consider Y." If a Miss, Friction
point, or Gap has no clear fix, say so explicitly in that section
instead of forcing a vague Recommendation.
