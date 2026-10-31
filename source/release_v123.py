"""v0.12.3: pharmacokinetic values rebuilt from current product information.

Every PK field that cited the Renal Drug Handbook (5th ed.) is replaced by a value quoted from the
current US FDA label (DailyMed), or for medicines with no US label, the EMA product information
(vildagliptin) or the UK SmPC. Each value carries the label sentence it came from. Fields that could
not be confirmed from a label are left blank ("being rebuilt"). The handbook is then removed from
the sources and the reference directory. No dose table changes.
"""
from pathlib import Path
import json, re, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-10-31'; VERSION = '0.12.3'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.12.2'
ext = json.loads((R/'pk_extract_v123.json').read_text())
# Second pass: values a reviewer accepted from broader candidate sentences (review_pk_v123b.py).
SECOND = {(a['id'], a['field']): a for a in json.loads((R/'pk_review_v123b.json').read_text())}
sources = {s['id']: s for s in data['sources']}
drugs = {d['id']: d for d in data['drugs']}
CORE = ['halfLife', 'renalHalfLife', 'volumeOfDistribution', 'proteinBinding']
MOD = dict(ihd='hemodialysis', pd='peritoneal dialysis')
PENDING = 'Being rebuilt from current product information.'

def norm(v):
    for a, b in [(r'\bapproximately |\babout |\bapprox\. ', '≈'), (r' to ', '–'), (r'\bhours?\b|\bhrs?\b', 'h'),
                 (r'\bminutes?\b', 'min'), (r'\b[Ll]it(er|re)s\b', 'L'), (r'greater than or equal to ', '≥'),
                 (r'greater than ', '>'), (r'less than ', '<'), (r'an average of ', 'mean '), (r'≥ ', '≥'), (r'(\d)-(\d)', r'\1–\2')]:
        v = re.sub(a, b, v)
    return v.strip()

HEAD = re.compile(r'^(?:\d{1,2}(?:\.\d{1,2})*\s+(?:[A-Z][A-Z&/ ]{3,}(?=\s[A-Z][a-z])|[A-Z][a-z]+(?: [A-Z][a-z]+)*(?=\s[A-Z]))\s*)+')
def fragment(sentence, needle):
    """Shortest sub-sentence of the extracted window that contains the needle, minus section headings."""
    parts = re.split(r'(?<=[a-z0-9\)\]%])\.\s+(?=[A-Z0-9])', sentence)
    hit = [p for p in parts if needle.lower() in p.lower()] or parts
    return HEAD.sub('', hit[-1] if needle.lower().startswith('dialy') else hit[0]).strip().rstrip('.') + '.'

def nums(s): return re.findall(r'\d+(?:\.\d+)?', s)

# ---- Corrections after line-by-line review of all 181 extracted values (2026-10-31) ----
# value: replacement value (None = drop); move: put the sentence under another field; status: dialysis status.
OVR = {
 ('acetylcysteine', 'renalHalfLife'): dict(move='halfLife', value='5.6 h (mean terminal, total acetylcysteine)', needle='5.6 hours'),
 ('aprepitant', 'dial-ihd'): dict(status='not_removed'),
 ('cephalexin', 'proteinBinding'): dict(value='10–15%'),
 ('clarithromycin', 'halfLife'): dict(value='3–4 h (250 mg every 12 h); 5–7 h (500 mg every 8–12 h)'),
 ('fludrocortisone', 'halfLife'): dict(value='≥3.5 h (plasma); biological half-life 18–36 h'),
 ('hydroxychloroquine', 'halfLife'): dict(value='40–50 days (terminal, whole blood)', needle='40 to 50 days'),
 ('isosorbide-dinitrate', 'halfLife'): dict(value=None),           # sentence gives the 5-mononitrate half-life
 ('lanthanum-carbonate', 'halfLife'): dict(move='renalHalfLife', value='53 h (plasma, dialysis patients after stopping)'),
 ('mesalazine', 'proteinBinding'): dict(value='43±6% (mesalamine; N-acetyl metabolite 78±1%)'),
 ('moxifloxacin', 'dial-pd'): dict(value=None),                    # wrong sentence matched
 ('oxcarbazepine', 'volumeOfDistribution'): dict(value='49 L (MHD, active metabolite)'),
 ('oxcarbazepine', 'renalHalfLife'): dict(value='19 h (MHD, CrCl <30 mL/min)'),
 ('propafenone', 'halfLife'): dict(value=None),                    # poor metabolisers only
 ('sulfasalazine', 'halfLife'): dict(value=None),                  # sulfapyridine, not the parent
 ('sulfasalazine', 'proteinBinding'): dict(value='>99.3% (sulfasalazine); sulfapyridine ≈70%'),
 ('tigecycline', 'dial-ihd'): dict(status='not_removed'),
 ('digoxin', 'renalHalfLife'): dict(value='3.5–5 days (anuric)'),
 ('cefixime', 'renalHalfLife'): dict(value='mean 11.5 h (CrCl 5–20 mL/min)'),
 ('vancomycin', 'dial-ihd'): dict(value='Poorly removed by dialysis (label)', extra='High-flux membranes remove more; the HD dosing rows give post-session doses guided by pre-dialysis levels.', extraSources=['unmc-vanco-hd']),
}

