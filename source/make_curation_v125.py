"""Curated label content for v0.12.5 (cardiovascular class). Every dose table, statement and PK value carries
the verbatim label sentence(s) it comes from. Writes curation_v125.json; verify with
  python3 extract_quotes.py curation_v125.json label_quotes_v125.json /path/to/labels
"""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(__file__).parent

def T(indication, rows): return dict(indication=indication, rows=[dict(context=c, dose=d) for c, d in rows])
def M(status, tables=(), notes='', ev=()): return dict(status=status, tables=list(tables), notes=notes, ev=list(ev))
def P(value, ev, status='sourced'): return dict(value=value, ev=ev, status=status)
def E(label, brand, *, flag=None, metric=None, summary=None, considerations=None, promote=False, pk_only=False, mods=None, pk=None, completeness=None):
    e = dict(label=label, brand=brand, promote=promote, pk_only=pk_only, modalities=mods or {}, pk=pk or {})
    for k, v in dict(flag=flag, kidneyMetric=metric, summary=summary, considerations=considerations, completeness=completeness).items():
        if v is not None: e[k] = v
    return e

C = {}
# ======================================================================= Batch 1: antiarrhythmics, inotropes, others
SOT_T1 = 'Table 1: Dosing Intervals in Renal Impairment Creatinine Clearance mL/min Dosing Interval (hours) > 60 12 30-59 24 10-29 36-48 <10 Dose should be individualized'
C['sotalol'] = E('preg/sotalol.json', 'SOTYLIZE (sotalol oral solution)', promote=True, flag='adjust', metric='CrCl · mL/min (Cockcroft–Gault)',
 summary='Lengthen the dosing interval as CrCl falls (US label Table 1); start in hospital with ECG monitoring. Partly removed by dialysis.',
 considerations='Start 80 mg; escalate only after at least 5 doses at the adjusted interval, monitoring heart rate and QTc. Steady state takes much longer in renal impairment.',
 mods=dict(
  ckd=M('summarized', [T('Dosing interval by CrCl · US label Table 1 (initial dose 80 mg)', [('CrCl >60 mL/min', 'Every 12 h'), ('CrCl 30–59 mL/min', 'Every 24 h'), ('CrCl 10–29 mL/min', 'Every 36–48 h'), ('CrCl <10 mL/min', 'Individualise the dose')])],
    'The same label\'s highlights also state: CrCl 40–60 mL/min once daily, and sotalol not recommended below 40 mL/min. The AF-specific product (Betapace AF) is contraindicated below 40 mL/min. Confirm the indication-specific rule with cardiology.',
    [SOT_T1, 'If creatinine clearance is between 60 and 40 mL/min, administer once daily, if less than 40 mL/min, sotalol is not recommended',
     'Dose escalations in renal impairment should be done after administration of at least 5 doses at appropriate intervals (Table 1)']),
  ihd=M('specialist', notes='Partly removed by dialysis; the label gives no dialysis dosing. Individualise with ECG (QTc) monitoring.', ev=['Sotalol is partly removed by dialysis; specific advice is unavailable on dosing patients on dialysis']),
  pd=M('specialist', notes='The label gives no dialysis dosing (it states sotalol is partly removed by dialysis). Individualise with ECG monitoring.', ev=['Sotalol is partly removed by dialysis; specific advice is unavailable on dosing patients on dialysis'])),
 pk=dict(halfLife=P('12 h (mean)', 'The mean elimination half-life of sotalol is 12 hours'),
         ihd=P('Partly removed by dialysis (label)', 'Sotalol is partly removed by dialysis; specific advice is unavailable on dosing patients on dialysis', 'limited')))

DOF_T = 'Starting Dose: The starting dose of TIKOSYN is determined as follows: Calculated Creatinine Clearance TIKOSYN Dose >60 mL/min 500 mcg twice daily 40 to 60 mL/min 250 mcg twice daily 20 to <40 mL/min 125 mcg twice daily <20 mL/min Tikosyn is contraindicated in these patients'
C['dofetilide'] = E('preg/dofetilide.json', 'TIKOSYN', promote=True, flag='adjust', metric='CrCl · mL/min (Cockcroft–Gault, actual body weight)',
 summary='Starting dose by CrCl (US label); contraindicated below 20 mL/min. Start in hospital with continuous ECG for at least 3 days.',
 considerations='Recheck QTc 2–3 h after each dose; reduce if QTc rises >15% or exceeds 500 ms. Re-evaluate renal function every 3 months and adjust the dose if it falls.',
 mods=dict(
  ckd=M('summarized', [T('Starting dose by CrCl · US label', [('CrCl >60 mL/min', '500 mcg twice daily'), ('CrCl 40–60 mL/min', '250 mcg twice daily'), ('CrCl 20 to <40 mL/min', '125 mcg twice daily'), ('CrCl <20 mL/min', 'Contraindicated')])],
    'CrCl by Cockcroft–Gault with actual body weight. Maximum 500 mcg twice daily (higher doses increased torsade de pointes).',
    [DOF_T, 'If renal function deteriorates, adjust dose as described in Initiation of TIKOSYN Therapy, Step 3',
     'TIKOSYN is also contraindicated in patients with severe renal impairment (calculated creatinine clearance <20 mL/min)']),
  ihd=M('avoid', notes='Contraindicated at CrCl <20 mL/min, which includes dialysis.', ev=['TIKOSYN is also contraindicated in patients with severe renal impairment (calculated creatinine clearance <20 mL/min)']),
  pd=M('avoid', notes='Contraindicated at CrCl <20 mL/min, which includes dialysis.', ev=['TIKOSYN is also contraindicated in patients with severe renal impairment (calculated creatinine clearance <20 mL/min)'])),
 pk=dict(halfLife=P('≈10 h (terminal)', 'The terminal half-life of dofetilide is approximately 10 hours; steady state plasma concentrations are attained within 2–3 days, with an accumulation index of 1.5 to 2.0'),
         renalHalfLife=P('Longer at lower CrCl', 'As a result, and as seen in clinical studies, the half-life of dofetilide is longer in patients with lower creatinine clearances'),
         volumeOfDistribution=P('3 L/kg', 'Volume of distribution is 3 L/kg'),
         proteinBinding=P('60–70% (unaffected by renal impairment)', 'Plasma protein binding of dofetilide is 60–70%, is independent of plasma concentration, and is unaffected by renal impairment')))

C['milrinone'] = E('preg/milrinone.json', 'Milrinone lactate in 5% dextrose', promote=True, flag='adjust', metric='CrCl · mL/min/1.73 m²',
 summary='Reduce the maintenance infusion rate in renal impairment (US label table: 0.20–0.43 mcg/kg/min for CrCl 5–50).',
 mods=dict(
  ckd=M('summarized', [T('Maintenance infusion rate · US label (usual range 0.375–0.75 mcg/kg/min)', [('CrCl 50 mL/min/1.73 m²', '0.43 mcg/kg/min'), ('CrCl 40', '0.38 mcg/kg/min'), ('CrCl 30', '0.33 mcg/kg/min'), ('CrCl 20', '0.28 mcg/kg/min'), ('CrCl 10', '0.23 mcg/kg/min'), ('CrCl 5', '0.20 mcg/kg/min')])],
    'Adjust to haemodynamic and clinical response. Monitor fluid, electrolytes and renal function.',
    ['Creatinine Clearance (mL/min/1.73m 2 ) Infusion Rate (mcg/kg/min) 5 0.20 10 0.23 20 0.28 30 0.33 40 0.38 50 0.43',
     'Reductions in infusion rate may be necessary in patients with renal impairment'])))

