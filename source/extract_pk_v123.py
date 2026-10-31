"""Replace handbook-cited pharmacokinetic fields with statements from current labels.
For each field, the value is a short phrase taken from one label sentence, and the sentence itself is
kept verbatim as evidence. Fields the label does not state become "not reported".
Usage: python3 extract_pk_v123.py /path/to/labels   (writes pk_extract_v123.json; needs no network)
"""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
LAB = Path(sys.argv[1]); R = Path(__file__).parent
db = json.loads((R/'dist'/'database.json').read_text())
PK_KEYS = ('clinical_pharmacology', 'pharmacokinetics', 'overdosage', 'use_in_specific_populations', 'precautions', 'warnings', 'warnings_and_cautions', 'dosage_and_administration')

def sentences(text):
    text = re.sub(r'\s+', ' ', text)
    return [s.strip() for s in re.split(r'(?<=[a-z0-9\)\]%])\.\s+(?=[A-Z])', text) if 20 < len(s) < 600]

NUM = r'(?:\d+(?:\.\d+)?)(?:\s*(?:±|to|-|–)\s*\d+(?:\.\d+)?)?'
Q = r'(?:approximately |about |an average of |a mean of |on average |mean |average |greater than |more than |less than |>\s*|<\s*|≥\s*|~\s*)?'
UNIT_T = r'(?:hours?|hrs?|h\b|days?|minutes?|min\b)'
BAD = r'pediatric|paediatric|child|neonat|infant|ECMO|rats?\b|dogs?\b|mice|animal|distribution phase|distribution half|initial|alpha|α|beta-half|β-half|metabolite|hepatic|cirrho|elderly|geriatric|after removal|overdose|Parameter|Table|Dosing Interval'
def drug_ok(s, name):
    m = re.search(r'half[- ]?life of ([a-z][a-z\- ]{2,40}?)(?: is| was| in| after| following| averag| rang|,|\()', s, re.I)
    return (not m) or any(t in m.group(1).lower() for t in name.lower().split()[:2]) or m.group(1).lower().strip() in ('elimination', 'the drug', 'the parent')
def pick(sents, key, name):
    for s in sents:
        if key in ('halfLife', 'renalHalfLife') and re.search(BAD, s, re.I): continue
        if key == 'halfLife':
            if re.search(RENAL, s, re.I) or not drug_ok(s, name): continue
            m = re.search(r'(?:elimination |terminal |plasma |serum |apparent |mean |effective |overall )*half[- ]?life(?: \(t ?1/2\)| \(t½\))?(?: of [a-z\- ]{2,40}?)?(?: in (?:healthy|normal|adult)[a-z ]{0,40}?)? (?:is|was|averages?|averaged|ranges?(?: from)?|ranged(?: from)?|of|has been|is reported as)\s+' + Q + '(' + NUM + r')\s*' + UNIT_T, s, re.I)
        elif key == 'renalHalfLife':
            if not re.search(RENAL, s, re.I): continue
            m = re.search(r'half[- ]?life[^.]{0,80}?(?:increased|prolonged|rose|was|is|to|of)\s+' + Q + '(' + NUM + r')\s*' + UNIT_T, s, re.I)
        elif key == 'volumeOfDistribution':
            if re.search(r'pediatric|child|neonat|infant|ECMO|metabolite|central compartment|rats?\b|animal', s, re.I): continue
            m = re.search(r'volume of distribution(?: \([A-Za-z /]{1,12}\))?(?: at steady[- ]state)?(?: \([A-Za-z /]{1,12}\))?(?: of [a-z\- ]{2,40}?)?(?: after [a-z ]{2,40}?)? (?:is|was|of|averaged|averages|ranges?(?: from)?|ranged(?: from)?|averaging|has been|approximates)\s+' + Q + '(' + NUM + r')\s*(L/kg|L\b|liters?|litres?)', s, re.I)
        elif key == 'proteinBinding':
            if re.search(r'metabolite|hepatic|unbound|decrease|AUC|C ?max|free fraction', s, re.I): continue
            m = re.search(Q + '(' + NUM + r')\s*%\s*(?:protein[- ])?bound', s, re.I) or re.search(r'(?:protein|plasma protein|serum protein) binding(?: of [a-z\- ]{2,30}?)? (?:is|was|of|ranges?(?: from)?|averaged)\s+(?:low |high |moderate )?\(?' + Q + '(' + NUM + r')\s*%', s, re.I) or re.search(r'bound to (?:human )?(?:plasma|serum) proteins? \(?' + Q + '(' + NUM + r')\s*%', s, re.I)
        else: m = None
        if m:
            val = (re.search(Q + re.escape(m.group(1)) + r'\s*(?:%|' + UNIT_T + r'|L/kg|L\b|liters?|litres?)', m.group(0), re.I) or m).group(0).strip()
            return val, s
    return None, None
