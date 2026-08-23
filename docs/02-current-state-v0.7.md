# Current state — v0.7

## Baseline reviewed
The supplied v0.7 archive contains 11 runtime/support files and approximately 5.1 MB uncompressed data.

### Frontend
`index.html` is a single-file application containing UI, state management and most engineering calculations.

It already exposes:
- Proyectos
- Catálogo
- Inicio
- Potencia
- Control
- Seguridad
- PLC
- Ajustes

### Persistence
Projects are stored in browser `localStorage`. Current project structure is created by `makeProject()` and includes `elements`, `circuits` and `settings`.

### Shared components
All engineering blocks use the same `state.elements` collection. This is the correct starting point for linking functional safety to components already defined elsewhere in the project.

### Safety today
The safety block currently manages generic safety elements such as:
- Relé de seguridad
- PLC de seguridad
- Seta de emergencia
- Barrera de seguridad
- Escáner de seguridad
- Magnético / enclavamiento
- Mando bimanual

Legacy signal import can classify elements as safety based on SDI/SDO or safety-zone data.

What is **not yet implemented**:
- project-level safety functions,
- PLr per function,
- structured Input / Logic / Output chains,
- automatic component proposal for a target PLr,
- SISTEMA library importer,
- normalized SISTEMA safety data,
- PL calculation engine,
- SISTEMA project export.

### Power today
The power block is already substantially implemented. Its current intended workflow is:
1. real receivers,
2. network data,
3. manufacturer/manual restrictions,
4. suggested physical branches,
5. general protection and RCD constraints,
6. EPLAN article selection.

Important v0.7 behaviors that must be preserved:
- one physical S210 = one physical branch by default,
- S210 manufacturer-specific protection rules,
- missing `Iz`/`Ik` blocks final approval,
- DC power-supply output current is not interpreted as AC input current,
- local EPLAN match does not automatically equal technical approval.

### Backend today
`backend.py` provides:
- `/api/health`
- `/api/sql/status`
- `/api/enrich`
- `/api/power/reference`
- `/api/power/search-protection`

SQL integration is only a configuration/status placeholder at this stage.

### Tests today
`TESTS.txt` documents manual/baseline checks, but there is not yet a proper automated test suite. Adding deterministic tests is a priority as engineering logic grows.