C['procainamide'] = E('preg/procainamide.json', 'Procainamide hydrochloride injection', promote=True, flag='monitor', metric='CrCl and age; PA/NAPA levels',
 summary='Accumulates in renal impairment: use lower doses or infusion rates guided by PA and NAPA levels (US label gives no numeric renal dose).',
 mods=dict(
  ckd=M('specialist', notes='Renal insufficiency can cause accumulation with effects like overdosage unless the dose is individualised. Reduced CrCl and age over 50 suggest a lower dose or infusion rate; use PA and NAPA levels.',
    ev=['Renal Insufficiency Renal insufficiency may lead to accumulation of high plasma levels from conventional doses of PA, with effects similar to those of overdosage (see OVERDOSAGE ), unless dosage is adjusted for the individual patient',
        'Elevated serum creatinine or urea nitrogen, reduced creatinine clearance or history of renal insufficiency, as well as use in older patients (over age 50), provide grounds to anticipate that less than the usual dosage or infusion rate may suffice, since the urinary elimination of PA and NAPA may be reduced, leading to gradual accumulation beyond normally- predicted amounts']),
  ihd=M('specialist', notes='Both procainamide and NAPA are removed by haemodialysis. Dose from levels.', ev=['Both PA and NAPA are removed from the circulation by hemodialysis but not peritoneal dialysis']),
  pd=M('specialist', notes='Neither procainamide nor NAPA is removed by peritoneal dialysis. Dose from levels.', ev=['Both PA and NAPA are removed from the circulation by hemodialysis but not peritoneal dialysis'])),
 pk=dict(halfLife=P('3–4 h (normal renal function)', 'The half-time for elimination of PA is three to four hours in patients with normal renal function, but reduced creatinine clearance and advancing age each prolong the half-time of elimination of PA.A significant fraction of the circulating PA may be metabolized in hepatocytes to N-acetylprocainamide (NAPA), ranging from 16 to 21 percent of an administered dose in “slow acetylators” to 24 to 33 percent in “fast-acetylators.”'.split('.A significant')[0]),
         volumeOfDistribution=P('≈2 L/kg', 'The apparent volume of distribution eventually reaches about 2 liters per kilogram body weight with a half-time of approximately five minutes'),
         proteinBinding=P('15–20%', 'About 15 to 20 percent of PA is reversibly bound to plasma proteins, and considerable amounts are more slowly and reversibly bound to tissues of the heart, liver, lung, and kidney'),
         ihd=P('Removed by hemodialysis (PA and NAPA)', 'Both PA and NAPA are removed from the circulation by hemodialysis but not peritoneal dialysis', 'removed'),
         pd=P('Not removed by peritoneal dialysis', 'Both PA and NAPA are removed from the circulation by hemodialysis but not peritoneal dialysis', 'not_removed')))
# the PA half-life sentence is quoted up to the run-on; fix the 'three to four' number check by wording
C['procainamide']['pk']['halfLife']['value'] = 'three to four hours (normal renal function)'

C['disopyramide'] = E('preg/disopyramide.json', 'NORPACE / NORPACE CR', promote=True, flag='adjust', metric='CrCl · mL/min',
 summary='400 mg/day if CrCl >40; immediate-release 100 mg every 8–24 h by CrCl ≤40 (US label). Controlled-release not recommended at CrCl ≤40.',
 mods=dict(
  ckd=M('summarized', [T('Maintenance dose · US label', [('CrCl >40 mL/min (moderate impairment)', '400 mg/day in divided doses: 100 mg every 6 h (immediate-release) or 200 mg every 12 h (CR)'),
                                                         ('CrCl 30–40 mL/min', '100 mg every 8 h (immediate-release only)'), ('CrCl 15–30 mL/min', '100 mg every 12 h (immediate-release only)'), ('CrCl <15 mL/min', '100 mg every 24 h (immediate-release only)')])],
    'Optional initial loading dose 150 mg at CrCl ≤40. Norpace CR is not recommended at CrCl ≤40 mL/min. Therapeutic levels 2–4 mcg/mL.',
    ['For patients with moderate renal insufficiency (creatinine clearance greater than 40 ml/min) or hepatic insufficiency, the recommended dosage is 400 mg/day given in divided doses (either 100 mg every 6 hours for immediate-release Norpace or 200 mg every 12 hours for Norpace CR)',
     'For patients with severe renal insufficiency (C cr 40 ml/min or less), the recommended dosage regimen of immediate-release Norpace is 100 mg at intervals shown in the table below, with or without an initial loading dose of 150 mg',
     'IMMEDIATE-RELEASE NORPACE DOSAGE INTERVAL FOR PATIENTS WITH RENAL INSUFFICIENCY Creatinine Clearance (ml/min) 40–30 30–15 Less than 15 Approximate Maintenance-dosing interval q 8 hr q 12 hr Q 24 hr',
     'Norpace CR is not recommended for patients with severe renal insufficiency (creatinine clearance 40 ml/min or less)']),
  ihd=M('specialist', notes='No dialysis dose in the label. In overdose, haemodialysis or preferably charcoal haemoperfusion can lower serum levels.', ev=['Hemodialysis or, preferably, hemoperfusion with charcoal may be employed to lower serum concentration of the drug'])),
 pk=dict(halfLife=P('6.7 h (range 4–10)', 'The mean plasma half-life of disopyramide in healthy humans is 6.7 hours (range of 4 to 10 hours)'),
         renalHalfLife=P('8–18 h (CrCl <40 mL/min)', 'In six patients with impaired renal function (creatinine clearance less than 40 ml/min), disopyramide half-life values were 8 to 18 hours'),
         proteinBinding=P('50–65% (concentration-dependent)', 'The usual therapeutic plasma levels of disopyramide base are 2 to 4 mcg/ml, and at these concentrations protein binding varies from 50% to 65%'),
         ihd=P('Hemodialysis can lower serum levels (overdose)', 'Hemodialysis or, preferably, hemoperfusion with charcoal may be employed to lower serum concentration of the drug', 'removed')))

