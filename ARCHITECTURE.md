# Architecture

## Current runtime

```text
Browser
  |
  | index.html (UI + application state + engineering logic)
  |
  +---- localStorage (projects/catalog/current persisted data)
  |
  +---- eplan_catalog.js (local browser catalogue)
  |
  +---- HTTP /api/* when backend is running
             |
             v
         backend.py
             |
             +---- eplan_catalog.json
             +---- catalog_seed.json
             +---- manufacturer/web documentation lookup
```

## Project aggregate
A project currently contains roughly:

```text
Project
├── id / code / name / client / notes
├── elements[]
├── circuits[]
├── safetyFunctions[]
└── settings
```

All four design blocks use the shared `elements[]` collection and distinguish ownership with `element.block`:
- `power`
- `control`
- `safety`
- `plc`

This shared model is intentional because an engineering component can affect multiple calculations (I/O, DC consumption, safety, power, cable, etc.).

## Functional safety Phase 1 extension
Phase 1 preserves `elements[]` and extends the project aggregate with:

```text
Project
├── elements[]
├── circuits[]
├── safetyFunctions[]
└── settings
```

A safety function references existing elements rather than duplicating them.
Projects persisted before Phase 1 are normalized on load with an empty `safetyFunctions[]` collection while preserving their elements, circuits and settings.

```text
SafetyFunction
├── id
├── code
├── name
├── description
├── requiredPL (PLr)
├── source / import metadata
├── stages
│   ├── input[]  -> links to project elements and/or proposed components
│   ├── logic[]  -> safety relay or safety PLC path
│   └── output[] -> links to project elements and/or proposed components
├── preferences
├── calculation
└── validationStatus
```

## EPLAN catalogue boundary
EPLAN catalogue data is not the engineering truth by itself. It is used for:
- article identity,
- availability in the company catalogue,
- manufacturer/reference matching,
- known metadata that can be safely normalized.

Critical engineering values should be sourced from verified manufacturer documentation or validated library data.

## SISTEMA boundary
SISTEMA/IFA integration should be isolated behind a dedicated import/normalization layer. The rest of the application should consume a normalized safety-component model and should not depend directly on a vendor/library file structure.

Safety libraries are persisted in the application-level repository (`safetyLibraries[]`), outside individual projects, so the same imported source can be reused. The current infrastructure detects supported containers and records provenance. It does not interpret Firebird `.slb` schemas or calculate safety performance.

Target flow:

```text
SISTEMA/IFA library file
        ↓
Importer / parser
        ↓
Normalized safety library model
        ↓
Safety component repository
        ↓
Safety-function design engine
```

A later export layer may transform the normalized project safety model into a verified SISTEMA-compatible project file, but only after the real format is proven with round-trip tests in the official application.
