# Watchlist and Findings Batch — Design

**Date:** 2026-10-15
**Status:** Approved
**User-Facing:** Yes

## Context

This spec supersedes `2026-09-08-watchlist-release-notes-batch-design.md`.
That spec reached Approved status and then stopped: no plan, no
`watchlist.md`, and no code change exist for it. This spec carries its
four parts (A–D) and adds three items from the ArcGISProMCP findings
file, `docs/superpowers/process-reviews/external-project-arcgispromcp-findings.md`.

The three new items each change a file that A–D also change, so one
plan edits each shared file once:

| Part | Source | Shared file |
|---|---|---|
| E | Findings A6 (lines 619–672, update at 694–725) | `check_docs.py`, also edited by D |
| F | Findings A5, 2026-09-24 addendum (lines 557–617) | `process-review/SKILL.md`, also edited by A |
| G | Findings A11 (lines 815–847), plus line 91 of `review-after-2026-09-01-convention-retirement-design.md` | `notes.md` header and `process-review` step 2, also edited by A |

The findings file labels two different items "A5". This spec calls
the 2026-09-24 one **A5b**.

### The 09-08 spec's four problems, carried unchanged

- **A. Watch items have no durable home.** Three `Watch` entries sit in
  `notes.md` (lines 126–128). A `notes.md` entry gets the attention of one
  review window only.
- **B. `plugin/RELEASE-NOTES.md` holds no entry after v6.2.0.** The fork
  shipped 6.3.0 through 6.6.0 without one. Human-partner decision
  (`notes.md`, 2026-09-02): MAINTAIN.
- **C. No step makes a version bump write an entry.**
- **D. `check_docs.py` misses nested doc paths and crashes on Windows
  consoles** (BUG-0001, BUG-0002).

### E. `check_docs.py` returns empty section bodies without a warning

`extract_section` (`check_docs.py:16`) builds the pattern
`r'^## ' + re.escape(heading) + r'\n...'`. That pattern matches only an
exact `## Context`, `## Decision`, or `## Consequences` line. On a miss it
returns `""`, and `main()` prints the empty body under the heading. The
verdict line stays correct, because `git diff --name-only` decides it.
Only the section bodies fail.

Measured on 2026-10-15 by a run of `extract_section` against every
`User-Facing: Yes` spec:

| Repo | User-facing specs | Specs with an empty section | Heading form that fails |
|---|---|---|---|
| superfunk | 7 | 2 (Decision) | `## Decisions` |
| ArcGISProMCP | 16 | 15 (all three sections) | `## 1. Context`, `## 2. Decision`, `## N. Consequences` |

The findings file records 6 sightings of this failure across
ArcGISProMCP review windows. Its proposed regex adds the ordinal and
misses the plural, so it fixes neither superfunk failure.

### F. `process-review` step 3 misses a spec's second plan

Step 3 finds a spec's outcomes file by two rules: the stem with `-design`
stripped, then the spec's date prefix. ArcGISProMCP shipped
`2026-09-19-edit-module-design.md` through two plans:
`2026-09-19-edit-module-surface.md` and `2026-09-20-edit-module-handlers.md`.
The date rule reaches the first plan's outcomes file. Neither rule reaches
the second one. The findings file counts 32 `notes.md` entries from the
second plan that a literal run of step 3 drops.

On 2026-10-15 this spec's author measured three anchors across superfunk (52 specs,
42 plans) and ArcGISProMCP:

- **A full-text grep of plans for the spec filename** returns more than one
  plan for 9 superfunk specs. Most hits cite a spec as background.
- **A grep of each plan's header region** (lines above the first `---`)
  still returns extra plans for 2 superfunk specs: `concept-index` and
  `hazard-signal-words`.
- **Commit trailers** (`Part of docs/superpowers/specs/...`) reach the
  R1–R4 batch's outcomes file. `git log --grep` finds no trailer for
  ArcGISProMCP's `edit-module` spec.

The `writing-plans` header template carries no spec field, so no
superfunk plan has one. ArcGISProMCP's handlers plan already writes
`**Spec:**` at line 11, by its own convention.

### G. `notes.md` documents one entry type, and the files use five

The `notes.md` header documents `Catch` only. `process-review` step 2
reads only `Catch`. The files in use hold more types, counted on
2026-10-15 by field 2:

| File | Catch | Miss | Gap | Friction | Watch |
|---|---|---|---|---|---|
| superfunk `notes.md` | 106 | 0 | 0 | 0 | 3 |
| ArcGISProMCP `notes.md` | 437 | 43 | 1 | 1 | 0 |

