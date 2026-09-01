Self-review complete. I ran the loaded skill's seven checks (that variant's step 2 includes the rule-membership sub-check, a superset of the repo copy's step 2).

## What verified clean

Every numeric and citation claim in Context and Decision holds:

| Claim | Result |
|---|---|
| "zero of 43 shipped specs" contain `## Alternatives Considered` | exactly 43 `Status: Shipped` specs, 0 with the heading |
| "the forty-fourth consecutive spec" | 44 spec files total |
| "19 plugin skills, 5 user-level… all 24 skill files" | 19 + 5 = 24 |
| `brainstorming/SKILL.md:27` and `:139` quoted text | verbatim match |
| `branching-research` names `adhd-research` "on six lines" | lines 10, 12, 17, 39, 77, 90 |
| `multi-lens-research:29` names `general-purpose` | confirmed |
| both JSON files read `6.2.0` | confirmed |
| `writing-plans:270-278`, process-review "real evidence over vibes", principles.md "Mechanisms, Not Goodwill" | all confirmed |
| install state (`superpowers@claude-plugins-official` enabled; `"repositories": {}`) | confirmed |
| "confirmed failure mode from `adhd-research` testing" | exists verbatim at line 90 |
| null-option / flip-factor keyword probe returns zero | re-ran with 8 phrasings — zero for all; "baseline" hits 6 files in unrelated senses |

Placeholder scan and scope check: clean. No TBD/TODO; the work fits one plan.

## Eight findings

**1. Decision §5 adds a table row to a bulleted list.** `calibrating-recommendations`' `## Common Mistakes` section is a bulleted list (`- **Dropping required fields…**`), not a table. The section that *is* a table is `## Edge Cases`. The spec supplies `| **Restating the pre-mortem…** | … |`. Criterion 6 requires that row "worded as Decision section 5 states" — so a literal implementation lands a header-less table row inside a bullet list, and the criterion passes on a malformed file.

**2. Criterion 3 contradicts Decision §2.** The criterion demands every backtick-quoted skill name in the three adopted files resolve to a `plugin/skills/` directory, "checked by script." The actual set is `adhd-research`, `calibrating-recommendations`, `dispatching-parallel-agents`, `general-purpose`, `multi-lens-research`. `general-purpose` is an agent type that Decision §2 explicitly exempts — but Criterion 3 carries no carve-out, so the script fails on a *correct* implementation. (`dispatching-parallel-agents` does resolve; §2's "no other reference fails to resolve" claim is true.)

**3. Rule-membership hole in Decision §4.** The new bullet enumerates three branches keyed on which producer ran: fan-out (`multi-lens-research`/`branching-research`) → full comparison; "only step 4's inline proposal ran" → short form; no choice → skip. But §1 of this same spec deliberately keeps `adhd-research` at user level — a fourth producer of an option comparison. A decision researched with it matches neither the first branch (names only two skills) nor the second (inline didn't run). Key the first branch on "a research skill ran" rather than naming two.

**4. Criterion 9 is under-specified and falsifies on one sample.** It never names the brainstorming prompt, so no other implementer can reproduce it; and it says a single current-wording run producing both artifacts "falsifies the change, which then does not ship." The change raises a floor, not a ceiling — one lucky stochastic run shouldn't kill it. Live counter-evidence: this session loaded brainstorming from `C:\sf-bcv-plugins\arm1\skills\brainstorming`, a variant whose step 4 already carries the confidence/evidence clause but neither the do-nothing candidate nor the flip factor. The "current wording" arm isn't a stable target across installs.

**5. `Status: Draft` is outside the mandated vocabulary.** The skill allows `Proposed`, `Approved`, or `Superseded by <filename>`, and bans free-text. Should read `Proposed`.

**6. The `:91-94` prose edit has no replacement text.** Every other edit in the spec supplies exact before/after. This one says only "update… to carry the same three requirements," and Criterion 4 correspondingly weakens to "carries," while demanding exact match for `:27`. Also `:94` is the YAGNI bullet — the restatement is `:91-93`.

**7. The keyword probe isn't reproducible.** Context asserts "a keyword probe… returns zero matches for either" without recording the terms. The claim holds (I confirmed it), but as written nobody can re-run it.

**8. The LeCunSkills provenance is unverified.** "Nine skills," "six of the nine duplicate existing coverage" — external, no fetch made. Nothing in Decision or Criteria depends on it, so this is a provenance note rather than a defect.

Findings 1–4 change what ships; 5–6 are mechanical; 7–8 are notes. The spec is committed, and fixes 3 and 4 are judgment calls on wording rather than mechanical edits — want me to apply all eight, or just 1, 2, 5, and 6 and leave the rewordings to you?
