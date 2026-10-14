# External project — `ArcGISProMCP` — findings for superfunk

**Reporting project:** `C:\Users\marko\source\repos\ArcGISProMCP` — an MCP server that drives a
running ArcGIS Pro session through a named pipe and a companion add-in. C#, .NET, Windows only.
Five plans shipped through the full superfunk pipeline (A–E), plus a sixth harness-hardening
plan (F). It is not a trial fixture. It is a real project with real hardware in the loop.

**Plugin version at the time of writing:** 6.6.0, read from
`plugin/.claude-plugin/plugin.json:4` on 2026-09-15.

**Source of these findings:** the project's own process review,
`C:\Users\marko\source\repos\ArcGISProMCP\docs\superpowers\process-reviews\review-after-2026-09-14-sdk-facts-and-fixture-hardening-design.md`,
committed as `7f144aa`. That review covers three shipped specs (navigate, select, hardening),
58 raw `notes.md` entries, and 27 fix commits, over the window 2026-09-11 → 2026-09-15.

**Date:** 2026-09-15.

**What this document asks for.** The source review produced 9 Recommendations. Five of them
change files inside ArcGISProMCP and that project is fixing them itself. **Four of them change
superfunk's own skill files, and those four are what this document carries.** A fifth is
offered as optional. Nothing in ArcGISProMCP has been edited to depend on any of these — act on
them, defer them, or reject them freely.

**What this document does not do.** It proposes no edits to `plugin/`. The reporting project
deliberately did not touch the plugin source. Every proposed change below is a draft for a
superfunk session to take through superfunk's own pipeline.

---

## 1. Executive summary

Five findings, labelled **A1–A5** to avoid collision with the `F1–F15` labels the taskq trial
already used.

| # | Target skill | Miss it closes | Cost | Recommended |
|---|---|---|---|---|
| **A1** | `writing-plans` Self-Review | An SDK behaviour the design assumed, never measured | net new item | **Yes — strongest evidence in the set** |
| **A2** | `writing-plans` Self-Review | A check answers a narrower question than the claim it supports | net new item | **Yes** |
| **A3** | `subagent-driven-development` Finish | The stand-in cannot express the defect | net new step | **Yes** |
| **A4** | `subagent-driven-development` Step 1 | The controller's own dispatch carries false claims | net new bullet | Yes, with a caveat — see §7 |
| **A5** | `writing-plans` or `docs/patterns/` | A correction propagates less far than the claim it corrects | pattern or item | Optional |

**The headline finding is A1.** On the select branch, the plan spiked three SDK behaviours the
design felt uncertain about. All three held and none produced a defect. **Six behaviours the
design simply assumed each produced a defect**, including two in the same method of the same
API, both of which shipped to `main`. Two of the six were worse than unmeasured: the measurement
already existed and did not reach the code — once from three steps earlier in the same session,
once from the previous plan. No Self-Review item in `writing-plans` asks which API calls a
design depends on, and `grep -rn "measurement inventory\|MEASURED / DOCUMENTED\|MEASURED,
DOCUMENTED" superfunk --include=*.md` returns zero hits, so this is net new.

**A4 independently reproduces taskq trial finding F15** — *every adversarial pass in
`subagent-driven-development` sits downstream of the brief, and the brief is where the defects
are.* ArcGISProMCP hit that from the other end. See §6, which also records that **F15's own
proposed fix does not appear in the shipped v6.6.0 text**.

**A2 targets the window's dominant pattern.** It appeared in all three reviewed specs, was named
explicitly part-way through, and then recurred in both later specs after being named. Every
instance looked like evidence: a command ran, its output was quoted, and the question it
answered was not the question being claimed.

---

## 2. Why this project's evidence is worth reading

The taskq and bookmark-cli trials were driven fixtures. This project is not. Three properties
make its failures different:

1. **A live-hardware test stage no unit test can substitute.** Every plan ends with a scripted
   pass against a real ArcGIS Pro process — 184 checks as of 2026-09-15. **Every plan found
   defects there that nothing cheaper caught.** On the select branch the live pass found
   `pro_select_by_location` had `within` and `contains` swapped; the compiler, unit tests, a
   full MSBuild, a task review, and a most-capable-model review all passed that code.
2. **Long enough to show recurrence.** Five shipped plans, roughly 119 logged defects, and two
   process reviews. A Miss here is measured across specs, not inferred from one incident.
3. **A domain where "it compiles" proves very little.** The SDK is a closed third-party API
   whose member names actively mislead. `SpatialRelationship.Within` and `.Contains` describe
   the filter geometry's relationship to the candidate feature, not the reverse — which is the
   opposite of their plain English reading, and is the direct cause of the swap above.

That third property is what makes **A1** matter. A project whose dependencies are well
documented may see less from it.

---

## 3. Verify this before trusting anything below

**superfunk's own `notes.md` records a case where a process review claimed a mechanism failed
when no mechanism had loaded** (entry dated 2026-09-01, `Process review
(convention-retirement)`): `~/.claude/plugins/config.json` read `{"repositories": {}}`, the
session ran upstream superpowers 5.1.0 throughout, and superfunk's conventions got applied by
hand by the same agent that authored the documents under review.

**That exact risk applies to this document, and I could not fully rule it out.** Here is what I
checked and what it proves.

