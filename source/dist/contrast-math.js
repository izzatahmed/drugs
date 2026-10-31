'use strict';
// Contrast-associated AKI risk. Pure functions only: nothing is stored, exported or sent.
// IV contrast: ACR–NKF consensus statements (Davenport et al., Kidney Med 2020;2:85–93).
// Intra-arterial / PCI: Mehran risk score (Mehran et al., J Am Coll Cardiol 2004;44:1393–9), eGFR version.
const ContrastMath = (() => {
  const num = v => (v === '' || v === null || v === undefined) ? NaN : Number(v);
  const fail = (field, message) => ({ok: false, field, message});
  function iv(input) {
    const dialysis = input.dialysis || 'none';
    if (!['none', 'nonanuric', 'anuric'].includes(dialysis)) return fail('ca-dialysis', 'Choose the dialysis status.');
    if (dialysis === 'anuric') return {ok: true, level: 'none', title: 'Anuric on maintenance dialysis',
      advice: ['No residual kidney function is at risk from the contrast.', 'Prophylaxis is not indicated, and dialysis should not be started early or rescheduled because of the contrast.']};
    if (dialysis === 'nonanuric') return {ok: true, level: 'high', title: 'High-risk group: on dialysis with residual urine output',
      advice: ['Patients on dialysis who still pass urine are in the ACR–NKF high-risk group (residual function may be at risk).', 'IV saline prophylaxis is not indicated in dialysis patients.', 'Dialysis should not be started or rescheduled solely because of the contrast.', 'Use the standard diagnostic dose; do not withhold a necessary study.']};
    const egfr = num(input.egfr);
    if (!input.aki && !(Number.isFinite(egfr) && egfr > 0 && egfr <= 200)) return fail('ca-egfr', 'Enter a stable eGFR between 1 and 200 mL/min/1.73 m², or tick acute kidney injury.');
    const common = ['Do not withhold a necessary contrast study because of kidney risk alone; use the standard diagnostic dose rather than an ad hoc lower one.'];
    if (input.aki || egfr < 30) return {ok: true, level: 'high', title: input.aki ? 'High risk: acute kidney injury' : 'High risk: eGFR <30 mL/min/1.73 m²',
      advice: ['IV isotonic (normal) saline prophylaxis is indicated unless contraindicated, for example by heart failure or volume overload.', 'Withhold nonessential nephrotoxic drugs when feasible; withhold metformin.', ...common]};
    if (egfr < 45) return {ok: true, level: 'intermediate', title: 'eGFR 30–44 mL/min/1.73 m²',
      advice: ['Prophylaxis is optional: it may be considered in individual high-risk circumstances at the ordering clinician’s discretion.', 'Metformin: decide individually (the CI-AKI risk is low at eGFR 30 or more).', ...common]};
    return {ok: true, level: 'low', title: 'Stable eGFR ≥45 mL/min/1.73 m²',
      advice: ['Prophylaxis is not indicated.', ...common]};
  }
  const BANDS = [
    {max: 5, label: 'Low', cin: '7.5%', dialysis: '0.04%'},
    {max: 10, label: 'Moderate', cin: '14.0%', dialysis: '0.12%'},
    {max: 15, label: 'High', cin: '26.1%', dialysis: '1.09%'},
    {max: Infinity, label: 'Very high', cin: '57.3%', dialysis: '12.6%'}];
  function mehran(input) {
    const egfr = num(input.egfr), volume = num(input.volume);
    if (!(Number.isFinite(egfr) && egfr > 0 && egfr <= 200)) return fail('ca-m-egfr', 'Enter the baseline eGFR (1–200 mL/min/1.73 m²).');
    if (!(Number.isFinite(volume) && volume >= 0 && volume <= 2000)) return fail('ca-volume', 'Enter the contrast volume in mL (0–2000).');
    const items = [];
    const add = (on, points, label) => { if (on) items.push([label, points]); };
    add(input.hypotension, 5, 'Hypotension');
    add(input.iabp, 5, 'Intra-aortic balloon pump');
    add(input.chf, 5, 'Congestive heart failure');
    add(input.age75, 4, 'Age >75 years');
    add(input.anaemia, 3, 'Anaemia');
    add(input.diabetes, 3, 'Diabetes');
    const vp = Math.floor(volume / 100); add(vp > 0, vp, `Contrast ${volume} mL`);
    const gp = egfr < 20 ? 6 : egfr < 40 ? 4 : egfr < 60 ? 2 : 0; add(gp > 0, gp, `eGFR ${egfr}`);
    const score = items.reduce((s, [, p]) => s + p, 0);
    const band = BANDS.find(b => score <= b.max);
    return {ok: true, score, items, band};
  }
  return {iv, mehran, BANDS};
})();
