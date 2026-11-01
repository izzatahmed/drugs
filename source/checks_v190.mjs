import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v180.json'));
const C=JSON.parse(read('./curation_v190.json')),Q=JSON.parse(read('./label_quotes_v190.json'));
assert.equal(db.version,'0.19.0');assert.equal(db.clinicalDataVersion,'0.19.0');
const src=new Map(db.sources.map(s=>[s.id,s])),drug=id=>db.drugs.find(d=>d.id===id);
const inLabel=(id,e)=>{const two=e.startsWith('2|'),q=(two?e.slice(2):e).replace(/\.$/,'');return (two?Q[id].windows2:Q[id].windows).some(w=>w.includes(q))||(!two&&Q[id].windows2&&Q[id].windows2.some(w=>w.includes(q)));};
const CORE=['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'];
let quotes=0,promoted=0,newPk=0;
const tpl=base.drugs.find(x=>x.entryType==='catalog'&&x.pharmacokinetics.status==='not_curated'&&!x.sharedGuidanceId);const IX=JSON.parse(read('./interactions_v190.json'));let added=0;
for(const d of db.drugs){const c=C[d.id];let o=base.drugs.find(x=>x.id===d.id);
 if(!o){assert.ok(c&&c.new,`${d.id} unexpected new record`);added++;assert.equal(d.addedInVersion,'0.19.0');assert.equal(d.name,c.new.name);assert.equal(d.category,c.new.category);
  o={...structuredClone(tpl),id:d.id,name:d.name,aliases:d.aliases,category:d.category};delete o.pregnancyLactation;}
 if(d.interactions){const v=IX.drugs[d.id];if(v){assert.deepEqual(d.interactions.statements,v.statements);assert.equal(d.interactions.sourceIds[0],`ix190-${d.id}`);assert.ok(src.get(`ix190-${d.id}`).url.startsWith('https://'));}else assert.deepEqual(d.interactions.statements,[]);assert.deepEqual(d.interactions.fdaRoles,IX.roles[d.id]||[]);if(d.interactions.fdaRoles.length)assert.ok(d.interactions.sourceIds.includes('fda-cyp-table'));}
 {const {interactions:_i,updatedInVersion:_u,...dd}=d,{interactions:_j,updatedInVersion:_v,...oo}=o;if(!c){assert.deepEqual(dd,oo,`${d.id} changed beyond interactions`);continue;}}
 for(const k of ['pregnancyLactation','referenceChecks','aliases','name','category'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);
 const sid=`us190-${d.id}`,s=src.get(sid);for(const x of c.extraSources||[]){assert.ok(src.has(x),x);assert.ok(d.sourceIds.includes(x),`${d.id} cites ${x}`);}assert.ok(s&&/^https:\/\//.test(s.url),`${d.id} source`);assert.equal(s.label.setid,Q[d.id].meta.setid);
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
// 2. Key content: new records, vaccines, interactions.
const rows=(id,k='ckd',n=0)=>drug(id).modalities[k].tables[n].rows.map(r=>r.dose);
assert.equal(added,Object.values(C).filter(c=>c.new).length);
assert.deepEqual(rows('vaccine-hepatitis-b-engerix','ihd'),['2 mL at 0, 1, 2 and 6 months','Annual anti-HBs; 2 mL booster when below 10 mIU/mL']);
assert.equal(drug('vaccine-hepatitis-b-heplisav').modalities.ihd.status,'insufficient_data');assert.equal(drug('aprocitentan').modalities.ihd.status,'avoid');
assert.deepEqual(rows('lomitapide','ihd'),['Maximum 40 mg per day']);
for(const id of Object.keys(C).filter(i=>i.startsWith('vaccine-'))){assert.equal(drug(id).category,'Vaccines');for(const s of ['cdc-hd-vaccination','cdc-adult-schedule','cdc-altered-immunocompetence'])assert.ok(drug(id).sourceIds.includes(s));}
assert.ok(Object.keys(IX.drugs).length>=90);for(const id of ['tacrolimus','cyclosporine','spironolactone','lisinopril','rifampicin','clarithromycin','carbamazepine','amlodipine'])assert.ok(drug(id).interactions.statements.length>=3,id);
assert.ok(drug('tacrolimus').interactions.fdaRoles.some(r=>/3A sensitive substrate/.test(r)));assert.ok(drug('clarithromycin').interactions.fdaRoles.some(r=>/3A strong inhibitor/.test(r)));
assert.ok(db.interactionClasses['Strong CYP3A inhibitors'].members.includes('itraconazole'));assert.ok(db.interactionClasses['CYP3A inducers'].members.includes('rifampicin'));
// 2b. Checker logic (pure part of dist/interactions.js) on known label pairs.
{const vm=await import('node:vm');const code=read('./dist/interactions.js');const ctx=vm.createContext({});vm.runInContext(code.slice(0,code.indexOf('function interactionsPanel'))+';this.I=Interactions;',ctx);const I=ctx.I;
 const pair=(x,y)=>I.check(db,drug(x),drug(y));
 const tc=pair('tacrolimus','clarithromycin');assert.ok(tc.ab.length>0&&tc.mech.some(m=>/clarithromycin/i.test(m)&&/strong CYP3A inhibitor/.test(m)&&/may rise/.test(m)),'tacrolimus+clarithromycin');
 assert.ok(pair('spironolactone','lisinopril').ab.some(s=>/potassium/i.test(s.text)));
 assert.ok(pair('apixaban','rifampicin').ab.length>0&&pair('rifampicin','tacrolimus').mech.some(m=>/may fall/.test(m)));
 assert.ok(pair('amlodipine','simvastatin').ab.some(s=>/20 mg/.test(s.text)));
 assert.ok(pair('digoxin','clarithromycin').mech.some(m=>/P-gp/.test(m)));
 const none=pair('cetirizine-oral','paracetamol-iv');assert.equal(none.ab.length+none.ba.length+none.mech.length,0);}
// 3. Coverage and derived files.
assert.deepEqual(db.coverage,{renal:696,safety:10,catalog:21});
const q=JSON.parse(read('./dist/CURATION_QUEUE.json')),r=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));
assert.equal(q.version,'0.19.0');assert.equal(q.drugs.length,db.drugs.length);for(const x of q.drugs)assert.equal(x.content,drug(x.id).entryType);
assert.equal(r.remaining.length,db.coverage.safety+db.coverage.catalog);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.19.0'));
console.log(`PASS: ${Object.keys(C).length} entries changed (${promoted} promoted to renal profiles), others identical to v0.18.0; nothing curated was overwritten; ${newPk} new PK values; ${quotes} label quotes verified.`);
