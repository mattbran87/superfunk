# Trial harness — external bookmark-CLI trial

The reproduction rig for `../external-trial-bookmark-cli-findings.md`. Preserved here because
it originally lived in a session-scoped temp directory that does not survive.

## Files

| File | Purpose |
|---|---|
| `run-turn.ps1` | Drives one partner turn against the child session |
| `extract_turn.py` | Dumps every assistant text block for a turn (see the caveat below) |
| `trial-settings.json` | Disables competing plugins so the fork can be measured cleanly |

## The caveat that matters most

**`claude -p` prints ONLY the final assistant message of a turn.** Intermediate assistant
messages are written to the session transcript but never to stdout.

Two findings in the original trial were logged against the framework and then had to be
withdrawn or downgraded once the transcript was read directly. One was *entirely* an artifact
of this truncation. `run-turn.ps1` calls `extract_turn.py` after every turn and writes
`<out>.all.txt` containing all assistant blocks — **judge behavior from `.all.txt`, never from
the `-p` output alone.**

## Why `trial-settings.json` exists

The machine has `superpowers@claude-plugins-official` (the upstream marketplace framework)
enabled globally. Loaded alongside the fork, it shadows/competes under a different prefix and
no finding can be attributed cleanly. The settings file disables it plus context-mode,
chrome-devtools, frontend-design, and github.

Verify isolation before trusting a run: the child session should expose exactly the fork's
skills, all `superfunk:`-prefixed, with no `superpowers:` namespace present.

## Re-running

```powershell
# First turn of a NEW trial — generate a fresh UUID and pass -First
.\run-turn.ps1 -PromptFile p01.txt -OutFile o01.txt -First -SessionId <new-uuid>

# Every subsequent turn — omit -First; the script uses --resume
.\run-turn.ps1 -PromptFile p02.txt -OutFile o02.txt -SessionId <same-uuid>
```

`run-turn.ps1` has the original trial's session id as its `-SessionId` default and hardcodes
the plugin path and the working directory (`C:\sf-bookmark-cli-trial`). Change those before
pointing it at anything else.

Turns run long — cycle 2's execution turn took 103 minutes. Run them in the background rather
than blocking on them, and expect account rate limits on a trial of this length (the original
hit both a session limit and a weekly limit during cycle 3).

## What is NOT preserved here, and why

The 26 prompt/output pairs (`p01–p26.txt` / `o01–o26.txt`) were not copied — they are all
recoverable from the durable session transcript at:

```
~/.claude/projects/C--sf-bookmark-cli-trial/659f8ca6-433f-4f5e-b723-c07e3b724c9f.jsonl
```

Point `extract_turn.py` at that file to reconstruct any turn, including the intermediate
messages `-p` never printed.
