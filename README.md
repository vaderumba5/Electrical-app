# App Eléctrica — baseline v0.7

This repository is the current application baseline plus the project documentation required for continuing development with Codex.

## What already works
- Multi-project UI.
- Four project blocks: Potencia, Control, Seguridad, PLC.
- Shared project element model.
- EPLAN XML-derived catalogue with **6,133 normalized usable articles**.
- Curated/verified seed catalogue entries.
- Power engineering workflow based on real receivers.
- Receiver/manual/circuit/general-protection/RCD/article-selection flow.
- Specific verified rules for Siemens SINAMICS S210 references currently encoded in the baseline.
- Separation between DC supply output capacity and AC input current.
- Preliminary 24 VDC load aggregation from project consumers.
- Python backend for technical enrichment and manufacturer/reference lookup.
- XLSX import/export compatibility from the existing frontend flow.
- Windows launch scripts and local/offline mode.

The original v0.7 notes remain in `README.txt` and `TESTS.txt` and are part of the baseline evidence.

## Main files
- `index.html` — current frontend/application logic.
- `backend.py` — local Python backend and API endpoints.
- `eplan_catalog.json` — normalized EPLAN article data.
- `eplan_catalog.js` — browser-ready copy of the catalogue.
- `catalog_seed.json` — curated starter technical data.
- `requirements.txt` — Python dependencies.
- `start_windows.bat` — recommended Windows startup.

## Continue development
Codex should start by reading `AGENTS.md` and `docs/roadmap/current-phase.md`.

The next development objective is **Functional Safety Phase 1**: add project-level safety functions linked to existing project components, with PLr and Input/Logic/Output structure, while preparing for later SISTEMA/IFA library import.
