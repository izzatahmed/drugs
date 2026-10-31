import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v123.json'));
const C=JSON.parse(read('./curation_v124.json')),Q=JSON.parse(read('./label_quotes_v124.json'));
assert.equal(db.version,'0.12.4');assert.equal(db.clinicalDataVersion,'0.12.4');
const src=new Map(db.sources.map(s=>[s.id,s])),drug=id=>db.drugs.find(d=>d.id===id);
const inLabel=(id,e)=>Q[id].windows.some(w=>w.includes(e.replace(/\.$/,'')));
// 1. Only the eight curated entries changed.
for(const d of db.drugs){const o=base.drugs.find(x=>x.id===d.id);assert.ok(o);if(!C[d.id]){assert.deepEqual(d,o,`${d.id} changed`);continue;}
 for(const k of ['pregnancyLactation','referenceChecks','aliases','name'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);}
// 2. Every quote is verbatim label text and every table/PK change cites the label source.
let quotes=0;
for(const [id,c] of Object.entries(C)){const d=drug(id),sid=`us124-${id}`,s=src.get(sid);
 assert.ok(s&&/^https:\/\/dailymed\.nlm\.nih\.gov\//.test(s.url),`${id} source`);assert.equal(s.label.setid,Q[id].meta.setid);
 for(const [k,m] of Object.entries(c.modalities||{})){assert.equal(d.modalities[k].sourceIds[0],sid);assert.equal(d.modalities[k].status,m.status);for(const e of m.ev||[]){assert.ok(inLabel(id,e),`${id}/${k} quote`);quotes++;}}
 const p=d.pharmacokinetics;
 for(const [k,f] of Object.entries(c.pk)){const v=['ihd','pd'].includes(k)?p.dialysability[k]:p[k];
  assert.equal(v.value,f.value);assert.deepEqual(v.sourceIds,[sid]);assert.ok(inLabel(id,v.evidence),`${id}/${k} evidence`);quotes++;
  if(!['ihd','pd'].includes(k))for(const n of f.value.match(/\d+(?:\.\d+)?/g)||[])assert.ok(f.ev.includes(n),`${id}/${k}: ${n} not in quote`);}
 for(const k of ['crrt','sled'])assert.equal(p.dialysability[k].status,'not_curated');}
// 3. Digoxin table equals label Table 3 cell by cell (label row text stored in the quote window file is the SPL table).
const T3={10:['62.5*',125,125,187.5,187.5,187.5,250,19],20:[125,125,125,187.5,187.5,250,250,16],30:[125,125,187.5,187.5,250,250,312.5,14],40:[125,187.5,187.5,250,250,312.5,312.5,13],50:[125,187.5,187.5,250,250,312.5,312.5,12],60:[125,187.5,250,250,312.5,312.5,375,11],70:[187.5,187.5,250,250,312.5,375,375,10],80:[187.5,187.5,250,312.5,312.5,375,437.5,9],90:[187.5,250,250,312.5,375,437.5,437.5,8],100:[187.5,250,312.5,312.5,375,437.5,500,7]};
const lab=JSON.parse(read('./label_quotes_v124.json')).digoxin;
const rows=drug('digoxin').modalities.ckd.tables[0].rows;assert.equal(rows.length,10);
for(const [i,[c,r]] of Object.entries(Object.entries(T3))){const row=rows[i];assert.equal(row.context,`Corrected CrCl ${c} mL/min`);
 const cells=[...row.dose.matchAll(/(\d+) kg: ([\d.]+\*?)/g)].map(m=>[+m[1],m[2]]);assert.deepEqual(cells.map(x=>x[0]),[40,50,60,70,80,90,100]);
 assert.deepEqual(cells.map(x=>x[1]),r.slice(0,7).map(String));assert.match(row.dose,new RegExp(`steady state ≈${r[7]} days`));}
assert.ok(lab.windows.some(w=>w.includes('Table 3 provides the recommended (once daily) maintenance dose')));
// 4. Promotions, coverage and the PPI statements.
for(const id of ['esomeprazole','lansoprazole'])assert.equal(drug(id).entryType,'renal');
assert.deepEqual(db.coverage,{renal:359,safety:26,catalog:284});
for(const id of ['omeprazole','esomeprazole','lansoprazole','pantoprazole','rabeprazole','dexlansoprazole']){const d=drug(id);assert.match(d.modalities.ckd.tables[0].rows[0].dose,/^No dose adjustment/);assert.equal(d.pharmacokinetics.dialysability.ihd.status,'not_removed');assert.equal(d.modalities.pd.status,'not_curated');}
assert.equal(drug('digoxin').pharmacokinetics.dialysability.ihd.status,'not_removed');
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.12.4'));
console.log(`PASS: 8 entries changed (others identical to v0.12.3); ${quotes} label quotes verified; digoxin Table 3 matches cell by cell; PPI CKD/HD statements and PK sourced.`);
