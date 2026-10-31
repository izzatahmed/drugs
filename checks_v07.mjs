import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {performance} from 'node:perf_hooks';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json'));
const hash=x=>crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
const baseline=JSON.parse(read('./baseline_v06.json'));
const expanded=['losartan','valsartan','candesartan','irbesartan','telmisartan','bisoprolol','enalapril','ramipril','clonidine','hydralazine','methyldopa','indapamide'];
const newRenal=['acyclovir','amphotericin-b-deoxycholate','liposomal-amphotericin-b','aztreonam','cefadroxil','cefdinir','cefoxitin','cefpodoxime','ceftaroline','cefuroxime','clarithromycin','ethambutol','famciclovir','flucytosine','fosfomycin','ganciclovir','phenoxymethylpenicillin','tigecycline','valganciclovir','voriconazole'];
assert.deepEqual([...db.releaseChanges.newRenalIds].sort(),newRenal.sort());
assert.equal(db.releaseChanges.newPKIds.length,26);assert.equal(db.releaseChanges.pirrtSummaryIds.length,16);assert.equal(db.releaseChanges.changedIds.length,47);
for(const d of db.drugs){
 const old=baseline.drugs[d.id];assert.ok(old);
 if(!db.releaseChanges.changedIds.includes(d.id))assert.deepEqual(d,old,`${d.id}: unrelated record changed`);
 if(old.pharmacokinetics.status==='source_summary')assert.deepEqual(d.pharmacokinetics,old.pharmacokinetics,`${d.id}: old PK changed`);
 if(old.entryType==='renal')for(const key of ['ckd','ihd','pd','crrt'])assert.deepEqual(d.modalities[key],old.modalities[key],`${d.id}: existing ${key} changed`);
}
for(const old of baseline.sources)assert.deepEqual(db.sources.find(s=>s.id===old.id),old,`${old.id}: existing source changed`);
assert.deepEqual(db.sharedGuidance,baseline.sharedGuidance);
assert.equal(db.referenceScope.updatedEntries,47);assert.equal(db.referenceResources.length,14);
assert.deepEqual(JSON.parse(read('./dist/REFERENCE_DIRECTORY.json')),db.referenceResources);
assert.match(db.referenceScope.pnfStatus,/British National Formulary/);
const drug=id=>db.drugs.find(x=>x.id===id);
for(const id of expanded){const d=drug(id);assert.equal(d.entryType,'renal');assert.equal(d.review.clinicalApprovedAt,null);assert.equal(d.updatedInVersion,'0.6.0');for(const k of ['pd','crrt','sled']){assert.equal(d.modalities[k].status,'not_curated');assert.equal(d.modalities[k].tables.length,0);}}
assert.match(drug('bisoprolol').modalities.ckd.tables[0].rows[1].dose,/maximum 10 mg/);
assert.match(drug('bisoprolol').modalities.ckd.notes,/1.25.*not use the hypertension/i);
assert.match(drug('enalapril').modalities.ckd.tables[0].indication,/INITIAL TOTAL/);
assert.match(drug('enalapril').modalities.ihd.notes,/non-dialysis-day dosing.*not.*maintenance plan/i);
assert.match(drug('ramipril').modalities.ckd.notes,/overlap at 30 and 60/);
assert.match(drug('ramipril').modalities.ihd.notes,/daily regimen.*not.*thrice-weekly/);
assert.equal(drug('indapamide').modalities.ihd.status,'avoid');
assert.match(drug('indapamide').modalities.ckd.tables[0].rows[1].dose,/Contraindicated/);
assert.equal(drug('clonidine').modalities.ckd.status,'specialist');assert.match(drug('clonidine').modalities.ihd.tables[0].rows[0].dose,/No routine post-HD supplemental/);
assert.equal(drug('hydralazine').modalities.ckd.tables.length,0);
assert.equal(drug('methyldopa').modalities.ihd.tables.length,0);
assert.equal(drug('valsartan').modalities.ihd.status,'specialist');
assert.match(drug('valsartan').modalities.ckd.notes,/exact CrCl 10/);
assert.match(drug('candesartan').modalities.ihd.tables[0].rows[0].dose,/4 mg/);
assert.match(drug('irbesartan').modalities.ihd.tables[0].rows[0].dose,/75 mg/);
assert.match(drug('telmisartan').modalities.ihd.tables[0].rows[0].dose,/20 mg/);

