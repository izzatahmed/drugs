import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v122.json'));
const ext=JSON.parse(read('./pk_extract_v123.json')),second=JSON.parse(read('./pk_review_v123b.json'));
assert.equal(db.version,'0.12.3');assert.equal(db.clinicalDataVersion,'0.12.1','No dosing change in this release');
const src=new Map(db.sources.map(s=>[s.id,s]));
const CORE=['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'];
const WORDING=/older normal-dose dialysis advice from other references|88-microgram base-strength doses from non-US references|while the older BC source differs/;
// 1. Dose tables (apart from three handbook mentions reworded), pregnancy sections and statuses unchanged from v0.12.2.
const strip=o=>JSON.stringify(o).replace(/do not substitute (the historical handbook’s 88-microgram base strengths|88-microgram base-strength doses from non-US references)/g,'X').replace(/Do not transfer (the 2018 handbook’s normal-dose dialysis advice|older normal-dose dialysis advice from other references) into this entry/g,'X').replace(/while the older (BC\/handbook sources differ|BC source differs)/g,'X');
let reworded=0;
for(const d of db.drugs){const o=base.drugs.find(x=>x.id===d.id);assert.ok(o,d.id);
 if(WORDING.test(JSON.stringify(d.modalities)+d.considerations))reworded++;
 assert.equal(strip(d.modalities),strip(o.modalities),`${d.id} dosing changed`);assert.equal(strip(d.considerations),strip(o.considerations));
 for(const k of ['kidneyMetric','summary','flag','entryType','pregnancyLactation','referenceChecks','review'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);
 // PK of drugs outside the rebuild is untouched.
 if(!ext[d.id])assert.deepEqual(d.pharmacokinetics,o.pharmacokinetics,`${d.id} PK changed`);}
assert.ok(reworded>=2&&reworded<=3,`reworded ${reworded}`);
// 2. The handbook is gone.
const all=JSON.stringify(db);assert.ok(!all.includes('rdh5'),'rdh5 source left');
assert.ok(!JSON.stringify(db.drugs).match(/[Hh]andbook|fifth[- ]edition/),'handbook wording left in drugs');
assert.ok(!db.referenceResources.some(r=>/Renal Drug Handbook/.test(r.title)));
for(const d of db.drugs)assert.ok(!d.pharmacokinetics.historical&&!d.pharmacokinetics.evidenceDate,d.id);
// 3. Every rebuilt value cites a DailyMed, EMA or emc source and quotes its sentence; numbers in the value appear in that sentence.
let values=0,dial=0;
for(const id of Object.keys(ext)){const p=db.drugs.find(d=>d.id===id).pharmacokinetics;
 const facts=[...CORE.map(k=>[k,p[k]]),...['ihd','pd'].map(m=>['dial-'+m,p.dialysability[m]])];
 for(const [k,f] of facts){
  if(f.value===null){assert.ok(['not_curated','not_reported','unknown'].includes(f.status)||f.status==='not_curated',`${id}/${k}`);continue;}
  if(!f.sourceIds.some(s=>s.startsWith('pk123-')))continue; // value kept from a non-handbook source (UKKA, label PK added earlier)
  k.startsWith('dial')?dial++:values++;
  assert.ok(f.evidence&&f.evidence.length>10,`${id}/${k} has no quoted sentence`);
  assert.ok(f.context.includes(f.evidence.replace(/\.$/,'')),`${id}/${k} context lacks the quote`);
  const s=src.get(f.sourceIds[0]);assert.ok(s,`${id}/${k} source`);assert.match(s.url,/^https:\/\/(dailymed\.nlm\.nih\.gov|www\.ema\.europa\.eu|www\.medicines\.org\.uk)\//);
  assert.equal(s.accessed,'2026-10-31');
  if(!k.startsWith('dial'))for(const n of f.value.match(/\d+(?:\.\d+)?/g)||[])assert.ok(f.evidence.includes(n),`${id}/${k}: ${n} not in quoted sentence`);
  if(f.basis)assert.equal(f.basis,'label_renal_impairment');}}
// 4. US-label quotes come from the stored extraction (first pass) or the reviewed second pass.
const firstPass=new Set(Object.entries(ext).flatMap(([id,e])=>Object.values(e.found).map(f=>f.sentence.replace(/\s+/g,' '))));
const secondPass=new Set(second.map(a=>a.evidence));
for(const id of Object.keys(ext))if(ext[id].meta){const p=db.drugs.find(d=>d.id===id).pharmacokinetics;
 for(const f of [...CORE.map(k=>p[k]),p.dialysability.ihd,p.dialysability.pd])if(f.value!==null&&f.sourceIds.some(s=>s.startsWith('pk123-'))){
  const q=f.evidence.replace(/\.$/,'');assert.ok(secondPass.has(q)||[...firstPass].some(s=>s.includes(q)),`${id}: quote not from the stored label text`);}}
// 5. Metabolite values are labelled, reviewed errors are not reintroduced.
const pk=id=>db.drugs.find(d=>d.id===id).pharmacokinetics;
assert.match(pk('oxcarbazepine').volumeOfDistribution.value,/MHD/);assert.match(pk('sulfasalazine').proteinBinding.value,/sulfasalazine/);
assert.match(pk('mesalazine').proteinBinding.value,/^43±6%/);assert.equal(pk('aprepitant').dialysability.ihd.status,'not_removed');
assert.equal(pk('tigecycline').dialysability.ihd.status,'not_removed');assert.equal(pk('propafenone').halfLife.value===null||!/10–32/.test(pk('propafenone').halfLife.value),true);
assert.match(pk('hydroxychloroquine').halfLife.value,/40–50 days/);assert.match(pk('vildagliptin').volumeOfDistribution.value,/^71 L/);
assert.match(src.get('pk123-vildagliptin').url,/ema\.europa\.eu/);assert.match(src.get('pk123-teicoplanin').url,/medicines\.org\.uk/);
// 6. Coverage counts and no orphan PK sources.
const cited=new Set(all.match(/"pk123-[^"]+"/g).map(s=>s.slice(1,-1)));for(const s of db.sources)if(s.id.startsWith('pk123-'))assert.ok(cited.has(s.id),`${s.id} unused`);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.12.3'));
assert.ok(!read('./dist/app.js').includes('Renal Drug Handbook fifth edition'));
console.log(`PASS: dosing and pregnancy unchanged; handbook removed; ${values} PK values and ${dial} dialysis statements quoted from DailyMed/EMA/emc labels; PK coverage ${db.pharmacokineticCoverage.profiles}/${db.pharmacokineticCoverage.allFourCoreFields}.`);
