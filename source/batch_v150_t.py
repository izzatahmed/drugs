# ---- Batch T: transplant & immunology, OTC & safety, label corrections ----
NOREN = 'The current US label gives no renal dose statement.'
P_('cyclophosphamide', 'Cyclophosphamide', 'monitor', 'CrCl · mL/min', 'Monitor for toxicity in moderate–severe impairment (CrCl 10–24). Dialysable: keep a consistent interval between dose and dialysis.',
   S('All indications · US label', [('Moderate or severe impairment (CrCl 10–24 mL/min)', 'No fixed reduction stated; monitor closely for toxicity')],
     ['Monitor for toxicity in patients with moderate and severe renal impairment', 'Monitor patients with severe renal impairment (creatinine clearance (CLcr) = 10 mL/min to 24 mL/min) for signs and symptoms of toxicity']),
   ihd=HDT([('Dialysis', 'Keep a consistent interval between the dose and dialysis (cyclophosphamide and metabolites are dialysable)')],
     ['Cyclophosphamide and its metabolites are dialyzable although there are probably quantitative differences depending upon the dialysis system', 'In patients requiring dialysis, consider using a consistent interval between cyclophosphamide administration and dialysis should be considered']))
P_('methotrexate', 'Methotrexate', 'caution', 'CrCl · mL/min', 'Elimination is reduced at CrCl <90 and adverse reactions increase; no numeric renal dose in this label. Not removed by HD or PD.',
   M('specialist', notes='Elimination falls at CrCl <90 mL/min and adverse-reaction risk rises; no numeric renal dose in this label. Neither HD nor PD improves elimination.',
     ev=['Methotrexate elimination is reduced in patients with renal impairment [creatinine clearance (CLcr) less than 90 mL/min, calculated using Cockcroft-Gault]', 'Patients with renal impairment are at increased risk for methotrexate adverse reactions']),
   ihd=M('specialist', notes='Neither haemodialysis nor peritoneal dialysis improves methotrexate elimination.', ev=['Neither hemodialysis nor peritoneal dialysis has been shown to improve methotrexate elimination']))
P_('rituximab', 'Rituximab', 'monitor', 'No renal statement in the US label', 'No renal dose statement; tumour lysis can cause renal failure requiring dialysis — monitor renal function.',
   M('specialist', notes='No renal dose statement. In tumour lysis syndrome, correct electrolytes, monitor renal function and fluid balance, and give supportive care including dialysis as indicated.',
     ev=['Correct electrolyte abnormalities, monitor renal function and fluid balance, and administer supportive care, including dialysis as indicated']))
P_('sirolimus', 'Sirolimus', 'no_adjust', 'No renal dose adjustment (US label)', 'No dose adjustment in renal impairment; not dialysable.',
   S('Transplant · US label', [('Any renal impairment', 'No dose adjustment')], ['Dosage adjustment is not needed in patients with impaired renal function']),
   ihd=HDT([('Haemodialysis', 'No dialysis dose in the label; not dialysable to any significant extent, so no supplement')], ['it is anticipated that sirolimus is not dialyzable to any significant extent']))
P_('everolimus', 'Everolimus', 'no_adjust', 'CrCl · mL/min', 'No influence of CrCl 25–178 on clearance; monitor kidney function.',
   S('All indications · US label', [('CrCl 25–178 mL/min', 'No change in clearance; usual dose')], ['No significant influence of creatinine clearance (25 to 178 mL/min) was detected on oral clearance (CL/F) of everolimus']))
P_('leflunomide', 'Leflunomide', 'monitor', 'Renal function', 'Not studied in renal impairment; teriflunomide is not dialysable.',
   M('specialist', notes='No dedicated renal studies; no renal dose in the label.', ev=['Dedicated studies of the effect of renal impairment on leflunomide pharmacokinetics have not been conducted']),
   ihd=HDT([('Haemodialysis or CAPD', 'No dialysis dose; teriflunomide is not dialysable, so no supplement')], ['Studies with both hemodialysis and CAPD (chronic ambulatory peritoneal dialysis) indicate that teriflunomide is not dialyzable']))
