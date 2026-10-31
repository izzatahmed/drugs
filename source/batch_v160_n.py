# ---- v0.16.0 batch: new medicines (oncology, anaesthesia & critical care, contrast media, others) and three catalog promotions ----
def P_(i, brand, flag, metric, summary, ckd, ihd=None, pd=None, considerations=None):
    mods = dict(ckd=ckd)
    if ihd: mods['ihd'] = ihd
    if pd: mods['pd'] = pd
    add(i, brand, promote=True, flag=flag, metric=metric, summary=summary, mods=mods, considerations=considerations)
S = lambda ind, rows, ev, notes='': M('summarized', [T(ind, rows)], notes, ev)
HDT = lambda rows, ev, notes='': M('summarized', [T('Haemodialysis · US label', rows)], notes, ev)
NOREN = 'The current US label gives no renal dose statement.'

# New inventory records: id -> (name, aliases, category, drug class, routes, OTC)
ON, AC, CM, TI = 'Oncology', 'Anaesthesia & critical care', 'Contrast media', 'Transplant & immunology'
NEW.update({
 'ifosfamide': ('Ifosfamide', ['Ifex'], ON, 'Alkylating agent', ['Parenteral']),
 'mesna': ('Mesna', ['Mesnex', 'Uromitexan'], ON, 'Uroprotectant', ['Parenteral', 'Oral']),
 'cytarabine': ('Cytarabine', ['Ara-C', 'Cytosar'], ON, 'Antimetabolite', ['Parenteral']),
 'fludarabine': ('Fludarabine', ['Fludara'], ON, 'Purine analogue', ['Parenteral']),
 'cladribine': ('Cladribine', ['Leustatin', 'Mavenclad'], ON, 'Purine analogue', ['Parenteral', 'Oral']),
 'bendamustine': ('Bendamustine', ['Bendeka', 'Treanda', 'Belrapzo', 'Levact'], ON, 'Alkylating agent', ['Parenteral']),
 'busulfan': ('Busulfan (IV)', ['Busulfex'], ON, 'Alkylating agent', ['Parenteral']),
 'topotecan': ('Topotecan (IV)', ['Hycamtin'], ON, 'Topoisomerase I inhibitor', ['Parenteral']),
 'irinotecan': ('Irinotecan', ['Camptosar'], ON, 'Topoisomerase I inhibitor', ['Parenteral']),
 'vinorelbine': ('Vinorelbine', ['Navelbine'], ON, 'Vinca alkaloid', ['Parenteral']),
 'temozolomide': ('Temozolomide', ['Temodar', 'Temodal'], ON, 'Alkylating agent', ['Oral', 'Parenteral']),
 'azacitidine': ('Azacitidine (injection)', ['Vidaza'], ON, 'Hypomethylating agent', ['Parenteral']),
 'arsenic-trioxide': ('Arsenic trioxide', ['Trisenox'], ON, 'Antineoplastic', ['Parenteral']),
 'leucovorin': ('Leucovorin (folinic acid)', ['Calcium folinate', 'Folinic acid'], ON, 'Folate analogue · rescue', ['Parenteral', 'Oral']),
 'rocuronium': ('Rocuronium', ['Zemuron', 'Esmeron'], AC, 'Neuromuscular blocker (aminosteroid)', ['Parenteral']),
 'cisatracurium': ('Cisatracurium', ['Nimbex'], AC, 'Neuromuscular blocker (benzylisoquinolinium)', ['Parenteral']),
 'succinylcholine': ('Succinylcholine (suxamethonium)', ['Suxamethonium', 'Quelicin', 'Anectine'], AC, 'Depolarising neuromuscular blocker', ['Parenteral']),
 'neostigmine': ('Neostigmine (IV)', ['Bloxiverz'], AC, 'Cholinesterase inhibitor · reversal', ['Parenteral']),
 'sugammadex': ('Sugammadex', ['Bridion'], AC, 'Selective relaxant binding agent', ['Parenteral']),
 'bupivacaine': ('Bupivacaine', ['Marcaine', 'Sensorcaine'], AC, 'Local anaesthetic (amide)', ['Parenteral']),
 'flumazenil': ('Flumazenil', ['Anexate', 'Romazicon'], AC, 'Benzodiazepine antagonist', ['Parenteral']),
 'mannitol': ('Mannitol (IV)', ['Osmitrol'], AC, 'Osmotic diuretic', ['Parenteral']),
 'albumin-human': ('Albumin (human)', ['Human albumin solution', 'Albuminex'], AC, 'Plasma protein · colloid', ['Parenteral']),
 'terlipressin': ('Terlipressin', ['Terlivaz', 'Glypressin'], 'Specialist kidney therapies', 'Vasopressin analogue', ['Parenteral']),
 'gadobutrol': ('Gadobutrol', ['Gadavist', 'Gadovist'], CM, 'Gadolinium contrast · macrocyclic · ACR group II', ['Parenteral']),
 'gadoterate': ('Gadoterate meglumine', ['Dotarem', 'Clariscan'], CM, 'Gadolinium contrast · macrocyclic · ACR group II', ['Parenteral']),
 'gadoteridol': ('Gadoteridol', ['ProHance'], CM, 'Gadolinium contrast · macrocyclic · ACR group II', ['Parenteral']),
 'gadobenate': ('Gadobenate dimeglumine', ['MultiHance'], CM, 'Gadolinium contrast · linear · ACR group II', ['Parenteral']),
 'gadopiclenol': ('Gadopiclenol', ['Elucirem', 'Vueway'], CM, 'Gadolinium contrast · macrocyclic · ACR group II', ['Parenteral']),
 'gadoxetate': ('Gadoxetate disodium', ['Eovist', 'Primovist'], CM, 'Gadolinium contrast · linear, liver-specific · ACR group III', ['Parenteral']),
 'gadodiamide': ('Gadodiamide', ['Omniscan'], CM, 'Gadolinium contrast · linear · ACR group I', ['Parenteral']),
 'iohexol': ('Iohexol', ['Omnipaque'], CM, 'Iodinated contrast · non-ionic low-osmolality', ['Parenteral', 'Oral']),
 'iodixanol': ('Iodixanol', ['Visipaque'], CM, 'Iodinated contrast · non-ionic iso-osmolality', ['Parenteral']),
 'iopamidol': ('Iopamidol', ['Isovue', 'Iopamiro'], CM, 'Iodinated contrast · non-ionic low-osmolality', ['Parenteral']),
 'ioversol': ('Ioversol', ['Optiray'], CM, 'Iodinated contrast · non-ionic low-osmolality', ['Parenteral']),
 'iopromide': ('Iopromide', ['Ultravist'], CM, 'Iodinated contrast · non-ionic low-osmolality', ['Parenteral']),
 'alprazolam': ('Alprazolam', ['Xanax'], 'Psychiatry', 'Benzodiazepine', ['Oral']),
 'penicillamine': ('Penicillamine', ['Cuprimine', 'Depen'], 'Urology & other medicines', 'Chelating agent', ['Oral']),
 'droxidopa': ('Droxidopa', ['Northera'], 'Cardiovascular', 'Noradrenaline prodrug', ['Oral']),
 'alemtuzumab': ('Alemtuzumab', ['Lemtrada', 'Campath'], TI, 'Anti-CD52 monoclonal antibody', ['Parenteral']),
 'thiamine': ('Thiamine (IV/IM)', ['Vitamin B1'], 'Urology & other medicines', 'Vitamin', ['Parenteral']),
})
for i, (name, al, cat, cls, routes) in list(NEW.items()):
    LAB.setdefault(i, f'us3/{i}.json')
