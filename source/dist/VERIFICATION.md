# v0.6.0 verification — 29 October 2026

Clinical content remains draft: 668 records, 113 renal profiles, 28 shared safety notes and 527 renal-dose-pending catalog records. PK coverage remains 27 profiles, 15 with four core PK items. Independent clinical approval is pending for every record.

## Clinical-source work in this release

Twelve catalog records were promoted to renal profiles: bisoprolol, candesartan, clonidine, enalapril, hydralazine, indapamide, irbesartan, losartan, methyldopa, ramipril, telmisartan and valsartan. Individual UK product information was reviewed; source links remain on each profile. Eight new CKD tables and one product-specific restriction/reference table were added; clonidine, hydralazine and methyldopa retain nonnumeric specialist advice. Seven new IHD summary panels include explicit starting/initial or supplement advice. No new PD/CRRT/SLED dose was extrapolated.

BNF is clarified as British National Formulary. Direct BNF access returned 403; reconciliation is pending. ERA's indexed guidance directory was reviewed but direct access returned 403; linked documents are not all reviewed. ASN Kidney News August 2024 pages 13–14, NKF medication safety pages and KDIGO 2024 medication-management practice points were reviewed for their stated educational/guideline roles. The reference directory does not imply ASN/ERA/NKF approval of the new drug tables.

## Passed checks

- General checks.mjs: record/source integrity, review state, explicit PK/modality gaps, original regimen regressions and embedded data/documents.
- checks_v06.mjs: SHA-256 fingerprints match all 656 unrelated clinical records, every existing source and all 668 PK records from v0.5; twelve updated records are explicitly allowlisted.
- New checks preserve initial TOTAL daily amounts, ramipril boundary overlaps and daily/HD timing, enalapril dialysis/non-dialysis distinction, bisoprolol indication differences, indapamide product restriction, absent numeric clonidine/hydralazine/methyldopa bands and valsartan dialysis uncertainty.
- Actual search/filter functions, spelling suggestion behavior, completion queue and reference-directory export consistency. Browser startup, new enalapril/irbesartan CKD/HD tables, five further updated HD panels and the full reference directory were checked. At 320/390 px phone widths, the directory showed all 9 cards with no horizontal overflow (content widths 256/326 px).
- Actual worker logic in simulated network/cache tests: offline reopen, explicit update activation, checksum/wrong-release/404 rejection and cache isolation across repository paths.

## Limits

Software checks do not establish clinical validity. No independent nephrologist/renal-pharmacist approval, licensed BNF reconciliation, full interaction monograph, physical-phone installation or HTTPS airplane-mode test is claimed. The internal HTTP preview cannot activate the offline worker; check on the user's GitHub Pages site after upload. Source links require internet. Numerical gaps are retained and not inferred from PK parameters.
