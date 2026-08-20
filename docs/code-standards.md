# Code Standards

Coding and documentation standards for superfunk. Contributors and Claude both follow these conventions.

**Legend:** `[Rule]` = must follow | `[Preference]` = should follow

---

## File Naming

- `[Rule]` All markdown and documentation files use kebab-case: `ai-code-guidelines.md`, `code-standards.md`, `2026-08-13-roadmap-multifile-split-automation-design.md`
- `[Rule]` Feature directories use the `YYYY-MM-DD-<slug>` convention, not a sequential number — matches the date-slug ID scheme already decided for feature-tracking, since it doubles as a real timeline without needing a counter to stay in sync
- `[Preference]` Keep names short and descriptive — prefer `split_roadmap.py` over `split_the_module_roadmap_into_files.py`
- `[Preference]` Doc files in `docs/` and `docs/superpowers/specs/` use descriptive names matching their content topic, prefixed with the date for dated artifacts (specs, plans)

---

## Markdown Conventions

### Headings

- `[Rule]` H1 (`#`) for the document's title only — one per file
- `[Rule]` H2 (`##`) for major sections
- `[Rule]` H3 (`###`) for subsections within a major section
- `[Rule]` Never skip heading levels (no H1 → H3 without an H2 in between)

### Formatting

- `[Rule]` Use `---` horizontal rules to separate major sections
- `[Rule]` Use `**bold**` for labels, key terms, and emphasis within lists
- `[Rule]` Use backtick code spans for file paths, command names, and inline code: `` `CLAUDE.md` ``, `` `.superfunk/rebuild_index.py` ``
- `[Preference]` Use tables for structured comparisons
- `[Preference]` Use code blocks with language identifiers for all multi-line code samples
- `[Preference]` Use bullet lists for unordered items; numbered lists only when sequence matters

### Links

- `[Rule]` Use relative paths for internal links
- `[Preference]` Link to a referenced file on its first mention within a document

---

## Git Conventions

- `[Rule]` Conventional commits: `type(scope): description`
- `[Rule]` Types: `feat`, `fix`, `docs`, `refactor`, `chore`
- `[Rule]` Scope identifies the affected area: `feature-tracking`, `skills`, `docs`, `plugin`
- `[Rule]` Description in lowercase, imperative mood, no trailing period
- `[Rule]` Example: `feat(feature-tracking): add dependency tracking to spec.md`
- `[Preference]` Keep commits focused — one logical change per commit
- `[Rule]` Never commit build artifacts, secrets, or generated files — `.superfunk/tracking.db` and `.superfunk/__pycache__/` are real, already-gitignored examples of exactly this

---

## Spec File Conventions

- `[Rule]` Every design spec in `docs/superpowers/specs/` must be self-contained — readable without external context beyond `CLAUDE.md`
- `[Rule]` Acceptance criteria must be testable: observable and binary for a full Workflow-Validated spec's Falsifiable Criteria, or verified against disposable scratch trials with quoted evidence for a lighter-path addition's Testing section — this project's two real validation tracks, not a single fixed format
- `[Rule]` Use the standard templates in `specs/_template/` — do not invent new formats
- `[Preference]` `spec.md`'s `Status:` line stays current: `Planned` → `In Progress` → `Done` (or `Deferred`/`Dropped`)

---

## Lessons vs. Patterns

Two related but distinct artifacts capture what the project learns from real work.

- `[Rule]` A Lesson answers *what happened and what to watch out for* — one retrospective fact, tied to the plan that surfaced it. Lives in `docs/lessons-learned.md`.
- `[Rule]` A Pattern answers *what future work should do* — a prospective, reusable rule that applies across many future situations. Lives in `docs/patterns/` as its own file.
- `[Preference]` Secondary test when the distinction feels unclear: one specific fact tied to one context makes a Lesson; a rule that applies broadly makes a Pattern.
- `[Rule]` A Lesson gets captured at `subagent-driven-development`'s Finish step; "nothing notable" counts as a complete answer.
- `[Rule]` A Lesson promotes to a Pattern when it expresses a prospective rule that applies across many future situations, or when the same failure mode recurs a second time — whichever comes first.

---

## Checklist Construction

- `[Rule]` Choose READ-DO (a fixed sequence, run in order) or DO-CONFIRM (do the work, then pause and confirm nothing got missed) deliberately, per checklist.
- `[Rule]` A checklist item exists to catch a step people easily skip. An item that restates the obvious earns no place on the list.
- `[Rule]` Cap a single checklist at 5-9 items. Past that, split into grouped sub-checklists by phase or component, each with its own pause point.
- `[Rule]` A DO-CONFIRM checklist checks `docs/lessons-learned.md` for entries relevant to its own domain, once per run, not once per sub-checklist.

---

## CLAUDE.md Maintenance

`CLAUDE.md` is a living document — it drifts from reality unless actively maintained.

### When to Update

- `[Rule]` Update `CLAUDE.md` when `workflows/`, `docs/superpowers/specs/`, or the feature-tracking process changes in ways that affect how Claude should behave session-to-session
- `[Preference]` Update when an architectural decision changes how Claude should approach the project
- `[Preference]` Update when Claude repeatedly does something `CLAUDE.md` says not to — the instruction may be buried or unclear, and the section should get restructured or pruned

### Pruning Test

- `[Preference]` For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it. Apply this test whenever the file approaches 150 lines.

### Length Limit

- `[Rule]` Target under 150 lines. `CLAUDE.md` sits at 20 lines today — this is forward-looking discipline, not an active cleanup. If it exceeds 150 lines, look for one section to trim or delegate to a referenced doc. If it still exceeds 200 lines after that pass, delegate a full section to a referenced doc and replace it with a summary and a link.

### Maintenance Comment

- `[Preference]` A substantially revised `CLAUDE.md` carries an HTML comment maintenance note at the top, naming the date and what should trigger the next update:

```markdown
<!-- CLAUDE.md — last updated: YYYY-MM-DD -->
<!-- Update when: workflows change · specs/plans conventions change · an architectural decision is made · Claude keeps violating a rule -->
```

---

## Cross-File Field Dependencies

When a field written by one script or template gets read by another via exact string match, both ends must agree on the same bare-word format.

- `[Rule]` A template field consumed by an exact-string read must be written as a bare word — not bracket-hint syntax (`[true — or: false]`). A bracket hint risks Claude writing the literal bracket text, which won't match the read.
- `[Rule]` When writing such a field, note nearby the exact string the downstream reader expects, so the dependency stays visible to whoever edits either side later.

This isn't hypothetical here: `spec.md`'s `**Status:**`, `**Bundle:**`, and `**Dependencies:**` fields get parsed by `.superfunk/rebuild_index.py`'s `FIELD_RE` via exact regex match. A bracket-hint placeholder like `**Status:** [Planned or Done]` would corrupt every downstream query built on that field.

---

## Edit Tool Guidelines

- `[Rule]` Do not use `replace_all: true` with patterns shorter than ~6 characters, or with patterns that could appear as substrings of longer identifiers. A targeted edit with enough surrounding context to make the match unique is safer.
- `[Preference]` When renaming a symbol across many files, prefer a targeted multi-file search (grep for every call site, then edit each) over `replace_all` — the extra step catches false positives before they land in a commit.
