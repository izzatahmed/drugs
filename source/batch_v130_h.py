# ---- Batch H: anticoagulation & haematology catalog entries ----
add('bivalirudin', 'Bivalirudin', promote=True, flag='adjust', metric='CrCl · mL/min (Cockcroft–Gault)',
 summary='Bolus unchanged; infusion 1 mg/kg/h at CrCl <30 and 0.25 mg/kg/h on haemodialysis.',
 mods=dict(ckd=M('summarized', [T('PCI · US label', [('Any renal function', 'Bolus unchanged'), ('CrCl <30 mL/min', 'Maintenance infusion 1 mg/kg/h')])], 'Monitor anticoagulant status in renal impairment.',
   ['No reduction in the bolus dose is needed for any degree of renal impairment', 'In patients with creatinine clearance less than 30mL/min (by Cockcroft Gault equation), reduce the infusion rate to 1 mg/kg/h', 'Monitor anticoagulant status in patients with renal impairment']),
  ihd=M('summarized', [T('Haemodialysis · US label', [('Haemodialysis', 'Bolus unchanged; infusion 0.25 mg/kg/h')])], 'About 25% is cleared by haemodialysis.', ['In patients on hemodialysis, reduce the infusion rate to 0.25 mg/kg/h', 'Approximately 25% bivalirudin is cleared by hemodialysis'])))
add('eptifibatide', 'Eptifibatide', promote=True, flag='adjust', metric='CrCl · mL/min',
 summary='CrCl <50: same bolus, infusion 1 mcg/kg/min. Contraindicated in patients dependent on dialysis.',
 mods=dict(ckd=M('summarized', [T('ACS / PCI · US label', [('CrCl ≥50 mL/min', '180 mcg/kg bolus, then 2 mcg/kg/min'), ('CrCl <50 mL/min', '180 mcg/kg bolus, then 1 mcg/kg/min')])], '', ['In patients with creatinine clearance less than 50 mL/min, reduce the infusion to 1 mcg/kg/min']),
  ihd=M('avoid', notes='Contraindicated in dependency on renal dialysis.', ev=['Dependency on renal dialysis']), pd=M('avoid', notes='Contraindicated in dependency on renal dialysis.', ev=['Dependency on renal dialysis'])))
add('tirofiban', 'AGGRASTAT', promote=True, flag='adjust', metric='CrCl · mL/min',
 summary='CrCl ≤60: 25 mcg/kg over 5 min, then 0.075 mcg/kg/min (half the usual infusion). Clearance falls >50% at CrCl <30 including haemodialysis.',
 mods=dict(ckd=M('summarized', [T('ACS · US label', [('CrCl >60 mL/min', '25 mcg/kg within 5 min, then 0.15 mcg/kg/min up to 18 h'), ('CrCl ≤60 mL/min', '25 mcg/kg within 5 min, then 0.075 mcg/kg/min')])], '',
   ['In patients with creatinine clearance ≤60 mL/min, give 25 mcg/kg within 5 minutes and then 0.075 mcg/kg/min', 'The recommended dosage is 25 mcg/kg administered intravenously within 5 minutes and then 0.15 mcg/kg/min for up to 18 hours']),
  ihd=M('summarized', [T('Haemodialysis · US label', [('Haemodialysis (CrCl ≤60)', '25 mcg/kg within 5 min, then 0.075 mcg/kg/min')])], '',
   ['In patients with creatinine clearance ≤60 mL/min, give 25 mcg/kg within 5 minutes and then 0.075 mcg/kg/min', 'Plasma clearance of tirofiban is decreased about 40% in subjects with creatinine clearance <60 mL/min and >50% in patients with creatinine clearance <30 mL/min, including patients requiring hemodialysis'])))
add('fondaparinux', 'Fondaparinux sodium', promote=True, flag='caution', metric='CrCl · mL/min',
 summary='Contraindicated at CrCl <30 for VTE prophylaxis or treatment. Bleeding risk rises as clearance falls (≈40% lower at CrCl 30–50).',
 mods=dict(ckd=M('summarized', [T('VTE prophylaxis / treatment · US label', [('CrCl 30–50 mL/min', 'Clearance ≈40% lower: higher bleeding risk, use with caution'), ('CrCl <30 mL/min', 'Contraindicated')])], '',
   ['Severe renal impairment (creatinine clearance less than 30 mL/min) in prophylaxis or treatment of venous thromboembolism', 'approximately 40% lower in patients with moderate renal impairment (CrCl 30 mL/min to 50 mL/min)',
    'Fondaparinux sodium increases the risk of bleeding in adult patients with impaired renal function due to reduced clearance']),
  ihd=M('avoid', notes='Contraindicated at CrCl <30 mL/min.', ev=['Severe renal impairment (creatinine clearance less than 30 mL/min) in prophylaxis or treatment of venous thromboembolism']),
  pd=M('avoid', notes='Contraindicated at CrCl <30 mL/min.', ev=['Severe renal impairment (creatinine clearance less than 30 mL/min) in prophylaxis or treatment of venous thromboembolism'])))