for i in ('antithymocyte-globulin-rabbit', 'intravenous-immunoglobulin'): LAB[i] = f'us3/{i}.json'

# -------- Oncology --------
P_('ifosfamide', 'Ifosfamide', 'caution', 'Renal function', 'Accumulates in renal impairment: monitor closely for toxicity and consider dose reduction; itself nephrotoxic. Dialysable.',
   M('specialist', notes='No numeric renal dose in the label. Ifosfamide is itself nephrotoxic (glomerular and tubular): weigh risk and benefit in pre-existing renal impairment and check renal function before, during and after treatment.',
     ev=['Patients with renal impairment should be closely monitored for toxicity and dose reduction may be considered', 'Glomerular and tubular kidney function must be evaluated before commencement of therapy as well as during and after treatment', 'The risk and expected benefits of ifosfamide therapy should be carefully weighed when considering the use of ifosfamide in patients with preexisting renal impairment or reduced nephron reserve']),
   ihd=M('specialist', notes='Ifosfamide and its metabolites are dialysable; no dialysis dose is given in the label.', ev=['Ifosfamide as well as ifosfamide metabolites are dialyzable']))
P_('mesna', 'MESNEX', 'monitor', 'No renal statement in the US label', 'No renal pharmacokinetic studies; dose is tied to the ifosfamide regimen.',
   M('specialist', notes='No renal studies; mesna is given as a fixed proportion of the ifosfamide dose.', ev=['No clinical studies were conducted to evaluate the effect of renal impairment on the pharmacokinetics of MESNEX']))
P_('cytarabine', 'Cytarabine injection', 'caution', 'Renal function', 'Use with caution and possibly at reduced dose when kidney function is poor; check renal function periodically.',
   M('specialist', notes='No numeric renal dose in this label.', ev=['Use the drug with caution and possibly at reduced dose in patients whose liver or kidney function is poor', 'Periodic checks of bone marrow, liver and kidney functions should be performed in patients receiving Cytarabine Injection']))
