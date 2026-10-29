# v0.7.0 verification — 29 October 2026

668 indexed records: 133 selected renal profiles, 28 shared safety notes and 507 renal-dose-pending catalog records. 53 source-based PK profiles; 40 contain all four core items. Every entry remains independently unapproved.

## Source review scope

Selected sections of five supplied PDFs were reviewed, not every monograph in the handbook. Individual imported source pages, continued pages, file hashes, edition/date and six source disagreements are recorded in SOURCE_AUDIT.json and sources[].suppliedDocument. PK table crops were visually inspected for all 26 handbook additions; dialysis-category text was checked separately. Superscript references were distinguished from digits, ceftaroline total-L Vd from L/kg, conventional HD from high-flux, and the adjacent anephric column from CVVHD flow columns. Current oral cefuroxime and oral/IV voriconazole labels were checked to reconcile specific source differences. A source check is not independent clinical validation.

## Automated checks

- checks.mjs checks all drug/source IDs, approved-review state, schema, embedded data/document equality, unchanged pre-existing CKD/IHD/PD/CRRT tables and clinically important original edge cases.
- checks_v07.mjs compares against the full v0.6 baseline: 621 unrelated records and all 27 existing PK summaries are unchanged; the 47 changed records cover the declared additions. Existing source records and shared guidance remain unchanged.
- Specific regressions cover Vd units/superscripts, high-flux uncertainty, unknown versus not-curated removal, oral versus IV restrictions, daily versus post-session HD, withheld continuous-PD schedules, TMP component units, PIRRT source/page/session/timing and CVVHD flow columns.
- Actual app search functions cover brand/exact-name ordering, spelling suggestions, setting/PK/latest filters and queue/reference exports. The 668-drug completion queue matches the final data.
- Actual service-worker logic is exercised with simulated network/caches: install, offline reopen, deliberate update activation, wrong-release/checksum/404 rejection and per-path cache isolation.
- ZIP CRC and root SHA-256 checksums are verified. A fresh extraction rebuild is compared with the packaged runtime/data/documents.

## Browser checks

The managed HTTP preview displayed the final release. Cefuroxime showed the current oral-label table and source-disagreement notice. At 320- and 390-pixel iframe widths, ceftaroline/meropenem search, PK and PIRRT sections had no horizontal page overflow. Ceftaroline Vd displayed 20.3 L; meropenem displayed the 3–4-hour infusion/timing note and prescription conditions. These are responsive-browser checks, not physical-phone performance or bedside validation.

## Remaining checks and limitations

Independent nephrologist and renal-pharmacist review, full formulary/indication coverage, authorised BNF monograph comparison and resolution of retained source conflicts remain incomplete. The historical PK additions are clearly dated 2018 (©2019). No modern circuit clearance or supplemental dose was calculated from PK properties. No intraperitoneal peritonitis regimen is implied.

The internal HTTP preview cannot activate the offline worker. Check HTTPS installation, airplane-mode reopen, update activation and storage persistence on a physical phone after GitHub upload. External clinical source links need internet. Software checks cannot establish clinical validity.
