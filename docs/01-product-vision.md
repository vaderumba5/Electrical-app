# Product vision

App Eléctrica is intended to assist the electrical department in designing industrial-machine electrical projects from real project requirements and standard company articles.

## Core project blocks
1. **Potencia** — incoming supply, distribution, real receivers, branch circuits, protections and auxiliary power supplies.
2. **Control** — devices that are not simple PLC I/O, such as vision systems, readers and special controllers.
3. **Seguridad** — safety devices and, progressively, complete functional-safety functions and PL evaluation.
4. **PLC** — CPU, remote I/O, normal and safe I/O needs, communications and related devices.

## Design philosophy
The user should enter the real equipment/requirements of the machine. The application then derives engineering consequences and proposes compatible standard articles.

The application must distinguish:
- engineering requirement,
- technical validation,
- commercial article availability,
- provenance of technical data,
- pending/unknown values.

It is an engineering-assistance tool, not an excuse to silently infer missing safety-critical data.
