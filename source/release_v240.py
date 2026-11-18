"""v0.24.0: adds a reviewer preview page, med-review.html (kidney medication review: a list of medicines, kidney function or dialysis,
the RenalRounds guidance for each, interactions between them and Jordanian prices from Dalil v0.17). The page reads database.json
and is not linked from the app. Drug records, sources and calculator sources are unchanged."""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-18'; VERSION = '0.24.0'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.23.0'
data.update(version=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=[], newRenalIds=[], newIds=[], newPKIds=[], pirrtSummaryIds=[], note='Reviewer preview page med-review.html added; drug content unchanged.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
for f in ('CURATION_QUEUE.json', 'REMAINING_MEDICATIONS.json'):
    x = json.loads((D/f).read_text()); x['version'] = VERSION; (D/f).write_text(json.dumps(x, ensure_ascii=False, indent=2))
header = f'''# RenalRounds v{VERSION} · 18 November 2026

- **Reviewer preview: kidney medication review** at `med-review.html` (not linked from the app). Add a patient's medicines by generic name, Jordanian brand or box barcode; enter eGFR/CrCl (or calculate them from creatinine) or choose haemodialysis, PD or CRRT. The page shows each medicine's RenalRounds guidance with the matching row highlighted, label-quoted interactions between the listed medicines, and Dalil v0.17 pack prices. Nothing is stored or sent.
- Clinical content is unchanged (drug content version 0.19.0).

'''
for target, base in [('CHANGELOG.md', 'changelog_v230.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v230.md'), ('SOURCE_AUDIT.md', 'source_audit_v230.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v240.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v240.py, apply_reviews.py, build_standalone.py and build_med_review.py. checks_v240.mjs proves drug records, sources, calculator sources and Jordan products are unchanged from v0.23.0, tests the review page's row matching, and checks its product data.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION)))
