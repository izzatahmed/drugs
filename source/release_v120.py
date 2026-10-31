"""v0.12.0: replace handbook-derived renal dosing for 61 entries with current product labels.

US FDA labels (DailyMed) are the primary source; UK SmPCs (emc) are used only where no US product
exists. Pharmacokinetic panels are not changed here (rebuilt in the next release).
"""
from pathlib import Path
import json, importlib.util, sys
sys.dont_write_bytecode = True  # keep the published repository free of __pycache__

R = Path(__file__).parent; D = R/'dist'
DATE = '2026-10-30'; VERSION = '0.12.0'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.11.3'
spec = importlib.util.spec_from_file_location('rebuild', R/'label_rebuild_v120.py'); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
meta = json.loads((R/'label_meta_v120.json').read_text())
drugs = {d['id']: d for d in data['drugs']}; sources = {s['id']: s for s in data['sources']}
HANDBOOK = lambda i: i.startswith('rdh5')

JORDAN = 'Jordan: confirm against the JFDA-approved leaflet of the product dispensed.'
def add_source(i, m, name):
    if m['kind'] == 'US':
        sid = f'us120-{i}'
        sources[sid] = dict(id=sid, title=f"DailyMed · {m['brand'] or name} ({m['manufacturer']})", url=m['url'],
            section=f"Current US FDA label: dosage and administration, use in specific populations (renal impairment), clinical pharmacology and overdosage. SPL version {m['splVersion']}, effective {m['effective']}; application {m['application']}.",
            type='US FDA label (DailyMed)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))
        return [sid]
    out = []
    for k, x in [('', m)] + ([('-inj', m['extra'])] if 'extra' in m else []):
        sid = f'uk120-{i}{k}'
        sources[sid] = dict(id=sid, title=f"emc · {x['title']}", url=x['url'],
            section=f"UK Summary of Product Characteristics: sections 4.2, 4.3, 4.4 and 5.2. Last updated on emc {x['emcUpdated']}. No US-marketed product; used as the closest regulator-approved source for Jordan-registered products.",
            type='UK SmPC (emc)', accessed=DATE)
        out.append(sid)
    return out

changed = []
for i, e in mod.R.items():
    d = drugs[i]; m = meta[i]; sids = add_source(i, m, d['name'])
    keep = [s for s in d['sourceIds'] if not HANDBOOK(s) and s != 'nm11-telavancin']
    def modality(x):
        out = dict(status=x['status'], tables=x['tables'], notes=x['notes'], sourceIds=[] if x['status'] == 'not_curated' else list(sids))
        if i == 'domperidone' and x['status'] != 'not_curated': out['sourceIds'] += ['mhra-domperidone-v112']
        return out
    d['modalities'] = dict(ckd=modality(e['ckd']), ihd=modality(e['ihd']), crrt=modality(e['crrt']), pd=modality(e['pd']),
                           sled=dict(status='not_curated', tables=[], notes=mod.NC, sourceIds=[]))
    d.update(kidneyMetric=e['kidneyMetric'], summary=e['summary'], flag=e['flag'], formulation=e['formulation'], considerations=e['considerations'],
             sourceIds=sids + keep, updatedInVersion=VERSION,
             jurisdiction=('US FDA label. ' if m['kind'] == 'US' else 'UK SmPC (no US product). ') + JORDAN,
             completeness='Renal statements from the cited current label only. Other formulations, indications and dialysis settings are not covered; the pharmacokinetic panel is still being rebuilt from labels.')
    d['review'] = dict(status='clinical_review_pending', sourceCheckedAt=DATE, clinicalReviewer=None, clinicalApprovedAt=None)
    for k in ['handbookSource', 'doseEvidence', 'evidenceNotes']: d.pop(k, None)
    assert not any(HANDBOOK(s) for mo in d['modalities'].values() for s in mo['sourceIds']), i
    changed.append(i)

# Conflicts and directory text that described the handbook as a dose source.
data['sourceConflicts'] = [c for c in data['sourceConflicts'] if c['drug'] not in changed or 'handbook' not in json.dumps(c).lower()]
for r in data['referenceResources']:
    if r['id'] == 'upload-0':
        r.update(role='Historical reference being replaced',
                 use='No longer used for dose tables. Some pharmacokinetic values still cite it and are being rebuilt from current labels.',
                 access='Cited by page number; the original document is not redistributed.')
data['researchLimitations'] = dict(onlinePrimarySourceLookup='Labels retrieved directly from openFDA/DailyMed (US) and emc (UK) on 30 October 2026.',
    scope='Primary jurisdictions: US and Jordan. US FDA labels first; UK SmPCs only where no US product exists. Jordan-registered leaflets (JFDA) were not directly checked.')
data['referenceScope']['primaryJurisdictions'] = ['US', 'Jordan']

# Drop sources that nothing references any more.
used = {s for d in data['drugs'] for s in d['sourceIds']} | {s for d in data['drugs'] for m in d['modalities'].values() for s in m['sourceIds']}
def pk_ids(p):
    out = set()
    for k, v in p.items():
        if isinstance(v, dict):
            out |= set(v.get('sourceIds', [])); out |= pk_ids(v)
    return out
for d in data['drugs']: used |= pk_ids(d['pharmacokinetics'])
for g in data['sharedGuidance'].values(): used |= set(g['sourceIds'])
used |= set(data.get('drugStewardship', {}).get('sourceIds', []))
used |= {s for c in data['sourceConflicts'] for s in c.get('sourceIds', [])}
txt = json.dumps({k: v for k, v in data.items() if k not in ('sources', 'drugs')})
data['sources'] = [s for s in sources.values() if s['id'] in used or s['id'] in txt]

data.update(version=VERSION, clinicalDataVersion=VERSION, softwareReleaseDate=DATE)
data['clinicalUpdates'] = dict(version=VERSION, changedIds=changed, newRenalIds=[], newPKIds=[], newPDIds=[],
    scope='Renal dose tables for 61 entries rebuilt from current US FDA labels (55) or UK SmPCs (6), replacing the 2018 handbook.')
data['releaseChanges'] = dict(version=VERSION, changedIds=changed, newRenalIds=[], newPKIds=[], pirrtSummaryIds=[],
    note='Dose tables rebuilt from current labels; PK panels unchanged in this release.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
(D/'REFERENCE_DIRECTORY.json').write_text(json.dumps(data['referenceResources'], ensure_ascii=False, indent=2))
queue = json.loads((D/'CURATION_QUEUE.json').read_text()); queue['version'] = VERSION
for q in queue['drugs']:
    if q['id'] in changed: q['modalities'] = {k: m['status'] for k, m in drugs[q['id']]['modalities'].items()}
(D/'CURATION_QUEUE.json').write_text(json.dumps(queue, ensure_ascii=False, indent=2))
rem = json.loads((D/'REMAINING_MEDICATIONS.json').read_text()); rem['version'] = VERSION
(D/'REMAINING_MEDICATIONS.json').write_text(json.dumps(rem, ensure_ascii=False, indent=2))

us = sum(meta[i]['kind'] == 'US' for i in changed)
header = f'''# RenalRounds v{VERSION} · 30 October 2026

Primary jurisdictions are now the **US and Jordan**. Renal dose tables for {len(changed)} entries that were previously built from the Renal Drug Handbook (5th edition, 2018) have been rebuilt from current product labels: {us} from US FDA labels retrieved from DailyMed/openFDA and {len(changed)-us} from UK SmPCs (emc) for medicines with no US product (alfacalcidol, carbimazole, colecalciferol, domperidone, hyoscine butylbromide, vildagliptin). Each table shows its source country; every entry reminds readers to confirm against the JFDA-approved leaflet in Jordan.

- No handbook value remains in any dose table. Where a label gives no renal statement, the entry now says so (status "insufficient data in cited source") instead of carrying the handbook's advice.
- Notable changes from the handbook: flecainide now follows the US label (initial 100 mg once daily or 50 mg twice daily at CrCl ≤35 mL/min/1.73 m²; 100 mg every 12 hours in less severe disease); telavancin now shows the US label bands (Cockcroft–Gault with ideal body weight) with its boxed mortality warning; colecalciferol is contraindicated in severe renal impairment in the cited SmPC; repaglinide, midodrine, verapamil (bedtime ER), domperidone and vildagliptin carry label-specific starting doses.
- Pharmacokinetic panels still cite the handbook for some entries and will be rebuilt from labels in the next release.
- Each entry covers one product and route (named in the formulation line); other routes are marked as not covered.
- All entries remain pending independent nephrologist review.

'''
for target, base in [('CHANGELOG.md', 'changelog_v113.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v113.md'), ('SOURCE_AUDIT.md', 'source_audit_v113.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'COMPLETION_PLAN.md').write_text(header + '## Remaining clinical work\n\nRebuild the remaining handbook-cited pharmacokinetic values from current labels; nephrologist review of every entry using the review sheet; renal profiles for the 285 catalog-only entries, prioritised by risk; dialysis-setting coverage (CRRT, SLED, PD); JFDA leaflet checks for products used in Jordan.\n')
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v120.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v120.py. checks_v120.mjs proves no dose table cites the handbook, every rebuilt entry cites a retrieved label with set ID/version or emc product ID, entries outside the 61 are unchanged from v0.11.3, and runs the service-worker contract for {VERSION}.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, rebuilt=len(changed), us=us, uk=len(changed)-us, sources=len(data['sources']))))
