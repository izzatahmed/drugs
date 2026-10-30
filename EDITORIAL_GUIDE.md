# RenalRounds v0.11.0 · 30 October 2026

The upper area is reduced to two compact rows: smaller text/theme/eGFR controls first, then a 40-px search field with Filters and Clear filters beside it. Filter actions use icons on narrow phones and visible labels on larger screens. Clear filters is disabled when no filter is active and does not erase the search query. Filter details remain collapsed until opened. Clinical-review badges and informational missing-data notices follow the clinical findings; explicit do-not-use warnings remain with their relevant setting.

The manual day/night choice, text-size preference, calculator and in-app semicircular back arrows are retained. Clinical text size remains readable and can increase independently of the compact controls.

Medication information is expanded for 32 records: two partial adult institutional renal profiles (omadacycline and telavancin), plus 30 historical PK-only panels in pain/neurology. The 668-entry inventory now has 260 partial renal profiles, 28 shared safety notes and 380 renal-dose-pending catalog entries. There are 99 PK panels; 55 have all four core items. Thirty new panels contain half-life, Vd and binding; their dialysis removal and dose schedules remain uncurated.

Online primary-source search and retrieval were unavailable during this batch. No new current product-label verification is claimed. The renal additions use the supplied institutional protocol approved April 2026; the PK additions use selected supplied fifth-edition handbook tables published in 2018 (copyright 2019). Historical reference numbers are distinguished from numeric values, and total Litres from L/kg. No historical renal-dose table or new dialysis-removal category is imported. Telavancin's current label, indication and jurisdiction need reconciliation; its numeric renal regimen is withheld.

Coverage remains incomplete. REMAINING_MEDICATIONS.json lists 408 records without a drug-specific renal profile (380 catalog entries plus 28 shared safety notes). PK availability does not establish a dose. Existing renal profiles also retain formulation/indication/RRT gaps. Independent clinical approval and BNF monograph reconciliation remain pending.

## Existing editorial policy · historical record

# RenalRounds v0.10.0 · 30 October 2026

Search is the first visible control. Large titles, introductory paragraphs and coverage blocks have been removed from above it. A compact text-size / manual day-night / eGFR toolbar follows search. Filters start collapsed. Renal dosing leads each drug entry; PK and secondary copy/print/coverage tools follow it. Sources, coverage and offline-update details are below the findings. A small fixed ↶ button returns through in-app medicine/setting/search history; each dialog also has a back arrow that closes the panel. It never leaves the app. Calculator inputs are excluded from navigation history and still clear on close.

Day/night preference is saved independently of the system theme, with light as the first-use default. Text-size controls retain 100%, 115%, 130% and 150%. Enlarged tables stack on narrow phones. Favourites, theme and text size use browser-local preferences when storage is available; patient calculator inputs are not persisted.

This release adds 40 selected adult renal profiles and 3 product-information PK panels. The inventory remains 668 entries: 258 partial renal profiles, 28 shared safety notes and 382 catalog entries without renal guidance. There are 69 PK profiles; 55 contain all four core items, including qualitative IHD product statements where expressly qualified. These are not all measured modern circuit-clearance studies.

New additions include cardiovascular/diuretic/lipid drugs, 11 BPH/bladder agents, 6 allergy/respiratory agents and 8 GI/constipation agents. Some entries provide caution or insufficient-data guidance without numeric doses. Selected product labels/SmPCs were checked on 30 October; existing sources retain their original dates. BNF monograph reconciliation and independent clinical approval remain pending. All older drug regimens and PK panels are retained unchanged.

Key distinctions: perindopril erbumine versus arginine strengths and unassigned exact cutoffs; fenofibrate product-specific starting doses and dialysis contraindication; mirabegron indexed MDRD measure; indexed CLcr wording for solifenacin/tamsulosin; IR versus ER trospium/tolterodine/oxybutynin; tiotropium capsules for inhalation only; aluminium toxicity risk with sucralfate. No CKD table is copied into missing RRT modalities.

This remains incomplete: REMAINING_MEDICATIONS.json lists 410 entries without drug-specific renal profiles (382 catalog entries plus 28 shared safety notes). Existing renal profiles also retain indication, formulation and RRT gaps. No entry has independent clinical approval.

## Existing editorial policy · historical release record

# RenalRounds v0.9.0 · 29 October 2026

This cumulative release adds 85 selected adult renal profiles and 13 historical PK profiles. The 668-entry inventory now contains 218 partial renal profiles, 28 shared safety notes and 422 renal-dose-pending catalog entries. There are 66 PK profiles, 52 with all four core items. No independent clinical approval is recorded.