| Check | Result | What it establishes |
|---|---|---|
| `C:\Users\marko\source\repos\ArcGISProMCP\.claude\settings.local.json` | `enabledPlugins` sets `superfunk@superfunk-dev: true` and `superpowers@claude-plugins-official: false`; `extraKnownMarketplaces.superfunk-dev` points at `C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin` | The project **declares** the fork as its source, by directory, and disables the marketplace copy |
| `C:\Users\marko\.claude\plugins\config.json` | `{"repositories": {}}` | The same reading that accompanied the 2026-09-01 mis-attribution. Here it is expected — the project uses `extraKnownMarketplaces` in project settings rather than a global repository entry — but it is **not** positive proof the fork loaded |

**Before acting on A1–A4, confirm the skill text quoted in §5 is the text that actually ran.**
The cheapest confirmation: in a session opened on ArcGISProMCP, check that the available skills
carry `superfunk:` ids and that `writing-plans`' Self-Review holds 14 items. If it holds 3, the
marketplace copy loaded and every finding below needs re-reading as "the fork's text would not
have prevented this either" rather than "the fork's text failed".

The quoted anchors in §5 were read from the fork's files on 2026-09-15 and are accurate for
v6.6.0 whatever loaded in the reporting project.

---

## 4. The four recurring Misses these findings come from

Taken verbatim in substance from the source review's own analysis. A Miss is a Catch that
recurred across two or more reviewed specs.

| Miss | Statement | Specs | Finding |
|---|---|---|---|
| **M-1** | A check answers a narrower question than the claim it supports | all 3 | A2 |
| **M-2** | The stand-in cannot express the defect | all 3, 6th occurrence overall | A3 |
| **M-3** | A measurement that exists does not reach the code that needs it | all 3 | A1 |
| **M-6** | A correction propagates less far than the claim it corrects | 2 of 3 | A5 |

Two further Misses (M-4, two callers of one decision with one covered; M-5, a fix wave
introducing a defect of the class it was closing) produced **no** superfunk recommendation. Both
were caught reliably by mechanisms superfunk already ships — the whole-branch review and the
scoped re-review of the fix wave. They are recorded here as **positives**, see §8.

---

## 5. Findings

### A1 — No Self-Review item asks which API behaviours the design assumed

**Severity: high. Cost: one net-new Self-Review item plus the spike work it triggers.**

#### What happened

On the select branch, the plan's Task 1 measured three SDK behaviours the design had flagged as
open questions. All three measurements held. **None of the three produced a defect.**

Six behaviours the design treated as settled each produced a defect:

| Behaviour assumed | How it failed | Where it was caught |
|---|---|---|
| `SpatialRelationship.Within` / `.Contains` read feature-first | The SDK applies them FilterGeometry-first — the opposite | **Live pass only.** Compiler, unit tests, task review and a most-capable-model review all passed it |
| Applying a spatial predicate to a union of reference features answers the same question as applying it per feature | It does not. `contains` became "contains *all* references at once" | **Whole-branch review.** Rated Critical. The spec's own pseudocode specified the union, so the code and the spec were wrong together |
| An empty `ObjectIDs` collection constrains a selection to nothing | ArcGIS Pro 3.6.2 treats it as **unconstrained**. A zero-match `replace` selected the entire layer, measured at `Selected 3 feature(s)` where zero matched | **Scoped re-review of the fix wave.** Introduced by the fix for the row above |
| `SelectionCombinationMethod`'s members | The controller had measured them during brainstorming and left them out of the brief; the implementer re-derived them from IL | Implementer reporting rather than repairing |
| `Wkid` inequality implies spatial-reference inequality | It does not. **Already measured on the previous plan, in commit `5149daa`** | Task review |
| `SpatialReferenceBuilder`'s failure modes | Fails two undocumented ways; `wkid 0` returns `IsUnknown` without throwing | The plan's own measurement task — this one was caught early |

Raw entries: `notes.md` `:110`, `:115`, `:120`, `:126`, `:131`, `:133`. The human partner raised
the pattern directly at `:133` and the review adopted it.

#### The mechanism

`writing-plans`' Self-Review has 14 items. Item 7 checks `docs/lessons-learned.md`. Item 13 runs
a hostile-input pass over each code block. **No item asks what the design believes about an API
it calls, nor whether that belief was ever observed.** The spike work therefore gets aimed by
the design's own sense of uncertainty — and the evidence above says that sense is
anti-correlated with where the defects are.

Note the two worst rows: `Wkid` and `SelectionCombinationMethod`. Both were **already measured**.
An inventory catches these even when no new spike runs, because the inventory forces the
question "does the code that needs this fact carry it?"

#### Proposed change

Add a 15th item to `plugin/skills/writing-plans/SKILL.md`' Self-Review. Insert it after item 14
(which ends at line 295) and before the closing line at 297, `If you find issues, fix them
inline.`

> **15. Measurement inventory:** List every external API call this plan's tasks depend on — a
> third-party SDK member, a platform call, a tool whose output a step parses. Mark each
> **MEASURED** (this project observed the behaviour and can cite the record), **DOCUMENTED**
> (vendor documentation states it and the version matches), or **ASSUMED** (neither). For each
> MEASURED entry, name the task that carries the fact into the code — a measurement that exists
> and does not reach the code is the same failure as no measurement. Spike every ASSUMED entry
> before the plan ships, however confident the design sounds. A design's own sense of which
> behaviours are uncertain is not evidence: on one reviewed branch, three spiked behaviours all
> held while six assumed ones each produced a defect.

