# ---- Batch D1: diabetes & endocrine catalog entries ----
INS = 'Monitor blood glucose more often and reduce the dose as needed (higher hypoglycaemia risk).'
def insulin(i, brand, ev, ihd=None):
    mods = dict(ckd=M('summarized', [T('Renal impairment · US label', [('Any CrCl / eGFR', INS)])], '', ev))
    if ihd: mods['ihd'] = ihd
    add(i, brand, promote=True, flag='monitor', metric='Glucose monitoring (no fixed renal dose)', summary='No fixed renal dose; requirements may fall — monitor glucose more often and adjust.', mods=mods)
insulin('insulin-aspart', 'Insulin aspart', ['Patients with renal impairment may be at increased risk of hypoglycemia and may require more frequent Insulin Aspart dose adjustment and more frequent blood glucose monitoring'])
insulin('insulin-glulisine', 'APIDRA', ['Patients with renal impairment may be at increased risk of hypoglycemia and may require more frequent APIDRA dose adjustment and more frequent blood glucose monitoring'])
insulin('insulin-lispro', 'HUMALOG', ['Patients with renal impairment may be at increased risk of hypoglycemia and may require more frequent HUMALOG dose adjustment and more frequent blood glucose monitoring'])
insulin('insulin-nph', 'HUMULIN N', ['Patients with renal impairment are at increased risk of hypoglycemia and may require more frequent HUMULIN N dose adjustment and more frequent blood glucose monitoring'])
insulin('insulin-regular', 'MYXREDLIN (IV regular insulin)', ['Patients with renal impairment are at increased risk of hypoglycemia and may require more frequent MYXREDLIN dose adjustment and more frequent blood glucose monitoring'])
insulin('insulin-glargine', 'BASAGLAR', ['Frequent glucose monitoring and dose adjustment may be necessary for BASAGLAR in patients with renal impairment'])
insulin('insulin-degludec', 'Insulin degludec', ['in patients with renal impairment or hepatic impairment or hypoglycemia unawareness',
   'Total (AUC IDeg,0-120h,SD ) and peak exposure of Insulin Degludec were on average about 10-25% and 13-27% higher, respectively in subjects with mild to severe renal impairment except subjects with ESRD who showed similar exposure as compared to subjects with normal renal function'])
insulin('insulin-detemir', 'LEVEMIR', ['No difference was observed in the pharmacokinetics of LEVEMIR between non-diabetic patients with kidney impairment and healthy volunteers', 'in patients with renal impairment or hepatic impairment or hypoglycemia unawareness'],
   ihd=M('summarized', [T('Haemodialysis · US label', [('Haemodialysis-dependent', 'No PK difference from healthy subjects; monitor glucose and adjust as needed')])], '',
     ['administered to healthy subjects and those with varying degrees of renal impairment (mild, moderate, severe, and hemodialysis-dependent)', 'In this study, there were no differences in the pharmacokinetics of LEVEMIR between healthy subjects and those with renal impairment']))
add('acarbose', 'Acarbose', promote=True, flag='caution', metric='Serum creatinine / CrCl',
 summary='Not recommended when serum creatinine >2.0 mg/dL (no long-term trials); exposure ~6-fold at CrCl <25.',
 mods=dict(ckd=M('summarized', [T('Type 2 diabetes · US label', [('Serum creatinine ≤2.0 mg/dL', 'Usual dose'), ('Serum creatinine >2.0 mg/dL', 'Not recommended (no long-term trials)')])], 'At CrCl <25 mL/min/1.73 m², peak levels are about 5-fold and AUC 6-fold higher.',
   ['Long-term clinical trials in diabetic patients with significant renal dysfunction (serum creatinine > 2.0 mg/dL) have not been conducted', 'Therefore, treatment of these patients with Acarbose Tablets is not recommended',
    'Patients with severe renal impairment (Clcr < 25 mL/min/1.73m 2 ) attained about 5 times higher peak plasma concentrations of acarbose and 6 times larger AUCs than volunteers with normal renal function']),
  ihd=M('avoid', notes='Not recommended in significant renal dysfunction.', ev=['Therefore, treatment of these patients with Acarbose Tablets is not recommended'])))
add('miglitol', 'Miglitol', promote=True, flag='caution', metric='Serum creatinine / CrCl',
 summary='Not studied long term when serum creatinine >2.0 mg/dL; levels more than double at CrCl <25.',
 mods=dict(ckd=M('summarized', [T('Type 2 diabetes · US label', [('Serum creatinine >2.0 mg/dL', 'No long-term trials; little safety information at CrCl <25'), ('CrCl <25 mL/min', 'Levels more than double on 25 mg three times daily')])], '',
   ['trials in diabetic patients with significant renal dysfunction (serum creatinine >2.0 mg/dL) have not been conducted', 'Little information is available on the safety of miglitol in patients with creatinine clearance <25 mL/min',
    'Patients with creatinine clearance <25 mL/min taking 25 mg 3 times daily, exhibited a greater than two-fold increase in miglitol plasma levels as compared to subjects with creatinine clearance >60 mL/min'])))
