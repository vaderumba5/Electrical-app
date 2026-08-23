# Current phase — Phase 1: Functional safety foundation

## Objective
Extend the existing v0.7 project model so functional safety is a first-class project feature, while preserving every working v0.7 behavior.

## First implementation slice
Implement only the following coherent slice:

1. Extend `makeProject()` / normalization/migration so every project has `safetyFunctions: []`.
2. Existing localStorage projects must migrate without data loss.
3. In the Seguridad view, add a **Funciones de seguridad** area separate from the existing generic safety-component list.
4. Support manual create/edit/delete of a safety function with:
   - code,
   - name,
   - description,
   - required PLr (`a`..`e`),
   - source type (`manual` initially),
   - validation status.
5. Add Input / Logic / Output stage containers.
6. Allow a stage to link to an existing project element by `elementId`.
7. Display linked element tag/name/manufacturer/reference without duplicating the element.
8. Add preferences for:
   - input manufacturer,
   - logic type (`safety_relay`, `safety_plc`, `either`),
   - logic manufacturer,
   - output manufacturer.
9. Calculation status must remain `not_calculated` / `missing_data`; do not produce an achieved PL yet.
10. Add tests or deterministic verification for migration and safety-function persistence.

## Explicitly out of scope for this slice
- SISTEMA file parsing.
- PL calculation formulas.
- automatic safety component selection.
- SISTEMA project export.
- broad frontend framework migration.
- replacing localStorage with a database.

## Acceptance criteria
- Existing sample/current v0.7 projects still load.
- Existing `elements` and `circuits` are unchanged after migration.
- A safety function persists across browser reload.
- A safety function can link to an existing safety/PLC/power element.
- Deleting a safety function does not delete linked elements.
- Deleting an element does not silently corrupt the safety function; the UI must show the reference as missing/unresolved.
- No PL value is fabricated.
