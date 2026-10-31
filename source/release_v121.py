"""v0.12.1: vancomycin and aminoglycosides with numeric CKD/HD/PD dosing, ISPD 2022 intraperitoneal
peritonitis dosing for every antibiotic in its Table 5, vonoprazan (P-CAB), pregnancy/lactation excerpts
from the cited labels, and the icon-only back arrow.
"""
from pathlib import Path
import json, re, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-10-31'; VERSION = '0.12.1'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.12.0'
labels = json.loads((R/'label_extract_v121.json').read_text())   # pregnancy/lactation excerpts + label metadata, built by extract_labels_v121.py
drugs = {d['id']: d for d in data['drugs']}; sources = {s['id']: s for s in data['sources']}
def T(ind, rows): return dict(indication=ind, rows=[dict(context=c, dose=x) for c, x in rows])

sources['ispd2022'] = dict(id='ispd2022', title='ISPD peritonitis guideline recommendations: 2022 update · Table 5 (Li PKT et al., Perit Dial Int 2022;42:110–153)',
    url='https://doi.org/10.1177/08968608221080586', section='Table 5: intraperitoneal antibiotic dosing for PD peritonitis (intermittent: one exchange daily, dwell at least 6 h; continuous: all exchanges). Footnotes on residual kidney function, APD and ampicillin.',
    type='International clinical practice guideline (ISPD)', accessed=DATE)
sources['nm-ip-2025'] = dict(id='nm-ip-2025', title='Northwestern Medicine ADSP · Intra-peritoneal antibiotic guideline (updated July 2025)',
    url='https://adsp.nm.org/uploads/1/4/3/0/143064172/intra_peritoneal_antibiotic_guideline.pdf', section='Reproduces ISPD 2022 Table 5 (used to verify the table values); vancomycin and gentamicin level monitoring for IP therapy.',
    type='Institutional dosing protocol', accessed=DATE)
sources['unmc-vanco-hd'] = dict(id='unmc-vanco-hd', title='Nebraska Medicine/UNMC · Nephrology preferred vancomycin dosing for adult haemodialysis (updated March 2024)',
    url='https://www.unmc.edu/intmed/_documents/id/asp/dose-vancomycin-nephrology-preferred-dosing-strategy.pdf', section='Stable maintenance haemodialysis only: loading, post-dialysis maintenance and pre-dialysis level adjustment table. Excludes CRRT, PIRRT, PD and irregular HD.',
    type='Institutional dosing protocol', accessed=DATE)
def label_source(i):
    m = labels[i]['meta']; sid = f'us121-{i}'
    sources[sid] = dict(id=sid, title=f"DailyMed · {m['brand']} ({m['manufacturer']})", url=m['url'],
        section=f"Current US FDA label: dosage and administration (renal impairment, dialysis), use in specific populations. SPL version {m['splVersion']}, effective {m['effective']}; application {m['application']}.",
        type='US FDA label (DailyMed)', accessed=DATE, label=dict(setid=m['setid'], splVersion=m['splVersion'], effective=m['effective'], application=m['application']))
    return sid

