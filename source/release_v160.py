"""v0.16.0: 42 medicines added to the inventory (oncology, anaesthesia & critical care, contrast media and others) and three catalog entries completed from current US labels
(curation_v160.json, quotes verified in label_quotes_v160.json). Catalog entries become renal profiles with label dosing; existing profiles gain PK and
dialysis statements. Existing curated content is never overwritten: a setting
is filled only where it was "not curated", and a PK field only where it was blank.
"""
from pathlib import Path
import copy, json, re, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-01'; VERSION = '0.16.0'; TAG = 'us160'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.15.0'
C = json.loads((R/'curation_v160.json').read_text()); Q = json.loads((R/'label_quotes_v160.json').read_text())
sources = {s['id']: s for s in data['sources']}; drugs = {d['id']: d for d in data['drugs']}
CORE = ['halfLife', 'renalHalfLife', 'volumeOfDistribution', 'proteinBinding']

def quoted(did, ev):
    key, q = ('windows2', ev[2:]) if ev.startswith('2|') else ('windows', ev)
    assert any(q in w for w in Q[did][key]), (did, ev[:80]); return q
def shown(did, ev):
    return (f"US label ({Q[did]['meta2']['brand']})" if ev.startswith('2|') else 'US label') + f': “{quoted(did, ev)}.”'