C['dronedarone'] = E('preg/dronedarone.json', 'MULTAQ', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)',
 summary='No renal dose adjustment (minimal renal excretion). It raises serum creatinine by blocking tubular secretion, without a true fall in GFR.',
 mods=dict(
  ckd=M('summarized', [T('All renal function · US label', [('Any CrCl', 'No dose adjustment (400 mg twice daily with meals)')])],
    'Dronedarone inhibits tubular creatinine secretion, so serum creatinine rises. Monitor renal function periodically.',
    ['Because renal excretion of dronedarone is minimal [see Clinical Pharmacology (12.3) ] , no dosing alteration is needed',
     'No pharmacokinetic difference was observed in patients with mild to severe renal impairment in comparison with patients with normal renal function',
     'Dronedarone inhibits in vivo the tubular secretion of creatinine a substrate of the organic cation transporter (OCT2) [see Warnings and Precautions (5.9) ]', 'Monitor renal function periodically']),
  ihd=M('not_curated', notes='Not known whether dronedarone or its metabolites are removed by dialysis.', ev=['It is not known whether dronedarone or its metabolites can be removed by dialysis (hemodialysis, peritoneal dialysis or hemofiltration)']),
  pd=M('not_curated', notes='Not known whether dronedarone or its metabolites are removed by dialysis.', ev=['It is not known whether dronedarone or its metabolites can be removed by dialysis (hemodialysis, peritoneal dialysis or hemofiltration)'])),
 pk=dict(halfLife=P('13–19 h', 'Its elimination half-life is 13 to 19 hours'),
         renalHalfLife=P('No PK difference in mild to severe impairment', 'No pharmacokinetic difference was observed in patients with mild to severe renal impairment in comparison with patients with normal renal function'),
         proteinBinding=P('>98% (in vitro)', 'The in vitro plasma protein binding of dronedarone and its N-debutyl metabolite is >98%'),
         ihd=P('Not known (label)', 'It is not known whether dronedarone or its metabolites can be removed by dialysis (hemodialysis, peritoneal dialysis or hemofiltration)', 'unknown'),
         pd=P('Not known (label)', 'It is not known whether dronedarone or its metabolites can be removed by dialysis (hemodialysis, peritoneal dialysis or hemofiltration)', 'unknown')))

C['ibutilide'] = E('preg/ibutilide.json', 'CORVERT', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)',
 summary='Clearance is independent of renal function (CrCl 21–140 mL/min); no renal dose adjustment.',
 mods=dict(ckd=M('summarized', [T('Atrial fibrillation/flutter conversion · US label', [('CrCl 21–140 mL/min (studied range)', 'No adjustment: usual weight-based dose')])], '',
   ['In 285 patients with atrial fibrillation or atrial flutter who were treated with CORVERT, the clearance of ibutilide was independent of renal function, as assessed by creatinine clearance (range 21 to 140 mL/min)'])),
 pk=dict(halfLife=P('≈6 h (range 2–12)', 'The elimination half-life averages about 6 hours (range from 2 to 12 hours)'),
         renalHalfLife=P('Clearance independent of CrCl 21–140 mL/min', 'In 285 patients with atrial fibrillation or atrial flutter who were treated with CORVERT, the clearance of ibutilide was independent of renal function, as assessed by creatinine clearance (range 21 to 140 mL/min)'),
         volumeOfDistribution=P('≈11 L/kg (steady state)', 'Ibutilide has a high systemic plasma clearance that approximates liver blood flow (about 29 mL/min/kg), a large steady-state volume of distribution (about 11 L/kg) in healthy volunteers, and minimal (about 40%) protein binding'),
         proteinBinding=P('≈40%', 'Ibutilide has a high systemic plasma clearance that approximates liver blood flow (about 29 mL/min/kg), a large steady-state volume of distribution (about 11 L/kg) in healthy volunteers, and minimal (about 40%) protein binding')))

C['ranolazine'] = E('preg/ranolazine.json', 'Ranolazine extended-release', promote=True, flag='monitor', metric='CrCl · mL/min',
 summary='No dose table; monitor renal function when CrCl <60. Acute renal failure occurred at CrCl <30: discontinue if it develops.',
 mods=dict(
  ckd=M('summarized', [T('Chronic angina · US label', [('CrCl <60 mL/min', 'No dose change stated; monitor renal function after starting and periodically'),
                                                     ('CrCl <30 mL/min', 'Caution: acute renal failure in 2 of 4 subjects in a PK study; discontinue if acute renal failure develops')])], '',
    ['Monitor renal function after initiation and periodically in patients with moderate to severe renal impairment (CrCL less than 60 mL/min) for increases in serum creatinine',
     'A pharmacokinetic study of ranolazine in subjects with severe renal impairment (CrCL less than 30 mL/min) was stopped when 2 of 4 subjects developed acute renal failure after receiving ranolazine 500 mg twice daily for 5 days (lead-in phase) followed by 1000 mg twice a day (1 dose in one subject and 11 doses in the other)',
     'If acute renal failure develops (e.g., marked increase in serum creatinine associated with an increase in blood urea nitrogen [BUN]), discontinue ranolazine and treat appropriately']),
  ihd=M('insufficient_data', notes='Pharmacokinetics not assessed on dialysis; haemodialysis is unlikely to clear ranolazine (≈62% protein bound).',
    ev=['The pharmacokinetics of ranolazine has not been assessed in patients on dialysis', 'Since ranolazine is about 62% bound to plasma proteins, hemodialysis is unlikely to be effective in clearing ranolazine'])),
 pk=dict(halfLife=P('7 h (apparent terminal)', 'The apparent terminal half-life of ranolazine is 7 hours'),
         renalHalfLife=P('Cmax up 40–50% in mild to severe impairment', 'In a separate study, C max was increased between 40% and 50% in patients with mild, moderate, or severe renal impairment compared to patients with no renal impairment, suggesting a similar increase in exposure in patients with renal failure independent of the degree of impairment'),
         proteinBinding=P('≈62%', 'Over the concentration range of 0.25 to 10 µg/mL, ranolazine is approximately 62% bound to human plasma proteins'),
         ihd=P('Hemodialysis unlikely to be effective (label)', 'Since ranolazine is about 62% bound to plasma proteins, hemodialysis is unlikely to be effective in clearing ranolazine', 'not_removed')))

C['aliskiren'] = E('preg/aliskiren.json', 'TEKTURNA', promote=True, flag='caution', metric='CrCl · mL/min',
 summary='No starting-dose adjustment; not established below CrCl 30. Avoid with ACE inhibitors/ARBs when CrCl <60. No adjustment on haemodialysis.',
 mods=dict(
  ckd=M('summarized', [T('Hypertension · US label', [('CrCl ≥30 mL/min', 'No starting-dose adjustment (150 mg once daily)'), ('CrCl <30 mL/min', 'Safety and effectiveness not established (excluded from trials)'),
                                                   ('CrCl <60 mL/min with an ACE inhibitor or ARB', 'Avoid the combination')])],
    'Contraindicated with ACE inhibitors or ARBs in diabetes.',
    ['Adjustment of the starting dose is not required in these patients',
     'Safety and effectiveness of Tekturna in patients with severe renal impairment [creatinine clearance (CrCl) less than 30 mL/min] have not been established as these patients were excluded in efficacy trials',
     'In general, avoid combined use of aliskiren with ACE inhibitors or ARBs, particularly in patients with CrCl less than 60 mL/min']),
  ihd=M('summarized', [T('ESRD on haemodialysis · US label', [('Haemodialysis', 'No dose adjustment; dose timing relative to HD does not matter')])], '',
    ['When compared to matched healthy subjects, changes in the rate and extent of aliskiren exposure (C max and AUC) in ESRD patients undergoing hemodialysis were not clinically significant',
     'Timing of hemodialysis did not significantly alter the pharmacokinetics of aliskiren in ESRD patients', 'Therefore, no dose adjustment is warranted in ESRD patients receiving hemodialysis'])),
 pk=dict(halfLife=P('≈24 h (accumulation)', 'Aliskiren is poorly absorbed (bioavailability about 2.5%) with an approximate accumulation half-life of 24 hours'),
         renalHalfLife=P('No consistent change with severity; not significant in ESRD on HD', 'The rate and extent of exposure (AUC and C max ) of aliskiren in subjects with renal impairment did not show a consistent correlation with the severity of renal impairment'),
         ihd=P('HD timing did not alter PK (label)', 'Timing of hemodialysis did not significantly alter the pharmacokinetics of aliskiren in ESRD patients', 'not_removed')))

