'use strict';
// AHA PREVENT equations (Khan et al., Circulation 2024;149:430–449; doi:10.1161/CIRCULATIONAHA.123.067626), base model and base + UACR model,
// 10-year (ages 30–79) and 30-year (ages 30–59) risk of total CVD, ASCVD and heart failure. Coefficients as published (supplement), cross-checked
// against the open-source preventr implementation (CRAN 0.12.2, 2026-10-31) and the MDCalc coefficient review. The HbA1c and SDI add-on
// models (HbA1c coefficients corrected by erratum, Circulation 2026, doi:10.1161/CIR.0000000000001491) are not implemented here.
// Pure functions only: nothing is stored, exported or sent.
const PreventMath = (() => {
  const COEF = {
  base_10yr: {terms: ["age", "non_hdl_c", "hdl_c", "sbp_lt_110", "sbp_gte_110", "dm", "smoking", "bmi_lt_30", "bmi_gte_30", "egfr_lt_60", "egfr_gte_60", "bp_tx", "statin", "bp_tx_sbp_gte_110", "statin_non_hdl_c", "age_non_hdl_c", "age_hdl_c", "age_sbp_gte_110", "age_dm", "age_smoking", "age_bmi_gte_30", "age_egfr_lt_60", "constant"],
    female_total_cvd: [0.7939329,0.0305239,-0.1606857,-0.2394003,0.3600781,0.8667604,0.5360739,0.0,0.0,0.6045917,0.0433769,0.3151672,-0.1477655,-0.0663612,0.1197879,-0.0819715,0.0306769,-0.0946348,-0.27057,-0.078715,0.0,-0.1637806,-3.307728],
    male_total_cvd: [0.7688528,0.0736174,-0.0954431,-0.4347345,0.3362658,0.7692857,0.4386871,0.0,0.0,0.5378979,0.0164827,0.288879,-0.1337349,-0.0475924,0.150273,-0.0517874,0.0191169,-0.1049477,-0.2251948,-0.0895067,0.0,-0.1543702,-3.031168],
    female_ascvd: [0.719883,0.1176967,-0.151185,-0.0835358,0.3592852,0.8348585,0.4831078,0.0,0.0,0.4864619,0.0397779,0.2265309,-0.0592374,-0.0395762,0.0844423,-0.0567839,0.0325692,-0.1035985,-0.2417542,-0.0791142,0.0,-0.1671492,-3.819975],
    male_ascvd: [0.7099847,0.1658663,-0.1144285,-0.2837212,0.3239977,0.7189597,0.3956973,0.0,0.0,0.3690075,0.0203619,0.2036522,-0.0865581,-0.0322916,0.114563,-0.0300005,0.0232747,-0.0927024,-0.2018525,-0.0970527,0.0,-0.1217081,-3.500655],
    female_heart_failure: [0.8998235,0.0,0.0,-0.4559771,0.3576505,1.038346,0.583916,-0.0072294,0.2997706,0.7451638,0.0557087,0.3534442,0.0,-0.0981511,0.0,0.0,0.0,-0.0946663,-0.3581041,-0.1159453,-0.003878,-0.1884289,-4.310409],
    male_heart_failure: [0.8972642,0.0,0.0,-0.6811466,0.3634461,0.923776,0.5023736,-0.0485841,0.3726929,0.6926917,0.0251827,0.2980922,0.0,-0.0497731,0.0,0.0,0.0,-0.1289201,-0.3040924,-0.1401688,0.0068126,-0.1797778,-3.946391]},
  base_30yr: {terms: ["age", "age_squared", "non_hdl_c", "hdl_c", "sbp_lt_110", "sbp_gte_110", "dm", "smoking", "bmi_lt_30", "bmi_gte_30", "egfr_lt_60", "egfr_gte_60", "bp_tx", "statin", "bp_tx_sbp_gte_110", "statin_non_hdl_c", "age_non_hdl_c", "age_hdl_c", "age_sbp_gte_110", "age_dm", "age_smoking", "age_bmi_gte_30", "age_egfr_lt_60", "constant"],
    female_total_cvd: [0.5503079,-0.0928369,0.0409794,-0.1663306,-0.1628654,0.3299505,0.6793894,0.3196112,0.0,0.0,0.1857101,0.0553528,0.2894,-0.075688,-0.056367,0.1071019,-0.0751438,0.0301786,-0.0998776,-0.3206166,-0.1607862,0.0,-0.1450788,-1.318827],
    male_total_cvd: [0.4627309,-0.0984281,0.0836088,-0.1029824,-0.2140352,0.2904325,0.5331276,0.2141914,0.0,0.0,0.1155556,0.0603775,0.232714,-0.0272112,-0.0384488,0.134192,-0.0511759,0.0165865,-0.1101437,-0.2585943,-0.1566406,0.0,-0.1166776,-1.148204],
    female_ascvd: [0.4669202,-0.0893118,0.1256901,-0.1542255,-0.0018093,0.322949,0.6296707,0.268292,0.0,0.0,0.100106,0.0499663,0.1875292,0.0152476,-0.0276123,0.0736147,-0.0521962,0.0316918,-0.1046101,-0.2727793,-0.1530907,0.0,-0.1299149,-1.974074],
    male_ascvd: [0.3994099,-0.0937484,0.1744643,-0.120203,-0.0665117,0.2753037,0.4790257,0.1782635,0.0,0.0,-0.0218789,0.0602553,0.1421182,0.0135996,-0.0218265,0.1013148,-0.0312619,0.020673,-0.0920935,-0.2159947,-0.1548811,0.0,-0.0712547,-1.736444],
    female_heart_failure: [0.6254374,-0.0983038,0.0,0.0,-0.3919241,0.3142295,0.8330787,0.3438651,0.0594874,0.2525536,0.2981642,0.0667159,0.333921,0.0,-0.0893177,0.0,0.0,0.0,-0.0974299,-0.404855,-0.1982991,-0.0035619,-0.1564215,-2.205379],
    male_heart_failure: [0.5681541,-0.1048388,0.0,0.0,-0.4761564,0.30324,0.6840338,0.2656273,0.0833107,0.26999,0.2541805,0.0638923,0.2583631,0.0,-0.0391938,0.0,0.0,0.0,-0.1269124,-0.3273572,-0.2043019,-0.0182831,-0.1342618,-1.95751]},
  uacr_10yr: {terms: ["age", "non_hdl_c", "hdl_c", "sbp_lt_110", "sbp_gte_110", "dm", "smoking", "bmi_lt_30", "bmi_gte_30", "egfr_lt_60", "egfr_gte_60", "bp_tx", "statin", "bp_tx_sbp_gte_110", "statin_non_hdl_c", "age_non_hdl_c", "age_hdl_c", "age_sbp_gte_110", "age_dm", "age_smoking", "age_bmi_gte_30", "age_egfr_lt_60", "ln_uacr", "missing_uacr", "constant"],
    female_total_cvd: [0.7969249,0.0256635,-0.1588107,-0.2255701,0.3396649,0.8047515,0.5285338,0.0,0.0,0.4803511,0.0434472,0.2985207,-0.1497787,-0.0742889,0.106756,-0.0778126,0.0306768,-0.0907168,-0.2705122,-0.0830564,0.0,-0.1389249,0.1793037,0.0132073,-3.738341],
    male_total_cvd: [0.7768655,0.0659949,-0.0951111,-0.420667,0.3120151,0.698521,0.4314669,0.0,0.0,0.3841364,0.009384,0.2676494,-0.1390966,-0.0579315,0.1383719,-0.0488332,0.0200406,-0.102454,-0.2236355,-0.089485,0.0,-0.1321848,0.1887974,0.0916979,-3.510705],
    female_ascvd: [0.7201999,0.1135771,-0.1493506,-0.0726677,0.3436259,0.7773094,0.4746662,0.0,0.0,0.3824646,0.0394178,0.2125182,-0.0603046,-0.0466053,0.0733118,-0.0534262,0.0325689,-0.0999887,-0.2411762,-0.0826941,0.0,-0.1444737,0.1501217,0.0050257,-4.174614],
    male_ascvd: [0.7141718,0.1602194,-0.1139086,-0.2719456,0.3058719,0.6600631,0.3884022,0.0,0.0,0.2466316,0.0151852,0.186167,-0.0894395,-0.0411884,0.1058212,-0.028089,0.0240427,-0.0912325,-0.2004894,-0.096936,0.0,-0.1022867,0.1510073,0.0556,-3.85146],
    female_heart_failure: [0.9145975,0.0,0.0,-0.4441346,0.3260323,0.9611365,0.5755787,0.0008831,0.2988964,0.5915291,0.0556823,0.3314097,0.0,-0.1078596,0.0,0.0,0.0,-0.0875231,-0.356859,-0.1220248,-0.0053637,-0.1610389,0.2197281,0.0326667,-4.841506],
    male_heart_failure: [0.9111795,0.0,0.0,-0.6693649,0.3290082,0.8377655,0.4978917,-0.042749,0.3624165,0.5075796,0.0137716,0.2739963,0.0,-0.0645712,0.0,0.0,0.0,-0.1230039,-0.3013297,-0.1410318,0.0021531,-0.1548018,0.2306299,0.1472194,-4.556907]},
  uacr_30yr: {terms: ["age", "age_squared", "non_hdl_c", "hdl_c", "sbp_lt_110", "sbp_gte_110", "dm", "smoking", "bmi_lt_30", "bmi_gte_30", "egfr_lt_60", "egfr_gte_60", "bp_tx", "statin", "bp_tx_sbp_gte_110", "statin_non_hdl_c", "age_non_hdl_c", "age_hdl_c", "age_sbp_gte_110", "age_dm", "age_smoking", "age_bmi_gte_30", "age_egfr_lt_60", "ln_uacr", "missing_uacr", "constant"],
    female_total_cvd: [0.5491768,-0.0937311,0.0359847,-0.1642965,-0.1483404,0.313353,0.6253766,0.3147172,0.0,0.0,0.1094663,0.0550705,0.2782433,-0.0786239,-0.0628947,0.093204,-0.0710685,0.0306363,-0.0951455,-0.3168231,-0.1636391,0.0,-0.1265483,0.1142251,-0.0055863,-1.583738],
    male_total_cvd: [0.464491,-0.0998895,0.0757606,-0.1031778,-0.1990714,0.2715816,0.4754637,0.2069672,0.0,0.0,0.0331103,0.0540474,0.2189911,-0.0331044,-0.04534,0.1214535,-0.0483995,0.0178997,-0.1059324,-0.2492861,-0.1561543,0.0,-0.1012429,0.1007571,0.0572456,-1.398727],
    female_ascvd: [0.4629669,-0.0902777,0.1215214,-0.1522069,0.0092679,0.3113609,0.581256,0.263167,0.0,0.0,0.0391726,0.0492959,0.1786178,0.0131058,-0.0325135,0.0617093,-0.0489189,0.0321079,-0.1003185,-0.2684574,-0.1547301,0.0,-0.1130703,0.0903471,-0.0145818,-2.178888],
    male_ascvd: [0.3995607,-0.094557,0.1686692,-0.1202145,-0.0555561,0.2633566,0.4362036,0.1716233,0.0,0.0,-0.0775282,0.0561236,0.1319331,0.0102428,-0.0269294,0.0920557,-0.0297021,0.0217935,-0.0893347,-0.2081467,-0.1542716,0.0,-0.0597254,0.0684872,0.0193962,-1.873449],
    female_heart_failure: [0.6319513,-0.1009284,0.0,0.0,-0.3787175,0.2863393,0.7631221,0.3355843,0.0677084,0.2517238,0.1940067,0.0664006,0.3171436,0.0,-0.0970661,0.0,0.0,0.0,-0.0896239,-0.400743,-0.2042041,-0.0054699,-0.13602,0.1486028,0.011608,-2.538952],
    male_heart_failure: [0.5750236,-0.1062268,0.0,0.0,-0.4633994,0.2742874,0.612208,0.2614987,0.0895459,0.2632424,0.1430472,0.0535184,0.2417468,0.0,-0.0498574,0.0,0.0,0.0,-0.1193827,-0.316651,-0.2046122,-0.0216878,-0.1165637,0.1366452,0.1078355,-2.314872]}
  };
  const MGDL_TO_MMOL = 0.02586;
  const RANGES = {age: [30, 79], sbp: [90, 180], bmi: [18.5, 39.9], egfr: [15, 140], uacr: [0.1, 25000],
    tc: {mgdl: [130, 320], mmol: [3.36, 8.28]}, hdl: {mgdl: [20, 100], mmol: [0.52, 2.59]}};
  const num = v => (v === '' || v === null || v === undefined) ? NaN : Number(v);
  const fail = (field, message) => ({ok: false, field, message});
  const inRange = (v, [lo, hi]) => Number.isFinite(v) && v >= lo && v <= hi;
  function terms(x) {
    const age = (x.age - 55) / 10, nonHdl = x.tcMmol - x.hdlMmol - 3.5, hdl = (x.hdlMmol - 1.3) / 0.3;
    const sbpLt = (Math.min(x.sbp, 110) - 110) / 20, sbpGte = (Math.max(x.sbp, 110) - 130) / 20;
    const bmiLt = (Math.min(x.bmi, 30) - 25) / 5, bmiGte = (Math.max(x.bmi, 30) - 30) / 5;
    const egfrLt = (Math.min(x.egfr, 60) - 60) / -15, egfrGte = (Math.max(x.egfr, 60) - 90) / -15;
    const dm = x.dm ? 1 : 0, smoking = x.smoking ? 1 : 0, bpTx = x.bpTx ? 1 : 0, statin = x.statin ? 1 : 0;
    return {age, age_squared: age * age, non_hdl_c: nonHdl, hdl_c: hdl, sbp_lt_110: sbpLt, sbp_gte_110: sbpGte, dm, smoking,
      bmi_lt_30: bmiLt, bmi_gte_30: bmiGte, egfr_lt_60: egfrLt, egfr_gte_60: egfrGte, bp_tx: bpTx, statin,
      bp_tx_sbp_gte_110: bpTx * sbpGte, statin_non_hdl_c: statin * nonHdl, age_non_hdl_c: age * nonHdl, age_hdl_c: age * hdl,
      age_sbp_gte_110: age * sbpGte, age_dm: age * dm, age_smoking: age * smoking, age_bmi_gte_30: age * bmiGte, age_egfr_lt_60: age * egfrLt,
      ln_uacr: x.uacr === null ? 0 : Math.log(x.uacr), missing_uacr: x.uacr === null ? 1 : 0, constant: 1};
  }
  function risk(model, t, sex, outcome) {
    const m = COEF[model], beta = m[`${sex}_${outcome}`];
    const lp = m.terms.reduce((s, name, i) => s + beta[i] * t[name], 0);
    return Math.exp(lp) / (1 + Math.exp(lp));
  }
  function compute(input) {
    const sex = input.sex;
    if (sex !== 'female' && sex !== 'male') return fail('pv-sex', 'Choose the sex used by the equations.');
    const age = num(input.age);
    if (!inRange(age, RANGES.age)) return fail('pv-age', 'PREVENT is for ages 30–79 years.');
    const unit = input.cholUnit === 'mmol' ? 'mmol' : 'mgdl';
    const tc = num(input.tc), hdl = num(input.hdl);
    if (!inRange(tc, RANGES.tc[unit])) return fail('pv-tc', `Total cholesterol must be ${RANGES.tc[unit].join('–')} ${unit === 'mmol' ? 'mmol/L' : 'mg/dL'}.`);
    if (!inRange(hdl, RANGES.hdl[unit])) return fail('pv-hdl', `HDL cholesterol must be ${RANGES.hdl[unit].join('–')} ${unit === 'mmol' ? 'mmol/L' : 'mg/dL'}.`);
    const sbp = num(input.sbp);
    if (!inRange(sbp, RANGES.sbp)) return fail('pv-sbp', 'Systolic BP must be 90–180 mmHg.');
    const bmi = num(input.bmi);
    if (!inRange(bmi, RANGES.bmi)) return fail('pv-bmi', 'BMI must be 18.5–39.9 kg/m² (the derivation range).');
    const egfr = num(input.egfr);
    if (!inRange(egfr, RANGES.egfr)) return fail('pv-egfr', 'eGFR must be 15–140 mL/min/1.73 m².');
    let uacr = null;
    if (input.uacr !== '' && input.uacr !== null && input.uacr !== undefined) {
      const raw = num(input.uacr), mg = input.uacrUnit === 'mgmmol' ? raw * 8.84 : raw;
      if (!Number.isFinite(raw) || raw <= 0) return fail('pv-uacr', 'Enter a positive UACR or leave it blank.');
      uacr = Math.min(Math.max(mg, 0.1), 25000);
    }
    const x = {age, sbp, bmi, egfr, uacr, dm: !!input.dm, smoking: !!input.smoking, bpTx: !!input.bpTx, statin: !!input.statin,
      tcMmol: unit === 'mmol' ? tc : tc * MGDL_TO_MMOL, hdlMmol: unit === 'mmol' ? hdl : hdl * MGDL_TO_MMOL};
    const t = terms(x), model = uacr === null ? 'base' : 'uacr';
    const out = years => ({total_cvd: risk(`${model}_${years}`, t, sex, 'total_cvd'), ascvd: risk(`${model}_${years}`, t, sex, 'ascvd'), heart_failure: risk(`${model}_${years}`, t, sex, 'heart_failure')});
    return {ok: true, model, tenYear: out('10yr'), thirtyYear: age <= 59 ? out('30yr') : null};
  }
  return {compute, RANGES};
})();