P_('fludarabine', 'Fludarabine phosphate injection', 'adjust', 'CrCl · mL/min/1.73 m²', 'CrCl 30–70: reduce dose by 20%; CrCl <30: do not give.',
   S('All indications · US label', [('CrCl 30–70 mL/min/1.73 m²', 'Reduce dose by 20% and monitor closely'), ('CrCl <30 mL/min/1.73 m²', 'Do not administer')],
     ['Adult patients with moderate impairment of renal function (creatinine clearance 30 to 70 mL/min/1.73 m 2 ) should have a 20% dose reduction of Fludarabine Phosphate Injection, USP', 'Fludarabine Phosphate Injection, USP should not be administered to patients with severely impaired renal function (creatinine clearance less than 30 mL/min/1.73 m 2 )']),
   ihd=M('avoid', notes='Not recommended in severely impaired renal function.', ev=['Fludarabine is not recommended for patients with severely impaired renal function (creatinine clearance less than 30 mL/min/1.73 m 2 )']))
P_('cladribine', 'Cladribine injection', 'caution', 'CrCl · mL/min', 'IV: proceed carefully in renal insufficiency (nephrotoxic at high doses). Oral (Mavenclad): no adjustment at CrCl 60–89; experience below 60 limited.',
   M('specialist', notes='IV cladribine: no numeric renal dose; acute renal insufficiency has occurred at high doses. Oral cladribine (Mavenclad, MS): see the second label.',
     ev=['In view of the known toxicities of agents of this class, it would be prudent to proceed carefully in patients with known or suspected renal insufficiency or severe bone marrow impairment of any etiology', 'Development of acute renal insufficiency in some patients receiving high doses of cladribine has been described', '2|No dosage adjustment is recommended in patients with mild renal impairment (creatinine clearance 60 to 89 mL per minute)', '2|Clinical experience in patients with moderate to severe renal impairment (i.e., CL CR below 60 mL per minute) is limited']),
   ihd=M('specialist', notes='Removal by dialysis is unknown (IV label) and unlikely to be significant (oral label).', ev=['It is not known whether the drug can be removed from the circulation by dialysis or hemofiltration', '2|Because of the rapid and extensive intracellular and tissue distribution, hemodialysis is unlikely to eliminate cladribine to a significant extent']))
C['cladribine'].update(label2='us3/cladribine-oral.json', brand2='MAVENCLAD')
P_('bendamustine', 'BENDEKA', 'caution', 'CrCl · mL/min', 'Do not use at CrCl <30; no meaningful PK change at CrCl ≥30.',
   S('CLL / NHL · US label', [('CrCl ≥30 mL/min', 'No clinically meaningful PK effect; usual dose'), ('CrCl <30 mL/min', 'Do not use')],
     ['Do not use BENDEKA in patients with creatinine clearance (CLcr) < 30 mL/min', 'No clinically meaningful effects on the pharmacokinetics of bendamustine were observed based on age (31 to 84 years), sex, mild to moderate renal impairment (CLcr ≥ 30 mL/min)']),
   ihd=M('avoid', notes='Not for use at CrCl <30 mL/min.', ev=['Do not use BENDEKA in patients with creatinine clearance (CLcr) < 30 mL/min']))
P_('busulfan', 'Busulfan injection', 'monitor', 'No renal statement in the US label', NOREN + ' One report of dialysability (overdose).',
   M('specialist', notes=NOREN), ihd=M('specialist', notes='One report describes busulfan as dialysable; dialysis may be considered in overdose.', ev=['There is one report that busulfan is dialyzable, thus dialysis should be considered in the case of overdose']))
P_('topotecan', 'Topotecan injection', 'adjust', 'CrCl · mL/min (Cockcroft–Gault, ideal body weight)', 'CrCl 20–39: 0.75 mg/m²/day; CrCl ≥40: no adjustment.',
   S('IV topotecan · US label', [('CrCl ≥40 mL/min', 'No dose adjustment (1.5 mg/m²/day × 5 days)'), ('CrCl 20–39 mL/min', '0.75 mg/m²/day')],
     ['Reduce the dose of Topotecan Injection to 0.75 mg/m 2 /day for patients with creatinine clearance (CLcr) of 20 to 39 mL/min (calculated with the Cockcroft-Gault method using ideal body weight)', 'No dosage adjustment is recommended for patients with CLcr greater than or equal to 40 mL/min']))
P_('irinotecan', 'CAMPTOSAR', 'caution', 'Renal function', 'Not evaluated in renal impairment; use caution. AKI reported with volume depletion from diarrhoea or vomiting.',
   M('specialist', notes='No renal dose; renal impairment has not been studied.', ev=['The influence of renal impairment on the pharmacokinetics of irinotecan has not been evaluated', 'Therefore, use caution in patients with impaired renal function', 'Renal impairment and acute renal failure have been identified, usually in patients who became volume depleted from severe vomiting and/or diarrhea']))