IP = 'Intraperitoneal · PD peritonitis · ISPD 2022 Table 5'
IPNOTE = 'Intraperitoneal (IP) doses treat PD peritonitis; intermittent means added to one exchange daily with a dwell of at least 6 hours. Check stability and compatibility before mixing antibiotics in one bag. Other PD rows on this tab are systemic doses.'
RKF = ' ISPD: doses may need about 25% increase with significant residual kidney function.'
ip_table = {
 'cefazolin': ([('Intermittent', '15 mg/kg daily (long dwell); 20 mg/kg daily (short dwell)'), ('Continuous', 'Loading 500 mg/L, then 125 mg/L')], RKF),
 'cefepime': ([('Intermittent', '1,000 mg daily'), ('Continuous', 'Loading 500 mg/L, then 125 mg/L')], RKF),
 'cefotaxime': ([('Intermittent', '500–1,000 mg daily'), ('Continuous', 'No data')], ''),
 'ceftazidime': ([('Intermittent', '1,000–1,500 mg daily (long dwell); 20 mg/kg daily (short dwell)'), ('Continuous', 'Loading 500 mg/L, then 125 mg/L')], RKF),
 'ceftriaxone': ([('Intermittent', '1,000 mg daily'), ('Continuous', 'No data')], ''),
 'benzylpenicillin': ([('Intermittent', 'No data'), ('Continuous', 'Loading 50,000 units/L, then 25,000 units/L')], ''),
 'amoxicillin': ([('Intermittent', 'No data'), ('Continuous', 'Maintenance 150 mg/L')], ''),
 'ampicillin': ([('Intermittent', '4 g daily'), ('Continuous', 'Maintenance 125 mg/L')], ' ISPD: IP ampicillin is not recommended for enterococcal peritonitis.'),
 'ampicillin-sulbactam': ([('Intermittent', 'Not stated'), ('Continuous', 'Loading 1,000 mg/500 mg, then 133.3 mg/66.7 mg')], ''),
 'piperacillin-tazobactam': ([('Intermittent', 'No data'), ('Continuous', 'Loading 4 g/0.5 g, then 1 g/0.125 g')], ''),
 'aztreonam': ([('Intermittent', '2 g daily'), ('Continuous', 'Loading 500 mg/L, then 250 mg/L')], ''),
 'ciprofloxacin': ([('Intermittent', 'No data'), ('Continuous', 'Maintenance 50 mg/L')], ''),
 'clindamycin': ([('Intermittent', 'No data'), ('Continuous', 'Maintenance 600 mg per bag')], ''),
 'daptomycin': ([('Intermittent', '300 mg daily'), ('Continuous', 'Loading 100 mg/L, then 20 mg/L')], ''),
 'fosfomycin': ([('Intermittent', '4 g daily'), ('Continuous', 'No data')], ' Requires an injectable fosfomycin product (not marketed in the US).'),
 'imipenem-cilastatin': ([('Intermittent', '500 mg in alternate exchanges'), ('Continuous', 'Loading 250 mg/L, then 50 mg/L')], ''),
 'ofloxacin': ([('Intermittent', 'No data'), ('Continuous', 'Loading 200 mg, then 25 mg/L')], ''),
 'polymyxin-b': ([('Intermittent', 'No data'), ('Continuous', 'Maintenance 300,000 units (30 mg) per bag')], ''),
 'meropenem': ([('Intermittent', '500 mg daily (long dwell, APD); 1,000 mg daily (short dwell, CAPD)'), ('Continuous', 'Maintenance 125 mg/L')], ''),
 'teicoplanin': ([('Intermittent', '15 mg/kg every 5 days'), ('Continuous', 'Loading 400 mg per bag, then 20 mg/L')], ''),
 'fluconazole': ([('Intermittent', 'IP 150–200 mg every 24–48 hours (oral route preferred)'), ('Continuous', 'No data')], ''),
 'voriconazole': ([('Intermittent', 'IP 2.5 mg/kg daily (oral route preferred)'), ('Continuous', 'No data')], ''),
 'tobramycin': ([('Intermittent', '0.6 mg/kg daily'), ('Continuous', 'Not advised')], ''),
}
changed = []
def add_ip(i, rows, extra):
    d = drugs[i]; pd = d['modalities']['pd']
    pd['tables'] = [T(IP, rows)] + pd['tables']
    pd['status'] = 'summarized'
    keep = re.sub(r'\s*(This is not intraperitoneal peritonitis treatment\.|Systemic adult PD mapping only\.)', '', pd['notes']).strip()
    if 'not_curated' in pd.get('_old', '') or 'No drug-specific renal dose' in keep: keep = ''
    pd['notes'] = (IPNOTE + extra + (' ' + keep if keep else '')).strip()
    for s in ['ispd2022', 'nm-ip-2025']:
        if s not in pd['sourceIds']: pd['sourceIds'].append(s)
        if s not in d['sourceIds']: d['sourceIds'].append(s)
    d['completeness'] = d['completeness'].replace('PD rows are systemic therapy, not intraperitoneal peritonitis therapy.', 'PD rows labelled ISPD are intraperitoneal peritonitis doses; other PD rows are systemic.')
    if d['entryType'] == 'catalog':
        d.update(entryType='renal', flag='monitor', kidneyMetric='PD peritonitis (ISPD 2022); systemic renal dosing not yet curated',
                 summary='Intraperitoneal PD peritonitis dosing only; systemic renal dosing not yet curated.',
                 jurisdiction='International guideline (ISPD). Jordan: confirm local product and protocol.',
                 completeness='Only ISPD intraperitoneal peritonitis dosing is curated. Systemic CKD and dialysis dosing remain uncurated.')
        d['review'] = dict(status='clinical_review_pending', sourceCheckedAt='2026-10-30', clinicalReviewer=None, clinicalApprovedAt=None)
        data['coverage']['renal'] += 1; data['coverage']['catalog'] -= 1; promoted.append(i)
    d['updatedInVersion'] = VERSION; changed.append(i)
