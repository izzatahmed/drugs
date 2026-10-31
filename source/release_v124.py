"""v0.12.4: digoxin and the proton pump inhibitors completed from their current US labels.
Digoxin gets the label's maintenance-dose table by corrected CrCl and lean body weight, the loading dose,
target levels and dialysis statements. Omeprazole, esomeprazole, lansoprazole, pantoprazole, rabeprazole
and dexlansoprazole get CKD and haemodialysis statements and PK; vonoprazan gets PK and dialysis data.
Content: curation_v124.json (from make_curation_v124.py), quotes verified in label_quotes_v124.json.
"""
from pathlib import Path
import json, re, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-10-31'; VERSION = '0.12.4'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.12.3'
C = json.loads((R/'curation_v124.json').read_text()); Q = json.loads((R/'label_quotes_v124.json').read_text())
sources = {s['id']: s for s in data['sources']}; drugs = {d['id']: d for d in data['drugs']}
CORE = ['halfLife', 'renalHalfLife', 'volumeOfDistribution', 'proteinBinding']

def quoted(did, ev):
    assert any(ev in w for w in Q[did]['windows']), (did, ev[:80]); return ev

changed, promoted = [], []
for did, c in C.items():
    d = drugs[did]; m = Q[did]['meta']; sid = f'us124-{did}'
    sources[sid] = dict(id=sid, title=f"DailyMed · {m['brand']} ({m['manufacturer']})", url=m['url'],
        section=f"Current US FDA label: dosage and administration, renal impairment (8.6), clinical pharmacology (12.3) and overdosage. SPL version {m['splVersion']}, effective {m['effective']}; application {m['application']}.",
        type='US FDA label (DailyMed)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))
    for k, mod in c.get('modalities', {}).items():
        evs = [quoted(did, e) for e in mod.get('ev', [])]
        notes = mod['notes'] or ' '.join(f'US label: “{e}.”' for e in evs)
        d['modalities'][k] = dict(status=mod['status'], tables=mod['tables'], notes=notes,
                                  sourceIds=[sid] + [s for s in d['modalities'][k].get('sourceIds', []) if s != sid])
    p = d['pharmacokinetics']
    for k, f in c['pk'].items():
        fact = dict(status=f['status'], value=f['value'], context=f'US label: “{quoted(did, f["ev"])}.”', sourceIds=[sid], evidence=f['ev'] + '.')
        if k in CORE:
            if k == 'renalHalfLife': fact['basis'] = 'label_renal_impairment'
            p[k] = fact
        else: p['dialysability'][k] = fact
    for k in CORE:
        if p[k]['value'] is None and p[k]['status'] == 'not_curated': p[k]['context'] = 'Not stated in the current US label.'
    p.update(status='source_summary', sourceCheckedAt=DATE,
             notes='Values quoted from the current US label; the sentence behind each value is shown. Circuit clearance and dialysis supplements are not inferred from these values.')
    if not c.get('pk_only'):
        for k in ('kidneyMetric', 'summary', 'flag', 'considerations'):
            if k in c: d[k] = c[k]
        d['sourceIds'] = [sid] + [s for s in d.get('sourceIds', []) if s != sid]
        d['jurisdiction'] = 'US FDA label; check the JFDA-approved leaflet for products marketed in Jordan.'
        d['completeness'] = 'CKD and haemodialysis statements and PK from the current US label. PD and CRRT dosing are not stated in the label and are not inferred.'
        d['review']['sourceCheckedAt'] = DATE
        if c.get('promote'):
            d.update(entryType='renal', category='Gastrointestinal', formulation='Oral'); promoted.append(did)
    d['updatedInVersion'] = VERSION; changed.append(did)

cited = {s for x in re.findall(r'"sourceIds": \[(.*?)\]', json.dumps(data, ensure_ascii=False)) for s in re.findall(r'"([^"]+)"', x)}
data['sources'] = [s for s in sources.values() if not s['id'].startswith(('pk123-', 'us124-')) or s['id'] in cited]
data['coverage'] = {t: sum(1 for d in data['drugs'] if d['entryType'] == t) for t in ('renal', 'safety', 'catalog')}
pk = [d for d in data['drugs'] if d['pharmacokinetics']['status'] == 'source_summary']
full = [d for d in pk if all(d['pharmacokinetics'][k]['status'] == 'sourced' for k in ['halfLife', 'volumeOfDistribution', 'proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None]
data['pharmacokineticCoverage'] = dict(profiles=len(pk), allFourCoreFields=len(full))
data.update(version=VERSION, clinicalDataVersion=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=changed, newRenalIds=promoted, newPKIds=[], pirrtSummaryIds=[],
    note='Digoxin and the proton pump inhibitors completed from current US labels (dose tables, CKD/HD statements, PK).')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))

header = f'''# RenalRounds v{VERSION} · 31 October 2026

- **Digoxin:** the US label's once-daily maintenance-dose table by corrected CrCl (10–100 mL/min) and lean body weight (40–100 kg), with days to steady state; loading dose; target levels (efficacy falls below 0.5 ng/mL, toxicity rises above 2 ng/mL); not removed by dialysis, so no post-HD supplement. Source: LANOXIN tablets label.
- **Proton pump inhibitors** (omeprazole, esomeprazole, lansoprazole, pantoprazole, rabeprazole, dexlansoprazole): no renal dose adjustment at any level of kidney function and no removal by haemodialysis, each quoted from its current US label, plus half-life, protein binding and Vd where stated. Esomeprazole and lansoprazole are now full renal profiles.
- **Vonoprazan:** pharmacokinetics added; on dialysis, exposure is 1.3-fold and only 0.94% of the dose appears in dialysate.
- Coverage: {data['coverage']['renal']} renal profiles; PK {len(pk)} profiles ({len(full)} with all four core items). Drug content version {VERSION}.

'''
for target, base in [('CHANGELOG.md', 'changelog_v123.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v123.md'), ('SOURCE_AUDIT.md', 'source_audit_v123.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v124.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v124.py and apply_reviews.py. checks_v124.mjs proves only the eight curated entries changed, every quoted sentence is verbatim text of its stored label window, the digoxin table matches the label's Table 3 cell by cell, and every number in a PK value appears in its quote.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, changed=changed, promoted=promoted, coverage=data['coverage'], pk=data['pharmacokineticCoverage'])))
