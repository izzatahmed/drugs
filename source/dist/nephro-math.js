'use strict';
// Pure arithmetic for the nephrology calculators (v0.21). No DOM, no storage. Every function returns
// {ok:true, ...} or {ok:false, field, message}. Inputs arrive as strings from forms.
const NephroMath = (() => {
  const GLU = 18.016, CA = 4.008, CREAT = 88.42, BUN_UREA = 2.8;
  const num = v => { if (v === '' || v === null || v === undefined) return NaN; const n = Number(String(v).replace(',', '.')); return Number.isFinite(n) ? n : NaN; };
  const bad = (field, message) => ({ok: false, field, message});
  function need(o, field, label, lo, hi, optional = false) {
    const v = num(o[field]);
    if (Number.isNaN(v)) return optional ? {v: null} : {err: bad(field, `Enter ${label}.`)};
    if (v < lo || v > hi) return {err: bad(field, `${label[0].toUpperCase() + label.slice(1)} must be between ${lo} and ${hi}.`)};
    return {v};
  }
  function read(o, spec) {
    const out = {};
    for (const [field, label, lo, hi, optional] of spec) { const r = need(o, field, label, lo, hi, optional); if (r.err) return r; out[field] = r.v; }
    return {vals: out};
  }
  // Total body water (Adrogué & Madias, NEJM 2000): fraction of body weight by age and sex.
  function tbwFraction(sex, age) { const old = age >= 65; return sex === 'male' ? (old ? 0.5 : 0.6) : (old ? 0.45 : 0.5); }
  function tbw(o) {
    if (!['male', 'female'].includes(o.sex)) return {err: bad('sex', 'Choose sex.')};
    const r = read(o, [['weight', 'weight (kg)', 25, 300], ['age', 'age (years)', 18, 110]]); if (r.err) return {err: r.err};
    const f = tbwFraction(o.sex, r.vals.age); return {f, litres: f * r.vals.weight};
  }
  const INFUSATES = {
    'nacl3': {name: '3% sodium chloride', na: 513, k: 0}, 'nacl09': {name: '0.9% sodium chloride', na: 154, k: 0}, 'nacl045': {name: '0.45% sodium chloride', na: 77, k: 0},
    'rl': {name: 'Ringer’s lactate', na: 130, k: 4}, 'd5w': {name: '5% dextrose in water', na: 0, k: 0}};

  function naGlucose(o) {
    const r = read(o, [['na', 'measured sodium (mmol/L)', 100, 180], ['glucose', 'glucose', 0.1, 3000]]); if (r.err) return r.err;
    const g = o.gluUnit === 'mmol' ? r.vals.glucose * GLU : r.vals.glucose;
    if (g > 3000) return bad('glucose', 'Glucose is outside the supported range.');
    const excess = Math.max(0, g - 100) / 100;
    return {ok: true, glucoseMgDl: g, katz: r.vals.na + 1.6 * excess, hillier: r.vals.na + 2.4 * excess, below: g <= 100};
  }
  function hyponatremia(o) {
    const t = tbw(o); if (t.err) return t.err;
    const r = read(o, [['na', 'serum sodium (mmol/L)', 90, 135]]); if (r.err) return r.err;
    let inf = INFUSATES[o.infusate];
    if (o.infusate === 'custom') {
      const c = read(o, [['infNa', 'infusate sodium (mmol/L)', 0, 1000], ['infK', 'infusate potassium (mmol/L)', 0, 200]]); if (c.err) return c.err;
      inf = {name: 'Custom infusate', na: c.vals.infNa, k: c.vals.infK};
    }
    if (!inf) return bad('infusate', 'Choose an infusate.');
    const perLitre = (inf.na + inf.k - r.vals.na) / (t.litres + 1);
    const lim = l => perLitre > 0 ? l / perLitre : null;
    return {ok: true, tbw: t.litres, fraction: t.f, infusate: inf, perLitre, litresFor6: lim(6), litresFor8: lim(8)};
  }
  function freeWater(o) {
    const t = tbw(o); if (t.err) return t.err;
    const r = read(o, [['na', 'serum sodium (mmol/L)', 141, 200], ['target', 'target sodium (mmol/L)', 130, 150, true]]); if (r.err) return r.err;
    const target = r.vals.target ?? 140;
    if (target >= r.vals.na) return bad('target', 'Target sodium must be below the measured sodium.');
    return {ok: true, tbw: t.litres, fraction: t.f, target, deficit: t.litres * (r.vals.na / target - 1)};
  }
  function correctedCalcium(o) {
    const si = o.caUnit === 'mmol';
    const r = read(o, si ? [['ca', 'total calcium (mmol/L)', 0.5, 5], ['alb', 'albumin (g/L)', 5, 70]] : [['ca', 'total calcium (mg/dL)', 2, 20], ['alb', 'albumin (g/dL)', 0.5, 7]]); if (r.err) return r.err;
    const mg = si ? r.vals.ca * CA : r.vals.ca, albG = si ? r.vals.alb / 10 : r.vals.alb;
    const corr = mg + 0.8 * (4 - albG);
    return {ok: true, mgdl: corr, mmol: corr / CA, si};
  }
  function osmolalGap(o) {
    const r = read(o, [['na', 'sodium (mmol/L)', 100, 200], ['glucose', 'glucose', 0.1, 3000], ['urea', o.ureaUnit === 'mmol' ? 'urea (mmol/L)' : 'BUN (mg/dL)', 0.1, 400],
      ['measured', 'measured osmolality (mOsm/kg)', 200, 500, true], ['ethanol', 'ethanol', 0, 1000, true]]); if (r.err) return r.err;
    const g = o.gluUnit === 'mmol' ? r.vals.glucose : r.vals.glucose / GLU;
    const u = o.ureaUnit === 'mmol' ? r.vals.urea : r.vals.urea / BUN_UREA;
    const e = r.vals.ethanol === null ? 0 : o.etohUnit === 'mmol' ? r.vals.ethanol : r.vals.ethanol / 3.7;
    const calc = 2 * r.vals.na + g + u + e;
    return {ok: true, calculated: calc, gap: r.vals.measured === null ? null : r.vals.measured - calc, ethanolIncluded: r.vals.ethanol !== null};
  }
  function anionGap(o) {
    const r = read(o, [['na', 'sodium (mmol/L)', 100, 200], ['cl', 'chloride (mmol/L)', 50, 150], ['hco3', 'bicarbonate (mmol/L)', 1, 60], ['alb', 'albumin', 0.5, 70, true], ['normal', 'normal anion gap', 3, 20, true]]); if (r.err) return r.err;
    const v = r.vals, ag = v.na - (v.cl + v.hco3), normal = v.normal ?? 12;
    let albG = null; if (v.alb !== null) { albG = o.albUnit === 'gl' ? v.alb / 10 : v.alb; if (albG > 7) return bad('alb', 'Check the albumin unit.'); }
    const corr = albG === null ? null : ag + 2.5 * (4 - albG);
    const used = corr ?? ag, delta = v.hco3 < 24 ? (used - normal) / (24 - v.hco3) : null;
    let deltaNote = null;
    if (delta !== null && used > normal + 4) deltaNote = delta < 0.4 ? 'Hyperchloraemic normal-anion-gap acidosis predominates' : delta < 1 ? 'High-anion-gap acidosis with a coexisting normal-anion-gap acidosis' : delta <= 2 ? 'Consistent with an uncomplicated high-anion-gap acidosis' : 'High-anion-gap acidosis with a coexisting metabolic alkalosis (or compensated respiratory acidosis)';
    return {ok: true, ag, corrected: corr, normal, delta, deltaNote, high: used > normal + 4};
  }
  function winters(o) {
    const r = read(o, [['hco3', 'bicarbonate (mmol/L)', 1, 30], ['pco2', 'measured pCO₂ (mmHg)', 5, 150, true]]); if (r.err) return r.err;
    const e = 1.5 * r.vals.hco3 + 8, p = r.vals.pco2;
    return {ok: true, expected: e, low: e - 2, high: e + 2, verdict: p === null ? null : p < e - 2 ? 'lower than expected: additional respiratory alkalosis' : p > e + 2 ? 'higher than expected: additional respiratory acidosis' : 'within the expected range: appropriate respiratory compensation'};
  }
  function fractionalExcretion(o) {
    const r = read(o, [['uCr', 'urine creatinine', 0.01, 50000], ['pCr', 'plasma creatinine', 0.01, 3000], ['uNa', 'urine sodium (mmol/L)', 0, 400, true], ['pNa', 'plasma sodium (mmol/L)', 100, 200, true],
      ['uUrea', 'urine urea', 0, 5000, true], ['pUrea', 'plasma urea', 0.1, 500, true]]); if (r.err) return r.err;
    const v = r.vals, out = {ok: true, fena: null, feurea: null};
    if (v.uNa !== null || v.pNa !== null) { if (v.uNa === null) return bad('uNa', 'Enter urine sodium.'); if (v.pNa === null) return bad('pNa', 'Enter plasma sodium.'); out.fena = 100 * v.uNa * v.pCr / (v.pNa * v.uCr); }
    if (v.uUrea !== null || v.pUrea !== null) { if (v.uUrea === null) return bad('uUrea', 'Enter urine urea.'); if (v.pUrea === null) return bad('pUrea', 'Enter plasma urea.'); out.feurea = 100 * v.uUrea * v.pCr / (v.pUrea * v.uCr); }
    if (out.fena === null && out.feurea === null) return bad('uNa', 'Enter urine and plasma sodium, urea, or both.');
    return out;
  }
  function akiStage(o) {
    const si = o.crUnit === 'umol';
    const r = read(o, [['base', 'baseline creatinine', si ? 10 : 0.1, si ? 1500 : 17], ['cur', 'current creatinine', si ? 10 : 0.1, si ? 2500 : 28], ['uo', 'urine output (mL/kg/h)', 0, 10, true], ['uoHours', 'urine output duration (h)', 1, 72, true]]); if (r.err) return r.err;
    const v = r.vals, b = si ? v.base / CREAT : v.base, c = si ? v.cur / CREAT : v.cur, ratio = c / b, rise = c - b;
    let cr = 0, crWhy = 'Creatinine criteria not met';
    if (o.rrt === 'yes') { cr = 3; crWhy = 'Kidney replacement therapy started'; }
    else if (ratio >= 3) { cr = 3; crWhy = `Creatinine ${ratio.toFixed(1)} × baseline (≥3.0)`; }
    else if (c >= 4 && rise >= 0.3) { cr = 3; crWhy = 'Creatinine ≥4.0 mg/dL (≥354 µmol/L)'; }
    else if (ratio >= 2) { cr = 2; crWhy = `Creatinine ${ratio.toFixed(1)} × baseline (2.0–2.9)`; }
    else if (ratio >= 1.5) { cr = 1; crWhy = `Creatinine ${ratio.toFixed(1)} × baseline (1.5–1.9, within 7 days)`; }
    else if (rise >= 0.3) { cr = 1; crWhy = `Rise of ${si ? (rise * CREAT).toFixed(0) + ' µmol/L' : rise.toFixed(2) + ' mg/dL'} (≥0.3 mg/dL / 26.5 µmol/L within 48 h)`; }
    let uo = 0, uoWhy = null;
    if (v.uo !== null || v.uoHours !== null) {
      if (v.uo === null) return bad('uo', 'Enter urine output.'); if (v.uoHours === null) return bad('uoHours', 'Enter how long urine output has been at this level.');
      if (v.uo === 0 && v.uoHours >= 12) { uo = 3; uoWhy = 'Anuria for ≥12 h'; }
      else if (v.uo < 0.3 && v.uoHours >= 24) { uo = 3; uoWhy = '<0.3 mL/kg/h for ≥24 h'; }
      else if (v.uo < 0.5 && v.uoHours >= 12) { uo = 2; uoWhy = '<0.5 mL/kg/h for ≥12 h'; }
      else if (v.uo < 0.5 && v.uoHours >= 6) { uo = 1; uoWhy = '<0.5 mL/kg/h for 6–12 h'; }
      else uoWhy = 'Urine output criteria not met';
    }
    return {ok: true, stage: Math.max(cr, uo), cr, crWhy, uo, uoWhy, ratio};
  }
  const PER_MMOL = 8.842; // mg/mmol → mg/g (1 mmol creatinine = 113.1 mg)
  function proteinuria(o) {
    let mgG;
    if (o.mode === 'raw') {
      const r = read(o, [['uProt', 'urine protein or albumin (mg/dL)', 0.1, 5000], ['uCr', 'urine creatinine (mg/dL)', 1, 1000]]); if (r.err) return r.err;
      mgG = 1000 * r.vals.uProt / r.vals.uCr;
    } else {
      const r = read(o, [['ratio', 'ratio', 0.01, 100000]]); if (r.err) return r.err;
      mgG = {mgg: 1, gg: 1000, mgmg: 1000, mgmmol: PER_MMOL}[o.unit] * r.vals.ratio;
      if (!mgG) return bad('unit', 'Choose the unit.');
    }
    const albumin = o.kind === 'albumin';
    const cat = albumin ? (mgG < 30 ? ['A1', 'normal to mildly increased'] : mgG <= 300 ? ['A2', 'moderately increased'] : ['A3', 'severely increased'])
      : (mgG < 150 ? ['A1', 'normal to mildly increased'] : mgG <= 500 ? ['A2', 'moderately increased'] : ['A3', 'severely increased']);
    return {ok: true, albumin, mgG, mgMmol: mgG / PER_MMOL, perDay: mgG / 1000, cat: cat[0], catLabel: cat[1], nephrotic: !albumin && mgG >= 3500};
  }
  function ufRate(o) {
    const r = read(o, [['uf', 'ultrafiltration goal (L)', 0.1, 10], ['hours', 'session length (h)', 1, 12], ['weight', 'target (dry) weight (kg)', 25, 250]]); if (r.err) return r.err;
    const v = r.vals, rate = v.uf * 1000 / (v.weight * v.hours);
    return {ok: true, rate, max13: 13 * v.weight * v.hours / 1000, hoursFor13: v.uf * 1000 / (13 * v.weight), high: rate > 13};
  }
  function crrt(o) {
    const r = read(o, [['weight', 'weight (kg)', 25, 300], ['qb', 'blood flow (mL/min)', 50, 500], ['hct', 'haematocrit (%)', 10, 60], ['pre', 'pre-filter replacement (mL/h)', 0, 10000], ['post', 'post-filter replacement (mL/h)', 0, 10000],
      ['qd', 'dialysate (mL/h)', 0, 10000], ['net', 'net fluid removal (mL/h)', 0, 1000]]); if (r.err) return r.err;
    const v = r.vals, effluent = v.pre + v.post + v.qd + v.net;
    if (!effluent) return bad('qd', 'Enter at least one fluid flow.');
    const qbh = v.qb * 60, qp = qbh * (1 - v.hct / 100), factor = qbh / (qbh + v.pre);
    const ff = (v.pre + v.post + v.net) / (qp + v.pre);
    return {ok: true, effluent, dose: effluent / v.weight, corrected: effluent * factor / v.weight, factor, ff, plasmaFlow: qp};
  }
  function watson(o) {
    if (!['male', 'female'].includes(o.sex)) return {err: bad('sex', 'Choose sex.')};
    const r = read(o, [['age', 'age (years)', 18, 110], ['height', 'height (cm)', 120, 230], ['weight', 'weight (kg)', 25, 300]]); if (r.err) return {err: r.err};
    const {age, height, weight} = r.vals;
    return {v: o.sex === 'male' ? 2.447 - 0.09516 * age + 0.1074 * height + 0.3362 * weight : -2.097 + 0.1069 * height + 0.2466 * weight};
  }
  function pdKtv(o) {
    const w = watson(o); if (w.err) return w.err;
    const r = read(o, [['dUrea', 'dialysate urea', 0.1, 500], ['pUrea', 'plasma urea', 0.1, 500], ['drain', '24-hour drained volume (L)', 1, 40], ['uUrea', 'urine urea', 0, 5000, true], ['urine', '24-hour urine volume (L)', 0, 6, true]]); if (r.err) return r.err;
    const v = r.vals, dp = v.dUrea / v.pUrea; if (dp > 1.2) return bad('dUrea', 'Dialysate urea should not exceed plasma urea; check the values.');
    const perit = dp * v.drain * 7 / w.v;
    let renal = null;
    if (v.uUrea !== null || v.urine !== null) { if (v.uUrea === null) return bad('uUrea', 'Enter urine urea.'); if (v.urine === null) return bad('urine', 'Enter 24-hour urine volume.'); renal = (v.uUrea / v.pUrea) * v.urine * 7 / w.v; }
    return {ok: true, V: w.v, dp, perit, renal, total: perit + (renal ?? 0)};
  }
  function tsat(o) {
    const r = read(o, [['fe', 'serum iron', 1, 1000], ['tibc', 'TIBC', 10, 1200], ['ferritin', 'ferritin (ng/mL)', 1, 10000, true]]); if (r.err) return r.err;
    if (r.vals.fe > r.vals.tibc) return bad('fe', 'Serum iron cannot exceed TIBC; check units (both µg/dL or both µmol/L).');
    const t = 100 * r.vals.fe / r.vals.tibc, f = r.vals.ferritin;
    return {ok: true, tsat: t, ferritin: f, ivIronTrial: f === null ? null : t <= 30 && f <= 500};
  }
  function ganzoni(o) {
    const gl = o.hbUnit === 'gl';
    const r = read(o, gl ? [['weight', 'weight (kg)', 35, 250], ['hb', 'haemoglobin (g/L)', 30, 200], ['target', 'target haemoglobin (g/L)', 80, 160]] : [['weight', 'weight (kg)', 35, 250], ['hb', 'haemoglobin (g/dL)', 3, 20], ['target', 'target haemoglobin (g/dL)', 8, 16]]); if (r.err) return r.err;
    const hb = gl ? r.vals.hb / 10 : r.vals.hb, target = gl ? r.vals.target / 10 : r.vals.target;
    if (target <= hb) return bad('target', 'Target haemoglobin must be above the current value.');
    const deficit = r.vals.weight * (target - hb) * 2.4 + 500;
    return {ok: true, deficit, hbPart: deficit - 500};
  }
  function potassium(o) {
    const r = read(o, [['uK', 'urine potassium (mmol/L)', 1, 300], ['uCr', 'urine creatinine', 0.1, 50000], ['pK', 'plasma potassium (mmol/L)', 1, 10],
      ['uOsm', 'urine osmolality (mOsm/kg)', 50, 1500, true], ['pOsm', 'plasma osmolality (mOsm/kg)', 200, 450, true], ['uNa', 'urine sodium (mmol/L)', 0, 400, true]]); if (r.err) return r.err;
    const v = r.vals, ucr = o.crUnit === 'umol' ? v.uCr / 1000 : o.crUnit === 'mgdl' ? v.uCr * 10 / CREAT : v.uCr; // → mmol/L
    if (ucr < 0.3 || ucr > 60) return bad('uCr', 'Urine creatinine is outside the expected range; check the unit.');
    const ratio = v.uK / ucr, context = v.pK < 3.5 ? 'hypo' : v.pK > 5.0 ? 'hyper' : 'normal';
    let ttkg = null, ttkgNote = null;
    if (v.uOsm !== null || v.pOsm !== null) {
      if (v.uOsm === null) return bad('uOsm', 'Enter urine osmolality for the TTKG.'); if (v.pOsm === null) return bad('pOsm', 'Enter plasma osmolality for the TTKG.');
      ttkg = (v.uK / v.pK) / (v.uOsm / v.pOsm);
      ttkgNote = v.uOsm <= v.pOsm ? 'not valid: urine osmolality must exceed plasma osmolality' : v.uNa !== null && v.uNa <= 25 ? 'not valid: urine sodium must exceed 25 mmol/L' : null;
    }
    return {ok: true, ratio, mEqPerG: ratio * PER_MMOL, context, ttkg, ttkgNote};
  }
  function urineAnionGap(o) {
    const r = read(o, [['uNa', 'urine sodium (mmol/L)', 0, 400], ['uK', 'urine potassium (mmol/L)', 0, 300], ['uCl', 'urine chloride (mmol/L)', 0, 400],
      ['uOsm', 'urine osmolality (mOsm/kg)', 50, 1500, true], ['uUrea', 'urine urea', 0, 5000, true], ['uGlu', 'urine glucose', 0, 3000, true]]); if (r.err) return r.err;
    const v = r.vals, uag = v.uNa + v.uK - v.uCl;
    let gap = null;
    if (v.uOsm !== null || v.uUrea !== null) {
      if (v.uOsm === null) return bad('uOsm', 'Enter urine osmolality for the osmolal gap.'); if (v.uUrea === null) return bad('uUrea', 'Enter urine urea for the osmolal gap.');
      const urea = o.ureaUnit === 'mgdl' ? v.uUrea / BUN_UREA : v.uUrea, glu = v.uGlu === null ? 0 : o.gluUnit === 'mgdl' ? v.uGlu / GLU : v.uGlu;
      gap = v.uOsm - (2 * (v.uNa + v.uK) + urea + glu);
    }
    return {ok: true, uag, osmGap: gap, nh4: gap === null ? null : gap / 2};
  }
  const P_MG = 3.097; // phosphate mg/dL = mmol/L × 3.097
  function phosphate(o) {
    const r = read(o, [['uP', 'urine phosphate', 0.01, 500], ['pP', 'plasma phosphate', 0.1, 20], ['uCr', 'urine creatinine', 0.01, 50000], ['pCr', 'plasma creatinine', 0.01, 3000]]); if (r.err) return r.err;
    const v = r.vals, fe = v.uP * v.pCr / (v.pP * v.uCr), trp = 1 - fe;
    if (trp <= 0) return bad('uP', 'Fractional excretion is 100% or more; check that urine and plasma values use the same units.');
    const pMmol = o.pUnit === 'mgdl' ? v.pP / P_MG : v.pP;
    if (pMmol < 0.1 || pMmol > 5) return bad('pP', 'Plasma phosphate is outside the expected range; check the unit.');
    const tmp = trp <= 0.86 ? trp * pMmol : (0.3 * trp / (1 - 0.8 * trp)) * pMmol;
    return {ok: true, fe: fe * 100, trp, tmp, tmpMg: tmp * P_MG, low: pMmol < 0.8};
  }
  function magnesium(o) {
    const r = read(o, [['uMg', 'urine magnesium', 0.01, 100], ['pMg', 'plasma magnesium', 0.05, 10], ['uCr', 'urine creatinine', 0.01, 50000], ['pCr', 'plasma creatinine', 0.01, 3000]]); if (r.err) return r.err;
    const v = r.vals, fe = 100 * v.uMg * v.pCr / (0.7 * v.pMg * v.uCr);
    return {ok: true, fe};
  }
  return {num, tbwFraction, INFUSATES, naGlucose, hyponatremia, freeWater, correctedCalcium, osmolalGap, anionGap, winters, fractionalExcretion, akiStage, proteinuria, ufRate, crrt, pdKtv, tsat, ganzoni, watson, potassium, urineAnionGap, phosphate, magnesium};
})();
if (typeof module !== 'undefined') module.exports = NephroMath;
