"""Build interactions_vNNN.json: verbatim drug-interaction sentences from each priority drug's current label, the FDA CYP/transporter
roles (FDA 'Examples of drugs that interact with CYP enzymes and transporter systems', Table 1) and class phrases used by the checker.
Needs the labels folder and the parsed FDA table; the build only reads the output file.
Usage: python3 extract_interactions.py interactions_vNNN.json /path/to/labels /path/to/fda_cyp.json"""
import json, re, sys, html
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(__file__).parent; OUT, LAB, FDA = R/sys.argv[1], Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text())
db = json.loads((R/'dist'/'database.json').read_text()); D = {d['id']: d for d in db['drugs']}
src = {s['id']: s for s in db['sources']}
NEWIDS = ['lomitapide', 'belumosudil', 'aprocitentan', 'sotagliflozin', 'vericiguat', 'mavacamten', 'evinacumab']
PRIORITY = '''tacrolimus cyclosporine sirolimus everolimus mycophenolate-mofetil mycophenolate-sodium azathioprine belatacept voclosporin belumosudil
captopril enalapril lisinopril ramipril perindopril candesartan irbesartan losartan telmisartan valsartan olmesartan sacubitril-valsartan aliskiren
amlodipine nifedipine felodipine diltiazem verapamil atenolol bisoprolol metoprolol carvedilol nebivolol propranolol labetalol
hydrochlorothiazide chlorthalidone indapamide furosemide torsemide bumetanide spironolactone eplerenone finerenone amiloride triamterene
clonidine methyldopa hydralazine minoxidil-systemic doxazosin prazosin aprocitentan
cetirizine-oral levocetirizine loratadine desloratadine fexofenadine chlorphenamine diphenhydramine hydroxyzine montelukast
rifampicin rifabutin carbamazepine phenytoin phenobarbital enzalutamide
clarithromycin erythromycin itraconazole voriconazole posaconazole fluconazole isavuconazonium ritonavir nirmatrelvir-ritonavir darunavir amiodarone dronedarone
digoxin warfarin apixaban rivaroxaban dabigatran edoxaban atorvastatin simvastatin rosuvastatin colchicine ticagrelor clopidogrel trimethoprim lomitapide'''.split()
CLASSES = {
 'ACE inhibitors': (r'\bACE inhibitors?|angiotensin[- ]converting[- ]enzyme', 'captopril enalapril enalaprilat lisinopril ramipril perindopril'),
 'Angiotensin receptor blockers': (r'angiotensin (?:II )?receptor (?:blockers?|antagonists?)|\bARBs?\b', 'candesartan irbesartan losartan telmisartan valsartan olmesartan sacubitril-valsartan'),
 'Renin–angiotensin system inhibitors': (r'renin[- ]angiotensin|\bRAAS?\b|\bRAS inhibit', 'captopril enalapril lisinopril ramipril perindopril candesartan irbesartan losartan telmisartan valsartan olmesartan sacubitril-valsartan aliskiren'),
 'Potassium-sparing diuretics / potassium': (r'potassium[- ]sparing|potassium supplement|potassium-containing|salt substitutes?', 'amiloride triamterene spironolactone eplerenone finerenone potassium-chloride potassium-citrate potassium-containing-salt-substitutes'),
 'Mineralocorticoid receptor antagonists': (r'mineralocorticoid receptor antagonist|aldosterone (?:receptor )?antagonist', 'spironolactone eplerenone finerenone'),
 'NSAIDs': (r'\bNSAIDs?\b|non-?steroidal anti-?inflammatory', 'ibuprofen naproxen diclofenac-systemic celecoxib meloxicam ketorolac etoricoxib aspirin'),
 'Diuretics': (r'\bdiuretics?\b', 'furosemide torsemide bumetanide hydrochlorothiazide chlorthalidone indapamide metolazone'),
 'Beta-blockers': (r'beta[- ]?(?:adrenergic[- ])?block|β-?blocker', 'atenolol bisoprolol metoprolol carvedilol nebivolol propranolol labetalol sotalol esmolol'),
 'Calcium-channel blockers': (r'calcium[- ]channel block', 'amlodipine nifedipine felodipine nicardipine diltiazem verapamil'),
 'Statins': (r'\bstatins?\b|HMG-CoA reductase', 'atorvastatin simvastatin rosuvastatin pravastatin fluvastatin pitavastatin'),
 'Anticoagulants': (r'anticoagulant', 'warfarin apixaban rivaroxaban dabigatran edoxaban heparin enoxaparin'),
 'Antiplatelet drugs': (r'antiplatelet|platelet (?:aggregation )?inhibitor', 'aspirin clopidogrel ticagrelor prasugrel'),
 'Macrolide antibiotics': (r'macrolide', 'clarithromycin erythromycin azithromycin'),
 'Azole antifungals': (r'azole antifungal', 'itraconazole voriconazole posaconazole fluconazole isavuconazonium'),
 'CNS depressants / sedatives': (r'CNS depressants?|\bsedatives?\b|tranquili[sz]ers?|\bhypnotics?\b|\balcohol\b', 'alprazolam diazepam lorazepam midazolam zolpidem chlorphenamine diphenhydramine hydroxyzine promethazine morphine oxycodone hydromorphone fentanyl tramadol-ir methadone gabapentin pregabalin'),
 'Calcineurin inhibitors / immunosuppressants': (r'calcineurin inhibitor|immunosuppressants?\b', 'tacrolimus cyclosporine voclosporin'),
}
def fda_ids(pred):
    out = set()
    for name, roles in FDA['rows'].items():
        i = FDA['mapped'].get(name)
        if i and any(pred(r) for r in roles): out.add(i)
    return out
