"""Build label_extract_v121.json from retrieved label files (run once with network-fetched labels;
the release build reads only the JSON). Pregnancy/lactation excerpts are verbatim label text.
Usage: python3 extract_labels_v121.py /path/to/labels
"""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
LAB = Path(sys.argv[1]); R = Path(__file__).parent
meta120 = json.loads((R/'label_meta_v120.json').read_text())
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
def us(i):
    r = json.loads((LAB/'us'/f'{i}.json').read_text()); o = r.get('openfda', {})
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
def uk(i, pid):
    o = [x for x in json.loads((LAB/'uk'/f'{i}.json').read_text()) if x['pid'] == pid][0]; t = o['text']
    m = re.search(r'4\.6\s*Fertility,? pregnancy and lactation(.*?)4\.7', t, re.I | re.S)
    sec = m.group(1) if m else ''
    pm = re.search(r'Pregnancy\s+(.*?)(?=Breast[- ]?feeding|Lactation|Fertility|$)', sec, re.S)
    lm = re.search(r'(?:Breast[- ]?feeding|Lactation)\s+(.*?)(?=Fertility|$)', sec, re.S)
    return dict(kind='UK', meta=dict(emcProductId=pid, title=o['title'], updated=o['updated']), letter=None,
                pregnancy=clean(pm.group(1)) if pm else None, lactation=clean(lm.group(1)) if lm else None, sourceText=re.sub(r'\s+', ' ', sec))
out = {}
for i, m in meta120.items():
    e = us(i) if m['kind'] == 'US' else uk(i, m['emcProductId'])
    e['sourceId'] = ('us120-' if m['kind'] == 'US' else 'uk120-') + i
    out[i] = e
for i in ['vancomycin', 'gentamicin', 'amikacin', 'tobramycin', 'vonoprazan']:
    e = us(i); e['sourceId'] = f'us121-{i}'; out[i] = e
(R/'label_extract_v121.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(out), 'labels;', sum(bool(e['pregnancy']) for e in out.values()), 'pregnancy;', sum(bool(e['lactation']) for e in out.values()), 'lactation;', sum(bool(e['letter']) for e in out.values()), 'with FDA letter')
