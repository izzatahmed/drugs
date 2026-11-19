// v0.25.0: the kidney medication review is linked from the app and follows the night theme. Drug content and Jordan products unchanged.
import assert from 'node:assert/strict'; import fs from 'node:fs';
const read = f => fs.readFileSync(new URL(f, import.meta.url), 'utf8');
const db = JSON.parse(read('./dist/database.json')), base = JSON.parse(read('./baseline_v240.json'));
assert.equal(db.version, '0.25.0'); assert.equal(base.version, '0.24.0'); assert.equal(db.clinicalDataVersion, '0.19.0');
assert.deepEqual(db.drugs, base.drugs); assert.deepEqual(db.sources, base.sources); assert.deepEqual(db.calculatorSources, base.calculatorSources); assert.deepEqual(db.jordanProducts, base.jordanProducts);
const page = read('./dist/med-review.html'), data = JSON.parse(read('./dist/med-review-data.json'));
assert.equal(read('./dist/med-review-data.json'), read('./med_review_data_v240.json'));
assert.ok(!/noindex/.test(page)); assert.match(page, /Draft clinical reference — independent review pending/); assert.match(page, /html\[data-theme=dark\]\{/);
assert.ok(page.includes(read('./dist/renal-math.js').replace("'use strict';", '')), 'RenalMath/CrClMath inlined unchanged');
assert.ok(!/@@[A-Z]+@@/.test(page)); assert.ok(page.includes('RenalRounds v0.25.0'));
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
for (const [fg, bg] of [['ink', 'bg'], ['ink', 'card'], ['muted', 'card'], ['teal', 'card'], ['on-teal', 'teal'], ['ink', 'hit'], ['red', 'red-soft'], ['amber', 'amber-soft'], ['green', 'green-soft'], ['note', 'amber-soft']]) for (const vars of themes) assert.ok(ratio(vars[fg], vars[bg]) >= 4.5, `${fg} on ${bg}: ${ratio(vars[fg], vars[bg]).toFixed(2)}`);
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
console.log(`checks_v250 ok: review page ${Math.round(page.length / 1024)} KB · ${data.products.length} Jordanian products · ${Object.keys(data.barcodes).length} barcodes`);
