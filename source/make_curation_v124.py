"""Curated label content for v0.12.4 (digoxin, proton pump inhibitors, vonoprazan PK).
Every value carries the verbatim label sentence it comes from ("ev"). Writes curation_v124.json.
Edit here, rerun, then run extract_quotes_v124.py (needs the downloaded labels) and the build.
"""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(__file__).parent

def pk(value, ev, status='sourced'): return dict(value=value, ev=ev, status=status)

PPI_PD = 'The US label has no peritoneal-dialysis data. It reports no renal dose adjustment at any level of kidney function and no removal by haemodialysis; a PD dose is not inferred.'

C = {}
# ---------------------------------------------------------------- Digoxin (Lanoxin tablets)
LBW = [40, 50, 60, 70, 80, 90, 100]
T3 = {10: ('62.5*', 125, 125, 187.5, 187.5, 187.5, 250, 19), 20: (125, 125, 125, 187.5, 187.5, 250, 250, 16),
      30: (125, 125, 187.5, 187.5, 250, 250, 312.5, 14), 40: (125, 187.5, 187.5, 250, 250, 312.5, 312.5, 13),
      50: (125, 187.5, 187.5, 250, 250, 312.5, 312.5, 12), 60: (125, 187.5, 250, 250, 312.5, 312.5, 375, 11),
      70: (187.5, 187.5, 250, 250, 312.5, 375, 375, 10), 80: (187.5, 187.5, 250, 312.5, 312.5, 375, 437.5, 9),
      90: (187.5, 250, 250, 312.5, 375, 437.5, 437.5, 8), 100: (187.5, 250, 312.5, 312.5, 375, 437.5, 500, 7)}
C['digoxin'] = dict(label='extra/lanoxin_tab.json', brand='LANOXIN tablets',
 kidneyMetric='Corrected CrCl (mL/min per 70 kg) and lean body weight',
 summary='Once-daily maintenance dose by corrected CrCl and lean body weight (US label Table 3); not removed by dialysis.',
 considerations='Base the dose on lean body weight and corrected CrCl, then adjust to clinical response and serum digoxin concentrations. Steady state takes 7–19 days depending on renal function.',
 modalities=dict(
  ckd=dict(status='summarized', tables=[
    dict(indication='Maintenance dose, micrograms once daily (tablets) · US label Table 3', rows=[
      dict(context=f'Corrected CrCl {c} mL/min', dose='; '.join(f'{w} kg: {v}' for w, v in zip(LBW, r[:7])) + f' mcg (lean body weight) · steady state ≈{r[7]} days')
      for c, r in T3.items()]),
    dict(indication='Loading dose, if needed (adults) · US label Table 1', rows=[
      dict(context='Adults', dose='10–15 mcg/kg in total: half first, then ¼ every 6–8 h twice, assessing response and toxicity before each dose')])],
   notes='Corrected CrCl is per 70 kg or 1.73 m²; the label estimates it in men as (140 − age) ÷ SCr, × 0.85 in women. * = about 30% below the calculated dose: check a level and increase if needed. Alternative: maintenance = loading dose × (14 + CrCl/5) ÷ 100. Reduce the dose when lean weight is a small fraction of total body mass (obesity, oedema). Levels <0.5 ng/mL are associated with diminished efficacy and >2 ng/mL with toxicity; adverse reactions may increase above 1.2 ng/mL. Doses come from studies in heart failure.',
   ev=['Table 3 provides the recommended (once daily) maintenance dose for adults and pediatric patients over 10 years old (to be given once daily) according to lean body weight and renal function',
       'Recommended doses approximately 30 percent lower than the calculated dose are designated with an *',
       'Total Maintenance Dose = Loading Dose (i.e., Peak Body Stores) x % Daily Loss/100 (% Daily Loss = 14 + Creatinine clearance/5)',
       'Serum digoxin levels less than 0.5 ng/mL have been associated with diminished efficacy, while levels above 2 ng/mL have been associated with increased toxicity without increased benefit',
       'As digoxin serum levels increase above 1.2 ng/mL, there is a potential for increase in adverse reactions']),
  ihd=dict(status='specialist', tables=[], notes='Not removed by dialysis: give no supplement after haemodialysis. The label dose table stops at CrCl 10 mL/min, so the maintenance dose in dialysis patients is individualised from serum levels (half-life 3.5–5 days in anuria).',
   ev=['Digoxin is not effectively removed from the body by dialysis, exchange transfusion, or during cardiopulmonary bypass because most of the drug is bound to extravascular tissues', 'The half-life in anuric patients is prolonged to 3.5-5 days']),
  pd=dict(status='specialist', tables=[], notes='The label states digoxin is not effectively removed by dialysis (modality not specified). No PD dose is given; individualise from serum levels.',
   ev=['Digoxin is not effectively removed from the body by dialysis because of its large extravascular volume of distribution'])),
 pk=dict(halfLife=pk('1.5–2 days (normal renal function)', 'In healthy volunteers with normal renal function, digoxin has a half-life of 1.5-2 days'),
         renalHalfLife=pk('3.5–5 days (anuric)', 'The half-life in anuric patients is prolonged to 3.5-5 days'),
         volumeOfDistribution=pk('≈475–500 L (follows lean body weight)', 'Digoxin is concentrated in tissues and therefore has a large apparent volume of distribution (approximately 475-500 L)'),
         proteinBinding=pk('≈25%', 'Approximately 25% of digoxin in the plasma is bound to protein'),
         ihd=pk('Not effectively removed by dialysis (label)', 'Digoxin is not effectively removed from the body by dialysis, exchange transfusion, or during cardiopulmonary bypass because most of the drug is bound to extravascular tissues', 'not_removed'),
         pd=pk('Not effectively removed by dialysis (label; modality not specified)', 'Digoxin is not effectively removed from the body by dialysis because of its large extravascular volume of distribution', 'not_removed')))

