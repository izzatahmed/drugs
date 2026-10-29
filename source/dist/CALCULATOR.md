# Adult eGFR calculator · v0.8.0

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

- NIDDK · adult CKD-EPI equations: https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/glomerular-filtration-rate-equations/adults — 2021 creatinine equation, units and coefficients
- NIDDK · previous eGFR equations: https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/glomerular-filtration-rate-equations/adults/previous — IDMS MDRD; the app explicitly omits the historical race multiplier
- NIDDK · kidney function for drug dosing: https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/ckd-drug-dosing-providers — Kidney-function measures, de-indexing and decision cutoffs
- NIDDK · clinical measurements and eGFR accuracy: https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/factors-affecting-egfr-accuracy/clinical-measurements — Non-steady-state and creatinine limitations
- NKF · CKD-EPI 2021 implementation: https://www.kidney.org/recommendations-implementing-ckd-epi-2021-race-free-egfr-calculation-guidelines-clinical — Table S1 published verification values
- eviQ · body surface area: https://www.eviq.org.au/clinical-resources/eviq-calculators/3198-body-surface-area-calculator — Mosteller BSA formula