promoted = []
for i, (rows, extra) in ip_table.items(): add_ip(i, rows, extra)

NC = 'No dosing source curated for this setting; consult renal pharmacy.'
# Vancomycin
v = drugs['vancomycin']; sv = label_source('vancomycin')
v['modalities']['ckd']['tables'] = [T('IV · US label', [('Any degree of renal impairment', 'Initial dose no less than 15 mg/kg, then adjust using serum concentrations'), ('Functionally anephric', '15 mg/kg initially, then 1.9 mg/kg every 24 hours')])] + v['modalities']['ckd']['tables']
v['modalities']['ckd']['sourceIds'] = [sv, 'v09-vancomycin']
v['modalities']['ihd'] = dict(status='summarized', sourceIds=['unmc-vanco-hd'], tables=[T('IV · stable maintenance haemodialysis · UNMC nephrology protocol', [
    ('Loading', '20 mg/kg IV once (minimum 1,000 mg, maximum 2,000 mg)'), ('Maintenance', '750 mg IV after each dialysis session (roughly 7–10 mg/kg)'),
    ('Pre-dialysis level >20 mcg/mL', 'Reduce the dose by 250 mg; recheck before the next session'), ('Pre-dialysis level 15–20 mcg/mL', 'Continue; check weekly'),
    ('Pre-dialysis level <15 mcg/mL', 'Increase the dose by 250 mg; recheck before the next session')])],
    notes='Target pre-dialysis level 15–20 mcg/mL. Draw it before the 2nd dialysis after the load, before the next session after any change, then weekly. Modern high-flux haemodialysis removes about 40%. Not for CRRT, PIRRT, PD or irregular haemodialysis.')
v['modalities']['pd'] = dict(status='summarized', sourceIds=['ispd2022', 'nm-ip-2025', 'v09-vancomycin'], tables=[
    T(IP, [('Intermittent, CAPD', '15–30 mg/kg IP every 5–7 days'), ('Intermittent, APD', '15 mg/kg IP every 4 days'), ('Continuous (all exchanges)', 'Loading 20–25 mg/kg, then 25 mg/L in each exchange')]),
    T('IV · systemic · UNMC protocol', [('PD', 'Measure serum levels to decide when to redose')])],
    notes=IPNOTE + ' ISPD: supplemental doses may be needed in APD. Northwestern guideline: consider redosing when the serum level is 15 mcg/mL or lower; intermittent dosing is preferred.')
v['kidneyMetric'] = 'CrCl · mL/min; serum vancomycin concentrations'
v['summary'] = 'IV: individualise by levels (anephric 1.9 mg/kg/day after 15 mg/kg); HD: load then 750 mg after each session; PD peritonitis: IP dosing per ISPD 2022.'
v['sourceIds'] = [sv, 'v09-vancomycin', 'unmc-vanco-hd', 'ispd2022', 'nm-ip-2025']

# Gentamicin
g = drugs['gentamicin']; sg = label_source('gentamicin')
g['modalities']['ckd'] = dict(status='summarized', sourceIds=[sg, 'v09-gentamicin'], notes=g['modalities']['ckd']['notes'], tables=[
    T('IV conventional dosing · US label', [('Interval method', 'Usual dose (e.g. 1 mg/kg) every (serum creatinine in mg/dL × 8) hours'), ('Reduced-dose method', 'After the usual first dose, give the usual dose ÷ serum creatinine every 8 hours'), ('Monitoring', 'Measure peak and trough levels; worsening renal function may need larger reductions')]),
    T('IV synergy dosing (1 mg/kg) · UNMC protocol', [('CrCl 51–90', 'Same dose every 12 hours'), ('CrCl 10–50', 'Same dose every 24 hours'), ('CrCl <10', 'Same dose every 48 hours')]),
    T('IV extended-interval dosing · UNMC protocol', [('Any CrCl', '7 mg/kg (adjusted body weight) once, then set the interval from a level 6–14 hours after the start of infusion (Hartford nomogram) or AUC 80–110')])])