# ---------------------------------------------------------------- Proton pump inhibitors
def ppi(label, brand, renal_ev, ihd_text, ihd_ev, pkd, promote=False):
    return dict(label=label, brand=brand, promote=promote,
     kidneyMetric='No renal dose adjustment (US label)', flag='no_adjust',
     summary='No renal dose adjustment at any level of kidney function (US label). Review the need for long-term acid suppression separately.',
     modalities=dict(
      ckd=dict(status='summarized', tables=[dict(indication='All adult indications · US label', rows=[dict(context='Any CrCl / eGFR, including severe impairment', dose='No dose adjustment: use the usual indication-specific dose')])],
               notes='', ev=renal_ev),
      ihd=dict(status='summarized', tables=[dict(indication='Haemodialysis · US label', rows=[dict(context='Haemodialysis', dose=ihd_text)])], notes='', ev=ihd_ev),
      pd=dict(status='not_curated', tables=[], notes=PPI_PD, ev=[])),
     pk=pkd)

C['omeprazole'] = ppi('preg/omeprazole.json', 'Omeprazole',
 ['In patients with chronic renal impairment (creatinine clearance between 10 and 62 mL/min/1.73 m2), the disposition of omeprazole was very similar to that in healthy subjects, although there was a slight increase in bioavailability'],
 'No adjustment stated; not readily dialyzable, so no supplement after HD',
 ['Omeprazole is extensively protein bound and is, therefore, not readily dialyzable'],
 dict(halfLife=pk('0.5–1 h', 'In healthy subjects the plasma half-life is 0.5 to 1 hour, and the total body clearance is 500 to 600 mL/min'),
      renalHalfLife=pk('Disposition similar to healthy subjects (CrCl 10–62 mL/min)', 'In patients with chronic renal impairment (creatinine clearance between 10 and 62 mL/min/1.73 m2), the disposition of omeprazole was very similar to that in healthy subjects, although there was a slight increase in bioavailability'),
      proteinBinding=pk('≈95%', 'Protein binding is approximately 95%'),
      ihd=pk('Not readily dialyzable (label)', 'Omeprazole is extensively protein bound and is, therefore, not readily dialyzable', 'not_removed')))

