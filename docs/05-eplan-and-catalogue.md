# EPLAN and article catalogue

## Current baseline
The normalized EPLAN export contains **6,133 parsed/usable `<part>` records**. The original export declared a larger count, so the application reports the actually normalized records.

Current generated files:
- `eplan_catalog.json`
- `eplan_catalog.js`

## Current role
The normalized catalogue supports manufacturer/reference identity and selected normalized technical metadata such as voltage/current when semantically clear, poles, trip curve, RCD sensitivity/type, breaking capacity and document links.

## Important rule
EPLAN article presence is not proof that the article satisfies a safety or power requirement. Official/verified technical documentation takes priority.

## Future SQL path
The backend currently exposes SQL configuration status through `/api/sql/status`, but direct EPLAN SQL access is not implemented yet. When SQL integration is added, preserve the same normalized internal article model so the rest of the app does not depend on the physical EPLAN database schema.