def make_source(sid, m):
    return dict(id=sid, title=f"DailyMed · {m['brand']} ({m['manufacturer']})", url=m['url'],
        section=f"Current US FDA label: dosage and administration, renal impairment, clinical pharmacology and overdosage. SPL version {m['splVersion']}, effective {m['effective']}; application {m['application']}.",
        type='US FDA label (DailyMed)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))

# Brand-new inventory records start as catalog entries (same shape as an untouched catalog entry) and are then promoted below.
TEMPLATE = copy.deepcopy(drugs['docusate']); assert TEMPLATE['entryType'] == 'catalog' and TEMPLATE['pharmacokinetics']['status'] == 'not_curated'
new_ids = []
for did, c in C.items():
    if 'new' not in c: continue
    assert did not in drugs, did
    n = c['new']; d = copy.deepcopy(TEMPLATE)
    d.update(id=did, name=n['name'], aliases=n['aliases'], category=n['category'], drugClass=n['drugClass'], routes=n['routes'], otc=False,
             formulation=' / '.join(n['routes']) + ' · verify exact local product', addedInVersion=VERSION,
             labelSearchUrl='https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=' + n['name'].split(' (')[0].replace(' ', '+'))
    d.pop('pregnancyLactation', None); d.pop('updatedInVersion', None)
    data['drugs'].append(d); drugs[did] = d; new_ids.append(did)
data['drugs'].sort(key=lambda d: d['name'].lower())
GUIDE = {
 'acr-nkf-gbcm-2021': dict(title='ACR–NKF consensus · intravenous gadolinium-based contrast media in kidney disease (Weinreb et al., Kidney Med 2021;3:142–150)', url='https://doi.org/10.1016/j.xkme.2020.10.001',
    section='ACR group I/II/III classification; NSF risk with group II agents at eGFR <30 or AKI; screening, dialysis timing and the advice not to start or change dialysis for the contrast.', type='Specialist consensus report', accessed=DATE),
 'acr-contrast-manual': dict(title='ACR Manual on Contrast Media · gadolinium agent groups', url='https://www.acr.org/Clinical-Resources/Clinical-Tools-and-Reference/Contrast-Manual',
    section='Group classification of gadolinium-based agents by NSF association, including gadopiclenol as group II (2023).', type='Specialist consensus report', accessed=DATE),
 'acr-nkf-icm-2020': dict(title='ACR–NKF consensus · intravenous iodinated contrast media in kidney disease (Davenport et al., Kidney Med 2020;2:85–93)', url='https://doi.org/10.1016/j.xkme.2020.01.001',
    section='High-risk definition (AKI or eGFR <30), IV saline prophylaxis thresholds (eGFR <30; optional 30–44; not ≥45), nephrotoxic drugs, metformin and dialysis.', type='Specialist consensus report', accessed=DATE)}
for sid, s in GUIDE.items(): sources[sid] = dict(id=sid, **s)
changed, promoted, skipped = [], [], []
for did, c in C.items():
    d = drugs[did]; m = Q[did]['meta']; sid = f'{TAG}-{did}'; promote = c['promote']
    assert not promote or d['entryType'] in ('catalog', 'safety'), (did, d['entryType'])
    if not promote and d['entryType'] != 'renal': assert not c['modalities'], (did, 'dosing for a non-renal entry must promote it')
    sources[sid] = make_source(sid, m); sid2 = f'{TAG}b-{did}'
    if 'meta2' in Q[did]: sources[sid2] = make_source(sid2, Q[did]['meta2'])
    for k, mod in c['modalities'].items():
        cur = d['modalities'][k]
        if not promote and cur['status'] != 'not_curated': skipped.append(f'{did}/{k}'); continue
        notes = ' '.join(x for x in [mod['notes'], ' '.join(shown(did, e) for e in mod['ev'])] if x)
        extra = [sid2] if any(e.startswith('2|') for e in mod['ev']) else []
        d['modalities'][k] = dict(status=mod['status'], tables=mod['tables'], notes=notes, sourceIds=[sid] + extra + [s for s in cur.get('sourceIds', []) if s not in (sid, sid2)])
    p = d['pharmacokinetics']; filled = 0
    for k, f in c['pk'].items():
        slot = p[k] if k in CORE else p['dialysability'][k]
        if slot['value'] is not None: skipped.append(f'{did}/pk.{k}'); continue
        fact = dict(status=f['status'], value=f['value'], context=f'US label: “{quoted(did, f["ev"])}.”', sourceIds=[sid], evidence=f['ev'] + '.')
        if k == 'renalHalfLife': fact['basis'] = 'label_renal_impairment'
        if k in CORE: p[k] = fact
        else: p['dialysability'][k] = fact
        filled += 1
    if filled:
        if p['status'] != 'source_summary':
            for k in CORE:
                if p[k]['value'] is None: p[k] = dict(status='not_curated', value=None, context='Not stated in the current US label.', sourceIds=[])
            p['notes'] = 'Values quoted from the current US label; the sentence behind each value is shown. Circuit clearance and dialysis supplements are not inferred from these values.'
        p.update(status='source_summary', sourceCheckedAt=DATE)
    if promote:
        for k in ('kidneyMetric', 'summary', 'flag', 'considerations'):
            if k in c: d[k] = c[k]
        d.update(entryType='renal', sourceIds=[sid], sharedGuidanceId=d.get('sharedGuidanceId'),
                 jurisdiction='US FDA label; check the JFDA-approved leaflet for products marketed in Jordan.',
                 completeness=c.get('completeness', 'Renal statements, dialysis notes and PK from the current US label. Settings the label does not address stay "not curated"; nothing is inferred.'),
                 formulation=d['formulation'].replace(' · verify exact local product', ''))
        if 'meta2' in Q[did]: d['sourceIds'].append(sid2)
        d['review']['sourceCheckedAt'] = DATE
        promoted.append(did)
    elif d['entryType'] == 'renal':
        d['sourceIds'] = d.get('sourceIds', []) + ([sid] if sid not in d.get('sourceIds', []) else [])
    for sid3 in c.get('extraSources', []):
        if sid3 not in d['sourceIds']: d['sourceIds'].append(sid3)
    d['updatedInVersion'] = VERSION; changed.append(did)

cited = {s for x in re.findall(r'"sourceIds": \[(.*?)\]', json.dumps(data, ensure_ascii=False)) for s in re.findall(r'"([^"]+)"', x)}
data['sources'] = [s for s in sources.values() if not s['id'].startswith(('pk123-', 'us124-', 'us125-', 'us130-', 'us130b-', 'us140-', 'us140b-', 'us150-', 'us150b-', TAG + '-', TAG + 'b-')) or s['id'] in cited]
data['coverage'] = {t: sum(1 for d in data['drugs'] if d['entryType'] == t) for t in ('renal', 'safety', 'catalog')}
pk = [d for d in data['drugs'] if d['pharmacokinetics']['status'] == 'source_summary']
full = [d for d in pk if all(d['pharmacokinetics'][k]['status'] == 'sourced' for k in ['halfLife', 'volumeOfDistribution', 'proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None]
data['pharmacokineticCoverage'] = dict(profiles=len(pk), allFourCoreFields=len(full))
data.update(version=VERSION, clinicalDataVersion=VERSION, softwareReleaseDate=DATE)
# Contrast-associated AKI calculator sources (shown in the calculator's method section).
assert len(data['calculatorSources']) == 6
data['calculatorSources'] += [
 dict(title='ACR–NKF consensus · IV iodinated contrast media in kidney disease (Kidney Med 2020;2:85–93)', url='https://doi.org/10.1016/j.xkme.2020.01.001', checked=DATE, scope='High-risk definition (AKI or eGFR <30, incl. non-anuric dialysis) and IV saline prophylaxis thresholds (<30; optional 30–44; not ≥45)'),
 dict(title='ACR–NKF consensus · gadolinium-based contrast media in kidney disease (Kidney Med 2021;3:142–150)', url='https://doi.org/10.1016/j.xkme.2020.10.001', checked=DATE, scope='Gadolinium groups and NSF risk; why the AKI calculator is not used for gadolinium'),
 dict(title='Mehran et al. · risk score for contrast-induced nephropathy after PCI (J Am Coll Cardiol 2004;44:1393–9)', url='https://doi.org/10.1016/j.jacc.2004.06.068', checked=DATE, scope='Eight weighted factors, eGFR bands, four risk bands with CIN and dialysis rates')]
data['releaseChanges'] = dict(version=VERSION, changedIds=changed, newRenalIds=promoted, newIds=new_ids, newPKIds=[], pirrtSummaryIds=[],
    note='42 medicines added (oncology, anaesthesia & critical care, contrast media and others) and three catalog entries completed from current US labels; contrast-AKI calculator added.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))

# Curation queue and remaining list are derived from the database every release.
queue = json.loads((D/'CURATION_QUEUE.json').read_text()); prio = {q['id']: q.get('priority') for q in queue['drugs']}
def qitem(d):
    p = d['pharmacokinetics']
    return dict(id=d['id'], name=d['name'], category=d['category'], routes=d.get('routes', []), content=d['entryType'],
                renalDoseSourceCheckedAt=d['review']['sourceCheckedAt'], pkSourceCheckedAt=p.get('sourceCheckedAt'),
                modalities={k: m['status'] for k, m in d['modalities'].items()}, pkFields={k: p[k]['status'] for k in CORE},
                removal={k: v['status'] for k, v in p['dialysability'].items()}, independentClinicalReview=d['review']['status'], priority=prio.get(d['id']))
queue.update(version=VERSION, generatedAt=DATE, drugs=[qitem(d) for d in data['drugs']])
(D/'CURATION_QUEUE.json').write_text(json.dumps(queue, ensure_ascii=False, indent=2))
rem = json.loads((D/'REMAINING_MEDICATIONS.json').read_text())
rem.update(version=VERSION, remaining=[dict(id=d['id'], name=d['name'], category=d['category'], reason='Renal-dose curation pending' if d['entryType'] == 'catalog' else 'Shared safety note only; renal-dose curation pending')
                                        for d in data['drugs'] if d['entryType'] != 'renal'])
(D/'REMAINING_MEDICATIONS.json').write_text(json.dumps(rem, ensure_ascii=False, indent=2))

header = f'''# RenalRounds v{VERSION} · 1 November 2026

- **{len(new_ids)} medicines added to the inventory**, each with renal dosing from its current US label: oncology (ifosfamide, mesna, cytarabine, fludarabine — 20% less at CrCl 30–70 and not below 30, cladribine, bendamustine — not below CrCl 30, busulfan, topotecan — 0.75 mg/m² at CrCl 20–39, irinotecan, vinorelbine, temozolomide, azacitidine, arsenic trioxide, leucovorin rescue); anaesthesia & critical care (rocuronium, cisatracurium, succinylcholine, neostigmine, sugammadex — not below CrCl 30, bupivacaine, flumazenil, mannitol, albumin, terlipressin); alprazolam, penicillamine, droxidopa, isavuconazole, alemtuzumab and IV thiamine.
- **New category: contrast media.** Gadolinium agents carry their ACR group: group I gadodiamide (Omniscan) is contraindicated at GFR <30 or AKI; group II gadobutrol, gadoterate, gadoteridol, gadobenate and gadopiclenol and group III gadoxetate have their label NSF warnings plus the ACR–NKF consensus advice. Iodinated agents (iohexol, iodixanol, iopamidol, ioversol, iopromide) have the label AKI risk factors and ACR–NKF prophylaxis thresholds.
- **Contrast-associated AKI calculator** (from the eGFR · CrCl panel): IV contrast risk by ACR–NKF eGFR thresholds, and the Mehran score for coronary angiography/PCI with its published CIN and dialysis risks.
- Melphalan, rabbit antithymocyte globulin and IV immunoglobulin are now renal profiles.
- Every table, statement and value quotes its label sentence; guideline advice is cited to the ACR–NKF consensus papers. Existing curated content was not overwritten.
- Coverage: {data['coverage']['renal']} renal profiles, {data['coverage']['catalog']} catalog entries; PK {len(pk)} profiles ({len(full)} with all four core items). Drug content version {VERSION}.

'''
for target, base in [('CHANGELOG.md', 'changelog_v150.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v150.md'), ('SOURCE_AUDIT.md', 'source_audit_v150.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v160.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v160.py and apply_reviews.py. checks_v160.mjs proves only curated entries changed, no previously curated setting or PK value was overwritten, every quoted sentence is verbatim text of its stored label window, and every number in a PK value appears in its quote.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, changed=len(changed), promoted=len(promoted), skipped=skipped, coverage=data['coverage'], pk=data['pharmacokineticCoverage'])))