A step-2 read sees none of the non-`Catch` entries. ArcGISProMCP's one
`Gap` entry, dated 2026-10-06, named the citation-rot class on the first
day of its window. The same class then produced 12 blockers at the
`arcade` whole-branch gate 8 days later (findings lines 823–834).

The convention-retirement review's line-91 Recommendation adds a second
header rule: escape a literal `|` inside a field. One superfunk entry
(`notes.md:88`) holds literal pipes in its finding field today.

## Decisions

1. **One spec, seven parts, superseding the 09-08 spec.** One plan edits
   each shared file once. The 09-08 file keeps its text and gets the
   Status line `Superseded by 2026-10-15-watchlist-and-findings-batch-design.md`.
2. **No trials.** Every part changes a format, a script, a template field,
   or bookkeeping, and each part has a runnable acceptance check. No part
   claims a behavior change that only a trial can establish. This carries
   the 09-08 spec's Decision 2.
3. **Part E keeps the verdict and marks each failed section.** The first
   line and the exit codes stay unchanged. Four callers branch on the
   verdict name: `documentation` Step 2, SDD Final Review, `executing-plans`
   Step 2.5, and `writing-plans` User-Facing Documentation Timing. A new
   verdict needs a new branch in all four. A caller that misses the
   branch falls through with no instruction, which repeats the silent
   failure that part E exists to fix.
4. **Part F adds a `**Spec:**` field to the plan header.** Of the three
   anchors measured, only this one has zero over-matches and zero misses
   on new plans. It works from now on only. Old plans keep the two
   existing rules.
5. **Part G admits five entry types, and each type routes to one review
   section.**
6. **A `Gap` entry names its disposition** (the mechanism it wants), or
   writes the literal `(no mechanism proposed)`.
7. **A logged `Miss` gets its own Recommendation, without a recurrence
   threshold.** The threshold exists to infer a missing check from
   repeated Catches. A logged `Miss` records the failed check directly.
8. **Recommendation dispositions recorded at the gate.** The
   convention-retirement review's 5 open items got these dispositions
   on 2026-10-14: lines 89, 90, and 93 closed by other routes; line 91
   folded into part G; line 92 carried by part D.

## Design

Parts A–D keep the 09-08 spec's content. Their prose follows this
spec's style rules, and code, paths, and quoted text stay byte-identical.

### A. Watchlist mechanism

Carried from the 09-08 spec, with one change: part G replaces skill-hook
edit 1.

**New file:** `docs/superpowers/process-reviews/watchlist.md`.

Entry format:

```markdown
- **<kebab-slug>** (added YYYY-MM-DD, <origin spec or discussion>)
  - Watching: <the thing under watch>
  - Trigger: <observable condition>
  - Action when tripped: <pre-decided action>
```

**Six seed entries.** The three 2026-09-02 Watch items (item-10
accretion; executing-plans→SDD Finish pointers; plugin/-wide bump
trigger), plus homes for all three carried review gaps: G1 (title-based
overlap claims — trigger: a spec or review asserts two checks overlap
from their titles or first sentences alone), G3 (attribution coverage —
trigger: a review window where unattributed catches again dominate,
blocking Zero-yield), and G2 (plan-less shipping path — trigger: a spec
ships via spec → trial → ship with no plan again; action: hold its
Finish until the G2 ownership design conversation happens). The gap
list enumerates completely: G1, G2, G3 — no member skipped silently.
The plan drafts each seed entry's full text from the `notes.md` originals and the
review file's Gaps section.

**Skill hook:** one edit to `plugin/skills/process-review/SKILL.md`.
Insert a new step between steps 4 and 5 (later steps renumber):

> Append the window's Watch entries to
> `docs/superpowers/process-reviews/watchlist.md` in the entry format
> above. Derive each new entry's slug and its Watching field from the
> entry's label. Skip a `Watch` entry the watchlist already holds — the
> same origin label and trigger. Then, for every watchlist entry,
> evaluate its trigger against this window's evidence. A tripped entry
> becomes a Recommendation that
> names the entry's pre-decided action. A resolved or obsolete entry
> leaves the file, with a one-line removal note in the review. Every
> other entry stays. The review names how many entries it checked, so an
> unread watchlist shows up as a zero.

The 09-08 spec's edit 1 (step 2 reads `Watch`) moves into part G, which
rewrites step 2 for all five types.

### B. RELEASE-NOTES backfill

Carried from the 09-08 spec. Insert directly under the
`# Superpowers Release Notes` H1:

