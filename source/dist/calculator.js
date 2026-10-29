'use strict';
(function setupKidneyCalculator(){
  const panel = document.querySelector('#calculator');
  const form = document.querySelector('#renal-calculator-form');
  const result = document.querySelector('#calc-result');
  const el = id => document.getElementById(id);
  let previousUnit = 'mgdl';
  const equationNames = {ckdepi2021:'CKD-EPI 2021 · creatinine · race-free',mdrd:'MDRD · IDMS 175 · legacy, race multiplier omitted'};
  function reset() {
    form.reset(); previousUnit = 'mgdl';
    el('calc-body-fields').hidden = true;
    el('calc-body-fields').disabled = true;
    el('calc-legacy-note').hidden = true;
    form.querySelectorAll('[aria-invalid]').forEach(node=>node.removeAttribute('aria-invalid'));
    result.innerHTML = '<p class="calc-placeholder">Enter the values above to see an estimate. Nothing is saved or sent.</p>';
  }
  function update(focusError=false) {
    const deindex = el('calc-deindex').checked;
    el('calc-body-fields').hidden = !deindex;
    el('calc-body-fields').disabled = !deindex;
    el('calc-legacy-note').hidden = el('calc-equation').value !== 'mdrd';
    form.querySelectorAll('[aria-invalid]').forEach(node=>node.removeAttribute('aria-invalid'));
    const answer = RenalMath.compute({equation:el('calc-equation').value,age:el('calc-age').value,sex:el('calc-sex').value,creatinine:el('calc-creatinine').value,unit:el('calc-unit').value,context:el('calc-context').value,deindex,height:el('calc-height').value,weight:el('calc-weight').value});
    if (!answer.ok) {
      result.innerHTML = `<p class="calc-error">${h(answer.message)}</p>`;
      el(answer.field)?.setAttribute('aria-invalid','true');
      if (focusError) el(answer.field)?.focus();
      return;
    }
    result.innerHTML = `<div class="calc-output"><div class="calc-output-label">${h(equationNames[answer.equation])}</div><div class="calc-number">${answer.indexed.toFixed(1)} <span>mL/min/1.73 m²</span></div><p>Indexed eGFR · creatinine ${Number(answer.scrMgDl.toPrecision(6))} mg/dL</p>${answer.absolute===null?'':`<div class="calc-absolute"><strong>${answer.absolute.toFixed(1)} <span>mL/min</span></strong><p>Non-indexed eGFR · Mosteller BSA ${answer.bsa.toFixed(3)} m²</p></div>`}</div>${answer.warnings.map(note=>`<p class="calc-warning">${h(note)}</p>`).join('')}<p class="calc-precision">Estimate, not measured GFR. Values are displayed to one decimal; do not select a dose solely from a rounded cutoff or diagnose CKD from one result.</p>`;
  }
  document.addEventListener('click', event=>{
    if (event.target.closest('[data-open="calculator"]')) {panel.showModal();el('calc-age').focus();}
  });
  el('close-calculator').addEventListener('click',()=>panel.close());
  panel.addEventListener('close',reset);
  window.addEventListener('pagehide',reset);
  form.addEventListener('submit',event=>{event.preventDefault();update(true);});
  form.addEventListener('input',event=>{if(event.target.id!=='calc-unit')update();});
  form.addEventListener('change',event=>{
    if (event.target.id === 'calc-unit') {
      const value = el('calc-creatinine').valueAsNumber, next = event.target.value;
      if (Number.isFinite(value) && value > 0 && next !== previousUnit) {
        const converted = next === 'umol' ? value * 88.4 : value / 88.4;
        el('calc-creatinine').value = String(Number(converted.toPrecision(12)));
      }
      previousUnit = next;
    }
    update();
  });
  el('calc-clear').addEventListener('click',()=>{reset();el('calc-age').focus();});
  reset();
})();