#### Interactions and risks

- **Checklist length.** This makes 15 items. The reporting project's review flagged it "net new
  load" and justified it on the evidence above. A superfunk session may reasonably decide the
  list needs splitting rather than extending.
- **Scope wording matters.** "External API" is the load-bearing phrase. A project with no
  third-party API should reach the item, answer "none", and move on in one line. Word it so an
  empty inventory is a legitimate answer, or it becomes ritual.
- **The three-way mark is doing real work.** DOCUMENTED is not MEASURED. Two of the six
  behaviours above are documented by Esri and still wrong for version 3.6.2.

#### What would falsify it

A branch where the inventory runs, marks something ASSUMED, spikes it, and the spike finds
nothing — repeated enough that the spike cost exceeds what it prevents. Track the per-branch
count of ASSUMED entries and how many spikes changed a decision.

---

### A2 — Nothing asks whether a verification command answers the question being claimed

**Severity: high — the window's most frequent single pattern. Cost: one net-new item.**

#### What happened

Eleven instances across three specs. Each one ran a command, quoted real output, and drew a
conclusion the command did not support.

| Instance | The command | What it actually answered |
|---|---|---|
| `notes.md:112` | a substring check on a tool's reply, asserting a mode worked | The substring also appeared in a **refusal** message. 3 of 4 mode checks could not fail. Rated Critical |
| `notes.md:109` | the same shape again, one spec earlier | A check passing on a substring of a refusal |
| `notes.md:116` | a boundary check on a cap | Both `>` and `>=` pass it. The boundary that actually runs is pinned by nothing |
| `notes.md:148` | a verification claim about a test artifact | The command ran at a 2-test interim state and the claim was reported against the 9-test artifact, which did not exist when it ran |
| `notes.md:103` | six separate instances on one branch | Named at the time, then recurred in both later specs |
| the `Enforced by` column | `docs/sdk-facts.md` carries a column stating which test enforces each row | The column was verified for **format**, never against the codebase. One row of five claiming `Enforced by: Nothing` was enforced by three live checks |

`notes.md:160` is the clearest miniature: a document said "the eight checks", adding five
navigate **tools** to a criterion's three **checks** — two different units summed into one
number, in a sentence that read as a count.

#### The mechanism

Item 10 covers `Expected:` **values** — counts, budgets, and greps against drafted insertions.
It confirms the number is real. **It does not ask what proposition the number supports.** The
failure is upstream of arithmetic: the command is correct, its output is correct, and the
sentence built on it asserts something wider.

This is the same family as taskq **F13** (item 10 checked enumerated counts, not asserted
budgets), but it is not the same fix. F13 widened *which numbers* item 10 covers, and that
widening shipped — v6.6.0 lines 251–257 now name "any numeric budget the plan's Global
Constraints section states". A2 is about the **inference**, not the number.

#### Proposed change

Add as a 16th Self-Review item, beside A1's 15th:

> **16. Claim-to-command match:** For every claim a step verifies, write the question the
> command actually answers directly beside the claim it supports, and confirm they match. A
> substring check answers "does this text appear somewhere in the output" — not "did the tool
> succeed", because a refusal message may contain the same substring. A boundary check that
> passes under both `>` and `>=` answers "is there a cap" — not "is the cap at N". A command run
> against an interim state answers a question about that state, not about the final artifact.
> Where the two do not match, either change the command or narrow the claim.

#### Interactions and risks

- **Do not add this to item 10.** `notes.md` 2026-09-02 carries an open **Watch** entry on
  exactly this: *"writing-plans Self-Review item 10 accretion — trigger: any change gives item
  10 a fourth duty (it now carries three: run Expected-count commands, budget arithmetic,
  drafted-insertion grep). Action: split item 10 into separate items via its own spec; the
  drafted-insertion sentence is trial-tested and must move verbatim, not be reworded."* The
  reporting project's review proposed appending to item 10 without knowing that Watch existed.
  **Appending would trip the trigger.** Ship A2 as its own item, or fold it into the item-10
  split the Watch already prescribes.
- **This is the one finding with a cheap mechanical proxy.** A grep for unanchored substring
  assertions in test files catches the three worst instances above. It is narrower than the
  item, but it needs no judgment.

#### What would falsify it

A branch where the item fires, every claim matches its command, and nothing is found — while a
later review still finds an M-1 instance on that same branch. That would mean the item is asked
at the wrong moment, not that the Miss is absent.

---

### A3 — Nothing names the check that reads each new fixture feature

**Severity: medium-high. Sixth occurrence of the underlying Miss. Cost: one net-new Finish step.**

#### What happened

The hardening plan's whole subject was closing gaps in a test fixture. It added five layers.
**Four of them are read by no check.**

`pipelines`, `parcels_joined`, `broken_source` and `degenerate` appear in
`tools/manual-test/desktop_pass.py` only inside a layer-*order* assertion at lines 1133–1135.
Only `wells_utm` is genuinely exercised, by criterion 25.

The sharpest detail: `pipelines` is a line layer, and it exists **specifically** because a
zero-area clamp defect on the navigate branch survived 117 checks — no fixture feature had
exactly one zero dimension, so no check could distinguish a `||` from an `&&` in the guard
(`notes.md:104`). The capability to catch that defect was built, and the question was never
asked. The plan's own text at line 440 claims `pipelines` "is exercised by Task 8's live pass";
`grep -c "pipelines" tools/manual-test/desktop_pass.py` returns 1, and that one hit is the
ordering assertion.