1. A short **Fork** note: superfunk diverged from obra/superpowers after
   v6.2.0. Entries above the v6.2.0 heading describe superfunk. Upstream
   released a different v6.3.0, so the two histories share version
   numbers by coincidence only.
2. Four new entries in the file's existing `## vX.Y.Z (YYYY-MM-DD)`
   format, newest first. Each version's content comes from the commits
   between its bump and the bump before it:
   - v6.6.0 (2026-09-03): Step 2.5 whole-branch review for
     `executing-plans`.
   - v6.5.0 (2026-09-02): R1–R4 batch — the trial-gated drafted-insertion
     check, the outcome-space rule, the bump script without `jq`, and the
     Finish bookkeeping and bump gate.
   - v6.4.0 (2026-09-01): `process-review` Retirements and the attribution
     field; the taskq batch-1 fixes; three trial-gated mechanisms — the
     rule-membership check, the Rule-sentence enumeration, and the
     behavioral-claim widening.
   - v6.3.0 (2026-09-01): the fork's first release — every change from
     the fork point through the research-skill adoption, including the
     rebrand to superfunk. The rebrand commit `5196ecf` left the version
     at 6.2.0, so v6.3.0 first carries it.

   Each entry gets 2 to 4 bullets. The plan drafts the full text.

   The 09-08 spec assigned the rebrand alone to v6.3.0 and left
   convention-retirement and taskq batch 1 out of v6.4.0. `git log`
   between the bump commits shows both ranges as listed above.

Everything from the `## v6.2.0` heading down stays byte-identical.

### C. Release-notes duty in the bump gate

Carried from the 09-08 spec. Append to both gate copies, worded
identically and edited together
(`plugin/skills/subagent-driven-development/SKILL.md` and
`plugin/skills/executing-plans/SKILL.md`):

> Before that commit, add this version's entry at the top of
> `plugin/RELEASE-NOTES.md`, under the Fork note — or, if a
> `## vX.Y.Z (unreleased)` heading already exists, replace
> `unreleased` with the date — so the file holds a
> `## vX.Y.Z (date)` heading with at least one bullet. Include it in
> the same commit as the bump.

The existing normalized-extraction identity check extends to cover the
longer block. The gate paragraph now carries two duties: the bump and the
entry.

### D. `check_docs.py` path and encoding fixes

Carried from the 09-08 spec. Two edits to
`plugin/skills/documentation/scripts/check_docs.py`:

1. At the top of `main()`:
   `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`. This
   closes BUG-0002.
2. Line 47's set extends to
   `("README.md", "CHANGELOG.md", "plugin/README.md", "plugin/RELEASE-NOTES.md")`.
   This closes BUG-0001 and the rebrand spec's deferred recognition item.

Close both `docs/bugs/` files per the bug tracker's own format. Annotate
the rebrand spec's Deferred bullet as resolved by this spec.

### E. `check_docs.py` section parse

Three edits:

1. **Widen the heading match.** `extract_section` accepts an optional
   ordinal and an optional plural `s`:

   ```python
   pattern = r'^##\s+(?:\d+\.\s+)?' + re.escape(heading) + r's?[ \t]*\n(.*?)(?=^## |\Z)'
   ```

2. **Mark a failed section.** When `extract_section` returns an empty
   string, `main()` prints this line in place of the body:

   ```
   SECTION_NOT_FOUND: read "<heading>" from the spec directly
   ```

   The verdict line `ACTION_NEEDED` and exit code 1 stay unchanged.
3. **Teach the one consumer.** `plugin/skills/documentation/SKILL.md`
   Step 2, item 3 gains one sentence: for a section printed as
   `SECTION_NOT_FOUND`, read that section from the spec file directly.
   The other three callers act on the verdict line only, so they need no
   change.

`test_check_docs.py` gains four tests: a numbered heading, a plural
heading, a longer heading that must not match, and an absent section
that prints the marker. Part D adds two more: a nested
`plugin/RELEASE-NOTES.md` path and an em dash on a `cp1252` console.

### F. `**Spec:**` header field

Five edits:

1. **`writing-plans` header template.** Add one line after `**Tech Stack:**`:

   ```markdown
   **Spec:** [Path to the design spec this plan implements, or "none"]
   ```

2. **`writing-plans` Self-Review item 11.** The element list
   "(Goal, Architecture, Tech Stack, Global Constraints)" gains `Spec`.
