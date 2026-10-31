# ---- Batch G/E/U: gastrointestinal, electrolyte and urology/PAH catalog entries ----
def noadj(i, brand, ev, rows=None, ihd=None, summary='No renal dose adjustment (US label).', metric='No renal dose adjustment (US label)'):
    mods = dict(ckd=M('summarized', [T('All indications · US label', rows or [('Any renal impairment', 'No dose adjustment')])], '', ev if isinstance(ev, list) else [ev]))
    if ihd: mods['ihd'] = ihd
    add(i, brand, promote=True, flag='no_adjust', metric=metric, summary=summary, mods=mods)
def spec(i, brand, notes, ev, flag='caution', summary=None, metric='Renal function'):
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary or notes, mods=dict(ckd=M('specialist', notes=notes, ev=ev)))
# GI
spec('cholestyramine', 'Cholestyramine', 'Use with caution in renal insufficiency (risk of hyperchloraemic acidosis noted in the label); no renal dose.', ['Caution should also be exercised in patients with renal insufficiency or volume depletion and in patients receiving concomitant spironolactone'])
spec('dicyclomine', 'Dicyclomine', 'Not studied in renal impairment; use with caution.', ['Effects of renal impairment on PK, safety and efficacy of dicyclomine hydrochloride has not been studied', 'Dicyclomine hydrochloride should be used with caution in patients with known hepatic and renal impairment'])
spec('glycerol-rectal', 'RAVICTI (glycerol phenylbutyrate)', 'Efficacy and safety unknown in renal impairment; not studied in ESRD or haemodialysis. Monitor ammonia closely when starting.', ['The efficacy and safety of RAVICTI in patients with renal impairment are unknown', 'Monitor ammonia levels closely when starting patients with impaired renal function on RAVICTI'], flag='monitor')
spec('pancrelipase', 'ZENPEP', 'High doses can cause hyperuricaemia: consider monitoring uric acid in renal impairment.', ['Consider monitoring blood uric acid levels in patients with gout, renal impairment, or hyperuricemia during treatment with ZENPEP'], flag='monitor')
add('fosaprepitant', 'Fosaprepitant', promote=True, flag='no_adjust', metric='Renal function (no adjustment stated)', summary='Aprepitant exposure studied in severe impairment and haemodialysis; not removed by haemodialysis.',
 mods=dict(ckd=M('specialist', notes='PK studied in severe renal impairment (CrCl <30) and in ESRD on haemodialysis; no renal dose change is stated in the label.', ev=['A single 240 mg oral dose of aprepitant was administered to patients with severe renal impairment (creatinine clearance less than 30 mL/min/1']),
  ihd=M('summarized', [T('Haemodialysis · US label', [('Haemodialysis', 'No dose change stated; aprepitant is not removed by haemodialysis')])], '', ['Aprepitant is not removed by hemodialysis'])))
# Electrolytes & mineral metabolism
add('calcium-chloride', 'Calcium chloride injection', promote=True, flag='adjust', metric='Renal impairment (start low); serum calcium',
 summary='Adults with renal impairment: start at 200 mg.', mods=dict(ckd=M('summarized', [T('Hypocalcaemia · US label', [('Adults with renal impairment', 'Starting dose 200 mg')])], 'Monitor serum calcium.', ['Adults with renal impairment is 200 mg'])))
add('calcium-gluconate', 'Calcium gluconate injection', promote=True, flag='adjust', metric='Renal impairment (start low); serum calcium',
 summary='Start at the lowest dose of the range and check calcium every 4 hours.', mods=dict(ckd=M('summarized', [T('Hypocalcaemia · US label', [('Renal impairment', 'Start at the lowest dose of the range; check serum calcium every 4 h')])], '',
   ['For patients with renal impairment, initiate Calcium Gluconate Injection at the lowest dose of the recommended dose ranges for all age groups and monitor serum calcium levels every 4 hours'])))
add('magnesium-sulfate', 'Magnesium sulfate in 5% dextrose', promote=True, flag='adjust', metric='Renal impairment / urine output',
 summary='Severe impairment or urine output <0.5 mL/kg/h: 4 g load, then 1 g/h; maximum 20 g in 48 h; titrate to levels.',
 mods=dict(ckd=M('summarized', [T('Pre-eclampsia / eclampsia · US label', [('Severe impairment or urine output <0.5 mL/kg/h', '4 g load, then 1 g/h; do not exceed 20 g over 48 h')])], 'Titrate to serum magnesium. Aluminium may accumulate with prolonged use in renal impairment.',
   ['In patients with severe renal impairment and/or urine output less than 0.5 mL/kg/hour, administer a 4 gram loading dose followed by a maintenance dosage of 1 gram every hour; do not exceed the maximum recommended dosage of 20 grams over 48 hours'])))
