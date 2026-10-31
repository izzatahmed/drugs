import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v124.json'));
const C=JSON.parse(read('./curation_v125.json')),Q=JSON.parse(read('./label_quotes_v125.json'));
assert.equal(db.version,'0.12.5');assert.equal(db.clinicalDataVersion,'0.12.5');
const src=new Map(db.sources.map(s=>[s.id,s])),drug=id=>db.drugs.find(d=>d.id===id);
const inLabel=(id,e)=>Q[id].windows.some(w=>w.includes(e.replace(/\.$/,'')));
const CORE=['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'];
let quotes=0,promoted=0,newPk=0;
for(const d of db.drugs){const o=base.drugs.find(x=>x.id===d.id);assert.ok(o);const c=C[d.id];
 if(!c){assert.deepEqual(d,o,`${d.id} changed`);continue;}
 for(const k of ['pregnancyLactation','referenceChecks','aliases','name','category'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);
 const sid=`us125-${d.id}`,s=src.get(sid);assert.ok(s&&/^https:\/\/dailymed\.nlm\.nih\.gov\//.test(s.url),`${d.id} source`);assert.equal(s.label.setid,Q[d.id].meta.setid);
 if(c.promote){promoted++;assert.equal(o.entryType==='renal',false);assert.equal(d.entryType,'renal');assert.notEqual(d.flag,'catalog');assert.deepEqual(d.sourceIds,[sid]);}
 // 1. Previously curated settings and PK values are untouched.
 for(const k of Object.keys(d.modalities)){if(!c.modalities[k]||(!c.promote&&o.modalities[k].status!=='not_curated'))assert.deepEqual(d.modalities[k],o.modalities[k],`${d.id}/${k} overwritten`);
  else{assert.equal(d.modalities[k].status,c.modalities[k].status);assert.equal(d.modalities[k].sourceIds[0],sid);for(const e of c.modalities[k].ev){assert.ok(inLabel(d.id,e),`${d.id}/${k} quote`);quotes++;}}}
 const op=o.pharmacokinetics,p=d.pharmacokinetics;
 for(const k of [...CORE,'ihd','pd','crrt','sled']){const a=CORE.includes(k)?op[k]:op.dialysability[k],b=CORE.includes(k)?p[k]:p.dialysability[k];
  if(a.value!==null){assert.deepEqual(b,a,`${d.id}/pk.${k} overwritten`);continue;}
  const f=c.pk[k];if(!f||b.value===null)continue;newPk++;
  assert.equal(b.value,f.value);assert.deepEqual(b.sourceIds,[sid]);assert.ok(inLabel(d.id,b.evidence),`${d.id}/${k} evidence`);quotes++;
  if(CORE.includes(k))for(const n of f.value.match(/\d+(?:\.\d+)?/g)||[])assert.ok(f.ev.includes(n),`${d.id}/${k}: ${n} not in quote`);}
 for(const k of ['crrt','sled'])assert.equal(p.dialysability[k].status,'not_curated');}
// 2. Key tables match the label wording.
const sot=drug('sotalol').modalities.ckd.tables[0].rows.map(r=>r.dose);assert.deepEqual(sot,['Every 12 h','Every 24 h','Every 36–48 h','Individualise the dose']);
const dof=drug('dofetilide').modalities.ckd.tables[0].rows.map(r=>r.dose);assert.deepEqual(dof,['500 mcg twice daily','250 mcg twice daily','125 mcg twice daily','Contraindicated']);
assert.deepEqual(drug('milrinone').modalities.ckd.tables[0].rows.map(r=>r.dose.split(' ')[0]),['0.43','0.38','0.33','0.28','0.23','0.20']);
// 3. Coverage and derived files.
assert.deepEqual(db.coverage,{renal:383,safety:26,catalog:260});
const q=JSON.parse(read('./dist/CURATION_QUEUE.json')),r=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));
assert.equal(q.version,'0.12.5');assert.equal(q.drugs.length,db.drugs.length);for(const x of q.drugs)assert.equal(x.content,drug(x.id).entryType);
assert.equal(r.remaining.length,db.coverage.safety+db.coverage.catalog);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.12.5'));
console.log(`PASS: ${Object.keys(C).length} entries changed (${promoted} promoted to renal profiles), others identical to v0.12.4; nothing curated was overwritten; ${newPk} new PK values; ${quotes} label quotes verified.`);