3. **`process-review` step 3, third rule.** After the date rule, add:

   > Then read the outcomes file of every plan whose `**Spec:**` header
   > field names this spec, whatever the two rules above found. This rule
   > overrides the ambiguity skip: read a date-rule candidate whose plan's
   > `**Spec:**` field names this spec, and drop it from the Gaps note. A
   > spec that shipped through more than one plan has more than one
   > outcomes file, and its later plans carry dates no spec shares.

4. **`process-review` step 6, Specs Reviewed.** Each listed spec names
   every outcomes file the review read for it, or `none`.
5. **The four spec-trace definitions.** Each one decides whether a plan
   "traces to a design spec" from the plan's "Goal line or a task's commit
   trailer". Each one gains the `**Spec:**` field as the first source:
   - `plugin/skills/subagent-driven-development/SKILL.md`, Final Review
     (line 509)
   - `plugin/skills/subagent-driven-development/SKILL.md`, Finish (line 561)
   - `plugin/skills/executing-plans/SKILL.md`, Step 2.5 item 1 (line 40)
   - `plugin/skills/subagent-driven-development/re-review-prompt.md`,
     the cross-section check (line 95). The plan's first enumeration
     missed this copy, because it words the definition differently;
     the Task 4 review found it.

   The two SDD copies use identical wording today. The `executing-plans`
   copy omits the `e.g.` example. The edit keeps that difference and
   changes only the source list.

### G. Entry-type vocabulary

Two edits:

1. **The `notes.md` header.** Replace the single `Format:` line with a
   format line and a type table:

   ```markdown
   Format: `- <YYYY-MM-DD> | <type> | <task/spec label> | <field 4> | <field 5>`

   | Type | Records | Field 4 | Field 5 |
   |---|---|---|---|
   | `Catch` | A defect found before it shipped | The check that caught it | The finding |
   | `Miss` | A defect that got past a check that should have caught it | The check that missed it | The finding |
   | `Gap` | A class of defect that no check covers | The mechanism it wants, or `(no mechanism proposed)` | The finding |
   | `Friction` | Process cost with no defect behind it | The step that cost too much | The finding |
   | `Watch` | A condition to watch, with a pre-decided action | `trigger: <condition>` | `action: <pre-decided action>` |

   A literal `|` inside a field gets written as `\|`. A reader splits an
   entry on unescaped `|` only.
   ```

   The existing paragraphs about field 4 and about four-field entries
   stay. Entries already in the file stay as written, including
   `notes.md:88`. The `Watch` row matches the shape of lines 126–128.
2. **`process-review` step 2.** Rewrite it to collect every type and
   route each one:
   - `Catch` → the Catch synthesis, as today.
   - `Miss` → the Misses section directly, without the recurrence
     threshold. Its Recommendation targets the check its field 4 names.
   - `Gap` → the Gaps section, with its disposition. An empty field 4
     reads as `(no mechanism proposed)`.
   - `Friction` → the Friction section.
   - `Watch` → the watchlist step from part A.

   The step keeps its rules for four-field entries and for
   `none — found ad hoc`. It also reads entries on unescaped `|` only.

Step 6's Misses, Gaps, and Friction bullets each gain one clause that
admits their logged type. The `Catch`-only write sites stay unchanged:
SDD line 365, SDD line 536, and `executing-plans` line 60 log review
findings, and every review finding gets the `Catch` type.

## Falsifiable Criteria

1. `watchlist.md` holds six seed entries. Each entry carries Watching,
   Trigger, and Action fields.
2. `process-review/SKILL.md` holds the harvest-and-evaluate step. Its
   steps number consecutively, and no cross-reference names a step that
   no longer exists.
3. `plugin/RELEASE-NOTES.md` holds the Fork note and four new version
   headings above `## v6.2.0`. `git diff` shows additions above that
   heading only.
4. Both bump-gate copies hold the new sentence. The normalized-extraction
   diff over the extended block prints `IDENTICAL`.
5. On this machine, `check_docs.py`:
   - returns `NOT_APPLICABLE` (exit 0) on a `User-Facing: No` spec;
   - prints its full `ACTION_NEEDED` report without a traceback on a
     `User-Facing: Yes` spec that holds em dashes;
   - returns `ALREADY_UPDATED` (exit 0) when the diff range includes
     `plugin/RELEASE-NOTES.md`.

   BUG-0001 and BUG-0002 show a closed status.
6. A run of `extract_section` against every `User-Facing: Yes` spec
   returns zero empty sections in superfunk (from 2) and zero in
   ArcGISProMCP (from 15). `test_check_docs.py` passes with 16 tests.