add('dalteparin', 'FRAGMIN', promote=True, flag='monitor', metric='CrCl · mL/min; anti-Xa',
 summary='At CrCl <30 (cancer VTE) monitor anti-Xa levels to set the dose; elimination is prolonged.',
 mods=dict(ckd=M('summarized', [T('Extended VTE treatment in cancer · US label', [('CrCl <30 mL/min', 'Monitor anti-Xa levels to determine the dose')])], 'Prolonged elimination at CrCl <30: consider doubling the time before neuraxial catheter removal.',
   ['In patients with severely impaired renal function (CrCl <30 mL/min), monitor anti-Xa levels to determine the appropriate FRAGMIN dose',
    'For patients with creatinine clearance <30 mL/minute, additional considerations are necessary because elimination of FRAGMIN may be more prolonged']),
  ihd=M('specialist', notes='Anti-Xa half-life about 5.7 h in haemodialysis patients (single IV dose); dose by anti-Xa levels.', ev=['In patients with chronic renal insufficiency requiring hemodialysis, the mean terminal half-life of anti-Xa activity following a single intravenous dose of 5,000 units FRAGMIN was 5.7 ± 2.0 hours'])))
add('argatroban', 'Argatroban', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)',
 summary='No dose adjustment in renal dysfunction; about 20% cleared during a 4-h haemodialysis.',
 mods=dict(ckd=M('summarized', [T('HIT / PCI · US label', [('Any renal function', 'No dose adjustment')])], '', ['No dosage adjustment is necessary in patients with renal dysfunction']),
  ihd=M('summarized', [T('Haemodialysis · US label', [('Intermittent haemodialysis', 'Studied at 2–3 mcg/kg/min (or 250 mcg/kg bolus then 2 mcg/kg/min); ≈20% cleared during a 4-h session')])], '',
   ['Argatroban was administered at a rate of 2 to 3 mcg/kg/min (begun at least 4 hours prior to dialysis) or as a bolus dose of 250 mcg/kg at the start of dialysis followed by a continuous infusion of 2 mcg/kg/min',
    'approximately 20% of argatroban was cleared through dialysis'])))
add('tranexamic-acid', 'Tranexamic acid tablets (Lysteda)', promote=True, flag='adjust', metric='Serum creatinine · mg/dL',
 summary='Heavy menstrual bleeding: reduce the oral dose when serum creatinine >1.4 mg/dL (label table).',
 mods=dict(ckd=M('summarized', [T('Heavy menstrual bleeding, oral, max 5 days · US label', [('SCr ≤1.4 mg/dL', '1,300 mg three times daily'), ('SCr >1.4 to ≤2.8 mg/dL', '1,300 mg twice daily'), ('SCr >2.8 to ≤5.7 mg/dL', '1,300 mg once daily'), ('SCr >5.7 mg/dL', '650 mg once daily')])],
   'The IV product has its own renal table — check the IV label.', ['Cr above 1.4 mg/dL and ≤ 2.8 mg/dL: 1,300 mg two times a day (2,600 mg/day) Cr above 2.8 mg/dL and ≤ 5.7 mg/dL: 1,300 mg once a day (1,300 mg/day) Cr above 5.7 mg/dL: 650 mg once a day (650 mg/day)',
    '1,300 mg three times a day (3,900 mg/day) for a maximum of 5 days during monthly menstruation'])))
add('desmopressin', 'Desmopressin acetate injection', promote=True, flag='caution', metric='CrCl · mL/min',
 summary='Contraindicated at CrCl <50 (hyponatraemia risk).',
 mods=dict(ckd=M('summarized', [T('All indications · US label', [('CrCl ≥50 mL/min', 'Usual dose'), ('CrCl <50 mL/min', 'Contraindicated (hyponatraemia)')])], '', ['Desmopressin acetate is contraindicated in patients with moderate to severe renal impairment (defined as a creatinine clearance below 50 mL/min)']),
  ihd=M('avoid', notes='Contraindicated at CrCl <50 mL/min.', ev=['Desmopressin acetate is contraindicated in patients with moderate to severe renal impairment (defined as a creatinine clearance below 50 mL/min)']),
  pd=M('avoid', notes='Contraindicated at CrCl <50 mL/min.', ev=['Desmopressin acetate is contraindicated in patients with moderate to severe renal impairment (defined as a creatinine clearance below 50 mL/min)'])))
