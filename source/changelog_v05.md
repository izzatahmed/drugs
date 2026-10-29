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
