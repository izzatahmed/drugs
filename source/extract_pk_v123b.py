"""Second pass for PK fields still blank after extract_pk_v123.py: list every candidate sentence
(broader patterns) so a reviewer can accept or reject each one. Accepted values go into
pk_review_v123b.json with the verbatim sentence; nothing here is published automatically.
Usage: python3 extract_pk_v123b.py /path/to/labels pending.json  → pk_candidates_v123b.json
"""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
LAB = Path(sys.argv[1]); pend = json.loads(Path(sys.argv[2]).read_text()); R = Path(__file__).parent
KEYS = ('clinical_pharmacology', 'pharmacokinetics', 'overdosage', 'use_in_specific_populations', 'precautions', 'warnings',
        'warnings_and_cautions', 'dosage_and_administration', 'description')
def label_text(i):
    for sub in ('us', 'preg'):
        f = LAB/sub/f'{i}.json'
        if f.exists():
            d = json.loads(f.read_text()); d = d[0] if isinstance(d, list) else d
            return ' '.join(' '.join(d[k]) if isinstance(d.get(k), list) else str(d.get(k, '')) for k in KEYS)
    return ''
def sentences(t):
    t = re.sub(r'\s+', ' ', t)
    return [s.strip() for s in re.split(r'(?<=[a-z0-9\)\]%])\.\s+(?=[A-Z])', t) if 15 < len(s) < 700]
NUM = r'\d+(?:\.\d+)?(?:\s*(?:±|to|-|–|and)\s*\d+(?:\.\d+)?)?'
TRIG = dict(halfLife=r'half[- ]?li(?:fe|ves)|t ?1/2|t½', renalHalfLife=r'half[- ]?li(?:fe|ves)|t ?1/2|t½',
            volumeOfDistribution=r'volume of distribution|\bV(?:d|ss|z|ss/F|z/F|d/F)\b', proteinBinding=r'bound|binding',
            **{'dial-ihd': r'hemodialy|haemodialy|dialy[sz]', 'dial-pd': r'peritoneal dialysis|CAPD'})
VAL = dict(halfLife=NUM + r'\s*(?:hours?|hrs?|h\b|days?|minutes?|min\b)', volumeOfDistribution=NUM + r'\s*(?:L/kg|L\b|liters?|litres?|mL/kg)',
           proteinBinding=NUM + r'\s*%')
VAL['renalHalfLife'] = VAL['halfLife']
RENAL = r'renal (?:impairment|failure|insufficiency|dysfunction)|end[- ]stage renal|ESRD|anuric|creatinine clearance|uremic|hemodialysis'
out = {}
for i, fields in pend.items():
    ss = sentences(label_text(i)); out[i] = {}
    for f in fields:
        c = []
        for s in ss:
            if not re.search(TRIG[f], s, re.I): continue
            if f == 'proteinBinding' and not re.search(r'protein|albumin|plasma', s, re.I): continue
            if f == 'renalHalfLife' and not re.search(RENAL, s, re.I): continue
            if f.startswith('dial'): c.append(dict(value=None, sentence=s[:500])); continue
            v = re.findall(VAL[f], s, re.I)
            if v: c.append(dict(value=v[:3], sentence=s[:500]))
        out[i][f] = c[:4]
(R/'pk_candidates_v123b.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(sum(len(c) for x in out.values() for c in x.values()), 'candidates for', sum(1 for x in out.values() for c in x.values() if c), 'fields')