g['modalities']['ihd'] = dict(status='summarized', sourceIds=[sg, 'v09-gentamicin'], notes='An 8-hour haemodialysis lowers serum gentamicin by about 50% (US label). Redose by levels.', tables=[
    T('IV · US label', [('After each haemodialysis', '1–1.7 mg/kg depending on severity of infection')]),
    T('IV · UNMC protocol', [('Traditional dosing', '1–2 mg/kg per dose; redose according to levels'), ('Synergy dosing', 'Same dose three times weekly')])])
g['modalities']['pd'] = dict(status='summarized', sourceIds=['ispd2022', 'nm-ip-2025', 'v09-gentamicin'], tables=[
    T(IP, [('Intermittent', '0.6 mg/kg IP daily'), ('Continuous', 'Not advised')]),
    T('IV · systemic · UNMC protocol', [('Traditional dosing', '1–2 mg/kg per dose; redose according to levels'), ('Synergy dosing', 'Same dose three times weekly')])],
    notes=IPNOTE + ' Northwestern guideline: with residual kidney function doses up to 0.9 mg/kg have been used; if continued while awaiting cultures, check a random level and redose when it is 0.5 mcg/mL or lower.')
g['kidneyMetric'] = 'Serum creatinine / CrCl · mL/min; serum gentamicin levels'
g['summary'] = 'Extend the interval or reduce the dose by renal function and levels; 1–1.7 mg/kg after each HD; PD peritonitis 0.6 mg/kg IP daily.'
g['flag'] = 'adjust'; g['sourceIds'] = [sg, 'v09-gentamicin', 'ispd2022', 'nm-ip-2025']

# Amikacin
a = drugs['amikacin']; sa = label_source('amikacin')
a['modalities']['ckd'] = dict(status='summarized', sourceIds=['v09-amikacin', sa], notes='Set the interval from a level 6–14 hours after the start of infusion (modified Hartford nomogram); a trough below 5 mg/L is probably less nephrotoxic (UNMC).', tables=[
    T('IV extended-interval · normal 15 mg/kg (adjusted body weight) every 24 h · UNMC protocol', [('CrCl >50–90', 'Consider a 20–25% reduction (12 or 15 mg/kg/day)'), ('CrCl 30–50', 'Reduce by 50% (7.5 mg/kg every 24 h or 15 mg/kg every 48 h)'), ('CrCl 10–30', 'Reduce by 67–75% (5 mg/kg every 24 h or 10 mg/kg every 48 h)'), ('CrCl <10', '7.5 mg/kg every 48 h; dose according to levels')]),
    T('IV/IM conventional dosing · US label', [('Loading', '7.5 mg/kg (the normal dose)'), ('Interval method', '7.5 mg/kg every (serum creatinine × 9) hours'), ('Reduced-dose method', 'Every 12 hours, reduced in proportion to CrCl, or normal dose ÷ serum creatinine'), ('During dialysis', 'Neither method applies')])])
a['modalities']['ihd'] = dict(status='summarized', sourceIds=['v09-amikacin'], notes='Dose according to levels.', tables=[T('IV · UNMC protocol', [('Haemodialysis', '10 mg/kg once, then 5 mg/kg after each dialysis')])])
a['modalities']['pd'] = dict(status='summarized', sourceIds=['ispd2022', 'nm-ip-2025', 'v09-amikacin'], notes=IPNOTE, tables=[
    T(IP, [('Intermittent', '2 mg/kg IP daily'), ('Continuous', 'Not advised')]), T('IV · systemic · UNMC protocol', [('PD', '10 mg/kg once, then 5 mg/kg after each dialysis (protocol wording)')])])
a['kidneyMetric'] = 'CrCl · mL/min; serum amikacin levels'
a['summary'] = 'Reduce dose/extend interval by CrCl and levels; HD 10 mg/kg then 5 mg/kg after each session; PD peritonitis 2 mg/kg IP daily.'
a['flag'] = 'adjust'; a['sourceIds'] = ['v09-amikacin', sa, 'ispd2022', 'nm-ip-2025']

# Tobramycin systemic (label) in addition to IP above
t = drugs['tobramycin']; st = label_source('tobramycin')
t['modalities']['ckd'] = dict(status='summarized', sourceIds=[st, 'v09-tobramycin'], notes=t['modalities']['ckd']['notes'], tables=[T('IV/IM conventional dosing · US label', [
    ('CrCl ≤70 mL/min (reduced dose, every 8 h)', 'Normal dose × the percentage from the label nomogram'), ('Interval method', 'Normal dose every (serum creatinine × 6) hours'), ('During dialysis', 'Neither method applies'), ('Obesity', 'Dose on lean body weight plus 40% of the excess')])])
