"""v0.11.3: reader-facing wording, drug classes and calculator/interface release.

No dose table, modality status, PK value or source URL is changed by this script.
checks_v113.mjs proves that against baseline_v112.json.
"""
from pathlib import Path
import json, re

R = Path(__file__).parent; D = R/'dist'
DATE = '2026-10-30'; VERSION = '0.11.3'
data = json.loads((D/'database.json').read_text()); assert data['version'] == '0.11.2'

# 1. Internal working notes rewritten as neutral reader-facing statements.
#    Applied to every string except dose-table cells (modalities.*.tables), which stay byte-identical.
EXACT = {
    'Monograph text inaccessible in this environment; presence in BNF 92 is not asserted.': 'BNF comparison not yet done.',
    'Monograph text inaccessible; not independently checked.': 'BNF comparison not yet done.',
    'Monograph access blocked in this environment; reconciliation pending.': 'BNF comparison not yet done.',
    'Indexed directory reviewed; direct portal access blocked. Linked documents are not all reviewed.': 'Directory reviewed; not every linked document has been reviewed.',
    'Monographs inaccessible; comparison pending. Edition existence checked with publisher only.': 'BNF comparison pending; no entry is BNF-verified.',
    'Clarified by the user: the intended reference is the British National Formulary (BNF), not a separate PNF.': 'BNF here means the British National Formulary.',
    'Search service unavailable. Supplied fifth-edition PDF and a directly retrieved MHRA safety page used for this batch.': 'This batch used the Renal Drug Handbook (5th edition, 2018) and an MHRA drug-safety notice.',
    'Original PDF remains a research input. Citations use page locators and the supplied-file checksum; original PDF is not in the GitHub package.': 'Cited by page number; the original document is not redistributed.',
    'Supplied fifth-edition renal reference': 'Renal Drug Handbook, 5th edition (2018)',
    'Supplied historical PK reference': 'Renal Drug Handbook, 5th edition (2018) · PK',
    'Supplied handbook · historical PK reference': 'Renal Drug Handbook, 5th edition (2018) · PK',
    'Supplied institutional protocol': 'Institutional protocol',
    'Supplied institutional sheet · historical comparison': 'Institutional sheet · historical comparison',
    'Supplied historical product comparison': 'Historical product comparison (handbook)',
    'Selected supplied-source adult statement only; current local product and independent clinical review remain pending.': 'Selected source-specific adult statement only; current local product and independent clinical review remain pending.',
}
PATTERNS = [
    (r'Publisher-listing link is not the supplied PDF\.', "The link is the publisher's catalogue, not the book."),
    (r'Link opens publisher listing, not the uploaded book\.', "The link is the publisher's catalogue, not the book."),
    (r'Link is a publisher listing, not this supplied PDF\.', "The link is the publisher's catalogue, not the book."),
    (r'\bthe supplied fifth edition\b', 'the fifth edition'),
    (r'\bSupplied fifth edition\b', 'Fifth edition'),
    (r'\bsupplied PDF\b', 'PDF'),
    (r'\bSupplied PDF\b', 'Handbook PDF'),
    (r'\bThe supplied protocol\b', 'The institutional protocol'),
    (r'\bSupplied 2026-approved institutional dose bands\b', 'Institutional dose bands approved in 2026'),
    (r'\buploaded institutional and historical sources\b', 'institutional and historical sources'),
    (r'\bthe new PIRRT row\b', 'the PIRRT row'),
    (r'Public link is the organisation homepage, not this supplied file\.', "The link is the organisation's homepage, not the document."),
]
ORG = {'upload-0': 'CRC Press (Taylor & Francis)', 'upload-1': 'KDIGO', 'upload-2': 'BC Renal',
       'upload-3': 'University of Nebraska Medical Center', 'upload-4': 'University of Nebraska Medical Center'}

def clean(s):
    s = EXACT.get(s, s)
    for pat, rep in PATTERNS: s = re.sub(pat, rep, s)
    return s
def walk(o, path=()):
    if isinstance(o, dict):
        return {k: (v if k == 'tables' and 'modalities' in path else walk(v, path+(k,))) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, path) for v in o]
    return clean(o) if isinstance(o, str) else o
data = walk(data)
for r in data['referenceResources']:
    if r['id'] in ORG: r['organisation'] = ORG[r['id']]

# 2. Pharmacological classes where the class field only repeated the category.
classes = json.loads((R/'drug_classes_v113.json').read_text())
for d in data['drugs']:
    if d['id'] in classes:
        assert d['drugClass'] == d['category'], d['id']
        d['drugClass'] = classes[d['id']]
assert not [d['id'] for d in data['drugs'] if d['drugClass'] == d['category']]

