# ---- Batch R: allergy & respiratory catalog entries ----
def spec3(i, brand, notes, ev, flag='monitor', ihd=None, status='specialist'):
    mods = dict(ckd=M(status, notes=notes, ev=ev))
    if ihd: mods['ihd'] = ihd
    add(i, brand, promote=True, flag=flag, metric='Renal function', summary=notes, mods=mods)
add('umeclidinium', 'INCRUSE ELLIPTA', promote=True, flag='no_adjust', metric='No renal dose adjustment (US label)', summary='No adjustment, including CrCl <30 (no relevant exposure change).',
 mods=dict(ckd=M('summarized', [T('COPD · US label', [('Any renal impairment, including CrCl <30', 'No dose adjustment')])], '',
   ['No dosage adjustment is required in patients with renal impairment', 'Patients with severe renal impairment (CrCl <30 mL/min) showed no relevant increases in C max or AUC, nor did protein binding differ between subjects with severe renal impairment and their healthy controls'])))
add('benralizumab', 'FASENRA', promote=True, flag='no_adjust', metric='CrCl · mL/min', summary='Clearance comparable at CrCl 30–80; no formal renal studies.',
 mods=dict(ckd=M('summarized', [T('Asthma · US label', [('CrCl 30–80 mL/min', 'Clearance comparable; usual dose')])], 'No formal renal impairment studies.',
   ['Based on population pharmacokinetic analysis, benralizumab clearance was comparable in patients with creatinine clearance values between 30 and 80 mL/min and patients with normal renal function'])))
spec3('beclometasone', 'QVAR REDIHALER', 'Effect of renal impairment not evaluated (inhaled corticosteroid).', ['The effect of renal impairment on the pharmacokinetics of QVAR REDIHALER has not been evaluated'])
spec3('budesonide-inhaled', 'PULMICORT FLEXHALER', 'No data in renal impairment (inhaled corticosteroid).', ['There are no data regarding the specific use of PULMICORT FLEXHALER in patients with hepatic or renal impairment'])
spec3('fluticasone', 'Fluticasone propionate DISKUS', 'No formal PK studies in renal impairment (inhaled corticosteroid).', ['Formal pharmacokinetic studies using fluticasone propionate DISKUS have not been conducted in patients with renal impairment'])
spec3('salmeterol', 'SEREVENT DISKUS', 'No renal dose statement; benefit of dialysis in overdose not established.', ['There is insufficient evidence to determine if dialysis is beneficial for overdosage of SEREVENT DISKUS'])
for i, brand in [('mepolizumab', 'NUCALA'), ('omalizumab', 'XOLAIR'), ('dupilumab', 'DUPIXENT'), ('benzonatate', 'Benzonatate'), ('diphenhydramine', 'Diphenhydramine injection')]:
    spec3(i, brand, 'The current US label gives no renal dose statement.', [])