Readable text: default clinical text is 16 px. A− / percentage reset / A+ select 100%, 115%, 130% or 150%, including renal tables and PK values. The preference persists when browser storage is available. Old enlarged-text preferences migrate to 115%.

New guidance includes remaining selected anti-infectives, all 24 indexed psychiatry entries (selected renal statements only), warfarin, nebivolol, olmesartan, digoxin, selected diabetes agents, bone medicines and prucalopride. Exact route, product, indication, dose units, loading versus maintenance and renal measure remain visible. Some profiles contain monitoring, caution or insufficient-data statements rather than numeric doses.

The adult CKD-EPI 2021 / legacy MDRD calculator is retained. It does not select a drug dose; CrCl, indexed eGFR and non-indexed eGFR must not be interchanged automatically.

Source differences retained: minocycline oral daily limit versus institutional high dosing; IV posaconazole vehicle restriction; lamivudine label versus institutional practice; emtricitabine NIH/FDC-derived advice; dated EXBLIFEP measure ambiguity; VABOMERE historical MDRD equation. Paliperidone ER starting alternatives differ between products; only the linked label's table is selected.

This is not a completed formulary. REMAINING_MEDICATIONS.json lists 450 entries without drug-specific renal profiles, including 28 shared safety notes. Every renal profile also requires formulation/indication/RRT completion and independent nephrology plus renal-pharmacy review. Missing dialysis information is not extrapolated from CKD, another modality or PK. BNF monograph comparison remains pending.

## Data editing and prior source policy

# RenalRounds — editorial guide

Version 0.8.0 · 29 October 2026 · Adult draft inventory and reference

This release contains 668 indexed drug/formulation entries: 133 sourced renal profiles, 28 shared safety-note records and 507 renal-dose-pending catalog records. Every entry awaits independent nephrologist and renal-pharmacist review. It is not a comprehensive formulary or an approved prescribing system.

## Data model

`database.json` separates drug identity, aliases, category, class, formulation, source-native kidney-function metric, source records and review state. Each drug has five treatment settings: `ckd`, `ihd`, `crrt`, `pd`, and `sled`. Each setting has an explicit status, indication-specific tables, source IDs and qualifying notes.

Allowed modality statuses:

- `summarized`: selected source dosing has been transcribed and condensed; this does not mean clinically approved or complete.
- `not_curated`: no applicable recommendation has yet been curated.
- `insufficient_data`: the cited reference explicitly identifies insufficient data.
- `specialist`: no automatic regimen is assigned; specialist review is needed.
- `avoid`: the cited restriction precludes use in the stated setting.
- `not_indicated`: the curated product/indication does not cover this setting. This is distinct from a drug-wide contraindication.

`review.sourceCheckedAt` records source access, not independent approval. `clinicalReviewer` and `clinicalApprovedAt` remain null throughout this release. A future approved release should have two independent named sign-offs, recorded discrepancies, a review date and a retained change log. Do not set these fields without a real review.

## Editorial workflow for a comprehensive formulary

1. Define jurisdiction, adult population, hospital formulary and approved clinical sources. Add generic names and country-specific brands without implying automatic interchangeability.
2. Prioritise antimicrobials, anticoagulants, analgesics, antiepileptics, diabetes drugs, cardiovascular drugs, immunosuppressants, antivirals, gout drugs, oncology therapies and common OTC agents. This release covers only selected drugs and indications in some of these groups.
3. For each indication and formulation, record the usual regimen, initial/loading dose, maintenance dose, interval, maximum dose, intended duration when appropriate, and source-native function metric and units. Store route and formulation distinctly; future numeric prescribing rules need structured min/max bounds and explicit inclusive/exclusive operators.
4. Preserve kidney-function thresholds exactly as written. Log source gaps and overlapping cutoffs. Do not invent a dose at an unassigned boundary. CKD stage alone is not a dosing rule. Do not treat indexed eGFR, absolute GFR, CrCl and serum creatinine as interchangeable.
5. Curate IHD dialyser type, schedule, dialytic removal, timing, interdialytic interval, post-HD supplementation and residual function. Separate daily regimens from post-session regimens.
6. Curate PD by CAPD/APD and residual function. Intraperitoneal peritonitis dosing needs a distinct route, dwell time and prescription. Do not copy systemic doses into IP therapy.
7. Curate CRRT by CVVH/CVVHD/CVVHDF, delivered effluent/flow, body weight, pre/post dilution, interruptions and residual function. UCSF summaries in this release assume CVVHD at 2 L/h and residual native GFR <10 mL/min. SLED/PIRRT needs its own session duration and settings.
8. Add drug-specific monitoring, toxicity, renal adverse effects, contraindications, major interactions, active metabolites and dialyzability from cited sources. These domains are not complete in the curated monographs.
9. Reconcile label-versus-guideline disagreements in writing, including jurisdiction and indication. Do not silently merge incompatible protocols. Confirm permissions before reproducing extensive commercial reference content.
10. Obtain independent renal-pharmacist and nephrologist sign-off, including indication, formulation, threshold boundaries, unit conversions and dialysis timing. Test approved clinical scenarios before bedside deployment.
11. Assign an editorial owner, review interval and source-change process. Record the exact label or guidance version where available, not just access date. This release has no automatic clinical updates; the interface flags source checks older than 90 days as overdue, an editorial reminder rather than a validated clinical review interval.