RENAL = r'renal (?:impairment|failure|insufficiency|dysfunction)|end[- ]stage renal|ESRD|anuric|creatinine clearance|uremic|kidney failure'

def dialysis(sents, kind):
    trig = r'hemodialysis|haemodialysis|dialy[sz]' if kind == 'ihd' else r'peritoneal dialysis|CAPD'
    for s in sents:
        if not re.search(trig, s, re.I): continue
        if kind == 'ihd' and re.search(r'peritoneal', s, re.I) and not re.search(r'hemodialysis|haemodialysis', s, re.I): continue
        if re.search(r'pediatric|child|neonat|Table|Dosage of|hepatic impairment', s, re.I): continue
        low = s.lower()
        if re.search(r'not known (?:if|whether|which)|no data|not been studied|insufficient (?:evidence|data)|not (?:been )?established|have not been performed', low):
            return 'unknown', 'Not established (label statement)', s
        pct = re.search(r'removes? (?:only )?(?:approximately |about |less than )?(\d+(?:\.\d+)?)\s*%|(?:only|less than) (?:about )?(\d+(?:\.\d+)?)\s*%[^.]{0,40}removed', low)
        if pct and float(pct.group(1) or pct.group(2)) < 15:
            return 'not_removed', 'Negligible removal (label statement)', s
        if re.search(r'not (?:be )?(?:effectively |significantly |appreciably |substantially )?(?:removed|dialy[sz]able|dialy[sz]ed|cleared)|poorly (?:removed|dialy)|neither[^.]{0,60}(?:dialy|removed)|unlikely to be (?:effective|removed|dialy|of benefit)|not effective (?:in|for) (?:removing|removal)|(?:is|are) ineffective|of (?:little|limited) value|not (?:of )?benefi|no evidence that[^.]{0,40}dialy[sz]able|not dialy', low):
            return 'not_removed', 'Not significantly removed (label statement)', s
        if re.search(r'(?:is|are|was|were|can be|may be) (?:readily |significantly |substantially |partially |rapidly |moderately |effectively )?(?:removed|dialy[sz]ed|cleared) (?:from [a-z ]{2,30} )?(?:by|during|with) (?:hemo|haemo|peritoneal )?dialysis|\bis (?:hemo|haemo)?dialy[sz]able\b|(?:hemo)?dialysis removes|dialysis (?:session )?(?:decreases|reduces|lowers)|removed by hemodialysis|eliminated by hemodialysis|significantly removed from the blood during', low):
            return 'removed', 'Removed by dialysis (label statement)', s
    return None, None, None

def label_text(i):
    for sub in ('us', 'preg'):
        f = LAB/sub/f'{i}.json'
        if f.exists():
            r = json.loads(f.read_text())
            return 'US', r, ' '.join(' '.join(r.get(k, [])) for k in PK_KEYS)
    return None, None, None

out = {}
for d in db['drugs']:
    p = d['pharmacokinetics']
    fields = [k for k in ('halfLife', 'renalHalfLife', 'volumeOfDistribution', 'proteinBinding') if any(s.startswith('rdh5') for s in p[k]['sourceIds'])]
    dials = [k for k, v in p['dialysability'].items() if any(s.startswith('rdh5') for s in v['sourceIds'])]
    if not (fields or dials): continue
    kind, r, text = label_text(d['id'])
    e = dict(fields=fields, dialysis=dials, found={})
    if r:
        e['meta'] = dict(setid=r['set_id'], splVersion=r.get('version'), effective=f"{r['effective_time'][:4]}-{r['effective_time'][4:6]}-{r['effective_time'][6:8]}",
                         brand=(r.get('openfda', {}).get('brand_name') or [''])[0], manufacturer=(r.get('openfda', {}).get('manufacturer_name') or [''])[0],
                         application=(r.get('openfda', {}).get('application_number') or [None])[0], url=f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={r['set_id']}")
        sents = sentences(text)
        for k in fields:
            v, s = pick(sents, k, d['name'])
            if v: e['found'][k] = dict(value=v, sentence=s)
        for k in dials:
            st, v, s = dialysis(sents, k)
            if st: e['found']['dial-' + k] = dict(status=st, value=v, sentence=s)
    out[d['id']] = e
(R/'pk_extract_v123.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
withlabel = sum(1 for e in out.values() if 'meta' in e)
print(json.dumps(dict(drugs=len(out), withLabel=withlabel, found={k: sum(1 for e in out.values() if k in e['found']) for k in ['halfLife', 'renalHalfLife', 'volumeOfDistribution', 'proteinBinding', 'dial-ihd', 'dial-pd']})))
