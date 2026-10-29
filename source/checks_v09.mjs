import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {performance} from 'node:perf_hooks';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),baseline=JSON.parse(read('./baseline_v08.json'));
const drug=id=>db.drugs.find(d=>d.id===id),changed=new Set(db.clinicalUpdates.changedIds);
assert.equal(changed.size,85);assert.equal(db.clinicalUpdates.newRenalIds.length,85);assert.equal(db.clinicalUpdates.newPKIds.length,13);
for(const d of db.drugs){
 const old=baseline.drugs.find(x=>x.id===d.id);assert.ok(old);
 if(!changed.has(d.id))assert.deepEqual(d,old,`${d.id}: unrelated clinical record changed`);
 if(old.entryType==='renal')assert.deepEqual(d.modalities,old.modalities,`${d.id}: prior regimen changed`);
 if(old.pharmacokinetics.status==='source_summary')assert.deepEqual(d.pharmacokinetics,old.pharmacokinetics,`${d.id}: prior PK changed`);
}
for(const s of baseline.sources)assert.deepEqual(db.sources.find(x=>x.id===s.id),s);
assert.deepEqual(db.sharedGuidance,baseline.sharedGuidance);
const text=id=>JSON.stringify(drug(id));
assert.match(text('minocycline'),/200 mg per 24 h/);
assert.match(text('posaconazole'),/eGFR <50/);assert.match(drug('posaconazole').formulation,/IV/);
assert.match(text('aztreonam-avibactam'),/2.67 g/);assert.match(text('aztreonam-avibactam'),/start-to-start/);assert.match(text('aztreonam-avibactam'),/metronidazole/);
assert.match(text('ceftobiprole'),/667 mg prodrug salt equals 500 mg/);assert.match(text('ceftobiprole'),/SAB regimen/);
assert.match(drug('meropenem-vaborbactam').kidneyMetric,/MDRD.*1.73/);
assert.equal(drug('cefepime-enmetazobactam').modalities.ckd.tables.length,0);
assert.match(text('lamivudine'),/50 mg first dose, then 25 mg/);
assert.match(text('emtricitabine'),/NIH/);
assert.match(text('tenofovir-disoproxil'),/once weekly after HD/);
assert.match(text('denosumab'),/weekly/);assert.match(text('denosumab'),/CKD-MBD/);
assert.match(text('warfarin'),/monitor INR more often/);
assert.match(text('venlafaxine'),/TOTAL daily/);
assert.match(text('desvenlafaxine'),/Maximum 25 mg/);
assert.match(text('paliperidone'),/maximum 3 mg/);assert.match(text('paliperidone'),/Long-acting injectable thresholds differ/);
assert.match(text('lithium'),/Cockcroft/);assert.equal(drug('lithium').modalities.ihd.tables.length,0);
assert.match(drug('haloperidol').formulation,/decanoate depot only/);assert.deepEqual(drug('haloperidol').routes,['Parenteral']);assert.deepEqual(drug('aripiprazole').routes,['Oral']);
assert.equal(db.drugs.filter(d=>d.category==='Psychiatry'&&d.entryType==='renal').length,24);
assert.equal(drug('vancomycin').modalities.ihd.tables.length,0);
assert.equal(drug('mirtazapine').pharmacokinetics.volumeOfDistribution.value,'107 L');
assert.equal(drug('ibandronate').pharmacokinetics.volumeOfDistribution.value,'90 L');
for(const id of db.clinicalUpdates.newPKIds){const p=drug(id).pharmacokinetics;assert.equal(p.historical,true);assert.match(p.evidenceDate,/2018/);assert.equal(p.dialysability.crrt.value,null);assert.equal(p.dialysability.sled.value,null);}
const inventory=JSON.parse(read('./source_inventory_v07.json'));
for(const s of db.sources.filter(s=>s.suppliedDocument)){const f=inventory.find(f=>f.fileName===s.suppliedDocument.fileName);assert.equal(s.suppliedDocument.sha256,f.sha256);for(const page of [s.suppliedDocument.pdfPage,...s.suppliedDocument.additionalPdfPages||[]])assert.ok(page>=1&&page<=f.pages);}
const remaining=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));assert.equal(remaining.notComplete,true);assert.equal(remaining.remaining.length,450);assert.deepEqual(remaining.remaining.map(x=>x.id),db.drugs.filter(d=>d.entryType!=='renal').map(d=>d.id));
const queue=JSON.parse(read('./dist/CURATION_QUEUE.json'));assert.equal(queue.version,db.version);assert.equal(queue.drugs.length,668);
for(const q of queue.drugs){const d=drug(q.id);assert.equal(q.content,d.entryType);assert.equal(q.renalDoseSourceCheckedAt,d.review.sourceCheckedAt);assert.deepEqual(q.modalities,Object.fromEntries(Object.entries(d.modalities).map(([k,v])=>[k,v.status])));}
const app=read('./dist/app.js'),workflow=read('./dist/workflow.js');
const controls={'#route-filter':{value:'all'},'#content-filter':{value:'all'},'#setting-filter':{value:'all'},'#otc-filter':{checked:false}};
const ctx=vm.createContext({db,controls,performance});
vm.runInContext(`const $=q=>controls[q];const norm=${app.match(/const norm = ([^\n]+);/)[1]};let category='all',view='all',favourites=new Set(),clinicalVersionCache;
${workflow.match(/function latestClinicalVersion\(\)\{[^\n]+/)[0]}
${workflow.slice(workflow.indexOf('function suggestions('),workflow.indexOf('function renderCompletion('))}
${app.slice(app.indexOf('function filterDrugs('),app.indexOf('function renderResults('))}
db.drugs.forEach(d=>{d.searchText=norm([d.name,...d.aliases,d.drugClass,d.category,...d.routes].join(' '));d.nameKeys=[d.name,...d.aliases].map(norm);});`,ctx);
const run=s=>vm.runInContext(s,ctx);
for(const id of ['captopril','amlodipine','lithium','aztreonam-avibactam','nebivolol'])assert.equal(run(`filterDrugs('${id}','all',false)[0].id`),id);
assert.equal(run("filterDrugs('Capoten','all',false)[0].id"),'captopril');
assert.equal(run("latestClinicalVersion()"),'0.9.0');
controls['#content-filter'].value='catalog';assert.ok(run("filterDrugs('','all',false).every(d=>d.entryType==='catalog')"));
controls['#content-filter'].value='all';
const html=read('./dist/index.html'),docs=JSON.parse(html.match(/<script id="renalrounds-docs" type="application\/json">([\s\S]*?)<\/script>/)[1]);assert.equal(docs.plan,read('./dist/COMPLETION_PLAN.md'));
for(const f of ['CHANGELOG.md','COMPLETION_PLAN.md','EDITORIAL_GUIDE.md'])assert.match(read('./dist/'+f),/v0.9.0/);
assert.match(read('./dist/sw.js'),/0.9.0/);
console.log('PASS: 85 new renal profiles, 13 historical PK profiles; v0.8 clinical baselines retained; high-consequence source distinctions, remaining-work exports, source pages, filters and standalone documents verified. Clinical approval pending.');

// Execute the actual service worker with deterministic network/cache contracts.
const store=new Map();
const caches={async keys(){return [...store.keys()];},async delete(n){return store.delete(n);},async open(n){if(!store.has(n))store.set(n,new Map());const map=store.get(n);return {async put(k,v){map.set(typeof k==='string'?k:k.url,v.clone());},async match(k){return map.get(typeof k==='string'?k:k.url)?.clone();}};}};
let online=true,servedVersion='0.8.0',httpStatus=200;
function worker(version='0.8.0',build='old'){
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
assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.8.0/);
assert.match(await (await first.navigate('https://example.org/drugs/index.html?x=1')).text(),/0.8.0/);
assert.equal(await first.navigate('https://example.org/other/'),undefined);
assert.equal(await first.navigate('https://source.example/label'),undefined);
await first.fire('message',{data:{type:'CACHE_STATUS'},source:{postMessage:x=>first.messages.push(x)}});assert.equal(first.messages[0].ready,true);
online=true;servedVersion='0.9.0';const second=worker('0.9.0','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.8.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.9.0/);
online=true;const mismatch=worker('0.10.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.9.0','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.9.0','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.9 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