P_('tofacitinib', 'Tofacitinib', 'adjust', 'CrCl · mL/min', 'RA/PsA/AS: CrCl 30–50 or <30 → 5 mg once daily; on haemodialysis give after dialysis (no supplement if taken before).',
   S('RA / PsA / AS · US label', [('CrCl >50–80 mL/min', '5 mg twice daily'), ('CrCl 30–50 mL/min', '5 mg once daily'), ('CrCl <30 mL/min', '5 mg once daily')],
     ['Mild RI (CLcr >50 and ≤80 mL/min) 5 mg twice daily Moderate RI (CLcr ≥30 and ≤50 mL/min) 5 mg once daily Severe RI (CLcr <30 mL/min) 5 mg once daily']),
   ihd=HDT([('Haemodialysis', '5 mg once daily, after the session on dialysis days; no supplement if taken before dialysis')],
     ['For patients undergoing hemodialysis, administer the dose after the dialysis session on dialysis days. If a dose was taken before the dialysis procedure, supplemental doses are not recommended after dialysis']))
P_('upadacitinib', 'RINVOQ', 'adjust', 'Renal function', 'Severe renal impairment: 15 mg once daily.',
   S('All indications · US label', [('Severe renal impairment', '15 mg once daily')], ['Severe Renal Impairment : Recommended dosage of RINVOQ is 15 mg once daily']))
P_('baricitinib', 'Baricitinib', 'caution', 'eGFR · mL/min/1.73 m²', 'Dose by eGFR per label; not recommended on dialysis, in ESRD (eGFR <15) or AKI.',
   M('specialist', notes='Check eGFR before starting; dose reductions by eGFR are in the label. Not recommended on dialysis, in ESRD or AKI.', ev=['Evaluate baseline eGFR, liver enzymes, and complete blood count to determine treatment suitability and dose', 'Patients who are on dialysis, have end-stage renal disease (ESRD, EGFR <15 mL/min/1']),
   ihd=M('avoid', notes='Not recommended on dialysis or in ESRD.', ev=['Patients who are on dialysis, have end-stage renal disease (ESRD, EGFR <15 mL/min/1']))
P_('apremilast', 'OTEZLA', 'adjust', 'Renal function', 'Severe renal impairment: titrate with morning doses only; maintenance 30 mg once daily. XR form not recommended.',
   S('Psoriasis / PsA / Behçet · US label', [('Severe renal impairment', 'Titrate using morning doses only; maintenance 30 mg once daily'), ('Severe impairment, OTEZLA XR', 'Not recommended')],
     ['For initial dosage titration, titrate using only morning schedule listed in Table 1 and skip afternoon doses. Recommended maintenance dosage is OTEZLA 30 mg once daily', 'OTEZLA XR is not recommended for adult patients with severe renal impairment']))
P_('avacopan', 'TAVNEOS', 'no_adjust', 'No renal dose adjustment (US label)', 'No adjustment in mild to severe impairment; not studied on dialysis.',
   S('ANCA vasculitis · US label', [('Mild, moderate or severe impairment', 'No dose adjustment'), ('Dialysis', 'Not studied')], ['No dose adjustment is required for patients with mild, moderate, or severe renal impairment', 'TAVNEOS has not been studied in patients with ANCA-associated vasculitis who are on dialysis']))
P_('tocilizumab', 'Tocilizumab', 'no_adjust', 'Renal function', 'No adjustment in mild–moderate impairment; not studied in severe impairment.',
   S('All indications · US label', [('Mild or moderate impairment', 'No dose adjustment'), ('Severe impairment', 'Not studied')], ['No dose adjustment is required in patients with mild or moderate renal impairment', 'Tocilizumab products have not been studied in patients with severe renal impairment']))
