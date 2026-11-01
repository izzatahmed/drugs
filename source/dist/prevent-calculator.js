'use strict';
(function setupPreventCalculator(){
  const menu = document.querySelector('#calc-menu');
  const panel = document.querySelector('#prevent-calculator');
  const form = document.querySelector('#prevent-form');
  const result = document.querySelector('#pv-result');
  const el = id => document.getElementById(id);
  const placeholder = '<p class="calc-placeholder">Enter the values above to see the estimate. Nothing is saved or sent.</p>';
  const pct = v => (v * 100 < 1 ? '<1' : (v * 100).toFixed(1)) + '%';
  function reset() { form.reset(); form.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid')); result.innerHTML = placeholder; }
  function values() {
    return {sex: el('pv-sex').value, age: el('pv-age').value, tc: el('pv-tc').value, hdl: el('pv-hdl').value, cholUnit: el('pv-chol-unit').value,
      sbp: el('pv-sbp').value, bmi: el('pv-bmi').value, egfr: el('pv-egfr').value, uacr: el('pv-uacr').value, uacrUnit: el('pv-uacr-unit').value,
      dm: el('pv-dm').checked, smoking: el('pv-smoking').checked, bpTx: el('pv-bptx').checked, statin: el('pv-statin').checked};
  }
  function render(a) {
    const row = (label, ten, thirty) => `<tr><th scope="row">${label}</th><td>${pct(ten)}</td><td>${thirty === null ? '—' : pct(thirty)}</td></tr>`;
    const t = a.tenYear, s = a.thirtyYear;
    const flag = t.total_cvd >= 0.075;
    return `<div class="calc-output${flag ? ' ca-intermediate' : ''}"><div class="calc-output-label">PREVENT · ${a.model === 'uacr' ? 'base model + UACR' : 'base model'}</div>`
      + `<div class="calc-number">${pct(t.total_cvd)} <span>10-year total CVD risk</span></div>`
      + `<p>${flag ? 'At or above 7.5%: the 2025 AHA/ACC threshold that supports starting BP medication in stage 1 hypertension.' : 'Below 7.5%: in stage 1 hypertension without CKD, diabetes or CVD, the 2025 AHA/ACC guideline starts with 3–6 months of lifestyle therapy.'}</p>`
      + `<table class="calc-crcl-table"><thead><tr><th scope="col">Outcome</th><th scope="col">10-year</th><th scope="col">30-year</th></tr></thead><tbody>`
      + row('Total CVD', t.total_cvd, s && s.total_cvd) + row('ASCVD', t.ascvd, s && s.ascvd) + row('Heart failure', t.heart_failure, s && s.heart_failure)
      + `</tbody></table>${s ? '' : '<p>30-year risk is shown only for ages 30–59.</p>'}</div>`;
  }
  function update(focusError = false) {
    form.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid'));
    const a = PreventMath.compute(values());
    if (!a.ok) { result.innerHTML = `<p class="calc-error">${h(a.message)}</p>`; el(a.field)?.setAttribute('aria-invalid', 'true'); if (focusError) el(a.field)?.focus(); return false; }
    result.innerHTML = render(a); return true;
  }
  document.addEventListener('click', event => {
    const opener = event.target.closest('[data-open]');
    if (!opener) return;
    const target = opener.dataset.open;
    if (target === 'calc-menu') { menu.showModal(); menu.querySelector('button[data-open]').focus(); return; }
    if (menu.open && ['calculator', 'contrast-calculator', 'prevent-calculator'].includes(target)) menu.close();
    if (target === 'prevent-calculator') { panel.showModal(); el('pv-sex').focus(); }
  });
  el('close-calc-menu').addEventListener('click', () => menu.close());
  el('close-prevent-calculator').addEventListener('click', () => panel.close());
  panel.addEventListener('close', reset);
  window.addEventListener('pagehide', reset);
  form.addEventListener('submit', event => { event.preventDefault(); if (update(true)) result.scrollIntoView({block: 'nearest', behavior: 'smooth'}); });
  form.addEventListener('input', event => { if (event.target.id !== 'pv-chol-unit' && event.target.id !== 'pv-uacr-unit') update(); });
  let cholUnit = 'mgdl', uacrUnit = 'mgg';
  form.addEventListener('change', event => {
    if (event.target.id === 'pv-chol-unit') {
      const next = event.target.value;
      for (const id of ['pv-tc', 'pv-hdl']) { const v = el(id).valueAsNumber; if (Number.isFinite(v) && v > 0 && next !== cholUnit) el(id).value = String(Number((next === 'mmol' ? v * 0.02586 : v / 0.02586).toPrecision(4))); }
      cholUnit = next;
    }
    if (event.target.id === 'pv-uacr-unit') {
      const next = event.target.value, v = el('pv-uacr').valueAsNumber;
      if (Number.isFinite(v) && v > 0 && next !== uacrUnit) el('pv-uacr').value = String(Number((next === 'mgmmol' ? v / 8.84 : v * 8.84).toPrecision(4)));
      uacrUnit = next;
    }
    update();
  });
  panel.addEventListener('close', () => { cholUnit = 'mgdl'; uacrUnit = 'mgg'; });
  el('pv-clear').addEventListener('click', () => { reset(); el('pv-sex').focus(); });
  reset();
})();