// High-consequence units, timing, formulation and prescription regressions.
assert.equal(drug('ceftaroline').pharmacokinetics.volumeOfDistribution.value,'20.3 L');
assert.equal(drug('meropenem').pharmacokinetics.volumeOfDistribution.value,'0.35 L/kg');
assert.equal(drug('meropenem').pharmacokinetics.renalHalfLife.value,'6–13.7 h');
assert.equal(drug('ertapenem').pharmacokinetics.dialysability.pd.status,'removed');
assert.match(drug('doxycycline').pharmacokinetics.dialysability.ihd.value,/high-flux: unknown/);
assert.equal(drug('moxifloxacin').pharmacokinetics.dialysability.ihd.status,'unknown');
assert.equal(drug('moxifloxacin').pharmacokinetics.dialysability.ihd.value,null);
assert.equal(drug('piperacillin-tazobactam').pharmacokinetics.dialysability.pd.status,'source_difference');
for(const id of db.releaseChanges.newPKIds){const p=drug(id).pharmacokinetics;assert.equal(p.historical,true);assert.match(p.evidenceDate,/2018/);for(const key of ['crrt','sled'])assert.equal(p.dialysability[key].value,null);}
assert.equal(drug('clarithromycin').modalities.pd.status,'specialist');
assert.equal(drug('flucytosine').modalities.pd.tables.length,0);
assert.equal(drug('valganciclovir').pharmacokinetics.status,'not_curated');
assert.equal(drug('valganciclovir').modalities.ihd.tables.length,0);
assert.equal(drug('levofloxacin').modalities.sled.tables.length,0);
assert.match(drug('cefuroxime').modalities.ckd.tables[0].rows[1].dose,/every 24 h/);
assert.match(drug('cefuroxime').modalities.ckd.tables[0].rows[2].dose,/every 48 h/);
assert.match(drug('cefuroxime').formulation,/Oral/);assert.ok(drug('cefuroxime').evidenceNotes.length);
assert.match(drug('voriconazole').modalities.ckd.notes,/SBECD/);
assert.match(drug('acyclovir').modalities.ihd.notes,/daily.*not only/);
for(const id of db.releaseChanges.pirrtSummaryIds){const m=drug(id).modalities.sled;assert.match(m.settingMeasure,/Nebraska PIRRT/);assert.ok(m.notes);const ref=db.sources.find(s=>s.id===m.sourceIds[0]);assert.ok(ref.suppliedDocument.pdfPage>=10&&ref.suppliedDocument.pdfPage<=13);}
for(const id of ['acyclovir','aztreonam','ceftaroline','ganciclovir']){const m=drug(id).modalities.crrt;assert.match(m.settingMeasure,/CVVHD/);assert.match(m.notes,/not CVVH/);for(const t of m.tables.filter(t=>t.indication!=='Loading dose'))assert.deepEqual(t.rows.map(r=>r.context),['CVVHD dialysate 1 L/h','CVVHD dialysate 2 L/h','CVVHD dialysate 3–4 L/h']);}
assert.match(drug('meropenem').modalities.sled.notes,/3–4 hours/);
assert.match(drug('piperacillin-tazobactam').modalities.sled.settingMeasure,/6 L.h.*6-hour/);
const inventory=JSON.parse(read('./source_inventory_v07.json'));
assert.equal(inventory.length,5);assert.deepEqual(db.sourceAudit,inventory);
for(const s of db.sources.filter(s=>s.suppliedDocument)){const f=inventory.find(f=>f.fileName===s.suppliedDocument.fileName);assert.equal(s.suppliedDocument.sha256,f.sha256);assert.ok(s.suppliedDocument.pdfPage>0&&s.suppliedDocument.pdfPage<=f.pages);}
const valref=db.sources.find(s=>s.id===drug('valganciclovir').modalities.sled.sourceIds[0]);assert.equal(valref.suppliedDocument.pdfPage,13);
assert.equal(db.sourceConflicts.length,6);
const queue=JSON.parse(read('./dist/CURATION_QUEUE.json'));
assert.equal(queue.drugs.length,668);assert.equal(queue.version,db.version);
for(const q of queue.drugs){const d=db.drugs.find(x=>x.id===q.id);assert.equal(q.renalDoseSourceCheckedAt,d.review.sourceCheckedAt);assert.deepEqual(q.modalities,Object.fromEntries(Object.entries(d.modalities).map(([k,v])=>[k,v.status])));}
const html=read('./dist/index.html'),docs=JSON.parse(html.match(/<script id="renalrounds-docs" type="application\/json">([\s\S]*?)<\/script>/)[1]);
assert.equal(docs.plan,read('./dist/COMPLETION_PLAN.md'));
const manifest=JSON.parse(read('./dist/manifest.webmanifest'));assert.equal(manifest.scope,'./');assert.equal(manifest.start_url,'./');
const controls={'#route-filter':{value:'all'},'#content-filter':{value:'all'},'#setting-filter':{value:'all'},'#otc-filter':{checked:false}};
const ctx=vm.createContext({db,controls,performance});
const app=read('./dist/app.js'),workflow=read('./dist/workflow.js');
vm.runInContext(`const $=q=>controls[q];const norm=${app.match(/const norm = ([^\n]+);/)[1]};let category='all',view='all',favourites=new Set(),clinicalVersionCache;
${workflow.match(/function latestClinicalVersion\(\)\{[^\n]+/)[0]}
${workflow.slice(workflow.indexOf('function suggestions('),workflow.indexOf('function renderCompletion('))}
${app.slice(app.indexOf('function filterDrugs('),app.indexOf('function renderResults('))}
db.drugs.forEach(d=>{d.searchText=norm([d.name,...d.aliases,d.drugClass,d.category,...d.routes].join(' '));d.nameKeys=[d.name,...d.aliases].map(norm);});`,ctx);
const run=code=>vm.runInContext(code,ctx);
assert.equal(run("filterDrugs('Capoten','all',false)[0].id"),'captopril');
assert.equal(run("filterDrugs('Norvasc','all',false)[0].id"),'amlodipine');
assert.equal(run("filterDrugs('AMLODIPINE','all',false)[0].id"),'amlodipine');
assert.equal(run("filterDrugs('amlodpine','all',false).length"),0);
assert.equal(run("suggestions('amlodpine')[0].id"),'amlodipine');
assert.equal(run("suggestions('x').length"),0);
controls['#content-filter'].value='pk';assert.equal(run("filterDrugs('','all',false).length"),53);
controls['#content-filter'].value='all';controls['#setting-filter'].value='sled';assert.equal(run("filterDrugs('','all',false).length"),16);
controls['#setting-filter'].value='pd';assert.equal(run("filterDrugs('','all',false).length"),db.drugs.filter(d=>d.modalities.pd.status==='summarized').length);
controls['#setting-filter'].value='all';run("view='new'");assert.equal(run("filterDrugs('','all',false).length"),47);run("view='all'");
const elapsed=run("(()=>{const start=performance.now();for(let i=0;i<1000;i++)filterDrugs(['captopril','metformin','cef','a','Norvasc','amlo'][i%6],'all',false);return performance.now()-start;})()");
console.log(`PASS: actual search functions, brand/exact ordering, explicit spelling suggestions, modality/PK/latest filters. 1,000 queries: ${elapsed.toFixed(1)} ms on this container (not a phone benchmark).`);

