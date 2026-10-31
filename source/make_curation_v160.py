"""Curated label content for v0.16.0 (new medicines: oncology, anaesthesia & critical care, contrast media and others). Every dose table, statement and PK value carries
the verbatim label sentence(s) it comes from. Writes curation_v160.json; verify with
  python3 extract_quotes.py curation_v160.json label_quotes_v160.json /path/to/labels
"""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(__file__).parent

def T(indication, rows): return dict(indication=indication, rows=[dict(context=c, dose=d) for c, d in rows])
def M(status, tables=(), notes='', ev=()): return dict(status=status, tables=list(tables), notes=notes, ev=list(ev))
def P(value, ev, status='sourced'): return dict(value=value, ev=ev, status=status)
def E(label, brand, *, flag=None, metric=None, summary=None, considerations=None, promote=False, pk_only=False, mods=None, pk=None, completeness=None):
    e = dict(label=label, brand=brand, promote=promote, pk_only=pk_only, modalities=mods or {}, pk=pk or {})
    for k, v in dict(flag=flag, kidneyMetric=metric, summary=summary, considerations=considerations, completeness=completeness).items():
        if v is not None: e[k] = v
    return e

C = {}
LAB = {}   # label file per entry (relative to the labels folder)
NEW = {}   # brand-new inventory records created by the release
def lab(i):
    import os
    if i in LAB: return LAB[i]
    for s in ('us', 'preg', 'extra', 'us2', 'eu'):
        if os.path.exists(f'/home/claude/labels/{s}/{i}.json'): return f'{s}/{i}.json'
    return LAB[i]
def add(i, brand, **kw): C[i] = E(lab(i), brand, **kw)

# ---- curated entries are appended below in batches ----
exec(open(R/'batch_v160_n.py').read())
#@@BATCHES@@

# ---- reviewed PK values (pk_v160.txt) merged into each entry; PK-only entries created where needed ----
for line in (R/'pk_v160.txt').read_text().splitlines():
    if not line.strip() or line.startswith('#'): continue
    i, field, status, value, ev = line.split('|', 4)
    if i not in C: C[i] = E(lab(i), '', pk_only=True)
    C[i]['pk'].setdefault(field, P(value, ev, 'sourced' if status == '-' else status))
for i, (name, al, cat, cls, routes) in NEW.items(): C[i]['new'] = dict(name=name, aliases=al, category=cat, drugClass=cls, routes=routes)
(R/'curation_v160.json').write_text(json.dumps(C, ensure_ascii=False, indent=1))
print(len(C), 'entries')
