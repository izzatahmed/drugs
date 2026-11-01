# ---- v0.18.0 batch: remaining medicines from other official labels (manufacturer label, NZ Medsafe, Dutch MEB) and a US label ----
def P_(i, brand, flag, metric, summary, ckd, ihd=None, pd=None, considerations=None, folder='uk3', note=None):
    mods = dict(ckd=ckd)
    if ihd: mods['ihd'] = ihd
    if pd: mods['pd'] = pd
    LAB[i] = f'{folder}/{i}.json'
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary, mods=mods, considerations=considerations)
    if note: C[i]['sourceNote'] = note
S = lambda ind, rows, ev, notes='': M('summarized', [T(ind, rows)], notes, ev)
JO = ' Check the JFDA-approved leaflet for products marketed in Jordan.'

P_('cefoperazone-sulbactam', 'SULPERAZON', 'adjust', 'CrCl · mL/min', 'Sulbactam limits: CrCl 15–30 → max 1 g sulbactam every 12 h; CrCl <15 → max 500 mg every 12 h. Give after HD.',
   S('All indications · Pfizer label', [('CrCl 15–30 mL/min', 'Maximum 1 g sulbactam every 12 h (2 g/day); extra cefoperazone separately if needed in severe infection'), ('CrCl <15 mL/min', 'Maximum 500 mg sulbactam every 12 h (1 g/day)')],
     ['Dosage regimens of SULPERAZON should be adjusted in patients with marked decrease in renal function (creatinine clearance of less than 30 mL/min) to compensate for the reduced clearance of sulbactam', 'Patients with creatinine clearances between 15 and 30 mL/min should receive a maximum of 1 g of sulbactam administered every 12 hours (maximum daily dosage of 2 g sulbactam), while patients with creatinine clearances of less than 15 mL/min should receive a maximum of 500 mg of sulbactam every 12 hours (maximum daily dosage of 1 g of sulbactam)']),
   ihd=M('summarized', [T('Haemodialysis · Pfizer label', [('Haemodialysis', 'Schedule the dose after dialysis (sulbactam is removed by HD); CrCl <15 limits apply')])], '', ['The pharmacokinetic profile of sulbactam is significantly altered by haemodialysis', 'Thus, dosing should be scheduled to follow a dialysis period']),
   note='Not marketed in the US, UK or EU; renal dosing from the Pfizer SULPERAZON product label (Hong Kong, January 2020).' + JO)
P_('roxithromycin', 'Arrow-Roxithromycin', 'no_adjust', 'No renal dose adjustment (NZ data sheet)', 'Usual dose in renal impairment; no reduction needed for the normally short course. Half-life ≈18 h in renal insufficiency.',
   S('All indications · NZ data sheet', [('Impaired renal function, including renal failure', '300 mg daily (one 300 mg tablet daily, or 150 mg twice daily); no reduction for a normal short course')],
     ['Impaired renal function Roxithromycin 300 mg tablets: one tablet daily', 'In the elderly and those with renal failure, dosage reduction is not required for the normally short course of treatment']),
   note='Not marketed in the US or UK; dosing from the New Zealand Data Sheet (Medsafe, revised 3 November 2025).' + JO)
P_('paracetamol', 'Paracetalgin 1000 mg', 'adjust', 'CrCl · mL/min', 'Oral: CrCl 10–50 → at least 6 h between doses; CrCl <10 → at least 8 h. Use with caution in renal insufficiency.',
   S('Oral paracetamol · Dutch SmPC', [('CrCl 10–50 mL/min', 'Minimum interval 6 hours'), ('CrCl <10 mL/min', 'Minimum interval 8 hours; use under medical supervision')],
     ['Where creatinine clearance is between 10-50 ml/min, the minimum interval between administrations should be 6 hours', 'When creatinine clearance is lower than 10 ml/min, the minimum interval between two administrations should be 8 hours', 'Paracetamol should be used with caution in the presence of renal insufficiency and increased interval between doses is recommended in cases of severe renal insufficiency']),
   note='US OTC labels and the UK SmPCs reviewed give no renal dosing interval; intervals from an EU national SmPC (Dutch Medicines Evaluation Board, decentralised procedure DE/H/6508, 25 November 2024).' + JO)
P_('diphenoxylate-atropine', 'Diphenoxylate HCl and atropine sulfate', 'caution', 'Hepatorenal disease', 'Use with extreme caution in advanced hepatorenal disease (risk of hepatic coma).',
   M('specialist', notes='No renal dose in the label.', ev=['Diphenoxylate hydrochloride and atropine sulfate tablets should be used with extreme caution in patients with advanced hepatorenal disease and in all patients with abnormal liver function since hepatic coma may be precipitated']), folder='us3')
