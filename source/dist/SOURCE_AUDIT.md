# RenalRounds v0.11.1 · 30 October 2026

This update prioritises renal instructions rather than search names or PK alone. It adds 35 selected product-specific renal profiles from official DailyMed SPLs, fills 17 previously empty systemic PD schedules from the supplied Nebraska protocol approved April 2026, and reconciles eight IHD-removal fields to the selected labels. It retains all previously populated dosing tables and all PK half-life/Vd/binding fields. There are 295 partial renal profiles, 28 shared safety entries and 345 catalog entries in the 668-medicine index. PK remains 99 profiles; 63 have all four core items, including qualified label statements and historical values.

Numeric additions include entecavir by indication/renal function/HD/CAPD, IR amantadine weekly HD, ropinirole HD by indication, adult lacosamide renal maximum and a qualified HD supplement, oxcarbazepine initial TOTAL daily dose, topiramate indexed-CrCl reduction, memantine IR target, sulbactam/durlobactam and imipenem/cilastatin/relebactam combination regimens, delafloxacin route-specific adjustment, ofloxacin and trimethoprim. Other labels specify titration or insufficient evidence rather than a safe universal numeric dose. Three new profiles withhold numeric selection because of study gaps or conflicting warnings (buprenorphine patch, lorazepam injection, cefixime product table).

Sources: search retrieval failed, but 35 selected SPLs were retrieved directly through the official DailyMed API. Source metadata records exact set ID, publication date, SPL version, retrieval endpoint and XML SHA-256. DailyMed presence is not FDA approval: phenobarbital's selected label is a marketed unapproved drug; molnupiravir is an EUA fact sheet, not full approval. BNF comparison and independent clinical approval remain pending. The supplied handbook's 2018 PK values retain their historical status. No old handbook renal-dose table is promoted into current prescribing.

PD tables describe systemic treatment, not intraperitoneal peritonitis prescriptions. CAPD does not establish APD dosing. Indications, formulation, residual function, susceptibility and institutional protocol differences remain material. Current removal evidence does not automatically establish a maintenance or replacement dose. No unlisted CRRT or SLED regimen is inferred.

The top centre now displays RenalRounds v0.11.1, with the existing compact font/theme controls retained. The cumulative package contains everything needed after v0.10. The smaller package contains only files changed or added since the exact v0.10 archive; apply it preserving paths. Both lead to the same release. No deployment or GitHub write is performed by downloading.

373 entries still lack drug-specific renal profiles; existing profiles also retain substantial gaps. This remains a draft, not a completed formulary or approved clinical decision system.

## Earlier release record

# RenalRounds v0.11.0 · 30 October 2026

The upper area is reduced to two compact rows: smaller text/theme/eGFR controls first, then a 40-px search field with Filters and Clear filters beside it. Filter actions use icons on narrow phones and visible labels on larger screens. Clear filters is disabled when no filter is active and does not erase the search query. Filter details remain collapsed until opened. Clinical-review badges and informational missing-data notices follow the clinical findings; explicit do-not-use warnings remain with their relevant setting.

The manual day/night choice, text-size preference, calculator and in-app semicircular back arrows are retained. Clinical text size remains readable and can increase independently of the compact controls.

Medication information is expanded for 32 records: two partial adult institutional renal profiles (omadacycline and telavancin), plus 30 historical PK-only panels in pain/neurology. The 668-entry inventory now has 260 partial renal profiles, 28 shared safety notes and 380 renal-dose-pending catalog entries. There are 99 PK panels; 55 have all four core items. Thirty new panels contain half-life, Vd and binding; their dialysis removal and dose schedules remain uncurated.

Online primary-source search and retrieval were unavailable during this batch. No new current product-label verification is claimed. The renal additions use the supplied institutional protocol approved April 2026; the PK additions use selected supplied fifth-edition handbook tables published in 2018 (copyright 2019). Historical reference numbers are distinguished from numeric values, and total Litres from L/kg. No historical renal-dose table or new dialysis-removal category is imported. Telavancin's current label, indication and jurisdiction need reconciliation; its numeric renal regimen is withheld.

