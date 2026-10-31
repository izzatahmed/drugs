# ---- Batch A: antimicrobial catalog entries ----
def noadj(i, brand, ev, rows=None, ihd=None, pd=None, summary='No renal dose adjustment (US label).', metric='No renal dose adjustment (US label)', flag='no_adjust'):
    mods = dict(ckd=M('summarized', [T('All indications · US label', rows or [('Any renal impairment', 'No dose adjustment')])], '', ev if isinstance(ev, list) else [ev]))
    if ihd: mods['ihd'] = ihd
    if pd: mods['pd'] = pd
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary, mods=mods)
def spec(i, brand, notes, ev, flag='caution', summary=None, metric='Renal function', ihd=None):
    mods = dict(ckd=M('specialist', notes=notes, ev=ev))
    if ihd: mods['ihd'] = ihd
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary or notes, mods=mods)
HDT = lambda rows, ev, notes='': M('summarized', [T('Haemodialysis · US label', rows)], notes, ev)
spec('albendazole', 'Albendazole', 'Not studied in renal impairment; no renal dose in the label.', ['The pharmacokinetics of albendazole in patients with impaired renal function has not been studied'], flag='monitor')
noadj('baloxavir', 'XOFLUZA', ['creatinine clearance (CrCl: 50 mL/min and above)'], rows=[('CrCl ≥50 mL/min', 'No PK difference; usual dose'), ('CrCl <50 mL/min', 'Not characterised in the label')],
 summary='No PK difference at CrCl ≥50; lower CrCl not characterised. Unlikely to be removed by dialysis.', ihd=M('insufficient_data', notes='No dialysis dose; unlikely to be removed by dialysis (highly protein bound).', ev=['Baloxavir is unlikely to be significantly removed by dialysis due to high serum protein binding']))
noadj('bedaquiline', 'SIRTURO', ['No dose adjustment is required in patients with mild or moderate renal impairment', 'Use with caution in patients with severe renal impairment'],
 rows=[('Mild or moderate impairment', 'No dose adjustment'), ('Severe impairment', 'Use with caution')], summary='No adjustment in mild–moderate impairment; caution in severe impairment.')
add('bictegravir-emtricitabine-tenofovir-alafenamide', 'BIKTARVY', promote=True, flag='caution', metric='CrCl · mL/min',
 summary='Not recommended at CrCl 15–29, or <15 if not on chronic haemodialysis. On haemodialysis (treatment-experienced), give after dialysis.',
 mods=dict(ckd=M('summarized', [T('HIV-1 · US label', [('CrCl ≥30 mL/min', 'No dose adjustment'), ('CrCl 15 to <30 mL/min', 'Not recommended'), ('CrCl <15, not on chronic haemodialysis', 'Not recommended')])], 'Check creatinine, CrCl, urine glucose and protein before and during treatment.',
   ['BIKTARVY is not recommended in patients with estimated creatinine clearance of 15 to below 30 mL/min, or below 15 mL/min who are not receiving chronic hemodialysis, or below 15 mL/min who have no antiretroviral treatment history']),
  ihd=HDT([('CrCl <15 on chronic haemodialysis (treatment-experienced)', 'Usual daily dose; on HD days give after dialysis')], ['adults with an estimated creatinine clearance below 15 mL/min who are receiving chronic hemodialysis', 'days of hemodialysis, administer the daily dose of BIKTARVY after completion of hemodialysis treatment'],
   'Not recommended below CrCl 15 without prior antiretroviral treatment.')))
noadj('cefaclor', 'Cefaclor', ['Since the half-life of cefaclor in anuria is 2.3 to 2.8 hours, dosage adjustments for patients with moderate or severe renal impairment are usually not required'],
 rows=[('Moderate or severe impairment', 'Usually no adjustment (half-life 2.3–2.8 h in anuria)')], summary='Usually no adjustment in moderate–severe impairment (half-life only 2.3–2.8 h in anuria).')