P_('vinorelbine', 'Vinorelbine injection', 'monitor', 'No renal statement in the US label', NOREN, M('specialist', notes=NOREN))
P_('temozolomide', 'TEMODAR', 'no_adjust', 'CrCl · mL/min/m²', 'No adjustment at CrCl 36–130 mL/min/m²; dose not established below 36 or on dialysis.',
   S('All indications · US label', [('CrCl 36–130 mL/min/m²', 'No dose adjustment'), ('CrCl <36 mL/min/m²', 'Dose not established')],
     ['No dosage adjustment is recommended for patients with creatinine clearance (CLcr) of 36 to 130 mL/min/m 2', 'The recommended dose of TEMODAR has not been established for patients with severe renal impairment (CLcr <36 mL/min/m 2 ) or for patients with end-stage renal disease on dialysis']),
   ihd=M('insufficient_data', notes='Dose not established on dialysis.', ev=['The recommended dose of TEMODAR has not been established for patients with severe renal impairment (CLcr <36 mL/min/m 2 ) or for patients with end-stage renal disease on dialysis']))
P_('azacitidine', 'Azacitidine for injection', 'monitor', 'Serum creatinine / BUN', 'Monitor creatinine each cycle; unexplained rise in BUN or creatinine → delay and give 50% dose next course.',
   S('MDS · US label', [('Unexplained rise in BUN or serum creatinine', 'Delay next cycle until values return to normal or baseline; reduce dose by 50% for the next course')],
     ['If unexplained elevations of BUN or serum creatinine occur, delay the next cycle until values return to normal or baseline and reduce the dose by 50% for the next course', 'Monitor patients with renal impairment for toxicity since azacitidine and its metabolites are primarily excreted by the kidneys']))
P_('arsenic-trioxide', 'Arsenic trioxide', 'monitor', 'CrCl · mL/min', 'CrCl <30: exposure ≈48% higher — monitor frequently; a dose reduction may be warranted. Not studied on dialysis.',
   S('APL · US label', [('CrCl <30 mL/min', 'Monitor frequently for toxicity; dose reduction may be warranted')],
     ['Monitor patients with severe renal impairment (creatinine clearance [CL CR ] less than 30 mL/min) frequently for toxicity; a dose reduction may be warranted', 'However, in the severe renal impairment group, the mean AUC 0-INF for As III was approximately 48% higher than that in the normal group']),
   ihd=M('insufficient_data', notes='Not studied on dialysis.', ev=['The use of arsenic trioxide in patients on dialysis has not been studied']))
P_('leucovorin', 'VYKOURA', 'adjust', 'Serum creatinine and methotrexate level', 'Methotrexate rescue: dose and duration rise with creatinine rise or delayed methotrexate elimination (label table).',
   S('High-dose methotrexate rescue · US label', [('Serum creatinine up ≥50% at 24 h, or MTX >5 µM at 24 h / >0.9 µM at 48 h', '100 mg/m² IV every 3 hours until MTX <0.01 µM'), ('Creatinine up ≥100% at 24 h, or MTX ≥50 µM at 24 h / ≥5 µM at 48 h', '150 mg IV/IM every 3 hours until MTX <1 µM, then 15 mg every 3 hours until <0.05 µM'), ('Renal impairment (subsequent courses)', 'Extend rescue by 24 hours (14 doses over 84 hours)')],
     ['Increase the dosage of VYKOURA to 100 mg/m 2 intravenously every 3 hours if serum creatinine at 24-hours increases 50% or more compared to baseline the methotrexate level at 24-hours is greater than 5 micromolar (5 x 10 -6 M) the methotrexate level at 48-hours is greater than 0.9 micromolar (9 x 10 -7 M) Continue VYKOURA at the same dosage until the methotrexate level is less than 0.01 micromolar (1 x 10 -8 M)', 'Serum methotrexate level of 50 micromolar or more at 24 hours, or 5 micromolar or more at 48 hours after administration, OR 100% or greater increase in serum creatinine level at 24 hours after methotrexate administration (e.g., an increase from 0.5 mg/dL to a level of 1 mg/dL or more). 150 mg intravenously or intramuscularly every 3 hours, until methotrexate level is less than 1 micromolar; then 15 mg intravenously or intramuscularly every 3 hours until methotrexate level is less than 0.05 micromolar', 'Extend VYKOURA rescue for an additional 24 hours (total of 14 doses over 84 hours) in subsequent courses of methotrexate in patients with: Impaired methotrexate elimination including third-space fluid accumulation and inadequate hydration Renal impairment']))
P_('melphalan', 'Alkeran IV', 'caution', 'BUN / renal function', 'IV melphalan: consider dose reduction in renal insufficiency (trial protocol used 50% at BUN ≥30 mg/dL). Not removed by HD.',
   S('IV melphalan · US label', [('Renal insufficiency', 'Consider dose reduction'), ('BUN ≥30 mg/dL (trial protocol)', 'IV dose reduced by 50% in the trial')],
     ['Dose reduction should be considered in patients with renal insufficiency receiving IV melphalan', 'An association was noted between poor renal function and myelosuppression; consequently, an amendment to the protocol required a 50% reduction in IV melphalan dose if the BUN was ≥30 mg/dL']))