is3A = lambda r: '3A' in r['enzymes']
CYP = {
 'Strong CYP3A inhibitors': (r'strong CYP3A4? inhibitor', fda_ids(lambda r: r['col'] == 'strong_inhibitor' and is3A(r))),
 'CYP3A inhibitors': (r'CYP3A4? inhibitor|inhibitors? of CYP3A4?', fda_ids(lambda r: r['col'] in ('strong_inhibitor', 'moderate_inhibitor') and is3A(r))),
 'CYP3A inducers': (r'CYP3A4? inducer|inducers? of CYP3A4?|strong (?:CYP3A4? )?inducer', fda_ids(lambda r: r['col'] in ('strong_inducer', 'moderate_inducer') and is3A(r))),
 'P-gp inhibitors': (r'P-?g(?:p|lycoprotein) (?:\(P-gp\) )?inhibitor|inhibitors? of P-?gp', fda_ids(lambda r: r['col'] == 'transporter_inhibitor' and 'P-gp' in r['enzymes'])),
}
CYP['CYP3A inhibitors'][1].add('nirmatrelvir-ritonavir'); CYP['Strong CYP3A inhibitors'][1].add('nirmatrelvir-ritonavir')
for k, (rx, mem) in CLASSES.items(): CLASSES[k] = (rx, sorted(set(mem.split())))
for k, (rx, mem) in CYP.items(): CYP[k] = (rx, sorted(mem))
def text_of(d, section):
    if section and d.get(section): parts = d[section]
    elif d.get('label_text'):
        t = ' '.join(d['label_text'])
        m = re.search(r'7\.?\s*DRUG INTERACTIONS(.*?)(?:\s8\.?\s*USE IN SPECIFIC POPULATIONS|$)', t, re.S) or re.search(r'4\.5\.?\s*Interaction with other medicinal products(.*?)\s4\.6\.?\s', t, re.S | re.I)
        parts = [m.group(1)] if m else []
    else: parts = []
    t = html.unescape(re.sub(r'</?[a-zA-Z][^<>]*>', ' ', ' '.join(str(x) for x in parts)))
    return re.sub(r'\s+', ' ', t).strip()
def label_for(i):
    setids = {src[s].get('label', {}).get('setid') for s in D[i]['sourceIds'] if s in src} if i in D else set()
    found = []
    for folder in ('ix', 'us', 'us2', 'us3', 'extra', 'alt', 'preg', 'uk3'):
        f = LAB/folder/f'{i}.json'
        if f.exists():
            d = json.loads(f.read_text()); d = d[0] if isinstance(d, list) else d
            if folder == 'ix' or d.get('set_id') in setids: return folder, d
            found.append((folder, d))
    return found[0] if found else (None, None)
names = {}
for d in db['drugs']:
    for n in [d['name'].split(' (')[0]] + d.get('aliases', []):
        n = n.strip()
        if len(n) >= 5 and not re.search(r'vaccine|supplement|oral|topical|nasal', n, re.I): names.setdefault(n.lower(), d['id'])
