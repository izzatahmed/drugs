# v0.11.2 verification

Current suites: checks.mjs, checks_v112.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v112.py. Checks cover exact preservation of v0.11.1 records, 60 edition-based additions, source checksum/page references, dose units and special cases, partial PK/absent versus withheld fields, clear continuous/SLED gaps, live Home/filter/back/theme/font logic, calculator arithmetic/privacy, embedded documents and actual service-worker offline/update integrity. Cumulative extraction/rebuild and byte-level patch overlays are verified. Browser QA checks Home at phone widths, preserved reader settings, in-app back, and dated dose displays.

These are software/source-integrity checks, not clinical validation. Current product reconciliation, BNF comparison, independent approval and physical-phone HTTPS integration remain pending.