C['esomeprazole'] = ppi('preg/esomeprazole.json', 'Esomeprazole magnesium', promote=True,
 renal_ev=['The pharmacokinetics of esomeprazole magnesium delayed-release capsules in patients with renal impairment are not expected to be altered relative to healthy subjects as less than 1% of esomeprazole is excreted unchanged in urine'],
 ihd_text='No adjustment; not expected to be removed by dialysis, so no supplement after HD',
 ihd_ev=['Since esomeprazole is extensively protein bound, it is not expected to be removed by dialysis'],
 pkd=dict(halfLife=pk('≈1–1.5 h', 'The plasma elimination half-life of esomeprazole is approximately 1 to 1.5 hours'),
      renalHalfLife=pk('Not expected to change (<1% excreted unchanged)', 'The pharmacokinetics of esomeprazole magnesium delayed-release capsules in patients with renal impairment are not expected to be altered relative to healthy subjects as less than 1% of esomeprazole is excreted unchanged in urine'),
      volumeOfDistribution=pk('≈16 L (steady state)', 'The apparent volume of distribution at steady state in healthy subjects is approximately 16 L'),
      proteinBinding=pk('97%', 'Esomeprazole is 97% bound to plasma proteins'),
      ihd=pk('Not expected to be removed by dialysis (label)', 'Since esomeprazole is extensively protein bound, it is not expected to be removed by dialysis', 'not_removed')))

C['lansoprazole'] = ppi('preg/lansoprazole.json', 'Lansoprazole', promote=True,
 renal_ev=['Therefore, the pharmacokinetics of lansoprazole were not clinically different in patients with mild, moderate or severe renal impairment compared to healthy subjects with normal renal function'],
 ihd_text='No adjustment; not removed by haemodialysis, so no supplement after HD',
 ihd_ev=['Lansoprazole is not removed from the circulation by hemodialysis'],
 pkd=dict(halfLife=pk('1.5 ± 1.0 h', 'In healthy subjects, the mean (±SD) plasma half-life was 1.5 (±1.0) hours'),
      renalHalfLife=pk('Shortened; PK not clinically different in renal impairment', 'Patients with renal impairment had a shortened elimination half-life and decreased total AUC (free and bound)'),
      proteinBinding=pk('97%', 'Lansoprazole is 97% bound to plasma proteins'),
      ihd=pk('Not removed by hemodialysis (label)', 'Lansoprazole is not removed from the circulation by hemodialysis', 'not_removed')))

C['pantoprazole'] = ppi('preg/pantoprazole.json', 'PROTONIX delayed-release',
 ['In patients with severe renal impairment, pharmacokinetic parameters for pantoprazole were similar to those of healthy subjects'],
 'No adjustment; not removed by haemodialysis, so no supplement after HD',
 ['Pantoprazole is not removed by hemodialysis'],
 dict(halfLife=pk('about one hour (terminal)', 'Following oral or intravenous administration, the serum concentration of pantoprazole declines biexponentially, with a terminal elimination half-life of approximately one hour'),
      renalHalfLife=pk('Similar to healthy subjects (severe renal impairment)', 'In patients with severe renal impairment, pharmacokinetic parameters for pantoprazole were similar to those of healthy subjects'),
      volumeOfDistribution=pk('≈11–23.6 L', 'The apparent volume of distribution of pantoprazole is approximately 11 to 23.6 L, distributing mainly in extracellular fluid'),
      proteinBinding=pk('≈98%', 'The serum protein binding of pantoprazole is about 98%, primarily to albumin'),
      ihd=pk('Not removed by hemodialysis (label)', 'Pantoprazole is not removed by hemodialysis', 'not_removed')))