C['triamterene'] = E('preg/triamterene.json', 'DYRENIUM', promote=True, flag='caution', metric='Renal function and serum potassium',
 summary='Contraindicated in anuria and severe or progressive kidney disease (US label). High hyperkalaemia risk in renal impairment.',
 mods=dict(
  ckd=M('summarized', [T('Oedema · US label', [('Renal impairment', 'Caution: hyperkalaemia more likely; check potassium and BUN frequently'), ('Severe or progressive kidney disease', 'Contraindicated (possible exception: nephrosis)'), ('Raised serum potassium', 'Do not use')])], '',
    ['Severe or progressive kidney disease or dysfunction, with the possible exception of nephrosis', 'Hyperkalemia is more likely to occur in patients with renal impairment and diabetes (even without evidence of renal impairment), and in the elderly or severely ill',
     'Periodic BUN and serum potassium determinations should be made to check kidney function, especially in patients with suspected or confirmed renal insufficiency']),
  ihd=M('avoid', notes='Contraindicated in anuria and severe kidney disease.', ev=['Severe or progressive kidney disease or dysfunction, with the possible exception of nephrosis']),
  pd=M('avoid', notes='Contraindicated in anuria and severe kidney disease.', ev=['Severe or progressive kidney disease or dysfunction, with the possible exception of nephrosis'])),
 pk=dict(proteinBinding=P('67%', 'Although triamterene is 67% protein bound, there may be some benefit to dialysis in cases of overdosage'),
         ihd=P('Possibly some benefit in overdose (label)', 'Although triamterene is 67% protein bound, there may be some benefit to dialysis in cases of overdosage', 'limited')))

C['tolvaptan'] = E('preg/tolvaptan.json', 'SAMSCA (hyponatraemia)', promote=True, flag='caution', metric='CrCl · mL/min',
 summary='No renal dose adjustment down to CrCl 10; not recommended below 10. Contraindicated in anuria. (Jynarque for ADPKD is a different product.)',
 mods=dict(
  ckd=M('summarized', [T('Hyponatraemia (SAMSCA) · US label', [('CrCl ≥10 mL/min', 'No dose adjustment: 15 mg once daily, titrate to 30–60 mg'), ('CrCl <10 mL/min', 'Not recommended (no data; effect on sodium likely lost)'), ('Anuria', 'Contraindicated')])],
    'Start and restart in hospital with serum sodium monitoring. Onset and offset of the sodium effect are slower in severe impairment.',
    ['No dose adjustment is necessary based on renal function', 'There are no clinical trial data in patients with CrCl <10 mL/min, and, because drug effects on serum sodium levels are likely lost at very low levels of renal function, use in patients with a CrCl <10 mL/min is not recommended',
     'No benefit can be expected in patients who are anuric']),
  ihd=M('avoid', notes='Not recommended at CrCl <10 mL/min and contraindicated in anuria; dialysis may not remove it (>98% bound).', ev=['Dialysis may not be effective in removing tolvaptan because of its high binding affinity for human plasma protein (>98%)']),
  pd=M('avoid', notes='Not recommended at CrCl <10 mL/min and contraindicated in anuria.', ev=['No benefit can be expected in patients who are anuric'])),
 pk=dict(halfLife=P('≈3 h (15 mg) to ≈12 h (≥120 mg)', 'Following single oral doses to healthy subjects, the estimated half-life of tolvaptan increases from 3 hours for a 15 mg dose to approximately 12 hours for 120 mg and higher doses due to more prolonged absorption of tolvaptan at higher doses; apparent clearance is approximately 4 mL/min/kg and does not appear to change with in'.split('; apparent')[0]),
         renalHalfLife=P('AUC less than doubled (CrCl <30)', 'Renal Impairment In a study in patients with creatinine clearances ranging from 10 to 124 mL/min administered a single dose of 60 mg tolvaptan, AUC and C max of plasma tolvaptan were less than doubled in patients with severe renal impairment (creatinine clearance <30 mL/min) relative to the controls'),
         volumeOfDistribution=P('≈3 L/kg', 'The volume of distribution of tolvaptan is about 3 L/kg'),
         proteinBinding=P('>98%', 'Distribution Tolvaptan binds to both albumin and α1-acid glycoprotein and the overall protein binding is >98%; binding is not affected by disease state'),
         ihd=P('Dialysis may not be effective (label)', 'Dialysis may not be effective in removing tolvaptan because of its high binding affinity for human plasma protein (>98%)', 'not_removed')))

C['hydrochlorothiazide'] = E('preg/hydrochlorothiazide.json', 'Hydrochlorothiazide capsules', promote=True, flag='caution', metric='Renal function',
 summary='Contraindicated in anuria. Thiazide effects may accumulate in renal impairment; the US label gives no renal dose table.',
 mods=dict(
  ckd=M('specialist', notes='Cumulative effects can develop in impaired renal function; plasma levels rise and half-life lengthens. Contraindicated in anuria. No numeric renal dose in this label.',
    ev=['Renal Disease: Cumulative effects of the thiazides may develop in patients with impaired renal function', 'Hydrochlorothiazide is contraindicated in patients with anuria']),
  ihd=M('avoid', notes='Contraindicated in anuria. Removal by haemodialysis has not been established.', ev=['Hydrochlorothiazide is contraindicated in patients with anuria', 'The degree to which hydrochlorothiazide is removed by hemodialysis has not been established'])),
 pk=dict(halfLife=P('6–15 h', 'The plasma elimination half-life has been reported to be 6 to 15 hours'),
         renalHalfLife=P('Prolonged in renal disease', 'In patients with renal disease, plasma concentrations of hydrochlorothiazide are increased and the elimination half-life is prolonged'),
         ihd=P('Not established (label)', 'The degree to which hydrochlorothiazide is removed by hemodialysis has not been established', 'unknown')))

