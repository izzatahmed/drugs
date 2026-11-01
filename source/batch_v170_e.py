# ---- v0.17.0 batch: medicines without a current US label, from UK SmPCs (emc) and EMA product information ----
def P_(i, brand, flag, metric, summary, ckd, ihd=None, pd=None, considerations=None):
    mods = dict(ckd=ckd)
    if ihd: mods['ihd'] = ihd
    if pd: mods['pd'] = pd
    LAB[i] = f'uk3/{i}.json'
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary, mods=mods, considerations=considerations)
S = lambda ind, rows, ev, notes='': M('summarized', [T(ind, rows)], notes, ev)
HDT = lambda rows, ev, notes='': M('summarized', [T('Haemodialysis · SmPC', rows)], notes, ev)
NOREN = 'The current SmPC gives no renal dose statement.'
for i in ('gliclazide-mr',): LAB[i] = f'uk3/{i}.json'

# -------- Diabetes, anticoagulation, anaemia --------
P_('gliclazide', 'DIAMICRON 80 mg', 'caution', 'Renal function', 'Mild–moderate renal insufficiency: same dose with careful monitoring; renal insufficiency raises hypoglycaemia risk. Not removed by dialysis.',
   S('Type 2 diabetes · UK SmPC', [('Mild to moderate renal insufficiency', 'Usual dosing regimen with careful monitoring (IR 80 mg and MR 30 mg tablets)')],
     ['Renal impairment In patients with mild to moderate renal insufficiency, the same dosing regimen can be used as in patients with normal renal function with careful patient monitoring', '2|Renal impairment In patients with mild to moderate renal insufficiency the same dosing regimen can be used as in patients with normal renal function with careful patient monitoring'],
     notes='Renal insufficiency is listed among factors that increase the risk of hypoglycaemia. The SmPC gives no dose for severe impairment.'),
   ihd=M('specialist', notes='Dialysis does not remove gliclazide (strongly protein bound); no dialysis dose is given.', ev=['Dialysis is of no benefit to patients due to the strong binding of gliclazide to proteins']))
C['gliclazide'].update(label2='uk3/gliclazide-mr.json', brand2='DIAMICRON 30 mg MR')
P_('lixisenatide', 'Suliqua (insulin glargine/lixisenatide)', 'caution', 'CrCl · mL/min', 'No adjustment in mild–moderate impairment; not recommended at CrCl <30 or ESRD (no experience).',
   S('Type 2 diabetes · EU SmPC (Suliqua)', [('Mild or moderate impairment', 'No lixisenatide dose adjustment; monitor glucose (insulin needs may fall)'), ('CrCl <30 mL/min or ESRD', 'Not recommended')],
     ['No dose adjustment is required for lixisenatide in patients with mild or moderate renal impairment', 'In patients with mild to moderate renal impairment using Suliqua, frequent glucose monitoring and dose adjustment may be necessary', 'There is no therapeutic experience in patients with severe renal impairment (creatinine clearance less than 30 ml/min) or end-stage renal disease']),
   ihd=M('avoid', notes='Not recommended in end-stage renal disease.', ev=['Suliqua is not recommended in patients with severe renal impairment and end-stage renal disease as there is no sufficient therapeutic experience with use of lixisenatide']),
   considerations='Lixisenatide alone (Lyxumia) is no longer authorised in the EU; this entry uses the combination product Suliqua.')