# -------- Transplant & immunology (catalog promotions + new) --------
P_('antithymocyte-globulin-rabbit', 'THYMOGLOBULIN', 'monitor', 'No renal statement in the US label', 'No renal dose; dose by weight with WBC/platelet-based reductions.',
   M('specialist', notes=NOREN + ' Reduce by half for WBC 2,000–3,000/mm³ or platelets 50,000–75,000/mm³ (label).', ev=['The THYMOGLOBULIN dose should be reduced by one-half if the white blood cell (WBC) count is between 2,000 and 3,000 cells/mm 3 or if the platelet count is between 50,000 and 75,000 cells/mm 3']))
P_('intravenous-immunoglobulin', 'PRIVIGEN', 'caution', 'Renal risk factors', 'Renal dysfunction and AKI can occur: ensure euvolaemia and use the minimum dose and infusion rate practicable in at-risk patients.',
   M('specialist', notes='Boxed warning: renal dysfunction, AKI and thrombosis. Risk factors include any pre-existing renal insufficiency, diabetes, age >65, volume depletion, sepsis, paraproteinaemia and nephrotoxic drugs.',
     ev=['Patients predisposed to renal dysfunction include those with any degree of pre-existing renal insufficiency, diabetes mellitus, age greater than 65, volume depletion, sepsis, paraproteinemia, or patients receiving known nephrotoxic drugs', 'Ensure that patients with pre-existing renal insufficiency are not volume depleted', 'For patients judged to be at risk for renal dysfunction or thrombosis, administer PRIVIGEN at the minimum dose and infusion rate practicable, and discontinue PRIVIGEN administration if renal function deteriorates']))
P_('alemtuzumab', 'LEMTRADA', 'monitor', 'Serum creatinine and urinalysis', 'No renal dose; monitor creatinine and urinalysis monthly (anti-GBM disease risk) until 48 months after the last dose.',
   M('specialist', notes=NOREN + ' Monthly creatinine and urinalysis are part of the label monitoring.', ev=['Monitor complete blood counts with differential, serum creatinine levels, and urinalysis with urine cell counts before starting treatment and then at monthly intervals until 48 months after the last dose of LEMTRADA']))

# -------- Anaesthesia & critical care --------
P_('rocuronium', 'Rocuronium bromide injection', 'no_adjust', 'No renal dose adjustment (US label)', 'Usual dosing in renal impairment; duration similar but more variable in ESRD.',
   S('Neuromuscular blockade · US label', [('Renal impairment, including ESRD', 'Usual dosing; expect similar but more variable duration')],
     ['Due to the limited role of the kidney in the excretion of rocuronium bromide, usual dosing recommendations Rocuronium Bromide Injection for should be followed', 'The net result of these findings is that subjects with renal failure have clinical durations that are similar to but somewhat more variable than the duration that one would expect in subjects with normal renal function']))
P_('cisatracurium', 'Cisatracurium besylate', 'no_adjust', 'ESRD', 'ESRD: onset ≈1 min slower — allow at least 1 extra minute before intubation; recovery unchanged.',
   S('Neuromuscular blockade · US label', [('End-stage renal disease', 'Usual dose; wait at least 1 minute longer before intubation')],
     ['There was no clinically significant alteration in the recovery profile of Cisatracurium Besylate Injection in patients with end-stage renal disease following a 0.1 mg/kg dose', 'consider extending the interval between administering Cisatracurium Besylate Injection and attempting intubation by at least 1 minute to achieve adequate intubation conditions in geriatric patients and patients with end-stage renal disease']))
P_('succinylcholine', 'QUELICIN', 'caution', 'Severe kidney disease', 'Plasma cholinesterase may be reduced in severe kidney disease (prolonged block). Hyperkalaemia risk applies.',
   M('specialist', notes='No renal dose. Severe kidney disease can lower plasma cholinesterase activity.', ev=['Plasma cholinesterase activity may be diminished in the presence of genetic abnormalities of plasma cholinesterase (e.g., patients heterozygous or homozygous for atypical plasma cholinesterase gene), pregnancy, severe liver or kidney disease']))
P_('neostigmine', 'BLOXIVERZ', 'monitor', 'Renal function', 'No dose adjustment, but half-life is prolonged in anephric patients — monitor that the blocker does not outlast reversal.',
   S('NMB reversal · US label', [('Renal impairment', 'No adjustment; monitor closely for persistent neuromuscular block')],
     ['Although no adjustments to BLOXIVERZ dosing appear to be warranted in patients with impaired renal function, they should be closely monitored to assure the effects of the neuromuscular blocking agent, particularly one cleared by the kidneys, do not persist beyond those of BLOXIVERZ']))