C['rabeprazole'] = ppi('preg/rabeprazole.json', 'ACIPHEX',
 ['In 10 patients with stable end-stage renal disease requiring maintenance hemodialysis (creatinine clearance ≤5 mL/min/1.73 m 2 ), no clinically significant differences were observed in the pharmacokinetics of rabeprazole after a single 20 mg dose of ACIPHEX delayed-release tablets when compared to 10 healthy subjects'],
 'No adjustment: PK in maintenance-HD patients similar to healthy subjects; not readily dialyzable',
 ['In 10 patients with stable end-stage renal disease requiring maintenance hemodialysis (creatinine clearance ≤5 mL/min/1.73 m 2 ), no clinically significant differences were observed in the pharmacokinetics of rabeprazole after a single 20 mg dose of ACIPHEX delayed-release tablets when compared to 10 healthy subjects',
  'Rabeprazole is extensively protein bound and is not readily dialyzable'],
 dict(halfLife=pk('1–2 h', 'This relatively prolonged pharmacodynamic action compared to the short pharmacokinetic half-life (1 to 2 hours) reflects the sustained inactivation of the H + , K + ATPase'),
      renalHalfLife=pk('No clinically significant change in ESRD on haemodialysis', 'In 10 patients with stable end-stage renal disease requiring maintenance hemodialysis (creatinine clearance ≤5 mL/min/1.73 m 2 ), no clinically significant differences were observed in the pharmacokinetics of rabeprazole after a single 20 mg dose of ACIPHEX delayed-release tablets when compared to 10 healthy subjects'),
      proteinBinding=pk('96.3%', 'Rabeprazole is 96.3% bound to human plasma proteins'),
      ihd=pk('Not readily dialyzable (label)', 'Rabeprazole is extensively protein bound and is not readily dialyzable', 'not_removed')))

C['dexlansoprazole'] = ppi('preg/dexlansoprazole.json', 'DEXILANT',
 ['Therefore, the pharmacokinetics of dexlansoprazole are not expected to be altered in patients with renal impairment, and no studies were conducted in patients with renal impairment'],
 'No adjustment expected (not studied); not expected to be removed by haemodialysis',
 ['Dexlansoprazole is not expected to be removed from the circulation by hemodialysis'],
 dict(halfLife=pk('about one to two hours', 'Dexlansoprazole is eliminated with a half-life of approximately one to two hours in healthy subjects and in patients with symptomatic GERD'),
      renalHalfLife=pk('Not expected to change (no parent drug in urine; not studied)', 'Renal Impairment Dexlansoprazole is extensively metabolized in the liver to inactive metabolites, and no parent drug is recovered in the urine following an oral dose of dexlansoprazole'),
      ihd=pk('Not expected to be removed by hemodialysis (label)', 'Dexlansoprazole is not expected to be removed from the circulation by hemodialysis', 'not_removed')))

# ---------------------------------------------------------------- Vonoprazan (dosing added in v0.12.1; PK and dialysis note here)
C['vonoprazan'] = dict(label='us/vonoprazan.json', brand='VOQUEZNA', pk_only=True,
 modalities=dict(ihd=dict(status='not_curated', tables=[], notes='No dialysis dose in the US label. On dialysis, exposure (AUC) was 1.3-fold that of normal renal function and only 0.94% of the dose appeared in the dialysate.',
   ev=['In subjects requiring dialysis (N=8), AUC 0-inf estimates were 1.3-fold greater compared to estimates from subjects with normal renal function', 'In patients requiring dialysis, vonoprazan was present in the dialysate and represented 0.94% of the dose administered'])),
 pk=dict(halfLife=pk('6.8–7.9 h (steady state)', 't 1/2z (h) 7.7 (27.1) 7.9 (22.6) 6.8 (22.7)'),
         renalHalfLife=pk('Exposure (AUC) 2.4× in severe impairment; 1.3× on dialysis', 'Compared to subjects with normal renal function, systemic exposure (AUC 0-inf ) was 1.7-, 1.3-, and 2.4-times greater in patients with mild, moderate, and severe renal impairment, respectively'),
         volumeOfDistribution=pk('782.7–1270.7 L (apparent oral, Vz/F)', 'V z /F (L) 1270.7 (26.6) 1114.0 (39.6) 782.7 (34.4)'),
         proteinBinding=pk('85–88%', 'Plasma protein binding of vonoprazan ranged from 85 to 88% in healthy subjects and was independent of concentration from 0.1 to 10 mcg/mL'),
         ihd=pk('0.94% of the dose in dialysate (negligible)', 'In patients requiring dialysis, vonoprazan was present in the dialysate and represented 0.94% of the dose administered', 'negligible')))

(R/'curation_v124.json').write_text(json.dumps(C, ensure_ascii=False, indent=1))
print(len(C), 'entries')
