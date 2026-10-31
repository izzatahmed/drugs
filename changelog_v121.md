# RenalRounds v0.12.1 · 31 October 2026

- **Vancomycin, gentamicin, amikacin and tobramycin** now have numeric dosing: US label renal methods, Nebraska Medicine/UNMC renal and haemodialysis protocols (vancomycin: 20 mg/kg load, 750 mg after each session, adjusted by pre-dialysis level), and systemic PD doses.
- **PD peritonitis:** intraperitoneal doses from the ISPD 2022 guideline (Table 5) were added to the PD tab of 26 antibiotics, clearly labelled and separate from systemic PD doses.
- **Vonoprazan** (potassium-competitive acid blocker) added from its US label; searchable as "P-CAB".
- **Pregnancy and lactation:** a new section quotes the pregnancy and lactation statements of the cited label for 63 entries. The FDA retired the A/B/C/D/X letters; a letter appears only where the label still prints one.
- The back arrow is an icon in the lower-left corner again and hides while scrolling down.

## Earlier release record

# RenalRounds v0.12.0 · 30 October 2026

Primary jurisdictions are now the **US and Jordan**. Renal dose tables for 61 entries that were previously built from the Renal Drug Handbook (5th edition, 2018) have been rebuilt from current product labels: 55 from US FDA labels retrieved from DailyMed/openFDA and 6 from UK SmPCs (emc) for medicines with no US product (alfacalcidol, carbimazole, colecalciferol, domperidone, hyoscine butylbromide, vildagliptin). Each table shows its source country; every entry reminds readers to confirm against the JFDA-approved leaflet in Jordan.

- No handbook value remains in any dose table. Where a label gives no renal statement, the entry now says so (status "insufficient data in cited source") instead of carrying the handbook's advice.
- Notable changes from the handbook: flecainide now follows the US label (initial 100 mg once daily or 50 mg twice daily at CrCl ≤35 mL/min/1.73 m²; 100 mg every 12 hours in less severe disease); telavancin now shows the US label bands (Cockcroft–Gault with ideal body weight) with its boxed mortality warning; colecalciferol is contraindicated in severe renal impairment in the cited SmPC; repaglinide, midodrine, verapamil (bedtime ER), domperidone and vildagliptin carry label-specific starting doses.
- Pharmacokinetic panels still cite the handbook for some entries and will be rebuilt from labels in the next release.
- Each entry covers one product and route (named in the formulation line); other routes are marked as not covered.
- All entries remain pending independent nephrologist review.

## Earlier release record

# RenalRounds v0.11.3 · 30 October 2026

Software and wording release. No dose table, setting status or PK value changed; drug content remains 0.11.2.

- Kidney-function calculator now has two tabs: eGFR (CKD-EPI 2021 / legacy MDRD) and Cockcroft–Gault creatinine clearance with actual, ideal and adjusted body weight. Most drug tables in this reference are banded by CrCl.
- Phone layout: the floating back button no longer covers dose tables; on phones a "Back" button sits at the top of each drug. Pressing Enter in search opens the selected drug. The calculator scrolls to its result.
- Converted creatinine is shown to two decimals.
- 426 entries whose class only repeated the category now have a pharmacological class (e.g. flecainide: Class Ic antiarrhythmic). Search understands common abbreviations (PPI, NSAID, DOAC, LMWH, SGLT2i, ACEi, ARB, ESA and others).
- Internal working notes were rewritten as neutral statements (e.g. "BNF comparison not yet done").
- Each drug has a "Report an error" link that opens a pre-filled GitHub issue.
- Link previews (Open Graph) added.

## Earlier release record

# RenalRounds v0.11.2 · 30 October 2026

The top program title is a semantic Home link. It clears the query, selected drug, category/content/route/setting/OTC filters and returns to non-dialysis search at the top, closing open panels. Reader theme/font and favourites remain saved. The in-app back arrow can restore the previous browsing context; calculator values remain excluded and clear on close.

This batch adds 60 selected adult renal profiles from the supplied Renal Drug Handbook fifth edition (published 2018, copyright 2019). They cover cardiovascular, endocrine/steroid, phosphate/vitamin, respiratory, GI and common-medicine entries. There are 355 partial renal profiles, 28 shared safety notes and 285 catalog entries among 668 indexed medicines. 313 entries still lack a drug-specific renal profile. Existing current-label dosing and PK records are retained unchanged.