# ---- Medicines with no US label: EMA product information (vildagliptin) or UK SmPC 5.2 / 4.9 ----
NONUS = {
 'vildagliptin': dict(src=dict(title='EMA · Galvus (vildagliptin) product information', url='https://www.ema.europa.eu/en/documents/product-information/galvus-epar-product-information_en.pdf',
        section='Summary of product characteristics 4.9 Overdose and 5.2 Pharmacokinetic properties (centrally authorised product). Reproduced with acknowledgement of the European Medicines Agency.', type='EMA product information'),
     halfLife=('≈3 h (oral); ≈2 h (IV)', 'The mean elimination half-life after intravenous administration is approximately 2 hours. The elimination half-life after oral administration is approximately 3 hours.'),
     volumeOfDistribution=('71 L (Vss)', 'The mean volume of distribution of vildagliptin at steady-state after intravenous administration (Vss) is 71 litres, suggesting extravascular distribution.'),
     proteinBinding=('9.3%', 'The plasma protein binding of vildagliptin is low (9.3%) and vildagliptin distributes equally between plasma and red blood cells.'),
     ihd=('negligible', '≈3% removed over a 3–4 h session', 'Vildagliptin was removed by haemodialysis to a limited extent (3% over a 3-4 hour haemodialysis session starting 4 hours post dose).')),
 'teicoplanin': dict(src=dict(title='UK SmPC · Targocid 400 mg powder for solution for injection/infusion (Sanofi)', url='https://www.medicines.org.uk/emc/product/2927/smpc',
        section='4.2 Posology (renal impairment, CAPD), 4.9 Overdose and 5.2 Pharmacokinetic properties. No current US label (not marketed in the US).', type='UK product information'),
     halfLife=('100–170 h', 'Elimination half-life of teicoplanin varies from 100 to 170 hours in the most recent studies where blood sampling duration is about 8 to 35 days.'),
     volumeOfDistribution=('0.7–1.4 L/kg (Vss)', 'The volume of distribution at steady-state (Vss) varies from 0.7 to 1.4 L/kg.'),
     proteinBinding=('87.6–90.8%', 'The binding to human serum proteins ranges from 87.6 to 90.8% without any variation in function of the teicoplanin concentrations.'),
     ihd=('not_removed', 'Not removed by haemodialysis (SmPC)', 'Teicoplanin is not removed by haemodialysis and only slowly by peritoneal dialysis.'),
     pd=('negligible', 'Only slowly removed by peritoneal dialysis (SmPC)', 'Teicoplanin is not removed by haemodialysis and only slowly by peritoneal dialysis.')),
 'domperidone': dict(src=dict(title='UK SmPC · Domperidone 1 mg/ml oral suspension', url='https://www.medicines.org.uk/emc/product/3188/smpc',
        section='5.2 Pharmacokinetic properties. No US label (not approved in the US).', type='UK product information'),
     halfLife=('7–9 h (single oral dose)', 'The plasma half-life after a single oral dose is 7-9 hours in healthy subjects but is prolonged in patients with severe renal insufficiency.'),
     renalHalfLife=('20.8 h (severe renal insufficiency)', 'In subjects with severe renal insufficiency (serum creatine>6mg/100L,ie 0.6 mmol/L) the elimination half-life of domperidone is increased from 7.4 to 20.8 hours, but plasma drug levels are lower than in healthy volunteers.'),
     proteinBinding=('91–93%', 'Domperidone is 91-93% bound to plasma proteins.')),
 'carbimazole': dict(src=dict(title='UK SmPC · Carbimazole 10 mg tablets', url='https://www.medicines.org.uk/emc/product/100092/smpc',
        section='5.2 Pharmacokinetic properties. No US label (methimazole is the US product).', type='UK product information'),
     halfLife=('5.3–5.4 h', 'Carbimazole has a half-life of 5.3 to 5.4 hours.'),
     volumeOfDistribution=('0.5 L/kg (thiamazole)', 'The total volume of distribution of thiamazole is 0.5 1/kg.'),
     proteinBinding=('Moderate (thiamazole)', 'Thiamazole is moderately bound to plasma proteins.')),
 'hyoscine-butylbromide': dict(src=dict(title='UK SmPC · Buscopan 10 mg tablets (Opella Healthcare)', url='https://www.medicines.org.uk/emc/product/1775/smpc',
        section='5.2 Pharmacokinetic properties. No US label (not approved in the US).', type='UK product information'),
     halfLife=('6.2–10.6 h (oral, 100–400 mg)', 'Following oral administration of single doses in the range of 100 to 400 mg, the terminal elimination half-lives ranged from 6.2 to 10.6 hours.'),
     proteinBinding=('≈4.4% (albumin)', 'Plasma protein binding (albumin) of hyoscine butylbromide is approximately 4.4%.')),
 'alfacalcidol': dict(src=dict(title='UK SmPC · Alfacalcidol 0.25 microgram soft capsules', url='https://www.medicines.org.uk/emc/product/14383/smpc',
        section='5.2 Pharmacokinetic properties. No US label (not approved in the US).', type='UK product information'),
     halfLife=('≈4 h', 'The half-life of alfacalcidol is about 4 hours.')),
 'cholecalciferol': dict(src=dict(title='UK SmPC · Fultium-D3 20,000 IU capsules', url='https://www.medicines.org.uk/emc/product/3659/smpc',
        section='5.2 Pharmacokinetic properties (no numeric values stated). US products are supplements without an FDA label.', type='UK product information')),
}