P_('sugammadex', 'BRIDION', 'caution', 'CrCl · mL/min', 'Not recommended at CrCl <30 or on dialysis; exposure up to 17-fold higher. High-flux HD removes ≈70%.',
   S('NMB reversal · US label', [('CrCl 30–80 mL/min', 'Usual dose'), ('CrCl <30 mL/min, including dialysis', 'Not recommended')],
     ['BRIDION is not recommended for use in patients with severe renal impairment (creatinine clearance <30 mL/min) due to insufficient safety information combined with the prolonged and increased overall exposure in these patients', 'Effect of mild or moderate renal impairment (creatinine clearance ≥30 and ≤80 mL/min) on sugammadex PK and PD was obtained from a study in elderly patients']),
   ihd=M('avoid', notes='Not recommended on dialysis. High-flux (not low-flux) HD lowers plasma levels by about 70% per 3–6 h session.', ev=['BRIDION is not recommended for use in patients with severe renal impairment, including those requiring dialysis', 'BRIDION can be removed using hemodialysis with a high-flux filter, but not with a low-flux filter']))
P_('bupivacaine', 'MARCAINE', 'caution', 'Renal function', 'Renally excreted metabolites: greater risk of adverse reactions in renal impairment; no numeric dose change.',
   M('specialist', notes='No numeric renal dose; renal disease can alter local anaesthetic pharmacokinetics.', ev=['This product is known to be substantially excreted by the kidney, and the risk of adverse reactions to this drug may be greater in patients with impaired renal function', 'Various pharmacokinetic parameters of the local anesthetics can be significantly altered by the presence of renal disease, factors affecting urinary pH, and renal blood flow']))
P_('flumazenil', 'Flumazenil injection', 'no_adjust', 'CrCl <10 mL/min and haemodialysis', 'Pharmacokinetics not significantly affected in renal failure or haemodialysis.',
   S('Benzodiazepine reversal · US label', [('CrCl <10 mL/min or haemodialysis', 'No significant PK change; usual dose')], ['Renal Failure (creatinine clearance <10 mL/min) and Hemodialysis The pharmacokinetics of flumazenil are not significantly affected']),
   ihd=HDT([('Haemodialysis', 'Usual dose (PK not significantly affected)')], ['Renal Failure (creatinine clearance <10 mL/min) and Hemodialysis The pharmacokinetics of flumazenil are not significantly affected']))
P_('mannitol', 'Mannitol injection', 'caution', 'Renal function and urine output', 'Pre-existing renal disease raises AKI risk; stop if renal function worsens. Anuria during treatment → risk of heart failure and pulmonary oedema. Dialysable.',
   M('specialist', notes='Evaluate renal status and correct fluid and electrolytes first; monitor urine output.', ev=['Patients with pre-existing renal disease, patients with conditions that put them at high risk for renal failure, or those receiving potentially nephrotoxic drugs or other diuretics, are at increased risk of renal failure with administration of mannitol', 'Monitor renal function closely, including signs of urine output reduction, during mannitol injection', 'Patients with oliguric acute kidney injury who subsequently develop anuria while receiving mannitol are at risk of congestive heart failure, pulmonary edema, hypertensive crisis, coma, and death']),
   ihd=M('specialist', notes='Dialysable by HD and PD; HD may increase elimination.', ev=['Mannitol Injection is dialyzable (hemodialysis and peritoneal dialysis), hemodialysis may increase mannitol elimination']))
P_('albumin-human', 'ALBUMINEX', 'caution', 'Volume status', 'Renal dialysis: initial dose should not exceed 25 g; watch for fluid overload.',
   S('Hypovolaemia / dialysis · US label', [('Renal dialysis', 'Initial dose not more than 25 g; observe for fluid overload')], ['For renal dialysis; the initial dose should not exceed 25 g and patients should be carefully observed for signs of fluid overload']),
   ihd=HDT([('Haemodialysis', 'Initial dose ≤25 g; observe for fluid overload')], ['For renal dialysis; the initial dose should not exceed 25 g and patients should be carefully observed for signs of fluid overload']))
P_('terlipressin', 'TERLIVAZ', 'caution', 'Serum creatinine', 'Hepatorenal syndrome: dose by SCr trajectory (label chart); patients with SCr >5 mg/dL are unlikely to benefit.',
   M('specialist', notes='Record baseline SCr and assess on day 4 per the label dosing chart; check ACLF grade, volume status and oxygenation first.', ev=['Patients with a serum creatinine >5 mg/dL are unlikely to experience benefit', 'Record last available serum creatinine (SCr) value prior to initiating treatment (baseline SCr)', 'Day 4: Assess serum creatinine (SCr) versus baseline']))

