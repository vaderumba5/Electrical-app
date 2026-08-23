# Codex bootstrap — complete v0.7 baseline

The repository already contains the v0.7 documentation, backend and support files. The GitHub connector used during setup could not transfer the three largest local files directly.

## Required archive
Upload this file to the repository root before starting development:

`App_Electrica_v0.7_CodexReady.zip`

Expected SHA-256:

`fe65153c4d8cb1a6998a92b9c5bbcdabf723fd0ab9a596312ee23301a8e5bfef`

## Bootstrap task for Codex
If the archive exists and any of the following baseline files are missing:

- `index.html`
- `eplan_catalog.json`
- `eplan_catalog.js`

then, before implementing any feature:

1. Verify the ZIP SHA-256 against the value above.
2. Extract it to a temporary directory.
3. Copy the **contents** of `App_Electrica_v0.7_CodexReady/` to the repository root, preserving the directory structure.
4. Do not place the project under a nested `App_Electrica_v0.7_CodexReady/` directory.
5. Verify these baseline hashes:
   - `index.html`: `376d31c33c956baba92969ea4e543e286582a3c480802eb18547db0c3a641cb1`
   - `eplan_catalog.json`: `cc68686a5d1ada384d73582c1829ef32ec8f76e3adb3d1c33e1a8b65b6627758`
   - `eplan_catalog.js`: `88339ccdf3c5bf2aecf271ea860d19d60c8ce5df5f322a7a1468688c0ab3cbdf`
6. Confirm `python -m py_compile backend.py` succeeds.
7. Run a JavaScript syntax check for the inline script in `index.html`.
8. Remove the ZIP from the working tree after successful extraction unless it is intentionally retained outside version control.
9. Commit the restored v0.7 baseline before beginning Phase 1 feature work.
10. Then read `AGENTS.md` and execute `CODEX_START_HERE.md`.

Do not modify engineering behavior during the bootstrap commit.
