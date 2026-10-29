# RenalRounds v0.9.0 · 29 October 2026

This cumulative release adds 85 selected adult renal profiles and 13 historical PK profiles. The 668-entry inventory now contains 218 partial renal profiles, 28 shared safety notes and 422 renal-dose-pending catalog entries. There are 66 PK profiles, 52 with all four core items. No independent clinical approval is recorded.

Readable text: default clinical text is 16 px. A− / percentage reset / A+ select 100%, 115%, 130% or 150%, including renal tables and PK values. The preference persists when browser storage is available. Old enlarged-text preferences migrate to 115%.

New guidance includes remaining selected anti-infectives, all 24 indexed psychiatry entries (selected renal statements only), warfarin, nebivolol, olmesartan, digoxin, selected diabetes agents, bone medicines and prucalopride. Exact route, product, indication, dose units, loading versus maintenance and renal measure remain visible. Some profiles contain monitoring, caution or insufficient-data statements rather than numeric doses.

The adult CKD-EPI 2021 / legacy MDRD calculator is retained. It does not select a drug dose; CrCl, indexed eGFR and non-indexed eGFR must not be interchanged automatically.

Source differences retained: minocycline oral daily limit versus institutional high dosing; IV posaconazole vehicle restriction; lamivudine label versus institutional practice; emtricitabine NIH/FDC-derived advice; dated EXBLIFEP measure ambiguity; VABOMERE historical MDRD equation. Paliperidone ER starting alternatives differ between products; only the linked label's table is selected.

This is not a completed formulary. REMAINING_MEDICATIONS.json lists 450 entries without drug-specific renal profiles, including 28 shared safety notes. Every renal profile also requires formulation/indication/RRT completion and independent nephrology plus renal-pharmacy review. Missing dialysis information is not extrapolated from CKD, another modality or PK. BNF monograph comparison remains pending.

## Completion work

Use CURATION_QUEUE.json for field-by-field status and REMAINING_MEDICATIONS.json for the remaining renal-profile inventory. Agree the local adult formulary and prioritise common rounds/OTC agents, then check each exact product and indication against current authorised information and licensed references. Reconcile conflicting doses and kidney-function measures. Complete IHD, systemic PD, CRRT and prescription-specific PIRRT/SLED separately; intraperitoneal peritonitis regimens require their own review. Record independent sign-off before clinical release. Current-source checks and software verification do not confer clinical approval.
