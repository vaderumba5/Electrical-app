# Roadmap

## Baseline — v0.7
Existing project/catalogue/power functionality is the preserved starting point.

## Phase 1 — Functional safety foundation
- Add `safetyFunctions[]` to projects with backward-compatible migration.
- Create/edit/delete safety functions.
- Capture function code/name/description and required PLr.
- Model Input / Logic / Output stages.
- Link stage entries to existing project `elements`.
- Add manufacturer/logic-type preferences.
- Show incomplete/ready status without inventing PL calculations.
- Preserve current generic safety elements and legacy imported SDI/SDO data.

## Phase 2 — SISTEMA library import
- Collect real library samples.
- Detect supported file/version structures.
- Parse safely.
- Normalize library components.
- Store provenance.
- Search/filter imported safety components.

## Phase 3 — Safety component proposal
- Use required PLr, role and user preferences to find candidate architectures/components.
- Prefer company-standard/EPLAN articles when verified data supports them.
- Reuse project components when valid.
- Explain why candidates are compatible, pending, or rejected.

## Phase 4 — PL calculation engine
- Implement the verified calculation model and necessary validation inputs.
- Track missing data and assumptions explicitly.
- Compare achieved PL with PLr.
- Add deterministic test cases and reference comparisons.

## Phase 5 — SISTEMA project export
- Reverse-engineer only from legitimate real sample project files/documented interfaces.
- Generate a project containing all safety functions/subsystems/components.
- Open generated files in official SISTEMA.
- Validate calculations/structure against the app.
- Generate official reports from SISTEMA.

## Phase 6 — Deeper project/EPLAN automation
- EPLAN SQL integration using a normalized repository boundary.
- Further automated article assignment.
- Future EPLAN project/script/API integration where supported.
