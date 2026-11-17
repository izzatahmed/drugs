"""Cross-links between RenalRounds and Dalil (دليل الادوية الاردني, izzatahmed.github.io/dalil).
Writes (1) renalrounds_links.json for Dalil: ingredient keys -> RenalRounds entries, matched in the browser;
(2) jordan_products_vNNN.json for RenalRounds: per drug, the JFDA-registered products in Dalil's catalogue snapshot.
Usage: python3 build_dalil_links.py /path/to/dalil/catalogue.json jordan_products_vNNN.json /path/to/renalrounds_links.json"""
import json, re, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(__file__).parent; CAT, OUT, LINKS = Path(sys.argv[1]), R/sys.argv[2], Path(sys.argv[3])
db = json.loads((R/'dist'/'database.json').read_text()); cat = json.loads(CAT.read_text())
SYN = {'hct': 'hydrochlorothiazide', 'acetaminophen': 'paracetamol', 'albuterol': 'salbutamol', 'glyburide': 'glibenclamide', 'rifampin': 'rifampicin',
       'clavulanate': 'clavulanic', 'epinephrine': 'adrenaline', 'norepinephrine': 'noradrenaline', 'cyclosporin': 'cyclosporine', 'ciclosporin': 'cyclosporine',
       'colecalciferol': 'cholecalciferol', 'sulphate': 'sulfate', 'sulphamethoxazole': 'sulfamethoxazole', 'frusemide': 'furosemide', 'lignocaine': 'lidocaine', 'thyroxine': 'levothyroxine', 'chlorpheniramine': 'chlorphenamine',
       'cetirizine dihydrochloride': 'cetirizine', 'mesalamine': 'mesalazine', 'ursodiol': 'ursodeoxycholic', 'valproic': 'valproate', 'co amoxiclav': 'amoxicillin clavulanic'}
SKIP_WORDS = {'oral', 'iv', 'systemic', 'topical', 'nasal', 'inhaled', 'injection', 'tablets', 'tablet', 'xl', 'er', 'ir', 'sc', 'im', 'dialysis', 'formulation', 'high', 'dose', 'adjuvanted', 'recombinant'}
GENERIC = {'iron', 'zinc', 'calcium', 'magnesium', 'potassium', 'sodium', 'vitamin', 'insulin', 'st'}
def norm(s):
    s = re.sub(r'[^a-z ]', ' ', s.lower()); s = re.sub(r'\s+', ' ', s).strip()
    for a, b in SYN.items(): s = re.sub(rf'\b{a}\b', b, s)
    return s
def keys_for(d):
    if d['category'] == 'Vaccines' or d['entryType'] == 'safety' and d['category'] == 'OTC & medicine safety' and 'supplement' in d['id']: return None, []
    base = d['name'].split(' (')[0]
    parts = re.split(r'\s*/\s*|\s+\+\s+|\s+and\s+', base)
    out = []
    for p in parts:
        w = [x for x in norm(p).split() if x not in SKIP_WORDS]
        if w:
            k = ' '.join(w[:2]) if w[0] in ('insulin', 'vitamin', 'ferrous', 'iron', 'st', 'sodium', 'potassium', 'calcium', 'magnesium', 'folic', 'zinc', 'human') else w[0]
            if k not in out: out.append(k)
    combo = len(out) > 1
    if not combo:
        for a in d.get('aliases', []):
            if re.fullmatch(r'[A-Za-z][a-z]+(?: [a-z]+)?', a) and len(a) >= 5:
                a = norm(a); a = a if a.split()[0] in ('insulin', 'vitamin') else a.split()[0]
                if a not in out and a not in SKIP_WORDS and a not in GENERIC and len(a) >= 4: out.append(a)
    return (out if combo else None), out
INJ = re.compile(r'inject|infus|vial|ampoule|ampule|i\.?v|syringe|pen\b|lyophil|concentrate for', re.I)
INH = re.compile(r'inhal|nebul|aerosol|rotacap|diskus|turbuhaler|ellipta|breezhaler', re.I)
EYE = re.compile(r'eye|ophthalm|ocular|s\.d\.u', re.I)
NOSE = re.compile(r'nasal|nose', re.I)
RECT = re.compile(r'rectal|suppos|enema', re.I)
TOP = re.compile(r'cream|ointment|gel\b|emulgel|lotion|topical|patch|eye|ear|nasal|vaginal|shampoo|spray|drops', re.I)
def form_kind(form):
    form = form or ''
    return 'inj' if INJ.search(form) else 'inh' if INH.search(form) else 'rect' if RECT.search(form) else 'eye' if EYE.search(form) else 'nose' if NOSE.search(form) else 'top' if TOP.search(form) else 'oral'
def fit(d, kind):
    r = set(d.get('routes', []))
    return {'inj': 'Parenteral' in r, 'inh': 'Inhaled' in r, 'rect': bool(r & {'Rectal', 'Oral'}), 'eye': 'Ophthalmic' in r, 'nose': 'Nasal' in r, 'top': bool(r & {'Topical', 'Nasal', 'Ophthalmic', 'Transdermal'}), 'oral': 'Oral' in r}[kind]
