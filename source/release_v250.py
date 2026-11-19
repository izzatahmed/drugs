"""v0.25.0: the kidney medication review (med-review.html) becomes part of the app: linked from the CALC menu, the side menu, the
footer and each medicine's interactions panel ("Add to a medication review"), follows the night theme, and can be opened from Dalil
with a medicine already added. Drug records, sources and calculator sources are unchanged."""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-19'; VERSION = '0.25.0'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.24.0'
data.update(version=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=[], newRenalIds=[], newIds=[], newPKIds=[], pirrtSummaryIds=[], note='Kidney medication review linked from the app; drug content unchanged.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
for f in ('CURATION_QUEUE.json', 'REMAINING_MEDICATIONS.json'):
    x = json.loads((D/f).read_text()); x['version'] = VERSION; (D/f).write_text(json.dumps(x, ensure_ascii=False, indent=2))
header = f'''# RenalRounds v{VERSION} · 19 November 2026

- **Kidney medication review is now part of the app.** Open it from CALC → Medicines, the side menu, the footer, or "Add to a medication review" in any medicine's interactions panel (that medicine is added for you). Dalil v0.18 links to it from medicines that have a RenalRounds page. The page follows the night theme and keeps the draft-reference notice used across the app. Nothing entered is saved or sent.
- CALC menu: on phones, items with two-line descriptions were squeezed so the text overlapped the next item; each item now takes the height its text needs.
- Clinical content is unchanged (drug content version 0.19.0).

'''
for target, base in [('CHANGELOG.md', 'changelog_v240.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v240.md'), ('SOURCE_AUDIT.md', 'source_audit_v240.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v250.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v250.py, apply_reviews.py, build_standalone.py and build_med_review.py. checks_v250.mjs proves drug records, sources, calculator sources and Jordan products are unchanged from v0.24.0, checks the review page's row matching, product data and dark-theme contrast, and that the app links to it.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION)))