Edition/year appear at the point of each new dose table. The book GFR bands are not silently relabelled Cockcroft–Gault CrCl or indexed eGFR. Historical HD and HDF/high-flux categories remain separate; APD/CAPD is identified as a combined source category, not an intraperitoneal peritonitis protocol. Source CAV/VVHD rows have no delivered settings, so no universal modern CRRT regimen is assigned. SLED gaps remain explicit. No supplemental dose is calculated from a removal category.

The new profiles include numeric selected references and adjustments where support exists (e.g. flecainide oral initial total versus IV reduction, nicardipine IV titration, vildagliptin 50 mg/day, midodrine initial pre-HD weight bands with exact 70 kg unassigned, calcitriol micrograms, and selected oral/infusion regimens). Many drugs require no fixed renal reduction, while others require response/level-based titration. Three profiles withhold numeric renal selection: hydroxychloroquine, mesalazine and cholecalciferol, because their older/product-dependent guidance needs reconciliation.

Domperidone's older high-dose/prolonged schedules are excluded in favour of the directly retrieved MHRA adult dose/duration restrictions, alongside the handbook renal-frequency note. Aminophylline's continuation explains that the active theophylline is dialysable; the parent category is not a no-clearance rule. Vildagliptin and hydrocortisone preserve the differences between table categories and explanatory notes. Levothyroxine Vd and clopidogrel/hydroxychloroquine half-life fields are withheld where units/analytes need confirmation.

PK coverage is 157 source-summary profiles, of which 99 have all four core items (including qualified qualitative removal statements and historical data). A checked source can have missing parameters: partial panels leave those fields blank; calcium acetate has an explicit source-checked no-parameters-reported state and is not counted as a PK profile. Total L, L/kg, minutes, hours, days, parent and active-metabolite qualifications remain distinct.

Source metadata records exact supplied-PDF page, continuation pages, edition and original file checksum. The original PDF is not redistributed. Source check is not a new study, current product approval, completed BNF comparison or independent clinical sign-off. This remains a reference in development; verify current local products and obtain nephrology/renal-pharmacy review before clinical release.

Both cumulative and modified-file ZIPs include the same target release. The modified-file ZIP compares against the exact v0.10 cumulative package and includes intervening v0.11/v0.11.1 changes, including source paths. It can be overlaid on those retained packages; no original PDFs, credentials or preview files are distributed.

## Earlier release record

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

## Earlier releases · historical

# RenalRounds v0.10.0 · 30 October 2026

Search is the first visible control. Large titles, introductory paragraphs and coverage blocks have been removed from above it. A compact text-size / manual day-night / eGFR toolbar follows search. Filters start collapsed. Renal dosing leads each drug entry; PK and secondary copy/print/coverage tools follow it. Sources, coverage and offline-update details are below the findings. A small fixed ↶ button returns through in-app medicine/setting/search history; each dialog also has a back arrow that closes the panel. It never leaves the app. Calculator inputs are excluded from navigation history and still clear on close.

Day/night preference is saved independently of the system theme, with light as the first-use default. Text-size controls retain 100%, 115%, 130% and 150%. Enlarged tables stack on narrow phones. Favourites, theme and text size use browser-local preferences when storage is available; patient calculator inputs are not persisted.

This release adds 40 selected adult renal profiles and 3 product-information PK panels. The inventory remains 668 entries: 258 partial renal profiles, 28 shared safety notes and 382 catalog entries without renal guidance. There are 69 PK profiles; 55 contain all four core items, including qualitative IHD product statements where expressly qualified. These are not all measured modern circuit-clearance studies.

New additions include cardiovascular/diuretic/lipid drugs, 11 BPH/bladder agents, 6 allergy/respiratory agents and 8 GI/constipation agents. Some entries provide caution or insufficient-data guidance without numeric doses. Selected product labels/SmPCs were checked on 30 October; existing sources retain their original dates. BNF monograph reconciliation and independent clinical approval remain pending. All older drug regimens and PK panels are retained unchanged.

