# v0.22.0 verification

Current suites: checks.mjs, checks_v220.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v220.py and apply_reviews.py. checks_v220.mjs proves drug records are unchanged from v0.21.0, checks the four new calculators against worked cases (including both branches of the TmP/GFR algorithm) and re-runs every v0.21 calculator case.

These are software/arithmetic checks, not clinical validation.