Coverage remains incomplete. REMAINING_MEDICATIONS.json lists 408 records without a drug-specific renal profile (380 catalog entries plus 28 shared safety notes). PK availability does not establish a dose. Existing renal profiles also retain formulation/indication/RRT gaps. Independent clinical approval and BNF monograph reconciliation remain pending.

## New historical PK page locators

- Morphine: PDF p695, printed p676.
- Hydromorphone: PDF p515, printed p496.
- Oxycodone: PDF p774, printed p755.
- Fentanyl: PDF p438, printed p419.
- Buprenorphine: PDF p166, printed p147.
- Codeine: PDF p267, printed p248.
- Pethidine / meperidine: PDF p811, printed p792.
- Methadone: PDF p660, printed p641.
- Lacosamide: PDF p585, printed p566.
- Lamotrigine: PDF p588, printed p569.
- Oxcarbazepine: PDF p771, printed p752.
- Topiramate: PDF p1036, printed p1017.
- Carbamazepine: PDF p187, printed p168.
- Phenytoin: PDF p819, printed p800.
- Valproate: PDF p950, printed p931.
- Pramipexole: PDF p839, printed p820.
- Ropinirole: PDF p915, printed p896.
- Amantadine: PDF p67, printed p48.
- Memantine: PDF p648, printed p629.
- Donepezil: PDF p354, printed p335.
- Rivastigmine: PDF p911, printed p892.
- Clonazepam: PDF p251, printed p232.
- Lorazepam: PDF p628, printed p609.
- Midazolam: PDF p676, printed p657.
- Diazepam: PDF p333, printed p314.
- Tizanidine: PDF p1027, printed p1008.
- Phenobarbital: PDF p814, printed p795.
- Brivaracetam: PDF p160, printed p141.
- Ketamine: PDF p572, printed p553.
- Sumatriptan: PDF p972, printed p953.

## Previous audit

# RenalRounds v0.10.0 · 30 October 2026

Search is the first visible control. Large titles, introductory paragraphs and coverage blocks have been removed from above it. A compact text-size / manual day-night / eGFR toolbar follows search. Filters start collapsed. Renal dosing leads each drug entry; PK and secondary copy/print/coverage tools follow it. Sources, coverage and offline-update details are below the findings. A small fixed ↶ button returns through in-app medicine/setting/search history; each dialog also has a back arrow that closes the panel. It never leaves the app. Calculator inputs are excluded from navigation history and still clear on close.

Day/night preference is saved independently of the system theme, with light as the first-use default. Text-size controls retain 100%, 115%, 130% and 150%. Enlarged tables stack on narrow phones. Favourites, theme and text size use browser-local preferences when storage is available; patient calculator inputs are not persisted.

This release adds 40 selected adult renal profiles and 3 product-information PK panels. The inventory remains 668 entries: 258 partial renal profiles, 28 shared safety notes and 382 catalog entries without renal guidance. There are 69 PK profiles; 55 contain all four core items, including qualitative IHD product statements where expressly qualified. These are not all measured modern circuit-clearance studies.

New additions include cardiovascular/diuretic/lipid drugs, 11 BPH/bladder agents, 6 allergy/respiratory agents and 8 GI/constipation agents. Some entries provide caution or insufficient-data guidance without numeric doses. Selected product labels/SmPCs were checked on 30 October; existing sources retain their original dates. BNF monograph reconciliation and independent clinical approval remain pending. All older drug regimens and PK panels are retained unchanged.

Key distinctions: perindopril erbumine versus arginine strengths and unassigned exact cutoffs; fenofibrate product-specific starting doses and dialysis contraindication; mirabegron indexed MDRD measure; indexed CLcr wording for solifenacin/tamsulosin; IR versus ER trospium/tolterodine/oxybutynin; tiotropium capsules for inhalation only; aluminium toxicity risk with sucralfate. No CKD table is copied into missing RRT modalities.

