import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
const data=JSON.parse(readFileSync(new URL('./dist/database.json',import.meta.url),'utf8'));
const ids=new Set(data.drugs.map(d=>d.id));
const refs=new Map(data.sources.map(s=>[s.id,s]));
assert.equal(data.drugs.length,668);
assert.equal(ids.size,668,'Drug IDs must be unique');
assert.equal(data.drugs.filter(d=>d.addedInVersion==='0.2.0').length,40);
assert.equal(data.version,'0.6.0');
assert.deepEqual(data.coverage,{renal:113,safety:28,catalog:527});
assert.equal(data.drugs.filter(d=>d.addedInVersion==='0.3.0'&&d.entryType==='renal'&&d.id!=='captopril'&&d.updatedInVersion!=='0.6.0').length,30);
assert.equal(refs.size,data.sources.length,'Source IDs must be unique');
assert.match(data.clinicalStatus,/not approved/i);
const allowed=['summarized','not_curated','insufficient_data','specialist','avoid','not_indicated'];
for(const d of data.drugs){
  assert.ok(d.name&&d.drugClass&&d.kidneyMetric&&d.formulation);
  assert.equal(d.review.status,'clinical_review_pending');
  assert.equal(d.review.clinicalReviewer,null);
  assert.equal(d.review.clinicalApprovedAt,null);
  assert.ok(d.routes.length);
  assert.ok(['renal','safety','catalog'].includes(d.entryType));
  if(d.entryType==='catalog'){assert.equal(d.sourceIds.length,0);assert.equal(d.review.sourceCheckedAt,null);for(const m of Object.values(d.modalities)){assert.equal(m.tables.length,0);assert.equal(m.status,'not_curated');}}
  else{assert.ok(d.sourceIds.length);assert.equal(d.review.sourceCheckedAt,'2026-10-29');}
  if(d.entryType==='safety'){assert.ok(data.sharedGuidance[d.sharedGuidanceId]);for(const m of Object.values(d.modalities))assert.equal(m.tables.length,0);}
  assert.equal(d.referenceChecks.bnf.status,'comparison_pending','Never imply unavailable BNF monographs were checked');
  if(d.referenceChecks.pdr.status==='accessed')assert.ok(d.sourceIds.some(id=>refs.get(id).type==='PDR digital monograph'));
  assert.deepEqual(Object.keys(d.modalities),['ckd','ihd','crrt','pd','sled']);
  for(const id of d.sourceIds)assert.ok(refs.has(id),`Missing source ${id}`);
  for(const [mode,m] of Object.entries(d.modalities)){
    assert.ok(allowed.includes(m.status),`${d.id}/${mode} unknown status`);
    if(m.status==='summarized')assert.ok(m.tables.length,`${d.id}/${mode} empty summary`);
    if(m.tables.length)assert.ok(m.sourceIds.length,`${d.id}/${mode} unsourced tables`);
    for(const id of m.sourceIds)assert.ok(refs.has(id));
    for(const table of m.tables){
      assert.ok(table.indication&&table.rows.length);
      for(const row of table.rows)assert.ok(row.context&&row.dose);
    }
  }
  assert.equal(d.modalities.sled.tables.length,0,'No source-supported SLED regimen in this release');
  assert.notEqual(d.modalities.sled.status,'summarized');
}
for(const s of data.sources){assert.match(s.url,/^https:\/\//);assert.equal(s.accessed,'2026-10-29');}
const drug=id=>data.drugs.find(d=>d.id===id);
assert.match(drug('sitagliptin').kidneyMetric,/eGFR.*1.73/);
assert.deepEqual(drug('sitagliptin').modalities.ckd.tables[0].rows.map(x=>x.context),['≥45','30 to <45','<30']);
assert.equal(drug('sitagliptin').modalities.pd.tables[0].rows[0].dose,'25 mg PO once daily');
assert.equal(drug('metformin').modalities.ihd.status,'avoid');
assert.equal(drug('apixaban').modalities.ihd.tables.length,0,'Do not auto-select a dialysis apixaban dose');
assert.match(drug('apixaban').considerations,/at least|criteria/i);
assert.match(drug('cefepime').modalities.ihd.notes,/DIFFERENT SOURCE REGIMENS/);
assert.match(drug('cefepime').modalities.pd.notes,/not curated/);
assert.equal(drug('enoxaparin').modalities.ihd.tables.length,0,'Severe CKD regimen must not be copied into IHD');
assert.match(drug('gabapentin').modalities.ckd.tables[0].indication,/ranges/);
assert.match(drug('allopurinol').modalities.ckd.tables[0].indication,/initial/);
assert.equal(drug('daprodustat').modalities.ckd.status,'not_indicated');
assert.match(drug('daprodustat').marketStatus,/discontinued/i);
assert.match(drug('nirmatrelvir-ritonavir').modalities.ihd.notes,/5-day total course/);
assert.equal(drug('nirmatrelvir-ritonavir').modalities.ckd.tables[0].rows.at(-1).dose,'150 mg nirmatrelvir + 100 mg ritonavir PO once daily');
assert.match(drug('finerenone').modalities.ckd.tables[1].rows[1].dose,/40 mg/);
assert.match(drug('finerenone').modalities.ckd.tables[1].rows[0].dose,/20 mg/);
assert.equal(drug('finerenone').referenceChecks.pdr.status,'update_bulletin_checked');
assert.match(drug('dabigatran').modalities.ckd.tables[1].rows[0].dose,/Contraindicated/);
assert.match(drug('sodium-zirconium-cyclosilicate').modalities.ihd.tables[0].rows[0].dose,/NON-dialysis days only/);
assert.match(drug('difelikefalin').modalities.ihd.tables[0].rows[0].dose,/0.5 micrograms\/kg/);
assert.equal(drug('cefiderocol').modalities.crrt.tables[0].rows.length,4);
assert.match(drug('cefiderocol').modalities.crrt.settingMeasure,/effluent/);
assert.equal(drug('cefiderocol').sourceIds.some(id=>refs.get(id).title.startsWith('UCSF')),false);
const original=JSON.parse(readFileSync(new URL('./baseline_v02.json',import.meta.url),'utf8'));
for(const [id,old] of Object.entries(original)){assert.equal(drug(id).addedInVersion,old.addedInVersion);assert.deepEqual(drug(id).modalities,old.modalities,`${id}: original dosing changed unexpectedly`);}
for(const file of ['index.html','styles.css','app.js','database.json','EDITORIAL_GUIDE.md','CHANGELOG.md','icon.svg'])assert.ok(existsSync(new URL(`./dist/${file}`,import.meta.url)));
for(const g of Object.values(data.sharedGuidance)){assert.ok(g.title&&g.text&&g.sourceIds.length);g.sourceIds.forEach(id=>assert.ok(refs.has(id)));}
assert.deepEqual(drug('famotidine').routes,['Oral'],'Do not infer IV route from the word non-erosive');
assert.deepEqual(drug('semaglutide-sc').routes,['Parenteral']);
assert.equal(drug('baclofen').modalities.ihd.tables.length,0);
assert.equal(drug('etelcalcetide').modalities.pd.status,'not_indicated');
assert.equal(drug('cinacalcet').modalities.ckd.status,'not_indicated');
assert.equal(drug('cetirizine-oral').modalities.ckd.tables[0].rows[1].dose,'No more than 5 mg PO once daily');
assert.equal(drug('metoclopramide').modalities.pd.tables[0].rows[0].dose,'5 mg PO twice daily; maximum 10 mg/day');
assert.equal(drug('warfarin').review.sourceCheckedAt,null);
assert.equal(drug('ibuprofen').sharedGuidanceId,'systemic-nsaid');
assert.match(data.referenceScope.pnfStatus,/British National Formulary/);
const html=readFileSync(new URL('./dist/index.html',import.meta.url),'utf8');
const embedded=JSON.parse(html.match(/<script id="renalrounds-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
assert.deepEqual(embedded,data,'Embedded offline data must match export');
assert.ok(!/<script[^>]+src=|<link[^>]+rel="stylesheet"/i.test(html),'No required external runtime code or styles');
assert.ok(!/\bfetch\s*\(/.test(readFileSync(new URL('./dist/app.js',import.meta.url),'utf8')),'No runtime database fetch');
const docs=JSON.parse(html.match(/<script id="renalrounds-docs" type="application\/json">([\s\S]*?)<\/script>/)[1]);
assert.equal(docs.guide,readFileSync(new URL('./dist/EDITORIAL_GUIDE.md',import.meta.url),'utf8'));
assert.equal(docs.changelog,readFileSync(new URL('./dist/CHANGELOG.md',import.meta.url),'utf8'));
assert.ok(existsSync(new URL('./dist/.nojekyll',import.meta.url)));
const before=JSON.parse(readFileSync(new URL('./baseline_v03.json',import.meta.url),'utf8'));
for(const [id,modalities] of Object.entries(before))if(!['captopril','amlodipine','losartan','valsartan','candesartan','irbesartan','telmisartan','bisoprolol','enalapril','ramipril','clonidine','hydralazine','methyldopa','indapamide'].includes(id))assert.deepEqual(drug(id).modalities,modalities,`${id}: unrelated v0.3 regimen changed`);
const pkFields=['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'];
let pkCount=0,fullCount=0;
for(const d of data.drugs){
 const p=d.pharmacokinetics;assert.ok(p,'All drugs expose a PK curation state');
 assert.deepEqual(Object.keys(p.dialysability),['ihd','pd','crrt','sled']);
 const facts=[...pkFields.map(k=>p[k]),...Object.values(p.dialysability)];
 for(const f of facts){assert.ok(f&&f.status);assert.ok(Array.isArray(f.sourceIds));f.sourceIds.forEach(id=>assert.ok(refs.has(id),`${d.id}: missing PK source ${id}`));if(f.value!==null)assert.ok(f.sourceIds.length,`${d.id}: unsourced PK value`);if(['not_reported','not_curated'].includes(f.status))assert.equal(f.value,null);}
 if(p.status==='source_summary'){pkCount++;assert.equal(p.sourceCheckedAt,'2026-10-29');assert.ok(p.halfLife.value);}else{assert.equal(p.sourceCheckedAt,null);facts.forEach(f=>assert.equal(f.value,null));}
 if(['halfLife','volumeOfDistribution','proteinBinding'].every(k=>p[k].status==='sourced')&&p.dialysability.ihd.value!==null)fullCount++;
 for(const k of ['crrt','sled']){assert.equal(p.dialysability[k].status,'not_curated','Never infer circuit clearance from protein binding/Vd');assert.equal(p.dialysability[k].value,null);}
}
assert.equal(pkCount,27);assert.equal(fullCount,15);assert.deepEqual(data.pharmacokineticCoverage,{profiles:pkCount,allFourCoreFields:fullCount});
const cap=drug('captopril'),am=drug('amlodipine');
assert.equal(cap.entryType,'renal');assert.match(cap.kidneyMetric,/CrCl.*1.73/);
assert.match(cap.modalities.ckd.tables[0].indication,/TOTAL daily/);
assert.equal(cap.modalities.ckd.tables[0].rows[3].dose,'Initial total 6.25 mg/day; maximum total 37.5 mg/day');
assert.equal(cap.modalities.ihd.tables.length,0,'Do not copy CKD captopril totals to HD');
assert.equal(cap.pharmacokinetics.dialysability.ihd.status,'removed');
assert.equal(cap.pharmacokinetics.dialysability.pd.status,'not_removed');
assert.match(cap.pharmacokinetics.volumeOfDistribution.context,/Steady-state Vss/);
assert.match(cap.pharmacokinetics.notes,/free parent versus total/);
assert.equal(am.pharmacokinetics.halfLife.value,'35–50 h');
assert.equal(am.pharmacokinetics.proteinBinding.value,'About 97.5%');
assert.equal(am.pharmacokinetics.dialysability.ihd.status,'not_removed');
assert.match(am.modalities.ckd.tables[0].rows[0].dose,/5 mg.*maximum 10 mg/);
assert.equal(drug('bisoprolol').pharmacokinetics.dialysability.ihd.status,'removed');
assert.equal(drug('carvedilol').pharmacokinetics.dialysability.ihd.status,'negligible');
assert.equal(drug('ramipril').pharmacokinetics.dialysability.ihd.status,'source_difference');
assert.equal(drug('warfarin').pharmacokinetics.status,'not_curated');
assert.equal(drug('losartan').entryType,'renal');assert.equal(drug('losartan').review.sourceCheckedAt,'2026-10-29');assert.equal(drug('losartan').pharmacokinetics.status,'source_summary');
assert.ok(existsSync(new URL('./dist/pk.js',import.meta.url)));
console.log(`PASS: 668 records, 113 renal profiles, 28 safety notes, 527 dose-pending catalog entries; ${pkCount} source-based PK profiles (${fullCount} with all four core fields), ${data.sources.length} sources. Original 70 profiles retained; captopril/amlodipine plus the 12 v0.6 profiles are the only modality changes since v0.3. PK provenance, units/context, ESRF distinctions and explicit RRT gaps checked. Standalone data/documents match sources.`);
console.log('Software/data integrity checks do not establish clinical validity. Independent clinical review remains pending.');
