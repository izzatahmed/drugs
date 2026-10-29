"""Add the adult eGFR tool; preserve every v0.7 drug/source record unchanged.

Run after build_data.py, release_v06.py and release_v07.py.
"""
from pathlib import Path
import json

ROOT=Path(__file__).parent
D=ROOT/'dist'
DATE='2026-10-29'
data=json.loads((D/'database.json').read_text())
assert data['version'] in ['0.7.0','0.8.0']
data.update(version='0.8.0',clinicalDataVersion='0.7.0',softwareReleaseDate=DATE)
base='https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/'
data['calculatorSources']=[
 dict(title='NIDDK · adult CKD-EPI equations',url=base+'glomerular-filtration-rate-equations/adults',checked=DATE,scope='2021 creatinine equation, units and coefficients'),
 dict(title='NIDDK · previous eGFR equations',url=base+'glomerular-filtration-rate-equations/adults/previous',checked=DATE,scope='IDMS MDRD; the app explicitly omits the historical race multiplier'),
 dict(title='NIDDK · kidney function for drug dosing',url=base+'ckd-drug-dosing-providers',checked=DATE,scope='Kidney-function measures, de-indexing and decision cutoffs'),
 dict(title='NIDDK · clinical measurements and eGFR accuracy',url=base+'factors-affecting-egfr-accuracy/clinical-measurements',checked=DATE,scope='Non-steady-state and creatinine limitations'),
 dict(title='NKF · CKD-EPI 2021 implementation',url='https://www.kidney.org/recommendations-implementing-ckd-epi-2021-race-free-egfr-calculation-guidelines-clinical',checked=DATE,scope='Table S1 published verification values'),
 dict(title='eviQ · body surface area',url='https://www.eviq.org.au/clinical-resources/eviq-calculators/3198-body-surface-area-calculator',checked=DATE,scope='Mosteller BSA formula')]
