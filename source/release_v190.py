"""v0.19.0: newer medicines and vaccines for CKD/dialysis/transplant, label-quoted drug interactions with a two-drug checker, and four kidney calculators
(curation_v190.json, quotes verified in label_quotes_v190.json). Catalog entries become renal profiles with label dosing; existing profiles gain PK and
dialysis statements. Existing curated content is never overwritten: a setting
is filled only where it was "not curated", and a PK field only where it was blank.
"""
from pathlib import Path
import copy, json, re, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-01'; VERSION = '0.19.0'; TAG = 'us190'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.18.0'
C = json.loads((R/'curation_v190.json').read_text()); Q = json.loads((R/'label_quotes_v190.json').read_text())
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

# Brand-new inventory records start as catalog entries (same shape as an untouched catalog entry) and are then promoted below.
TEMPLATE = copy.deepcopy(next(d for d in data['drugs'] if d['entryType'] == 'catalog' and d['pharmacokinetics']['status'] == 'not_curated' and not d.get('sharedGuidanceId'))); assert TEMPLATE['entryType'] == 'catalog' and TEMPLATE['pharmacokinetics']['status'] == 'not_curated'
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
 'cdc-hd-vaccination': dict(title='CDC · Recommendations for preventing transmission of infections among chronic hemodialysis patients (MMWR 2001;50 RR-5)', url='https://www.cdc.gov/mmwr/preview/mmwrhtml/rr5005a1.htm',
    section='Hepatitis B vaccination of susceptible haemodialysis patients and of patients with CKD before dialysis; antibody testing and revaccination.', type='Public health guideline (CDC)', accessed=DATE),
 'cdc-adult-schedule': dict(title='CDC · Adult immunization schedule by medical condition', url='https://www.cdc.gov/vaccines/schedules/hcp/imz/adult-conditions.html',
    section='Column for kidney failure, end-stage renal disease or dialysis; immunocompromised column (including transplant).', type='Public health guideline (CDC)', accessed=DATE),
 'cdc-altered-immunocompetence': dict(title='CDC · General Best Practice Guidelines for Immunization: Altered Immunocompetence', url='https://www.cdc.gov/vaccines/hcp/imz-best-practices/altered-immunocompetence.html',
    section='Live vaccines and altered immunocompetence (including chronic renal disease and transplantation); timing of vaccination before immunosuppression.', type='Public health guideline (CDC)', accessed=DATE),
 'fda-cyp-table': dict(title="FDA · Examples of drugs that interact with CYP enzymes and transporter systems (Table 1)", url='https://www.fda.gov/drugs/drug-interactions-labeling/healthcare-professionals-fdas-examples-drugs-interact-cyp-enzymes-and-transporter-systems',
    section='Clinical index substrates, inhibitors and inducers of CYP enzymes and transporters (strong, moderate, weak; sensitive substrates).', type='Regulatory reference table (FDA)', accessed=DATE)}
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

# Drug interactions: verbatim label sentences (interactions_v190.json, built by extract_interactions.py) and FDA CYP/transporter roles.
IX = json.loads((R/'interactions_v190.json').read_text())
for did, v in IX['drugs'].items():
    d = drugs[did]; sid = f'ix190-{did}'; m = dict(v['meta'])
    sources[sid] = make_source(sid, m); sources[sid]['section'] = sources[sid]['section'].replace('dosage and administration, renal impairment, clinical pharmacology and overdosage', 'drug interactions section (or Precautions / OTC warnings for older labels)')
    d['interactions'] = dict(statements=v['statements'], fdaRoles=IX['roles'].get(did, []), sourceIds=[sid] + (['fda-cyp-table'] if IX['roles'].get(did) else []))
    if did not in changed: changed.append(did)
    d['updatedInVersion'] = VERSION
for did, roles in IX['roles'].items():
    if did in drugs and 'interactions' not in drugs[did]:
        drugs[did]['interactions'] = dict(statements=[], fdaRoles=roles, sourceIds=['fda-cyp-table'])
        if did not in changed: changed.append(did)
        drugs[did]['updatedInVersion'] = VERSION