t['sourceIds'] = list(dict.fromkeys([st] + t['sourceIds'])); t['flag'] = 'adjust'
for i in ['vancomycin', 'gentamicin', 'amikacin', 'tobramycin']:
    d = drugs[i]; d['updatedInVersion'] = VERSION
    d['review'] = dict(status='clinical_review_pending', sourceCheckedAt='2026-10-30', clinicalReviewer=None, clinicalApprovedAt=None)
    d['completeness'] = 'Selected adult systemic and intraperitoneal regimens. CRRT/PIRRT, paediatric and indication-specific targets are not covered; level monitoring is required.'
    if i not in changed: changed.append(i)

# Vonoprazan (P-CAB)
sv2 = label_source('vonoprazan')
pk_nc = dict(status='not_curated', value=None, context='Not yet curated. No value is inferred.', sourceIds=[])
vono = dict(id='vonoprazan', name='Vonoprazan', aliases=['Voquezna', 'Takecab'], category='Gastrointestinal', drugClass='Potassium-competitive acid blocker (P-CAB)',
    formulation='Oral tablets (Voquezna, US label)', routes=['Oral'], otc=False, kidneyMetric='eGFR · mL/min (label)',
    summary='Halve the erosive-oesophagitis healing dose at eGFR <30; H. pylori regimens not recommended at eGFR <30.', flag='adjust', entryType='renal', sharedGuidanceId=None,
    modalities=dict(
        ckd=dict(status='summarized', sourceIds=[sv2], notes='', tables=[
            T('Healing of erosive oesophagitis · US label', [('eGFR ≥30', '20 mg once daily for 8 weeks'), ('eGFR <30', '10 mg once daily')]),
            T('Maintenance of healed oesophagitis / non-erosive reflux · US label', [('Any degree of renal impairment', 'No adjustment (10 mg once daily)')]),
            T('H. pylori (with amoxicillin ± clarithromycin) · US label', [('eGFR ≥30', 'Usual regimen'), ('eGFR <30', 'Not recommended')])]),
        ihd=dict(status='not_curated', tables=[], notes=NC, sourceIds=[]), crrt=dict(status='not_curated', tables=[], notes=NC, sourceIds=[]),
        pd=dict(status='not_curated', tables=[], notes=NC, sourceIds=[]), sled=dict(status='not_curated', tables=[], notes=NC, sourceIds=[])),
    considerations='Also reduce the healing dose in moderate–severe hepatic impairment. Check the amoxicillin and clarithromycin labels for their own renal adjustments.',
    sourceIds=[sv2], labelSearchUrl='https://dailymed.nlm.nih.gov/dailymed/search.cfm?query=Vonoprazan',
    review=dict(status='clinical_review_pending', sourceCheckedAt='2026-10-30', clinicalReviewer=None, clinicalApprovedAt=None),
    completeness='Renal statements from the current US label only. Dialysis settings are not covered.', addedInVersion=VERSION,
    jurisdiction='US FDA label. Jordan: confirm against the JFDA-approved leaflet of the product dispensed.',
    referenceChecks=dict(bnf=dict(edition='92 (September 2026)', status='comparison_pending', reason='BNF comparison not yet done.'), pdr=dict(status='not_checked')),
    pharmacokinetics=dict(status='not_curated', sourceCheckedAt=None, halfLife=dict(pk_nc), renalHalfLife=dict(pk_nc), volumeOfDistribution=dict(pk_nc), proteinBinding=dict(pk_nc),
        dialysability={k: dict(status='not_curated', value=None, context='Modality-specific removal data have not been curated.', sourceIds=[]) for k in ['ihd', 'pd', 'crrt', 'sled']},
        notes='No pharmacokinetic value or dialytic removal is inferred from another drug or drug class.'))
data['drugs'].append(vono); data['drugs'].sort(key=lambda d: d['name'].lower()); changed.append('vonoprazan')
data['coverage']['renal'] += 1

