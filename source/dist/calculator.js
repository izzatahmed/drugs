'use strict';
(function setupKidneyCalculator(){
  const panel = document.querySelector('#calculator');
  const form = document.querySelector('#renal-calculator-form');
  const result = document.querySelector('#calc-result');
  const el = id => document.getElementById(id);
  let previousUnit = 'mgdl';
  const equationNames = {ckdepi2021:'CKD-EPI 2021 · creatinine · race-free',mdrd:'MDRD · IDMS 175 · legacy, race multiplier omitted'};
  const measure = () => form.querySelector('input[name="calc-measure"]:checked')?.value === 'crcl' ? 'crcl' : 'egfr';
  const mg = value => Number(value.toFixed(2));
  function layout() {
    const crcl = measure() === 'crcl';
    el('calc-equation-field').hidden = crcl;
    el('calc-deindex-field').hidden = crcl;
    el('calc-legacy-note').hidden = crcl || el('calc-equation').value !== 'mdrd';
    const showBody = crcl || el('calc-deindex').checked;
    el('calc-body-fields').hidden = !showBody;
    el('calc-body-fields').disabled = !showBody;
    el('calc-body-legend').textContent = crcl ? 'Body size for creatinine clearance' : 'Body size for non-indexed eGFR';
    el('calc-weight-label').textContent = crcl ? 'Actual weight · kg (required)' : 'Weight · kg';
    el('calc-height-label').textContent = crcl ? 'Height · cm (for ideal/adjusted weight)' : 'Height · cm';
    el('calc-body-note').textContent = crcl ? 'Height is optional: without it only actual-weight CrCl is shown. Oedema, ascites and amputation distort weight.' : 'Mosteller BSA. Body-size extremes and oedema require clinical judgement.';
  }
  function reset() {
    form.reset(); previousUnit = 'mgdl';
    layout();
    form.querySelectorAll('[aria-invalid]').forEach(node=>node.removeAttribute('aria-invalid'));
    result.innerHTML = '<p class="calc-placeholder">Enter the values above to see an estimate. Nothing is saved or sent.</p>';
  }
  function values() {
    return {equation:el('calc-equation').value,age:el('calc-age').value,sex:el('calc-sex').value,creatinine:el('calc-creatinine').value,unit:el('calc-unit').value,context:el('calc-context').value,deindex:el('calc-deindex').checked,height:el('calc-height').value,weight:el('calc-weight').value};
  }
  function renderEgfr(answer) {
    return `<div class="calc-output"><div class="calc-output-label">${h(equationNames[answer.equation])}</div><div class="calc-number">${answer.indexed.toFixed(1)} <span>mL/min/1.73 m²</span></div><p>Indexed eGFR · creatinine ${mg(answer.scrMgDl)} mg/dL</p>${answer.absolute===null?'':`<div class="calc-absolute"><strong>${answer.absolute.toFixed(1)} <span>mL/min</span></strong><p>Non-indexed eGFR · Mosteller BSA ${answer.bsa.toFixed(3)} m²</p></div>`}</div>${answer.warnings.map(note=>`<p class="calc-warning">${h(note)}</p>`).join('')}<p class="calc-precision">Estimate, not measured GFR. Values are displayed to one decimal; do not select a dose solely from a rounded cutoff or diagnose CKD from one result.</p>`;
  }
  function renderCrcl(answer) {
    const rows = [['Actual body weight', answer.weight, answer.actual]];
    if (answer.ideal !== null) rows.push(['Ideal body weight (Devine)', answer.ibw, answer.ideal]);
    if (answer.adjusted !== null) rows.push(['Adjusted body weight (IBW + 0.4 × excess)', answer.adjbw, answer.adjusted]);
    return `<div class="calc-output"><div class="calc-output-label">Cockcroft–Gault creatinine clearance · creatinine ${mg(answer.scrMgDl)} mg/dL</div><table class="calc-crcl-table"><thead><tr><th scope="col">Weight used</th><th scope="col">kg</th><th scope="col">CrCl · mL/min</th></tr></thead><tbody>${rows.map(([label,kg,value])=>`<tr><th scope="row">${h(label)}</th><td>${kg.toFixed(1)}</td><td><strong>${value.toFixed(1)}</strong></td></tr>`).join('')}</tbody></table><p>Not indexed to body surface area. Use the weight the drug label or your local protocol specifies.</p></div>${answer.warnings.map(note=>`<p class="calc-warning">${h(note)}</p>`).join('')}<p class="calc-precision">Estimate, not measured clearance. The equation predates standardized creatinine assays and may read higher with current IDMS-traceable creatinine. Do not select a dose solely from a rounded cutoff.</p>`;
  }
  function update(focusError=false) {
    layout();
    form.querySelectorAll('[aria-invalid]').forEach(node=>node.removeAttribute('aria-invalid'));
    const crcl = measure() === 'crcl';
    const answer = crcl ? CrClMath.compute(values()) : RenalMath.compute(values());
    if (!answer.ok) {
      result.innerHTML = `<p class="calc-error">${h(answer.message)}</p>`;
      el(answer.field)?.setAttribute('aria-invalid','true');
      if (focusError) el(answer.field)?.focus();
      return false;
    }
    result.innerHTML = crcl ? renderCrcl(answer) : renderEgfr(answer);
    return true;
  }
  document.addEventListener('click', event=>{
    if (event.target.closest('[data-open="calculator"]')) {panel.showModal();el('calc-age').focus();}
  });
  el('close-calculator').addEventListener('click',()=>panel.close());
  panel.addEventListener('close',reset);
  window.addEventListener('pagehide',reset);
  // On submit, bring the answer into view: on phones it sits below the form.
  form.addEventListener('submit',event=>{event.preventDefault();if(update(true))result.scrollIntoView({block:'nearest',behavior:'smooth'});});
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
