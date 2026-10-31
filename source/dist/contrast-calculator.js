'use strict';
(function setupContrastCalculator(){
  const panel = document.querySelector('#contrast-calculator');
  const form = document.querySelector('#contrast-form');
  const result = document.querySelector('#ca-result');
  const el = id => document.getElementById(id);
  const route = () => form.querySelector('input[name="ca-route"]:checked')?.value === 'pci' ? 'pci' : 'iv';
  const placeholder = '<p class="calc-placeholder">Enter the values above to see the risk group. Nothing is saved or sent.</p>';
  function layout() {
    const pci = route() === 'pci';
    el('ca-iv-fields').hidden = pci; el('ca-iv-fields').disabled = pci;
    el('ca-pci-fields').hidden = !pci; el('ca-pci-fields').disabled = !pci;
    el('ca-egfr-field').hidden = pci || el('ca-dialysis').value !== 'none';
  }
  function reset() { form.reset(); layout(); form.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid')); result.innerHTML = placeholder; }
  function renderIv(a) {
    return `<div class="calc-output ca-${a.level}"><div class="calc-output-label">IV iodinated contrast · ACR–NKF consensus</div><div class="ca-title">${h(a.title)}</div><ul class="ca-advice">${a.advice.map(x => `<li>${h(x)}</li>`).join('')}</ul></div>`;
  }
  function renderMehran(a) {
    const rows = a.items.length ? a.items.map(([l, p]) => `<tr><th scope="row">${h(l)}</th><td>${p}</td></tr>`).join('') : '<tr><th scope="row">No risk factors</th><td>0</td></tr>';
    return `<div class="calc-output"><div class="calc-output-label">Mehran score · coronary angiography / PCI</div><div class="calc-number">${a.score} <span>points · ${h(a.band.label)} risk</span></div>`
      + `<p>Published risk in the derivation cohort: contrast-induced nephropathy ${h(a.band.cin)}; dialysis ${h(a.band.dialysis)}.</p>`
      + `<table class="calc-crcl-table"><thead><tr><th scope="col">Factor</th><th scope="col">Points</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  }
  function update(focusError = false) {
    layout();
    form.querySelectorAll('[aria-invalid]').forEach(n => n.removeAttribute('aria-invalid'));
    const pci = route() === 'pci';
    const a = pci
      ? ContrastMath.mehran({egfr: el('ca-m-egfr').value, volume: el('ca-volume').value, hypotension: el('ca-hypotension').checked, iabp: el('ca-iabp').checked, chf: el('ca-chf').checked, age75: el('ca-age').checked, anaemia: el('ca-anaemia').checked, diabetes: el('ca-diabetes').checked})
      : ContrastMath.iv({egfr: el('ca-egfr').value, aki: el('ca-aki').checked, dialysis: el('ca-dialysis').value});
    if (!a.ok) { result.innerHTML = `<p class="calc-error">${h(a.message)}</p>`; el(a.field)?.setAttribute('aria-invalid', 'true'); if (focusError) el(a.field)?.focus(); return false; }
    result.innerHTML = pci ? renderMehran(a) : renderIv(a);
    return true;
  }
  document.addEventListener('click', event => {
    if (event.target.closest('[data-open="contrast-calculator"]')) {
      document.querySelector('#calculator')?.open && document.querySelector('#calculator').close();
      panel.showModal(); form.querySelector('input[name="ca-route"]:checked').focus();
    }
  });
  el('close-contrast-calculator').addEventListener('click', () => panel.close());
  panel.addEventListener('close', reset);
  window.addEventListener('pagehide', reset);
  form.addEventListener('submit', event => { event.preventDefault(); if (update(true)) result.scrollIntoView({block: 'nearest', behavior: 'smooth'}); });
  form.addEventListener('input', () => update());
  form.addEventListener('change', () => update());
  el('ca-clear').addEventListener('click', () => { reset(); form.querySelector('input[name="ca-route"]:checked').focus(); });
  reset();
})();