(D/'database.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
queue=json.loads((D/'CURATION_QUEUE.json').read_text());queue['version']=data['version']
(D/'CURATION_QUEUE.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2))
changelog='''# Changelog

## v0.8.0 — 29 October 2026

- Added an adult eGFR calculator accessible beside quick search and in the sidebar. Race-free CKD-EPI 2021 creatinine is the default; IDMS MDRD is labelled legacy with its historical race multiplier omitted.
- Added mg/dL and µmol/L inputs with automatic value conversion when the unit changes; estimates update as inputs change. Values are not capped at 60 or 90.
- Optional height/weight produces Mosteller BSA and non-indexed eGFR in mL/min, separately labelled from mL/min/1.73 m². This is not a CrCl calculator and selects no medicine dose.
- Invalid/incomplete entries remove any previous estimate. No result is produced for children, AKI/changing creatinine, dialysis or pregnancy. Calculator values clear on close and are not stored, exported or transmitted.
- Verified CKD-EPI arithmetic against NKF Table S1 reference cases; added legacy MDRD and BSA arithmetic, unit-equivalence and validation checks.
- All 668 drug records, 241 existing drug/source records, PK, doses, conflicts and review states are unchanged from clinical-data version 0.7.0. Software version 0.8.0 does not imply clinical approval.

'''
(D/'CHANGELOG.md').write_text(changelog+(ROOT/'changelog_v07.md').read_text())
guide=(D/'EDITORIAL_GUIDE.md').read_text().split('\n## v0.8 eGFR calculator')[0].replace('Version 0.7.0 ·','Version 0.8.0 ·')
guide=guide.replace('`python3 release_v07.py` and `python3 build_standalone.py`','`python3 release_v07.py`, `python3 release_v08.py` and `python3 build_standalone.py`')
guide+='''\n## v0.8 eGFR calculator\n\nThe calculator is a separate tool, not a prescribing rule. Clinical data remain version 0.7.0. CKD-EPI 2021 creatinine is the default. MDRD is a legacy IDMS comparison without the original race multiplier, not a newly refitted race-free MDRD equation. Preserve visible equation/units, correct SI conversion and the difference between indexed eGFR, non-indexed GFR and Cockcroft–Gault CrCl. Do not transfer the result into a drug-dose threshold automatically. Optional Mosteller BSA estimates must not be confused with lean/adjusted dosing weight. Check quantified IDMS-standardized creatinine within the laboratory reportable range. Standard estimates are withheld for AKI/changing creatinine, dialysis, pregnancy and children. No CKD diagnosis or stage is assigned from one reading. Calculator entries clear on close and have no persistence or export. Formula/arithmetic checks are not independent clinical approval. See CALCULATOR.md and checks_calculator.mjs.\n'''
(D/'EDITORIAL_GUIDE.md').write_text(guide)
plan=(D/'COMPLETION_PLAN.md').read_text().replace('# Clinical completion plan · v0.7.0','# Clinical completion plan · software v0.8.0 / drug data v0.7.0')
(D/'COMPLETION_PLAN.md').write_text(plan)
calculator='''# Adult eGFR calculator · v0.8.0

Open **eGFR calculator** beside quick search or in the sidebar. Enter age, the equation's sex parameter, a quantified IDMS-standardized serum creatinine and its units, and the clinical setting. No patient identifiers are requested. Values update locally and clear when the panel closes. No values enter URLs, local/session storage, database exports, completion queues or network requests.

## Equations and units

- CKD-EPI 2021 creatinine (default): 142 × min(SCr/κ,1)^α × max(SCr/κ,1)^−1.200 × 0.9938^age × 1.012 if female. κ is 0.7 female / 0.9 male; α is −0.241 female / −0.302 male.
- MDRD, IDMS: 175 × SCr^−1.154 × age^−0.203 × 0.742 if female. This app omits the original race multiplier and labels the result a legacy comparison, not a newly refitted race-free equation. CKD-EPI 2021 is preferred. Higher-GFR MDRD estimates require caution.
- SCr is mg/dL; convert µmol/L by dividing by 88.4. Changing the unit converts an entered numeric value rather than reinterpreting it.
- Standard output is mL/min/1.73 m². Optional Mosteller BSA = sqrt(height_cm × weight_kg / 3600); non-indexed eGFR = indexed eGFR × BSA / 1.73, in mL/min. This estimates GFR, not Cockcroft–Gault CrCl.

## Scope and prescribing

This app accepts ages 18–120, requires positive finite quantified creatinine, and does not calculate for AKI/changing creatinine, dialysis or pregnancy. Optional body-size input guards accept height 50–250 cm and weight 10–500 kg; these are input guards, not validation claims for body-size extremes. Results are displayed to one decimal; rounding does not determine a drug cutoff. A single result does not establish CKD or chronicity. For ages 18–25, consider comparison with CKiD U25 (not calculated here).

Check the metric/units stated in the selected product label or renal protocol. Drug decisions near cutoffs may need combined creatinine–cystatin C or measured kidney-function assessment. Frailty, atypical muscle mass, critical illness and body-size extremes may impair estimation. There is no automatic drug-dose selection, calculator result storage, AKI model or residual-dialysis clearance calculation.

## Verification

checks_calculator.mjs runs all eight numeric examples from NKF Table S1 using mg/dL and converted µmol/L and compares their rounded values. It also checks independent scalar MDRD examples, both sides of the CKD-EPI splice points, Mosteller/de-indexing arithmetic, missing/invalid fields, age limits and excluded clinical settings. The full v0.7 baseline proves every drug and existing source unchanged. Browser checks cover form updates, unit switching, invalid-value clearing, blocked settings, optional body size, close/reset and phone layout. These are software/arithmetic checks, not independent clinical approval or physical-phone validation.

## Sources checked 29 October 2026

'''
calculator+='\n'.join('- '+s['title']+': '+s['url']+' — '+s['scope'] for s in data['calculatorSources'])+'\n'
(D/'CALCULATOR.md').write_text(calculator)
verification='''# v0.8.0 verification — 29 October 2026

Drug content remains version 0.7.0 and independently unapproved. Software 0.8.0 adds the adult calculator only. See CALCULATOR.md for equations, scope and source links.

- checks.mjs and checks_v07.mjs retain previous clinical/source, search/filter, embedded-data and simulated service-worker safeguards.
- checks_calculator.mjs compares every drug/source and shared guidance with the complete v0.7 baseline; verifies all eight NKF Table S1 numeric cases in both units, MDRD scalar examples, BSA/de-indexing, splice continuity, input limits and excluded settings.
- Browser QA covers calculation, equation switch, SI conversion, result removal for invalid/missing fields, exclusion of dialysis/AKI/pregnancy, optional BSA, close/reset and 320/390-pixel layouts.
- ZIP CRC/root SHA-256 checks and a fresh extraction rebuild verify that the packaged runtime matches the source.

Clinical approval, BNF reconciliation, completion of remaining drug records, physical-phone testing and HTTPS offline installation/update verification remain pending. No automatic drug-dose selection is implemented. Below is the previous drug-source verification record, retained as historical context.

'''
(D/'VERIFICATION.md').write_text(verification+(ROOT/'verification_v07.md').read_text())
print('Prepared v0.8.0: adult eGFR calculator; clinical records unchanged from v0.7.0')