## Present limits

- Adult selected indications only. Not a complete interaction, adverse-effect, contraindication or prescribing monograph.
- Most PD and PIRRT/SLED entries remain gaps; 16 selected prescription-specific PIRRT summaries are included. UCSF CRRT content applies to specified CVVHD assumptions only. Cefiderocol is separately based on the US label effluent-flow table for CVVH/CVVHD/CVVHDF. Do not apply one source’s assumptions to the other.
- No patient-specific dose engine, AKI calculator, paediatric regimens, hepatic adjustment, pregnancy guidance or transplant protocols.
- US labels and institutional US guidance are not a substitute for the approved local product information.
- Brand aliases are examples, not an exhaustive brand index. A search miss is never evidence of safety.
- Favourites and text size are browser-local preferences. No patient data are collected. The self-contained HTML runs offline in browsers that execute local JavaScript; source links require internet. No service-worker installation or clinical approval editor is included.
- All clinical updates require an edited, checked and redeployed data version. Search does not call an AI model or generate a dose.

## Sources

Each monograph links its exact source. The collection uses UCSF Infectious Diseases Management Program pages, linked PDR digital monographs, current UK product SmPCs, and selected US prescribing information. BNF 92 (September 2026) was confirmed in the publisher listing, but its monograph content was inaccessible; every BNF comparison remains pending. PDR does not have a claimed numbered 2026 print edition in this release. Only linked monographs and the identified update bulletin are represented as consulted. Methodological guidance is linked from NIDDK's *Determining Drug Dosing in Adults with Chronic Kidney Disease*. These institutions have not endorsed this application.

## Application and data checks

Run `python3 build_data.py`, `python3 release_v06.py`, `python3 release_v07.py`, `python3 release_v08.py` and `python3 build_standalone.py` in order, then `node checks.mjs` and `node checks_v07.mjs` for data integrity, reference resolution, all-entry draft status and key search/boundary safeguards. Browser checks must additionally cover mobile layout, generic/brand searching, no-result state, modality selection, favourites, text size and source links. These checks validate the software/data structure; they do not constitute clinical validation.

## Version 0.2 reference comparison and expansion

The 40 additions are new to the collection, not 40 newly approved medicines. Per-entry `addedInVersion`, `jurisdiction`, and `referenceChecks` distinguish expansion, source basis and unresolved checks. No drug is labelled BNF-verified. A PDR update-bulletin check is distinct from accessing a PDR monograph. `marketStatus` flags historical US daprodustat: GSK discontinued Jesduvroq in December 2024.

UK and US advice remains separate where it differs (for example dapagliflozin and dabigatran). Product-specific formulations and indication restrictions are retained. Source access date is not a claim that a label was newly revised on that date. The label’s revision date is recorded in its source description only when actually observed. A full edition-wide BNF reconciliation still requires access to the licensed monograph text.

## Version 0.3 inventory distinctions

- `entryType=renal`: selected source renal-adjustment/monitoring profile, not necessarily a numeric dose or complete indication monograph.
- `entryType=safety`: shared patient-education safety guidance linked through `sharedGuidanceId`. This is not a drug-specific renal-dose monograph. No numeric renal or RRT dose is assigned.
- `entryType=catalog`: searchable inventory only. Clinical `sourceCheckedAt` is null; sources and dose tables are empty. The DailyMed search link is a search aid, not evidence that a label was checked. Identity, routes, aliases, current marketing and local availability need product-level verification.

Route metadata and the OTC filter are inventory aids; OTC availability varies by jurisdiction, formulation and strength. Do not infer a dose from a route or a class. Selected oral and injectable formulations are separate when renal advice or use differs. This broad inventory is not exhaustive of all medicines worldwide.

The 30 additional renal profiles cover selected antimicrobial, allergy, GI, cardiovascular, lipid, transplant and calcimimetic medicines. Shared OTC guidance is attributed to the National Kidney Foundation and Kidney Care UK, kept separate from numeric prescribing tables and stored once. The existing 70 profiles’ modality records are retained unchanged.

The user clarified that the intended reference is the British National Formulary (BNF), not a separate PNF. BNF reconciliation remains pending; PDR access is recorded only for individually consulted profiles.

