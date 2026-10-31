# v0.12.0 verification

Current suites: checks.mjs, checks_v120.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v120.py. checks_v120.mjs proves no dose table cites the handbook, every rebuilt entry cites a retrieved label with set ID/version or emc product ID, entries outside the 61 are unchanged from v0.11.3, and runs the service-worker contract for 0.12.0.

These are software/source-integrity checks, not clinical validation.
