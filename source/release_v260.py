"""v0.26.0: the kidney medication review gains a kidney-transplant option (immunosuppressants chosen once; every added medicine is
checked against them using the existing label sentences and FDA CYP/P-gp roles) and the draft notice becomes an asterisk with a footnote.
Drug records, sources and calculator sources are unchanged."""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-20'; VERSION = '0.26.0'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.25.0'
data.update(version=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=[], newRenalIds=[], newIds=[], newPKIds=[], pirrtSummaryIds=[], note='Kidney medication review: transplant immunosuppressant interaction check; drug content unchanged.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
for f in ('CURATION_QUEUE.json', 'REMAINING_MEDICATIONS.json'):
    x = json.loads((D/f).read_text()); x['version'] = VERSION; (D/f).write_text(json.dumps(x, ensure_ascii=False, indent=2))
header = f'''# RenalRounds v{VERSION} · 20 November 2026

- **Kidney medication review: kidney transplant.** Tick "Kidney transplant recipient" and choose the current immunosuppressants (tacrolimus, ciclosporin, sirolimus, everolimus, mycophenolate, azathioprine, prednisolone, belatacept). Every medicine added afterwards is checked against them: a warning appears as it is added, on its card, and in a transplant section at the top of the review. The check uses the same label sentences and FDA CYP/P-gp roles as the interaction checker; no interaction data were added.
- The draft-reference notice on the review page is now an asterisk on the title with the full note at the end of the page (and on prints).
- Clinical content is unchanged (drug content version 0.19.0).

'''
for target, base in [('CHANGELOG.md', 'changelog_v250.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v250.md'), ('SOURCE_AUDIT.md', 'source_audit_v250.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v260.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v260.py, apply_reviews.py, build_standalone.py and build_med_review.py. checks_v260.mjs proves drug records, sources, calculator sources and Jordan products are unchanged from v0.25.0, checks the review page's row matching, product data and dark-theme contrast, that the app links to it, and the transplant check.

These are software/source-integrity checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION)))
