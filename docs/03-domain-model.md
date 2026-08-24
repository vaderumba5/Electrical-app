# Domain model

## Project
A project is the top-level aggregate for one machine/electrical job.

Target model:

```text
Project
├── identity
├── settings
├── elements[]
├── circuits[]
└── safetyFunctions[]
```

## Element
An `Element` represents a physical or logical engineering component used in the project.

Existing relevant fields include:
- `id`
- `block`
- `type`
- `tag`
- `name`
- `manufacturer`
- `reference`
- `qty`
- `voltage`
- `phases`
- `currentA`
- `powerKw`
- `di`, `do`, `ai`, `ao`
- `sdi`, `sdo`
- `communication`
- `connection`
- `port`
- `safetyClass`
- cable fields
- `notes`

Do not duplicate an existing physical component just because it participates in a safety function. Reference it from the safety function.

### Adaptive power receiver metadata

Power elements retain their existing electrical fields and add a `receiver` object for type-specific metadata: normalized `kind`, location, supply type, frequency, starting method, simultaneity, starting current, associated-equipment identity and per-field data provenance. Provenance is one of `manual`, `imported`, `calculated` or `assumed`. Fields that do not apply to the selected receiver kind are stored as empty/null and must not participate in future calculations.

`receiver.calculations` stores traceable current results. `designCurrent` is the circuit Ib, `calculatedCurrent` keeps the independently calculated value for comparison when a plate/manufacturer current exists, and `demandCurrent` applies simultaneity only for aggregations. Each result retains status, unrounded value, unit, formula, inputs, missing data and warnings. Starting current remains separate and is explicitly excluded from Ib.

## Circuit
A circuit represents a power branch / distribution design result. It may reference the source `elementId`.

## SafetyFunction — Phase 1 entity

Minimum proposed structure:

```json
{
  "id": "sf-001",
  "code": "SF-001",
  "name": "Emergency stop",
  "description": "Stops hazardous movement",
  "requiredPL": "d",
  "source": {
    "type": "manual|import",
    "fileName": "",
    "row": null
  },
  "stages": {
    "input": [],
    "logic": [],
    "output": []
  },
  "preferences": {
    "inputManufacturer": "",
    "logicType": "safety_relay|safety_plc|either",
    "logicManufacturer": "",
    "outputManufacturer": ""
  },
  "calculation": {
    "status": "not_calculated",
    "achievedPL": null,
    "method": null,
    "warnings": []
  },
  "validationStatus": "draft"
}
```

Each stage entry should support at least:
- `elementId` for an existing project component,
- optional `proposedComponentId` when the engine proposes a library/article candidate,
- role/channel metadata,
- provenance/validation metadata.

In the implemented Phase 1 slice, stages store only `{ "elementId": "..." }` links. An empty stage array means that component selection is pending. Proposed components and reliability parameters remain out of scope.

## SafetyLibraryItem — target normalized model
Do not bind the app directly to the original SISTEMA library schema. Normalize imported records to a model containing only source-grounded fields, for example:

```text
SafetyLibraryItem
├── id
├── manufacturer
├── reference
├── name
├── subsystemType / role
├── safety parameters (only when present in source)
├── sourceLibrary
├── sourceItemId
├── sourceFile
├── importedAt
└── raw/source metadata for traceability
```

The exact reliability fields must be derived from real SISTEMA/IFA library samples rather than guessed from this document.

## SafetyLibrary — infrastructure

The application-level `safetyLibraries[]` repository stores detected `.slb`, VDMA 66413 XML and identifiable SISTEMA XML sources independently of projects. Each library retains its source filename, format, import date, status and warnings. Components remain empty until a verified parser can extract them with traceability; safety parameters default to `null` and are never inferred from EPLAN.
