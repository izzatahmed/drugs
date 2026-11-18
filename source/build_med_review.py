#!/usr/bin/env python3
"""Build the reviewer-preview kidney medication review page.

Usage: build_med_review.py [DALIL_DIR]

With DALIL_DIR (rerun only when Dalil's data changes) it first writes
med_review_data_v240.json here: Jordanian products that Dalil links to
RenalRounds entries, with the price Dalil shows and the barcodes.
It always writes dist/med-review.html (template + inlined RenalMath/CrClMath and
the Interactions checker) and copies the data to dist/med-review-data.json.
No RenalRounds clinical data is copied or changed: the page reads database.json.
"""
import json, pathlib, re, sys

src = pathlib.Path(__file__).resolve().parent
dist = src / 'dist'
DATA = src / 'med_review_data_v240.json'
load = lambda p: json.loads(p.read_text(encoding='utf-8'))
db = load(dist / 'database.json')


def dalil_version(dalil):
    m = re.search(r"0\.\d+\.\d+", (dalil / 'sw.js').read_text(encoding='utf-8'))
    return m.group(0) if m else ''


def build_data(dalil):

    cat = load(dalil / 'catalogue.json')['records']
    add_path = dalil / 'catalogue_additions.json'
    if add_path.exists():
        cat += load(add_path)['records']
    rr = load(dalil / 'renalrounds.json')
    prices = load(dalil / 'prices.json')
    codes = load(dalil / 'barcodes.json')['codes']

    rr_ids = {d['id'] for d in db['drugs'] if d.get('entryType') != 'catalog'}
    order = {s['id']: i for i, s in enumerate(prices['meta']['sources'])}
    shown = {}
    for i, e in enumerate(prices['entries']):  # newest source wins; later entry wins a tie (as Dalil)
        key = (order.get(e['sourceId'], -1), i)
        if e['recordId'] not in shown or key >= shown[e['recordId']][0]:
            shown[e['recordId']] = (key, e)

    drug_ids = [d[0] for d in rr['drugs']]
    used = sorted({i for v in rr['records'].values() for i in v if drug_ids[i] in rr_ids})
    remap = {old: new for new, old in enumerate(used)}
    def when(sid):
        m = re.search(r'(\d{4})-(\d{2})(?:-(\d{2}))?(?![\d])', sid)
        mon = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[int(m.group(2)) - 1]
        return f"{int(m.group(3))} {mon} {m.group(1)}" if m.group(3) else f"{mon} {m.group(1)}"
    sources = [s['labelEn'].split(' — ')[0].split(',')[0] + ', ' + when(s['id']) for s in prices['meta']['sources']]

    products, index = [], {}
    clean = lambda s: re.sub(r'\s+', ' ', str(s or '')).strip()
    for r in cat:
        ids = [drug_ids[i] for i in rr['records'].get(r['id'], []) if i in remap]
        # a combination entry (e.g. sacubitril-valsartan) replaces its single components for the review
        parts = {t for x in ids for t in x.split('-') if len(x.split('-')) > 1}
        links = [remap[drug_ids.index(x)] for x in ids if not (x in parts and any(y != x and x in y.split('-') for y in ids))]
        if not links:
            continue
        e = shown.get(r['id'], (None, None))[1]
        index[r['id']] = len(products)
        products.append([clean(r['brand']), clean(r['strength'])[:90], clean(r['pack']), links,
                         e['fils'] if e else 0, order[e['sourceId']] if e else -1])

    barcodes = {}
    for code, ids in codes.items():
        hits = sorted({index[i] for i in ids if i in index})
        if hits:
            barcodes[code] = hits

    data = {'title': 'RenalRounds medication review — Jordanian products',
            'dalilVersion': dalil_version(dalil),
            'note': 'Products, prices and barcodes from Dalil; links to RenalRounds entries by ingredient. Preview for reviewers.',
            'sources': sources, 'drugs': [drug_ids[i] for i in used], 'products': products, 'barcodes': barcodes}
    DATA.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')


    print(f'products {len(products)} · barcodes {len(barcodes)} · RR entries {len(used)}')


if len(sys.argv) > 1:
    build_data(pathlib.Path(sys.argv[1]))
data = load(DATA)
assert set(data['drugs']) <= {d['id'] for d in db['drugs']}
(dist / 'med-review-data.json').write_bytes(DATA.read_bytes())
js = (dist / 'interactions.js').read_text(encoding='utf-8')
m = re.search(r'^const Interactions = \(\(\) => \{.*?^\}\)\(\);', js, re.S | re.M)
math = (dist / 'renal-math.js').read_text(encoding='utf-8').replace("'use strict';", '')
price_note = 'newest listed price per pack, mostly the JFDA public search of 17 Nov 2026'
page = (src / 'med_review_template.html').read_text(encoding='utf-8')
for k, v in {'@@RENALMATH@@': math, '@@INTERACTIONS@@': m.group(0), '@@RRVERSION@@': 'v' + db['version'],
             '@@DALILVERSION@@': 'v' + data['dalilVersion'], '@@PRICENOTE@@': price_note}.items():
    page = page.replace(k, v)
assert '@@' not in page
(dist / 'med-review.html').write_text(page, encoding='utf-8')
print(f"med-review.html {len(page) // 1024} KB · med-review-data.json {DATA.stat().st_size // 1024} KB · {len(data['products'])} products")
