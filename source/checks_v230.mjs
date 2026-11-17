// v0.23.0: Products in Jordan refreshed from Dalil v0.16. Nothing else changes.
import assert from 'node:assert/strict'; import fs from 'node:fs';
const read = f => fs.readFileSync(new URL(f, import.meta.url), 'utf8');
const db = JSON.parse(read('./dist/database.json')), base = JSON.parse(read('./baseline_v220.json'));
assert.equal(db.version, '0.23.0'); assert.equal(base.version, '0.22.0'); assert.equal(db.clinicalDataVersion, '0.19.0');
assert.deepEqual(db.drugs, base.drugs); assert.deepEqual(db.sources, base.sources); assert.deepEqual(db.calculatorSources, base.calculatorSources);
const J = db.jordanProducts, ids = new Set(db.drugs.map(d => d.id));
assert.equal(J.source.additions.records, 175); assert.equal(J.source.additions.collected, '2026-11-17');
for (const [id, p] of Object.entries(J.drugs)) { assert.ok(ids.has(id), id); assert.ok(p.products + p.combinations > 0, id); assert.match(p.query, /^[a-z][a-z ]+$/, id); }
assert.ok(J.drugs['sacubitril-valsartan'].products >= 25, 'one-text sacubitril/valsartan products counted');
assert.ok(J.drugs['sacubitril-valsartan'].brands.includes('Entresto'));
assert.ok(J.drugs.valsartan.products < base.jordanProducts.drugs.valsartan.products, 'sacubitril/valsartan no longer counted as valsartan alone');
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.23.0'));
console.log(`checks_v230 ok: ${Object.keys(J.drugs).length} medicines with Jordan products; sacubitril/valsartan ${J.drugs['sacubitril-valsartan'].products}`);