Earlier occurrences of the same Miss: `notes.md:104`, `:108` (a `degenerate` layer that could not
express its defect because arcpy stores a NULL shape), `:159`, and three more before this window.

#### The mechanism

SDD's Finish section (lines 556–661) covers spec Status, the process-review tracker, the
Recommendation check-off, a bookkeeping self-verification, the lessons-learned capture, the
version bump, the concept index, parked findings, and workspace deletion. **It does not look at
test fixtures at all.** Every prior catch of this Miss came from someone noticing ad hoc — four
times out of six.

#### Proposed change

Add a step to `plugin/skills/subagent-driven-development/SKILL.md`' Finish. Place it beside the
existing bookkeeping-verification block, which ends at line 597, so it runs before the
lessons-learned capture:

> If this plan added or changed a test fixture — a generated data file, a seeded database, a
> recorded response set — list each feature it added. For each one, name the check that reads
> it. A feature no check reads is not a closed gap; it is a capability resting on a future
> plan's goodwill. Either add the check now, or record the feature as unexercised in the
> project's own test record, naming what it would catch if something asked. A fixture feature
> built and never read has verified nothing, and the plan text claiming otherwise is the defect.

**This replaces an existing informal mechanism** rather than adding pure load: the ad-hoc
noticing that caught four of the six occurrences.

#### Interactions and risks

- **"Fixture" needs a portable definition.** In this project it is a generated ArcGIS project
  with layers. In taskq it would be a seeded JSONL state file. Word it by role — the stand-in
  the tests read — not by file type.
- **The honest-record escape hatch is required, not optional.** Some fixture features are built
  one plan ahead of the checks that use them, for good reasons. Forcing a check immediately
  would push plans to write a weak check instead of an honest note.

#### What would falsify it

A project where fixtures are small and every added feature is read by the same task that added
it. There the step costs one line per Finish and finds nothing.

---

### A4 — Nothing confirms the controller's own dispatch claims against the tree

**Severity: medium. Cost: one net-new dispatch bullet. See the caveat in §7.**

#### What happened

On the select branch, one task's dispatch carried **three false controller-authored claims**
(`notes.md:117`):

1. A claim that a DTO already existed. The controller had written it, then deleted it.
2. A wrong tool count.
3. A wrong home directory for a test file.

That task returned 1 Critical, 3 Important and 2 Minor in a single review round. The review's
own Friction section concludes: **brief quality, not implementer quality, drove that round.**

`notes.md:110` is the same class with a different shape: the controller had measured
`SelectionCombinationMethod`'s members during brainstorming and did not put them in the brief.
The implementer re-derived them by decompiling the SDK.

`notes.md:111` records three more defects in one task's text, including a guard the plan
specified and never wired up.

Across the select branch, **nine findings came from implementers reporting rather than
repairing**, and every one was a defect in the controller's own brief.

#### The mechanism

SDD Step 1 (lines 208–275) is precise about *structure*: run `scripts/task-brief`, keep the
brief as the single source of requirements, fold in curated directory context, pseudocode
context and concept-index context, never paste history. **It says nothing about whether the
controller's own additions are true.**

The distinction matters for where the fix goes. `scripts/task-brief` extracts the task's text
from the plan verbatim, so an error inside the extracted brief is a *plan* error, which
`writing-plans`' Self-Review owns. The three false claims above sat in **dispatch items (3) and
(4)** — "interfaces and decisions from earlier tasks that the brief cannot know" and "your
resolution of any ambiguity you noticed in the brief". Those are written fresh by the
controller at dispatch time and no check reads them.

#### Proposed change

Add a bullet to Step 1, after the `Concept-index context` bullet (ends line 259) and before
`Report file`:

> - **Dispatch-claim check:** items (3) and (4) of the dispatch are written by you, not
>   extracted from the plan, and nothing downstream verifies them. Before dispatching, confirm
>   every existence claim and every count you wrote against the actual tree — a type you say
>   exists, a file you name as a test's home, a count of anything. Check the tree, not your
>   memory of earlier tasks in this session: one recorded failure was a DTO the controller had
>   written and then deleted. If you measured a fact earlier in this session that this task
>   needs, put the fact in the dispatch rather than the instruction to go find it.

#### Interactions and risks

- **This is the smaller half of taskq F15.** See §6. F15's own proposed fix targets the
  reviewer; this targets the dispatch. They are complementary and neither subsumes the other.
- **Cost is real and recurring.** It runs once per task, not once per plan. The reporting
  project's review marked it "net new load" and justified it on `:117` and `:110` alone, which
  is one task and one omission. That is the thinnest evidence base of the four.
- **If the checklist must stay flat, this is the one to defer**, and A1 is the one to keep.

#### What would falsify it

Counting, over one branch, how many dispatches carry a claim the check corrects. The reporting
project's own number is 2 tasks out of 9 on one branch.

---

### A5 — Optional: a correction propagates less far than the claim it corrects

**Severity: medium. Cost: a pattern file, or one Self-Review item. Offered, not recommended.**

#### What happened

Six instances across two specs. Each time a measurement retired a claim, the correction reached
some copies of the claim and not others.