add('aminocaproic-acid', 'Aminocaproic acid', promote=True, flag='monitor', metric='Renal clearance ≈ CrCl',
 summary='Renally cleared (renal clearance about equal to CrCl); the US label gives no renal dose. Removed by haemodialysis.',
 mods=dict(ckd=M('specialist', notes='Renal clearance approximates creatinine clearance; no numeric renal dose in the label.', ev=['Renal clearance (116 mL/min) approximates endogenous creatinine clearance']),
  ihd=M('specialist', notes='Removed by haemodialysis and possibly by peritoneal dialysis (overdose context).', ev=['evidence exists that aminocaproic acid is removed by hemodialysis and may be removed by peritoneal dialysis'])))
for i, brand, ev in [('cangrelor', 'KENGREAL', 'No dosage adjustment is required for patients with mild, moderate, or severe renal impairment'),
                     ('prasugrel', 'EFFIENT', 'No dosage adjustment is necessary for patients with renal impairment'),
                     ('ticagrelor', 'BRILINTA', 'No dosage adjustment is needed in patients with renal impairment'),
                     ('idarucizumab', 'PRAXBIND', 'No dose adjustment is required in renally impaired patients'),
                     ('filgrastim', 'Filgrastim', 'However, dose adjustment in patients with renal impairment is not necessary')]:
    add(i, brand, promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)', summary='No renal dose adjustment (US label).',
        mods=dict(ckd=M('summarized', [T('All indications · US label', [('Any renal impairment', 'No dose adjustment')])], '', [ev])))
C['ticagrelor']['modalities']['ihd'] = M('summarized', [T('Haemodialysis · US label', [('ESRD on dialysis', 'Not dialysable; ESRD on dialysis was not enrolled in efficacy trials')])], '',
   ['showing that BRILINTA is not dialyzable', 'Clinical efficacy and safety studies with BRILINTA did not enroll patients with end-stage renal disease (ESRD) on dialysis'])
C['prasugrel']['modalities']['ihd'] = M('summarized', [T('Haemodialysis · US label', [('Haemodialysis', 'No adjustment stated; active metabolite not likely removed by dialysis')])], '', ['The prasugrel active metabolite is not likely to be removed by dialysis'])
add('pegfilgrastim', 'Pegfilgrastim', promote=True, flag='no_adjust', metric='No PK effect of renal function (US label)', summary='Renal dysfunction, including end-stage disease, had no effect on pegfilgrastim PK.',
 mods=dict(ckd=M('summarized', [T('All indications · US label', [('Any renal function, including ESRD', 'Usual dose (no PK change)')])], '', ['In a study of 30 subjects with varying degrees of renal dysfunction, including end stage renal disease, renal dysfunction had no effect on the pharmacokinetics of pegfilgrastim'])))
add('eltrombopag', 'PROMACTA', promote=True, flag='monitor', metric='CrCl · mL/min', summary='Exposure lower in renal impairment (32–60%); no renal dose is given — monitor response and renal function.',
 mods=dict(ckd=M('specialist', notes='Exposure 32–36% lower in mild–moderate and 60% lower in severe impairment; the label gives no renal dose change. Evaluate unexpected serum creatinine results.',
   ev=['In the event of an unexpected serum creatinine test result, further evaluation of renal function should be performed'])))
add('hydroxocobalamin', 'CYANOKIT', promote=True, flag='monitor', metric='Monitor renal function',
 summary='Acute kidney injury with oxalate crystals reported: monitor renal function for 7 days after treatment.',
 mods=dict(ckd=M('specialist', notes='Acute renal failure with acute tubular necrosis and calcium oxalate crystals has been reported. Monitor renal function for 7 days.',
   ev=['Acute renal failure with acute tubular necrosis, renal impairment and urine calcium oxalate crystals have been reported following CYANOKIT therapy', 'Monitor renal function for 7 days following CYANOKIT therapy'])))
