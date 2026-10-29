# v0.9.0 software and source-integrity verification

The package provides checks.mjs, checks_v09.mjs and checks_calculator.mjs. They check schema/source integrity, exact retention of unrelated v0.8 records and prior PK/regimens, source-specific high-consequence formulation/units/timing distinctions, embedded data/documents, indexed remaining-work exports, search/filter behaviour and calculator arithmetic against published NKF examples and independent MDRD calculations.

Browser QA measures actual clinical font sizes at each text setting, tests increase/decrease/reset and reload persistence, checks 320/390-px layouts at 150%, and exercises drug navigation and the retained calculator. A clean extracted package is rebuilt and compared byte-for-byte with source/dist; root SHA256 sums and ZIP CRC are checked. These checks establish software behaviour and provenance consistency, not clinical validity. Physical-phone installation and hosted HTTPS offline update checks remain pending after upload.

Independent clinical approval, BNF comparison, full renal/RRT coverage, source reconciliation and local product authorisation remain pending. See COMPLETION_PLAN.md and REMAINING_MEDICATIONS.json.
