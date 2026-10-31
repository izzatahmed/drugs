# v0.12.3 verification

Current suites: checks.mjs, checks_v123.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v123.py and apply_reviews.py. checks_v123.mjs proves dose tables and pregnancy sections are unchanged from v0.12.2, no field cites the Renal Drug Handbook, every rebuilt PK value cites a DailyMed, EMA or emc source, and every number in a value appears in its quoted label sentence.

These are software/source-integrity checks, not clinical validation.