# ESAs
add('epoetin-alfa', 'EPOGEN', promote=True, flag='monitor', metric='Haemoglobin (CKD on / not on dialysis)',
 summary='CKD anaemia: start 50–100 units/kg three times weekly; start on dialysis when Hb <10 g/dL; reduce or interrupt as Hb approaches 11 (dialysis) or exceeds 10 (not on dialysis).',
 mods=dict(ckd=M('summarized', [T('Anaemia of CKD, not on dialysis · US label', [('Start', '50–100 units/kg three times weekly IV or SC (consider only when Hb <10 g/dL)'), ('Hb >10 g/dL', 'Reduce or interrupt; use the lowest dose that avoids transfusion')])], '',
   ['The recommended starting dose for adult patients is 50 to 100 Units/kg 3 times weekly intravenously or subcutaneously', 'If the hemoglobin level exceeds 10 g/dL, reduce or interrupt the dose of Epogen, and use the lowest dose of Epogen sufficient to reduce the need for RBC transfusions']),
  ihd=M('summarized', [T('Anaemia of CKD on dialysis · US label', [('Start (Hb <10 g/dL)', '50–100 units/kg three times weekly IV or SC'), ('Hb approaching or above 11 g/dL', 'Reduce or interrupt')])], '',
   ['For adult patients with CKD on dialysis: Initiate Epogen treatment when the hemoglobin level is less than 10 g/dL', 'If the hemoglobin level approaches or exceeds 11 g/dL, reduce or interrupt the dose of Epogen', 'The recommended starting dose for adult patients is 50 to 100 Units/kg 3 times weekly intravenously or subcutaneously'])))
C['epoetin-alfa']['modalities']['pd'] = C['epoetin-alfa']['modalities']['ihd']
add('darbepoetin-alfa', 'ARANESP', promote=True, flag='monitor', metric='Haemoglobin (CKD on / not on dialysis)',
 summary='CKD on dialysis: 0.45 mcg/kg weekly or 0.75 mcg/kg every 2 weeks (IV preferred on haemodialysis); not on dialysis: 0.45 mcg/kg every 4 weeks.',
 mods=dict(ckd=M('summarized', [T('Anaemia of CKD, not on dialysis · US label', [('Start (Hb <10 g/dL)', '0.45 mcg/kg IV or SC every 4 weeks')])], '', ['0.45 mcg/kg intravenously or subcutaneously at 4 week intervals']),
  ihd=M('summarized', [T('Anaemia of CKD on dialysis · US label', [('Start (Hb <10 g/dL)', '0.45 mcg/kg weekly or 0.75 mcg/kg every 2 weeks; IV route recommended on haemodialysis'), ('Hb approaching or above 11 g/dL', 'Reduce or interrupt')])], '',
   ['0.45 mcg/kg intravenously or subcutaneously weekly, or - 0.75 mcg/kg intravenously or subcutaneously every 2 weeks - Intravenous route is recommended for patients on hemodialysis', 'If the hemoglobin level approaches or exceeds 11 g/dL, reduce or interrupt the dose of Aranesp'])))
C['darbepoetin-alfa']['modalities']['pd'] = C['darbepoetin-alfa']['modalities']['ihd']
add('methoxy-polyethylene-glycol-epoetin-beta', 'MIRCERA', promote=True, flag='monitor', metric='Haemoglobin (CKD on / not on dialysis)',
 summary='ESA-naive adults: 0.6 mcg/kg every 2 weeks (IV or SC); not on dialysis alternatively 1.2 mcg/kg monthly SC.',
 mods=dict(ckd=M('summarized', [T('Anaemia of CKD, not on dialysis · US label', [('Start (ESA-naive)', '1.2 mcg/kg once monthly SC, or 0.6 mcg/kg every 2 weeks IV or SC')])], '',
   ['CKD patients not on dialysis: 1.2 mcg/kg body weight administered once every month as a single subcutaneous injection', 'Alternatively, a starting dose of 0.6 mcg/kg body weight may be administered once every two weeks as a single intravenous or subcutaneous injection']),
  ihd=M('summarized', [T('Anaemia of CKD on dialysis · US label', [('Start (ESA-naive)', '0.6 mcg/kg every 2 weeks IV or SC')])], '', ['CKD patients on dialysis: 0.6 mcg/kg body weight administered once every two weeks'])))