add('glibenclamide-glyburide', 'Glyburide', promote=True, flag='caution', metric='Renal function',
 summary='Renal insufficiency raises glyburide levels and the risk of serious hypoglycaemia; the US label gives no renal dose.',
 mods=dict(ckd=M('specialist', notes='Renal insufficiency can raise glyburide levels and the risk of serious hypoglycaemia. Assess renal function when choosing the dose; no numeric renal dose in the label.',
   ev=['Renal or hepatic insufficiency may cause elevated drug levels of glyburide and the latter may also diminish gluconeogenic capacity, both of which increase the risk of serious hypoglycemic reactions', 'Dose selection should include assessment of renal function'])))
add('nateglinide', 'Nateglinide', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)',
 summary='No dose adjustment in mild to severe renal impairment. On dialysis, exposure and protein binding fall.',
 mods=dict(ckd=M('summarized', [T('Type 2 diabetes · US label', [('Mild to severe impairment', 'No dose adjustment')])], '', ['No dosage adjustment is recommended in patients with mild to severe renal impairment']),
  ihd=M('specialist', notes='On dialysis, Cmax fell 49% (not significant) and protein binding was reduced; no dialysis dose is given.',
   ev=['Patients with type 2 diabetes and renal failure on dialysis exhibited reduced overall drug exposure (C max decreased by 49%; not statistically significant)', 'However, hemodialysis patients also experienced reductions in plasma protein binding compared to the matched healthy volunteers'])))
add('octreotide', 'SANDOSTATIN', promote=True, flag='monitor', metric='CrCl · mL/min',
 summary='Half-life 2.4–3.1 h in renal impairment not on dialysis; on dialysis clearance halves — adjust the maintenance dose.',
 mods=dict(ckd=M('summarized', [T('Not on dialysis · US label', [('CrCl 40–60 mL/min', 'Half-life 2.4 h'), ('CrCl 10–39 mL/min', 'Half-life 3.0 h'), ('CrCl <10 mL/min (not on dialysis)', 'Half-life 3.1 h')])], 'The label gives no dose change for patients not on dialysis.',
   ['In patients with mild renal impairment (CL CR 40 to 60 mL/min), octreotide t 1/2 was 2.4 hours and total body clearance was 8.8 L/hr, in moderate impairment (CL CR 10 to 39 mL/min) t 1/2 was 3.0 hours and total body clearance 7.3 L/hr',
    'In patients with severe renal impairment not requiring dialysis (CL CR < 10 mL/min), octreotide t 1/2 was 3.1 hours and total body clearance was 7.6 L/hr']),
  ihd=M('summarized', [T('Dialysis · US label', [('Severe renal failure on dialysis', 'Half-life may increase: adjust the maintenance dose (clearance about halved)')])], '',
   ['In patients with severe renal failure requiring dialysis, the half-life of Sandostatin may be increased, necessitating adjustment of the maintenance dosage', 'In patients with severe renal failure requiring dialysis, total body clearance was reduced to about half that found in healthy subjects (from approximately 10 L/hr to 4.5 L/hr)'])))
add('pamidronate', 'Pamidronate disodium', promote=True, flag='caution', metric='CrCl · mL/min; serum creatinine before each dose',
 summary='No change if CrCl >30. Not recommended in severe impairment for bone metastases. Check creatinine before each dose; withhold if renal function worsens.',
 mods=dict(ckd=M('summarized', [T('All indications · US label', [('CrCl >30 mL/min', 'No dose change'), ('Severe renal impairment (bone metastases)', 'Not recommended'), ('Renal deterioration during treatment', 'Withhold')])],
   'Check serum creatinine before each dose. Infusions longer than 2 hours may reduce renal toxicity in pre-existing impairment.',
   ['No changes in pamidronate disodium dosing regimen are recommended for patients with mild to moderate renal impairment (creatinine clearance > 30 mL/min)', 'In patients with bone metastases with severe renal impairment, use of pamidronate disodium is not recommended',
    'Treatment should be withheld for renal deterioration', 'Longer infusions (i.e., greater than 2 hours) may reduce the risk for renal toxicity, particularly in patients with preexisting renal impairment'])))
