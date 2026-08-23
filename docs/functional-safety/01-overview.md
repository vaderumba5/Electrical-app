# Functional safety — target architecture

## Goal
The safety block evolves from a list of safety devices into a project-level functional-safety workspace.

The company can receive safety functions already defined with a required PL. The application should be able to import or create those functions, then assist in building a compatible safety chain using company-standard articles and verified safety data.

## Safety function flow

```text
Safety function
    ↓
PLr required
    ↓
Input stage
    ↓
Logic stage
    ↓
Output stage
    ↓
verified safety data
    ↓
PL calculation / validation
    ↓
achieved PL vs PLr
```

## Component-selection preferences
The user should be able to constrain/provide preferences such as:
- input manufacturer,
- logic architecture: safety relay or safety PLC,
- logic manufacturer,
- output manufacturer,
- preference for company-standard/EPLAN articles,
- preference to reuse components already present in the project when technically valid.

## Project linkage
A safety function must be able to point to an existing `Element` from any appropriate block. Example: a drive defined under Potencia can later be part of the safety output stage without creating a duplicate drive record.

## Validation principle
The system may propose components, but a proposed chain is not approved merely because the target PL label matches. The required architecture/reliability parameters and manufacturer constraints must be validated using traceable data.
