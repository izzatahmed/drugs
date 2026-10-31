# ---- Batch O: oncology ----
def P_(i, brand, flag, metric, summary, ckd, ihd=None, pd=None):
    mods = dict(ckd=ckd)
    if ihd: mods['ihd'] = ihd
    if pd: mods['pd'] = pd
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary, mods=mods)
S = lambda ind, rows, ev, notes='': M('summarized', [T(ind, rows)], notes, ev)
HDT = lambda rows, ev, notes='': M('summarized', [T('Haemodialysis · US label', rows)], notes, ev)
NOREN = 'The current US label gives no renal dose statement.'
P_('carboplatin', 'Carboplatin', 'adjust', 'CrCl / GFR (Calvert formula)',
   'Dose by Calvert formula: total dose (mg) = target AUC × (GFR + 25). Single-agent table: CrCl 41–59 → 250 mg/m²; 16–40 → 200 mg/m².',
   S('All indications · US label', [('Calvert formula', 'Total dose (mg) = target AUC × (GFR + 25)'), ('Baseline CrCl 41–59 mL/min', '250 mg/m² on day 1'), ('Baseline CrCl 16–40 mL/min', '200 mg/m² on day 1')],
     ['Total Dose (mg) = (target AUC) × (GFR + 25)', 'Baseline Creatinine Clearance Recommended Dose on Day 1 41 - 59 mL/min 250 mg/m 2 16 - 40 mL/min 200 mg/m 2'], 'Insufficient data below CrCl 16 in this table.'))
P_('cisplatin', 'Cisplatin', 'caution', 'CrCl · mL/min', 'Nephrotoxic: measure creatinine, CrCl and electrolytes before treatment; consider dose reduction or alternatives in renal impairment.',
   M('specialist', notes='Consider dose reductions or alternative treatments in renal impairment; check serum creatinine, BUN, CrCl and electrolytes including magnesium before starting.',
     ev=['Consider dose reductions or alternative treatments in patients with renal impairment', 'Measure serum creatinine, blood urea nitrogen, creatinine clearance, and serum electrolytes including magnesium prior to initiating therapy, and as clinically indicated']))
P_('oxaliplatin', 'Oxaliplatin', 'adjust', 'CrCl · mL/min (Cockcroft–Gault)', 'CrCl <30: reduce the dose to 65 mg/m².',
   S('Colorectal cancer · US label', [('CrCl <30 mL/min', 'Reduce to 65 mg/m²')], ['In patients with severe renal impairment (creatinine clearance [CLcr] less than 30 mL/min, calculated by the Cockcroft-Gault equation), reduce the oxaliplatin injection dose to 65 mg/m 2']))
P_('capecitabine', 'Capecitabine', 'adjust', 'CrCl · mL/min (Cockcroft–Gault)', 'Reduce the dose by 25% at CrCl 30–50; no established dose below 30.',
   S('All indications · US label', [('CrCl 30–50 mL/min', 'Reduce the dose by 25%'), ('CrCl <30 mL/min', 'Dose not established')],
     ['Reduce the dose of capecitabine tablet by 25% for patients with creatinine clearance (CLcr) of 30 to 50 mL/min as determined by Cockcroft-Gault equation', 'A dosage has not been established in patients with severe renal impairment (CLcr <30 mL/min)']))
P_('etoposide', 'Etoposide', 'adjust', 'CrCl · mL/min', 'Give 75% of the dose at CrCl 15–50; no data below 15.',
   S('All indications · US label', [('CrCl 15–50 mL/min', '75% of the recommended dose'), ('CrCl <15 mL/min', 'No data')], ['In patients with a creatinine clearance (CLcr) 15-50 mL/min, administer 75% of the recommended dose', 'Data are not available in patients with CLcr less than 15 mL/min']))