// Execute the actual service worker with deterministic network/cache contracts.
const store=new Map();
const caches={async keys(){return [...store.keys()];},async delete(n){return store.delete(n);},async open(n){if(!store.has(n))store.set(n,new Map());const map=store.get(n);return {async put(k,v){map.set(typeof k==='string'?k:k.url,v.clone());},async match(k){return map.get(typeof k==='string'?k:k.url)?.clone();}};}};
let online=true,servedVersion='0.5.0',httpStatus=200;
function worker(version='0.5.0',build='old'){
 const events={},messages=[];let activated=false;
 const self={location:{href:'https://example.org/drugs/sw.js'},clients:{async claim(){}},async skipWaiting(){activated=true;},addEventListener:(n,f)=>events[n]=f};
 const expected=`<script id="renalrounds-data">{"version":"${version}"}</script>`;
 const checksum=build==='partial'?'incorrect':crypto.createHash('sha256').update(expected).digest('hex').slice(0,20);
 const code=read('./sw-template.js').replaceAll('__VERSION__',version).replaceAll('__BUILD__',checksum);
 vm.runInNewContext(code,{self,URL,Request,caches,crypto:crypto.webcrypto,TextEncoder,fetch:async()=>{if(!online)throw Error('offline');return new Response(`<script id="renalrounds-data">{"version":"${servedVersion}"}</script>`,{status:httpStatus,headers:{'content-type':'text/html'}});}});
 async function fire(type,extra={}){let result;events[type]({...extra,waitUntil:p=>result=p,respondWith:p=>result=p});return result===undefined?undefined:await result;}
 const navigate=url=>fire('fetch',{request:{url,method:'GET',mode:'navigate'}});
 return {fire,navigate,messages,get activated(){return activated;}};
}
store.set('unrelated-cache',new Map());store.set('renalrounds:/other/:old',new Map());store.set('renalrounds:/drugs/:obsolete',new Map());
const first=worker();await first.fire('install');await first.fire('activate');
assert.ok(store.has('unrelated-cache'));assert.ok(store.has('renalrounds:/other/:old'));assert.ok(!store.has('renalrounds:/drugs/:obsolete'));
online=false;
assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.5.0/);
assert.match(await (await first.navigate('https://example.org/drugs/index.html?x=1')).text(),/0.5.0/);
assert.equal(await first.navigate('https://example.org/other/'),undefined);
assert.equal(await first.navigate('https://source.example/label'),undefined);
await first.fire('message',{data:{type:'CACHE_STATUS'},source:{postMessage:x=>first.messages.push(x)}});assert.equal(first.messages[0].ready,true);
online=true;servedVersion='0.6.0';const second=worker('0.6.0','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.5.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.6.0/);
online=true;const mismatch=worker('0.7.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.6.0','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.6.0','404').fire('install'),/download failed/);
console.log('PASS: 621 unrelated records and all 27 previous PK summaries unchanged; 20 renal expansions, 26 historical PK additions, 16 PIRRT and four CVVHD additions; 668-row queue; actual service-worker install, offline reopen, explicit update activation, mismatched/404 rejection and per-path cache isolation. HTTPS/physical-phone integration remains to be checked after GitHub upload.');
