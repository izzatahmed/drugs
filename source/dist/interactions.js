'use strict';
// Drug–drug interactions: verbatim label statements per drug, FDA CYP/transporter roles, and a two-drug checker.
// The checker only surfaces label sentences and FDA-table pairings; absence of a result is not evidence of safety.
const Interactions = (() => {
  const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const namesOf = d => [d.name.split(' (')[0], ...(d.aliases || []), d.id.replace(/-/g, ' ')].map(s => s.trim()).filter(s => s.length >= 4 && !/vaccine|supplement|\boral\b|topical|nasal/i.test(s));
  function partnerRegexes(dataset, b) {
    const out = [];
    const names = namesOf(b);
    if (names.length) out.push({label: b.name, rx: new RegExp(`\\b(?:${names.map(esc).join('|')})\\b`, 'i')});
    for (const [cls, c] of Object.entries(dataset.interactionClasses || {})) if (c.members.includes(b.id)) out.push({label: cls, rx: new RegExp(c.pattern, 'i')});
    return out;
  }
  function roleTokens(d) {
    const out = [];
    for (const r of (d.interactions?.fdaRoles || [])) {
      const m = r.match(/^(.*?)\s+(strong|moderate sensitive|moderate|weak|sensitive)?\s*(inhibitor|inducer|substrate)$/i);
      if (!m) continue;
      for (const e of m[1].split(/[;,]/).map(s => s.trim()).filter(Boolean)) out.push({enzyme: e, strength: (m[2] || '').toLowerCase(), kind: m[3].toLowerCase(), text: r});
    }
    return out;
  }
  const label = e => /^[0-9][A-Z0-9]*$/.test(e) ? 'CYP' + e : e;
  function mechanism(a, b) {
    const flags = [];
    for (const x of roleTokens(a)) for (const y of roleTokens(b)) {
      if (x.enzyme !== y.enzyme || y.kind !== 'substrate') continue;
      if (x.kind === 'inhibitor' && x.strength !== 'weak') flags.push(`${a.name} is an FDA-listed ${x.strength} ${label(x.enzyme)} inhibitor and ${b.name} is a ${y.strength ? y.strength + ' ' : ''}${label(y.enzyme)} substrate: exposure to ${b.name} may rise.`);
      if (x.kind === 'inducer' && x.strength !== 'weak') flags.push(`${a.name} is an FDA-listed ${x.strength} ${label(x.enzyme)} inducer and ${b.name} is a ${y.strength ? y.strength + ' ' : ''}${label(y.enzyme)} substrate: exposure to ${b.name} may fall.`);
    }
    return [...new Set(flags)];
  }
  function statements(dataset, a, b) {
    const rxs = partnerRegexes(dataset, b), out = [];
    for (const s of (a.interactions?.statements || [])) { const hit = rxs.filter(r => r.rx.test(s)); if (hit.length) out.push({text: s, via: [...new Set(hit.map(h => h.label))]}); }
    return out;
  }
  function check(dataset, a, b) {
    return {ab: statements(dataset, a, b), ba: statements(dataset, b, a), mech: [...mechanism(a, b), ...mechanism(b, a)]};
  }
  return {check, roleTokens, namesOf};
})();

function interactionsPanel(d) {
  const ix = d.interactions;
  if (!ix || (!ix.statements?.length && !ix.fdaRoles?.length)) return `<details class="info-detail ix-panel"><summary>Drug interactions</summary><p class="preg-empty">Interaction statements have not been curated for this entry. Check the current label's interaction section.</p><p><button type="button" class="ix-open" data-open="interaction-checker" data-ix-drug="${h(d.id)}">Check a pair</button></p></details>`;
  const roles = ix.fdaRoles?.length ? `<div class="ix-roles"><strong>FDA CYP/transporter roles</strong> ${ix.fdaRoles.map(r => `<span class="pill">${h(r)}</span>`).join(' ')}</div>` : '';
  const list = ix.statements?.length ? `<div class="preg-block"><strong>Key interactions (quoted from label)</strong><ul class="ix-list">${ix.statements.map(s => `<li>${h(s)}.</li>`).join('')}</ul></div>` : '';
  return `<details class="info-detail ix-panel"><summary>Drug interactions${ix.statements?.length ? ` · ${ix.statements.length} label statements` : ''}</summary>${roles}${list}<p class="preg-note">Selected sentences from the label's interaction section that name another medicine, a drug class or a CYP/P-gp pathway. Not a complete list.</p><p><button type="button" class="ix-open" data-open="interaction-checker" data-ix-drug="${h(d.id)}">Check this drug against another</button></p><div class="source-inline"><span>SOURCE</span>${(ix.sourceIds || []).map(sourceLink).join('<span>·</span>')}</div></details>`;
}