- A document whose own header calls it authoritative asserted "every other row is still unbuilt"
  three lines above a table showing otherwise (commit `2287fee`).
- A mutation-blind assertion was cured in one file and left in its sibling (`notes.md:128`).
- On the hardening branch, four times in one branch: a retired conclusion reached five documents
  when four were listed; "a clean exit is untested" survived in `sdk-facts.md` row 18, **two rows
  above a row the same commit edited**; the same claim survived again in the manual-test record
  that rows 18 and 21 cite as their evidence; and a tenth test left two entry-point documents
  reporting nine.

**Every instance passed its mechanical checks.** The citation resolved, the line numbers were
right, and only the intended files changed.

#### Why it is optional

ArcGISProMCP is fixing this in its own `CLAUDE.md` rather than asking superfunk for it. The rule
is short: when a measurement retires a claim, grep the claim's distinctive phrase repo-wide
**before** editing, fix every hit in one pass, and leave dated records at their original values.

It reaches superfunk only if the framework wants it generally. The case for that: superfunk
already ships `docs/patterns/hunt-the-workaround-not-the-feature.md`, and Self-Review item 14
applies exactly this method to a *removed limitation*. A5 is the same method applied to a
*retired claim*. Widening item 14 may be cheaper than a new item — but item 14's current wording
is specific enough that widening could blunt it.

The dated-records carve-out is the part most likely to be got wrong by a general rule. A
manual-test record stating "197 tests" is **correct** as a dated record of a run where 197 was
true, and must not be "fixed" to 198.

---

## 6. Corroboration of taskq finding F15, and its fix status

`external-trial-taskq-findings.md` F15 states: **every adversarial pass in
`subagent-driven-development` sits downstream of the brief, and the brief is where the defects
have been.** Its triage table rates it Low cost — *"one item in `task-reviewer-prompt.md`"*.

**ArcGISProMCP reproduced this independently, on a real project, at Critical severity.** The
select branch's union defect:

- The spec's own pseudocode specified the union.
- The handler implemented the union.
- The per-task review compared the handler to the brief, found them to match, and passed it.
- **The fixture agreed with the wrong answer.** With two flood zones, both the correct and the
  incorrect reading return the same two numbers.

Four checks passed that defect and all four compared against the same wrong premise. The project
wrote it up as a lesson in these words:

> **An implementation checked against its own spec cannot fail on a defect they share.**

**F15's proposed fix does not appear to have shipped.** Checked on 2026-09-15 against v6.6.0:

| Check | Result |
|---|---|
| `grep -n "^ *## " plugin/skills/subagent-driven-development/task-reviewer-prompt.md` | Sections are: What Was Requested, What the Implementer Claims They Built, Diff Under Review, **Do Not Trust the Report**, Tests, Mutation Check, Part 1: Spec Compliance, Part 2: Code Quality, Calibration, Output Format |
| `grep -n -i "brief" task-reviewer-prompt.md` | 3 hits: line 23 "Read the task brief", line 183 "If the plan or brief explicitly mandates something this rubric calls a…", line 228 the placeholder definition |
| `grep -rn -i "wrong together\|shares the defect\|same premise\|premise" task-reviewer-prompt.md re-review-prompt.md` | 0 hits |

There is a **Do Not Trust the Report** section and no equivalent for the brief. Line 183 runs the
other way — it tells the reviewer to defer to the brief where it mandates something the rubric
would flag.

**A superfunk session should confirm this against its own record before acting.** If F15 was
closed by a different mechanism, that mechanism did not prevent the union Critical here, and the
question becomes why. If it was never closed, ArcGISProMCP's Critical is a second data point for
a fix already triaged as Low cost.

One caution from this project's experience, offered because it makes F15's fix harder than it
looks: telling a reviewer "do not trust the brief" leaves it nothing to calibrate against. What
actually found the union defect was reading the components as one system and asking whether
combining inputs before applying a predicate answers the same question as applying it one at a
time. That is a question about the **domain**, not about trust, and it is not obvious how to ask
it generically in a rubric.

---

## 7. What ArcGISProMCP is fixing itself

Listed so a superfunk session does not duplicate the work, and so the evidence trail stays
complete. None of these are superfunk's concern.

| Recommendation | Where it lands |
|---|---|
| The M-6 grep-before-editing rule | `ArcGISProMCP/CLAUDE.md` conventions section |
| Assert `tools/list` = 16 and = 20 | `tests/ArcGISProMCP.McpServer.Tests/McpPipelineTests.cs` |
| An `Enforced by` column check for `docs/sdk-facts.md` | `tests/ArcGISProMCP.SdkFacts.Tests/SuiteShapeFacts.cs` |
| Live checks reading the four unexercised fixture layers | `tools/manual-test/desktop_pass.py` — needs a live ArcGIS Pro pass |
| Define or close one vague outcomes follow-up | `docs/superpowers/plans/2026-09-13-select-module-outcomes.md:173` |

---

## 8. Positives — mechanisms that worked, do not weaken them

Two Misses in the window produced **no** recommendation, because superfunk's existing steps
caught them reliably. Both are worth protecting.

**The whole-branch review catches what per-task review cannot see by construction.** M-4 (a guard
covering some callers but not all) recurred across two specs, and every instance was caught by
the whole-branch review. `notes.md:127` states the reason directly: a per-task reviewer reading a
diff cannot see a guard that lives outside it.