def fact(value, sid, context, status='sourced', **kw):
    return dict(status=status, value=value, context=context, sourceIds=sid if isinstance(sid, list) else [sid], **kw)
def pending(): return dict(status='not_curated', value=None, context=PENDING, sourceIds=[])

rebuilt, log = [], []
for did, e in ext.items():
    d = drugs[did]; p = d['pharmacokinetics']
    old = {k: p[k] for k in CORE} | {f'dial-{m}': p['dialysability'][m] for m in ('ihd', 'pd')}
    if did in NONUS:
        n = NONUS[did]; sid = f'pk123-{did}'
        sources[sid] = dict(id=sid, accessed=DATE, **n['src'])
        lab = 'EMA SmPC' if 'EMA' in n['src']['type'] else 'UK SmPC'
        for k in CORE:
            if not any('rdh5' in s for s in p[k]['sourceIds']): continue
            p[k] = fact(n[k][0], sid, f'{lab}: “{n[k][1]}”', evidence=n[k][1]) if k in n else pending()
        for m in ('ihd', 'pd'):
            if not any('rdh5' in s for s in p['dialysability'][m]['sourceIds']): continue
            p['dialysability'][m] = fact(n[m][1], sid, f'{lab}: “{n[m][2]}”', status=n[m][0], evidence=n[m][2]) if m in n else pending()
    else:
        meta = e['meta']; sid = f'pk123-{did}'
        sources[sid] = dict(id=sid, title=f"DailyMed · {meta['brand'] or d['name']} ({meta['manufacturer']}) · pharmacokinetics", url=meta['url'],
            section=f"US FDA label 12.3 Pharmacokinetics, 8.6 Renal impairment and 10 Overdosage (older labels: Clinical Pharmacology / Overdosage). SPL version {meta['splVersion']}, effective {meta['effective']}; application {meta['application']}.",
            type='US FDA label (DailyMed)', accessed=DATE, label=dict(setid=meta['setid'], splVersion=meta['splVersion'], effective=meta['effective'], application=meta['application']))
        found = dict(e['found'])
        new = {}
        for key, f in found.items():
            o = OVR.get((did, key), {})
            if 'value' in o and o['value'] is None: log.append(f'{did}/{key}: dropped'); continue
            tgt = o.get('move', key)
            if key.startswith('dial-'):
                frag = fragment(f['sentence'], 'dialy') if 'dialy' in f['sentence'].lower() else fragment(f['sentence'], 'hemoperfusion')
                st = o.get('status', f['status']); m = key[5:]
                val = o.get('value') or {'removed': f'Removed by {MOD[m]} (label)', 'not_removed': f'Not significantly removed by {MOD[m]} (label)',
                       'negligible': f'Negligible removal by {MOD[m]} (label)', 'unknown': f'Benefit of {MOD[m]} not established (label)'}[st]
                ctx = f'US label: “{frag}”' + (' ' + o['extra'] if 'extra' in o else '')
                new[tgt] = fact(val, [sid] + o.get('extraSources', []), ctx, status=st, evidence=frag)
            else:
                needle = o.get('needle') or (nums(f['value']) or [f['value']])[0]
                frag = fragment(f['sentence'], needle)
                val = o.get('value') or norm(f['value'])
                for x in nums(val): assert x in frag, (did, key, val, frag)
                extra = dict(basis='label_renal_impairment') if tgt == 'renalHalfLife' else {}
                new[tgt] = fact(val, sid, f'US label: “{frag}”', evidence=frag, **extra)
        for (i2, key), a in SECOND.items():
            if i2 != did: continue
            tgt = key
            assert tgt not in new, (did, key)
            if key.startswith('dial-'):
                new[tgt] = fact(a['value'], sid, f'US label: “{a["evidence"]}.”', status=a['status'], evidence=a['evidence'] + '.')
            else:
                extra = dict(basis='label_renal_impairment') if key == 'renalHalfLife' else {}
                new[tgt] = fact(a['value'], sid, f'US label: “{a["evidence"]}.”', evidence=a['evidence'] + '.', **extra)
        for k in CORE:
            if any('rdh5' in s for s in p[k]['sourceIds']): p[k] = new.get(k) or pending()
        for m in ('ihd', 'pd'):
            if any('rdh5' in s for s in p['dialysability'][m]['sourceIds']): p['dialysability'][m] = new.get(f'dial-{m}') or pending()
    assert not any('rdh5' in s for k in CORE for s in p[k]['sourceIds'])
    assert not any('rdh5' in s for m in p['dialysability'].values() for s in m['sourceIds'])
    used = any(p[k]['value'] is not None for k in CORE) or any(m['value'] is not None for m in p['dialysability'].values())
    p.pop('historical', None); p.pop('evidenceDate', None)
    if used:
        p.update(status='source_summary', sourceCheckedAt=DATE,
                 notes='Values quoted from current product information; the sentence behind each value is shown. Blank fields are being rebuilt. Circuit clearance and dialysis supplements are not inferred from these values.')
    else:
        p.update(status='not_curated', sourceCheckedAt=None, notes='Pharmacokinetic values are being rebuilt from current product information.')
        for m in ('crrt', 'sled'): p['dialysability'][m] = dict(status='not_curated', value=None, context='Modality-specific removal data have not been curated.', sourceIds=[])
    for k in CORE: p[k].pop('basis', None) if p[k].get('basis') == 'handbook_normal_esrf_columns' else None
    rebuilt.append(did)