def raw_components(sci):
    sci = re.sub(r'(?<=[a-z]{3})\s*/\s*(?=[a-z]{4})', ',', sci or '', flags=re.I)
    out = []
    for x in re.split(r',|\+|&|\band\b', sci, flags=re.I):
        c = norm(x)
        if c and not re.fullmatch(r'(?:mg|ml|g|iu|mcg|tab|cap|one|unit|units|w|v| )+', c): out.append((c, re.sub(r'\s+', ' ', re.sub(r'[^a-z ]', ' ', x.lower())).strip()))
    return out
def components(sci): return [c for c, _ in raw_components(sci)]
def brand(r): return re.sub(r'^[^\w]+|[^\w]+$', '', r['brand'].split(' ')[0]) or r['brand']
def comp_has(comp, key): return comp == key or comp.startswith(key + ' ') or (' ' + key + ' ') in (' ' + comp + ' ')
entries = []
for d in db['drugs']:
    combo, keys = keys_for(d)
    if not keys: continue
    entries.append(dict(id=d['id'], name=d['name'], keys=keys, combo=combo, routes=d.get('routes', []), flag=d['flag'], entryType=d['entryType']))
by_key = collections.defaultdict(list)
for e in entries:
    if not e['combo']:
        for k in e['keys']: by_key[k].append(e)
# Match every catalogue record: single-ingredient records to single entries, multi-ingredient records to combination entries and (as combinations) to each single entry.
prod = collections.defaultdict(lambda: dict(single=set(), combo=set(), brands=collections.Counter()))
rec_links = {}
qwords = collections.defaultdict(collections.Counter)
for r in cat['records']:
    rc = raw_components(r.get('scientific')); comps = [c for c, _ in rc]
    if not comps: continue
    kind = form_kind(r.get('form'))
    matched_single = []
    for c, raw in rc:
        cands = {e['id']: e for k, es in by_key.items() if comp_has(c, k) for e in es}
        if not cands: continue
        fitting = [e for e in cands.values() if fit(e, kind)] or ([] if kind in ('top', 'eye', 'nose') else list(cands.values()))
        if not fitting: continue
        if len(fitting) > 1:
            longest = max(len(k) for e in fitting for k in e['keys'] if comp_has(c, k))
            fitting = [e for e in fitting if any(len(k) == longest and comp_has(c, k) for k in e['keys'])]
        matched_single.append(fitting)
        for e in fitting: qwords[e['id']][next((k for k in e['keys'] if (' ' + k + ' ') in (' ' + raw + ' ')), ' '.join([w for w in raw.split() if w not in ('dried', 'as', 'the')][:2]))] += 1
    linked = [e['id'] for es in matched_single for e in es]
    combos = [e for e in entries if e['combo'] and len(e['combo']) == len(comps) and all(any(comp_has(c, k) for c in comps) for k in e['combo'])] if len(comps) > 1 else \
             [e for e in entries if e['combo'] and len(comps) == 1 and all(comp_has(comps[0], k) for k in e['combo'])]  # "Sacubitril Valsartan 200 (...)" written as one component
    if combos: linked = [e['id'] for e in combos] + linked
    if linked: rec_links[r['id']] = list(dict.fromkeys(linked))
    if len(comps) == 1 and combos:
        for e in combos: prod[e['id']]['single'].add(r['id']); prod[e['id']]['brands'][brand(r)] += 1
        for e in (matched_single[0] if matched_single else []): prod[e['id']]['combo'].add(r['id'])
    elif len(comps) == 1:
        for e in (matched_single[0] if matched_single else []):
            prod[e['id']]['single'].add(r['id']); prod[e['id']]['brands'][brand(r)] += 1
    else:
        for es in matched_single:
            for e in es: prod[e['id']]['combo'].add(r['id'])
        for e in entries:
            if e['combo'] and len(e['combo']) == len(comps) and all(any(comp_has(c, k) for c in comps) for k in e['combo']):
                prod[e['id']]['single'].add(r['id']); prod[e['id']]['brands'][brand(r)] += 1
meta = cat['meta']
res = {}
for e in entries:
    p = prod.get(e['id'])
    if not p or not (p['single'] or p['combo']): continue
    q = ' '.join(e['combo']) if e['combo'] else (qwords[e['id']].most_common(1)[0][0] if qwords[e['id']] else e['keys'][0])
    res[e['id']] = dict(query=q, products=len(p['single']), combinations=len(p['combo']), brands=[b for b, _ in p['brands'].most_common(8)])
OUT.write_text(json.dumps(dict(source=dict(title=meta['sourceTitle'], fileLabelDate=meta['fileLabelDate'], retrievedOn=meta['retrievedOn'], sha256=meta['sha256'], records=meta['recordCount']), drugs=res), ensure_ascii=False, indent=1))
used = sorted({i for v in rec_links.values() for i in v}); idx = {i: n for n, i in enumerate(used)}; names = {e['id']: e['name'] for e in entries}
LINKS.write_text(json.dumps(dict(title='RenalRounds', version=db['version'], base='https://izzatahmed.github.io/drugs/#drug=',
    catalogueSha256=meta['sha256'], drugs=[[i, names[i]] for i in used], records={rid: [idx[i] for i in v] for rid, v in rec_links.items()}), ensure_ascii=False, separators=(',', ':')))
print(len(res), 'RenalRounds entries with Jordan products;', sum(v['products'] for v in res.values()), 'product matches;', len([r for r in cat['records'] if components(r.get('scientific'))]), 'records with ingredients')
