"""v0.14.0: antimicrobials, pain & neurology, psychiatry and allergy & respiratory completed from current US labels
(curation_v140.json, quotes verified in label_quotes_v140.json). Catalog entries become renal profiles with label dosing; existing profiles gain PK and
dialysis statements. Existing curated content is never overwritten: a setting
is filled only where it was "not curated", and a PK field only where it was blank.
"""
from pathlib import Path
import json, re, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-01'; VERSION = '0.14.0'; TAG = 'us140'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.13.0'
C = json.loads((R/'curation_v140.json').read_text()); Q = json.loads((R/'label_quotes_v140.json').read_text())
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
    d['updatedInVersion'] = VERSION; changed.append(did)

cited = {s for x in re.findall(r'"sourceIds": \[(.*?)\]', json.dumps(data, ensure_ascii=False)) for s in re.findall(r'"([^"]+)"', x)}
data['sources'] = [s for s in sources.values() if not s['id'].startswith(('pk123-', 'us124-', 'us125-', 'us130-', 'us130b-', TAG + '-', TAG + 'b-')) or s['id'] in cited]
data['coverage'] = {t: sum(1 for d in data['drugs'] if d['entryType'] == t) for t in ('renal', 'safety', 'catalog')}
pk = [d for d in data['drugs'] if d['pharmacokinetics']['status'] == 'source_summary']
full = [d for d in pk if all(d['pharmacokinetics'][k]['status'] == 'sourced' for k in ['halfLife', 'volumeOfDistribution', 'proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None]
data['pharmacokineticCoverage'] = dict(profiles=len(pk), allFourCoreFields=len(full))
data.update(version=VERSION, clinicalDataVersion=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=changed, newRenalIds=promoted, newPKIds=[], pirrtSummaryIds=[],
    note='Antimicrobials, pain & neurology, psychiatry and allergy & respiratory completed from current US labels.')
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

- **Four classes in one release, from current US labels:** antimicrobials, pain & neurology, psychiatry, and allergy & respiratory.
- **{len(promoted)} medicines that had no renal dosing are now renal profiles.** Examples: plazomicin (dose and interval by CrCl), cidofovir (contraindicated at CrCl ≤55 or SCr >1.5), Biktarvy (not recommended at CrCl 15–29; after dialysis on HD days), tinidazole (extra half dose after HD), nafcillin, sofosbuvir-velpatasvir and glecaprevir-pibrentasvir (no adjustment, including dialysis), streptomycin and tetracycline cautions; atogepant, ubrogepant and rimegepant renal limits; tapentadol ER and tramadol ER not for CrCl <30; inhaled and biologic respiratory medicines.
- **Dialysis statements** added to about 25 existing profiles (e.g. fosfomycin after HD, voriconazole, raltegravir timing, foscarnet not recommended on HD, valganciclovir no HD dose), and about {sum(1 for c in C.values() if c['pk'])} entries gained half-life, protein binding, volume of distribution or dialysis-removal values.
- Every table, statement and value quotes its label sentence; settings the label does not address stay "not curated". Existing curated content was not overwritten.
- Coverage: {data['coverage']['renal']} renal profiles, {data['coverage']['catalog']} catalog entries; PK {len(pk)} profiles ({len(full)} with all four core items). Drug content version {VERSION}.

'''
for target, base in [('CHANGELOG.md', 'changelog_v130.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v130.md'), ('SOURCE_AUDIT.md', 'source_audit_v130.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v140.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v140.py and apply_reviews.py. checks_v140.mjs proves only curated entries changed, no previously curated setting or PK value was overwritten, every quoted sentence is verbatim text of its stored label window, and every number in a PK value appears in its quote.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, changed=len(changed), promoted=len(promoted), skipped=skipped, coverage=data['coverage'], pk=data['pharmacokineticCoverage'])))
