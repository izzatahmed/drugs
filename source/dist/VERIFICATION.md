# v0.12.1 verification

Current suites: checks.mjs, checks_v121.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v121.py. checks_v121.mjs checks the ISPD Table 5 values, the vancomycin/aminoglycoside numbers against their sources, the vonoprazan label table, that pregnancy excerpts are verbatim substrings of the stored label text, and that all other entries are unchanged from v0.12.0.

These are software/source-integrity checks, not clinical validation.