P_('tinzaparin', 'innohep', 'caution', 'CrCl · mL/min (Cockcroft–Gault)', 'Not recommended at CrCl <30 (dose not established); no accumulation down to CrCl 20. HD circuit anticoagulation dosing given.',
   S('VTE prophylaxis / treatment · UK SmPC', [('CrCl ≥30 mL/min', 'Usual dose (no accumulation shown down to CrCl 20)'), ('CrCl <30 mL/min', 'Not recommended (dose not established)')],
     ['If renal impairment is suspected, renal function should be assessed using a formula based on serum creatinine to estimate creatinine clearance level', 'Use in patients with a creatinine clearance level < 30 ml/minute is not recommended, as dosage in this population has not been established', 'Available evidence demonstrates no accumulation in patients with creatinine clearance levels down to 20 ml/min']),
   ihd=HDT([('Circuit anticoagulation, session ≤4 h', 'Bolus 2,000–2,500 anti-Xa IU at the start of dialysis'), ('Circuit anticoagulation, session >4 h', 'Bolus 2,500 anti-Xa IU, then 750 anti-Xa IU/hour infusion'), ('Monitoring', 'Plasma anti-Xa activity can guide the dose')],
     ['Haemodialysis and haemofiltration in adults: Duration of 4 hours or less: A bolus injection of 2,000 to 2,500 anti-Xa IU at the start of dialysis', 'Duration of more than 4 hours: A bolus injection of 2,500 anti-Xa IU at the start of dialysis/filtration, followed by 750 anti-Xa IU/hour as a continuous infusion', 'Determination of plasma anti-Xa activity can be used to monitor the tinzaparin sodium dose during haemodialysis/haemofiltration'],
     notes='These doses prevent circuit clotting; they are not VTE treatment doses for dialysis patients.'))
P_('roxadustat', 'Evrenzo', 'adjust', 'CKD anaemia · dialysis status', 'Dose by Hb response; maximum 3 mg/kg or 300 mg three times weekly (not on dialysis) or 400 mg (on dialysis). No change on starting dialysis; not removed by HD.',
   S('Anaemia of CKD · EU SmPC', [('Not on dialysis', 'Maximum 3 mg/kg or 300 mg three times per week, whichever is lower'), ('Starting dialysis on treatment', 'No specific dose adjustment')],
     ['Patients not on dialysis Do not exceed a roxadustat dose of 3 mg/kg body weight or 300 mg three times per week, whichever is lower', 'No specific dose adjustment is required for CKD patients who start dialysis while on treatment with roxadustat']),
   ihd=HDT([('On dialysis', 'Maximum 3 mg/kg or 400 mg three times per week, whichever is lower'), ('Removal', 'Not significantly removed by haemodialysis')],
     ['Patients on dialysis Do not exceed a roxadustat dose of 3 mg/kg body weight or 400 mg three times per week, whichever is lower', 'Roxadustat and its metabolites are not significantly removed by haemodialysis'],
     notes='Converting dialysis patients who are stable on an ESA is only for a valid clinical reason.'),
   considerations='Converting dialysis patients otherwise stable on an ESA should only be considered for a valid clinical reason (EU SmPC).')
P_('ferrous-fumarate', 'Fersamal 210 mg', 'monitor', 'No renal statement in the SmPC', NOREN + ' In iron overdose, HD does not remove iron but supports desferrioxamine–iron removal in acute renal failure.',
   M('specialist', notes=NOREN), ihd=M('specialist', notes='Haemodialysis does not remove iron effectively; in overdose with acute renal failure it helps remove the iron–desferrioxamine complex.', ev=['Haemodialysis does not remove iron effectively but should be considered on a supportive basis for acute renal failure as this will facilitate removal of the iron-desferrioxamine complex']))
P_('ferrous-sulfate', 'Ferrous Sulfate 200 mg', 'monitor', 'No renal statement in the SmPC', NOREN, M('specialist', notes=NOREN))

# -------- Pain, respiratory, allergy --------
P_('etoricoxib', 'ARCOXIA', 'caution', 'CrCl · mL/min', 'No adjustment at CrCl ≥30; contraindicated at CrCl <30. Not removed by HD. NSAID renal-perfusion risk.',
   S('All indications · UK SmPC', [('CrCl ≥30 mL/min', 'No dose adjustment'), ('CrCl <30 mL/min', 'Contraindicated')],
     ['Patients with renal impairment No dosage adjustment is necessary for patients with creatinine clearance ≥ 30 mL/min', 'The use of etoricoxib in patients with creatinine clearance < 30 mL/min is contra-indicated'],
     notes='May reduce renal blood flow when renal perfusion is compromised; greatest risk with significant renal impairment, uncompensated heart failure or cirrhosis.'),
   ihd=M('avoid', notes='Contraindicated at CrCl <30 mL/min; not removed by haemodialysis.', ev=['The use of etoricoxib in patients with creatinine clearance < 30 mL/min is contra-indicated', 'Etoricoxib is not dialysable by haemodialysis; it is not known whether etoricoxib is dialysable by peritoneal dialysis']))
