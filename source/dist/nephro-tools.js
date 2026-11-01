'use strict';
// v0.21 nephrology calculators: one dialog (#nephro-tools) hosts every calculator defined below.
// Arithmetic lives in nephro-math.js. Inputs clear when the panel closes; nothing is stored or sent.
const NephroTools = (() => {
  const M = NephroMath;
  const f = (x, d = 1) => Number(x).toFixed(d);
  const sexSel = ['sel', 'sex', 'Sex', [['', 'Choose…'], ['female', 'Female'], ['male', 'Male']]];
  const age = ['num', 'age', 'Age · years', '18–110'], weight = ['num', 'weight', 'Weight · kg', '25–300'];
  const gluUnit = ['sel', 'gluUnit', 'Glucose unit', [['mgdl', 'mg/dL'], ['mmol', 'mmol/L']]];
  const tbwNote = a => `Total body water ${f(a.tbw)} L (${f(a.fraction * 100, 0)}% of body weight).`;
  const out = (label, number, unit, body, cls = '') => `<div class="calc-output${cls}"><div class="calc-output-label">${label}</div>${number !== null ? `<div class="calc-number">${number} <span>${unit}</span></div>` : ''}${body}</div>`;
  const C = {
    'na-glucose': {group: 'Electrolytes & acid–base', title: 'Sodium corrected for glucose', sub: 'Hyperglycaemia · Katz and Hillier factors',
      fields: [['num', 'na', 'Measured sodium · mmol/L', '100–180'], ['num', 'glucose', 'Glucose', 'value'], gluUnit],
      run: M.naGlucose,
      render: a => out('Corrected sodium', f(a.hillier), 'mmol/L (Hillier, 2.4)', `<p>Katz (1.6 per 100 mg/dL): ${f(a.katz)} mmol/L. Glucose ${f(a.glucoseMgDl, 0)} mg/dL.${a.below ? ' Glucose ≤100 mg/dL: no correction applies.' : ''} Hillier found 2.4 mmol/L per 100 mg/dL a better overall estimate, especially above 400 mg/dL.</p>`),
      method: 'Corrected Na = measured Na + factor × (glucose mg/dL − 100) ÷ 100; factor 1.6 (Katz) or 2.4 (Hillier). Glucose mmol/L × 18.016 = mg/dL.',
      sources: [['Katz MA. Hyperglycemia-induced hyponatremia — calculation of expected serum sodium depression. N Engl J Med 1973;289:843–4', 'https://doi.org/10.1056/NEJM197310182891607'], ['Hillier TA et al. Hyponatremia: evaluating the correction factor for hyperglycemia. Am J Med 1999;106:399–403', 'https://doi.org/10.1016/S0002-9343(99)00055-8']]},
    'hyponatremia': {group: 'Electrolytes & acid–base', title: 'Hyponatraemia: infusate effect', sub: 'Adrogué–Madias · change per litre · volume for a 6–8 mmol/L rise',
      fields: [['num', 'na', 'Serum sodium · mmol/L', '90–135'], sexSel, age, weight,
        ['sel', 'infusate', 'Infusate', [['', 'Choose…'], ['nacl3', '3% NaCl (Na 513)'], ['nacl09', '0.9% NaCl (Na 154)'], ['nacl045', '0.45% NaCl (Na 77)'], ['rl', 'Ringer’s lactate (Na 130, K 4)'], ['d5w', '5% dextrose (Na 0)'], ['custom', 'Custom…']]],
        ['num', 'infNa', 'Custom infusate Na · mmol/L', 'if custom'], ['num', 'infK', 'Custom infusate K · mmol/L', 'if custom']],
      run: M.hyponatremia,
      render: a => out(`${a.infusate.name} · per litre`, (a.perLitre >= 0 ? '+' : '') + f(a.perLitre), 'mmol/L expected change',
        `<p>${tbwNote(a)}</p>${a.perLitre > 0 ? `<table class="calc-crcl-table"><tbody><tr><th scope="row">Volume for a 6 mmol/L rise</th><td>${f(a.litresFor6 * 1000, 0)} mL</td></tr><tr><th scope="row">Volume for an 8 mmol/L rise</th><td>${f(a.litresFor8 * 1000, 0)} mL</td></tr></tbody></table>` : '<p>This infusate will not raise the serum sodium.</p>'}`
        + '<p><strong>Limits:</strong> chronic hyponatraemia — do not exceed 10 mmol/L in the first 24 h and 8 mmol/L in any later 24 h (European guideline); 8 mmol/L in 24 h when the risk of osmotic demyelination is high (US expert panel). The formula ignores ongoing losses, urine output and aquaresis: recheck sodium every 2–4 hours.</p>', a.perLitre > 10 ? ' ca-high' : ''),
      method: 'Change in serum Na per litre = (infusate Na + infusate K − serum Na) ÷ (total body water + 1). Total body water = weight × 0.6 (men <65), 0.5 (women <65; men ≥65), 0.45 (women ≥65).',
      sources: [['Adrogué HJ, Madias NE. Hyponatremia. N Engl J Med 2000;342:1581–9', 'https://doi.org/10.1056/NEJM200005253422107'], ['Spasovski G et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia. Nephrol Dial Transplant 2014;29 Suppl 2:i1–39', 'https://doi.org/10.1093/ndt/gfu040'], ['Verbalis JG et al. Diagnosis, evaluation, and treatment of hyponatremia: expert panel recommendations. Am J Med 2013;126(10 Suppl 1):S1–42', 'https://doi.org/10.1016/j.amjmed.2013.07.006']]},
    'free-water': {group: 'Electrolytes & acid–base', title: 'Free water deficit', sub: 'Hypernatraemia',
      fields: [['num', 'na', 'Serum sodium · mmol/L', '141–200'], ['num', 'target', 'Target sodium · mmol/L (optional, default 140)', '130–150'], sexSel, age, weight],
      run: M.freeWater,
      render: a => out('Free water deficit', f(a.deficit), 'L', `<p>${tbwNote(a)} Target ${f(a.target, 0)} mmol/L.</p><p>Add ongoing losses. In chronic hypernatraemia aim for a fall of no more than 10 mmol/L in 24 hours (Adrogué–Madias).</p>`),
      method: 'Deficit = total body water × (serum Na ÷ target Na − 1). Total body water as for hyponatraemia.',
      sources: [['Adrogué HJ, Madias NE. Hypernatremia. N Engl J Med 2000;342:1493–9', 'https://doi.org/10.1056/NEJM200005183422006']]},
    'calcium': {group: 'Electrolytes & acid–base', title: 'Calcium corrected for albumin', sub: 'Payne formula',
      fields: [['num', 'ca', 'Total calcium', 'value'], ['num', 'alb', 'Albumin', 'value'], ['sel', 'caUnit', 'Units', [['mgdl', 'mg/dL and g/dL'], ['mmol', 'mmol/L and g/L']]]],
      run: M.correctedCalcium,
      render: a => out('Corrected calcium', a.si ? f(a.mmol, 2) : f(a.mgdl, 2), a.si ? 'mmol/L' : 'mg/dL', `<p>= ${a.si ? f(a.mgdl, 2) + ' mg/dL' : f(a.mmol, 2) + ' mmol/L'}. In CKD, dialysis and critical illness albumin correction is unreliable; KDIGO CKD-MBD prefers measured ionised calcium when the decision matters.</p>`),
      method: 'Corrected Ca (mg/dL) = Ca + 0.8 × (4.0 − albumin g/dL); SI: Ca (mmol/L) + 0.02 × (40 − albumin g/L).',
      sources: [['Payne RB et al. Interpretation of serum calcium in patients with abnormal serum proteins. BMJ 1973;4:643–6', 'https://doi.org/10.1136/bmj.4.5893.643'], ['KDIGO 2017 CKD-MBD guideline update', 'https://kdigo.org/guidelines/ckd-mbd/']]},
    'osmolal-gap': {group: 'Electrolytes & acid–base', title: 'Serum osmolality & osmolal gap', sub: 'Toxic alcohols · ethanol term optional',
      fields: [['num', 'na', 'Sodium · mmol/L', '100–200'], ['num', 'glucose', 'Glucose', 'value'], gluUnit, ['num', 'urea', 'BUN or urea', 'value'], ['sel', 'ureaUnit', 'Urea unit', [['mgdl', 'BUN mg/dL'], ['mmol', 'urea mmol/L']]],
        ['num', 'measured', 'Measured osmolality · mOsm/kg (optional)', '200–500'], ['num', 'ethanol', 'Ethanol (optional)', 'value'], ['sel', 'etohUnit', 'Ethanol unit', [['mgdl', 'mg/dL'], ['mmol', 'mmol/L']]]],
      run: M.osmolalGap,
      render: a => out('Calculated osmolality', f(a.calculated, 0), 'mOsm/kg', a.gap === null ? '<p>Enter a measured osmolality to obtain the gap.</p>' : `<p><strong>Osmolal gap ${f(a.gap, 0)} mOsm/kg.</strong> ${a.gap > 10 ? 'Raised (>10): consider methanol, ethylene glycol, other alcohols, mannitol or contrast; ' : 'Not raised (≤10); '}a normal gap does not exclude toxic alcohol ingestion.${a.ethanolIncluded ? ' Ethanol included.' : ''}</p>`),
      method: 'Calculated = 2 × Na + glucose (mg/dL) ÷ 18 + BUN (mg/dL) ÷ 2.8 [+ ethanol (mg/dL) ÷ 3.7]; SI: 2 × Na + glucose + urea [+ ethanol] in mmol/L. Gap = measured − calculated.',
      sources: [['Purssell RA et al. Derivation and validation of a formula to calculate the contribution of ethanol to the osmolal gap. Ann Emerg Med 2001;38:653–9', 'https://doi.org/10.1067/mem.2001.119455']]},
    'anion-gap': {group: 'Electrolytes & acid–base', title: 'Anion gap, albumin correction & delta ratio', sub: 'Metabolic acidosis',
      fields: [['num', 'na', 'Sodium · mmol/L', '100–200'], ['num', 'cl', 'Chloride · mmol/L', '50–150'], ['num', 'hco3', 'Bicarbonate · mmol/L', '1–60'], ['num', 'alb', 'Albumin (optional)', 'value'], ['sel', 'albUnit', 'Albumin unit', [['gdl', 'g/dL'], ['gl', 'g/L']]], ['num', 'normal', 'Your laboratory’s normal anion gap (optional, default 12)', '3–20']],
      run: M.anionGap,
      render: a => out('Anion gap', f(a.ag), 'mmol/L', `${a.corrected !== null ? `<p>Albumin-corrected anion gap <strong>${f(a.corrected)}</strong> mmol/L.</p>` : ''}<p>${a.high ? 'Raised anion gap.' : 'Anion gap not raised against a normal of ' + f(a.normal, 0) + ' (±4).'}${a.delta !== null ? ` Delta ratio ${f(a.delta, 2)}${a.deltaNote ? ': ' + h(a.deltaNote) + '.' : '.'}` : ''}</p>`),
      method: 'Anion gap = Na − (Cl + HCO₃). Corrected = AG + 2.5 × (4.0 − albumin g/dL). Delta ratio = (AG − normal AG) ÷ (24 − HCO₃): <0.4 normal-gap acidosis; 0.4–1 mixed; 1–2 pure high-gap acidosis; >2 coexisting metabolic alkalosis. Normal ranges vary by analyser.',
      sources: [['Figge J et al. Anion gap and hypoalbuminemia. Crit Care Med 1998;26:1807–10', 'https://doi.org/10.1097/00003246-199811000-00019'], ['Rastegar A. Use of the ΔAG/ΔHCO3− ratio in the diagnosis of mixed acid-base disorders. J Am Soc Nephrol 2007;18:2429–31', 'https://doi.org/10.1681/ASN.2006121408']]},
    'winters': {group: 'Electrolytes & acid–base', title: 'Expected pCO₂ (Winter’s formula)', sub: 'Respiratory compensation for metabolic acidosis',
      fields: [['num', 'hco3', 'Bicarbonate · mmol/L', '1–30'], ['num', 'pco2', 'Measured pCO₂ · mmHg (optional)', '5–150']],
      run: M.winters,
      render: a => out('Expected pCO₂', `${f(a.low, 0)}–${f(a.high, 0)}`, 'mmHg', `<p>Midpoint ${f(a.expected, 1)} mmHg.${a.verdict ? ' Measured pCO₂ is ' + a.verdict + '.' : ''}</p>`),
      method: 'Expected pCO₂ = 1.5 × HCO₃ + 8 ± 2 mmHg (metabolic acidosis only).',
      sources: [['Albert MS, Dell RB, Winters RW. Quantitative displacement of acid-base equilibrium in metabolic acidosis. Ann Intern Med 1967;66:312–22', 'https://doi.org/10.7326/0003-4819-66-2-312']]},
    'fena': {group: 'AKI & proteinuria', title: 'FENa / FEUrea', sub: 'Pre-renal versus intrinsic AKI',
      fields: [['num', 'uCr', 'Urine creatinine', 'same unit as plasma'], ['num', 'pCr', 'Plasma creatinine', 'same unit as urine'], ['num', 'uNa', 'Urine sodium · mmol/L', 'for FENa'], ['num', 'pNa', 'Plasma sodium · mmol/L', 'for FENa'],
        ['num', 'uUrea', 'Urine urea', 'for FEUrea'], ['num', 'pUrea', 'Plasma urea', 'same unit as urine']],
      run: M.fractionalExcretion,
      render: a => out('Fractional excretion', null, '', `<table class="calc-crcl-table"><tbody>${a.fena !== null ? `<tr><th scope="row">FENa</th><td>${f(a.fena, 2)}% — ${a.fena < 1 ? '<1%: suggests pre-renal physiology' : a.fena > 2 ? '>2%: suggests intrinsic (tubular) injury' : '1–2%: indeterminate'}</td></tr>` : ''}${a.feurea !== null ? `<tr><th scope="row">FEUrea</th><td>${f(a.feurea, 1)}% — ${a.feurea < 35 ? '<35%: suggests pre-renal physiology' : a.feurea > 50 ? '>50%: suggests intrinsic injury' : '35–50%: indeterminate'}</td></tr>` : ''}</tbody></table><p>Interpret in oliguric AKI only. Diuretics raise FENa (FEUrea is less affected); contrast nephropathy, myoglobinuria, sepsis and early obstruction can give a low FENa.</p>`),
      method: 'FE (%) = (urine X × plasma creatinine) ÷ (plasma X × urine creatinine) × 100. Creatinine must be in the same unit in urine and plasma; likewise urea.',
      sources: [['Espinel CH. The FENa test: use in the differential diagnosis of acute renal failure. JAMA 1976;236:579–81', 'https://doi.org/10.1001/jama.1976.03270060029022'], ['Carvounis CP et al. Significance of the fractional excretion of urea in the differential diagnosis of acute renal failure. Kidney Int 2002;62:2223–9', 'https://doi.org/10.1046/j.1523-1755.2002.00683.x']]},
    'aki-stage': {group: 'AKI & proteinuria', title: 'KDIGO AKI stage', sub: 'Creatinine and urine output criteria',
      fields: [['num', 'base', 'Baseline creatinine', 'value'], ['num', 'cur', 'Current creatinine', 'value'], ['sel', 'crUnit', 'Creatinine unit', [['mgdl', 'mg/dL'], ['umol', 'µmol/L']]],
        ['num', 'uo', 'Urine output · mL/kg/h (optional)', '0–10'], ['num', 'uoHours', 'For how many hours (optional)', '1–72'], ['sel', 'rrt', 'Kidney replacement therapy started?', [['no', 'No'], ['yes', 'Yes']]]],
      run: M.akiStage,
      render: a => out('KDIGO AKI', a.stage ? 'Stage ' + a.stage : 'No AKI', a.stage ? '' : 'by these values', `<ul><li>Creatinine: ${h(a.crWhy)}${a.cr ? ' → stage ' + a.cr : ''}.</li>${a.uoWhy ? `<li>Urine output: ${h(a.uoWhy)}${a.uo ? ' → stage ' + a.uo : ''}.</li>` : ''}</ul><p>The higher of the two criteria sets the stage. The 0.3 mg/dL rise must occur within 48 hours and the 1.5-fold rise within 7 days.</p>`, a.stage >= 3 ? ' ca-high' : a.stage ? ' ca-intermediate' : ''),
      method: 'KDIGO 2012: stage 1 — creatinine 1.5–1.9 × baseline or ≥0.3 mg/dL (26.5 µmol/L) rise; urine <0.5 mL/kg/h for 6–12 h. Stage 2 — 2.0–2.9 ×; <0.5 mL/kg/h ≥12 h. Stage 3 — 3.0 ×, or creatinine ≥4.0 mg/dL (353.6 µmol/L), or start of KRT; <0.3 mL/kg/h ≥24 h or anuria ≥12 h.',
      sources: [['KDIGO 2012 clinical practice guideline for acute kidney injury', 'https://kdigo.org/guidelines/acute-kidney-injury/']]},
    'proteinuria': {group: 'AKI & proteinuria', title: 'Spot ratio → 24-hour estimate', sub: 'PCR/ACR unit conversion · KDIGO A category',
      fields: [['sel', 'kind', 'Measured', [['protein', 'Protein (PCR)'], ['albumin', 'Albumin (ACR)']]], ['sel', 'mode', 'Enter', [['ratio', 'Ratio'], ['raw', 'Spot urine values (mg/dL)']]],
        ['num', 'ratio', 'Ratio', 'value'], ['sel', 'unit', 'Ratio unit', [['mgmmol', 'mg/mmol'], ['mgg', 'mg/g'], ['gg', 'g/g (= mg/mg)']]], ['num', 'uProt', 'Urine protein or albumin · mg/dL', 'if spot values'], ['num', 'uCr', 'Urine creatinine · mg/dL', 'if spot values']],
      run: M.proteinuria,
      render: a => out(a.albumin ? 'Albumin–creatinine ratio' : 'Protein–creatinine ratio', f(a.mgG, 0), `mg/g · ${f(a.mgMmol, 1)} mg/mmol`, `<p>KDIGO ${a.cat}: ${a.catLabel}. Estimated excretion ≈ ${f(a.perDay, 2)} g/day${a.albumin ? ' of albumin' : ''}${a.nephrotic ? ' — nephrotic range (≥3.5 g/day)' : ''}.</p><p>The estimate assumes about 1 g of creatinine excreted per day; it underestimates in muscular people and overestimates in frail or sarcopenic people.</p>`),
      method: '1 mmol creatinine = 113.1 mg, so mg/mmol × 8.84 = mg/g. Ratio in g/g ≈ g/day. KDIGO: ACR <30, 30–300, >300 mg/g; PCR <150, 150–500, >500 mg/g.',
      sources: [['KDIGO 2024 clinical practice guideline for CKD evaluation and management', 'https://kdigo.org/guidelines/ckd-evaluation-and-management/']]},
    'potassium': {group: 'Tubular function', title: 'Potassium work-up: urine K⁺/creatinine & TTKG', sub: 'Renal response to hypo- or hyperkalaemia',
      fields: [['num', 'pK', 'Plasma potassium · mmol/L', '1–10'], ['num', 'uK', 'Urine potassium · mmol/L', 'spot urine'], ['num', 'uCr', 'Urine creatinine', 'spot urine'], ['sel', 'crUnit', 'Urine creatinine unit', [['mmol', 'mmol/L'], ['umol', 'µmol/L'], ['mgdl', 'mg/dL']]],
        ['num', 'uOsm', 'Urine osmolality · mOsm/kg (for TTKG, optional)', '50–1500'], ['num', 'pOsm', 'Plasma osmolality · mOsm/kg (for TTKG)', '200–450'], ['num', 'uNa', 'Urine sodium · mmol/L (for TTKG validity)', '0–400']],
      run: M.potassium,
      render: a => out('Urine K⁺/creatinine', f(a.ratio, 2), `mmol/mmol · ${f(a.mEqPerG, 0)} mEq/g`, `<p>${a.context === 'hypo' ? (a.ratio < 1.5 ? 'Hypokalaemia with a ratio <1.5: appropriate renal K⁺ conservation — suggests a non-renal cause (intake, GI loss) or a shift into cells.' : 'Hypokalaemia with a ratio ≥1.5: inappropriate renal K⁺ excretion — consider renal potassium loss (diuretics, mineralocorticoid excess, tubulopathies, magnesium deficiency).') : a.context === 'hyper' ? (a.ratio > 20 ? 'Hyperkalaemia with a ratio >20: appropriate renal K⁺ excretion — suggests a load or a shift out of cells.' : 'Hyperkalaemia with a ratio ≤20: renal K⁺ excretion lower than expected — consider low distal delivery, low aldosterone activity or its blockade, or reduced kidney function.') : 'Plasma potassium is normal; the ratio is interpreted against hypo- or hyperkalaemia.'}</p>`
        + (a.ttkg !== null ? `<p><strong>TTKG ${f(a.ttkg, 1)}</strong>${a.ttkgNote ? ' — ' + a.ttkgNote : ''}. Historically, TTKG <3 in hypokalaemia and >7 in hyperkalaemia were taken as appropriate. Its authors no longer recommend it because urea recycling in the medullary collecting duct invalidates its assumptions; prefer the K⁺/creatinine ratio.</p>` : '')),
      method: 'Urine K⁺/creatinine (mmol/mmol) = urine K ÷ urine creatinine (mmol/L); × 8.84 = mEq/g. Halperin: <1.5 expected with hypokalaemia of non-renal cause; >20 expected as the response to hyperkalaemia. TTKG = (urine K ÷ plasma K) ÷ (urine osm ÷ plasma osm), valid only when urine osm > plasma osm and urine Na > 25 mmol/L.',
      sources: [['Halperin ML. Assessing the renal response in patients with potassium disorders: a shift in emphasis from the TTKG to the urine K+/creatinine ratio. Afr J Nephrol 2017;20:22–4', 'https://doi.org/10.21804/20-1-2453'], ['Kamel KS, Halperin ML. Use of urine electrolytes and urine osmolality in the clinical diagnosis of fluid, electrolytes, and acid-base disorders. Kidney Int Rep 2021;6:1211–24', 'https://doi.org/10.1016/j.ekir.2021.02.003'], ['West ML et al. New clinical approach to evaluate disorders of potassium excretion. Miner Electrolyte Metab 1986;12:234–8 (PMID 3762510)', 'https://pubmed.ncbi.nlm.nih.gov/3762510/']]},
    'urine-ag': {group: 'Tubular function', title: 'Urine anion gap & urine osmolal gap', sub: 'Normal-anion-gap acidosis · estimated urine ammonium',
      fields: [['num', 'uNa', 'Urine sodium · mmol/L', '0–400'], ['num', 'uK', 'Urine potassium · mmol/L', '0–300'], ['num', 'uCl', 'Urine chloride · mmol/L', '0–400'],
        ['num', 'uOsm', 'Urine osmolality · mOsm/kg (optional)', '50–1500'], ['num', 'uUrea', 'Urine urea (optional)', 'value'], ['sel', 'ureaUnit', 'Urine urea unit', [['mmol', 'urea mmol/L'], ['mgdl', 'urea nitrogen mg/dL']]], ['num', 'uGlu', 'Urine glucose (optional)', 'value'], ['sel', 'gluUnit', 'Urine glucose unit', [['mmol', 'mmol/L'], ['mgdl', 'mg/dL']]]],
      run: M.urineAnionGap,
      render: a => out('Urine anion gap', (a.uag > 0 ? '+' : '') + f(a.uag, 0), 'mmol/L', `<p>${a.uag < 0 ? 'Negative: suggests adequate urinary ammonium (for example, acidosis from diarrhoea).' : 'Positive: suggests low urinary ammonium (for example, distal renal tubular acidosis or reduced kidney function).'} Use only in normal-anion-gap metabolic acidosis; ketones, hippurate, low urine sodium (<20 mmol/L) or very alkaline urine make it unreliable.</p>`
        + (a.osmGap !== null ? `<p><strong>Urine osmolal gap ${f(a.osmGap, 0)} mOsm/kg</strong> → estimated urine NH₄⁺ ≈ ${f(a.nh4, 0)} mmol/L. The osmolal gap is the more reliable estimate of ammonium when other anions are present.</p>` : '')),
      method: 'Urine anion gap = urine Na + K − Cl. Urine osmolal gap = measured urine osmolality − [2 × (Na + K) + urea + glucose] (mmol/L); urine NH₄⁺ ≈ osmolal gap ÷ 2.',
      sources: [['Batlle DC et al. The use of the urinary anion gap in the diagnosis of hyperchloremic metabolic acidosis. N Engl J Med 1988;318:594–9', 'https://doi.org/10.1056/NEJM198803103181002'], ['Kamel KS, Halperin ML. Use of urine electrolytes and urine osmolality in the clinical diagnosis of fluid, electrolytes, and acid-base disorders. Kidney Int Rep 2021;6:1211–24', 'https://doi.org/10.1016/j.ekir.2021.02.003']]},
    'phosphate': {group: 'Tubular function', title: 'Phosphate: FEPO₄, TRP & TmP/GFR', sub: 'Renal phosphate handling · fasting morning sample',
      fields: [['num', 'uP', 'Urine phosphate', 'same unit as plasma'], ['num', 'pP', 'Plasma phosphate', 'value'], ['sel', 'pUnit', 'Phosphate unit (both)', [['mmol', 'mmol/L'], ['mgdl', 'mg/dL']]], ['num', 'uCr', 'Urine creatinine', 'same unit as plasma'], ['num', 'pCr', 'Plasma creatinine', 'same unit as urine']],
      run: M.phosphate,
      render: a => out('TmP/GFR', f(a.tmp, 2), `mmol/L · ${f(a.tmpMg, 2)} mg/dL`, `<table class="calc-crcl-table"><tbody><tr><th scope="row">Fractional excretion of phosphate (FEPO₄)</th><td>${f(a.fe, 1)}%</td></tr><tr><th scope="row">Tubular reabsorption of phosphate (TRP)</th><td>${f(a.trp, 3)}</td></tr></tbody></table><p>${a.low ? 'With hypophosphataemia, a low TmP/GFR (below the age- and sex-specific reference range) indicates renal phosphate wasting (for example FGF23 excess, hyperparathyroidism, Fanconi syndrome, drugs); a TmP/GFR within range points to a non-renal cause.' : 'Compare TmP/GFR with the age- and sex-specific reference range.'} Use a fasting second-morning urine with a simultaneous blood sample.</p>`),
      method: 'FEPO₄ = (urine P × plasma creatinine) ÷ (plasma P × urine creatinine); TRP = 1 − FEPO₄. TmP/GFR (Kenny & Glen algorithm, Barth et al.): if TRP ≤0.86, TmP/GFR = TRP × plasma P; if TRP >0.86, TmP/GFR = [0.3 × TRP ÷ (1 − 0.8 × TRP)] × plasma P (plasma P in mmol/L). Phosphate mg/dL = mmol/L × 3.097.',
      sources: [['Kenny AP, Glen AC. Tests of phosphate reabsorption. Lancet 1973;2:158', 'https://doi.org/10.1016/S0140-6736(73)93112-7'], ['Barth JH, Jones RG, Payne RB. Calculation of renal tubular reabsorption of phosphate: the algorithm performs better than the nomogram. Ann Clin Biochem 2000;37:79–81', 'https://doi.org/10.1258/0004563001901371'], ['Payne RB. Renal tubular reabsorption of phosphate (TmP/GFR): indications and interpretation. Ann Clin Biochem 1998;35:201–6', 'https://doi.org/10.1177/000456329803500203']]},
    'magnesium': {group: 'Tubular function', title: 'Fractional excretion of magnesium', sub: 'Hypomagnesaemia: renal versus non-renal loss',
      fields: [['num', 'uMg', 'Urine magnesium', 'same unit as plasma'], ['num', 'pMg', 'Plasma magnesium', 'value'], ['num', 'uCr', 'Urine creatinine', 'same unit as plasma'], ['num', 'pCr', 'Plasma creatinine', 'same unit as urine']],
      run: M.magnesium,
      render: a => out('FEMg', f(a.fe, 1), '%', `<p>${a.fe > 2 ? 'Above 2% in hypomagnesaemia (with normal kidney function): suggests renal magnesium wasting (for example loop or thiazide diuretics, cisplatin, calcineurin inhibitors, aminoglycosides, tubulopathies).' : '2% or less in hypomagnesaemia: suggests a non-renal cause (GI loss, low intake, PPI-associated intestinal malabsorption).'}</p>`),
      method: 'FEMg = (urine Mg × plasma creatinine) ÷ (0.7 × plasma Mg × urine creatinine) × 100. The factor 0.7 allows for the ~30% of plasma magnesium bound to albumin and not filtered.',
      sources: [['Agus ZS. Hypomagnesemia. J Am Soc Nephrol 1999;10:1616–22', 'https://doi.org/10.1681/ASN.V1071616']]},
    'uf-rate': {group: 'Dialysis', title: 'Ultrafiltration rate', sub: 'Haemodialysis · 13 mL/kg/h threshold',
      fields: [['num', 'uf', 'Ultrafiltration goal · L', '0.1–10'], ['num', 'hours', 'Session length · h', '1–12'], ['num', 'weight', 'Target (dry) weight · kg', '25–250']],
      run: M.ufRate,
      render: a => out('Ultrafiltration rate', f(a.rate, 1), 'mL/kg/h', `<table class="calc-crcl-table"><tbody><tr><th scope="row">Maximum UF at 13 mL/kg/h for this session</th><td>${f(a.max13, 2)} L</td></tr><tr><th scope="row">Session length to stay ≤13 mL/kg/h</th><td>${f(a.hoursFor13, 1)} h</td></tr></tbody></table><p>Rates above 13 mL/kg/h were associated with higher mortality in observational data; consider a longer or extra session or lower interdialytic gain.</p>`, a.high ? ' ca-high' : ''),
      method: 'UF rate = UF goal (mL) ÷ (dry weight kg × hours).',
      sources: [['Flythe JE et al. Rapid fluid removal during dialysis is associated with cardiovascular morbidity and mortality. Kidney Int 2011;79:250–7', 'https://doi.org/10.1038/ki.2010.383']]},
    'crrt': {group: 'Dialysis', title: 'CRRT dose & filtration fraction', sub: 'Effluent mL/kg/h · pre-dilution correction',
      fields: [weight, ['num', 'qb', 'Blood flow · mL/min', '50–500'], ['num', 'hct', 'Haematocrit · %', '10–60'], ['num', 'pre', 'Pre-filter replacement · mL/h', '0 if none'], ['num', 'post', 'Post-filter replacement · mL/h', '0 if none'],
        ['num', 'qd', 'Dialysate · mL/h', '0 if none'], ['num', 'net', 'Net fluid removal · mL/h', '0–1000']],
      run: M.crrt,
      render: a => out('Prescribed effluent dose', f(a.dose, 1), 'mL/kg/h', `<table class="calc-crcl-table"><tbody><tr><th scope="row">Total effluent</th><td>${f(a.effluent, 0)} mL/h</td></tr><tr><th scope="row">Dose corrected for pre-dilution (× ${f(a.factor, 3)})</th><td>${f(a.corrected, 1)} mL/kg/h</td></tr><tr><th scope="row">Filtration fraction</th><td>${f(a.ff * 100, 1)}%${a.ff > 0.25 ? ' — above 25%: higher risk of filter clotting' : a.ff > 0.2 ? ' — 20–25%: borderline' : ''}</td></tr></tbody></table><p>KDIGO: deliver an effluent volume of 20–25 mL/kg/h; prescribing more is usually needed to allow for interruptions.</p>`, a.corrected < 20 ? ' ca-intermediate' : ''),
      method: 'Effluent = pre + post replacement + dialysate + net removal. Pre-dilution factor = Qb ÷ (Qb + pre-filter replacement), both in mL/h. Plasma flow = Qb × (1 − Hct). Filtration fraction = (pre + post replacement + net removal) ÷ (plasma flow + pre-filter replacement).',
      sources: [['KDIGO 2012 clinical practice guideline for acute kidney injury (recommendation 5.8.4)', 'https://kdigo.org/guidelines/acute-kidney-injury/'], ['Tolwani A. Continuous renal-replacement therapy for acute kidney injury. N Engl J Med 2012;367:2505–14', 'https://doi.org/10.1056/NEJMct1206045']]},
    'pd-ktv': {group: 'Dialysis', title: 'Peritoneal dialysis weekly Kt/V', sub: 'Peritoneal + residual renal · Watson volume',
      fields: [['num', 'dUrea', 'Dialysate urea (24-h collection)', 'same unit as plasma'], ['num', 'pUrea', 'Plasma urea', 'value'], ['num', 'drain', '24-hour drained volume · L', '1–40'], ['num', 'uUrea', 'Urine urea (optional)', 'same unit'], ['num', 'urine', '24-hour urine volume · L (optional)', '0–6'], sexSel, age, ['num', 'height', 'Height · cm', '120–230'], weight],
      run: M.pdKtv,
      render: a => out('Weekly Kt/V urea', f(a.total, 2), 'total', `<table class="calc-crcl-table"><tbody><tr><th scope="row">Peritoneal (D/P urea ${f(a.dp, 2)})</th><td>${f(a.perit, 2)}</td></tr>${a.renal !== null ? `<tr><th scope="row">Residual renal</th><td>${f(a.renal, 2)}</td></tr>` : ''}<tr><th scope="row">Urea volume (Watson)</th><td>${f(a.V, 1)} L</td></tr></tbody></table><p>KDOQI: minimum total weekly Kt/V 1.7. ISPD 2020 favours goal-directed, individualised prescription over a single small-solute target.</p>`, a.total < 1.7 ? ' ca-intermediate' : ''),
      method: 'Weekly peritoneal Kt/V = (dialysate urea ÷ plasma urea) × 24-h drained volume × 7 ÷ V. Renal = (urine urea ÷ plasma urea) × 24-h urine volume × 7 ÷ V. Watson V: men 2.447 − 0.09516 × age + 0.1074 × height + 0.3362 × weight; women −2.097 + 0.1069 × height + 0.2466 × weight.',
      sources: [['Watson PE et al. Total body water volumes for adult males and females estimated from simple anthropometric measurements. Am J Clin Nutr 1980;33:27–39', 'https://doi.org/10.1093/ajcn/33.1.27'], ['KDOQI clinical practice guidelines for peritoneal dialysis adequacy. Am J Kidney Dis 2006;48 Suppl 1:S98–129', 'https://doi.org/10.1053/j.ajkd.2006.04.006'], ['Brown EA et al. ISPD practice recommendation: prescribing high-quality goal-directed peritoneal dialysis. Perit Dial Int 2020;40:244–53', 'https://doi.org/10.1177/0896860819895364']]},
    'tsat': {group: 'Anaemia', title: 'Transferrin saturation (TSAT)', sub: 'KDIGO anaemia iron thresholds',
      fields: [['num', 'fe', 'Serum iron', 'same unit as TIBC'], ['num', 'tibc', 'TIBC', 'same unit'], ['num', 'ferritin', 'Ferritin · ng/mL (optional)', '1–10000']],
      run: M.tsat,
      render: a => out('TSAT', f(a.tsat, 1), '%', `<p>${a.ivIronTrial === null ? 'Add ferritin to compare with the KDIGO threshold.' : a.ivIronTrial ? 'TSAT ≤30% and ferritin ≤500 ng/mL: KDIGO suggests a trial of iron in adults with CKD anaemia (when an increase in Hb or a lower ESA dose is desired).' : 'Outside the KDIGO trial-of-iron thresholds (TSAT ≤30% and ferritin ≤500 ng/mL).'}</p>`),
      method: 'TSAT (%) = serum iron ÷ TIBC × 100 (same units).',
      sources: [['KDIGO 2012 clinical practice guideline for anemia in CKD', 'https://kdigo.org/guidelines/anemia-in-ckd/']]},
    'ganzoni': {group: 'Anaemia', title: 'Iron deficit (Ganzoni)', sub: 'Total iron dose estimate',
      fields: [weight, ['num', 'hb', 'Current haemoglobin', 'value'], ['num', 'target', 'Target haemoglobin', 'e.g. 15 g/dL'], ['sel', 'hbUnit', 'Haemoglobin unit', [['gdl', 'g/dL'], ['gl', 'g/L']]]],
      run: M.ganzoni,
      render: a => out('Total iron deficit', f(a.deficit, 0), 'mg', `<p>${f(a.hbPart, 0)} mg for haemoglobin + 500 mg for iron stores. Give the product-specific dose and maximum single dose from the label. In CKD, the haemoglobin target for ESA therapy is lower; this formula estimates total iron need only.</p>`),
      method: 'Iron deficit (mg) = weight (kg) × (target Hb − actual Hb) (g/dL) × 2.4 + 500 mg depot iron (body weight ≥35 kg). Several IV iron labels use target Hb 15 g/dL.',
      sources: [['Ganzoni AM. Intravenous iron-dextran: therapeutic and experimental possibilities. Schweiz Med Wochenschr 1970;100:301–3 (PMID 5413918)', 'https://pubmed.ncbi.nlm.nih.gov/5413918/']]}
  };
  const el = id => document.getElementById(id);
  let current = null;
  const placeholder = '<p class="calc-placeholder">Enter the values above. Nothing is saved or sent.</p>';
  function field([type, id, label, extra]) {
    const fid = 'nt-' + id;
    if (type === 'sel') return `<label>${h(label)}<select id="${fid}" data-key="${id}">${extra.map(([v, t]) => `<option value="${h(v)}">${h(t)}</option>`).join('')}</select></label>`;
    return `<label>${h(label)}<input id="${fid}" data-key="${id}" type="number" inputmode="decimal" step="any" placeholder="${h(extra || '')}" autocomplete="off"></label>`;
  }
  function render(id) {
    const c = C[id]; current = id;
    el('nephro-tools-title').textContent = c.title; el('nephro-tools-eyebrow').textContent = c.group.toUpperCase();
    el('nephro-tools-body').innerHTML = `<p class="calc-intro">${h(c.sub)}.</p><form id="nt-form" autocomplete="off" novalidate><div class="calc-grid">${c.fields.map(field).join('')}</div><div class="calc-actions"><button type="submit" class="calc-primary">Calculate</button><button type="button" class="tool-clear">Clear values</button></div></form><div id="nt-result" role="status" aria-live="polite" aria-atomic="true">${placeholder}</div>`
      + `<p class="calc-privacy">Values stay in this tab and clear when this panel closes. No identifiers, results or entries are stored or transmitted.</p>`
      + `<details class="calc-method"><summary>Method, limits &amp; sources</summary><p class="calc-formula">${h(c.method)}</p><ul>${c.sources.map(([t, u]) => `<li><a href="${h(u)}" target="_blank" rel="noopener noreferrer">${h(t)}</a></li>`).join('')}</ul><p>Sources checked 1 November 2026. Arithmetic/software verification is separate from clinical approval. Adults only.</p></details>`;
    const form = el('nt-form'), result = el('nt-result');
    const values = () => Object.fromEntries([...form.querySelectorAll('[data-key]')].map(n => [n.dataset.key, n.value]));
    const update = (focus = false) => {
      form.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid'));
      const a = c.run(values());
      if (!a.ok) { result.innerHTML = `<p class="calc-error">${h(a.message)}</p>`; const bad = el('nt-' + a.field); bad?.setAttribute('aria-invalid', 'true'); if (focus) bad?.focus(); return false; }
      result.innerHTML = c.render(a); return true;
    };
    let touched = false;
    form.addEventListener('submit', e => { e.preventDefault(); touched = true; if (update(true)) result.scrollIntoView({block: 'nearest', behavior: 'smooth'}); });
    form.addEventListener('input', () => { if (touched || form.querySelector('input:not(:placeholder-shown)')) update(); });
    form.addEventListener('change', () => update());
    form.querySelector('.tool-clear').addEventListener('click', () => { form.reset(); result.innerHTML = placeholder; touched = false; form.querySelector('input,select').focus(); });
  }
  function clear() { if (el('nephro-tools-body')) el('nephro-tools-body').innerHTML = ''; current = null; }
  function setup() {
    const panel = el('nephro-tools'); if (!panel) return;
    panel.querySelector('.tool-close').addEventListener('click', () => panel.close());
    panel.addEventListener('close', clear); window.addEventListener('pagehide', () => { if (panel.open) panel.close(); clear(); });
    document.addEventListener('click', e => {
      const o = e.target.closest('[data-open="nephro-tools"][data-calc]'); if (!o || !C[o.dataset.calc]) return;
      const menu = el('calc-menu'); if (menu?.open) menu.close();
      render(o.dataset.calc); if (!panel.open) panel.showModal(); el('nt-form').querySelector('input,select').focus();
    });
  }
  if (typeof document !== 'undefined') setup();
  return {C, render};
})();
