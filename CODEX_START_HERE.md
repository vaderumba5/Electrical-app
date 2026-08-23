# First task for Codex

Read `AGENTS.md`, `README.md`, `ARCHITECTURE.md`, `docs/02-current-state-v0.7.md`, `docs/03-domain-model.md`, and `docs/roadmap/current-phase.md` before editing anything.

This repository is the real v0.7 baseline of App Eléctrica. Preserve all existing behavior.

## Task
Implement **only** the first implementation slice described in `docs/roadmap/current-phase.md`.

Before coding:
1. inspect the current state/persistence/rendering functions in `index.html`,
2. identify the smallest backward-compatible schema change,
3. identify how the existing generic Seguridad renderer can be extended without duplicating project elements.

Then implement the slice, add deterministic verification/tests, and update the documentation only where behavior actually changes.

Do not implement SISTEMA parsing, PL formulas, automatic component selection or SISTEMA export in this task.

At completion, report:
- files changed,
- migration behavior,
- tests/checks run,
- any unresolved risks or data needed for the next phase.
