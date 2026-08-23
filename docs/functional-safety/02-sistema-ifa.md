# SISTEMA / IFA integration

## Objective
Use SISTEMA/IFA manufacturer libraries as a source of traceable safety data and later make it possible to transfer completed safety functions to SISTEMA for official project/report workflows.

## Phase order
1. Obtain representative real SISTEMA library files used by the team.
2. Inspect their actual structure/version.
3. Implement a parser/importer.
4. Normalize imported records into the application's internal safety-library model.
5. Preserve source provenance and raw identifiers.
6. Build calculation/selection logic against the normalized model.
7. Only later implement project export after verifying the real SISTEMA project format.
8. Round-trip test by opening generated output in official SISTEMA and comparing the resulting structure/calculation.

## No-guess rule
Do not invent a SISTEMA library or project schema from memory. Parser and exporter work must be driven by real sample files and verified behavior.

## Desired end state

```text
Manufacturer SISTEMA libraries
          ↓
import + normalization
          ↓
App safety library
          ↓
SafetyFunction design
          ↓
complete validated safety project
          ↓
verified SISTEMA export
          ↓
open in SISTEMA
          ↓
official SISTEMA reports
```