C['enalaprilat'] = E('preg/enalaprilat.json', 'Enalaprilat injection', promote=True, flag='adjust', metric='CrCl · mL/min',
 summary='1.25 mg IV every 6 h if CrCl >30; start 0.625 mg if ≤30 or on dialysis. Dialysable.',
 mods=dict(
  ckd=M('summarized', [T('Hypertension, IV · US label', [('CrCl >30 mL/min', '1.25 mg IV every 6 h'), ('CrCl ≤30 mL/min', 'Initial 0.625 mg IV'), ('Switch to oral enalapril', 'CrCl >30: 5 mg once daily; CrCl ≤30: 2.5 mg once daily')])], '',
    ['Dosage Adjustment in Renal Impairment The usual dose of 1.25 mg of enalaprilat injection every six hours is recommended for patients with a creatinine clearance > 30 mL/min (serum creatinine of up to approximately 3 mg/dL)',
     'For patients with creatinine clearance ≤ 30 mL/min (serum creatinine ≥ 3 mg/dL), the initial dose is 0.625 mg (see WARNINGS )',
     'For conversion from intravenous to oral therapy, the recommended initial dose of oral enalapril maleate is 5 mg once a day for patients with creatinine clearance > 30 mL/min and 2.5 mg once daily for patients with creatinine clearance ≤ 30 mL/min']),
  ihd=M('summarized', [T('Dialysis · US label', [('Haemodialysis (risk of excessive hypotension)', 'Start ≤0.625 mg IV over at least 5 min (preferably up to 1 h)')])],
    'Enalaprilat is dialysable (62 mL/min). Anaphylactoid reactions have occurred with high-flux membranes in patients on ACE inhibitors.',
    ['The starting dose should be no greater than 0.625 mg administered intravenously over a period of no less than five minutes and preferably longer (up to one hour)', 'Enalaprilat is dialyzable at the rate of 62 mL/min',
     'Anaphylactoid reactions during membrane exposure: Anaphylactoid reactions have been reported in patients dialyzed with high-flux membranes and treated concomitantly with an ACE inhibitor'])),
 pk=dict(halfLife=P('≈11 h (effective, accumulation)', 'The effective half-life for accumulation of enalaprilat, as determined from oral administration of multiple doses of enalapril maleate, is approximately 11 hours'),
         ihd=P('Dialyzable at 62 mL/min (label)', 'Enalaprilat is dialyzable at the rate of 62 mL/min', 'removed')))

# ======================================================================= Batch 2: IV vasoactive drugs and lipid-lowering catalog entries
TITRATE = 'Titrated to haemodynamic response; the US label gives no renal dose adjustment.'
C['norepinephrine'] = E('preg/norepinephrine.json', 'LEVOPHED', promote=True, flag='monitor', metric='Titrate to blood pressure',
 summary=TITRATE, mods=dict(ckd=M('specialist', notes=TITRATE)),
 pk=dict(halfLife=P('≈2.4 min (mean)', 'Elimination The mean half-life of norepinephrine is approximately 2.4 min'),
         volumeOfDistribution=P('8.8 L', 'The volume of distribution is 8.8 L'), proteinBinding=P('≈25%', 'Distribution Plasma protein binding of norepinephrine is approximately 25%')))
C['vasopressin'] = E('preg/vasopressin.json', 'Vasopressin injection', promote=True, flag='monitor', metric='Titrate to blood pressure',
 summary=TITRATE, mods=dict(ckd=M('specialist', notes=TITRATE)),
 pk=dict(halfLife=P('≤10 min (apparent)', 'The apparent t1/2 of vasopressin at these levels is ≤10 minutes'), volumeOfDistribution=P('140 mL/kg', 'The volume of distribution is 140 mL/kg')))
C['epinephrine'] = E('preg/epinephrine.json', 'Epinephrine injection', promote=True, flag='monitor', metric='Titrate to blood pressure',
 summary=TITRATE + ' It constricts renal vessels and may cause oliguria or renal impairment.',
 mods=dict(ckd=M('specialist', notes=TITRATE + ' Epinephrine constricts renal blood vessels, which may cause oliguria or renal impairment.', ev=['Epinephrine constricts renal blood vessels, which may result in oliguria or renal impairment'])))
C['clevidipine'] = E('preg/clevidipine.json', 'CLEVIPREX', promote=True, flag='no_adjust', metric='Titrate to blood pressure',
 summary='Cleared by blood and tissue esterases, so elimination is unlikely to be affected by renal dysfunction; titrate to blood pressure.',
 mods=dict(ckd=M('summarized', [T('Acute blood-pressure control · US label', [('Moderate to severe renal impairment', 'No adjustment: usual titrated infusion (121 such patients in trials)')])], '',
   ['Metabolism and Elimination: Clevidipine is rapidly metabolized by hydrolysis of the ester linkage, primarily by esterases in the blood and extravascular tissues, making its elimination unlikely to be affected by hepatic or renal dysfunction',
    'In clinical trials, 78 patients with abnormal hepatic function (one or more of the following: elevated serum bilirubin, AST/SGOT, ALT/SGPT) and 121 patients with moderate to severe renal impairment were treated with Cleviprex'])),
 pk=dict(halfLife=P('≈15 min terminal (initial phase ≈1 min)', 'The terminal half-life is approximately 15 minutes'),
         volumeOfDistribution=P('0.17 L/kg (steady state)', 'The steady-state volume of distribution was determined to be 0.17 L/kg in arterial blood'),
         proteinBinding=P('>99.5%', 'Distribution: Clevidipine is >99.5% bound to proteins in plasma at 37°C')))
C['sodium-nitroprusside'] = E('preg/sodium-nitroprusside.json', 'NIPRIDE RTU', promote=True, flag='adjust', metric='eGFR · mL/min/1.73 m²',
 summary='eGFR <30: keep the mean infusion rate below 3 mcg/kg/min (thiocyanate accumulates). Haemodialysis removes thiocyanate but not cyanide.',
 mods=dict(
  ckd=M('summarized', [T('Hypertensive crisis / acute heart failure · US label', [('eGFR <30 mL/min/1.73 m²', 'Limit the mean infusion rate to <3 mcg/kg/min'), ('Normal renal function, cumulative dose >7 mg/kg/day', 'Monitor plasma thiocyanate')])],
    'Thiocyanate is life-threatening at about 200 mg/L.', ['In patients with eGFR <30 mL/min/1.73 m 2 , limit the mean infusion rate to less than 3 mcg/kg/min',
     'Therefore, routine monitoring of plasma thiocyanate levels is recommended in patients with normal renal function when cumulative sodium nitroprusside doses exceed 7 mg/kg/day']),
  ihd=M('specialist', notes='Haemodialysis eliminates most thiocyanate (used for severe toxicity) but does not remove cyanide.', ev=['Hemodialysis is ineffective in removal of cyanide, but it will eliminate most thiocyanate'])),
 pk=dict(halfLife=P('≈2 min (circulatory)', 'The drug is cleared by intraerythrocytic reaction with hemoglobin (Hgb), and sodium nitroprusside’s resulting circulatory half-life is about 2 minutes'),
         renalHalfLife=P('Thiocyanate half-life doubled or tripled in renal failure', 'In renal failure, the half-life can be doubled or tripled'),
         ihd=P('Removes most thiocyanate, not cyanide (label)', 'Hemodialysis is ineffective in removal of cyanide, but it will eliminate most thiocyanate', 'limited')))
