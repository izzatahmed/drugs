# ---- Batch I: dialysis statements for existing renal profiles in these classes ----
def ihd_only(i, brand, rows, ev, notes='', status='summarized'):
    add(i, brand, pk_only=True, mods=dict(ihd=M(status, [T('Haemodialysis · US label', rows)] if rows else [], notes, ev)))
ALLO = 'eGFR Recommended Dosage > 20 mL/min to 60 mL/min No dosage modification 10 mL/min to 20 mL/min 200 mg/day < 10 mL/min 100 mg/day On dialysis 50 mg every 12 hours, or 100 mg every 24 hours'
ihd_only('allopurinol', 'Allopurinol tablets', [('On dialysis', '50 mg every 12 h or 100 mg every 24 h')], [ALLO, 'Both allopurinol and oxipurinol are dialyzable; however, the usefulness of hemodialysis or peritoneal dialysis in the management of an overdose of allopurinol is unknown'])
ihd_only('semaglutide-oral', 'RYBELSUS', [('ESRD / dialysis', 'No adjustment: no clinically relevant PK change in renal impairment including ESRD')],
 ['In patients with renal impairment including end-stage renal disease (ESRD), no clinically relevant change in semaglutide pharmacokinetics was observed'], 'Volume depletion from GI effects has caused acute kidney injury.')
ihd_only('linagliptin', 'TRADJENTA', [('Haemodialysis', 'No dialysis dose in the label; removal by haemodialysis or PD unlikely, so no supplement')], ['Removal of linagliptin by hemodialysis or peritoneal dialysis is unlikely'])
C['linagliptin']['modalities']['pd'] = M('summarized', [T('Peritoneal dialysis · US label', [('Peritoneal dialysis', 'No PD dose in the label; removal unlikely, so no supplement')])], '', ['Removal of linagliptin by hemodialysis or peritoneal dialysis is unlikely'])
ihd_only('glipizide', 'Glipizide', [], ['Because of the extensive protein binding of glipizide, dialysis is unlikely to be of benefit'], 'No dialysis dose in the label; dialysis is unlikely to remove glipizide (overdose context).', 'specialist')
ihd_only('alfuzosin', 'UROXATRAL', [], ['Alfuzosin is 82% to 90% protein bound; therefore, dialysis may not be of benefit'], 'No dialysis dose in the label; dialysis may not remove alfuzosin (overdose context).', 'specialist')
ihd_only('silodosin', 'Silodosin', [], ['Dialysis is unlikely to be of significant benefit since silodosin is highly (97%) protein bound'], 'No dialysis dose in the label; dialysis unlikely to remove silodosin (overdose context).', 'specialist')
for i, ev in [('alendronate', 'Dialysis would not be beneficial')]:
    C.setdefault(i, E(lab(i), '', pk_only=True))
