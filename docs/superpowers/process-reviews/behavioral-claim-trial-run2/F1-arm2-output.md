Self-review complete. I ran all seven steps against the real files rather than from recall. **Six findings need a fix; one is a no-action note.**

---

## 1. The spec edits a copy that has already diverged from the one this session loaded — blocking

The Skill tool loaded `brainstorming` from `C:\sf-bcv-plugins\arm2\skills\brainstorming\SKILL.md`, not from `plugin/skills/`. The two differ on five hunks, including **exactly the two lines the spec plans to rewrite**:

| | repo `plugin/skills/` (what the spec quotes) | `arm2` (what loaded) |
|---|---|---|
| step 4 (`:27`) | `— with trade-offs and your recommendation` | already adds confidence + project-specific evidence + "dispatch `multi-lens-research` or `branching-research` instead of proposing inline" |
| Alternatives bullet | `:139`, fan-out only | `:148`, already ~90% of the spec's Decision-4 replacement (missing only the do-nothing option and flip factor) |
| self-review item 6 | "Numeric-claim verification" | already broadened to "Claim verification," covering behavioral claims |

Consequence: applying Decision 3 verbatim to the repo file **drops** the confidence/evidence sentence arm2 already has, and Falsifiable Criterion 4 ("matches … exactly") would lock that regression in. Decision 4 re-implements work already done elsewhere.

This is `docs/patterns/resolve-skill-files-via-skill-tool-not-glob.md` one level up: the spec's premise "step 4 names no mechanism" is true of the repo copy and false of the copy that actually runs. **Needs your call on which tree is authoritative** — I can't decide that. Once decided, Decisions 3 and 4 should be rewritten as *additions* to the arm2 wording, not replacements of the older repo wording.

## 2. Two load-bearing behavioral claims rest on keyword greps

Context:34-45 claims a keyword probe "returns zero matches for either." I re-ran both probes across all 24 skill files plus `docs/principles.md` and `docs/ai-code-guidelines.md` — **both genuinely return zero**. The text claim holds.

But the claims as *stated* are behavioral: "No skill asks what happens if the project ships nothing" / "No skill asks which factor, if it moved, would reorder the candidates." The self-review's own item 6 (arm2 version) says: *"A grep over source text observes text, and an absent instruction does not establish an absent behavior."* No Catch record, control arm, or logged outcome is named. Criterion 9 supplies a control arm for the step-4 change only — nothing establishes a baseline for Decisions 5 or 6.

Fix: restate both as text claims ("no skill file contains an instruction to…"), or name the observation.

## 3. Falsifiable Criterion 3 names a mechanism it doesn't supply

"checked by script rather than by reading" — no script is named, located, or specified. Asserted, not supplied; the shape `docs/principles.md:35` (Mechanisms, Not Goodwill) calls out. Fix: inline the actual command.

## 4. Criterion 2 permits the repair Decision 2 forbids

Decision 2 says reword the three provenance lines (39, 77, 90) to keep the evidence. Criterion 2 only checks that `adhd-research` returns zero matches under `plugin/skills/` — **deleting those three lines passes it**, which is precisely the outcome Decision 2 rejects ("Deleting these lines discards evidence"). Fix: add a criterion that the three provenance clauses survive in reworded form.

## 5. `Status: Draft` sits outside the skill's own vocabulary

Line 4 reads `**Status:** Draft`. The skill mandates `Proposed`, `Approved`, or `Superseded by <filename>`. Across all 44 specs, 40 read `Shipped`, 3 read `Shipped (validated via …)`, and this is the only `Draft`. Textbook `docs/patterns/self-review-checks-own-required-template.md`. Fix: `Proposed`.

## 6. The spec exempts itself from the rule it writes

Decision 4 requires an `Alternatives Considered` section in *every spec that records a choice between approaches*. This spec records at least four: three skills vs. two; copy vs. move; reword vs. delete the provenance lines; step-3 vs. per-lens placement of the null option. Context:55-60 notes the skip under the *current* `:139` rule — but under the rule this spec itself writes, it wouldn't qualify for the skip. It would ship as the last artifact its own rule exempts. Fix: add the short-form section, or state explicitly that the new rule binds specs written after it ships.

## 7. "43 shipped specs" — accurate, flagging only for readers who count

`ls docs/superpowers/specs/*.md | wc -l` now returns **44** (this spec included), and `grep -rl "^## Alternatives Considered"` returns **0**. The claim is correct as written — 43 prior + this one = "the forty-fourth consecutive spec" — and consistent with the Consequences line. No change needed.

---

**Verified clean (steps 1, 3, 7 and the rest of 6):** `:27` and `:139` quoted verbatim against the repo copy; `adhd-research` on exactly lines 10, 12, 17, 39, 77, 90 of `branching-research`, splitting as the spec groups them; `multi-lens-research:29` names `general-purpose` (an agent type, correctly excluded); multi-lens step 3 is "Synthesize"; `calibrating-recommendations` has `**What would lower it:**` at `:48` and a Common Mistakes table at `:76`; both `plugin.json` and `marketplace.json` read `6.2.0`; 19 plugin + 5 user skills = 24, matching; `writing-plans:270-278` is item 14 "Stale-workaround grep," matching the spec's characterization; `process-review:13` "real evidence over vibes" and `docs/principles.md:35` "Mechanisms, Not Goodwill" both quoted correctly. No placeholders. Scope fits one plan.

Findings 2–6 I can fix inline now. Finding 1 needs you to say which tree is authoritative first — that answer changes what Decisions 3 and 4 should say.