add('zoledronic-acid', 'Zoledronic acid injection 4 mg vial (oncology)', promote=True, flag='adjust', metric='CrCl · mL/min (Cockcroft–Gault)',
 summary='Oncology 4 mg: reduce to 3.5/3.3/3.0 mg at CrCl 50–60/40–49/30–39; not recommended in severe impairment. Reclast 5 mg: contraindicated below CrCl 35.',
 mods=dict(ckd=M('summarized', [
   T('Myeloma / bone metastases, 4 mg vial · US label', [('CrCl >60 mL/min', '4 mg'), ('CrCl 50–60 mL/min', '3.5 mg'), ('CrCl 40–49 mL/min', '3.3 mg'), ('CrCl 30–39 mL/min', '3 mg'), ('Severe renal impairment', 'Not recommended')]),
   T('Osteoporosis / Paget disease, Reclast 5 mg · US label', [('CrCl ≥35 mL/min', 'No dose adjustment'), ('CrCl <35 mL/min or acute renal impairment', 'Contraindicated')])],
   'Measure serum creatinine before each oncology dose and withhold for renal deterioration.',
   ['Baseline Creatinine Clearance (mL/min) Zoledronic Acid Injection Recommended Dose* greater than 60 50 to 60 40 to 49 30 to 39 4 mg 3.5 mg 3.3 mg 3 mg', 'Treatment in patients with severe renal impairment is not recommended',
    'During treatment, serum creatinine should be measured before each zoledronic acid dose and treatment should be withheld for renal deterioration',
    '2|Reclast is contraindicated in patients with creatinine clearance less than 35 mL/min and in those with evidence of acute renal impairment', '2|Therefore, no dose adjustment is required in patients with creatinine clearance greater than or equal to 35 mL/min']),
  ihd=M('avoid', notes='Not recommended in severe renal impairment (oncology); Reclast contraindicated below CrCl 35.', ev=['Treatment in patients with severe renal impairment is not recommended', '2|Reclast is contraindicated in patients with creatinine clearance less than 35 mL/min and in those with evidence of acute renal impairment'])))
C['zoledronic-acid'].update(label='alt/zoledronic-acid-vial.json', label2='alt/zoledronic-acid-reclast.json', brand2='RECLAST')
add('risedronate', 'Risedronate sodium', promote=True, flag='caution', metric='CrCl · mL/min',
 summary='Not recommended at CrCl <30 (no clinical experience).',
 mods=dict(ckd=M('summarized', [T('Osteoporosis · US label', [('CrCl ≥30 mL/min', 'Usual dose'), ('CrCl <30 mL/min', 'Not recommended (lack of clinical experience)')])], '', ['Risedronate Sodium is not recommended for use in patients with severe renal impairment (creatinine clearance less than 30 mL/min) because of lack of clinical experience']),
  ihd=M('avoid', notes='Not recommended at CrCl <30 mL/min.', ev=['Risedronate Sodium is not recommended for use in patients with severe renal impairment (creatinine clearance less than 30 mL/min) because of lack of clinical experience'])))
add('teriparatide', 'FORTEO', promote=True, flag='no_adjust', metric='CrCl · mL/min',
 summary='No PK change at CrCl 30–72; at CrCl <30 exposure rose 73%. No renal dose adjustment is given.',
 mods=dict(ckd=M('summarized', [T('Osteoporosis · US label', [('CrCl 30–72 mL/min', 'No PK difference; usual dose'), ('CrCl <30 mL/min', 'AUC +73%, half-life +77%; no dose change stated')])], 'Effect on CKD metabolic bone disease is unknown.',
   ['No pharmacokinetic differences were identified in 11 patients with creatinine clearance (CrCl) 30 to 72 mL/minute', 'In 5 patients with severe renal impairment (CrCl<30 mL/minute), the AUC and T 1/2 of teriparatide were increased by 73% and 77%, respectively',
    'It is unknown whether FORTEO alters the underlying metabolic bone disease seen in chronic renal impairment'])))
add('romosozumab', 'EVENITY', promote=True, flag='caution', metric='eGFR · mL/min/1.73 m²',
 summary='Higher hypocalcaemia risk in severe impairment or dialysis: supplement calcium and vitamin D and monitor calcium.',
 mods=dict(ckd=M('summarized', [T('Osteoporosis · US label', [('eGFR 15–29 or on dialysis', 'Higher risk of hypocalcaemia: monitor calcium; give calcium and vitamin D')])], '',
   ['Monitor serum calcium and adequately supplement patients who have severe renal impairment or are receiving dialysis with calcium and vitamin D']),
  ihd=M('summarized', [T('Dialysis · US label', [('Haemodialysis / dialysis', 'Higher risk of hypocalcaemia: monitor calcium; give calcium and vitamin D')])], '',
   ['Monitor serum calcium and adequately supplement patients who have severe renal impairment or are receiving dialysis with calcium and vitamin D'])))
NOREN = 'The current US label gives no renal dose statement.'
for i, brand in [('glucagon', 'GVOKE'), ('calcitonin', 'Calcitonin salmon nasal'), ('methimazole', 'Methimazole'), ('propylthiouracil', 'Propylthiouracil'), ('prednisone', 'Prednisone')]:
    add(i, brand, promote=True, flag='monitor', metric='No renal statement in the US label', summary=NOREN, mods=dict(ckd=M('specialist', notes=NOREN)))
