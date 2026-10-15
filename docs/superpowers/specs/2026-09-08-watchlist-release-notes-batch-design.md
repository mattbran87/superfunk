# Watchlist and Release-Notes Batch — Design

**Date:** 2026-09-08
**Status:** Superseded by 2026-10-15-watchlist-and-findings-batch-design.md
**User-Facing:** Yes

## Context

The post-ship review discussion of the R1–R4 batch (notes.md, 2026-09-02
entries) opened five follow-ups. One (the Step 4 opener fix) shipped
already, in `2026-09-02-executing-plans-review-step-design.md` commit
`6524b43`. This batch closes the remaining four:

- **A. Watch items have no durable home.** Three Watch entries sit in
  notes.md with triggers and pre-decided actions, but notes.md entries
  get one review window of attention. Review Gaps G1 and G3 survive
  across windows only because each review hand-copies them forward.
- **B. `plugin/RELEASE-NOTES.md` sits dormant since the fork point.**
  The rebrand spec names it "this project's own established changelog
  file." The fork shipped 6.3.0, 6.4.0, 6.5.0, and 6.6.0 with no entry.
  Upstream separately released its own v6.3.0, so the numbers now
  collide across two histories. Human-partner decision (notes.md,
  2026-09-02): MAINTAIN.
- **C. Nothing makes future bumps write an entry.** The 6.6.0 bump
  happened after the Maintain decision and wrote no entry — the
  predicted failure mode, observed once already.
- **D. `check_docs.py` cannot do its job on this machine.** Line 47
  matches only bare root `README.md`/`CHANGELOG.md` (BUG-0001, plus the
  rebrand spec's deferred RELEASE-NOTES recognition), and the section
  printer crashes on Windows cp1252 consoles for any spec with an
  em-dash (BUG-0002). Three tasks in the R1–R4 batch each hit the same
  false ACTION_NEEDED. Human-partner decision: fix all three.

## Decisions

1. **One micro-batch spec, four items.** Same mold as taskq-batch1 and
   R1–R4: heterogeneous mechanical fixes, one pipeline pass, one Finish.
2. **No trials.** Every item changes procedural bookkeeping, a document,
   or a script with directly runnable acceptance checks — the R4 class,
   not the R1 class. No item claims a behavior change that a trial
   would establish.
3. **Watchlist data flow: notes.md as intake, watchlist.md as store,
   process-review as the transfer-and-check mechanism.** Sessions log
   `Watch` entries to notes.md exactly as before. Each process review
   harvests the window's Watch entries into the watchlist, then
   evaluates every watchlist entry's trigger. A direct-edit flow lost
   to this design: two write paths drift, and review time gives an
   audit moment for free.
4. **The gate duty covers every bump, patch included.** Upstream's file
   records patch releases; a one-line entry costs less than a gap.

## Design

### A. Watchlist mechanism

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
The plan drafts each seed entry's full text from the notes.md originals
and the review file's Gaps section.

**Skill hook:** two edits to `plugin/skills/process-review/SKILL.md`:

1. Amend step 2: an entry's second field may read `Watch` instead of
   `Catch`. Collect Watch entries separately; exclude them from Catch
   synthesis.
2. Insert a new step between steps 4 and 5 (later steps renumber):
   append the window's Watch entries to
   `docs/superpowers/process-reviews/watchlist.md` in the entry format
   above; then, for every watchlist entry, evaluate its trigger against
   this window's evidence. A tripped entry becomes a Recommendation
   that names the entry's pre-decided action. A resolved or obsolete
   entry leaves the file, with a one-line removal note in the review.
   Every other entry stays. The review names how many entries it
   checked, so an unread watchlist shows up as a zero.

### B. RELEASE-NOTES backfill

Insert directly under the `# Superpowers Release Notes` H1:

1. A short **Fork** note: superfunk diverged from obra/superpowers
   after v6.2.0; entries above the v6.2.0 heading describe superfunk;
   upstream's own later version numbers (it released a different
   v6.3.0) share numbering by coincidence only.
