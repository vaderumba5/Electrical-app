# Electrical engineering engine

## Receiver-driven design
Power design starts with real receivers, not protections.

```text
Receiver
  ↓
manufacturer/reference + electrical data
  ↓
manufacturer restrictions
  ↓
Ib / physical branch requirement
  ↓
cable / Iz context
  ↓
protection requirement
  ↓
EPLAN catalogue candidate
  ↓
technical validation
```

## Current rules
- Prefer documented input current over inferred current.
- If current must be calculated from power, voltage, phases, cos φ and efficiency, preserve the assumptions used.
- Unknown critical values must remain unknown.
- Single-phase loads can be automatically balanced across L1/L2/L3 when phase is not fixed.
- General protection must consider maximum phase current.
- Final protection validation depends on conductor capacity and short-circuit data (`Iz`, `Ik`) and on manufacturer constraints.

## 24 VDC
All real 24 VDC consumers across project blocks can contribute to DC supply sizing.

```text
24 VDC consumers
  ↓
sum known current
  ↓
identify unknown-current consumers
  ↓
apply configured design reserve
  ↓
select next suitable standard supply rating
```

If any relevant consumer current is unknown, the application must surface the uncertainty rather than pretend the supply is definitively sized.

## Article selection
1. Determine the technical requirement.
2. Search the normalized EPLAN catalogue.
3. If no sufficient local article exists, search/validate official manufacturer data through the backend when possible.
4. Keep technical status and inventory/catalogue status separate.
