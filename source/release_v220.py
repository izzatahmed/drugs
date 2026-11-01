"""v0.22.0: tubular-function calculators (potassium work-up with urine K/creatinine and TTKG; phosphate FEPO4, TRP and TmP/GFR;
fractional excretion of magnesium; urine anion and osmolal gaps) and voice search. Drug records are unchanged."""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-01'; VERSION = '0.22.0'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.21.0'
assert len(data['calculatorSources']) == 37
have = {s['url'] for s in data['calculatorSources']}
new = [s for s in json.loads((R/'calc_sources_v220.json').read_text()) if s['url'] not in have]
data['calculatorSources'] += new
data.update(version=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=[], newRenalIds=[], newIds=[], newPKIds=[], pirrtSummaryIds=[],
    note='Tubular-function calculators and voice search.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
for f in ('CURATION_QUEUE.json', 'REMAINING_MEDICATIONS.json'):
    x = json.loads((D/f).read_text()); x['version'] = VERSION; (D/f).write_text(json.dumps(x, ensure_ascii=False, indent=2))
header = f'''# RenalRounds v{VERSION} · 1 November 2026

- **Tubular function** — four new calculators: potassium work-up (urine K⁺/creatinine ratio as the main result, with TTKG and its validity checks); phosphate FEPO₄, TRP and TmP/GFR (Kenny & Glen algorithm); fractional excretion of magnesium; urine anion gap and urine osmolal gap with estimated ammonium. The CALC menu now has 26 calculators.
- **Voice search:** a mic button in the search box (Chrome on Android and other browsers with speech recognition). Misheard names are matched to the nearest medicine name. Speech is processed by the browser's speech service; nothing starts until the mic is tapped.
- {len(new)} new references. Clinical drug content is unchanged (drug content version 0.19.0).

'''
for target, base in [('CHANGELOG.md', 'changelog_v210.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v210.md'), ('SOURCE_AUDIT.md', 'source_audit_v210.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v220.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v220.py and apply_reviews.py. checks_v220.mjs proves drug records are unchanged from v0.21.0, checks the four new calculators against worked cases (including both branches of the TmP/GFR algorithm) and re-runs every v0.21 calculator case.

These are software/arithmetic checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, newCalculatorSources=len(new), total=len(data['calculatorSources']))))