P_('hydroxyurea', 'XROMI (hydroxyurea oral solution)', 'adjust', 'CrCl · mL/min', 'Halve the dose at CrCl <60 or ESRD; on dialysis days give after haemodialysis.',
   S('All indications · US label', [('CrCl <60 mL/min', 'Reduce the dose by 50%')], ['Reduce the dose of XROMI by 50% in patients with creatinine clearance of less than 60 mL/min or with end-stage renal disease (ESRD)']),
   ihd=HDT([('ESRD on haemodialysis', '50% dose; give after haemodialysis on dialysis days')], ['Reduce the dose of XROMI by 50% in patients with creatinine clearance of less than 60 mL/min or with end-stage renal disease (ESRD)', 'On dialysis days, administer XROMI to patients with ESRD following hemodialysis']))
P_('lenalidomide', 'REVLIMID', 'adjust', 'CrCl · mL/min (Cockcroft–Gault)', 'Starting dose by CrCl and indication (label Table 3); on dialysis give after the session.',
   M('summarized', [T('MM / MCL combination · US label Table 3', [('CrCl 30–60 mL/min', '10 mg once daily'), ('CrCl <30, not on dialysis', '15 mg every other day')]),
                     T('FL / MZL combination · US label Table 3', [('CrCl 30–60 mL/min', '10 mg once daily'), ('CrCl <30, not on dialysis', '5 mg once daily')]),
                     T('MM maintenance / MDS · US label Table 3', [('CrCl 30–60 mL/min', '5 mg once daily'), ('CrCl <30, not on dialysis', '2.5 mg once daily')])], '',
     ['CLcr 30 to 60 mL/min 10 mg once daily 10 mg once daily 5 mg once daily CLcr below 30 mL/min (not requiring dialysis) 15 mg every other day 5 mg once daily 2.5 mg once daily']),
   ihd=M('summarized', [T('On dialysis · US label Table 3', [('MM / MCL or FL / MZL combination', '5 mg once daily, after dialysis on dialysis days'), ('MM maintenance / MDS', '2.5 mg once daily, after dialysis on dialysis days')])], '',
     ['CLcr below 30 mL/min (requiring dialysis) 5 mg once daily. On dialysis days, administer the dose following dialysis']))
P_('pemetrexed', 'Pemetrexed', 'caution', 'CrCl · mL/min (Cockcroft–Gault)', 'Do not give if CrCl <45.',
   S('All indications · US label', [('CrCl ≥45 mL/min', '500 mg/m² every 21 days'), ('CrCl <45 mL/min', 'Do not administer')], ['Do not administer PEMFEXY if the creatinine clearance is less than 45 mL/min', 'The recommended dosage of PEMFEXY, administered as a single agent or with cisplatin, in patients with creatinine clearance of 45 mL/minute or greater, is 500 mg/m 2 as an intravenous infusion over 10 minutes on Day 1 of each 21-day cycle']),
   ihd=M('avoid', notes='Not to be given at CrCl <45 mL/min.', ev=['Do not administer PEMFEXY if the creatinine clearance is less than 45 mL/min']))
P_('olaparib', 'LYNPARZA', 'adjust', 'CrCl · mL/min', 'CrCl 31–50: 200 mg twice daily. No data at CrCl ≤30.',
   S('All indications · US label', [('CrCl 31–50 mL/min', '200 mg twice daily'), ('CrCl ≤30 mL/min or ESRD', 'No data')], ['In patients with moderate renal impairment (CLcr 31-50 mL/min), reduce the Lynparza dosage to 200 mg orally twice daily', 'There are no data in patients with severe renal impairment or end-stage renal disease (CLcr ≤30 mL/min)']))
