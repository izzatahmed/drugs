'use strict';
// CKD risk (KDIGO 2024 G/A categories and heat map), Kidney Failure Risk Equation (4-variable; Tangri, JAMA 2011 and 2016 recalibration),
// body size (BMI, Mosteller BSA, Devine IBW, adjusted weight) and haemodialysis adequacy (URR; Daugirdas second-generation spKt/V, KDOQI 2015).
// Pure functions only: nothing is stored, exported or sent.
const KidneyTools = (() => {
  const num = v => (v === '' || v === null || v === undefined) ? NaN : Number(v);
  const fail = (field, message) => ({ok: false, field, message});
  const G = [[90, 'G1', 'Normal or high'], [60, 'G2', 'Mildly decreased'], [45, 'G3a', 'Mildly to moderately decreased'], [30, 'G3b', 'Moderately to severely decreased'], [15, 'G4', 'Severely decreased'], [0, 'G5', 'Kidney failure']];
  const RISK = {G1: ['low', 'moderate', 'high'], G2: ['low', 'moderate', 'high'], G3a: ['moderate', 'high', 'very high'], G3b: ['high', 'very high', 'very high'], G4: ['very high', 'very high', 'very high'], G5: ['very high', 'very high', 'very high']};
  const gStage = egfr => G.find(([lo]) => egfr >= lo);
  const aStage = acrMgG => acrMgG < 30 ? ['A1', 'Normal to mildly increased'] : acrMgG <= 300 ? ['A2', 'Moderately increased'] : ['A3', 'Severely increased'];
  function ckd(input) {
    const egfr = num(input.egfr), raw = num(input.acr);
    if (!(Number.isFinite(egfr) && egfr > 0 && egfr <= 200)) return fail('ck-egfr', 'Enter eGFR (1–200 mL/min/1.73 m²).');
    if (!(Number.isFinite(raw) && raw > 0)) return fail('ck-acr', 'Enter a positive urine albumin-to-creatinine ratio.');
    const mgG = input.acrUnit === 'mgmmol' ? raw * 8.84 : raw, mgMmol = mgG / 8.84;
    const [, g, gLabel] = gStage(egfr), [a, aLabel] = aStage(mgG);
    const risk = RISK[g][Number(a[1]) - 1];
    const out = {ok: true, egfr, mgG, mgMmol, g, gLabel, a, aLabel, risk, kfre: null, kfreNote: null};
    if (egfr >= 60) { out.kfreNote = 'KFRE applies to CKD G3–G5 (eGFR <60).'; return out; }
    const age = num(input.age), sex = input.sex;
    if (!(Number.isFinite(age) && age >= 18 && age <= 120) || !['female', 'male'].includes(sex)) { out.kfreNote = 'Add age and sex for the kidney failure risk (KFRE).'; return out; }
    out.kfre = kfre({age, male: sex === 'male', egfr, acrMgG: mgG, region: input.region});
    return out;
  }
  // 4-variable KFRE: 1 − S0^exp(−0.2201(age/10 − 7.036) + 0.2467(male − 0.5642) − 0.5567(eGFR/5 − 7.222) + 0.4510(ln ACR − 5.137)), ACR in mg/g.
  const S0 = {nonNA: {two: 0.9832, five: 0.9365}, NA: {two: 0.9750, five: 0.9240}};
  function kfre({age, male, egfr, acrMgG, region}) {
    const lp = -0.2201 * (age / 10 - 7.036) + 0.2467 * ((male ? 1 : 0) - 0.5642) - 0.5567 * (egfr / 5 - 7.222) + 0.4510 * (Math.log(acrMgG) - 5.137);
    const s = S0[region === 'NA' ? 'NA' : 'nonNA'];
    return {region: region === 'NA' ? 'NA' : 'nonNA', two: 1 - Math.pow(s.two, Math.exp(lp)), five: 1 - Math.pow(s.five, Math.exp(lp))};
  }
  function body(input) {
    const h = num(input.height), w = num(input.weight), sex = input.sex;
    if (!(Number.isFinite(h) && h >= 100 && h <= 250)) return fail('bd-height', 'Enter height 100–250 cm.');
    if (!(Number.isFinite(w) && w >= 25 && w <= 350)) return fail('bd-weight', 'Enter weight 25–350 kg.');
    const m = h / 100, bmi = w / (m * m), bsa = Math.sqrt(h * w / 3600);
    const cls = bmi < 18.5 ? 'Underweight' : bmi < 25 ? 'Healthy weight' : bmi < 30 ? 'Overweight' : bmi < 35 ? 'Obesity class I' : bmi < 40 ? 'Obesity class II' : 'Obesity class III';
    let ibw = null, adj = null;
    if (sex === 'female' || sex === 'male') {
      ibw = (sex === 'male' ? 50 : 45.5) + 2.3 * (h / 2.54 - 60);
      if (h / 2.54 < 60) ibw = null;
      if (ibw !== null && w > ibw) adj = ibw + 0.4 * (w - ibw);
    }
    return {ok: true, bmi, cls, bsa, ibw, adj, pctIbw: ibw ? 100 * w / ibw : null};
  }
  // Daugirdas second generation: spKt/V = −ln(R − 0.008 t) + (4 − 3.5 R) × UF / W; URR = 1 − R.
  function dialysis(input) {
    const pre = num(input.pre), post = num(input.post), t = num(input.hours), uf = num(input.uf), w = num(input.weight);
    if (!(Number.isFinite(pre) && pre > 0)) return fail('dl-pre', 'Enter the pre-dialysis urea (BUN).');
    if (!(Number.isFinite(post) && post > 0 && post < pre)) return fail('dl-post', 'Post-dialysis urea must be positive and lower than pre-dialysis.');
    if (!(Number.isFinite(t) && t >= 1 && t <= 10)) return fail('dl-hours', 'Session length must be 1–10 hours.');
    if (!(Number.isFinite(uf) && uf >= 0 && uf <= 10)) return fail('dl-uf', 'Ultrafiltration volume must be 0–10 L.');
    if (!(Number.isFinite(w) && w >= 25 && w <= 300)) return fail('dl-weight', 'Post-dialysis weight must be 25–300 kg.');
    const R = post / pre, arg = R - 0.008 * t;
    if (arg <= 0) return fail('dl-post', 'These values fall outside the Daugirdas equation.');
    return {ok: true, R, urr: 1 - R, ktv: -Math.log(arg) + (4 - 3.5 * R) * uf / w};
  }
  return {ckd, kfre, body, dialysis, RISK};
})();