**The scoped re-review of the fix wave catches defects that fixes introduce.** M-5 recurred on two
branches and **the scoped re-review caught both**:

- navigate: an off-by-one at the cap, with the new unit test pinning the wrong wording.
- select: an empty `ObjectIDs` collection reading as unconstrained, so a zero-match `replace`
  selected the entire layer. Measured at `Selected 3 feature(s)` where zero matched.

The project's own record says an earlier plan skipped this step and the Critical its fix
introduced reached `main`, where it sat until someone ran the re-review afterwards.

**One habit worth naming in a skill.** `notes.md:125` records the single positive instance the
review singled out: an implementer reported 178/178 green and stated, unprompted, that a new SKIP
path did not fire — *"which is a property of this run's timing, not proof the race is gone."*
That is A2's discipline expressed voluntarily. **Report what a check established, not what it
returned.** M-1 is what happens when it lapses.

---

## 9. Suggested order of work

1. **A1** — the strongest evidence and the largest class of escaped defect.
2. **A2** — the most frequent pattern, but read the item-10 Watch in §5/A2 first and decide
   whether to ship it as a new item or as part of the prescribed split.
3. **F15 status check** (§6) — cheap, and it decides whether A4 is half a fix or a whole one.
4. **A3** — replaces an ad-hoc mechanism rather than adding load.
5. **A4** — thinnest evidence, recurring per-task cost. Defer with a reason if the checklist
   must stay flat.
6. **A5** — only if superfunk wants the rule generally.

Every proposed text above is a draft. None of it has been through superfunk's own spec, plan,
review and trial pipeline, and the taskq trial's own record shows that a plausible skill edit can
lose to the unmodified text on the exact dimension it targets.

---

# Addendum — 2026-09-24, after `2026-09-23-edit-module-slice-2-design.md`

Two findings from the second process review this project has run. Both were found by **following a
skill's instructions literally and noticing what they missed**, which is the same way A1–A4 arose.

Same caveat as above: every proposed text is a draft, unreviewed by superfunk's own pipeline.

## A5 — `process-review`'s outcomes lookup drops a spec that shipped across two dated plans

**Severity: real, and silent.** It does not error; it returns less material and says nothing.

### What happened

`process-review` step 3 resolves each shipped spec to its plan-outcomes file by two rules: strip the
trailing `-design` from the spec filename, and if that path does not exist, fall back to matching
`docs/superpowers/plans/*-outcomes.md` against the spec's own `YYYY-MM-DD` prefix.

The spec `2026-09-19-edit-module-design.md` shipped in **two branches**, three days apart:

- `docs/superpowers/plans/2026-09-19-edit-module-surface-outcomes.md` — reached by the date fallback
- `docs/superpowers/plans/2026-09-20-edit-module-handlers-outcomes.md` — **reached by neither rule**

The stem rule fails (no `2026-09-19-edit-module-outcomes.md`). The date fallback matches only
`2026-09-19-*`, and **no spec carries the date 2026-09-20**, so the handlers file is unreachable from
any spec in the list. Following the instructions literally would have dropped **32 notes entries'
worth of context** — an entire branch — from a review that covers that spec.

The reviewer read it manually only because it had independent knowledge the file existed.

### The mechanism

The lookup assumes **one spec produces one plan**. That assumption is silently violated by the
pattern this project uses for large specs — ship the surface, then ship the handlers — which the
spec itself documents as deliberate. Nothing in the naming makes the second plan traceable to its
spec: the date differs, and the stem differs.

Step 3 handles *zero* matches (correctly, as "no outcomes file exists") and *more than one* match
(correctly, as a Gaps entry). It has no case for **one match that is only half the story**, because
it cannot tell that case from a complete one.

### Proposed change

`plugin/skills/process-review/SKILL.md`, step 3. After the date-prefix fallback, add a third rule:

> Then, regardless of how many matched, search every `docs/superpowers/plans/*-outcomes.md` whose
> corresponding plan file names this spec in a commit trailer or in its own header, and include any
> that the two rules above did not reach. A spec that shipped in more than one plan — a surface plan
> and a handlers plan, say — has more than one outcomes file, and its later plans carry dates no
> spec shares. Name every file you read in the review's Specs Reviewed section, so a reader can see
> the coverage rather than assume it.

The commit-trailer form is already conventional in this project (`Part of
docs/superpowers/specs/...`), and `writing-plans` produces the header reference.

### Interactions and risks

- **Cost:** one extra grep per shipped spec. Negligible.
- **Risk of over-matching:** a plan that merely *cites* a spec without implementing it would be
  pulled in. Mitigated by requiring the reference to be a commit trailer or a header field rather
  than any mention.
- **Does not conflict with A3.** A3 proposes a fixture-coverage check in SDD's Finish; this is
  process-review's own input resolution.

### What would falsify it

A project where every spec maps to exactly one plan would never see this, and the added rule would
find nothing beyond what the first two already reached. If superfunk's own history has no
two-plan spec, the finding is real but the priority is low.

## A6 — `check_docs.py`'s heading regex does not match this project's spec format

**Fourth window in which this has been recorded here, and it has never been actionable from this
repo.**

### What happened

`plugin/skills/documentation/scripts/check_docs.py` locates a spec's sections by a regex expecting
`## Context`, `## Decision`, `## Consequences`. This project's design specs — written by
`brainstorming`, which produces numbered sections — use `## 1. Context`, `## 2. Decision`, and so on.

