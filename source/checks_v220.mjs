// v0.22.0: tubular-function calculators and voice search, plus every v0.21 calculator case. Drug records unchanged.
import assert from 'node:assert/strict'; import fs from 'node:fs'; import vm from 'node:vm';
const read = f => fs.readFileSync(new URL(f, import.meta.url), 'utf8');
const db = JSON.parse(read('./dist/database.json')), base = JSON.parse(read('./baseline_v210.json'));
assert.equal(db.version, '0.22.0'); assert.equal(db.clinicalDataVersion, '0.19.0'); assert.equal(base.version, '0.21.0');
assert.deepEqual(db.drugs, base.drugs); assert.deepEqual(db.sources, base.sources); assert.deepEqual(db.jordanProducts, base.jordanProducts);
assert.equal(db.calculatorSources.length, 15 + 22 + 8); for (const s of db.calculatorSources) assert.match(s.url, /^https:\/\//);
const ctx = {h: s => String(s ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]))};
vm.createContext(ctx); vm.runInContext(read('./dist/nephro-math.js') + ';this.M=NephroMath;', ctx); vm.runInContext(read('./dist/nephro-tools.js') + ';this.T=NephroTools;', ctx);
const M = ctx.M, T = ctx.T, near = (a, b, tol = 0.01, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg ?? ''} ${a} vs ${b}`);
// reference cases
let r = M.naGlucose({na: '130', glucose: '600'}); near(r.katz, 138); near(r.hillier, 142);
r = M.naGlucose({na: '130', glucose: '33.3', gluUnit: 'mmol'}); near(r.hillier, 142, 0.05);
r = M.hyponatremia({sex: 'female', age: '59', weight: '60', na: '112', infusate: 'nacl3'}); near(r.perLitre, 12.9, 0.05, 'NEJM 2000 hyponatremia example'); near(r.litresFor8 * 1000, 618.5, 1);
r = M.hyponatremia({sex: 'male', age: '30', weight: '70', na: '120', infusate: 'rl'}); near(r.perLitre, (134 - 120) / 43);
r = M.hyponatremia({sex: 'male', age: '30', weight: '70', na: '120', infusate: 'd5w'}); assert.ok(r.perLitre < 0 && r.litresFor8 === null);
assert.equal(M.tbwFraction('female', 70), 0.45); assert.equal(M.tbwFraction('male', 70), 0.5);
r = M.freeWater({sex: 'male', age: '40', weight: '70', na: '160'}); near(r.deficit, 6.0);
r = M.correctedCalcium({ca: '8', alb: '2'}); near(r.mgdl, 9.6); r = M.correctedCalcium({caUnit: 'mmol', ca: '2', alb: '20'}); near(r.mmol, 2.4, 0.005);
r = M.osmolalGap({na: '140', glucose: '90', urea: '14', measured: '310'}); near(r.calculated, 290, 0.05); near(r.gap, 20, 0.05);
r = M.osmolalGap({na: '140', glucose: '5', gluUnit: 'mmol', urea: '5', ureaUnit: 'mmol', ethanol: '20', etohUnit: 'mmol'}); near(r.calculated, 310);
r = M.anionGap({na: '140', cl: '100', hco3: '10', alb: '2'}); near(r.ag, 30); near(r.corrected, 35); near(r.delta, 23 / 14); assert.match(r.deltaNote, /uncomplicated/);
r = M.anionGap({na: '140', cl: '115', hco3: '12'}); assert.ok(!r.high);
r = M.winters({hco3: '10', pco2: '30'}); near(r.expected, 23); assert.match(r.verdict, /respiratory acidosis/);
r = M.fractionalExcretion({uNa: '20', pNa: '140', uCr: '100', pCr: '2'}); near(r.fena, 0.2857, 0.0005); assert.equal(r.feurea, null);
r = M.fractionalExcretion({uCr: '100', pCr: '2', uUrea: '300', pUrea: '30'}); near(r.feurea, 20);
assert.equal(M.fractionalExcretion({uCr: '100', pCr: '2'}).ok, false);
assert.equal(M.akiStage({base: '1', cur: '2.1'}).stage, 2); assert.equal(M.akiStage({base: '1', cur: '1.3'}).stage, 1); assert.equal(M.akiStage({base: '1', cur: '1.2'}).stage, 0);
assert.equal(M.akiStage({base: '2', cur: '4.4'}).stage, 3, '≥4.0 mg/dL'); assert.equal(M.akiStage({base: '88', cur: '265', crUnit: 'umol'}).stage, 3);
assert.equal(M.akiStage({base: '1', cur: '1', uo: '0.4', uoHours: '8'}).stage, 1); assert.equal(M.akiStage({base: '1', cur: '1', uo: '0', uoHours: '12'}).stage, 3); assert.equal(M.akiStage({base: '1', cur: '1', rrt: 'yes'}).stage, 3);
r = M.proteinuria({ratio: '300', unit: 'mgmmol', kind: 'protein'}); near(r.mgG, 2652.6, 0.5); assert.equal(r.cat, 'A3');
r = M.proteinuria({ratio: '25', unit: 'mgg', kind: 'albumin'}); assert.equal(r.cat, 'A1'); r = M.proteinuria({mode: 'raw', uProt: '400', uCr: '100', kind: 'protein'}); near(r.perDay, 4); assert.ok(r.nephrotic);
r = M.ufRate({uf: '3.5', hours: '4', weight: '70'}); near(r.rate, 12.5); near(r.max13, 3.64); assert.ok(!r.high);
r = M.crrt({weight: '80', qb: '200', hct: '30', pre: '1000', post: '500', qd: '1000', net: '100'}); near(r.dose, 32.5); near(r.corrected, 30); near(r.ff, 0.1702, 0.0005);
r = M.pdKtv({sex: 'male', age: '50', height: '175', weight: '70', dUrea: '14', pUrea: '20', drain: '10'}); near(r.V, 40.018, 0.001); near(r.perit, 0.7 * 70 / 40.018);
r = M.tsat({fe: '50', tibc: '300', ferritin: '200'}); near(r.tsat, 16.67); assert.equal(r.ivIronTrial, true); assert.equal(M.tsat({fe: '400', tibc: '300'}).ok, false);
r = M.ganzoni({weight: '70', hb: '9', target: '15'}); near(r.deficit, 1508); r = M.ganzoni({weight: '70', hb: '90', target: '150', hbUnit: 'gl'}); near(r.deficit, 1508);
const shell = read('./app-shell.html'), html = read('./dist/index.html');
// v0.22 tubular function
r = M.potassium({uK: '20', uCr: '10', crUnit: 'mmol', pK: '2.8'}); near(r.ratio, 2); near(r.mEqPerG, 17.68); assert.equal(r.context, 'hypo'); assert.equal(r.ttkg, null);
r = M.potassium({uK: '40', uCr: '100', crUnit: 'mgdl', pK: '6', uOsm: '500', pOsm: '290', uNa: '60'}); near(r.ratio, 40 / 11.31, 0.01); near(r.ttkg, 3.867, 0.001); assert.equal(r.ttkgNote, null); assert.equal(r.context, 'hyper');
r = M.potassium({uK: '40', uCr: '5000', crUnit: 'umol', pK: '6', uOsm: '250', pOsm: '290'}); near(r.ratio, 8); assert.match(r.ttkgNote, /not valid/);
assert.equal(M.potassium({uK: '40', uCr: '10', crUnit: 'mgdl', pK: '4'}).ok, true); assert.equal(M.potassium({uK: '40', uCr: '1', crUnit: 'mgdl', pK: '4'}).ok, false, 'implausible urine creatinine');
r = M.urineAnionGap({uNa: '40', uK: '30', uCl: '110', uOsm: '500', uUrea: '200'}); assert.equal(r.uag, -40); near(r.osmGap, 160); near(r.nh4, 80);
r = M.urineAnionGap({uNa: '60', uK: '30', uCl: '70', uOsm: '400', uUrea: '280', ureaUnit: 'mgdl', uGlu: '180', gluUnit: 'mgdl'}); assert.equal(r.uag, 20); near(r.osmGap, 400 - (180 + 100 + 9.99), 0.05);
r = M.phosphate({uP: '20', pP: '0.6', uCr: '8', pCr: '0.08'}); near(r.fe, 33.33); near(r.trp, 0.6667, 0.0005); near(r.tmp, 0.4, 0.0005, 'TRP ≤0.86 branch'); assert.ok(r.low);
r = M.phosphate({uP: '10', pP: '1.2', uCr: '10', pCr: '0.08'}); near(r.trp, 0.9333, 0.0005); near(r.tmp, 1.3263, 0.0005, 'TRP >0.86 branch');
r = M.phosphate({uP: '31', pP: '3.7', uCr: '100', pCr: '1', pUnit: 'mgdl'}); near(r.tmp, 1.2298, 0.0005); assert.equal(M.phosphate({uP: '200', pP: '1', uCr: '10', pCr: '0.08'}).ok, false, 'FEPO4 ≥100%');
r = M.magnesium({uMg: '2', pMg: '0.5', uCr: '8', pCr: '0.08'}); near(r.fe, 5.714, 0.001);
// voice search: alternative choice and correction to the nearest medicine word
const vctx = {}; vm.createContext(vctx); vm.runInContext(read('./dist/voice-search.js') + ';this.V=VoiceSearch;', vctx); const V = vctx.V;
assert.equal(V.best(['amlodibine'], db.drugs), 'amlodipine'); assert.equal(V.best(['glucofage'], db.drugs), 'glucophage'); assert.equal(V.best(['apex a band', 'apixaban'], db.drugs), 'apixaban'); assert.equal(V.best(['sefuroxime'], db.drugs), 'cefuroxime');
assert.ok(shell.includes('id="voice-search"') && /hidden><svg/.test(shell.slice(shell.indexOf('id="voice-search"'), shell.indexOf('id="voice-search"') + 400)), 'mic hidden until supported');
assert.ok(html.includes(read('./dist/voice-search.js')));
// every calculator renders without throwing and declares sources that are in calculatorSources
const urls = new Set(db.calculatorSources.map(s => s.url));
assert.equal(Object.keys(T.C).length, 19);
for (const [id, c] of Object.entries(T.C)) { assert.ok(c.sources.length && c.sources.every(([, u]) => urls.has(u)), id); assert.ok(c.method && c.title && c.group, id); }
const sample = {'na-glucose': {na: '130', glucose: '600'}, hyponatremia: {sex: 'female', age: '59', weight: '60', na: '112', infusate: 'nacl3'}, 'free-water': {sex: 'male', age: '40', weight: '70', na: '160'}, calcium: {ca: '8', alb: '2'}, 'osmolal-gap': {na: '140', glucose: '90', urea: '14', measured: '310'}, 'anion-gap': {na: '140', cl: '100', hco3: '10', alb: '2'}, winters: {hco3: '10', pco2: '30'}, fena: {uNa: '20', pNa: '140', uCr: '100', pCr: '2', uUrea: '300', pUrea: '30'}, 'aki-stage': {base: '1', cur: '2.1', uo: '0.4', uoHours: '8'}, proteinuria: {ratio: '300', unit: 'mgmmol'}, 'uf-rate': {uf: '3.5', hours: '4', weight: '70'}, crrt: {weight: '80', qb: '200', hct: '30', pre: '1000', post: '500', qd: '1000', net: '100'}, 'pd-ktv': {sex: 'male', age: '50', height: '175', weight: '70', dUrea: '14', pUrea: '20', drain: '10', uUrea: '200', urine: '0.5'}, tsat: {fe: '50', tibc: '300', ferritin: '200'}, ganzoni: {weight: '70', hb: '9', target: '15'}, potassium: {uK: '40', uCr: '100', crUnit: 'mgdl', pK: '6', uOsm: '500', pOsm: '290', uNa: '60'}, 'urine-ag': {uNa: '40', uK: '30', uCl: '110', uOsm: '500', uUrea: '200'}, phosphate: {uP: '20', pP: '0.6', uCr: '8', pCr: '0.08'}, magnesium: {uMg: '2', pMg: '0.5', uCr: '8', pCr: '0.08'}};
for (const [id, c] of Object.entries(T.C)) { const a = c.run(sample[id]); assert.ok(a.ok, id); assert.ok(c.render(a).includes('calc-output'), id); }
// shell wiring
for (const id of Object.keys(T.C)) assert.ok(shell.includes(`data-open="nephro-tools" data-calc="${id}"`), id);
assert.equal((shell.match(/class="calc-menu-item"/g) || []).length, 26); assert.ok(/<dialog id="nephro-tools"/.test(shell));
assert.ok(html.includes(read('./dist/nephro-math.js')) && html.includes(read('./dist/nephro-tools.js')) && html.includes('RenalRounds · adults · v0.22.0'));
assert.ok(!/localStorage|sessionStorage|fetch\s*\(|location\./.test(read('./dist/nephro-math.js') + read('./dist/nephro-tools.js')));
console.log('checks_v220 ok: 19 calculators (15 + 4 tubular), reference cases, voice search, sources and wiring');