Key distinctions: perindopril erbumine versus arginine strengths and unassigned exact cutoffs; fenofibrate product-specific starting doses and dialysis contraindication; mirabegron indexed MDRD measure; indexed CLcr wording for solifenacin/tamsulosin; IR versus ER trospium/tolterodine/oxybutynin; tiotropium capsules for inhalation only; aluminium toxicity risk with sucralfate. No CKD table is copied into missing RRT modalities.

This remains incomplete: REMAINING_MEDICATIONS.json lists 410 entries without drug-specific renal profiles (382 catalog entries plus 28 shared safety notes). Existing renal profiles also retain indication, formulation and RRT gaps. No entry has independent clinical approval.

## Earlier releases · historical

# RenalRounds v0.9.0 · 29 October 2026

This cumulative release adds 85 selected adult renal profiles and 13 historical PK profiles. The 668-entry inventory now contains 218 partial renal profiles, 28 shared safety notes and 422 renal-dose-pending catalog entries. There are 66 PK profiles, 52 with all four core items. No independent clinical approval is recorded.

Readable text: default clinical text is 16 px. A− / percentage reset / A+ select 100%, 115%, 130% or 150%, including renal tables and PK values. The preference persists when browser storage is available. Old enlarged-text preferences migrate to 115%.

New guidance includes remaining selected anti-infectives, all 24 indexed psychiatry entries (selected renal statements only), warfarin, nebivolol, olmesartan, digoxin, selected diabetes agents, bone medicines and prucalopride. Exact route, product, indication, dose units, loading versus maintenance and renal measure remain visible. Some profiles contain monitoring, caution or insufficient-data statements rather than numeric doses.

The adult CKD-EPI 2021 / legacy MDRD calculator is retained. It does not select a drug dose; CrCl, indexed eGFR and non-indexed eGFR must not be interchanged automatically.

Source differences retained: minocycline oral daily limit versus institutional high dosing; IV posaconazole vehicle restriction; lamivudine label versus institutional practice; emtricitabine NIH/FDC-derived advice; dated EXBLIFEP measure ambiguity; VABOMERE historical MDRD equation. Paliperidone ER starting alternatives differ between products; only the linked label's table is selected.

This is not a completed formulary. REMAINING_MEDICATIONS.json lists 450 entries without drug-specific renal profiles, including 28 shared safety notes. Every renal profile also requires formulation/indication/RRT completion and independent nephrology plus renal-pharmacy review. Missing dialysis information is not extrapolated from CKD, another modality or PK. BNF monograph comparison remains pending.

## Earlier releases (historical)

# Changelog

## v0.8.0 — 29 October 2026

- Added an adult eGFR calculator accessible beside quick search and in the sidebar. Race-free CKD-EPI 2021 creatinine is the default; IDMS MDRD is labelled legacy with its historical race multiplier omitted.
- Added mg/dL and µmol/L inputs with automatic value conversion when the unit changes; estimates update as inputs change. Values are not capped at 60 or 90.
- Optional height/weight produces Mosteller BSA and non-indexed eGFR in mL/min, separately labelled from mL/min/1.73 m². This is not a CrCl calculator and selects no medicine dose.
- Invalid/incomplete entries remove any previous estimate. No result is produced for children, AKI/changing creatinine, dialysis or pregnancy. Calculator values clear on close and are not stored, exported or transmitted.
- Verified CKD-EPI arithmetic against NKF Table S1 reference cases; added legacy MDRD and BSA arithmetic, unit-equivalence and validation checks.
- All 668 drug records, 241 existing drug/source records, PK, doses, conflicts and review states are unchanged from clinical-data version 0.7.0. Software version 0.8.0 does not imply clinical approval.

# Changelog

## v0.7.0 — 29 October 2026