The script does not fail. It returns **`ACTION_NEEDED` with empty section bodies**, which reads
exactly like a spec that has no content in those sections. Every implementer that hits it must work
out that the empty body is the script's defect rather than the spec's, and draft the README/CHANGELOG
update by hand from the spec directly.

Hit again on `edit-module-slice-2` Task 4, where the implementer diagnosed it correctly by reading
the spec, drafted by hand, and then re-ran the script against the real commit range to confirm
`ALREADY_UPDATED`.

### The mechanism

The regex encodes one heading convention. `brainstorming` does not mandate an unnumbered form, and
nothing downstream validates that a spec's headings match what `check_docs.py` expects — so the two
skills in the same plugin disagree about the format, and the disagreement surfaces as an empty
result rather than as an error.

### Proposed change

In `check_docs.py`, make the section pattern tolerate an optional leading ordinal:

```python
SECTION = re.compile(r"^##\s+(?:\d+\.\s*)?(Context|Decision|Consequences)\b", re.M | re.I)
```

And — more important than the regex — **make an empty body loud**:

> If a spec matches a heading but the section body is empty, report `SPEC_UNREADABLE: <section>`
> rather than `ACTION_NEEDED`. An empty body is far more often a parse failure than a genuinely
> empty section, and the two are indistinguishable to the caller today.

### Interactions and risks

- **Low risk.** The optional-ordinal group cannot match less than the current pattern.
- **The second half matters more than the first.** Even with the regex fixed, a future heading
  convention will break it again; a distinguishable failure mode means the next person spends a
  minute rather than an hour.
- **Interacts with SDD's Finish and `writing-plans`' User-Facing Documentation Timing**, both of
  which call this script and both of which currently treat `ACTION_NEEDED` as authoritative.

### What would falsify it

If `brainstorming` were changed to mandate unnumbered headings, the regex half becomes unnecessary —
but the empty-body-is-silent half stands regardless, and is the part worth taking.

---

# Addendum — 2026-10-14, after `2026-10-13-arcade-module-design.md`

Written at the process review closing the window of three specs:
`2026-10-06-spatial-measure-slice`, `2026-10-07-spatial-proximity-slice`, and
`2026-10-13-arcade-module`. 136 logged entries — 113 Catch, 21 Miss, 1 Gap, 1 Friction.

**Four of the five items below have been open for two or three review windows and were never
written out here.** That is itself the finding in A11: the receiving project's reviews keep
deferring superfunk items with a note saying "not edited from this repo", and the note is where
they stop. A6 and A5 were written out on 2026-09-24; nothing since. Verified before writing this,
by grepping this file for `re-run instruction`, `controller-revised` and `reachability` — all
three returned zero.

**This file is UNTRACKED in superfunk's git (`??`).** A `git clean -fdx` destroys it and every
finding in it. That is worth fixing before anything below.

---

## A6 update — sixth sighting, and the mechanism is now pinned to a line

A6's body above says *"Fourth window in which this has been recorded here."* It is now the
**sixth**, and the two new ones are more specific than their predecessors.

**Fifth sighting, 2026-10-12, `spatial-proximity` Task 8.** `check_docs.py` printed
`ACTION_NEEDED` — correct, because that verdict comes from `git diff --name-only` — followed by
**three empty sections**. The implementer noticed the tool had half-worked and said so rather
than treating the empty bodies as a real answer.

**The mechanism, pinned.** `check_docs.py:16`:

```python
pattern = r'^## ' + re.escape(heading)
```

This cannot match a numbered heading. The receiving project's specs are written by
`brainstorming`, which produces `## 1. Context`, `## 2. Decision`, `## 5. Consequences`. A
minimal fix is one character class:

```python
pattern = r'^##\s+(?:\d+\.\s+)?' + re.escape(heading)
```

**Sixth sighting, 2026-10-13.** The item had been **deferred at the `arcade` branch's own
brainstorming gate five days before it fired again** — so the gate read the open Recommendation,
noted it, deferred it, and the tool then failed in exactly the recorded way during that same
branch.

**This supersedes the 2026-09-29 review's standing item "re-send A6 with the fifth sighting's
evidence."** The item is no longer a re-send; it is a one-line fix with the failing regex, the
replacement, and six dated sightings behind it.

---

## A7 — `writing-plans`' self-review item 10 has no reachability clause

**Third deferral. Open since 2026-09-29, re-raised 2026-10-05, re-raised again here.** The
longest-standing item in this file.

Item 10 asks the plan author to verify numeric expectations — that a stated count came from a
command actually run. It does not ask whether the thing being counted is **reachable**. The
receiving project has shipped criteria whose subject does not exist, which pass item 10 cleanly
because the count was real; what was missing was anything to count it against.

That project built the in-repo half itself:
`docs/patterns/verify-a-criterion-can-fail.md` now names four failure shapes, the fourth being
*"the subject does not exist"*. The superfunk half — one clause in item 10 asking whether a
plan's check can fail — has never been added.

**Evidence from this window.** `spatial-proximity` criterion 10's over-cap arm was
**unreachable against the fixture**, and both the plan and the dispatch asserted it as a check.
It shipped half passed and half recorded as having no reachable subject.

---

## A8 — `subagent-driven-development`'s fix loop has no temporal corollary