P_('anakinra', 'KINERET', 'adjust', 'CrCl · mL/min', 'CrCl <30 or ESRD: consider 100 mg every other day. <2.5% removed by HD or CAPD.',
   S('RA / NOMID · US label', [('CrCl <30 mL/min or ESRD', 'Consider the prescribed dose every other day (RA: 100 mg every other day)')], ['Physicians should consider a dose of 100 mg of KINERET administered every other day for RA patients who have severe renal insufficiency or end stage renal disease (defined as creatinine clearance < 30 mL/min, as estimated from serum creatinine levels)']),
   ihd=HDT([('ESRD on HD', '100 mg every other day (RA); <2.5% removed by HD')], ['Physicians should consider a dose of 100 mg of KINERET administered every other day for RA patients who have severe renal insufficiency or end stage renal disease (defined as creatinine clearance < 30 mL/min, as estimated from serum creatinine levels)', 'Less than 2.5% of the administered dose of KINERET was removed by hemodialysis or continuous ambulatory peritoneal dialysis']))
# azathioprine is already a renal profile: add only the haemodialysis statement.
add('azathioprine', 'IMURAN', mods=dict(ihd=M('specialist', notes='About 45% is removed during an 8-hour haemodialysis.', ev=['About 30% of IMURAN is bound to serum proteins, but approximately 45% is removed during an 8-hour hemodialysis'])))
P_('belatacept', 'NULOJIX', 'no_adjust', 'No effect of renal function or dialysis on clearance', 'Renal function and concomitant dialysis did not affect belatacept clearance.',
   S('Kidney transplant · US label', [('Any GFR, including dialysis', 'Usual weight-based dose')], ['renal function (measured by calculated glomerular filtration rate [GFR]), hepatic function (measured by albumin), diabetes, and concomitant dialysis did not affect the clearance of belatacept']))
for i, brand in [('abatacept', 'ORENCIA'), ('adalimumab', 'Adalimumab'), ('anifrolumab', 'SAPHNELO'), ('basiliximab', 'SIMULECT'), ('belimumab', 'BENLYSTA'), ('eculizumab', 'SOLIRIS'),
                 ('efgartigimod', 'VYVGART'), ('etanercept', 'ENBREL'), ('inebilizumab', 'UPLIZNA'), ('infliximab', 'Infliximab'), ('iptacopan', 'FABHALTA'), ('obinutuzumab', 'GAZYVA'),
                 ('pegcetacoplan', 'Pegcetacoplan'), ('ravulizumab', 'ULTOMIRIS'), ('mycophenolate-sodium', 'Mycophenolic acid (enteric-coated)')]:
    P_(i, brand, 'monitor', 'No renal statement in the US label', NOREN, M('specialist', notes=NOREN))
# OTC & safety
P_('ibuprofen', 'Ibuprofen tablets', 'caution', 'Renal function', 'Not recommended in advanced renal disease.',
   S('All indications · US label', [('Advanced renal disease', 'Not recommended')], ['Therefore, treatment with Ibuprofen tablets is not recommended in these patients with advanced renal disease']), ihd=M('avoid', notes='Not recommended in advanced renal disease.', ev=['Therefore, treatment with Ibuprofen tablets is not recommended in these patients with advanced renal disease']))
P_('naproxen', 'Naproxen', 'caution', 'Renal function', 'Avoid in advanced renal disease unless benefit outweighs the risk of worsening renal function.',
   S('All indications · US label', [('Advanced renal disease', 'Avoid unless benefits outweigh the risk')], ['Avoid use of naproxen tablets and naproxen sodium tablets in patients with advanced renal disease unless benefits are expected to outweigh risk of worsening renal function']))
P_('celecoxib', 'Celecoxib', 'caution', 'Renal function', 'Avoid in advanced renal disease unless benefit outweighs the risk of worsening renal function.',
   S('All indications · US label', [('Advanced renal disease', 'Avoid unless benefits outweigh the risk')], ['Avoid use of celecoxib capsules in patients with advanced renal disease unless benefits are expected to outweigh risk of worsening renal function']))
P_('meloxicam', 'Meloxicam tablets', 'caution', 'Renal function', 'Not recommended in severe renal impairment; on haemodialysis maximum 7.5 mg/day.',
   S('All indications · US label', [('Severe renal impairment', 'Not recommended')], ['The use of Meloxicam Tablets, USP in subjects with severe renal impairment is not recommended']),
   ihd=HDT([('Haemodialysis', 'Maximum 7.5 mg per day (not dialysable)')], ['In patients with hemodialysis, a maximum daily dosage of 7.5 mg is recommended', 'Meloxicam is not dialyzable']))
