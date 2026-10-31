import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v150.json'));
const C=JSON.parse(read('./curation_v160.json')),Q=JSON.parse(read('./label_quotes_v160.json'));
assert.equal(db.version,'0.16.0');assert.equal(db.clinicalDataVersion,'0.16.0');
const src=new Map(db.sources.map(s=>[s.id,s])),drug=id=>db.drugs.find(d=>d.id===id);
const inLabel=(id,e)=>{const two=e.startsWith('2|'),q=(two?e.slice(2):e).replace(/\.$/,'');return (two?Q[id].windows2:Q[id].windows).some(w=>w.includes(q))||(!two&&Q[id].windows2&&Q[id].windows2.some(w=>w.includes(q)));};
const CORE=['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'];
let quotes=0,promoted=0,newPk=0;
const tpl=base.drugs.find(x=>x.id==='docusate');let added=0;
for(const d of db.drugs){const c=C[d.id];let o=base.drugs.find(x=>x.id===d.id);
 if(!o){assert.ok(c&&c.new,`${d.id} unexpected new record`);added++;assert.equal(d.addedInVersion,'0.16.0');assert.equal(d.name,c.new.name);assert.equal(d.category,c.new.category);
  o={...structuredClone(tpl),id:d.id,name:d.name,aliases:d.aliases,category:d.category};delete o.pregnancyLactation;}
 if(!c){assert.deepEqual(d,o,`${d.id} changed`);continue;}
 for(const k of ['pregnancyLactation','referenceChecks','aliases','name','category'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);
 const sid=`us160-${d.id}`,s=src.get(sid);for(const x of c.extraSources||[]){assert.ok(src.has(x),x);assert.ok(d.sourceIds.includes(x),`${d.id} cites ${x}`);}assert.ok(s&&/^https:\/\/dailymed\.nlm\.nih\.gov\//.test(s.url),`${d.id} source`);assert.equal(s.label.setid,Q[d.id].meta.setid);
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
assert.equal(added,Object.values(C).filter(c=>c.new).length);
assert.deepEqual(rows('fludarabine'),['Reduce dose by 20% and monitor closely','Do not administer']);
assert.deepEqual(rows('topotecan'),['No dose adjustment (1.5 mg/m²/day × 5 days)','0.75 mg/m²/day']);
assert.equal(rows('gadodiamide')[1],'Contraindicated');assert.equal(drug('gadodiamide').modalities.ihd.status,'avoid');
for(const g of ['gadobutrol','gadoterate','gadoteridol','gadobenate','gadopiclenol'])assert.match(drug(g).considerations,/^ACR group II /);
assert.match(drug('gadoxetate').considerations,/^ACR group III /);assert.match(drug('gadodiamide').considerations,/^ACR group I /);
for(const g of ['iohexol','iodixanol','iopamidol','ioversol','iopromide']){assert.equal(drug(g).category,'Contrast media');assert.ok(drug(g).sourceIds.includes('acr-nkf-icm-2020'));}
assert.equal(drug('sugammadex').modalities.ihd.status,'avoid');
// 3. Coverage and derived files.
assert.deepEqual(db.coverage,{renal:651,safety:15,catalog:44});
const q=JSON.parse(read('./dist/CURATION_QUEUE.json')),r=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));
assert.equal(q.version,'0.16.0');assert.equal(q.drugs.length,db.drugs.length);for(const x of q.drugs)assert.equal(x.content,drug(x.id).entryType);
assert.equal(r.remaining.length,db.coverage.safety+db.coverage.catalog);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.16.0'));
console.log(`PASS: ${Object.keys(C).length} entries changed (${promoted} promoted to renal profiles), others identical to v0.15.0; nothing curated was overwritten; ${newPk} new PK values; ${quotes} label quotes verified.`);
