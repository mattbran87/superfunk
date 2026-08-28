# Outcomes — 2026-08-28-superfunk-rebrand.md

One entry per completed task: what shipped, what diverged from the
plan, what to follow up on — in the implementer's own words, captured
before Finish deletes the plan's workspace (and its full report files).

<!-- entries below this line -->
## Task 1: Rebrand Claude Code manifest and dev marketplace
Shipped as planned; exact field values matched the plan's before/after blocks. `plugin/.claude-plugin/plugin.json`'s name/author/homepage/repository changed to superfunk/Matthew Brandenburg/matt.bran87@gmail.com/mattbran87 repo URLs. `marketplace.json`'s top-level `name` (superpowers-dev → superfunk-dev), `owner`, and nested `plugins[0].name`/`author` changed the same way; the marketplace's own `description` text stayed untouched as specified. Both files validated as parseable JSON before commit. Implemented directly (subagent spawn limit still exhausted; user chose "Continue direct execution" when asked). No divergence.

## Task 2: Rebrand Pi and Gemini CLI manifests
Shipped as planned; only the `name` field changed in each file (superpowers → superfunk). `package.json`'s `description`, `main`, and `pi.extensions` file-path references stayed untouched, as specified — no on-disk file rename occurred. Both files validated as parseable JSON before commit. Implemented directly. No divergence.

## Task 3: Rebrand Cursor, Codex, and Kimi Code manifests
Shipped as planned across all three files; name/displayName/author/homepage/repository/interface.developerName/interface.websiteURL changed to the Superfunk identity everywhere specified. `interface.longDescription`'s "Use Superpowers to guide..." prose, `composerIcon`'s asset path, and Kimi's `sessionStart.skill`/`skillInstructions` all stayed untouched as specified. All three files validated as parseable JSON before commit. Implemented directly. No divergence.

## Task 4: Rewrite superpowers: prefix to superfunk: in live content
Shipped as planned; the bulk sed pass across all 12 files completed cleanly, and both verification greps came back clean. One divergence from the plan itself (not the implementation): Step 1 and Step 4 predicted "33" for `grep -rn | wc -l` and the `grep -rc | awk` sum, but both commands count matching *lines*, not raw pattern occurrences — `writing-plans/SKILL.md:110` carries two `superpowers:` references on one line, so 33 total occurrences land on 32 matching lines. Caught by running the actual command before editing, not by trusting the plan's predicted count; the plan was corrected in place (33 → 32, with an explanatory note) before the sed pass ran. The sed pass itself, using `/g`, still rewrote all 33 occurrences correctly regardless of the line-counting distinction. Historical files (RELEASE-NOTES.md, plugin/docs/**) confirmed untouched via `git diff --stat`.
