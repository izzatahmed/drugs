"""v0.18.0: remaining medicines completed from other official labels (manufacturer, NZ Medsafe, Dutch MEB) and a US label; PREVENT calculator
(curation_v180.json, quotes verified in label_quotes_v180.json). Catalog entries become renal profiles with label dosing; existing profiles gain PK and
dialysis statements. Existing curated content is never overwritten: a setting
is filled only where it was "not curated", and a PK field only where it was blank.
"""
from pathlib import Path
import json, re, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-01'; VERSION = '0.18.0'; TAG = 'lb180'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.17.0'
C = json.loads((R/'curation_v180.json').read_text()); Q = json.loads((R/'label_quotes_v180.json').read_text())
sources = {s['id']: s for s in data['sources']}; drugs = {d['id']: d for d in data['drugs']}
CORE = ['halfLife', 'renalHalfLife', 'volumeOfDistribution', 'proteinBinding']

def quoted(did, ev):
    key, q = ('windows2', ev[2:]) if ev.startswith('2|') else ('windows', ev)
    assert any(q in w for w in Q[did][key]), (did, ev[:80]); return q
KIND = {'UK SmPC (emc)': 'UK SmPC', 'EMA product information (EPAR)': 'EU SmPC'}
def kind(m): return m.get('kind') or KIND.get(m.get('type'), 'US label')
def shown(did, ev):
    m = Q[did]['meta2'] if ev.startswith('2|') else Q[did]['meta']
    return (f"{kind(m)} ({m['brand']})" if ev.startswith('2|') else kind(m)) + f': “{quoted(did, ev)}.”'
def company(s):
    m = re.search(r'^(.*?\b(?:Limited|Ltd\.?|plc|B\.V\.|S\.r\.l\.|S\.A\.S?|GmbH|Inc\.?|Unlimited Company|Industrie|Europe B\.V\.))', s)
    return (m.group(1) if m else s.split(',')[0])[:70].strip()
