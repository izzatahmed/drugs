# v0.11.3 verification

Current suites: checks.mjs, checks_v113.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v113.py. checks_v113.mjs proves every dose table, modality status, PK field and source URL is identical to v0.11.2, checks the Cockcroft–Gault arithmetic against hand-worked examples, and runs the service-worker offline/update contract for 0.11.3.

These are software/source-integrity checks, not clinical validation.
