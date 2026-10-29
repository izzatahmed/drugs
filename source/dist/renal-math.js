'use strict';
// Published equations; UI and storage are deliberately outside this calculation module.
const RenalMath = Object.freeze({
  toMgDl(value, unit) {
    if (!['mgdl', 'umol'].includes(unit)) return NaN;
    return unit === 'umol' ? value / 88.4 : value;
  },
  compute(input) {
    const fail = (field, message) => ({ok:false, field, message});
    const number = value => value === null || value === undefined || String(value).trim() === '' ? NaN : Number(value);
    if (!['ckdepi2021', 'mdrd'].includes(input.equation)) return fail('calc-equation', 'Choose a supported equation.');
    if (input.context === 'dialysis') return fail('calc-context', 'No eGFR is calculated during dialysis. Use the drug’s modality-specific IHD, PD, CRRT or PIRRT guidance and assess residual function separately.');
    if (input.context === 'aki') return fail('calc-context', 'No result: these steady-state equations are unreliable in AKI or changing creatinine. Review the clinical trend and use an appropriate renal assessment.');
    if (input.context === 'pregnancy') return fail('calc-context', 'No result: standard CKD-EPI/MDRD estimates are not suitable for assessing kidney function in pregnancy. Use obstetric/renal guidance.');
    if (input.context !== 'stable') return fail('calc-context', 'Choose the clinical setting. This calculator is for stable kidney function outside pregnancy and dialysis.');
    const age = number(input.age);
    if (!Number.isFinite(age) || age < 18 || age > 120) return fail('calc-age', 'Enter an adult age from 18 to 120 years. This calculator does not cover children.');
    if (!['female', 'male'].includes(input.sex)) return fail('calc-sex', 'Choose the sex parameter used by the published equation.');
    const creatinine = number(input.creatinine);
    const scr = this.toMgDl(creatinine, input.unit);
    if (!Number.isFinite(scr) || scr <= 0) return fail('calc-creatinine', 'Enter a positive, quantified serum creatinine and check its units. Do not enter a result reported only as less than or greater than an assay limit.');
    const female = input.sex === 'female';
    let indexed;
    if (input.equation === 'ckdepi2021') {
      const ratio = scr / (female ? 0.7 : 0.9);
      indexed = 142 * Math.pow(Math.min(ratio, 1), female ? -0.241 : -0.302) * Math.pow(Math.max(ratio, 1), -1.200) * Math.pow(0.9938, age) * (female ? 1.012 : 1);
    } else {
      // IDMS 175 coefficient. Historical race multiplier is intentionally omitted.
      indexed = 175 * Math.pow(scr, -1.154) * Math.pow(age, -0.203) * (female ? 0.742 : 1);
    }
    let bsa = null, absolute = null;
    if (input.deindex) {
      const height = number(input.height), weight = number(input.weight);
      if (!Number.isFinite(height) || height < 50 || height > 250) return fail('calc-height', 'Enter height in cm (50–250) for the optional body-size calculation.');
      if (!Number.isFinite(weight) || weight < 10 || weight > 500) return fail('calc-weight', 'Enter weight in kg (10–500) for the optional body-size calculation.');
      bsa = Math.sqrt(height * weight / 3600);
      absolute = indexed * bsa / 1.73;
    }
    if (!Number.isFinite(indexed) || indexed <= 0 || (input.deindex && !Number.isFinite(absolute))) return fail('calc-creatinine', 'No finite estimate could be calculated. Recheck the laboratory value and units.');
    const warnings = [];
    if (input.equation === 'mdrd') warnings.push('Legacy MDRD: the original race multiplier is omitted. Prefer CKD-EPI 2021 for a current race-free estimate.');
    if (scr < 0.2 || scr > 20) warnings.push('Unusual creatinine value: verify the units and laboratory report. Creatinine-based estimates may be misleading at extremes.');
    if (age <= 25) warnings.push('Age 18–25: consider comparison with a CKiD U25 estimate, as advised by NIDDK. This app does not calculate U25.');
    return {ok:true, equation:input.equation, indexed, absolute, bsa, scrMgDl:scr, warnings};
  }
});