- Reviewed selected sections of five supplied references; original PDFs are not redistributed.
- Promoted 20 existing catalog entries to selected adult renal profiles: acyclovir, amphotericin-b-deoxycholate, aztreonam, cefadroxil, cefdinir, cefoxitin, cefpodoxime, ceftaroline, cefuroxime, clarithromycin, ethambutol, famciclovir, flucytosine, fosfomycin, ganciclovir, liposomal-amphotericin-b, phenoxymethylpenicillin, tigecycline, valganciclovir, voriconazole.
- Added 26 historical fifth-edition handbook PK/removal summaries with individual PDF page locators and visible 2018 (©2019) labels. Modern high-flux removal and continuous therapies are not inferred from historical conventional-HD categories.
- Added 16 prescription-specific PIRRT summaries and four CVVHD profiles. Retained session/flow assumptions, indication, infusion and dose timing. Existing CKD/IHD/PD/CRRT tables on previously curated renal entries are unchanged.
- Retained six source disagreements/ambiguities, including oral cefuroxime label intervals, clarithromycin PD, flucytosine PD timing, valganciclovir formulation/analyte issues, levofloxacin PIRRT and piperacillin/tazobactam PD removal.
- 668 indexed entries: 133 renal profiles, 28 shared safety notes and 507 renal-dose-pending catalog records. 53 PK profiles; 40 contain all four core items.
- These are selected source summaries. Independent clinical approval and BNF monograph reconciliation remain pending.

# Changelog

## v0.6.0 — 29 October 2026

- Corrected the reference clarification: BNF means British National Formulary. No separate PNF reference remains requested; BNF monograph reconciliation is still pending access.
- Expanded 12 existing catalog entries: bisoprolol, candesartan, clonidine, enalapril, hydralazine, indapamide, irbesartan, losartan, methyldopa, ramipril, telmisartan and valsartan. They are source-based drafts, not independently approved monographs.
- 113 renal profiles, 28 shared safety notes and 527 renal-dose-pending catalog records; total remains 668. PK coverage remains 27 profiles, with 15 having four core PK items.
- Added explicit HD advice where supplied by the cited label. No new PD, CRRT or SLED regimen was inferred. Clonidine, hydralazine and methyldopa retain nonnumeric renal guidance where the label gives no fixed regimen.
- Kept indication/route differences, source cutoff gaps and initial-versus-maximum daily amounts visible. Existing drug/PK data outside the 12 promoted entries are unchanged.
- Added a role-labelled directory of BNF, KDIGO, ASN, ERA, NKF, UKKA, UCSF and product-information resources. Portal discovery and patient education are distinguished from drug-specific prescribing evidence.

# Changelog

## v0.5.0 — 29 October 2026

Software and completion-workflow release; clinical drug content and source-check dates are unchanged from v0.4.0.

- Bounded mobile result list, immediate open-result control, return-to-search button and keyboard dismissal.
- Cached name/alias search keys, direct drug lookup and explicit spelling suggestions that require selection.
- Modality filter for existing sourced summaries and an in-app completion dashboard.
- Scoped offline cache, visible cached release, explicit refresh/update controls; optional installation manifest.
- Drug-level completion queue, release plan, link sharing and print layout.

# RenalRounds release 0.4.0

29 October 2026

- Expanded captopril from a catalog placeholder to a sourced renal profile, keeping UK daily totals, source-native units, formulation and RRT limits explicit. Expanded amlodipine with an adult hypertension starting dose and maximum.
- Added PK schema fields to every record, with sourced summaries for 27 BP/cardiovascular medicines. Fifteen have reference half-life, Vd, binding and an IHD removal statement; other fields have explicit gaps.
- Separated reference/ESRF half-life, parent/metabolite, Vss/apparent distribution volume, plasma/erythrocyte binding and IHD/PD/CRRT/SLED removal. Preserved source-specific evidence and differences.
- Added PK available filtering, updated-record browsing, quick searches for captopril/amlodipine and recovery of exact name matches hidden by active filters.
- 668 indexed records remain: 101 renal profiles, 28 shared safety notes, 539 dose-pending catalog entries. Only captopril/amlodipine modality content changed since v0.3; all original 70 profiles remain unchanged.
- No independent clinical sign-off, automatic prescribing or complete PK coverage is claimed. No GitHub account upload was performed.

---

# RenalRounds release 0.3.0

29 October 2026

668 indexed drugs/formulations: 100 sourced renal profiles, 28 shared safety-note entries and 540 catalog-only entries. All clinical approval remains pending. This is an expanding inventory, not a complete prescribing formulary.