P_('glycopyrronium-inhaled', 'Seebri Breezhaler', 'caution', 'eGFR · mL/min/1.73 m²', 'Mild–moderate: usual dose. Severe impairment or ESRD on dialysis: use only if benefit outweighs risk (exposure up to 2.2-fold).',
   S('COPD · UK SmPC', [('Mild to moderate impairment', 'Usual dose'), ('Severe impairment or ESRD on dialysis', 'Only if the expected benefit outweighs the potential risk')],
     ['Seebri Breezhaler can be used at the recommended dose in patients with mild to moderate renal impairment', 'In patients with severe renal impairment or end‑stage renal disease requiring dialysis Seebri Breezhaler should be used only if the expected benefit outweighs the potential risk since the systemic exposure to glycopyrronium may be increased in this population']),
   ihd=M('specialist', notes='ESRD on dialysis: only if benefit outweighs risk.', ev=['In patients with severe renal impairment or end‑stage renal disease requiring dialysis Seebri Breezhaler should be used only if the expected benefit outweighs the potential risk since the systemic exposure to glycopyrronium may be increased in this population']))
P_('fluticasone-nasal', 'AVAMYS', 'no_adjust', 'No renal dose adjustment (UK SmPC)', 'No dose adjustment in renal impairment.',
   S('Allergic rhinitis · UK SmPC', [('Renal impairment', 'No dose adjustment')], ['Renal Impairment No dose adjustment is required in this population']))
P_('pseudoephedrine', 'Sudafed Decongestant Tablets', 'caution', 'Renal function', 'Contraindicated in severe acute or chronic kidney disease/renal failure; caution in moderate impairment.',
   S('Nasal congestion · UK SmPC', [('Moderate renal impairment', 'Use with caution'), ('Severe acute or chronic kidney disease / renal failure', 'Contraindicated')],
     ['Caution should be exercised when administering Sudafed Decongestant Tablets to patients with moderate renal impairment', 'Cardiovascular disease including hypertension Diabetes mellitus Phaeochromocytoma Hyperthyroidism Closed angle glaucoma Severe acute or chronic kidney disease/renal failure']),
   ihd=M('avoid', notes='Contraindicated in renal failure. In overdose, dialysis can speed elimination.', ev=['If desired, the elimination of pseudoephedrine can be accelerated by acid diuresis or by dialysis']))
P_('guaifenesin', 'BENYLIN Chesty Coughs', 'caution', 'Renal function', 'Normal adult dose in mild–moderate dysfunction; caution in severe renal impairment.',
   S('Productive cough · UK SmPC', [('Mild to moderate dysfunction', 'Normal adult dose'), ('Severe renal impairment', 'Use with caution')],
     ['Experience with the use of this product suggests that normal adult dosage is appropriate for mild to moderate dysfunction', 'Caution should be exercised in severe hepatic and severe renal impairment']))
P_('dextromethorphan', 'BENYLIN DRY COUGHS 7.5 mg/5 ml', 'monitor', 'Renal function', 'Not studied in renal dysfunction; parent drug and dextrorphan are renally excreted.',
   M('specialist', notes='No renal dose; renal impairment has not been studied.', ev=['There have been no specific studies of this product in renal or hepatic dysfunction', 'Dextromethorphan is primarily excreted via the kidney as unchanged parent drug and its active metabolite, dextrorphan']))
P_('xylometazoline-nasal', 'Otrivine 0.1% Nasal Spray', 'monitor', 'No renal statement in the SmPC', NOREN, M('specialist', notes=NOREN))