data.update(version=VERSION, softwareReleaseDate=DATE)  # clinicalDataVersion stays 0.11.2: no dosing change
data['releaseChanges'] = dict(version=VERSION, changedIds=[], newRenalIds=[], newPKIds=[], pirrtSummaryIds=[],
    note='Software and wording release. Dose tables, statuses and PK values are unchanged from 0.11.2.')
(D/'database.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
(D/'REFERENCE_DIRECTORY.json').write_text(json.dumps(data['referenceResources'], ensure_ascii=False, indent=2))
for name in ['CURATION_QUEUE.json', 'REMAINING_MEDICATIONS.json']:
    q = json.loads((D/name).read_text()); q['version'] = VERSION; (D/name).write_text(json.dumps(q, ensure_ascii=False, indent=2))

header = f'''# RenalRounds v{VERSION} · 30 October 2026

Software and wording release. No dose table, setting status or PK value changed; drug content remains 0.11.2.

- Kidney-function calculator now has two tabs: eGFR (CKD-EPI 2021 / legacy MDRD) and Cockcroft–Gault creatinine clearance with actual, ideal and adjusted body weight. Most drug tables in this reference are banded by CrCl.
- Phone layout: the floating back button no longer covers dose tables; on phones a "Back" button sits at the top of each drug. Pressing Enter in search opens the selected drug. The calculator scrolls to its result.
- Converted creatinine is shown to two decimals.
- 426 entries whose class only repeated the category now have a pharmacological class (e.g. flecainide: Class Ic antiarrhythmic). Search understands common abbreviations (PPI, NSAID, DOAC, LMWH, SGLT2i, ACEi, ARB, ESA and others).
- Internal working notes were rewritten as neutral statements (e.g. "BNF comparison not yet done").
- Each drug has a "Report an error" link that opens a pre-filled GitHub issue.
- Link previews (Open Graph) added.

'''
for target, base in [('CHANGELOG.md', 'changelog_v112.md'), ('EDITORIAL_GUIDE.md', 'editorial_guide_v112.md'), ('SOURCE_AUDIT.md', 'source_audit_v112.md')]:
    (D/target).write_text(header+'## Earlier release record\n\n'+(R/base).read_text())
(D/'COMPLETION_PLAN.md').write_text(header+'## Remaining clinical work\n\nIndependent nephrologist and renal-pharmacist review of every entry; renal profiles for the 285 catalog-only entries, prioritised by risk; dialysis-setting coverage (CRRT, SLED, PD); a single primary jurisdiction with country labels on every table; and a decision on handbook-derived content.\n')
(D/'VERIFICATION.md').write_text(f'''# v{VERSION} verification

Current suites: checks.mjs, checks_v113.mjs, checks_interface.mjs and checks_calculator.mjs after the ordered build through release_v113.py. checks_v113.mjs proves every dose table, modality status, PK field and source URL is identical to v0.11.2, checks the Cockcroft–Gault arithmetic against hand-worked examples, and runs the service-worker offline/update contract for {VERSION}.

These are software/source-integrity checks, not clinical validation.
''')
calc = (D/'CALCULATOR.md').read_text().replace('# Adult eGFR calculator · v0.8.0', '# Adult kidney function calculator · v0.11.3 (eGFR v0.8.0)').replace('Open **eGFR calculator** beside quick search', 'Open the **eGFR · CrCl** calculator beside quick search')
calc += """

## Cockcroft–Gault creatinine clearance (added v0.11.3)

- CrCl (mL/min) = (140 − age) × weight (kg) ÷ (72 × SCr in mg/dL) × 0.85 if female. Not indexed to body surface area.
- Ideal body weight (Devine): 50 kg male / 45.5 kg female + 2.3 kg per inch over 152.4 cm. Adjusted body weight = IBW + 0.4 × (actual − IBW), shown only when actual weight exceeds IBW.
- Actual weight is required; height is optional. Without height only actual-weight CrCl is shown. All three results are shown side by side so the reader can use the weight the drug label or local protocol specifies.
- Creatinine is not rounded up. Warnings appear for height below 152 cm, actual weight ≥130% of IBW, low creatinine in adults ≥65 and unusual creatinine values.
- Same exclusions as eGFR: no result for AKI/changing creatinine, dialysis, pregnancy or age under 18.
- The equation predates IDMS-standardized creatinine and may read higher with current assays.
- Sources: Cockcroft DW, Gault MH. Nephron 1976;16:31–41, https://doi.org/10.1159/000180580 · McCarron MM, Devine BJ. Drug Intell Clin Pharm 1974;8:650–5, https://doi.org/10.1177/106002807400801104
- checks_v113.mjs verifies the arithmetic against hand-worked examples and the validation rules.
"""
(D/'CALCULATOR.md').write_text(calc)
print(json.dumps(dict(version=VERSION, classes=len(classes))))