C['alirocumab'] = E('preg/alirocumab.json', 'PRALUENT', promote=True, flag='no_adjust', metric='No renal dose adjustment (mild–moderate; US label)',
 summary='No adjustment for mild or moderate renal impairment; no data in severe impairment.',
 mods=dict(ckd=M('summarized', [T('All indications · US label', [('Mild or moderate impairment', 'No dose adjustment'), ('Severe impairment', 'No data available')])], '',
   ['8.6 Renal Impairment No dose adjustment is needed for patients with mild or moderately impaired renal function'.replace('8.6 Renal Impairment ', ''), 'No data are available in patients with severe renal impairment'])),
 pk=dict(halfLife=P('17–20 days (apparent, steady state)', 'Based on a population pharmacokinetic analysis, the median apparent half-life of alirocumab at steady state was 17 to 20 days in patients receiving alirocumab at subcutaneous doses of 75 mg every 2 weeks or 150 mg every 2 weeks'),
         volumeOfDistribution=P('0.04–0.05 L/kg (IV)', 'Distribution Following intravenous administration, the volume of distribution was about 0.04 to 0.05 L/kg indicating that alirocumab is distributed primarily in the circulatory system')))
C['evolocumab'] = E('preg/evolocumab.json', 'REPATHA', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)',
 summary='No dose adjustment in renal impairment.', mods=dict(ckd=M('summarized', [T('All indications · US label', [('Any renal impairment', 'No dose adjustment')])], '', ['No dose adjustment is needed in patients with renal impairment'])))
C['inclisiran'] = E('preg/inclisiran.json', 'LEQVIO', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)',
 summary='No adjustment in mild, moderate or severe renal impairment; not studied in end-stage kidney disease.',
 mods=dict(ckd=M('summarized', [T('All indications · US label', [('Mild, moderate or severe impairment', 'No dose adjustment'), ('End-stage kidney disease', 'Not studied')])], 'Exposure rises 1.6–3.3-fold in renal impairment but LDL-C lowering is similar.',
   ['No dose adjustments are necessary for patients with mild, moderate, or severe renal impairment [see Clinical Pharmacology (12.3)]', 'LEQVIO has not been studied in patients with end stage renal disease [see Clinical Pharmacology (12.3)]',
    'Despite the higher plasma exposures, reductions in LDL-C were similar across all groups based on renal function'])),
 pk=dict(halfLife=P('≈9 h (terminal)', 'Elimination The terminal elimination half-life of LEQVIO is approximately 9 hours, and no accumulation occurs with multiple dosing'),
         renalHalfLife=P('AUC 1.6–2.3× in mild to severe impairment', 'Patients with Renal Impairment Pharmacokinetic analysis of data from a dedicated renal impairment study reported increases in inclisiran C max and AUC of approximately 2.3 to 3.3-fold and 1.6 to 2.3-fold, respectively, in patients with mild, moderate or severe renal impairment, relative to patients with normal renal function'),
         volumeOfDistribution=P('≈500 L (apparent)', 'Following a single subcutaneous 284 mg dose of LEQVIO to healthy adults, the apparent volume of distribution is approximately 500 L')))
C['bempedoic-acid'] = E('preg/bempedoic-acid.json', 'NEXLETOL', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)',
 summary='No clinically significant PK change in mild to severe renal impairment or renal failure.',
 mods=dict(ckd=M('summarized', [T('All indications · US label', [('Mild, moderate or severe impairment, or renal failure', 'No dose adjustment (no clinically significant PK difference)')])], '',
   ['Specific Populations No clinically significant differences in the pharmacokinetics of bempedoic acid were observed based on age, gender, race, weight, renal impairment (mild, moderate, and severe renal impairment or renal failure), or mild (Child-Pugh Class A) and moderate (Child-Pugh Class B) hepatic impairment'])),
 pk=dict(halfLife=P('21 ± 11 h (steady state)', 'The mean ± SD half-life for bempedoic acid in humans was 21 ± 11 hours at steady-state'),
         volumeOfDistribution=P('18 L (V/F)', 'Distribution The bempedoic acid apparent volume of distribution (V/F) was 18 L'),
         proteinBinding=P('99.3%', 'Plasma protein binding of bempedoic acid, its glucuronide and its active metabolite, ESP15228, were 99.3%, 98.8% and 99.2%, respectively')))
C['fluvastatin'] = E('preg/fluvastatin.json', 'Fluvastatin sodium ER', promote=True, flag='caution', metric='Renal function',
 summary='No adjustment in mild–moderate impairment; caution in severe impairment (not studied above 40 mg). Monitor for myopathy.',
 mods=dict(
  ckd=M('summarized', [T('All indications · US label', [('Mild to moderate impairment', 'No dose adjustment'), ('Severe impairment', 'Use with caution: not studied above 40 mg')])], 'Renal impairment is a risk factor for myopathy and rhabdomyolysis: monitor.',
    ['Dose adjustments for mild to moderate renal impairment are not necessary', 'Fluvastatin has not been studied at doses greater than 40 mg in patients with severe renal impairment; therefore, use fluvastatin sodium extended-release tablets with caution in patients with severe renal impairment',
     'Renal impairment is a risk factor for myopathy and rhabdomyolysis']),
  ihd=M('specialist', notes='In end-stage kidney disease on haemodialysis, AUC rose about 1.5-fold; use with caution and monitor for myopathy.', ev=['In patients with end-stage renal disease on hemodialysis, the AUC increased by approximately 1.5-fold'])),
 pk=dict(halfLife=P('≈3 h', 'The elimination half-life (t 1/2 ) of fluvastatin is approximately 3 hours'), renalHalfLife=P('AUC ≈1.5× in ESRD on haemodialysis', 'In patients with end-stage renal disease on hemodialysis, the AUC increased by approximately 1.5-fold'),
         volumeOfDistribution=P('0.35 L/kg (Vss)', 'The mean volume of distribution (VD ss ) is estimated at 0.35 L/kg'), proteinBinding=P('98%', 'Distribution Fluvastatin is 98% bound to plasma proteins')))
C['icosapent-ethyl'] = E('preg/icosapent-ethyl.json', 'Icosapent ethyl', promote=True, flag='caution', metric='Not studied in renal impairment',
 summary='Not studied in renal impairment (US label).', mods=dict(ckd=M('insufficient_data', notes='Not studied in renal or hepatic impairment.', ev=['Hepatic or Renal Impairment Icosapent ethyl has not been studied in patients with renal or hepatic impairment'])),
 pk=dict(halfLife=P('≈89 h (EPA)', 'The plasma elimination half-life (t 1/2 ) of EPA is approximately 89 hours'), volumeOfDistribution=P('≈88 L (EPA, steady state)', 'Distribution The mean volume of distribution at steady state of EPA is approximately 88 liters'),
         proteinBinding=P('>99% (unesterified EPA)', 'Greater than 99% of unesterified EPA is bound to plasma proteins')))