P_('imatinib', 'Imatinib', 'adjust', 'CrCl · mL/min', 'CrCl 20–39: start at 50% of the dose; CrCl 40–59: max 600 mg; caution in severe impairment (100 mg/day tolerated in 2 patients).',
   S('All indications · US label', [('CrCl 40–59 mL/min', 'Doses above 600 mg not recommended'), ('CrCl 20–39 mL/min', '50% of the starting dose; increase as tolerated'), ('CrCl <20 mL/min', 'Caution (100 mg/day tolerated in two patients)')],
     ['Patients with moderate renal impairment (creatinine clearance [CrCL] = 20-39 mL/min) should receive a 50% decrease in the recommended starting dose and future doses can be increased as tolerated', 'Doses greater than 600 mg are not recommended in patients with mild renal impairment (CrCL = 40-59 mL/min)', 'A dose of 100 mg/day was tolerated in two patients with severe renal impairment']))
P_('pomalidomide', 'POMALYST', 'adjust', 'Dialysis', 'MM with severe impairment on dialysis: 3 mg daily, given after dialysis on HD days.',
   M('specialist', notes='Dose modification applies to severe renal impairment requiring dialysis (see dialysis tab).', ev=['For patients with MM with severe renal impairment requiring dialysis, reduce the recommended dosage to 3 mg orally daily']),
   ihd=HDT([('Severe impairment on dialysis (MM)', '3 mg daily; take after dialysis on HD days')], ['For patients with MM with severe renal impairment requiring dialysis, reduce the recommended dosage to 3 mg orally daily', 'Take POMALYST after completion of dialysis procedure on hemodialysis days']))
P_('bortezomib', 'VELCADE', 'no_adjust', 'No starting-dose adjustment (US label)', 'No starting-dose adjustment; on dialysis give after the procedure.',
   S('Myeloma / MCL · US label', [('Any renal impairment', 'No starting-dose adjustment')], ['No starting dosage adjustment of VELCADE is recommended for patients with renal impairment']),
   ihd=HDT([('Dialysis', 'Give after the dialysis procedure')], ['In patients requiring dialysis, VELCADE should be administered after the dialysis procedure']))
P_('carfilzomib', 'KYPROLIS', 'monitor', 'Renal function', 'Withhold for SCr ≥2× baseline, CrCl <15 or need for haemodialysis; on HD give after dialysis.',
   S('Renal toxicity · US label', [('SCr ≥2× baseline, CrCl <15, CrCl ≤50% of baseline, or need for HD', 'Withhold and monitor renal function')], ['Serum creatinine greater than or equal to 2 × baseline, or Creatinine clearance less than 15 mL/min, or creatinine clearance decreases to less than or equal to 50% of baseline, or need for hemodialysis Withhold dose and continue monitoring renal function']),
   ihd=HDT([('ESRD on haemodialysis', 'Give after the haemodialysis procedure')], ['For patients with end stage renal disease who are on hemodialysis, administer Kyprolis after the hemodialysis procedure']))
P_('bleomycin', 'Bleomycin', 'caution', 'CrCl · mL/min', 'CrCl <50: lower doses may be needed; monitor renal function (half-life rises steeply as CrCl falls).',
   M('specialist', notes='At CrCl <50 mL/min treat with caution and monitor renal function; lower doses may be required (see the label dose table).',
     ev=['Patients with creatinine clearance values of less than 50 mL/min should be treated with caution and their renal function should be carefully monitored during the administration of bleomycin', 'The terminal elimination half-life increases exponentially as the creatinine clearance decreases']))
P_('gemcitabine', 'Gemcitabine', 'caution', 'Renal function', 'Discontinue for haemolytic uraemic syndrome or severe renal impairment.',
   M('specialist', notes='Discontinue for HUS or severe renal impairment; HUS can cause renal failure requiring dialysis.', ev=['Discontinue gemcitabine for HUS or severe renal impairment']))
P_('abemaciclib', 'VERZENIO', 'no_adjust', 'CrCl · mL/min', 'No adjustment at CrCl 30–89; unknown in severe impairment, ESRD or dialysis.',
   S('Breast cancer · US label', [('CrCl 30–89 mL/min', 'No dose adjustment'), ('CrCl <30, ESRD or dialysis', 'PK unknown')], ['No dosage adjustment is required for patients with mild or moderate renal impairment (CLcr ≥30-89 mL/min, estimated by Cockcroft-Gault [C-G])', 'The pharmacokinetics of abemaciclib in patients with severe renal impairment (CLcr <30 mL/min, C-G), end stage renal disease, or in patients on dialysis is unknown']))