NAME_RX = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, names), key=len, reverse=True)) + r')\b', re.I)
TERMS = re.compile('|'.join(rx for rx, _ in list(CLASSES.values()) + list(CYP.values())), re.I)
WEIGHT = [(r'contraindicat', 6), (r'\bavoid', 5), (r'not recommended', 5), (r'(?:reduce|decrease|lower|adjust)[^.]{0,30}dos', 4), (r'monitor', 2), (r'increase', 1), (r'hyperkal', 3)]
res = {}
for i in PRIORITY:
    if i not in D and i not in NEWIDS: print('skip', i); continue
    folder, d = label_for(i)
    if not d: print('no label', i); continue
    t = text_of(d, 'drug_interactions')
    otc = False
    if not t and d.get('label_text') is None:
        t = text_of(d, 'precautions')
        if not t: t = (text_of(d, 'do_not_use') + ' ' + text_of(d, 'ask_doctor_or_pharmacist')).strip(); otc = bool(t)
    if d.get('precautions') and d.get('label_text') is None:
        pt = text_of(d, 'precautions'); m = re.search(r'Drug Interactions(.*?)(?:Carcinogenesis|Pregnancy|Information for Patients|Laboratory Tests|$)', pt)
        if m and m.group(1).strip() and m.group(1).strip() not in t: t = (t + ' |SPLIT| ' + m.group(1).strip()).strip()
    t = re.sub(r'(?<=[.)\]])\s+(?=\d+(?:\.\d+)+\s+[A-Z])', ' |SPLIT| ', t)
    sents = [s.strip() for s in re.split(r'(?<=[a-z0-9\)\]%])\.\s+(?=[A-Z])|\s\|SPLIT\|\s|\s•\s', t) if 30 <= len(s.strip()) <= 700]
    scored = []
    for k, s in enumerate(sents):
        partners = {names[m.group(1).lower()] for m in NAME_RX.finditer(s)} - {i}
        if not partners and not TERMS.search(s) and not otc: continue
        score = sum(w for rx, w in WEIGHT if re.search(rx, s, re.I)) + min(len(partners), 3)
        s = re.sub(r'^\d+(?:\.\d+)*\s+', '', s).strip()
        if len(s) >= 30: scored.append((score, k, s))
    keep = sorted(sorted(scored, reverse=True)[:12], key=lambda x: x[1])
    full = re.sub(r'\s+', ' ', html.unescape(re.sub(r'</?[a-zA-Z][^<>]*>', ' ', ' '.join(' '.join(map(str, v)) for k, v in d.items() if isinstance(v, list) and k != 'openfda'))))
    for _, _, s in keep: assert s in full, (i, s[:80])
    o = d.get('openfda', {})
    res[i] = dict(label=f'{folder}/{i}.json', meta=dict(setid=d.get('set_id'), splVersion=str(d.get('version')), effective=f"{d['effective_time'][:4]}-{d['effective_time'][4:6]}-{d['effective_time'][6:8]}",
        manufacturer=(o.get('manufacturer_name') or [''])[0], brand=(o.get('brand_name') or [''])[0], application=(o.get('application_number') or [''])[0],
        url=d.get('source_url') or f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={d.get('set_id')}", **({'type': d['source_type']} if d.get('source_type') else {})),
        statements=[s for _, _, s in keep])
roles = {}
for name, rs in FDA['rows'].items():
    i = FDA['mapped'].get(name)
    if i: roles.setdefault(i, []).extend(r['text'].replace('  ', ' ') for r in rs)
for a, b in [('ritonavir', 'nirmatrelvir-ritonavir'), ('dabigatran etexilate', 'dabigatran'), ('glyburide', 'glibenclamide-glyburide'), ('lomitapide', 'lomitapide'), ('belumosudil', 'belumosudil'), ('isavuconazole', 'isavuconazonium')]:
    key = next((n for n in FDA['rows'] if re.sub(r'\s+', ' ', n.replace('\xa0', ' ')).lower() == a), None)
    if key: roles.setdefault(b, []).extend(r['text'] for r in FDA['rows'][key] if r['text'] not in roles.get(b, []))
OUT.write_text(json.dumps(dict(drugs=res, roles=roles, classes={k: dict(pattern=v[0], members=v[1]) for k, v in {**CLASSES, **CYP}.items()}), ensure_ascii=False, indent=1))
print(len(res), 'drugs;', sum(len(v['statements']) for v in res.values()), 'statements;', len(roles), 'FDA roles')