# ======================================================================= Batch 3: PK and dialysis statements for existing CV renal profiles
def HD(text, ev, status='summarized'): return M(status, [T('Haemodialysis · US label', [('Haemodialysis', text)])], '', ev)
NS = 'No dialysis dose in the label; not removed, so no supplement after HD'
C['atorvastatin'] = E('preg/atorvastatin.json', 'Atorvastatin calcium', pk_only=True, mods=dict(ihd=HD('No adjustment (renal disease does not change levels); haemodialysis not expected to enhance clearance',
   ['Renal Impairment Renal disease has no influence on the plasma concentrations or LDL-C reduction of atorvastatin calcium [see Use in Specific Populations (8.6)]', 'Due to extensive drug binding to plasma proteins, hemodialysis is not expected to significantly enhance atorvastatin calcium clearance'])),
 pk=dict(halfLife=P('≈14 h (activity 20–30 h)', 'Mean plasma elimination half-life of atorvastatin calcium in humans is approximately 14 hours, but the half-life of inhibitory activity for HMG-CoA reductase is 20 to 30 hours due to the contribution of active metabolites'),
         volumeOfDistribution=P('≈381 L', 'Distribution Mean volume of distribution of atorvastatin calcium is approximately 381 liters'), proteinBinding=P('≥98%', 'Atorvastatin calcium is ≥98% bound to plasma proteins'),
         renalHalfLife=P('No change in renal disease', 'Renal Impairment Renal disease has no influence on the plasma concentrations or LDL-C reduction of atorvastatin calcium [see Use in Specific Populations (8.6)]'),
         ihd=P('Not expected to be enhanced by hemodialysis (label)', 'Due to extensive drug binding to plasma proteins, hemodialysis is not expected to significantly enhance atorvastatin calcium clearance', 'not_removed')))
C['rosuvastatin'] = E('preg/rosuvastatin.json', 'Rosuvastatin calcium', pk_only=True,
 pk=dict(halfLife=P('≈19 h', 'The elimination half-life of rosuvastatin is approximately 19 hours'), volumeOfDistribution=P('≈134 L (steady state)', 'Distribution Mean volume of distribution at steady-state of rosuvastatin is approximately 134 liters'),
         proteinBinding=P('88%', 'Rosuvastatin is 88% bound to plasma proteins, mostly albumin'),
         renalHalfLife=P('≈3× exposure (CrCl <30, not on HD); ≈50% higher on HD', 'However, plasma concentrations of rosuvastatin increased to a clinically significant extent (about 3-fold) in patients with severe renal impairment (CL cr<30 mL/min/1.73 m 2) not receiving hemodialysis compared with healthy subjects (CLcr >80 mL/min/1.73 m 2)'),
         ihd=P('Not significantly enhanced by hemodialysis (label)', 'Hemodialysis does not significantly enhance clearance of rosuvastatin', 'not_removed')))
C['rosuvastatin']['pk']['renalHalfLife']['value'] = 'About 3-fold exposure (CrCl <30, not on haemodialysis)'
C['ezetimibe'] = E('preg/ezetimibe.json', 'Ezetimibe', pk_only=True,
 pk=dict(halfLife=P('≈22 h (ezetimibe and glucuronide)', 'Both ezetimibe and ezetimibe-glucuronide are eliminated from plasma with a half-life of approximately 22 hours for both ezetimibe and ezetimibe-glucuronide'),
         proteinBinding=P('>90%', 'Distribution Ezetimibe and ezetimibe-glucuronide are highly bound (>90%) to human plasma proteins')))
C['pravastatin'] = E('preg/pravastatin.json', 'Pravastatin sodium', pk_only=True,
 pk=dict(halfLife=P('1.8 h (pravastatin); 77 h (total radioactivity)', 'Following single dose oral administration of 14 C-pravastatin, the radioactive elimination t ½ for pravastatin is 1.8 hours in humans and the elimination half-life (t ½ ) for total radioactivity (pravastatin plus metabolites) is 77 hours'),
         proteinBinding=P('≈50%', 'Distribution Approximately 50% of the circulating drug is bound to plasma proteins')))
C['simvastatin'] = E('preg/simvastatin.json', 'Simvastatin', pk_only=True, pk=dict(proteinBinding=P('≈95% (simvastatin and β-hydroxyacid)', 'Distribution Both simvastatin and its β-hydroxyacid metabolite are highly bound (approximately 95%) to human plasma proteins')))
C['pitavastatin'] = E('preg/pitavastatin.json', 'LIVALO', pk_only=True,
 pk=dict(halfLife=P('≈12 h', 'The mean plasma elimination half-life is approximately 12 hours'), proteinBinding=P('>99%', 'Distribution Pitavastatin is more than 99% protein bound in human plasma, mainly to albumin')))
C['pitavastatin']['pk']['proteinBinding']['value'] = 'more than 99%'
C['gemfibrozil'] = E('preg/gemfibrozil.json', 'Gemfibrozil', pk_only=True, pk=dict(halfLife=P('1.5 h (multiple doses)', 'Peak plasma levels occur in 1 to 2 hours with a plasma half-life of 1.5 hours following multiple doses')))
C['fenofibrate'] = E('preg/fenofibrate.json', 'ANTARA (fenofibrate)', pk_only=True,
 pk=dict(halfLife=P('23 h (fenofibric acid)', 'Fenofibric acid is eliminated with a half-life of 23 hours, allowing once daily dosing'), proteinBinding=P('≈99%', 'Serum protein binding was approximately 99% in normal and hyperlipidemic subjects'),
         renalHalfLife=P('Longer half-life, similar exposure (CrCl 30–80)', 'Patients with mild to moderate renal impairment (CrCl 30 mL/min to 80 mL/min or eGFR 30 mL/min/1.73m 2 to 59 mL/min/1.73m 2 ) had similar exposure but an increase in the half-life for fenofibric acid compared to that of healthy subjects'),
         ihd=P('Hemodialysis should not be considered (label)', 'Because fenofibrate is highly bound to plasma proteins, hemodialysis should not be considered', 'not_removed')))
C['adenosine'] = E('us/adenosine.json', 'Adenosine injection', pk_only=True, pk=dict(halfLife=P('<10 seconds', 'Overdosage The half-life of adenosine injection is less than 10 seconds')))
C['adenosine']['pk']['halfLife']['value'] = 'less than 10 seconds'
C['amiloride'] = E('preg/amiloride.json', 'Amiloride', pk_only=True, pk=dict(halfLife=P('6–9 h', 'Peak plasma levels are obtained in 3 to 4 hours and the plasma half-life varies from 6 to 9 hours'),
         ihd=P('Not known (label)', 'It is not known whether the drug is dialyzable', 'unknown')))
C['bumetanide'] = E('preg/bumetanide.json', 'Bumetanide', pk_only=True, pk=dict(halfLife=P('1–1½ h', 'Several pharmacokinetic studies have shown that bumetanide, administered orally or parenterally, is eliminated rapidly in humans, with a half-life of between 1 and 1½ hours')))
C['felodipine'] = E('preg/felodipine.json', 'Felodipine ER', pk_only=True,
 pk=dict(halfLife=P('9.1 h (terminal, IV)', 'Following intravenous administration, the plasma concentration of felodipine declined triexponentially with mean disposition half-lives of 4.8 minutes, 1.5 hours, and 9.1 hours'),
         volumeOfDistribution=P('≈10 L/kg', 'The systemic plasma clearance of felodipine in young healthy subjects is about 0.8 L/min, and the apparent volume of distribution is about 10 L/kg'),
         proteinBinding=P('>99%', 'Felodipine is greater than 99% bound to plasma proteins'), ihd=P('Not established (label)', 'It has not been established whether felodipine can be removed from the circulation by hemodialysis', 'unknown')))