add('potassium-chloride', 'KLOR-CON (potassium chloride ER)', promote=True, flag='caution', metric='Renal function; serum potassium',
 summary='Start at the low end of the dose range; renal impairment greatly increases hyperkalaemia risk.', mods=dict(ckd=M('summarized', [T('Hypokalaemia · US label', [('Renal impairment', 'Start at the low end of the dose range; monitor potassium closely')])], '',
   ['Renal Impairment: Initiate therapy at the low end of the dosing range', 'Patients with renal impairment have reduced urinary excretion of potassium and are at substantially increased risk of hyperkalemia'])))
add('potassium-citrate', 'UROCIT-K', promote=True, flag='caution', metric='GFR (mL/kg/min)', summary='Contraindicated when GFR <0.7 mL/kg/min (soft-tissue calcification, hyperkalaemia).',
 mods=dict(ckd=M('summarized', [T('Kidney stones / RTA · US label', [('GFR <0.7 mL/kg/min', 'Contraindicated (soft-tissue calcification and hyperkalaemia risk)')])], '',
   ['In patients with renal insufficiency (glomerular filtration rate of less than 0.7 ml/kg/min), because of the danger of soft tissue calcification and increased risk for the development of hyperkalemia']),
  ihd=M('avoid', notes='Contraindicated in renal insufficiency with GFR <0.7 mL/kg/min.', ev=['In patients with renal insufficiency (glomerular filtration rate of less than 0.7 ml/kg/min), because of the danger of soft tissue calcification and increased risk for the development of hyperkalemia'])))
add('potassium-phosphate', 'Potassium phosphates injection', promote=True, flag='caution', metric='eGFR · mL/min/1.73 m²',
 summary='eGFR 30–59: start at the low end of the range. Contraindicated at eGFR <30 or end-stage disease.',
 mods=dict(ckd=M('summarized', [T('Hypophosphataemia · US label', [('eGFR 30–59', 'Start at the low end of the dose range; monitor phosphorus, potassium, calcium, magnesium'), ('eGFR <30 or ESRD', 'Contraindicated')])], '',
   ['In patients with moderate renal impairment (eGFR ≥ 30 mL/min/1.73 m 2 to < 60 mL/min/1.73 m 2 ), start at the low end of the dose range', 'Severe renal impairment (eGFR less than 30 mL/min/1.73 m 2 ) or end stage renal disease']),
  ihd=M('avoid', notes='Contraindicated in end-stage renal disease.', ev=['Severe renal impairment (eGFR less than 30 mL/min/1.73 m 2 ) or end stage renal disease']),
  pd=M('avoid', notes='Contraindicated in end-stage renal disease.', ev=['Severe renal impairment (eGFR less than 30 mL/min/1.73 m 2 ) or end stage renal disease'])))
spec('sodium-phosphate-iv', 'Sodium phosphates injection', 'Use with great care in severe renal insufficiency: sodium retention; no numeric renal dose.', ['Solutions containing sodium ions should be used with great care, if at all, in patients with congestive heart failure, severe renal insufficiency and in clinical states in which there exists edema with sodium retention'])
add('doxercalciferol', 'Doxercalciferol injection', promote=True, flag='monitor', metric='CKD on dialysis (iPTH-guided)', summary='CKD on dialysis: 4 mcg IV three times weekly at the end of dialysis; maximum 18 mcg/week; titrate to iPTH.',
 mods=dict(ihd=M('summarized', [T('Secondary hyperparathyroidism, CKD on dialysis · US label', [('Start', '4 mcg IV bolus three times weekly at the end of dialysis (no more often than every other day)'), ('Maximum', '18 mcg per week')])], 'Active metabolite not removed by haemodialysis.',
   ['Initiate dosing at 4 mcg by bolus intravenous administration three times weekly at the end of dialysis (no more frequently than every other day)', 'Maximum dose is 18 mcg weekly'])))
add('sevelamer-hydrochloride', 'Sevelamer hydrochloride', promote=True, flag='monitor', metric='Serum phosphorus (CKD on dialysis)', summary='CKD on dialysis: start 800–1600 mg with meals by serum phosphorus; not studied in CKD not on dialysis.',
 mods=dict(ckd=M('insufficient_data', notes='Not studied in CKD not on dialysis.', ev=['The safety and efficacy of sevelamer hydrochloride tablets in CKD patients who are not on dialysis have not been studied']),
  ihd=M('summarized', [T('Hyperphosphataemia, CKD on dialysis · US label', [('Start', '800–1600 mg with each meal according to serum phosphorus (label Table 1)')])], '',
   ['e of sevelamer hydrochloride tablets is 800 to 1600 mg, which can be administered as one or two 800 mg sevelamer hydrochloride tablets or two to four 400 mg sevelamer hydrochloride tablets, with meals based on serum phosphorus level'.lstrip('e ')])))