# ---- Remove the handbook ----
for d in data['drugs']:
    for n in d.get('evidenceNotes', []):
        n['sourceIds'] = [s for s in n.get('sourceIds', []) if not s.startswith('rdh5')]
        n['text'] = n['text'].replace('The 2018 BC sheet and fifth-edition handbook retain', 'The 2018 BC sheet retains').replace('mixed-analyte handbook PK', 'mixed-analyte reference PK')
WORDING = [('do not substitute the historical handbook’s 88-microgram base strengths', 'do not substitute 88-microgram base-strength doses from non-US references'),
           ('Do not transfer the 2018 handbook’s normal-dose dialysis advice into this entry', 'Do not transfer older normal-dose dialysis advice from other references into this entry'),
           ('while the older BC/handbook sources differ', 'while the older BC source differs')]
def reword(o):
    if isinstance(o, dict): return {k: reword(v) for k, v in o.items()}
    if isinstance(o, list): return [reword(v) for v in o]
    if isinstance(o, str):
        for a, b in WORDING: o = o.replace(a, b)
    return o
for d in data['drugs']:
    for k in ('modalities', 'considerations'):
        if k in d: d[k] = reword(d[k])
for c in data['sourceConflicts']:
    c['issue'] = c['issue'].replace(', BC 2018 sheet and handbook fifth edition', ' and BC 2018 sheet').replace('mixed-analyte handbook PK', 'mixed-analyte reference PK')