`build_standalone.py` embeds the dataset, CSS, JavaScript, icon and these notes into one `index.html`. No network fetch is required for search. Content is static until a checked release is rebuilt and uploaded. The GitHub package has the generated index at its root and contains no Site identity, Git metadata, access credentials or patient data.

## Version 0.4 pharmacokinetic schema

Every record has `pharmacokinetics`: `halfLife`, `renalHalfLife`, `volumeOfDistribution`, `proteinBinding`, and a `dialysability` object for IHD, PD, CRRT and SLED. Each field has a value (or null), status, context and source IDs. The PK object has its own source-check date. A blank dose-review date on a catalog record can therefore coexist with a sourced PK summary; it does not mean a renal regimen has been checked.

At the v0.4 release, 27 cardiovascular/BP medicines had PK summaries; 15 had all four core reference items (half-life, Vd, binding and an IHD removal statement). Others retain explicit gaps. No profile has independent clinical approval. `updatedInVersion` records expanded pre-existing drugs separately from `addedInVersion`.

Reference half-life is distinct from renal/ESRF half-life and from duration of action or an extended-release dosing interval. Preserve the drug/analyte, route, population and Vd method. Do not convert L to L/kg without an appropriate patient weight or confuse plasma binding with erythrocyte binding. `not_reported` means absent from the checked source; `not_curated` means no field review; a guideline's `unknown` is its own evidence statement.

UKKA 2025 Appendix D (printed page 76) supplies selected ESRF and PD entries. Its half-life table does not consistently specify analyte/measurement method. Captopril's 21–32 h ESRF entry must not be treated as an experimentally matched estimate of free-parent half-life or used to derive a dose ratio. Ramipril is classed as dialysed in that table, while its SmPC describes ramiprilat as poorly removed and ramipril as slightly dialysable; the app records the difference. Nifedipine/verapamil product-label statements do not fill unknown HDF/high-flux evidence automatically.

The beta-blocker high-flux study (eight adults, crossover design) measured atenolol, metoprolol, bisoprolol and carvedilol. Recovery and arterial–venous clearance methods gave different results. Values in mL/min are not percentages of a dose removed. No RRT supplement is generated. CRRT/SLED removal remains uncurated and is not inferred from IHD, protein binding or Vd.

Captopril was promoted from catalog-only to a renal profile. The UK oral-solution table retains indexed CrCl units and **total daily** starting/maximal amounts, with frequency chosen separately; values are mg, not mL. Amlodipine now has a UK adult hypertension starting dose (5 mg daily) and maximum (10 mg daily), with no renal dose reduction. All other v0.3 modality records are retained.

## v0.6 source selection

Use REFERENCE_DIRECTORY.json and the in-app References view. BNF/labels support product-specific prescribing; professional guidelines and measured PK studies support renal decisions; institutional protocols retain their dialysis assumptions; ASN education and NKF patient pages provide context or safety information. An ERA directory listing is not evidence that every linked guideline has been reviewed. New cardiovascular renal tables cite the individual SmPCs, not a blanket ASN/ERA/NKF endorsement. No source type automatically establishes clinical approval.

## v0.7 supplied-reference rules

Use SOURCE_AUDIT.json for file hashes, edition dates, review scope and conflicts. PDF metadata is not a clinical revision date. Each imported numeric table has an individual source/page record; continued pages are retained. Handbook PK is historical and cannot establish a current dialysis replacement dose. Do not collapse “not dialysed” into measured zero clearance or carry conventional-HD conclusions into modern high-flux therapy. Categorical removal is not a numeric supplemental-dose recommendation. Read product route and analyte before using PK. The supplied PDFs remain research inputs outside the public package. Selected summaries are original condensations; full monographs are not republished.

## v0.8 eGFR calculator

The calculator is a separate tool, not a prescribing rule. Clinical data remain version 0.7.0. CKD-EPI 2021 creatinine is the default. MDRD is a legacy IDMS comparison without the original race multiplier, not a newly refitted race-free MDRD equation. Preserve visible equation/units, correct SI conversion and the difference between indexed eGFR, non-indexed GFR and Cockcroft–Gault CrCl. Do not transfer the result into a drug-dose threshold automatically. Optional Mosteller BSA estimates must not be confused with lean/adjusted dosing weight. Check quantified IDMS-standardized creatinine within the laboratory reportable range. Standard estimates are withheld for AKI/changing creatinine, dialysis, pregnancy and children. No CKD diagnosis or stage is assigned from one reading. Calculator entries clear on close and have no persistence or export. Formula/arithmetic checks are not independent clinical approval. See CALCULATOR.md and checks_calculator.mjs.
