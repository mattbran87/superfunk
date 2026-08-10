# Diagram — Feature Tracking

**Date:** 2026-08-10
**Stage:** 1 — Diagram

## Flow / State Diagram

```mermaid
flowchart TD
    subgraph Intake["Add a feature"]
        A1[Pick the module] --> A2{Module exists?}
        A2 -->|No| A3[Create specs/module/ + roadmap.md]
        A2 -->|Yes| A4[Pick the Bundle]
        A3 --> A4
        A4 --> A5{Bundle heading exists?}
        A5 -->|No| A6[Add ## Bundle heading]
        A5 -->|Yes| A7[Scaffold feature dir from template]
        A6 --> A7
        A7 --> A8[Set spec.md Status to Planned]
        A8 --> A9[Link feature under Bundle in roadmap.md]
    end

    subgraph Update["Update status"]
        B1[Edit spec.md Status line]
    end

    A9 --> D1
    B1 --> D1

    subgraph Query["Answer: is it complete?"]
        D1[Run the rebuild command] --> D2([Query .superfunk/tracking.db])
    end
```

## Notes

This diagram assumes rebuilding the index stays cheap enough to run before every query, avoiding any staleness-detection logic entirely. Criteria and Trials should confirm this holds at a realistic feature count.

Feature Intake assumes a feature belongs to exactly one module. Cross-cutting features spanning multiple modules have no defined home yet — an open risk one of the four lenses (Robustness) already flagged.

"Pick the module" assumes the target codebase already organizes into clear modules. A project without that structure yet, including `superfunk` itself today, has no defined fallback in this diagram.