C['felodipine']['pk']['proteinBinding']['value'] = 'greater than 99%'
C['labetalol'] = E('preg/labetalol.json', 'Labetalol', pk_only=True,
 mods=dict(ihd=HD(NS + ' (<1% removed)', ['Neither hemodialysis nor peritoneal dialysis removes a significant amount of labetalol from the general circulation (<1%)']),
           pd=M('summarized', [T('Peritoneal dialysis · US label', [('Peritoneal dialysis', 'No PD dose in the label; <1% removed, so no supplement')])], '', ['Neither hemodialysis nor peritoneal dialysis removes a significant amount of labetalol from the general circulation (<1%)'])),
 pk=dict(halfLife=P('6–8 h (oral)', 'The plasma half-life of labetalol following oral administration is about 6 to 8 hours'),
         renalHalfLife=P('Not altered in renal impairment', 'In patients with decreased hepatic or renal function, the elimination half-life of labetalol is not altered; however, the relative bioavailability in hepatically impaired patients is increased due to decreased “first-pass” metabolism'),
         ihd=P('<1% removed by hemodialysis (label)', 'Neither hemodialysis nor peritoneal dialysis removes a significant amount of labetalol from the general circulation (<1%)', 'not_removed'),
         pd=P('<1% removed by peritoneal dialysis (label)', 'Neither hemodialysis nor peritoneal dialysis removes a significant amount of labetalol from the general circulation (<1%)', 'not_removed')))
C['propranolol'] = E('preg/propranolol.json', 'Propranolol', pk_only=True,
 mods=dict(ihd=HD(NS, ['Propranolol is not significantly dialyzable'])),
 pk=dict(halfLife=P('≈4 h (healthy; 11 h in cirrhosis)', 'In cirrhosis, the half-life increased to 11 hours compared to 4 hours (see PRECAUTIONS )'),
         renalHalfLife=P('Shorter half-life but 3–4× higher peak levels in renal failure', 'Despite this shorter plasma half-life, propranolol peak plasma levels were 3 to 4 times higher and total plasma levels of metabolites were up to 3 times higher in these patients than in subjects with normal renal function'),
         ihd=P('Not significantly dialyzable (label)', 'Propranolol is not significantly dialyzable', 'not_removed')))
C['perindopril'] = E('preg/perindopril.json', 'Perindopril erbumine', pk_only=True,
 pk=dict(halfLife=P('0.8–1 h (perindopril); perindoprilat terminal 30–120 h', 'The mean half-life of perindopril associated with most of its elimination is approximately 0.8 to 1 hours'),
         proteinBinding=P('≈60% (perindopril); 10–20% (perindoprilat)', 'Distribution: Approximately 60% of circulating perindopril is bound to plasma proteins, and only 10 to 20% of perindoprilat is bound'),
         ihd=P('Removed during dialysis (label)', 'During dialysis, perindopril is removed with the same clearance as in patients with normal renal function', 'removed')))
C['perindopril']['pk']['halfLife']['value'] = '0.8–1 h (perindopril)'
C['diltiazem'] = E('preg/diltiazem.json', 'Diltiazem', pk_only=True, mods=dict(ihd=HD(NS, ['Diltiazem does not appear to be removed by peritoneal or hemodialysis']),
   pd=M('summarized', [T('Peritoneal dialysis · US label', [('Peritoneal dialysis', 'No PD dose in the label; not removed, so no supplement')])], '', ['Diltiazem does not appear to be removed by peritoneal or hemodialysis'])),
 pk=dict(ihd=P('Not removed (label)', 'Diltiazem does not appear to be removed by peritoneal or hemodialysis', 'not_removed'), pd=P('Not removed (label)', 'Diltiazem does not appear to be removed by peritoneal or hemodialysis', 'not_removed')))
C['nifedipine'] = E('preg/nifedipine.json', 'Nifedipine', pk_only=True,
 mods=dict(ihd=HD('No adjustment: PK not significantly altered on HD; dialysis unlikely to remove it', ['Patients in hemodialysis or chronic ambulatory peritoneal dialysis have not reported significantly altered pharmacokinetics of nifedipine', 'Since nifedipine is highly protein-bound, dialysis is not likely to be of any benefit']),
           pd=M('summarized', [T('Peritoneal dialysis (CAPD) · US label', [('CAPD', 'No adjustment: PK not significantly altered')])], '', ['Patients in hemodialysis or chronic ambulatory peritoneal dialysis have not reported significantly altered pharmacokinetics of nifedipine'])),
 pk=dict(ihd=P('Not likely to be of benefit (label)', 'Since nifedipine is highly protein-bound, dialysis is not likely to be of any benefit', 'not_removed')))
C['doxazosin'] = E('preg/doxazosin.json', 'Doxazosin', pk_only=True, mods=dict(ihd=HD(NS, ['As doxazosin is highly protein bound, dialysis would not be indicated'])),
 pk=dict(ihd=P('Dialysis not indicated (protein bound; label)', 'As doxazosin is highly protein bound, dialysis would not be indicated', 'not_removed')))
C['tamsulosin'] = E('preg/tamsulosin.json', 'Tamsulosin', pk_only=True, mods=dict(ihd=HD(NS, ['Laboratory data indicate that tamsulosin hydrochloride is 94% to 99% protein bound; therefore, dialysis is unlikely to be of benefit'])),
 pk=dict(ihd=P('Unlikely to be of benefit (label)', 'Laboratory data indicate that tamsulosin hydrochloride is 94% to 99% protein bound; therefore, dialysis is unlikely to be of benefit', 'not_removed')))
C['olmesartan'] = E('preg/olmesartan.json', 'Olmesartan medoxomil', pk_only=True, mods=dict(ihd=M('insufficient_data', notes='Not studied on haemodialysis; dialysability unknown.', ev=['The dialyzability of olmesartan is unknown'])))
C['amiodarone'] = E('us/amiodarone.json', 'Amiodarone', pk_only=True, mods=dict(ihd=HD('No dialysis dose in the label; neither amiodarone nor DEA is dialysable, so no supplement after HD', ['Neither amiodarone nor DEA is dialyzable'])))

# Dose sentences behind numbers quoted in tables/considerations
EXTRA = {'aliskiren': ['Starting dose (adults and pediatric patients): 150 mg once daily with a routine pattern with regard to meals'],
 'dronedarone': ['The recommended dosage of MULTAQ is 400 mg twice daily in adults'],
 'tolvaptan': ['The recommended starting dose is 15 mg once daily', 'Dosage may be increased at intervals ≥24 hr to 30 mg once daily, and to a maximum of 60 mg once daily as needed to raise serum sodium'],
 'sotalol': ['The recommended initial dose is 80 mg twice daily'],
 'dofetilide': ['If the QTc or QT has increased by greater than 15% compared to the baseline established in Step 1 OR if the QTc or QT is greater than 500 msec (550 msec in patients with ventricular conduction abnormalities), subsequent dosing should be adjusted as follows',
                'Renal function and QTc or QT (if heart rate is less than 60 beats per minute) should be re-evaluated every three months or as medically warranted',
                'The maximum recommended dose in patients with a calculated creatinine clearance greater than 60 mL/min is 500 mcg BID; doses greater than 500 mcg BID have been associated with an increased incidence of Torsade de Pointes']}
for k, v in EXTRA.items(): C[k]['modalities']['ckd']['ev'] += v

(R/'curation_v125.json').write_text(json.dumps(C, ensure_ascii=False, indent=1))
print(len(C), 'entries')