data['interactionClasses'] = IX['classes']
cited = {s for x in re.findall(r'"sourceIds": \[(.*?)\]', json.dumps(data, ensure_ascii=False)) for s in re.findall(r'"([^"]+)"', x)}
data['sources'] = [s for s in sources.values() if not s['id'].startswith(('pk123-', 'us124-', 'us125-', 'us130-', 'us130b-', 'us140-', 'us140b-', 'us150-', 'us150b-', 'us160-', 'us160b-', 'uk170-', 'uk170b-', 'lb180-', 'lb180b-', 'ix190-', TAG + '-', TAG + 'b-')) or s['id'] in cited]
data['coverage'] = {t: sum(1 for d in data['drugs'] if d['entryType'] == t) for t in ('renal', 'safety', 'catalog')}
pk = [d for d in data['drugs'] if d['pharmacokinetics']['status'] == 'source_summary']
full = [d for d in pk if all(d['pharmacokinetics'][k]['status'] == 'sourced' for k in ['halfLife', 'volumeOfDistribution', 'proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None]
data['pharmacokineticCoverage'] = dict(profiles=len(pk), allFourCoreFields=len(full))
data.update(version=VERSION, clinicalDataVersion=VERSION, softwareReleaseDate=DATE)
assert len(data['calculatorSources']) == 11
data['calculatorSources'] += [
 dict(title='KDIGO 2024 clinical practice guideline for CKD evaluation and management', url='https://kdigo.org/guidelines/ckd-evaluation-and-management/', checked=DATE, scope='G and A categories, heat-map risk colours, KFRE thresholds (practice points 2.2.1–2.2.3)'),
 dict(title='Tangri et al. · multinational assessment of kidney failure risk equations (JAMA 2016;315:164–174)', url='https://doi.org/10.1001/jama.2015.18202', checked=DATE, scope='4-variable KFRE coefficients; non-North American calibration (baseline risk lowered 32.9% at 2 years and 16.5% at 5 years)'),
 dict(title='KDOQI clinical practice guideline for hemodialysis adequacy: 2015 update', url='https://doi.org/10.1053/j.ajkd.2015.07.015', checked=DATE, scope='spKt/V target 1.4 and minimum 1.2 per session (thrice weekly); Daugirdas second-generation formula'),
 dict(title='WHO · body mass index classification', url='https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/body-mass-index', checked=DATE, scope='Adult BMI classes')]
data['releaseChanges'] = dict(version=VERSION, changedIds=changed, newRenalIds=promoted, newIds=new_ids, newPKIds=[], pirrtSummaryIds=[],
    note='Newer medicines and vaccines; label-quoted drug interactions and a two-drug checker; UACR/KDIGO/KFRE, BMI and dialysis-adequacy calculators.')
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

- **Drug interactions.** About 100 priority medicines (anti-rejection drugs, antihypertensives, antihistamines, enzyme inducers and inhibitors, anticoagulants, statins, digoxin, colchicine) now show a "Drug interactions" panel of sentences quoted from their label, plus FDA CYP/P-gp roles. A new **interaction checker** (CALC menu, or from any drug) shows label sentences in which one medicine names the other or its class, and FDA inhibitor/inducer + substrate pairings.
- **{len(new_ids)} medicines added:** evinacumab, lomitapide (40 mg maximum on HD), aprocitentan (not on dialysis), sotagliflozin, vericiguat, mavacamten, belumosudil, imlifidase (EU) and a new **Vaccines** category — hepatitis B with dialysis schedules (Engerix-B 40 mcg × 4; Recombivax HB Dialysis Formulation; Heplisav-B not established on HD), recombinant zoster, pneumococcal PCV20/PCV21, high-dose influenza, RSV and COVID-19 mRNA, with CDC notes on dialysis and live vaccines after transplant.
- **New calculators:** UACR with KDIGO G/A heat map and KFRE 2- and 5-year kidney failure risk; BMI and body size; haemodialysis adequacy (URR, Daugirdas spKt/V).
- Coverage: {data['coverage']['renal']} renal profiles, {data['coverage']['safety']} safety notes, {data['coverage']['catalog']} catalog entries; PK {len(pk)} profiles ({len(full)} with all four core items). Drug content version {VERSION}.

'''
for target, base in [('CHANGELOG.md', 'changelog_v180.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v180.md'), ('SOURCE_AUDIT.md', 'source_audit_v180.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v190.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v190.py and apply_reviews.py. checks_v190.mjs proves only curated entries changed, no previously curated setting or PK value was overwritten, every quoted sentence is verbatim text of its stored label window, and every number in a PK value appears in its quote.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, changed=len(changed), promoted=len(promoted), skipped=skipped, coverage=data['coverage'], pk=data['pharmacokineticCoverage'])))
