'use strict';
(function setupKidneyTools(){
  const el = id => document.getElementById(id);
  const pct = v => (v * 100 < 0.1 ? '<0.1' : (v * 100).toFixed(1)) + '%';
  const placeholder = '<p class="calc-placeholder">Enter the values above. Nothing is saved or sent.</p>';
  const RISKLABEL = {low: 'Low risk', moderate: 'Moderately increased risk', high: 'High risk', 'very high': 'Very high risk'};
  function heatmap(g, a) {
    const gs = ['G1', 'G2', 'G3a', 'G3b', 'G4', 'G5'], as = ['A1', 'A2', 'A3'];
    return `<table class="ck-heat" aria-label="KDIGO risk categories"><thead><tr><th></th>${as.map(x => `<th scope="col">${x}</th>`).join('')}</tr></thead><tbody>`
      + gs.map(gg => `<tr><th scope="row">${gg}</th>${as.map((aa, i) => { const r = KidneyTools.RISK[gg][i]; return `<td class="ck-${r.replace(' ', '-')}${gg === g && aa === a ? ' ck-here' : ''}">${gg === g && aa === a ? '●' : ''}</td>`; }).join('')}</tr>`).join('')
      + '</tbody></table>';
  }
  const tools = {
    'ckd-calculator': {form: 'ckd-form', result: 'ck-result', first: 'ck-egfr',
      read: () => ({egfr: el('ck-egfr').value, acr: el('ck-acr').value, acrUnit: el('ck-acr-unit').value, age: el('ck-age').value, sex: el('ck-sex').value, region: el('ck-region').value}),
      run: KidneyTools.ckd,
      render: a => `<div class="calc-output ck-out-${a.risk.replace(' ', '-')}"><div class="calc-output-label">KDIGO 2024 · ${h(a.g)} ${h(a.a)}</div><div class="ca-title">${RISKLABEL[a.risk]}</div>`
        + `<p>${h(a.g)}: ${h(a.gLabel)} · ${h(a.a)}: ${h(a.aLabel)} albuminuria. UACR ${a.mgG.toFixed(1)} mg/g = ${a.mgMmol.toFixed(1)} mg/mmol.</p>${heatmap(a.g, a.a)}`
        + (a.kfre ? `<div class="calc-absolute"><strong>${pct(a.kfre.two)} <span>2-year</span> · ${pct(a.kfre.five)} <span>5-year</span></strong><p>Kidney failure risk (KFRE, 4-variable, ${a.kfre.region === 'NA' ? 'North American' : 'non-North American'} calibration). KDIGO 2024: 5-year risk 3–5% supports nephrology referral; 2-year risk >10% multidisciplinary care; >40% kidney replacement therapy preparation (modality education, access, transplant referral).</p></div>` : `<p>${h(a.kfreNote)}</p>`)
        + '</div>'},
    'body-calculator': {form: 'body-form', result: 'bd-result', first: 'bd-height',
      read: () => ({height: el('bd-height').value, weight: el('bd-weight').value, sex: el('bd-sex').value}),
      run: KidneyTools.body,
      render: a => `<div class="calc-output"><div class="calc-output-label">Body size</div><div class="calc-number">${a.bmi.toFixed(1)} <span>kg/m² · ${h(a.cls)}</span></div>`
        + `<table class="calc-crcl-table"><tbody><tr><th scope="row">Body surface area (Mosteller)</th><td>${a.bsa.toFixed(2)} m²</td></tr>`
        + (a.ibw !== null ? `<tr><th scope="row">Ideal body weight (Devine)</th><td>${a.ibw.toFixed(1)} kg (${a.pctIbw.toFixed(0)}% of IBW)</td></tr>` : '<tr><th scope="row">Ideal body weight</th><td>Choose sex; height must be ≥152 cm (5 ft)</td></tr>')
        + (a.adj !== null ? `<tr><th scope="row">Adjusted body weight (IBW + 0.4 × excess)</th><td>${a.adj.toFixed(1)} kg</td></tr>` : '')
        + '</tbody></table><p>WHO adult BMI classes. Use the weight the drug label or local protocol specifies for dosing; oedema and ascites distort weight.</p></div>'},
    'dialysis-calculator': {form: 'dialysis-form', result: 'dl-result', first: 'dl-pre',
      read: () => ({pre: el('dl-pre').value, post: el('dl-post').value, hours: el('dl-hours').value, uf: el('dl-uf').value, weight: el('dl-weight').value}),
      run: KidneyTools.dialysis,
      render: a => `<div class="calc-output${a.ktv < 1.2 ? ' ca-high' : a.ktv < 1.4 ? ' ca-intermediate' : ''}"><div class="calc-output-label">Haemodialysis adequacy · single session</div><div class="calc-number">${a.ktv.toFixed(2)} <span>spKt/V</span></div>`
        + `<p>URR ${(a.urr * 100).toFixed(1)}%. KDOQI 2015 (thrice-weekly HD): target spKt/V 1.4 per session, minimum delivered 1.2; URR target 70%, minimum 65%.</p></div>`}
  };
  for (const [id, t] of Object.entries(tools)) {
    const panel = el(id), form = el(t.form), result = el(t.result);
    const reset = () => { form.reset(); form.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid')); result.innerHTML = placeholder; };
    const update = (focus = false) => {
      form.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid'));
      const a = t.run(t.read());
      if (!a.ok) { result.innerHTML = `<p class="calc-error">${h(a.message)}</p>`; el(a.field)?.setAttribute('aria-invalid', 'true'); if (focus) el(a.field)?.focus(); return false; }
      result.innerHTML = t.render(a); return true;
    };
    form.addEventListener('submit', e => { e.preventDefault(); if (update(true)) result.scrollIntoView({block: 'nearest', behavior: 'smooth'}); });
    form.addEventListener('input', () => update());
    form.addEventListener('change', () => update());
    panel.querySelector('.tool-clear').addEventListener('click', () => { reset(); el(t.first).focus(); });
    panel.querySelector('.tool-close').addEventListener('click', () => panel.close());
    panel.addEventListener('close', reset);
    window.addEventListener('pagehide', reset);
    reset();
  }
  document.addEventListener('click', e => {
    const o = e.target.closest('[data-open]');
    if (!o || !tools[o.dataset.open]) return;
    const menu = el('calc-menu'); if (menu.open) menu.close();
    el(o.dataset.open).showModal(); el(tools[o.dataset.open].first).focus();
  });
})();
