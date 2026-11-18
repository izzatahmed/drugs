// v0.24.0: reviewer preview page med-review.html. Drug content and Jordan products unchanged.
import assert from 'node:assert/strict'; import fs from 'node:fs';
const read = f => fs.readFileSync(new URL(f, import.meta.url), 'utf8');
const db = JSON.parse(read('./dist/database.json')), base = JSON.parse(read('./baseline_v230.json'));
assert.equal(db.version, '0.24.0'); assert.equal(base.version, '0.23.0'); assert.equal(db.clinicalDataVersion, '0.19.0');
assert.deepEqual(db.drugs, base.drugs); assert.deepEqual(db.sources, base.sources); assert.deepEqual(db.calculatorSources, base.calculatorSources); assert.deepEqual(db.jordanProducts, base.jordanProducts);
const page = read('./dist/med-review.html'), data = JSON.parse(read('./dist/med-review-data.json'));
assert.equal(read('./dist/med-review-data.json'), read('./med_review_data_v240.json'));
assert.match(page, /<meta name="robots" content="noindex, nofollow">/); assert.match(page, /Preview for clinical reviewers — not for patient care/);
assert.ok(page.includes(read('./dist/renal-math.js').replace("'use strict';", '')), 'RenalMath/CrClMath inlined unchanged');
assert.ok(!/@@[A-Z]+@@/.test(page)); assert.ok(page.includes('RenalRounds v0.24.0'));
assert.ok(!/localStorage|sessionStorage|indexedDB|method:\s*'POST'|sendBeacon/.test(page), 'nothing stored or sent');
assert.ok(!/href=["'`](?:\.\/)?med-review/.test(read('./dist/index.html')), 'preview is not linked from the app');
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
console.log(`checks_v240 ok: review page ${Math.round(page.length / 1024)} KB · ${data.products.length} Jordanian products · ${Object.keys(data.barcodes).length} barcodes`);