2. Four new entries in the file's existing `## vX.Y.Z (YYYY-MM-DD)`
   format, newest first: v6.6.0 (Step 2.5 whole-branch review for
   executing-plans), v6.5.0 (R1–R4 batch: trial-gated drafted-insertion
   check, outcome-space rule, de-jq'd bump script, Finish bookkeeping +
   bump gate), v6.4.0 (three trial-gated mechanisms: rule-membership
   check, Rule-sentence enumeration, behavioral-claim widening), v6.3.0
   (rebrand to superfunk and the surrounding fix waves). A few bullets
   each, sourced from the specs; dates from the bump commits. The plan
   drafts the full text.

Everything from the `## v6.2.0` heading down stays byte-identical.

### C. Release-notes duty in the bump gate

Append to both gate copies, worded identically and edited together
(`plugin/skills/subagent-driven-development/SKILL.md` and
`plugin/skills/executing-plans/SKILL.md`):

> Before that commit, append this version's entry to
> `plugin/RELEASE-NOTES.md` — a `## vX.Y.Z (date)` heading and at
> least one bullet — and include it in the same commit as the bump.

The existing normalized-extraction identity check extends to cover the
longer block. The gate paragraph now carries two duties (bump +
entry); the watchlist's gate-accretion analog to item-10 applies — the
plan adds no watchlist entry for it yet, one duty added once.

### D. check_docs.py fix-all

Two edits to `plugin/skills/documentation/scripts/check_docs.py`:

1. Top of `main()`:
   `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` —
   closes BUG-0002.
2. Line 47's set extends to
   `("README.md", "CHANGELOG.md", "plugin/README.md", "plugin/RELEASE-NOTES.md")`
   — closes BUG-0001 and the rebrand spec's deferred recognition item.

Close both `docs/bugs/` files per the bug tracker's own format, and
annotate the rebrand spec's Deferred bullet as resolved by this spec.

## Falsifiable Criteria

1. `watchlist.md` exists with the six seed entries, each carrying
   Watching, Trigger, and Action fields.
2. `process-review/SKILL.md` recognizes the `Watch` type in step 2 and
   contains the harvest-and-evaluate step; step numbering stays
   consecutive with no dangling cross-references.
3. `plugin/RELEASE-NOTES.md` contains the Fork note and four new
   version headings above `## v6.2.0`; `git diff` shows additions only
   above that heading.
4. Both gate copies contain the new sentence; the normalized-extraction
   diff over the extended block prints IDENTICAL.
5. On this machine: `check_docs.py` returns `NOT_APPLICABLE` (exit 0)
   on a `User-Facing: No` spec; prints its full `ACTION_NEEDED` report
   without traceback on a `User-Facing: Yes` spec containing em-dashes;
   and returns `ALREADY_UPDATED` (exit 0) when the diff range includes
   `plugin/RELEASE-NOTES.md`. BUG-0001 and BUG-0002 records close.
6. This batch's own Finish executes the full bookkeeping list, and its
   bump commit contains this batch's own RELEASE-NOTES entry — the
   first live execution of item C's duty.

## Out of Scope

- Resolving G1, G2, or G3 themselves — this batch gives them watchlist
  homes with triggers; the entries fire later or not at all.
- Retiring the notes.md Watch intake, or teaching other skills to write
  watchlist entries directly.
- Any upstream sync or renumbering to escape the version collision —
  the Fork note documents it instead.
- Trial-gating any item (Decision 2).

## Consequences

- The process-review skill gains one step — net new load, justified:
  without it, Watch entries hold attention for one window and the gap
  list survives by hand-copying, measured across two reviews.
- The watchlist stays load-bearing only while process-review runs; a
  long gap between reviews delays trigger checks by the same gap.
- The gate paragraph now holds two duties. A third duty joins the
  item-10 accretion watch rather than the gate silently growing.
- check_docs.py recognizes exactly four doc paths. A future doc file
  outside that set repeats BUG-0001's shape; the set stays a list, and
  the rule-membership check applies to it at any future edit.

## RESULT

*(filled at Finish)*
