"""Software-only release. Preserve every clinical field and its provenance."""
from pathlib import Path
import json

ROOT=Path(__file__).parent
path=ROOT/'dist/database.json'
data=json.loads(path.read_text())
data['version']='0.5.0'
data['softwareReleaseDate']='2026-10-29'
data['referenceScope']['newEntries']=0
data['referenceScope']['updatedEntries']=0
# Do not advance source dates or mark any record clinically approved.
path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
queue=[]
for d in data['drugs']:
    pk=d['pharmacokinetics']
    queue.append(dict(id=d['id'],name=d['name'],category=d['category'],routes=d['routes'],
        content=d['entryType'],renalDoseSourceCheckedAt=d['review']['sourceCheckedAt'],
        pkSourceCheckedAt=pk['sourceCheckedAt'],
        modalities={k:v['status'] for k,v in d['modalities'].items()},
        pkFields={k:pk[k]['status'] for k in ['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding']},
        removal={k:v['status'] for k,v in pk['dialysability'].items()},
        independentClinicalReview=d['review']['status'],
        priority='1: common rounds classes' if d['category'] in ['Cardiovascular','Antimicrobials','Diabetes & endocrine','Anticoagulation & haematology','Pain & neurology','OTC & medicine safety'] else '2: remaining formulary'))
(ROOT/'dist/CURATION_QUEUE.json').write_text(json.dumps(dict(version=data['version'],generatedAt='2026-10-29',
    note='Statuses describe curation coverage, not suitability for an individual patient. Summarized does not mean clinically approved or complete for every indication.',drugs=queue),ensure_ascii=False,indent=2))

intro='''## v0.5.0 — 29 October 2026

Software and completion-workflow release; clinical drug content and source-check dates are unchanged from v0.4.0.

- Bounded mobile result list, immediate open-result control, return-to-search button and keyboard dismissal.
- Cached name/alias search keys, direct drug lookup and explicit spelling suggestions that require selection.
- Modality filter for existing sourced summaries and an in-app completion dashboard.
- Scoped offline cache, visible cached release, explicit refresh/update controls; optional installation manifest.
- Drug-level completion queue, release plan, link sharing and print layout.

'''
p=ROOT/'dist/CHANGELOG.md';p.write_text('# Changelog\n\n'+intro+(ROOT/'clinical_changelog_v04.md').read_text())
(ROOT/'dist/COMPLETION_PLAN.md').write_text('''# RenalRounds completion plan — v0.5.0

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
''')
print('Prepared v0.5.0 and 668-row completion queue; clinical content unchanged')
