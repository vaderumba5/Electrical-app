# AGENTS.md — App Eléctrica

## Purpose
This repository is the current working baseline of **App Eléctrica**, an engineering-assistance application for industrial electrical design.

The current runtime baseline is **v0.7**. Do not discard or rewrite existing working behavior unless the active task explicitly requires it.

## Read before changing code
Read, in this order:
1. `README.md`
2. `ARCHITECTURE.md`
3. `docs/02-current-state-v0.7.md`
4. `docs/03-domain-model.md`
5. `docs/04-electrical-engine.md`
6. `docs/functional-safety/01-overview.md`
7. `docs/roadmap/current-phase.md`

## Non-negotiable engineering rules
- Electrical protections must be derived from real receiver/load data. Never hard-code a protection solely because of a generic equipment type.
- Manufacturer documentation has priority over generic assumptions and catalogue metadata.
- The EPLAN catalogue is primarily inventory/identity evidence. A catalogue match is not automatically a technically approved selection.
- Keep calculation logic separate from commercial-article selection.
- Do not treat the output current rating of a DC power supply as its AC input current.
- Do not approve general protection when critical inputs such as `Iz`, `Ik`, or required receiver input-current data are missing.
- Preserve one physical branch per physical receiver unless an explicitly supported manufacturer rule allows grouping and the architecture decision is visible to the user.
- Safety functions belong to the same electrical project and must be able to link to existing project components.
- Never invent SISTEMA/IFA reliability data, PL values, PFHd, MTTFd, DCavg, CCF, B10d, category, mission time, or manufacturer safety parameters.
- Imported SISTEMA library data must retain traceability to its original source/library/item.
- Do not claim official SISTEMA compatibility or report equivalence until the export format has been verified with real SISTEMA files and opened successfully in the official application.

## Current architecture constraints
- Frontend is currently a single `index.html` with inline CSS/JavaScript.
- Backend is `backend.py` using Python's `ThreadingHTTPServer`.
- Project persistence is currently browser `localStorage`.
- EPLAN normalized catalogue is in `eplan_catalog.json` / `eplan_catalog.js`.
- `catalog_seed.json` contains verified/curated starter technical data.
- Windows local launch flow (`start_windows.bat`) must keep working.

Do **not** perform a broad framework migration or split the monolith merely for style reasons. Refactoring should be incremental, test-backed, and tied to a concrete feature need.

## Data migration rule
Any change to the persisted project schema must include a backward-compatible migration path for existing v0.7 `localStorage` data. Existing projects must not silently lose elements, circuits, settings, or catalogue data.

## Safety development rule
The first safety phase is a domain/model and traceability phase, not a guessed PL calculator. First establish:
- `safetyFunctions` at project level,
- PLr required,
- input / logic / output stages,
- links to existing `elements`,
- manufacturer/preferences,
- provenance and validation status.

Only calculate PL when the required parameters and calculation method are grounded in verified sources.

## Tests
For every engineering change:
- add deterministic tests where practical,
- test missing/unknown data explicitly,
- test invalid combinations,
- preserve existing S210 behavior,
- preserve the distinction between DC output capacity and AC input current.

Before completing a task, at minimum run:
- `python -m py_compile backend.py`
- a JavaScript syntax check for the inline script in `index.html`
- any new tests added for the task.

## Change discipline
- Prefer the smallest coherent change that advances `docs/roadmap/current-phase.md`.
- Do not implement future roadmap phases opportunistically.
- Update documentation when the domain model or behavior changes.
- If a required technical fact is unknown, represent it as pending/unknown instead of guessing.