for a in data['sourceAudit']:
    if 'Renal Drug Handbook' in a.get('title', ''):
        a['selectedUse'] = 'Withdrawn. Dose tables were rebuilt in v0.12.0 and pharmacokinetic values in v0.12.3 from current product information; no value in this release cites it.'
data['referenceResources'] = [r for r in data['referenceResources'] if r['id'] != 'upload-0']
blob = json.dumps(data['drugs'] + data['sourceConflicts'], ensure_ascii=False)
assert 'rdh5' not in blob and 'andbook' not in blob, 'handbook still referenced'
cited = {s for x in re.findall(r'"sourceIds": \[(.*?)\]', json.dumps(data, ensure_ascii=False)) for s in re.findall(r'"([^"]+)"', x)}
data['sources'] = [s for s in sources.values() if not s['id'].startswith('rdh5') and (not s['id'].startswith('pk123-') or s['id'] in cited)]

pk = [d for d in data['drugs'] if d['pharmacokinetics']['status'] == 'source_summary']
full = [d for d in pk if all(d['pharmacokinetics'][k]['status'] == 'sourced' for k in ['halfLife', 'volumeOfDistribution', 'proteinBinding']) and d['pharmacokinetics']['dialysability']['ihd']['value'] is not None]
data['pharmacokineticCoverage'] = dict(profiles=len(pk), allFourCoreFields=len(full))
for did in rebuilt: drugs[did]['updatedInVersion'] = VERSION
data.update(version=VERSION, softwareReleaseDate=DATE)   # clinicalDataVersion unchanged: no dosing change
data['releaseChanges'] = dict(version=VERSION, changedIds=rebuilt, newRenalIds=[], newPKIds=[], pirrtSummaryIds=[],
    note=f'Pharmacokinetic values for {len(rebuilt)} entries rebuilt from current product information; the Renal Drug Handbook is no longer cited. Dose tables unchanged.')
data['referenceScope']['publishedSources'] = ('US FDA labels (DailyMed); EMA product information where no US label exists; UK SmPCs for medicines without a US or EMA product; '
                                              'international guidelines (KDIGO, ISPD) and named US hospital protocols.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))

own = lambda f: f['value'] is not None and any(s.startswith('pk123-') for s in f['sourceIds'])
filled = sum(1 for did in rebuilt for k in CORE if own(drugs[did]['pharmacokinetics'][k]))
dial = sum(1 for did in rebuilt for m in ('ihd', 'pd') if own(drugs[did]['pharmacokinetics']['dialysability'][m]))
header = f'''# RenalRounds v{VERSION} · 31 October 2026

- **Pharmacokinetics rebuilt from current product information.** The {len(rebuilt)} profiles that still quoted the Renal Drug Handbook (5th ed., 2018) now quote the current US FDA label, or the EMA product information (vildagliptin) or UK SmPC (teicoplanin, domperidone, carbimazole, hyoscine butylbromide, alfacalcidol, colecalciferol) where there is no US label. Each value shows the label sentence it came from: {filled} half-life / Vd / binding values and {dial} dialysis-removal statements.
- Values that a current label does not state are left blank and marked "being rebuilt"; the old handbook figures were not carried over. Metabolite values are labelled (e.g. oxcarbazepine MHD, sulfasalazine/sulfapyridine, mesalamine/N-acetyl-5-ASA).
- The Renal Drug Handbook is no longer cited anywhere in the app. PK coverage: {len(pk)} profiles, {len(full)} with all four core items.
- Dose tables unchanged (drug content version stays {data['clinicalDataVersion']}).

'''
for target, base in [('CHANGELOG.md', 'changelog_v122.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v122.md'), ('SOURCE_AUDIT.md', 'source_audit_v122.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'REFERENCE_DIRECTORY.json').write_text(json.dumps(data['referenceResources'], ensure_ascii=False, indent=2))
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v123.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v123.py and apply_reviews.py. checks_v123.mjs proves dose tables and pregnancy sections are unchanged from v0.12.2, no field cites the Renal Drug Handbook, every rebuilt PK value cites a DailyMed, EMA or emc source, and every number in a value appears in its quoted label sentence.

These are software/source-integrity checks, not clinical validation.
''')
print(f'v{VERSION}: {len(rebuilt)} PK profiles rebuilt; {filled} core values, {dial} dialysis statements; coverage {data["pharmacokineticCoverage"]}; sources {len(data["sources"])}')
print('\n'.join(log))