P_('ketorolac', 'Ketorolac tromethamine', 'caution', 'Renal function', 'Contraindicated in advanced renal impairment and in volume depletion with renal-failure risk.',
   S('Pain (short term) · US label', [('Advanced renal impairment, or risk of renal failure from volume depletion', 'Contraindicated')], ['Ketorolac tromethamine is CONTRAINDICATED in patients with advanced renal impairment and in patients at risk for renal failure due to volume depletion']),
   ihd=M('avoid', notes='Contraindicated in advanced renal impairment.', ev=['Ketorolac tromethamine is CONTRAINDICATED in patients with advanced renal impairment and in patients at risk for renal failure due to volume depletion']))
P_('diclofenac-systemic', 'Diclofenac', 'caution', 'Renal function', 'No PK difference in renal impairment, but NSAID nephrotoxicity applies — avoid in advanced disease per class warnings.',
   M('specialist', notes='No PK differences were found in renal impairment; NSAID renal risks still apply.', ev=['No differences in the pharmacokinetics of diclofenac have been detected in studies of patients with renal impairment']))
P_('cimetidine', 'Cimetidine', 'adjust', 'Renal function', 'Severe renal failure: accumulation possible — use the lowest dosing frequency that controls symptoms.',
   S('All indications · US label', [('Severe renal failure', 'Use the lowest dosing frequency compatible with response')], ['In severe renal failure, accumulation may occur and the lowest frequency of dosing compatible with an adequate patient response should be used']))
P_('nizatidine', 'Nizatidine', 'adjust', 'CrCl · mL/min', 'CrCl 20–50: 150 mg daily (maintenance every other day); <20: 150 mg every other day (maintenance every 3 days).',
   S('Ulcer / GERD · US label', [('CrCl 20–50 mL/min (active)', '150 mg daily'), ('CrCl <20 mL/min (active)', '150 mg every other day'), ('CrCl 20–50 mL/min (maintenance)', '150 mg every other day'), ('CrCl <20 mL/min (maintenance)', '150 mg every 3 days')],
     ['20-50 mL/min 150 mg daily less than 20 mL/min 150 mg every other day Maintenance Therapy C cr Dose 20-50 mL/min 150 mg every other day less than 20 mL/min 150 mg every 3 days']))
P_('loperamide', 'Loperamide', 'no_adjust', 'No renal dose adjustment (US label)', 'No adjustment needed in renal impairment (mainly faecal excretion).',
   S('Diarrhoea · US label', [('Renal impairment', 'No dose adjustment')], ['dosage adjustments in patients with renal impairment are not required']))
P_('paracetamol-iv', 'Acetaminophen injection', 'caution', 'CrCl · mL/min', 'Severe renal impairment (CrCl ≤30): consider longer dosing intervals and a lower total daily dose.',
   S('Pain / fever, IV · US label', [('CrCl ≤30 mL/min', 'Longer dosing interval and reduced total daily dose may be warranted')], ['In cases of severe renal impairment, longer dosing intervals and a reduced total daily dose of acetaminophen may be warranted', 'severe renal impairment (creatinine clearance ≤ 30 mL/min)']))
C['paracetamol-iv']['label'] = 'alt/paracetamol-iv-injection.json'
P_('magnesium-hydroxide', 'Magnesium hydroxide', 'caution', 'Kidney disease', 'OTC label: ask a doctor before use in kidney disease (magnesium accumulation).',
   M('specialist', notes='Ask a doctor before use if you have kidney disease (OTC label).', ev=['Ask a doctor before use if you have kidney disease a magnesium-restricted diet']))
P_('aspirin', 'Aspirin (OTC)', 'caution', 'Kidney disease', 'OTC label: ask a doctor before use in kidney disease.',
   M('specialist', notes='Ask a doctor before use if you have kidney disease (OTC label).', ev=['you have high blood pressure, heart disease, liver cirrhosis, or kidney disease']))
