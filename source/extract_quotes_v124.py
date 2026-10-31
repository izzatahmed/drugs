"""Check every quoted sentence in curation_v124.json against the downloaded label and store a short
text window around it plus the label's identity (setid, SPL version, date). Needs the labels folder;
the build itself only reads the output, label_quotes_v124.json.
Usage: python3 extract_quotes_v124.py /path/to/labels
"""
import json, re, sys, html
from pathlib import Path
sys.dont_write_bytecode = True
LAB = Path(sys.argv[1]); R = Path(__file__).parent
C = json.loads((R/'curation_v124.json').read_text())

def text_of(d):
    parts = []
    for k, v in d.items():
        if k in ('openfda', 'spl_product_data_elements', 'package_label_principal_display_panel'): continue
        if isinstance(v, list): parts += [str(x) for x in v]
    t = html.unescape(re.sub(r'</?[a-zA-Z][^<>]*>', ' ', ' '.join(parts)))
    return re.sub(r'\s+', ' ', t)

def evs(c):
    out = [m['ev'] for m in c['pk'].values()]
    for m in c.get('modalities', {}).values(): out += m.get('ev', [])
    return out

res = {}
for did, c in C.items():
    d = json.loads((LAB/c['label']).read_text()); d = d[0] if isinstance(d, list) else d
    t = text_of(d); o = d.get('openfda', {})
    windows = []
    for e in evs(c):
        i = t.find(e)
        if i < 0: raise SystemExit(f'{did}: quote not found in label: {e[:90]}')
        windows.append(t[max(0, i-200): i+len(e)+200])
    res[did] = dict(meta=dict(setid=d.get('set_id'), splVersion=str(d.get('version')), effective=f"{d['effective_time'][:4]}-{d['effective_time'][4:6]}-{d['effective_time'][6:8]}",
                              manufacturer=(o.get('manufacturer_name') or [''])[0], application=(o.get('application_number') or [''])[0], brand=c['brand'],
                              url=f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={d.get('set_id')}"), windows=windows)
(R/'label_quotes_v124.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(f'{sum(len(v["windows"]) for v in res.values())} quotes verified in {len(res)} labels')
