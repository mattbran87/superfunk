# Diagram — Superpowers Fork

**Date:** 2026-08-08
**Stage:** 1 — Diagram

## Flow / State Diagram

```mermaid
flowchart TD
    Setup1[One-time: fork obra/superpowers on GitHub] --> Setup2[One-time: git subtree add fork into superfunk]
    Setup2 --> Edit[Edit a skill file in superfunk repo]
    Edit --> Gate{Session running on\nsuperfunk's own in-repo skills?}
    Gate -->|Yes - forbidden| Blocked[[Blocked: always develop using\nthe globally-installed superpowers plugin]]
    Gate -->|No - correct| ReadyCheck{Ready to validate this change?}
    ReadyCheck -->|Not yet| Edit
    ReadyCheck -->|Yes| NewProj[Create a disposable local test project]
    NewProj --> Install[Install the in-progress build there]
    Install --> Trial[Run a trial session in the test project]
    Trial --> Outcome{Trial meets expectations?}
    Outcome -->|No| Edit
    Outcome -->|Yes| Commit[Commit the change in superfunk]
    Commit --> MoreWork{More skills to rework?}
    MoreWork -->|Yes| Edit
    MoreWork -->|No| SyncCheck{Pull upstream updates from the fork?}
    SyncCheck -->|Yes| Pull[git subtree pull]
    Pull --> ConflictCheck{Merge conflicts?}
    ConflictCheck -->|Yes| Edit
    ConflictCheck -->|No| End([Session complete])
    SyncCheck -->|No| End
```

## Notes

This diagram assumes Claude Code supports installing a plugin from a local path — the Trials stage needs to confirm this. "Disposable local test project" means a throwaway directory outside version control, not a location `superfunk` tracks.

The forbidden path — a `superfunk` session running on its own in-repo skills — has no automated guard yet. It stays a discipline rule for now. A later workflow can design an automated guard if the trials show discipline alone doesn't hold, echoing what happened to Casita's sync rule.

This diagram doesn't yet specify where forked skill files live inside `superfunk` relative to existing `docs/` and `workflows/` content. That directory-layout decision belongs to a later stage or a follow-up workflow.