spec('chloroquine', 'Chloroquine', 'Substantially renally excreted: risk of toxicity greater in impaired renal function; no numeric renal dose.', ['is known to be substantially excreted by the kidney, and the risk of toxic reactions to this drug may be greater in patients with impaired renal function'])
add('cidofovir', 'Cidofovir injection', promote=True, flag='caution', metric='Serum creatinine, CrCl, urine protein',
 summary='Contraindicated if serum creatinine >1.5 mg/dL, CrCl ≤55 mL/min or urine protein ≥100 mg/dL. Check renal function within 48 h before each dose.',
 mods=dict(ckd=M('summarized', [T('CMV retinitis · US label', [('SCr >1.5 mg/dL, CrCl ≤55 mL/min or urine protein ≥100 mg/dL (≥2+)', 'Contraindicated'), ('Before each dose', 'Check serum creatinine and urine protein within 48 h')])], 'Nephrotoxicity is the major toxicity (boxed warning).',
   ['cidofovir injection is contraindicated in patients with a serum creatinine >1.5 mg/dL, a calculated creatinine clearance ≤55 mL/min, or a urine protein ≥100 mg/dL (equivalent to ≥2+ proteinuria)', 'RENAL IMPAIRMENT IS THE MAJOR TOXICITY OF CIDOFOVIR INJECTION']),
  ihd=M('avoid', notes='Contraindicated at CrCl ≤55 mL/min.', ev=['cidofovir injection is contraindicated in patients with a serum creatinine >1.5 mg/dL, a calculated creatinine clearance ≤55 mL/min, or a urine protein ≥100 mg/dL (equivalent to ≥2+ proteinuria)'])))
spec('dicloxacillin', 'Dicloxacillin', 'Consider reducing the total dose in renal impairment and monitor levels (neurotoxicity). Minimal removal by HD or PD.',
 ['If any impairment of renal function is suspected or known to exist, a reduction in the total dosage should be considered and blood levels monitored to avoid possible neurotoxic reactions'])
spec('erythromycin', 'Erythromycin', 'No renal dose in the label; hearing loss reported mainly in renal insufficiency or high doses. Not removed by HD or PD.',
 ['There have been isolated reports of reversible hearing loss occurring chiefly in patients with renal insufficiency and in patients receiving high doses of erythromycin'], flag='monitor',
 ihd=HDT([('Haemodialysis', 'No dialysis dose in the label; not removed by HD or PD, so no supplement')], ['Erythromycin is not removed by peritoneal dialysis or hemodialysis']))
noadj('glecaprevir-pibrentasvir', 'MAVYRET', ['HCV/HIV-1 co-infection and patients with any degree of renal impairment: Follow the dosage recommendations in the tables above'],
 rows=[('Any renal impairment, including dialysis', 'No adjustment: usual regimen')], summary='Usual regimen at any level of renal function, including dialysis; not removed by haemodialysis.',
 ihd=HDT([('Dialysis', 'Usual regimen; not significantly removed by HD')], ['Glecaprevir and pibrentasvir are not significantly removed by hemodialysis']))
noadj('nafcillin', 'Nafcillin', ['no modification of the usual nafcillin dosage is necessary in renal failure with or without hemodialysis'], summary='No dose change in renal failure, with or without haemodialysis.',
 ihd=HDT([('Haemodialysis', 'No dose change; HD does not speed clearance')], ['no modification of the usual nafcillin dosage is necessary in renal failure with or without hemodialysis', 'Hemodialysis does not accelerate the rate of clearance of nafcillin from the blood']))
noadj('oritavancin', 'KIMYRSA', ['No dosage adjustment of KIMYRSA is needed in patients with mild or moderate renal impairment', 'The pharmacokinetics of KIMYRSA in severe renal impairment have not been evaluated'],
 rows=[('Mild or moderate impairment', 'No dose adjustment'), ('Severe impairment', 'Not evaluated')], summary='No adjustment in mild–moderate impairment; severe impairment not evaluated. Not removed by haemodialysis.')
add('plazomicin', 'ZEMDRI', promote=True, flag='adjust', metric='CrCl · mL/min (Cockcroft–Gault)',
 summary='15 mg/kg every 24 h at CrCl ≥60; 10 mg/kg every 24 h at 30–59; 10 mg/kg every 48 h at 15–29; insufficient data below 15.',
 mods=dict(ckd=M('summarized', [T('Complicated UTI · US label Table 1', [('CrCl ≥90 mL/min', '15 mg/kg every 24 h'), ('CrCl 60 to <90 mL/min', '15 mg/kg every 24 h'), ('CrCl 30 to <60 mL/min', '10 mg/kg every 24 h'), ('CrCl 15 to <30 mL/min', '10 mg/kg every 48 h'), ('CrCl <15 mL/min', 'Insufficient information')])],
   'Assess CrCl before starting and daily during therapy.',
   ['Administer ZEMDRI 15 mg/kg every 24 hours by intravenous (IV) infusion over 30 minutes to patients 18 years of age or older with creatinine clearance greater than or equal to 90 mL/min',
    'Greater than or equal to 60 to less than 90 15 mg/kg Every 24 hours Greater than or equal to 30 to less than 60 10 mg/kg Every 24 hours Greater than or equal to 15 to less than 30 10 mg/kg Every 48 hours', 'Assess creatinine clearance in all patients prior to initiating therapy and daily during therapy']),
  ihd=M('insufficient_data', notes='Insufficient information to recommend a regimen at CrCl <15 mL/min, including dialysis.', ev=['There is insufficient information to recommend a dosage regimen in patients with CLcr les'])))