(function setupInteractionChecker(){
  const panel = document.querySelector('#interaction-checker'), form = document.querySelector('#ix-form'), result = document.querySelector('#ix-result');
  const a = document.getElementById('ix-a'), b = document.getElementById('ix-b');
  const placeholder = '<p class="calc-placeholder">Choose two medicines. Results quote the labels; nothing is saved or sent.</p>';
  let listed = false;
  function fill() {
    if (listed || typeof db === 'undefined' || !db) return;
    document.getElementById('ix-names').innerHTML = db.drugs.map(d => `<option value="${h(d.name)}"></option>`).join('');
    listed = true;
  }
  const find = v => { const s = v.trim().toLowerCase(); if (!s) return null; return db.drugs.find(d => d.name.toLowerCase() === s) || db.drugs.find(d => d.id === s) || db.drugs.find(d => (d.aliases || []).some(x => x.toLowerCase() === s)) || null; };
  function run() {
    const da = find(a.value), dbb = find(b.value);
    if (!da || !dbb) { result.innerHTML = a.value && b.value ? '<p class="calc-error">Choose both medicines from the list.</p>' : placeholder; return; }
    if (da.id === dbb.id) { result.innerHTML = '<p class="calc-error">Choose two different medicines.</p>'; return; }
    const r = Interactions.check(db, da, dbb);
    const block = (who, other, items, d) => items.length ? `<div class="preg-block"><strong>${h(who.name)} label · relevant to ${h(other.name)}</strong><ul class="ix-list">${items.map(x => `<li>${h(x.text)}. <small>(matched: ${h(x.via.join(', '))})</small></li>`).join('')}</ul><div class="source-inline"><span>SOURCE</span>${(d.interactions.sourceIds || []).map(sourceLink).join('<span>·</span>')}</div></div>` : '';
    const mech = r.mech.length ? `<div class="preg-block"><strong>FDA CYP/transporter pairing</strong><ul class="ix-list">${r.mech.map(x => `<li>${h(x)}</li>`).join('')}</ul><div class="source-inline"><span>SOURCE</span>${sourceLink('fda-cyp-table')}</div></div>` : '';
    const any = r.ab.length || r.ba.length || r.mech.length;
    const coverage = [da, dbb].filter(d => !d.interactions?.statements?.length).map(d => d.name);
    result.innerHTML = `<div class="calc-output${any ? ' ca-intermediate' : ''}"><div class="calc-output-label">${h(da.name)} + ${h(dbb.name)}</div><div class="ca-title">${any ? 'Possible interaction — read the label wording' : 'No statement found'}</div>`
      + block(da, dbb, r.ab, da) + block(dbb, da, r.ba, dbb) + mech
      + (any ? '' : '<p>Neither label\'s curated interaction sentences mention the other medicine or its class, and the FDA table gives no CYP/P-gp pairing. This does not exclude an interaction.</p>')
      + (coverage.length ? `<p>Label interaction statements are not yet curated for: ${h(coverage.join(', '))}.</p>` : '') + '</div>';
  }
  document.addEventListener('click', e => {
    const o = e.target.closest('[data-open="interaction-checker"]');
    if (!o) return;
    fill(); const menu = document.getElementById('calc-menu'); if (menu.open) menu.close();
    form.reset(); result.innerHTML = placeholder;
    if (o.dataset.ixDrug) { const d = db.drugs.find(x => x.id === o.dataset.ixDrug); if (d) a.value = d.name; }
    panel.showModal(); (a.value ? b : a).focus();
  });
  form.addEventListener('submit', e => { e.preventDefault(); run(); });
  form.addEventListener('change', run);
  form.addEventListener('input', () => { if (find(a.value) && find(b.value)) run(); });
  panel.querySelector('.tool-close').addEventListener('click', () => panel.close());
  panel.querySelector('.tool-clear').addEventListener('click', () => { form.reset(); result.innerHTML = placeholder; a.focus(); });
  panel.addEventListener('close', () => { form.reset(); result.innerHTML = placeholder; });
  result.innerHTML = placeholder;
})();
