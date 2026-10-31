import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v140.json'));
const C=JSON.parse(read('./curation_v150.json')),Q=JSON.parse(read('./label_quotes_v150.json'));
assert.equal(db.version,'0.15.0');assert.equal(db.clinicalDataVersion,'0.15.0');
const src=new Map(db.sources.map(s=>[s.id,s])),drug=id=>db.drugs.find(d=>d.id===id);
const inLabel=(id,e)=>{const two=e.startsWith('2|'),q=(two?e.slice(2):e).replace(/\.$/,'');return (two?Q[id].windows2:Q[id].windows).some(w=>w.includes(q))||(!two&&Q[id].windows2&&Q[id].windows2.some(w=>w.includes(q)));};
const CORE=['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'];
const WITHDRAWN=['exenatide-extended-release','glycopyrronium-inhaled'];for(const id of WITHDRAWN)assert.ok(!src.has(`preg122-${id}`));
let quotes=0,promoted=0,newPk=0;
for(const d of db.drugs){const o=base.drugs.find(x=>x.id===d.id);assert.ok(o);const c=C[d.id];
 if(WITHDRAWN.includes(d.id)){assert.equal(d.pregnancyLactation,undefined);const{pregnancyLactation:_,updatedInVersion:__,...a}=o,{updatedInVersion:___,...b}=d;if(!c){assert.deepEqual(b,a,`${d.id} changed`);continue;}}
 if(!c){assert.deepEqual(d,o,`${d.id} changed`);continue;}
 for(const k of [...(WITHDRAWN.includes(d.id)?[]:['pregnancyLactation']),'referenceChecks','aliases','name','category'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);
 const sid=`us150-${d.id}`,s=src.get(sid);assert.ok(s&&/^https:\/\/dailymed\.nlm\.nih\.gov\//.test(s.url),`${d.id} source`);assert.equal(s.label.setid,Q[d.id].meta.setid);
 if(c.promote){promoted++;assert.equal(o.entryType==='renal',false);assert.equal(d.entryType,'renal');assert.notEqual(d.flag,'catalog');assert.equal(d.sourceIds[0],sid);}else if(o.entryType!=='renal'){assert.equal(d.entryType,o.entryType);assert.deepEqual(d.modalities,o.modalities);}
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
const rows=(id,k='ckd',n=0)=>drug(id).modalities[k].tables[n].rows.map(r=>r.dose);
assert.equal(drug('cyclophosphamide').entryType,'renal');assert.ok(drug('cyclophosphamide').aliases.some(a=>/cytoxan/i.test(a)));
assert.equal(drug('rituximab').entryType,'renal');
assert.deepEqual(rows('tofacitinib'),['5 mg twice daily','5 mg once daily','5 mg once daily']);
assert.ok(rows('nizatidine').includes('150 mg every 3 days'));
assert.equal(drug('ketorolac').modalities.ihd.status,'avoid');
assert.ok(drug('meloxicam').modalities.ihd.tables[0].rows[0].dose.startsWith('Maximum 7.5 mg'));
// 3. Coverage and derived files.
assert.deepEqual(db.coverage,{renal:607,safety:15,catalog:47});
const q=JSON.parse(read('./dist/CURATION_QUEUE.json')),r=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));
assert.equal(q.version,'0.15.0');assert.equal(q.drugs.length,db.drugs.length);for(const x of q.drugs)assert.equal(x.content,drug(x.id).entryType);
assert.equal(r.remaining.length,db.coverage.safety+db.coverage.catalog);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.15.0'));
console.log(`PASS: ${Object.keys(C).length} entries changed (${promoted} promoted to renal profiles), others identical to v0.14.0; nothing curated was overwritten; ${newPk} new PK values; ${quotes} label quotes verified.`);