noadj('praziquantel', 'BILTRICIDE', ['No dosage adjustment of Biltricide is necessary in patients with renal impairment'])
spec('pretomanid', 'Pretomanid', 'Effect of renal impairment unknown; the BPaL regimen is not established in renal impairment.', ['The effect of renal impairment on the safety, effectiveness, and pharmacokinetics of pretomanid is not known'], flag='monitor')
spec('rifaximin', 'XIFAXAN', 'Not studied in renal impairment (minimal systemic absorption).', ['The pharmacokinetics of rifaximin in patients with impaired renal function has not been studied'], flag='monitor')
noadj('sofosbuvir-velpatasvir', 'EPCLUSA', ['No dosage adjustment of EPCLUSA is recommended in patients with any degree of renal impairment, including patients requiring dialysis'],
 rows=[('Any renal impairment, including dialysis', 'No dose adjustment')], summary='No adjustment at any level of renal function, including dialysis (ribavirin, if added, needs its own adjustment).',
 ihd=HDT([('Dialysis', 'No dose adjustment')], ['No dosage adjustment of EPCLUSA is recommended in patients with any degree of renal impairment, including patients requiring dialysis']))
spec('streptomycin', 'Streptomycin', 'Neurotoxicity risk sharply higher in renal impairment: give reduced doses and monitor renal function (boxed warning); no numeric table in the label.',
 ['RENAL FUNCTION SHOULD BE MONITORED CAREFULLY; PATIENTS WITH RENAL IMPAIRMENT AND/OR NITROGEN RETENTION SHOULD RECEIVE REDUCED DOSES'], flag='adjust')
spec('terbinafine', 'Terbinafine tablets', 'Not adequately studied at CrCl ≤50; clearance about 50% lower.', ['In patients with renal impairment (creatinine clearance less than or equal to 50 mL/min), the use of terbinafine tablets has not been adequately studied',
 'In patients with renal impairment (creatinine clearance less than or equal to 50 mL/min) or hepatic cirrhosis, the clearance of terbinafine is decreased by approximately 50% compared to normal volunteers'])
spec('tetracycline', 'Tetracycline', 'Accumulates in renal impairment (azotaemia, hyperphosphataemia, acidosis, hepatotoxicity) even at usual doses; no numeric renal dose. Not dialysable.',
 ['If renal impairment exists, even usual oral or parenteral doses may lead to excessive systemic accumulation of the drug and possible liver toxicity'], flag='caution')
add('tinidazole', 'Tinidazole', promote=True, flag='no_adjust', metric='CrCl · mL/min',
 summary='No adjustment, even at CrCl <22. On haemodialysis days, if dosed before HD, give an extra half dose afterwards.',
 mods=dict(ckd=M('summarized', [T('All indications · US label', [('CrCl <22 mL/min', 'No dose adjustment')])], '', ['Because the pharmacokinetics of tinidazole in patients with severe renal impairment (CrCL < 22 mL/min) are not significantly different from those in healthy subjects, no dose adjustments are necessary in these patients']),
  ihd=HDT([('Dosed the same day, before HD', 'Give an additional half dose after the end of haemodialysis')], ['If tinidazole is administered on the same day as and prior to hemodialysis, it is recommended that an additional dose of tinidazole equivalent to one-half of the recommended dose be administered after the end of the hemodialysis'])))
spec('ivermectin', 'Ivermectin', 'The US label gives no renal dose statement.', [], flag='monitor')
spec('mebendazole', 'Mebendazole', 'The US label gives no renal dose statement.', [], flag='monitor')
spec('secnidazole', 'SOLOSEC', 'The US label gives no renal dose statement.', [], flag='monitor')
