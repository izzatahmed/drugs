"""Pregnancy/lactation excerpts for entries without a v0.12.1 excerpt, from the US label matched to each
entry (labels/preg/<id>.json, fetched from openFDA). Verbatim label text only.
Usage: python3 extract_labels_v122.py /path/to/labels
"""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
LAB = Path(sys.argv[1]); R = Path(__file__).parent
def first(text, n=2, cap=420):
    text = re.sub(r'\s+', ' ', text).strip()
    parts = re.split(r'(?<=[a-z0-9\)\]%])\.\s+(?=[A-Z])', text)
    out = '. '.join(parts[:n]).strip()
    if not out.endswith('.'): out += '.'
    if len(out) > cap: out = out[:cap].rsplit(' ', 1)[0] + ' …'
    return out
HEAD = re.compile(r'^(?:\s*(?:8\.[12]\s*)?(?:Teratogenic Effects|TERATOGENIC EFFECTS|Non-?teratogenic Effects|Pregnancy|PREGNANCY|Usage in Pregnancy|Pregnancy Category\s*:?\s*[ABCDX]\.?|Category\s*[ABCDX]\.?|Risk Summary|Nursing Mothers|NURSING MOTHERS|Lactation|LACTATION)\s*[:.]?\s*)+')
def clean(t):
    t = HEAD.sub('', re.sub(r'\s+', ' ', t)).strip()
    low = t.lower()
    return None if len(t) < 40 or low.startswith(('(see', 'see ')) or ('see warnings' in low and len(t) < 90) else first(t)
def us(i, sub='preg'):
    r = json.loads((LAB/sub/f'{i}.json').read_text()); o = r.get('openfda', {})
    preg_raw = ' '.join(r.get('pregnancy', []) + r.get('teratogenic_effects', []))
    usp = ' '.join(r.get('use_in_specific_populations', []))
    other = ' '.join(r.get('precautions', []) + r.get('warnings', []) + r.get('general_precautions', []))
    alltext = ' '.join(' '.join(v) for k, v in r.items() if isinstance(v, list) and k not in ('package_label_principal_display_panel', 'spl_product_data_elements'))
    letter = re.search(r'Pregnancy Category\s*:?\s*([ABCDX])\b', alltext, re.I)
    cands = []
    m = re.search(r'Risk Summary\s+(.*)', preg_raw); cands.append(m.group(1) if m else preg_raw)
    m = re.search(r'8\.1\s*Pregnancy\s*(?:Risk Summary\s*)?(.*?)(?=8\.2|$)', usp); cands.append(m.group(1) if m else '')
    m = re.search(r'(?:Usage in Pregnancy|Pregnancy)\s*:?\s*(?:Category\s*[ABCDX]\.?\s*)?(.*?)(?=Nursing Mothers|Labor and Delivery|Pediatric Use|Geriatric Use|$)', other); cands.append(m.group(1) if m else '')
    w = ' '.join(r.get('warnings', []) + r.get('boxed_warning', []))
    m = re.search(r'([A-Z][^.]*(?:fetal harm|harm to the fetus)[^.]*\.(?:\s+[A-Z][^.]*\.)?)', w); cands.append(m.group(1) if m else '')
    preg = next((c for c in (clean(x) for x in cands if x) if c), None)
    lc = []
    m = re.search(r'8\.2\s*Lactation\s*(?:Risk Summary\s*)?(.*?)(?=8\.3|8\.4|$)', usp); lc.append(m.group(1) if m else '')
    lc.append(' '.join(r.get('nursing_mothers', [])))
    m = re.search(r'Nursing Mothers\s*:?\s*(.*?)(?=Pediatric Use|Geriatric Use|Labor and Delivery|$)', other); lc.append(m.group(1) if m else '')
    lact = next((c for c in (clean(x) for x in lc if x) if c), None)
    e = r['effective_time']
    meta = dict(setid=r['set_id'], splVersion=r.get('version'), effective=f'{e[:4]}-{e[4:6]}-{e[6:]}', brand=(o.get('brand_name') or [''])[0],
                manufacturer=(o.get('manufacturer_name') or [''])[0], application=(o.get('application_number') or [None])[0],
                url=f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={r['set_id']}")
    src_text = re.sub(r'\s+', ' ', alltext)
    return dict(kind='US', meta=meta, letter=letter.group(1).upper() if letter else None, pregnancy=preg, lactation=lact, sourceText=src_text)

done = json.loads((R/'label_extract_v121.json').read_text())
out = {}
for f in sorted((LAB/'preg').glob('*.json')):
    i = f.stem
    if i in done: continue
    e = us(i)
    if not (e['pregnancy'] or e['lactation']): continue
    e['sourceId'] = f'preg122-{i}'; out[i] = e
for e in out.values():
    t = e['sourceText']; wins = []
    for k in ('pregnancy', 'lactation'):
        if e.get(k):
            pos = t.find(e[k].rstrip(' …').rstrip('.')[:120]); wins.append(t[max(0, pos - 150):pos + len(e[k]) + 150])
    e['sourceText'] = ' … '.join(wins)   # short window around each quote: enough to verify, small enough to keep in the repo
(R/'label_extract_v122.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(out), 'entries;', sum(bool(e['pregnancy']) for e in out.values()), 'pregnancy;', sum(bool(e['lactation']) for e in out.values()), 'lactation;', sum(bool(e['letter']) for e in out.values()), 'with FDA letter')