- Added 30 renal profiles covering selected antimicrobials, antihistamines, GI, cardiovascular, lipid, transplant and calcimimetic medicines. Some give adjustment or monitoring guidance without numeric dosing.
- Added shared kidney-safety guidance for common OTC products and selected systemic NSAIDs. No renal or RRT dose is inferred from these class notes.
- Added a broad provisional inventory across hospital and ambulatory classes, including oral, parenteral, topical, inhaled and other routes. Catalog entries have empty clinical sources, a null clinical source-check date and no dose tables.
- Added combined route, content-type, category and OTC filters; exact generic/alias matches rank first. Results display their content type.
- Bundled all assets and data into a self-contained index.html, including local JSON/editorial-document exports. Added a root-level GitHub Pages package and setup instructions.
- Preserved all previous 70 profiles’ modality records, source distinctions, restrictions and draft status.
- No PNF comparison is claimed because the title/edition is unidentified. BNF monograph reconciliation remains pending; only linked PDR monographs are represented as consulted.

Software checks do not constitute clinical validation. The catalog is not a claim of worldwide product availability or all-formulation completeness.

---

# RenalRounds release 0.2.0

29 October 2026

70 adult monographs: the original 30 plus 40 additions. All remain draft, with independent nephrology and renal-pharmacy approval pending.

## What was added

- Diabetes: dapagliflozin, canagliflozin, ertugliflozin, semaglutide (Ozempic injection), tirzepatide, dulaglutide, liraglutide (Victoza), exenatide (immediate release), saxagliptin and alogliptin.
- Cardiovascular: sacubitril/valsartan, lisinopril, atenolol, spironolactone and eplerenone.
- Anticoagulation: rivaroxaban, dabigatran and edoxaban, with indication and jurisdiction restrictions.
- Neurology/pain: duloxetine, immediate-release tramadol and immediate-release levetiracetam.
- Gout: colchicine and febuxostat.
- Antimicrobials: nirmatrelvir/ritonavir, cefiderocol and ceftazidime/avibactam.
- Specialist kidney therapies: finerenone, sparsentan, atrasentan, voclosporin, difelikefalin and IgAN-targeted-release budesonide.
- Dialysis anaemia: vadadustat and historical US daprodustat.
- Electrolytes/phosphate: tenapanor (Xphozah), patiromer, sodium zirconium cyclosilicate, sevelamer carbonate, sucroferric oxyhydroxide and ferric citrate.

These are additions to this database, not a list of 40 new regulatory approvals. The drugs are not all authorised or marketed in the same jurisdictions.

## Reference and clinical distinctions

- BNF 92 (September 2026) was confirmed from the publisher's listing. Its monographs were inaccessible, so **no drug is claimed to have completed BNF comparison**. UK SmPC content is identified as UK SmPC content.
- PDR is treated as a continuously updated digital reference. The source list identifies exactly which monographs were consulted. Finerenone's October 2026 PDR bulletin was checked against its September 2026 US label; this is recorded separately from a PDR monograph comparison.
- Paxlovid's checked US information contains a severe-renal-impairment/HD 5-day course. All active-ingredient amounts and dialysis timing are explicit; major interaction screening remains necessary.
- Finerenone starting and target doses are separated, including distinct US CKD and HF targets. Full indication-specific potassium/eGFR adjustment tables remain linked.
- Dapagliflozin UK product and US PDR initiation rules remain separate. Dabigatran's US severe-CKD AF advice is not transferred to UK prescribing.
- Cefiderocol has its own label-based CRRT effluent-flow table, separate from UCSF CVVHD assumptions.
- GSK's US Jesduvroq discontinuation is prominently flagged. A surviving label is not evidence of current commercial availability.
- The original 30 dosing tables were retained. This expansion does not imply a full re-review of those monographs against BNF/PDR.

## Application changes

- “New in v0.2” filter and per-entry markers.
- Dynamic counts, exported version and modality coverage.
- Reference-comparison record for every monograph.
- Explicit “not indicated in curated label” status, distinct from contraindication and missing data.
- Source-specific dialysis assumptions rather than applying an antimicrobial-category assumption to all drugs.

## Still pending

Full BNF reconciliation; complete formulation/indication coverage; most PD protocols; all SLED protocols; many prescription-specific CRRT protocols; complete interaction and safety monographs; independent clinical sign-off. This release is not a standalone bedside prescribing authority.
