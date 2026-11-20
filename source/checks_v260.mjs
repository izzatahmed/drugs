// v0.26.0: kidney medication review — transplant immunosuppressant check; draft notice as asterisk + footnote. Drug content and Jordan products unchanged.
import assert from 'node:assert/strict'; import fs from 'node:fs';
const read = f => fs.readFileSync(new URL(f, import.meta.url), 'utf8');
const db = JSON.parse(read('./dist/database.json')), base = JSON.parse(read('./baseline_v250.json'));
assert.equal(db.version, '0.26.0'); assert.equal(base.version, '0.25.0'); assert.equal(db.clinicalDataVersion, '0.19.0');
assert.deepEqual(db.drugs, base.drugs); assert.deepEqual(db.sources, base.sources); assert.deepEqual(db.calculatorSources, base.calculatorSources); assert.deepEqual(db.jordanProducts, base.jordanProducts);
const page = read('./dist/med-review.html'), data = JSON.parse(read('./dist/med-review-data.json'));
assert.equal(read('./dist/med-review-data.json'), read('./med_review_data_v240.json'));
assert.ok(!/noindex/.test(page)); assert.match(page, /Draft clinical reference — independent review pending/); assert.match(page, /html\[data-theme=dark\]\{/);
assert.ok(page.includes(read('./dist/renal-math.js').replace("'use strict';", '')), 'RenalMath/CrClMath inlined unchanged');
assert.ok(!/@@[A-Z]+@@/.test(page)); assert.ok(page.includes('RenalRounds v0.26.0'));
assert.ok(!/localStorage|sessionStorage|indexedDB|method:\s*'POST'|sendBeacon/.test(page), 'nothing stored or sent');
const app = read('./dist/index.html');
assert.equal((app.match(/class="[^"]*mr-open[^"]*" href="med-review\.html"/g) || []).length, 3, 'CALC menu, side menu and footer link to the review');
assert.ok(app.includes('href=\"med-review.html#add=${encodeURIComponent(d.id)}\"'), 'each medicine can be added from its interactions panel');
// add-from-address and theme
assert.ok(page.includes("hp.get('add')") && page.includes('history.replaceState(null'), 'opens with #add= and clears the address');
// dark-theme contrast of the main pairs
const themes = [/:root\{([^}]*)\}/, /html\[data-theme=dark\]\{([^}]*)\}/].map(rx => Object.fromEntries([...page.match(rx)[1].matchAll(/--([a-z-]+):#([0-9a-f]{6}|[0-9a-f]{3})\b/g)].map(m => [m[1], '#' + (m[2].length === 3 ? [...m[2]].map(c => c + c).join('') : m[2])])));
const lum = hx => { const c = [1, 3, 5].map(i => parseInt(hx.slice(i, i + 2), 16) / 255).map(v => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
for (const [fg, bg] of [['ink', 'bg'], ['ink', 'card'], ['muted', 'card'], ['teal', 'card'], ['on-teal', 'teal'], ['ink', 'hit'], ['red', 'red-soft'], ['amber', 'amber-soft'], ['green', 'green-soft'], ['note', 'amber-soft'], ['ink', 'red-soft'], ['amber', 'card']]) for (const vars of themes) assert.ok(ratio(vars[fg], vars[bg]) >= 4.5, `${fg} on ${bg}: ${ratio(vars[fg], vars[bg]).toFixed(2)}`);
// row matching
const fn = name => page.match(new RegExp(`function ${name}\\([^]*?\\n}`))[0];
const {rangeOf, rowHit} = new Function(`${fn('rangeOf')}\n${fn('drugMetric')}\n${fn('rowHit')}\nreturn {rangeOf, rowHit};`)();
const k = (egfr, crcl) => ({mode: 'ckd', egfr, crcl});
const met = db.drugs.find(d => d.id === 'metformin');
const hits = (d, kk) => d.modalities.ckd.tables.flatMap(t => t.rows).filter(r => rowHit(r.context, d, kk)).map(r => r.context);
assert.deepEqual(hits(met, k(35, null)), ['30 to <45']); assert.deepEqual(hits(met, k(45, null)), ['≥45']); assert.deepEqual(hits(met, k(29.9, null)), ['<30']); assert.deepEqual(hits(met, k(30, null)), ['30 to <45']);
assert.deepEqual(rangeOf('CrCl 30–50'), {lo: 30, hi: 50, metric: 'crcl'}); assert.deepEqual(rangeOf('eGFR ≤15'), {lo: 0, hi: 15, metric: 'egfr'});
assert.equal(rangeOf('Fewer than 2 reduction criteria'), null); assert.equal(rangeOf('Any CrCl / eGFR'), null);
assert.equal(rowHit('CrCl <30', met, k(20, null)).approx, true, 'falls back to eGFR when CrCl is missing, and says so');
assert.equal(rowHit('CrCl <30', met, k(null, null)), null);
// product data
const ids = new Set(db.drugs.filter(d => d.entryType !== 'catalog').map(d => d.id));
assert.ok(data.drugs.every(id => ids.has(id))); assert.ok(data.products.length > 6000);
for (const p of data.products) { assert.equal(p.length, 6); assert.ok(p[3].length && p[3].every(i => i < data.drugs.length)); assert.ok(Number.isInteger(p[4]) && p[4] >= 0); }
for (const v of Object.values(data.barcodes)) assert.ok(v.every(i => i < data.products.length));
const entresto = data.products.filter(p => /^Entresto/i.test(p[0]));
assert.ok(entresto.length && entresto.every(p => p[3].map(i => data.drugs[i]).join() === 'sacubitril-valsartan'), 'combination replaces its components');
// draft notice: asterisk on the title, footnote at the end
assert.ok(!page.includes('class="preview"')); assert.match(page, /<h1>Kidney medication review<a class="ast" href="#note"/); assert.ok(page.indexOf('id="note"') > page.indexOf('id="report"'));
// transplant: every listed immunosuppressant exists, and the existing data flag the classic pairs
const TX = [...page.match(/const TX = (\[\[.*?\]\]);/)[1].matchAll(/\['([a-z-]+)'/g)].map(m => m[1]);
assert.deepEqual(TX, ['tacrolimus', 'cyclosporine', 'sirolimus', 'everolimus', 'mycophenolate-mofetil', 'mycophenolate-sodium', 'azathioprine', 'prednisolone', 'belatacept']); assert.ok(TX.every(id => ids.has(id)));
const ixjs = read('./dist/interactions.js'); const Interactions = new Function(ixjs.match(/const Interactions = \(\(\) => \{[^]*?\n\}\)\(\);/)[0] + '\nreturn Interactions;')();
const by = new Map(db.drugs.map(d => [d.id, d])), found = (a, b) => { const r = Interactions.check(db, by.get(a), by.get(b)); return r.ab.length + r.ba.length + r.mech.length > 0; };
for (const [a, b] of [['tacrolimus', 'clarithromycin'], ['tacrolimus', 'voriconazole'], ['tacrolimus', 'rifampicin'], ['cyclosporine', 'atorvastatin'], ['cyclosporine', 'colchicine'], ['sirolimus', 'diltiazem'], ['azathioprine', 'allopurinol'], ['azathioprine', 'febuxostat'], ['everolimus', 'carbamazepine'], ['mycophenolate-sodium', 'rifampicin']]) assert.ok(found(a, b), `${a} + ${b}`);
console.log(`checks_v260 ok: review page ${Math.round(page.length / 1024)} KB · ${data.products.length} Jordanian products · ${Object.keys(data.barcodes).length} barcodes`);
