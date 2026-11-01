"""v0.21.0: fifteen more nephrology calculators (electrolytes, acid–base, AKI, proteinuria, dialysis/CRRT/PD, anaemia)
in a grouped CALC menu. Arithmetic in dist/nephro-math.js, UI in dist/nephro-tools.js. Drug records are unchanged."""
from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
R = Path(__file__).parent; D = R/'dist'
DATE = '2026-11-01'; VERSION = '0.21.0'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.20.0'
assert len(data['calculatorSources']) == 15
have = {s['url'] for s in data['calculatorSources']}
new = [s for s in json.loads((R/'calc_sources_v210.json').read_text()) if s['url'] not in have]
data['calculatorSources'] += new
data.update(version=VERSION, softwareReleaseDate=DATE)
data['releaseChanges'] = dict(version=VERSION, changedIds=[], newRenalIds=[], newIds=[], newPKIds=[], pirrtSummaryIds=[],
    note='Fifteen nephrology calculators in a grouped CALC menu.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
for f in ('CURATION_QUEUE.json', 'REMAINING_MEDICATIONS.json'):
    x = json.loads((D/f).read_text()); x['version'] = VERSION; (D/f).write_text(json.dumps(x, ensure_ascii=False, indent=2))
header = f'''# RenalRounds v{VERSION} · 1 November 2026

- **Fifteen new calculators**, with the CALC menu now grouped by topic:
  - AKI & proteinuria: KDIGO AKI stage; FENa / FEUrea; spot PCR/ACR → 24-hour estimate with KDIGO category.
  - Electrolytes & acid–base: hyponatraemia infusate effect (Adrogué–Madias, with volumes for a 6 and 8 mmol/L rise and correction limits); sodium corrected for glucose (Katz/Hillier); free water deficit; anion gap with albumin correction and delta ratio; expected pCO₂ (Winter's formula); osmolality and osmolal gap; calcium corrected for albumin.
  - Dialysis: ultrafiltration rate (13 mL/kg/h threshold); CRRT effluent dose with pre-dilution correction and filtration fraction; peritoneal dialysis weekly Kt/V (Watson volume).
  - Anaemia: TSAT with KDIGO iron thresholds; Ganzoni iron deficit.
- Each calculator states its formula and links its published source ({len(new)} new references). Inputs are not stored or sent. Clinical drug content is unchanged (drug content version 0.19.0).

'''
for target, base in [('CHANGELOG.md', 'changelog_v200.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v200.md'), ('SOURCE_AUDIT.md', 'source_audit_v200.md')]:
    (D/target).write_text(header + '## Earlier release record\n\n' + (R/base).read_text())
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v210.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v210.py and apply_reviews.py. checks_v210.mjs proves drug records are unchanged from v0.20.0 and checks every new calculator against worked reference cases (for example the NEJM 2000 hyponatraemia example: 3% saline raises sodium 12.9 mmol/L per litre).

These are software/arithmetic checks, not clinical validation.
''')
print(json.dumps(dict(version=VERSION, newCalculatorSources=len(new), total=len(data['calculatorSources']))))