7. An `ACTION_NEEDED` run against a spec without a `## Consequences`
   heading prints `SECTION_NOT_FOUND: read "Consequences" from the spec
   directly` and exits 1.
8. A scratch fixture holds one spec and two plans dated on different days.
   Both plans name the spec in their `**Spec:**` field. A literal run of
   the new step 3 reaches both outcomes files.
9. This batch's own plan carries a `**Spec:**` line that names this spec.
   All four spec-trace definitions name the `**Spec:**` field.
10. The `notes.md` header holds the five-type table and the pipe rule.
    `process-review` step 2 names all five types and routes each one to
    the section the table in part G lists.
11. This batch's own Finish runs the full bookkeeping list. Its bump
    commit holds this batch's own RELEASE-NOTES entry.

## Out of Scope

- Resolving G1, G2, or G3 themselves. This batch gives them watchlist
  homes with triggers.
- Retiring the `notes.md` Watch intake, or teaching other skills to write
  watchlist entries directly.
- An upstream sync, or a renumbering to escape the version collision.
- The SDD Finish step that reads `Gap` entries mid-window (the second
  half of findings A11). It changes SDD behavior, so it waits for a later
  batch with a trial.
- Findings A1–A4, A7–A10, and the optional A5. A8 and A9 belong in
  ArcGISProMCP's own `CLAUDE.md`.
- Adding a `**Spec:**` field to the 42 existing plans.

## Consequences

- `process-review` gains one step, the watchlist step. Without it,
  `Watch` entries hold attention for one window, and the gap list
  survives only by hand-copying.
- The watchlist does its job only while `process-review` runs. A long
  gap between reviews delays every trigger check by the same gap.
- The bump-gate paragraph now carries two duties. A third duty must
  first add a gate-accretion entry to the watchlist, so the gate never
  grows without a record. No seed watches the gate today.
- `check_docs.py` recognizes exactly four doc paths. A doc file outside
  that set repeats BUG-0001's failure. The set stays a list, so the
  rule-membership check applies to any future edit of it.
- A heading form that the widened pattern still misses now prints a
  marker rather than an empty body. The marker costs the caller one
  direct read of the spec.
- The plan header grows by one line. Item 11 checks the line on every
  new plan.
- A spec whose plans predate the `**Spec:**` field still depends on the
  stem and date rules. A pre-field spec with two plans can still lose its
  second outcomes file.
- A logged `Miss` produces a Recommendation on one entry.
  ArcGISProMCP logs 43 Misses in 482 entries, so its reviews can carry
  more Recommendations than before. The rule "names a target file and the
  exact change" still sends a vague `Miss` to Gaps.
- No check enforces the `Gap` disposition when an agent writes the entry.
  `process-review` step 2 lists a `Gap` with an empty field 4 under Gaps
  as `(no mechanism proposed)`, so the omission shows in the review.
- A `Gap` still waits for the next review, up to three specs away. The
  disposition makes the wait cheaper to act on. It does not shorten the
  wait.
- The plan's cross-section pass found no other text to change. It
  checked `process-review/SKILL.md`'s frontmatter, Core principle, and
  No Placeholders section for a claim that `notes.md` holds only
  `Catch`, and it searched `plugin/` and `docs/patterns/` for another
  list of plan-header elements. Neither search found one.

## Alternatives Considered

Each choice came from step 4's inline proposal. No research skill ran.

| Decision | Candidates | Chosen | Confidence and evidence |
|---|---|---|---|
| Spec structure | A. one new spec superseding 09-08; B. amend 09-08 in place; C. separate spec after 09-08 | A | Medium-high. The 09-08 spec has no plan and no code change. Its part D and part E edit the same 68-line script. Part A and part G edit the same step-2 sentence. |
| Spec-to-plan anchor | A. `**Spec:**` header field; B. header-region grep; C. commit trailers | A | Medium. Measured over-matches: full text 9, header region 2, field 0. Trailers found nothing for ArcGISProMCP's `edit-module` spec. |
| Failed-section signal | A. keep the verdict, mark the section; B. new `SPEC_UNREADABLE` verdict and exit code | A | High. Three of the four callers branch on the first line only. Every measured failure sits in a section body, never in the verdict. |
| `Gap` field 4 | A. disposition required; B. free-form | A | Medium. The one `Gap` on record named the right mechanism on day 1. ArcGISProMCP shipped the same rule on its side. |
| Logged `Miss` route | A. own Recommendation; B. counts toward recurrence | A | Medium. The recurrence threshold infers a failed check. A logged `Miss` records it directly. |

## RESULT

*(filled at Finish)*
