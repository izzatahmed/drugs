"""v0.23.0: refresh "Products in Jordan" from Dalil v0.16 (JFDA workbook June 2026 + 175 products added from the JFDA public price
search of 17 Nov 2026). The link builder now recognises combinations written as one ingredient text (e.g. "Sacubitril Valsartan 200 (...)").
Drug records are unchanged."""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-17'; VERSION = '0.23.0'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.22.0'
J = json.loads((R/'jordan_products_v230.json').read_text())
assert set(J['drugs']) <= {d['id'] for d in data['drugs']}
jp = data['jordanProducts']; jp['drugs'] = J['drugs']
jp['source'] = dict(J['source'], additions=dict(title='Products added from the JFDA public price search', collected='2026-11-17', records=175))
jp['note'] = 'Counts are JFDA-registered products whose scientific name contains this ingredient, matched by ingredient name and route, from the JFDA workbook (June 2026) plus products found in the JFDA public price search (17 November 2026). Registration is not proof of current marketing or availability; check the strength and the JFDA-approved leaflet.'
data.update(version=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=[], newRenalIds=[], newIds=[], newPKIds=[], pirrtSummaryIds=[], note='Products in Jordan refreshed from Dalil v0.16.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
for f in ('CURATION_QUEUE.json', 'REMAINING_MEDICATIONS.json'):
    x = json.loads((D/f).read_text()); x['version'] = VERSION; (D/f).write_text(json.dumps(x, ensure_ascii=False, indent=2))
sv = J['drugs'].get('sacubitril-valsartan', {})
header = f'''# RenalRounds v{VERSION} · 17 November 2026

- **Products in Jordan refreshed** from Dalil v0.16, which adds 175 products found in the JFDA public price search (17 November 2026) to the June 2026 JFDA workbook. Combination products written as one ingredient text are now recognised: sacubitril/valsartan now shows {sv.get('products')} Jordanian products (4 before), and those products no longer count as valsartan alone.
- Clinical content is unchanged (drug content version 0.19.0).

'''
for target, base in [('CHANGELOG.md', 'changelog_v220.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v220.md'), ('SOURCE_AUDIT.md', 'source_audit_v220.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v230.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v230.py and apply_reviews.py. checks_v230.mjs proves drug records, sources and calculator sources are unchanged from v0.22.0 and checks the refreshed Jordan-products data.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, jordanDrugs=len(J['drugs']), sacubitrilValsartan=sv)))