P_('abiraterone', 'Abiraterone acetate', 'no_adjust', 'No renal dose adjustment (US label)', 'No dose change in renal impairment (studied in ESRD on haemodialysis).',
   S('Prostate cancer · US label', [('Any renal impairment, including ESRD on HD', 'No dose modification')], ['No dosage modification is recommended for patients with renal impairment']))
P_('anastrozole', 'ARIMIDEX', 'no_adjust', 'No renal dose adjustment (US label)', 'No dose adjustment in renal impairment.',
   S('Breast cancer · US label', [('Any renal impairment', 'No dose adjustment')], ['Dosage adjustment in patients with renal impairment is not necessary']))
P_('letrozole', 'Letrozole', 'no_adjust', 'CrCl · mL/min', 'No adjustment if CrCl ≥10.',
   S('Breast cancer · US label', [('CrCl ≥10 mL/min', 'No dose adjustment')], ['No dosage adjustment is required for patients with renal impairment if creatinine clearance is greater than or equal to 10 mL/min']))
P_('enzalutamide', 'XTANDI', 'no_adjust', 'CrCl · mL/min', 'No adjustment at CrCl ≥30; not studied below 30 or in ESRD.',
   S('Prostate cancer · US label', [('CrCl ≥30 mL/min', 'No dose modification'), ('CrCl <30 or ESRD', 'Not studied')], ['No dosage modification is recommended for patients with mild to moderate renal impairment (creatinine clearance [CLcr] ≥ 30 mL/min)', 'XTANDI has not been studied in patients with severe renal impairment (CLcr < 30 mL/min) or end-stage renal disease']))
P_('osimertinib', 'TAGRISSO', 'no_adjust', 'CrCl · mL/min', 'No adjustment at CrCl 15–89; no recommended dose at CrCl <15.',
   S('NSCLC · US label', [('CrCl 15–89 mL/min', 'No dose adjustment'), ('CrCl <15 mL/min (ESRD)', 'No recommended dose')], ['No dose adjustment is recommended in patients with creatinine clearance (CLcr) 15 - 89 mL/min, as estimated by Cockcroft-Gault', 'There is no recommended dose of TAGRISSO for patients with end-stage renal disease (CLcr <15 mL/min)']))
P_('paclitaxel', 'Paclitaxel protein-bound (albumin-bound)', 'no_adjust', 'CrCl · mL/min', 'Albumin-bound form: no starting-dose change at CrCl 30–89; insufficient data below 30.',
   S('Albumin-bound paclitaxel · US label', [('CrCl 30 to <90 mL/min', 'No starting-dose adjustment'), ('CrCl <30 or ESRD', 'Insufficient data')], ['There are insufficient data to permit dosage recommendations in patients with severe renal impairment or end stage renal disease (estimated creatinine clearance <30 mL/min)']))
P_('palbociclib', 'IBRANCE', 'no_adjust', 'CrCl · mL/min', 'No adjustment at CrCl >15; not studied on haemodialysis.',
   S('Breast cancer · US label', [('CrCl >15 mL/min', 'No dose adjustment')], ['No dose adjustment is required in patients with mild, moderate, or severe renal impairment (CrCl >15 mL/min)']))
P_('ribociclib', 'KISQALI', 'adjust', 'CrCl · mL/min', 'No adjustment at CrCl 30–89; severe renal impairment: start 200 mg once daily.',
   S('Breast cancer · US label', [('Severe renal impairment', 'Starting dose 200 mg once daily')], ['The recommended starting dose is 200 mg KISQALI once daily for patients with severe renal impairment']))