C['methoxy-polyethylene-glycol-epoetin-beta']['modalities']['pd'] = C['methoxy-polyethylene-glycol-epoetin-beta']['modalities']['ihd']
# IV iron
add('iron-sucrose', 'VENOFER', promote=True, flag='monitor', metric='CKD setting (NDD / HD / PD)',
 summary='HD: 100 mg per session; NDD-CKD: 200 mg on 5 occasions over 14 days; PD: 300, 300, 400 mg over 28 days. Not dialysable.',
 mods=dict(ckd=M('summarized', [T('Iron deficiency anaemia, non-dialysis CKD · US label', [('NDD-CKD', '200 mg IV on 5 different occasions within 14 days (total 1,000 mg)')])], '',
   ['Administer Venofer 200 mg undiluted as a slow intravenous injection over 2 to 5 minutes or as an infusion of 200 mg in a maximum of 100 mL of 0.9% NaCl over a period of 15 minutes', 'Administer on 5 different occasions over a 14 day period']),
  ihd=M('summarized', [T('Haemodialysis-dependent CKD · US label', [('HDD-CKD', '100 mg IV per consecutive haemodialysis session (slow injection or ≥15-min infusion)')])], 'Not dialysable through high-efficiency or high-flux membranes.',
   ['Administer Venofer 100 mg undiluted as a slow intravenous injection over 2 to 5 minutes, or as an infusion of 100 mg diluted in a maximum of 100 mL of 0.9% NaCl over a period of at least 15 minutes, per consecutive hemodialysis session']),
  pd=M('summarized', [T('Peritoneal-dialysis-dependent CKD · US label', [('PDD-CKD', '300 mg over 1.5 h, repeat 14 days later, then 400 mg over 2.5 h 14 days after that')])], '',
   ['Administer Venofer in 3 divided doses, given by slow intravenous infusion, within a 28 day period: 2 infusions each of 300 mg over 1.5 hours 14 days apart followed by one 400 mg infusion over 2.5 hours 14 days later'])))
add('ferumoxytol', 'FERAHEME', promote=True, flag='monitor', metric='CKD (dosing not renally adjusted)',
 summary='510 mg IV, then 510 mg 3–8 days later. On haemodialysis give after BP is stable and at least 1 h of dialysis. Not removed by haemodialysis.',
 mods=dict(ckd=M('summarized', [T('Iron deficiency anaemia incl. CKD · US label', [('Adults', '510 mg IV, then 510 mg 3–8 days later')])], '', ['The recommended dose of Feraheme is an initial 510 mg dose followed by a second 510 mg dose 3 to 8 days later']),
  ihd=M('summarized', [T('Haemodialysis · US label', [('Haemodialysis', 'Give once BP is stable and after at least 1 h of the session; not removed by HD')])], '',
   ['For patients receiving hemodialysis, administer Feraheme once the blood pressure is stable and the patient has completed at least one hour of hemodialysis', 'Feraheme is not removed by hemodialysis'])))
add('ferric-carboxymaltose', 'Ferric carboxymaltose', promote=True, flag='monitor', metric='Body weight (CKD not on dialysis is an approved setting)',
 summary='Weight ≥50 kg: 750 mg IV twice, at least 7 days apart (1,500 mg per course); approved for non-dialysis CKD.',
 mods=dict(ckd=M('summarized', [T('Iron deficiency anaemia incl. non-dialysis CKD · US label', [('Weight ≥50 kg', '750 mg IV × 2, ≥7 days apart (1,500 mg per course)')])], '',
   ['the recommended dosage is ferric carboxymaltose injection 750 mg intravenously in two doses separated by at least 7 days for a total cumulative dose of 1,500 mg of iron per course', 'adult patients who have non-dialysis dependent chronic kidney disease'])))
add('iron-dextran', 'INFED', promote=True, flag='monitor', metric='Iron deficit', summary='Dose from the iron-deficit formula; removal by dialysis is negligible. Ferritin may mislead on chronic dialysis.',
 mods=dict(ihd=M('summarized', [T('Dialysis · US label', [('Haemodialysis', 'Not removed by dialysis; dose from iron deficit (ferritin may be unreliable on chronic dialysis)')])], '',
   ['In vitro studies have shown that removal of iron dextran by dialysis is negligible', 'Serum ferritin may not be an accurate measure of body iron stores in patients on chronic dialysis'])))
add('ferric-derisomaltose', 'MONOFERRIC', promote=True, flag='monitor', metric='Body weight', summary='Not excreted by the kidneys; no renal dose statement in the US label.',
 mods=dict(ckd=M('specialist', notes='Not excreted via the kidneys; no renal dose statement.', ev=['Due to the size of the complex, Monoferric is not excreted via the kidneys'])))
NOREN = 'The current US label gives no renal dose statement.'
for i, brand in [('unfractionated-heparin', 'Heparin sodium'), ('protamine', 'Protamine sulfate'), ('alteplase', 'ACTIVASE'), ('tenecteplase', 'TNKASE'), ('andexanet-alfa', 'ANDEXXA'),
                 ('dipyridamole', 'Dipyridamole injection'), ('romiplostim', 'NPLATE'), ('cyanocobalamin', 'Cyanocobalamin')]:
    add(i, brand, promote=True, flag='monitor', metric='No renal statement in the US label', summary=NOREN, mods=dict(ckd=M('specialist', notes=NOREN)))