**Open since 2026-09-29, never written out here.**

The fix loop tells an implementer to re-derive a citation rather than compute it from a shift.
It does not say **when**. Re-deriving *after your own edits* measures a tree that no longer
matches the brief, and produces confident false positives.

**Measured twice in this window, in both directions.**

- `arcade` Task 9: an implementer reported the controller's line numbers as rotted. Measured at
  the task's own base commit they were exactly right; the implementer had grepped after
  inserting ten lines above them. Its own diagnosis: *"I re-derived against a tree I had already
  changed, which measures something other than the brief — the reverse of the error the
  re-derivation rule exists to prevent."*
- `arcade` Task 13 and the gate fix wave: the opposite failure. Comparing `base[addr]` against
  `head[addr]` marks every **correctly repaired** citation as stale.

The clause worth adding is one sentence: re-derive against the commit the brief was written
against, and state which commit you measured at.

---

## A9 — the reviewer re-run instruction is backwards for fast suites

**Open since 2026-10-05, never written out here.**

The review templates tell a reviewer not to re-run the suite, on the assumption that suites are
slow and the implementer's reported numbers can be taken. In the receiving project all three
suites together run in about 13 seconds, and reported numbers have been wrong often enough that
re-running is cheaper than adjudicating.

**This window's evidence.** Two reviewers separately refused to bank a reported number and
measured instead; one of them diverged from the implementer's mutation count 27-to-17, in both
directions, which established that the count was a property of the implementer's stub rather
than of the code. A third found a report claiming 17 call sites against its own listed 16.

Suggested shape: re-run the suite when it completes in under a minute; take the reported numbers
only when it does not, and say which you did.

---

## A10 — nothing names the controller-revised brief

**Open since 2026-10-05, never written out here.**

When a controller edits a brief after the review has produced it, the implementer receives a
document with no provenance: it cannot tell which lines came from the plan, which from the
review, and which the controller added. The cost is that an agent cannot calibrate how much to
trust a given sentence.

**This window turned that into the single highest-yield check in the process, by accident.**
`implementer reporting rather than repairing` accounts for **37 of 136 logged entries**, second
only to `task review` at 55. On the `arcade` branch, **five agents corrected the brief they were
handed and every one of them was right** — stale line numbers, a false "pre-existing" premise, a
mislocated blocker, a safety property with an unstated limit, and a claim the branch had retired
one commit earlier.

Every one of those was found because the brief carried a line telling the agent to verify
citations against the source rather than against the brief. **Naming the provenance of each
section would make that check cheaper and more targeted**, rather than leaving the agent to
re-verify everything uniformly.

---

## A11 — a mid-window Gap has no route to a mechanism, and this window paid for it

**New, and it is the receiving project's headline finding for this window.**

`notes.md` admits `Catch` and `Miss`. A Catch gets a fix round immediately; a Miss gets a
Recommendation at review time. **A `Gap` entry — a structural hole somebody noticed mid-branch —
has no consumer at all.** It waits for a review up to three specs away.

**What that cost.** On 2026-10-06, the **first day** of this window, an agent logged:

> *"IMPORTANT, project-wide and unacted. Line citations into `docs/` prose are checked by
> nothing."*

Eight days later the `arcade` whole-branch gate returned **NOT READY TO MERGE on twelve
blockers, every one a line citation into prose.** In between, the same class produced three
rotted citations on `spatial-measure` — one *inside* the finding written to correct it — sixteen
on the `spatial-proximity` fix wave, and seven consecutive instances on `arcade`, including a fix
round convened to repair the class and an edit to the lessons-learned entry *about* the class.

The diagnosis was correct, early, in writing, and by the right mechanism. Nothing read it.

**Suggested shape**, two halves:

1. A `Gap` entry carries a disposition — either the mechanism it wants, or
   `(no mechanism proposed)`.
2. `subagent-driven-development`'s Finish section reads the window's `Gap` entries and either
   files one bug per actionable Gap or records why not. Finish already walks `notes.md`; this is
   one more pass over entries it is reading anyway.

**Also worth fixing while in that file:** `notes.md`'s documented field-2 vocabulary is
`Catch|Miss`, and two entries in this window used `Gap` and `Friction`. Both entries are useful
and neither is wrong to exist — but no count of the file can see them, which is how the Gap above
went unread for eight days.

---

## Two mechanisms from this window that superfunk may want, offered rather than filed

Neither is a defect in superfunk; both are techniques the receiving project measured and that
generalize.

**A sweep reports its corpus size beside its hit count.** A sweep that normalizes `*`, `_` and
backticks out of its corpus before matching turns `desktop_pass.py` into `desktoppass.py` and
silently drops every citation to it — a sweep that runs, reports zero, and has examined nothing.
The reviewer's examined-site count went **702 → 1062** once the index was made
underscore-insensitive, and two independent sweeps hit the same false zero first. The rule:
**strip markup for a phrase sweep; never strip `_`, `.` or `/` for an identifier or `file:NN`
sweep.**

**When a change reverses a behaviour, sweep the whole tree for the retired claim rather than the
diff for new ones.** The `arcade` gate swept all 9,684 **added** lines for sentences the branch
had falsified and reported none live in shipped code. Two existed, both in `.cs`. It could not
see them **by construction**: they were pre-existing sentences the change had falsified, so they
were never in the diff.