P_('rucaparib', 'RUBRACA', 'no_adjust', 'CrCl · mL/min', 'No change at CrCl 30–89; not studied below 30 or on dialysis.',
   S('All indications · US label', [('CrCl 30–89 mL/min', 'No dose modification'), ('CrCl <30 or dialysis', 'Not studied')], ['Rubraca has not been studied in patients with CLcr < 30 mL/min or patients on dialysis']))
P_('zanubrutinib', 'BRUKINSA', 'no_adjust', 'CrCl · mL/min', 'No adjustment at CrCl ≥15; monitor for adverse reactions on dialysis.',
   S('All indications · US label', [('CrCl ≥15 mL/min', 'No dose modification')], ['No dosage modification is recommended in patients with mild, moderate, or severe renal impairment (CLcr ≥15 mL/min, estimated by Cockcroft-Gault)']),
   ihd=HDT([('Dialysis', 'No dose stated; monitor for adverse reactions')], ['Monitor for BRUKINSA adverse reactions in patients on dialysis']))
P_('ibrutinib', 'IMBRUVICA', 'no_adjust', 'CrCl · mL/min', 'No influence on exposure at CrCl >25; no data in severe impairment or dialysis.',
   S('All indications · US label', [('CrCl >25 mL/min', 'No exposure change; usual dose'), ('CrCl <25 or dialysis', 'No data')], ['Mild and moderate renal impairment (creatinine clearance [CLcr] > 25 mL/min as estimated by Cockcroft-Gault equation) had no influence on the exposure of ibrutinib', 'No data is available in patients with severe renal impairment (CLcr < 25 mL/min) or in patients on dialysis']))
P_('venetoclax', 'VENCLEXTA', 'caution', 'CrCl · mL/min', 'Tumour lysis risk rises with CrCl <80: consider hospital admission for the first ramp-up doses.',
   M('specialist', notes='Reduced renal function (CrCl <80) raises tumour lysis risk; consider admission for the first 20 mg and 50 mg doses.', ev=['particularly reduced renal function (creatinine clearance [CLcr] <80 mL/min) and tumor burden']))
P_('vincristine', 'Vincristine', 'monitor', 'No renal statement in the US label', 'No renal dose statement; haemodialysis not useful in overdose.', M('specialist', notes='No renal dose statement; very little appears in dialysate.', ev=['Because only very small amounts of the drug appear in dialysate, hemodialysis is not likely to be helpful in cases of overdosage']))
P_('trastuzumab', 'Trastuzumab', 'no_adjust', 'CrCl · mL/min', 'No PK difference in mild–moderate renal impairment.',
   S('All indications · US label', [('CrCl 30–90 mL/min', 'No PK difference; usual dose')], ['and renal impairment (mild (creatinine clearance [CLcr] 60 to 90 mL/min) (n = 636) or moderate (CLcr 30 to 60 mL/min) (n = 133))']))
P_('rasburicase', 'ELITEK', 'no_adjust', 'No PK effect of CrCl (US label)', 'Creatinine clearance did not affect rasburicase PK.',
   S('Tumour lysis · US label', [('Any CrCl', 'Usual weight-based dose')], ['age, gender, baseline liver enzymes and creatinine clearance did not impact the pharmacokinetics of rasburicase']))
for i, brand in [('docetaxel', 'Docetaxel'), ('doxorubicin', 'Doxorubicin'), ('fluorouracil', 'Fluorouracil'), ('dasatinib', 'Dasatinib'), ('nilotinib', 'Nilotinib'), ('tamoxifen', 'Tamoxifen'),
                 ('atezolizumab', 'TECENTRIQ'), ('nivolumab', 'OPDIVO'), ('pembrolizumab', 'KEYTRUDA'), ('cetuximab', 'ERBITUX'), ('bevacizumab', 'Bevacizumab'), ('daratumumab', 'DARZALEX'), ('acalabrutinib', 'CALQUENCE')]:
    P_(i, brand, 'monitor', 'No renal statement in the US label', NOREN, M('specialist', notes=NOREN))
C['melphalan'] = E(lab('melphalan'), '', pk_only=True)