# -------- Gastrointestinal & laxatives --------
P_('mebeverine', 'Colofac 135 mg', 'no_adjust', 'No renal dose adjustment (UK SmPC)', 'No dosage adjustment deemed necessary in renal impairment.',
   S('IBS · UK SmPC', [('Renal impairment', 'No dosage adjustment')], ['No dosage adjustment is deemed necessary in elderly, renal and/or hepatic impaired patients', 'No posology studies in elderly, renal and/or hepatic impaired patients have been performed']))
P_('sodium-picosulfate', 'Dulcolax Adult Pico Liquid', 'caution', 'Volume status', 'Stop if fluid loss could be harmful (e.g. renal insufficiency); restart only under supervision.',
   M('specialist', notes='No renal dose.', ev=['In patients suffering from fluid loss where dehydration may be harmful (e.g. renal insufficiency, elderly patients) sodium picosulfate should be discontinued and only be restarted under medical supervision']))
P_('senna', 'Senokot 7.5 mg', 'caution', 'Volume and electrolytes', 'Possible electrolyte imbalance in kidney disorders; stop if dehydration could be harmful.',
   M('specialist', notes='No renal dose.', ev=['Patients with kidney disorders should be aware of possible electrolyte imbalance']))
P_('psyllium', 'Fybogel', 'caution', 'Potassium content', 'Contains potassium: consider in reduced kidney function or potassium-restricted diet.',
   M('specialist', notes='No renal dose; note the potassium content per sachet in the SmPC.', ev=['To be taken into consideration by patients with reduced kidney function or patients on a controlled potassium diet']))
P_('docusate', 'Dioctyl 100 mg', 'monitor', 'No renal statement in the SmPC', NOREN, M('specialist', notes=NOREN))
P_('sodium-alginate-combinations', 'Gaviscon Advance', 'caution', 'Sodium and potassium content', 'Caution with salt restriction in renal insufficiency; contains potassium (1.0 mmol/5 mL).',
   M('specialist', notes='No renal dose.', ev=['Renal Insufficiency: Caution if highly restricted salt diet is necessary', 'This medicine contains 1.0 mmol (39.06 mg) potassium per 5 ml . To be taken into consideration by patients with reduced kidney function or patients on a controlled potassium diet']))
P_('oral-rehydration-salts', 'Dioralyte', 'caution', 'Renal function', 'With normal kidneys over-hydration by mouth is unlikely; take care in severe renal failure.',
   M('specialist', notes='No renal dose.', ev=['Where the kidneys are functioning normally, it is difficult to over-hydrate by mouth and where there is doubt about the dosage, more rather than less should be taken', 'This is particularly important in the very young and in cases of severe hepatic of renal failure']))
P_('calcium-polystyrene-sulfonate', 'Calcium Resonium', 'monitor', 'Serum electrolytes', 'Used for hyperkalaemia including dialysis patients; dose by serum electrolytes. Hypercalcaemia reported in well-dialysed patients.',
   M('specialist', notes='Dosing is guided by regular serum electrolytes rather than renal function.', ev=['It is also used to treat hyperkalaemia in patients requiring dialysis and in patients on regular haemodialysis or on prolonged peritoneal dialysis', 'Hypercalcaemia has been reported in well dialysed patients receiving calcium resin, and occasionally in patients with chronic renal failure']),
   ihd=M('specialist', notes='Indicated in haemodialysis and PD patients; watch for hypercalcaemia.', ev=['Hypercalcaemia has been reported in well dialysed patients receiving calcium resin, and occasionally in patients with chronic renal failure']))

# -------- Topicals --------
for i, brand in [('hydrocortisone-topical', 'Dermacort Hydrocortisone Cream'), ('miconazole-topical', 'Daktarin 2% Cream'), ('clotrimazole-topical', 'Canesten 1% Cream')]:
    P_(i, brand, 'monitor', 'No renal statement in the SmPC', NOREN, M('specialist', notes=NOREN))
