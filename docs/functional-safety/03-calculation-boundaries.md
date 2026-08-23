# PL calculation boundaries

## Required behavior
The app will eventually evaluate whether the designed safety function reaches the requested PLr.

## Current rule
Do not implement a fake or simplified PL result merely to fill the UI. Until the necessary source data and method are grounded, use states such as:
- `not_calculated`
- `missing_data`
- `ready_to_calculate`
- `calculated`
- `needs_review`

## Traceability
Any calculated result must retain:
- components/subsystems used,
- source of safety parameters,
- assumptions,
- calculation method/version,
- warnings/missing values,
- achieved result,
- comparison with PLr.

The application should be auditable: a user must be able to understand why a function was considered valid or not valid.