C['sevelamer-hydrochloride']['modalities']['pd'] = C['sevelamer-hydrochloride']['modalities']['ihd']
spec('levocarnitine', 'Levocarnitine', 'High-dose oral levocarnitine can accumulate toxic metabolites (TMA, TMAO) in severe renal impairment or ESRD on dialysis; oral safety not evaluated in renal insufficiency.',
 ['The safety and efficacy of oral levocarnitine has not been evaluated in patients with renal insufficiency',
  'Chronic administration of high doses of oral levocarnitine in patients with severely compromised renal function or in ESRD patients on dialysis may result in accumulation of the potentially toxic metabolites, trimethylamine (TMA) and trimethylamine-N-oxide (TMAO), since these metabolites are normal'.split(', since')[0]])
spec('sodium-polystyrene-sulfonate', 'Sodium polystyrene sulfonate', 'Consider dialysis and other definitive measures in severe hyperkalaemia; no renal dose. Intestinal necrosis risk factors include renal failure.',
 ['Therefore, other definitive measures, including dialysis, should always be considered and may be imperative'], flag='monitor')
spec('ergocalciferol', 'Ergocalciferol', 'No renal dose in the label; hypervitaminosis D can impair renal function — monitor calcium.', ['Impairment of renal function with polyuria, nocturia, polydipsia, hypercalciuria, reversible azotemia, hypertension, nephrocalcinosis, generalized vascular calcification, or irreversible renal insufficiency'], flag='monitor')
# Urology / PAH / gout
add('allopurinol-iv', 'ALOPRIM (allopurinol IV)', promote=True, flag='adjust', metric='CrCl · mL/min',
 summary='CrCl 10–20: 200 mg/day; <10: 100 mg/day; on dialysis 50 mg every 12 h or 100 mg every 24 h.',
 mods=dict(ckd=M('summarized', [T('Tumour lysis prophylaxis, IV · US label Table 2', [('CrCl 10–20 mL/min', '200 mg/day'), ('CrCl <10 mL/min', '100 mg/day')])], '', ['Creatinine Clearance Recommended Daily Dose 10 to 20 mL/min 200 mg/day Less than 10 mL/min 100 mg/day On dialysis 50 mg every 12 hours, or 100 mg every 24 hours']),
  ihd=M('summarized', [T('Dialysis · US label Table 2', [('On dialysis', '50 mg every 12 h or 100 mg every 24 h')])], '', ['Creatinine Clearance Recommended Daily Dose 10 to 20 mL/min 200 mg/day Less than 10 mL/min 100 mg/day On dialysis 50 mg every 12 hours, or 100 mg every 24 hours'])))
noadj('ambrisentan', 'LETAIRIS', ['There was no significant impact of mild or moderate renal impairment on exposure to ambrisentan', 'Dose adjustment of Letairis in patients with mild or moderate renal impairment is therefore not required'], rows=[('Mild or moderate impairment', 'No dose adjustment'), ('Severe impairment', 'Not characterised (studied CrCl 20–150)')])
noadj('bosentan', 'TRACLEER', ['The effect of renal impairment on the pharmacokinetics of bosentan is small and does not require dosing adjustment'],
 ihd=M('summarized', [T('Dialysis · US label', [('Haemodialysis', 'No adjustment stated; unlikely to be removed by dialysis')])], '', ['Bosentan is unlikely to be effectively removed by dialysis due to the high molecular weight and extensive plasma protein binding']))
add('iloprost', 'Iloprost injection', promote=True, flag='adjust', metric='eGFR · mL/min', summary='eGFR <30: start the infusion at 0.5 ng/kg/min (0.25 if not tolerated) and titrate.',
 mods=dict(ckd=M('summarized', [T('IV iloprost · US label', [('eGFR <30 mL/min', 'Start at 0.5 ng/kg/min and titrate; reduce to 0.25 ng/kg/min if not tolerated')])], 'Effect of dialysis not evaluated.',
   ['Patients with renal impairment with eGFR less than 30 mL/min: initiate infusion at 0.5 ng/kg/minute and titrate as described above', 'The effect of dialysis on iloprost exposure has not been evaluated'])))
add('macitentan', 'OPSUMIT', promote=True, flag='no_adjust', metric='CrCl · mL/min', summary='Exposure up 30% (60% for the metabolite) at CrCl 15–29; no dose change stated. Dialysis unlikely to remove it.',
 mods=dict(ckd=M('specialist', notes='At CrCl 15–29, exposure rose 30% (active metabolite 60%); the label gives no renal dose change.', ev=['Exposure to macitentan and its active metabolite in patients with severe renal impairment (CrCl 15–29 mL/min) compared to healthy subjects was increased by 30% and 60%, respectively'])))