# Pregnancy and lactation excerpts (quoted from the cited label; not a risk grade).
preg_count = 0
for i, e in labels.items():
    if i not in drugs and i != 'vonoprazan': continue
    d = next(x for x in data['drugs'] if x['id'] == i)
    sid = e['sourceId'] if e['sourceId'] in sources else None
    if sid is None:
        sid = next((s for s in d['sourceIds'] if s.startswith(('us120-', 'uk120-', 'us121-'))), None)
    if not sid or not (e.get('pregnancy') or e.get('lactation')): continue
    d['pregnancyLactation'] = dict(status='label_excerpt', sourceIds=[sid], fdaLetterCategory=e.get('letter'),
        pregnancy=e.get('pregnancy'), lactation=e.get('lactation'), checkedAt=DATE,
        note='Quoted from the cited label. The FDA retired the A/B/C/D/X letter categories; a letter is shown only where this label still prints one. Not yet reviewed; safer alternatives are not listed.')
    preg_count += 1

data['sources'] = list(sources.values())
data.update(version=VERSION, clinicalDataVersion=VERSION, softwareReleaseDate=DATE)
data['clinicalUpdates'] = dict(version=VERSION, changedIds=changed, newRenalIds=['vonoprazan'] + promoted, newPKIds=[], newPDIds=[i for i in changed if i != 'vonoprazan'],
    scope='Vancomycin and aminoglycosides with numeric CKD/HD/PD dosing; ISPD 2022 intraperitoneal peritonitis doses; vonoprazan; pregnancy/lactation label excerpts.')
data['releaseChanges'] = dict(version=VERSION, changedIds=changed, newRenalIds=['vonoprazan'], newPKIds=[], pirrtSummaryIds=[], note=data['clinicalUpdates']['scope'])
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
queue = json.loads((D/'CURATION_QUEUE.json').read_text()); queue['version'] = VERSION
byid = {d['id']: d for d in data['drugs']}
for q in queue['drugs']:
    if q['id'] in changed: q['modalities'] = {k: m['status'] for k, m in byid[q['id']]['modalities'].items()}
    if q['id'] in promoted: q['content'] = 'renal'
queue['drugs'].append(dict(id='vonoprazan', name='Vonoprazan', category='Gastrointestinal', content='renal', modalities={k: m['status'] for k, m in vono['modalities'].items()}))
(D/'CURATION_QUEUE.json').write_text(json.dumps(queue, ensure_ascii=False, indent=2))
rem = json.loads((D/'REMAINING_MEDICATIONS.json').read_text()); rem['version'] = VERSION
rem['remaining'] = [x for x in rem['remaining'] if x['id'] not in promoted]
(D/'REMAINING_MEDICATIONS.json').write_text(json.dumps(rem, ensure_ascii=False, indent=2))

header = f'''# RenalRounds v{VERSION} · 31 October 2026

- **Vancomycin, gentamicin, amikacin and tobramycin** now have numeric dosing: US label renal methods, Nebraska Medicine/UNMC renal and haemodialysis protocols (vancomycin: 20 mg/kg load, 750 mg after each session, adjusted by pre-dialysis level), and systemic PD doses.
- **PD peritonitis:** intraperitoneal doses from the ISPD 2022 guideline (Table 5) were added to the PD tab of {len(ip_table) + 3} antibiotics, clearly labelled and separate from systemic PD doses.
- **Vonoprazan** (potassium-competitive acid blocker) added from its US label; searchable as "P-CAB".
- **Pregnancy and lactation:** a new section quotes the pregnancy and lactation statements of the cited label for {preg_count} entries. The FDA retired the A/B/C/D/X letters; a letter appears only where the label still prints one.
- The back arrow is an icon in the lower-left corner again and hides while scrolling down.

'''
for target, base in [('CHANGELOG.md', 'changelog_v120.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v120.md'), ('SOURCE_AUDIT.md', 'source_audit_v120.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'COMPLETION_PLAN.md').write_text(header + '## Remaining clinical work\n\nPregnancy/lactation for the remaining entries and a decision on letter grading; safer-alternative lists with clinical review; rebuild handbook-cited PK values from labels; nephrologist and JFDA reviews; catalog-only entries by risk; CRRT/SLED coverage.\n')
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v121.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v121.py. checks_v121.mjs checks the ISPD Table 5 values, the vancomycin/aminoglycoside numbers against their sources, the vonoprazan label table, that pregnancy excerpts are verbatim substrings of the stored label text, and that all other entries are unchanged from v0.12.0.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, changed=len(changed), ip=len(ip_table) + 3, pregnancy=preg_count, drugs=len(data['drugs']))))