# -------- Contrast media --------
GBCA2 = 'ACR group II (very low NSF risk). ACR–NKF consensus: do not withhold or delay a needed group II agent where harm would result; kidney-function screening optional; dialysis need not be started or changed for the contrast; on maintenance HD, ideally give before a scheduled session.'
GBCA3 = 'ACR group III (limited data; no unconfounded NSF cases). ACR–NKF consensus: screen kidney function; at eGFR <30 or in AKI the radiologist and referring clinician should discuss the risk; dialysis need not be started or changed for the contrast.'
GBCA1 = 'ACR group I (greatest number of NSF cases). Prefer a group II agent in advanced CKD, AKI or dialysis.'
def gbca(i, brand, quotes, hd_quote, group_note, flag='caution', status='summarized', dose_rows=None, extra_ev=()):
    rows = dose_rows or [('eGFR ≥30, no AKI', 'Usual dose'), ('eGFR <30 or AKI', 'Highest NSF risk: avoid unless essential and not available from non-contrast MRI or other modalities; do not exceed the recommended dose; allow time for elimination before re-dosing')]
    P_(i, brand, flag, 'eGFR · mL/min/1.73 m²', group_note.split('.')[0] + '. Label: highest NSF risk at GFR <30 or AKI.',
       M(status, [T('MRI contrast · US label', rows)], '', list(quotes) + list(extra_ev)),
       ihd=HDT([('Haemodialysis', 'Consider prompt HD after the dose to speed elimination (label)')] if hd_quote else [('Haemodialysis', 'Removed by HD (label)')], [hd_quote] if hd_quote else []),
       considerations=group_note)
    C[i]['extraSources'] = ['acr-nkf-gbcm-2021', 'acr-contrast-manual']
NSF_Q = 'The risk for NSF appears highest among patients with: Chronic, severe kidney disease (GFR < 30 mL/min/1.73m 2 ), or Acute kidney injury'
gbca('gadobutrol', 'GADAVIST', [NSF_Q, 'For patients at highest risk for NSF, do not exceed the recommended GADAVIST dose and allow a sufficient period of time for elimination of the drug from the body prior to any re-administration'],
     "For patients receiving hemodialysis, consider the prompt initiation of hemodialysis following the administration of a GBCA in order to enhance the contrast agent's elimination", GBCA2)
gbca('gadoterate', 'DOTAREM', ['The risk for NSF appears highest among patients with: Chronic, severe kidney disease (GFR < 30 mL/min/1.73 m 2 ), or Acute kidney injury', 'No DOTAREM dosage adjustment is recommended for patients with renal impairment'],
     None, GBCA2)
C['gadoterate']['modalities']['ihd']['ev'] = ['Gadoterate meglumine can be removed from the body by hemodialysis']
gbca('gadoteridol', 'ProHance', ['The risk for NSF appears highest among patients with: chronic, severe kidney disease (GFR less than 30 mL/min/1.73m 2 ), or acute kidney injury', 'No ProHance dosage adjustment is recommended for patients with renal impairment'], None, GBCA2)
C['gadoteridol']['modalities']['ihd']['ev'] = ['ProHance can be removed by hemodialysis']
gbca('gadobenate', 'MultiHance', ['The risk for NSF appears highest among patients with: chronic, severe kidney disease (GFR <30 mL/min/1.73m 2 ), or acute kidney injury'], None, GBCA2)
C['gadobenate']['modalities'].pop('ihd')
gbca('gadopiclenol', 'ELUCIREM', ['The risk for NSF appears highest among patients with: Chronic, severe kidney disease (GFR < 30 mL/min/1.73 m 2 ), or Acute kidney injury', 'No dose adjustment of ELUCIREM is recommended for patients with renal impairment'], None, GBCA2)
C['gadopiclenol']['modalities']['ihd']['ev'] = ['ELUCIREM can be removed from the body by hemodialysis']
gbca('gadoxetate', 'EOVIST', [NSF_Q, 'For patients at highest risk for NSF, do not exceed the recommended EOVIST dose and allow a sufficient period of time for elimination of the drug from the body prior to any re-administration'],
     "For patients receiving hemodialysis, consider the prompt initiation of hemodialysis following the administration of a GBCA in order to enhance the contrast agent's elimination", GBCA3)
gbca('gadodiamide', 'OMNISCAN', ['Do not administer OMNISCAN to patients with: chronic, severe kidney disease (GFR < 30 mL/min/1.73m 2 ), or acute kidney injury', 'Do not exceed the recommended OMNISCAN dose and allow a sufficient period of time for elimination of the drug from the body prior to any readministration'],
     None, GBCA1, flag='caution', status='avoid', dose_rows=[('eGFR ≥30, no AKI', 'Usual dose; do not exceed it'), ('eGFR <30 or AKI', 'Contraindicated')])
C['gadodiamide']['modalities']['ihd'] = M('avoid', notes='Contraindicated in chronic severe kidney disease, which includes dialysis; dialysable.', ev=['Do not administer OMNISCAN to patients with: chronic, severe kidney disease (GFR < 30 mL/min/1.73m 2 ), or acute kidney injury', 'OMNISCAN is dialyzable'])
C['gadodiamide']['modalities']['ckd']['status'] = 'summarized'