This remains incomplete: REMAINING_MEDICATIONS.json lists 410 entries without drug-specific renal profiles (382 catalog entries plus 28 shared safety notes). Existing renal profiles also retain indication, formulation and RRT gaps. No entry has independent clinical approval.

## v0.10 selected source IDs

- v10-alfuzosin: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f2f42c98-4118-5f70-e053-2a95a90add02
- v10-amiloride: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2b70cf0c-45be-428f-b396-5001ed4e30fc
- v10-bumetanide: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=551918e1-96c4-453a-870c-61b282882206
- v10-chlorthalidone: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d07eea8b-361b-486a-a572-3bf4a257f431
- v10-desloratadine: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0fe374d0-c14b-4102-b568-eb79165fc7ef
- v10-dexlansoprazole: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=fc3de800-bfad-4e2f-b664-d58a67550b2f
- v10-diltiazem: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=73b3607a-99d0-44d8-92ef-0074684c9d7d
- v10-doxazosin: https://www.medicines.org.uk/emc/product/3421/smpc
- v10-dutasteride: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=468df1b8-1f82-4328-a549-0a716ad1266d
- v10-felodipine: https://www.medicines.org.uk/emc/product/11604/smpc
- v10-fenofibrate: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9cc2038d-750e-42dc-b818-c5642cf6a5ad
- v10-finasteride: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=77589cc3-c440-4695-800c-82a0e5128a6c
- v10-gemfibrozil: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=b8bb442e-66dc-435e-830c-4ba3daa47c04
- v10-hydroxyzine: https://www.medicines.org.uk/emc/product/101010/smpc
- v10-labetalol: https://www.medicines.org.uk/emc/product/2647/smpc
- v10-lactulose: https://www.medicines.org.uk/emc/product/2796/smpc
- v10-levocetirizine: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=60ae7e0e-281c-40a3-a0d3-259b843ddaaa
- v10-linaclotide: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=09beda19-56d6-4a56-afdc-9a77b70b2ef3
- v10-lubiprostone: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5fd683a5-87ff-42b8-a8c8-fff81625f67f
- v10-macrogol-polyethylene-glycol: https://www.medicines.org.uk/emc/product/257/smpc
- v10-mirabegron: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=b71b939e-8cb1-492c-8311-28f75dc4c682
- v10-montelukast: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=97cc4e1e-e0fd-4bb5-8f9e-b8573f5230e5
- v10-nifedipine: https://www.medicines.org.uk/emc/product/3367/smpc
- v10-oxybutynin: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7db4ab81-b379-4a6d-b469-95eb9e184b56
- v10-pantoprazole: https://www.medicines.org.uk/emc/product/14643/smpc
- v10-perindopril: https://www.medicines.org.uk/emc/product/14520/smpc
- v10-pitavastatin: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=0f11ee80-871e-4f13-e063-6394a90af19d
- v10-propranolol: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1791ef4d-b609-41c8-b4ef-15bff752ddd7
- v10-rabeprazole: https://www.medicines.org.uk/emc/product/14539/smpc
- v10-roflumilast: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=30dd6eae-6435-cae1-e063-6294a90a003b
- v10-silodosin: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=aac3314b-af8c-400e-ba91-0cf2b95e70dd
- v10-simvastatin: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f94e5e28-f0b1-700a-e053-6394a90adb7b
- v10-solifenacin: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f0b8f111-1d76-4b04-9e2f-9fca9e5a0b00
- v10-sucralfate: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=cd25eb96-29ea-48b2-bdee-c2ea98f216b8
- v10-tamsulosin: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a242c8dc-576e-4a1f-a9e7-a05d7ebc0e0a
- v10-tiotropium: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=496b38ee-45b6-4bb2-a35e-9023c3b73719
- v10-tolterodine: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=fd6c8b3d-a52a-4418-aa9c-0297db6c0807
- v10-torsemide: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a6055317-8826-df85-e053-2a95a90a5378
- v10-trospium: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=801f2143-6816-4f34-b65d-16bb2cf07975
- v10-vibegron: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=25f21d25-14f8-4fda-91f6-7aa8b68aa1c8

## Prior source audit

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
