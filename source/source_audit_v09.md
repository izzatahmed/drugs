# RenalRounds v0.9.0 · 29 October 2026

This cumulative release adds 85 selected adult renal profiles and 13 historical PK profiles. The 668-entry inventory now contains 218 partial renal profiles, 28 shared safety notes and 422 renal-dose-pending catalog entries. There are 66 PK profiles, 52 with all four core items. No independent clinical approval is recorded.

Readable text: default clinical text is 16 px. A− / percentage reset / A+ select 100%, 115%, 130% or 150%, including renal tables and PK values. The preference persists when browser storage is available. Old enlarged-text preferences migrate to 115%.

New guidance includes remaining selected anti-infectives, all 24 indexed psychiatry entries (selected renal statements only), warfarin, nebivolol, olmesartan, digoxin, selected diabetes agents, bone medicines and prucalopride. Exact route, product, indication, dose units, loading versus maintenance and renal measure remain visible. Some profiles contain monitoring, caution or insufficient-data statements rather than numeric doses.

The adult CKD-EPI 2021 / legacy MDRD calculator is retained. It does not select a drug dose; CrCl, indexed eGFR and non-indexed eGFR must not be interchanged automatically.

Source differences retained: minocycline oral daily limit versus institutional high dosing; IV posaconazole vehicle restriction; lamivudine label versus institutional practice; emtricitabine NIH/FDC-derived advice; dated EXBLIFEP measure ambiguity; VABOMERE historical MDRD equation. Paliperidone ER starting alternatives differ between products; only the linked label's table is selected.

This is not a completed formulary. REMAINING_MEDICATIONS.json lists 450 entries without drug-specific renal profiles, including 28 shared safety notes. Every renal profile also requires formulation/indication/RRT completion and independent nephrology plus renal-pharmacy review. Missing dialysis information is not extrapolated from CKD, another modality or PK. BNF monograph comparison remains pending.

## Additional historical PK pages

- Warfarin: supplied fifth-edition PDF p1092, printed p1073.
- Glimepiride: supplied fifth-edition PDF p502, printed p483.
- Glipizide: supplied fifth-edition PDF p503, printed p484.
- Pioglitazone: supplied fifth-edition PDF p826, printed p807.
- Sertraline: supplied fifth-edition PDF p931, printed p912.
- Quetiapine: supplied fifth-edition PDF p870, printed p851.
- Mirtazapine: supplied fifth-edition PDF p684, printed p665.
- Olanzapine: supplied fifth-edition PDF p752, printed p733.
- Nebivolol: supplied fifth-edition PDF p718, printed p699.
- Olmesartan: supplied fifth-edition PDF p755, printed p736.
- Digoxin: supplied fifth-edition PDF p338, printed p319.
- Ibandronate: supplied fifth-edition PDF p521, printed p502.
- Minocycline: supplied fifth-edition PDF p680, printed p661.

## Prior audit and supplied-file hashes

# Supplied-source audit · v0.7.0

Selected sections reviewed on 2026-10-29. This is not a full clinical review of all five documents. Metadata dates do not establish clinical currency. Original PDFs are excluded from this package.

## Renal Drug Handbook, 5th edition

- Edition/date: Published June 2018; copyright 2019
- Supplied filename: The_Renal_Drug_Handbook_The_Ultimate.pdf
- PDF pages: 1109
- SHA-256: `f918bdcd99034cb93b5a24dbc7bf626bdb1fc831dcbb0d85e0f57ceecff83c20`
- Use: Selected PK/removal fields only; historical reference, not a current formulary
- Scope: Selected sections only; not a full clinical review of every page.

## KDIGO drug-dosing clinical update

- Edition/date: Kidney International 2011; 80:1122–1137
- Supplied filename: KDIGO-DrugDosingReportFinal.pdf
- PDF pages: 16
- SHA-256: `fc677826cdad42777ba4c3b20c8cc17d97e517400efd5fc0f45a93b53e877a4d`
- Use: Foundational principles; read with KDIGO 2024 medication guidance
- Scope: Selected sections only; not a full clinical review of every page.

## BC Renal common oral antimicrobial dosage adjustments

- Edition/date: February 2018; approved May 2017 version 1
- Supplied filename: Common_Oral_Antimicrobial_Therapy_Dosage_Adjustment.pdf
- PDF pages: 2
- SHA-256: `3a5bd18f3a79613410e0429631bf822840424ff444ac6a706531987b3c0a7c68`
- Use: Comparison source; broad indications and older schedules require reconciliation
- Scope: Selected sections only; not a full clinical review of every page.

## Nebraska CRRT/PIRRT antimicrobial recommendations

- Edition/date: 2023 filename; PDF created April 2026; no revision date printed
- Supplied filename: final_crrt_pirrt_abxrecommendations_2023.pdf
- PDF pages: 18
- SHA-256: `f1b249a31c3c12899c997bcc791ea3d1267865c0d33061e868f2cae815cf9307`
- Use: CVVHD flow tables and prescription-specific PIRRT recommendations; metadata is not a clinical revision date
- Scope: Selected sections only; not a full clinical review of every page.

## Nebraska renal antimicrobial protocol MP01 Attachment A

- Edition/date: P&T approval April 2026; PDF created August 2026
- Supplied filename: dose-nm-anti-infective-renal-dosing-guidelines.pdf
- PDF pages: 71
- SHA-256: `a3a5ec05580f383e130584a4be38575d00be207fb722423571b8fc53fd4830ed`
- Use: Selected adult CKD/IHD/systemic PD rows; excludes paediatric rows and IP peritonitis regimens
- Scope: Selected sections only; not a full clinical review of every page.

## Source disagreements and gaps

### cefuroxime

Oral renal intervals differ between current tablet label, Nebraska protocol, BC 2018 sheet and handbook fifth edition.

Action: Active oral table follows the current tablet label; IV and PD are not inferred.

Status: source_difference_retained

### clarithromycin

Nebraska PD no-adjustment row differs from older source reductions.

Action: Numeric PD regimen withheld; immediate-release CKD/IHD source retained.

Status: clinical_reconciliation_pending

### flucytosine

Nebraska HD/PD grouped post-dialysis three-times-weekly wording does not define a continuous-PD schedule.

Action: Only IHD schedule displayed; PD requires specialist review.

Status: source_ambiguity_retained

### valganciclovir

Institutional very-low-dose HD schedules and mixed-analyte handbook PK need formulation/analyte reconciliation.

Action: Non-dialysis induction/maintenance only. No numeric HD/PD dose or mixed-analyte PK profile imported.

Status: clinical_reconciliation_pending

### levofloxacin

PIRRT row lacks an unambiguous interval in its main dose cell; comments refer to different reference regimens.

Action: PIRRT numeric regimen not imported. Existing CKD/IHD remains unchanged.

Status: source_ambiguity_retained

### piperacillin-tazobactam

Book PD categorical statement and reported removal percentage differ in the same monograph.

Action: Both are qualified in PK evidence; no PD regimen inferred.

Status: source_difference_retained

See database.json sources[].suppliedDocument for per-drug PDF pages, continuation pages and checksums. Public publisher/organisation links are identified as listings where they do not provide the exact supplied PDF. Source access is separate from independent clinical approval.