ICM = 'ACR–NKF consensus (IV contrast): high risk = AKI or eGFR <30 (includes non-anuric dialysis patients). Give IV isotonic saline prophylaxis at eGFR <30 or AKI unless contraindicated (e.g. heart failure); optional at 30–44 in individual high-risk cases; not indicated at ≥45. Do not withhold a necessary study; use the standard diagnostic dose; withhold nonessential nephrotoxic drugs when feasible; dialysis should not be started or changed solely because of the contrast. Use the contrast-AKI calculator for the risk estimate.'
def icm(i, brand, risk_q, low_q, hd_q):
    P_(i, brand, 'caution', 'eGFR · mL/min/1.73 m²', 'Pre-existing renal impairment raises AKI risk: use the lowest necessary dose. ACR–NKF: high risk at eGFR <30 or AKI.',
       M('specialist', notes='No numeric renal dose in the label; AKI risk factors are listed.', ev=[risk_q, low_q]),
       ihd=M('specialist', notes='Removed by dialysis; dialysis need not be timed to the contrast (ACR–NKF).', ev=[hd_q]),
       considerations=ICM)
    C[i]['extraSources'] = ['acr-nkf-icm-2020']
RF = 'Risk factors include: pre-existing renal impairment, dehydration, diabetes mellitus, congestive heart failure, advanced vascular disease, elderly age, concomitant use of nephrotoxic or diuretic medications, multiple myeloma/paraproteinaceous diseases, repetitive and/or large doses of an iodinated contrast agent'
icm('iohexol', 'OMNIPAQUE', RF, 'Use the lowest necessary dose of OMNIPAQUE in patients with renal impairment', 'Iohexol can be removed by dialysis')
icm('iodixanol', 'VISIPAQUE', RF, 'Use the lowest necessary dose of VISIPAQUE in patients with renal impairment', 'VISIPAQUE Injection does not bind to plasma or serum protein and can be dialyzed')
icm('iopamidol', 'ISOVUE', 'Risk factors include: pre-existing renal insufficiency, dehydration, diabetes mellitus, congestive heart failure, advanced vascular disease, elderly age, concomitant use of nephrotoxic or diuretic medications, multiple myeloma or other paraproteinemias, and repetitive or large doses of ISOVUE', 'Use the lowest necessary dose of ISOVUE in patients with renal impairment', 'Iopamidol can be removed by dialysis')
icm('ioversol', 'OPTIRAY', 'Risk factors include: pre-existing renal impairment, dehydration, diabetes mellitus, congestive heart failure, advanced vascular disease, elderly age, concomitant use of nephrotoxic or diuretic medications, multiple myeloma / paraproteinaceous diseases, repetitive and/or large doses of an iodinated contrast agent', 'Use the lowest necessary dose of OPTIRAY in patients with renal impairment', 'Ioversol can be removed by dialysis')
icm('iopromide', 'ULTRAVIST', 'Risk factors include: pre-existing renal insufficiency, dehydration, diabetes mellitus, congestive heart failure, advanced vascular disease, elderly age, concomitant use of nephrotoxic or diuretic medications, multiple myeloma or other paraproteinemia, and repetitive and/or large doses of ULTRAVIST', 'Use the lowest necessary dose of ULTRAVIST in patients with renal impairment', 'Iopromide can be removed by dialysis')

# -------- Others --------
P_('alprazolam', 'XANAX', 'monitor', 'No renal statement in the US label', NOREN, M('specialist', notes=NOREN))
P_('penicillamine', 'CUPRIMINE', 'caution', 'Renal function', 'RA: do not use with renal insufficiency (nephrotoxic). Renally excreted — monitor renal function.',
   M('specialist', notes='No numeric renal dose; penicillamine can cause renal damage.', ev=['Because of its potential for causing renal damage, penicillamine should not be administered to rheumatoid arthritis patients with a history or other evidence of renal insufficiency', 'This drug is known to be substantially excreted by the kidney, and the risk of toxic reactions to this drug may be greater in patients with impaired renal function']))
P_('droxidopa', 'NORTHERA', 'caution', 'GFR · mL/min', 'No change at GFR >30; dosing cannot be recommended at GFR <30 (renally cleared).',
   S('Neurogenic orthostatic hypotension · US label', [('GFR >30 mL/min', 'Usual dose (no excess adverse reactions in trials)'), ('GFR <30 mL/min', 'Dosing recommendations cannot be provided')],
     ['Patients with mild or moderate renal impairment (GFR greater than 30 mL/min) were included in clinical trials and did not have a higher frequency of adverse reactions', 'Dosing recommendations cannot be provided for patients with GFR less than 30 mL/min']))
P_('thiamine', 'Thiamine hydrochloride injection', 'monitor', 'Renal function', 'No renal dose; aluminium can accumulate with prolonged parenteral use when kidney function is impaired.',
   M('specialist', notes=NOREN, ev=['Aluminum may reach toxic levels with prolonged parenteral administration if kidney function is impaired']))
