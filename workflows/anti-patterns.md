# Anti-Pattern Checklist

This checklist grows over time. Check every candidate workflow against it during the Brainstorm stage. When development reveals a new anti-pattern, append it here — the checklist applies to every future workflow brainstorm, not just the one that surfaced the new entry.

Source: `docs/superpowers/specs/2026-08-05-workflow-validation-process-design.md`

## Checklist

- Does this add a phase gate that doesn't earn its ceremony?
- Does this require a dedicated SME or agent, when a checklist or a single prompt could serve the same purpose?
- Does this let the live, currently-active instructions and an in-development next version share the same files or location? A session that does dev work can edit the very instructions guiding it, which leaks in-progress changes into the shipped version. Casita hit this during its v2 rewrite: sessions edited the main instructions and skills directly in the project directory, and that forced unreleased v2 changes into v1.