noadj('pegloticase', 'KRYSTEXXA', ['No dose adjustment is required for patients with renal impairment'])
add('probenecid', 'Probenecid', promote=True, flag='caution', metric='GFR · mL/min', summary='May not be effective at GFR ≤30; avoid with penicillin in renal impairment.',
 mods=dict(ckd=M('summarized', [T('Gout · US label', [('Some renal impairment', 'Usable; dose requirements may be higher'), ('GFR ≤30 mL/min', 'May not be effective')])], 'Not recommended with a penicillin when renal impairment is known.',
   ['Probenecid has been used in patients with some renal impairment but dosage requirements may be increased', 'Probenecid may not be effective in chronic renal insufficiency particularly when the glomerular filtration rate is 30 mL/minute or less',
    'Because of its mechanism of action, probenecid is not recommended in conjunction with a penicillin in the presence of known renal impairment'])))
noadj('selexipag', 'UPTRAVI', ['No adjustment to the dosing regimen is needed in patients with estimated glomerular filtration rate ≥15 mL/min', 'There is no clinical experience with UPTRAVI in patients undergoing dialysis or in patients with glomerular filtration rates <15 mL/min'],
 rows=[('eGFR ≥15 mL/min', 'No dose adjustment'), ('eGFR <15 or dialysis', 'No clinical experience')],
 ihd=M('insufficient_data', notes='No clinical experience on dialysis; dialysis unlikely to remove it (highly protein bound).', ev=['Dialysis is unlikely to be effective because selexipag and its active metabolite are highly protein-bound']))
add('sildenafil', 'VIAGRA', promote=True, flag='adjust', metric='CrCl · mL/min', summary='No adjustment at CrCl ≥30; consider starting at 25 mg if CrCl <30 (higher levels).',
 mods=dict(ckd=M('summarized', [T('Erectile dysfunction · US label', [('CrCl 30–80 mL/min', 'No dose adjustment'), ('CrCl <30 mL/min', 'Consider a 25 mg starting dose')])], 'Revatio (PAH) has its own label.',
   ['No dose adjustment is required for mild (CLcr=50–80 mL/min) and moderate (CLcr=30–49 mL/min) renal impairment', 'Consider a starting dose of 25 mg in patients > 65 years, patients with hepatic impairment (e.g., cirrhosis), and patients with severe renal impairment ('])))
add('tadalafil', 'Tadalafil (ED/BPH)', promote=True, flag='adjust', metric='CrCl · mL/min',
 summary='As needed: CrCl 30–50 start 5 mg, max 10 mg per 48 h; CrCl <30 or haemodialysis max 5 mg per 72 h. Once-daily use not recommended at CrCl <30.',
 mods=dict(ckd=M('summarized', [T('Erectile dysfunction, as needed · US label', [('CrCl 30–50 mL/min', 'Start 5 mg no more than once daily; maximum 10 mg once every 48 h'), ('CrCl <30 mL/min', 'Maximum 5 mg once every 72 h')]),
                                 T('Once-daily use · US label', [('CrCl <30 mL/min', 'Not recommended')])], 'Adcirca (PAH) has its own label.',
   ['Creatinine clearance 30 to 50 mL/min: A starting dose of 5 mg not more than once per day is recommended, and the maximum dose is 10 mg not more than once in every 48 hours',
    'Creatinine clearance less than 30 mL/min or on hemodialysis: The maximum dose is 5 mg not more than once in every 72 hours', 'Creatinine clearance less than 30 mL/min or on hemodialysis: tadalafil tablets for once daily use are not recommended']),
  ihd=M('summarized', [T('Haemodialysis · US label', [('As needed', 'Maximum 5 mg once every 72 h'), ('Once daily', 'Not recommended')])], '',
   ['Creatinine clearance less than 30 mL/min or on hemodialysis: The maximum dose is 5 mg not more than once in every 72 hours', 'Creatinine clearance less than 30 mL/min or on hemodialysis: tadalafil tablets for once daily use are not recommended'])))
noadj('treprostinil', 'Treprostinil', ['No dose adjustments are required in patients with renal impairment'],
 ihd=M('summarized', [T('Dialysis · US label', [('Severe impairment on dialysis', 'No adjustment: exposure unchanged; not cleared by dialysis')])], '',
   ['In patients with severe renal impairment requiring dialysis (n=8), administration of a single 1 mg dose of orally administered treprostinil pre- and post-dialysis resulted in AUC 0-inf that was not significantly altered compared to healthy subjects', 'Treprostinil is not cleared by dialysis']))