def paren(s): return f' ({s})' if s else ''
def make_source(sid, m):
    if m.get('type') == 'UK SmPC (emc)':
        return dict(id=sid, title=f"emc · {m['brand']}{paren(company(m['manufacturer']))}", url=m['url'],
            section=f"Current UK SmPC: posology (renal impairment), contraindications, warnings, overdose and pharmacokinetics. Last updated on emc {m['effective']}; licence {m['application'] or 'see SmPC'}.",
            type='UK SmPC (emc)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))
    if m.get('type') == 'EMA product information (EPAR)':
        return dict(id=sid, title=f"EMA · {m['brand']}{paren(company(m['manufacturer']))}", url=m['url'],
            section=f"Current EU product information (Annex I SmPC): posology, special populations and pharmacokinetics. Authorisation {m['application']}.",
            type='EMA product information (EPAR)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))
    if m.get('kind'):
        return dict(id=sid, title=f"{m['kind']} · {m['brand']}{paren(company(m['manufacturer']))}", url=m['url'], section=m.get('section', ''),
            type=m['type'], accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))
    return dict(id=sid, title=f"DailyMed · {m['brand']} ({m['manufacturer']})", url=m['url'],
        section=f"Current US FDA label: dosage and administration, renal impairment, clinical pharmacology and overdosage. SPL version {m['splVersion']}, effective {m['effective']}; application {m['application']}.",
        type='US FDA label (DailyMed)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))

new_ids = []
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
        fact = dict(status=f['status'], value=f['value'], context=f'{kind(m)}: “{quoted(did, f["ev"])}.”', sourceIds=[sid], evidence=f['ev'] + '.')
        if k == 'renalHalfLife': fact['basis'] = 'label_renal_impairment'
        if k in CORE: p[k] = fact
        else: p['dialysability'][k] = fact
        filled += 1
    if filled:
        if p['status'] != 'source_summary':
            for k in CORE:
                if p[k]['value'] is None: p[k] = dict(status='not_curated', value=None, context=f'Not stated in the current {kind(m)}.', sourceIds=[])
            p['notes'] = f'Values quoted from the current {kind(m)}; the sentence behind each value is shown. Circuit clearance and dialysis supplements are not inferred from these values.'
        p.update(status='source_summary', sourceCheckedAt=DATE)
    if promote:
        for k in ('kidneyMetric', 'summary', 'flag', 'considerations'):
            if k in c: d[k] = c[k]
        d.update(entryType='renal', sourceIds=[sid], sharedGuidanceId=d.get('sharedGuidanceId'),
                 jurisdiction=c.get('sourceNote') or (('No current US label; ' + kind(m) + ' used' if kind(m) != 'US label' else 'US FDA label') + '; check the JFDA-approved leaflet for products marketed in Jordan.'),
                 completeness=c.get('completeness', f'Renal statements, dialysis notes and PK from the current {kind(m)}. Settings the label does not address stay "not curated"; nothing is inferred.'),
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
data['sources'] = [s for s in sources.values() if not s['id'].startswith(('pk123-', 'us124-', 'us125-', 'us130-', 'us130b-', 'us140-', 'us140b-', 'us150-', 'us150b-', 'us160-', 'us160b-', 'uk170-', 'uk170b-', TAG + '-', TAG + 'b-')) or s['id'] in cited]
data['coverage'] = {t: sum(1 for d in data['drugs'] if d['entryType'] == t) for t in ('renal', 'safety', 'catalog')}
pk = [d for d in data['drugs'] if d['pharmacokinetics']['status'] == 'source_summary']
full = [d for d in pk if all(d['pharmacokinetics'][k]['status'] == 'sourced' for k in ['halfLife', 'volumeOfDistribution', 'proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None]
data['pharmacokineticCoverage'] = dict(profiles=len(pk), allFourCoreFields=len(full))
data.update(version=VERSION, clinicalDataVersion=VERSION, softwareReleaseDate=DATE)
assert len(data['calculatorSources']) == 9
data['calculatorSources'] += [
 dict(title='Khan et al. · Development and validation of the AHA PREVENT equations (Circulation 2024;149:430–449)', url='https://doi.org/10.1161/CIRCULATIONAHA.123.067626', checked=DATE, scope='Base and base + UACR models, 10- and 30-year total CVD, ASCVD and heart failure; coefficients cross-checked with preventr 0.12.2 and published reference outputs'),
 dict(title='2025 AHA/ACC high blood pressure guideline · PREVENT 10-year total CVD ≥7.5% for stage 1 treatment', url='https://doi.org/10.1161/HYP.0000000000000249', checked=DATE, scope='Stage 1 treatment threshold; CKD, diabetes or CVD qualify regardless of score')]
data['releaseChanges'] = dict(version=VERSION, changedIds=changed, newRenalIds=promoted, newIds=new_ids, newPKIds=[], pirrtSummaryIds=[],
    note='Remaining medicines completed from other official labels with a fine-print source note; CALC menu and PREVENT calculator added.')
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

- **CALC menu** replaces the eGFR button: kidney function, contrast-associated AKI risk and the new **PREVENT cardiovascular risk calculator** (AHA PREVENT base and base + UACR models; 10- and 30-year total CVD, ASCVD and heart failure; the 2025 AHA/ACC 7.5% stage 1 hypertension threshold).
- **Remaining medicines from other official labels**, with the origin stated in a fine-print source note: cefoperazone-sulbactam (Pfizer label: sulbactam maximum by CrCl; dose after HD), roxithromycin (New Zealand data sheet: no reduction), oral paracetamol (Dutch SmPC: at least 6-hourly at CrCl 10–50 and 8-hourly below 10) and diphenoxylate-atropine (US label).
- Coverage: {data['coverage']['renal']} renal profiles, {data['coverage']['safety']} safety notes, {data['coverage']['catalog']} catalog entries; PK {len(pk)} profiles ({len(full)} with all four core items). Drug content version {VERSION}.

'''
for target, base in [('CHANGELOG.md', 'changelog_v170.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v170.md'), ('SOURCE_AUDIT.md', 'source_audit_v170.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v180.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v180.py and apply_reviews.py. checks_v180.mjs proves only curated entries changed, no previously curated setting or PK value was overwritten, every quoted sentence is verbatim text of its stored label window, and every number in a PK value appears in its quote.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, changed=len(changed), promoted=len(promoted), skipped=skipped, coverage=data['coverage'], pk=data['pharmacokineticCoverage'])))
