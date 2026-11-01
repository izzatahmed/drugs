import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v170.json'));
const C=JSON.parse(read('./curation_v180.json')),Q=JSON.parse(read('./label_quotes_v180.json'));
assert.equal(db.version,'0.18.0');assert.equal(db.clinicalDataVersion,'0.18.0');
const src=new Map(db.sources.map(s=>[s.id,s])),drug=id=>db.drugs.find(d=>d.id===id);
const inLabel=(id,e)=>{const two=e.startsWith('2|'),q=(two?e.slice(2):e).replace(/\.$/,'');return (two?Q[id].windows2:Q[id].windows).some(w=>w.includes(q))||(!two&&Q[id].windows2&&Q[id].windows2.some(w=>w.includes(q)));};
const CORE=['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'];
let quotes=0,promoted=0,newPk=0;
const tpl=base.drugs.find(x=>x.id==='docusate');let added=0;
for(const d of db.drugs){const c=C[d.id];let o=base.drugs.find(x=>x.id===d.id);
 if(!o){assert.ok(c&&c.new,`${d.id} unexpected new record`);added++;assert.equal(d.addedInVersion,'0.18.0');assert.equal(d.name,c.new.name);assert.equal(d.category,c.new.category);
  o={...structuredClone(tpl),id:d.id,name:d.name,aliases:d.aliases,category:d.category};delete o.pregnancyLactation;}
 if(!c){assert.deepEqual(d,o,`${d.id} changed`);continue;}
 for(const k of ['pregnancyLactation','referenceChecks','aliases','name','category'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);
 const sid=`lb180-${d.id}`,s=src.get(sid);for(const x of c.extraSources||[]){assert.ok(src.has(x),x);assert.ok(d.sourceIds.includes(x),`${d.id} cites ${x}`);}assert.ok(s&&/^https:\/\//.test(s.url),`${d.id} source`);assert.equal(s.label.setid,Q[d.id].meta.setid);
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
// 2. Key tables and fine-print source notes.
const rows=(id,k='ckd',n=0)=>drug(id).modalities[k].tables[n].rows.map(r=>r.dose);
assert.equal(added,0);
assert.deepEqual(rows('paracetamol'),['Minimum interval 6 hours','Minimum interval 8 hours; use under medical supervision']);
assert.match(rows('cefoperazone-sulbactam')[1],/^Maximum 500 mg sulbactam every 12 h/);
for(const [id,host,note] of [['cefoperazone-sulbactam','labeling.pfizer.com',/Pfizer SULPERAZON product label \(Hong Kong/],['roxithromycin','www.medsafe.govt.nz',/New Zealand Data Sheet/],['paracetamol','www.geneesmiddeleninformatiebank.nl',/Dutch Medicines Evaluation Board/],['diphenoxylate-atropine','dailymed.nlm.nih.gov',/^US FDA label/]]){
  assert.equal(new URL(src.get(`lb180-${id}`).url).hostname,host);assert.match(drug(id).jurisdiction,note);assert.match(drug(id).jurisdiction,/JFDA/);}
assert.match(JSON.stringify(drug('paracetamol').modalities.ckd),/Dutch SmPC \(MEB\): “/);
// 3. Coverage and derived files.
assert.deepEqual(db.coverage,{renal:679,safety:10,catalog:21});
const q=JSON.parse(read('./dist/CURATION_QUEUE.json')),r=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));
assert.equal(q.version,'0.18.0');assert.equal(q.drugs.length,db.drugs.length);for(const x of q.drugs)assert.equal(x.content,drug(x.id).entryType);
assert.equal(r.remaining.length,db.coverage.safety+db.coverage.catalog);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.18.0'));
console.log(`PASS: ${Object.keys(C).length} entries changed (${promoted} promoted to renal profiles), others identical to v0.17.0; nothing curated was overwritten; ${newPk} new PK values; ${quotes} label quotes verified.`);
