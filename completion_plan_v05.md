# RenalRounds completion plan — v0.5.0

The software is functional; the clinical formulary is incomplete. This release adds no clinical claims or dosing regimens. All 668 entries still await independent clinical approval. Use CURATION_QUEUE.json or the in-app Completion dashboard to track each field separately.

## Current scope

- 668 searchable drug/formulation entries; 101 renal profiles, 28 shared safety notes and 539 renal-dose-pending catalog records.
- 27 PK profiles; 15 include all four core items (reference half-life, Vd, binding and an IHD-removal statement).
- Some existing renal profiles contain monitoring guidance rather than numeric doses. A summarized modality does not cover every indication or prescription.
- PD, CRRT and SLED coverage is incomplete. No dosing is extrapolated from other modalities or PK parameters.

## Completion sequence

1. Agree the adult local formulary and routes; prioritize cardiovascular drugs, antimicrobials, anticoagulants, diabetes medicines, analgesics and OTC products.
2. For each formulation/indication, curate the licensed standard regimen and CKD source bands with the exact function measure, units, boundaries and maximum dose. Separate loading from maintenance doses.
3. Curate IHD, PD, CRRT and SLED independently. Record membrane, session length, timing, supplement evidence, CRRT modality/effluent and residual kidney function. Preserve source disagreement.
4. Complete half-life (analyte and population), Vd (L versus L/kg and method), protein binding and measured or explicitly qualified removal. Record not reported/unknown when evidence does not supply a value.
5. Reconcile licensed references. Identify the requested PNF title and edition; obtain authorized monograph access for PNF/BNF/PDR as appropriate. No licensed-reference comparison may be claimed without actual access.
6. Record an independent nephrologist and renal-pharmacist review, reviewer identity, date and reconciled source version. Resolve every high-risk discrepancy before approving that monograph.
7. Recheck the priority formulary on a defined schedule and after label/safety updates. Archive releases and retain field-level source provenance.

## Release gates

Clinical release requires approved entries covering the agreed local formulary, explicit unresolved gaps, reviewed renal/RRT regimens and documented ownership of source updates. A larger searchable catalog alone does not satisfy these gates. v0.5.0 passes software/data checks only.

## Upload and mobile acceptance

Upload all root files from the cumulative ZIP to the existing drugs repository. Preserve index.html, sw.js, manifest.webmanifest, icon.svg and .nojekyll together. Refresh the site, check v0.5.0 in the header, wait for Offline ready, then test an airplane-mode reopen on a real phone. Check captopril, amlodipine, brand search, favourites and the selected RRT tab. Source links require internet. Updating cached data never counts as a new clinical source check.
