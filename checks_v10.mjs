import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {performance} from 'node:perf_hooks';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),baseline=JSON.parse(read('./baseline_v09.json'));
const drug=id=>db.drugs.find(d=>d.id===id),changed=new Set(db.clinicalUpdates.changedIds),text=id=>JSON.stringify(drug(id));
assert.equal(db.version,'0.10.0');assert.equal(changed.size,40);assert.equal(db.clinicalUpdates.newRenalIds.length,40);assert.equal(db.clinicalUpdates.newPKIds.length,3);
for(const d of db.drugs){const old=baseline.drugs.find(x=>x.id===d.id);assert.ok(old);if(!changed.has(d.id))assert.deepEqual(d,old,`${d.id}: unrelated record changed`);if(old.entryType==='renal')assert.deepEqual(d.modalities,old.modalities);if(old.pharmacokinetics.status==='source_summary')assert.deepEqual(d.pharmacokinetics,old.pharmacokinetics);}
for(const s of baseline.sources)assert.deepEqual(db.sources.find(x=>x.id===s.id),s);assert.deepEqual(db.sharedGuidance,baseline.sharedGuidance);assert.deepEqual(db.sourceConflicts,baseline.sourceConflicts);
assert.match(drug('perindopril').formulation,/erbumine/);assert.match(text('perindopril'),/exact 30 and 15/);assert.match(text('perindopril'),/non-dialysis-day dosing is not specified/);
assert.match(drug('fenofibrate').kidneyMetric,/1.73/);assert.match(text('fenofibrate'),/Start 48 mg/);assert.equal(drug('fenofibrate').modalities.pd.status,'avoid');
assert.match(text('pitavastatin'),/maximum 2 mg/);assert.match(text('simvastatin'),/Start 5 mg/);
assert.match(drug('mirabegron').kidneyMetric,/MDRD.*1.73/);assert.equal(drug('mirabegron').modalities.ihd.status,'avoid');
assert.match(drug('solifenacin').kidneyMetric,/CLcr.*1.73/);assert.match(drug('tamsulosin').kidneyMetric,/CLcr.*1.73/);
assert.match(drug('trospium').formulation,/immediate-release/);assert.match(text('trospium'),/20 mg PO once daily at bedtime/);assert.equal(drug('trospium').modalities.ihd.tables.length,0);
assert.match(drug('tolterodine').formulation,/extended-release/);assert.match(text('tolterodine'),/CrCl <10/);assert.equal(drug('oxybutynin').modalities.ckd.status,'insufficient_data');
assert.match(text('levocetirizine'),/once every 3–4 days/);assert.equal(drug('levocetirizine').modalities.ihd.status,'avoid');
assert.deepEqual(drug('tiotropium').routes,['Inhaled']);assert.match(drug('tiotropium').formulation,/DO NOT SWALLOW/);assert.match(text('tiotropium'),/CrCl <60/);
assert.match(text('hydroxyzine'),/TOTAL daily dose by 50%/);assert.match(text('sucralfate'),/aluminium/);
assert.equal(drug('doxazosin').pharmacokinetics.dialysability.ihd.status,'limited');assert.equal(drug('tamsulosin').pharmacokinetics.dialysability.ihd.status,'limited');assert.equal(drug('torsemide').pharmacokinetics.volumeOfDistribution.value,'12–15 L');
for(const id of changed){const d=drug(id);assert.equal(d.review.sourceCheckedAt,'2026-10-30');for(const key of ['crrt','sled'])assert.equal(d.modalities[key].tables.length,0);}
const remaining=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));assert.equal(remaining.remaining.length,410);assert.equal(remaining.notComplete,true);assert.deepEqual(remaining.remaining.map(d=>d.id),db.drugs.filter(d=>d.entryType!=='renal').map(d=>d.id));
assert.deepEqual(JSON.parse(read('./dist/REFERENCE_DIRECTORY.json')),db.referenceResources);
const queue=JSON.parse(read('./dist/CURATION_QUEUE.json'));assert.equal(queue.version,db.version);assert.equal(queue.drugs.length,668);for(const q of queue.drugs){const d=drug(q.id);assert.equal(q.content,d.entryType);assert.deepEqual(q.modalities,Object.fromEntries(Object.entries(d.modalities).map(([k,m])=>[k,m.status])));}
const app=read('./dist/app.js'),workflow=read('./dist/workflow.js'),controls={'#route-filter':{value:'all'},'#content-filter':{value:'all'},'#setting-filter':{value:'all'},'#otc-filter':{checked:false}};
const ctx=vm.createContext({db,controls,performance});vm.runInContext(`const $=q=>controls[q];const norm=${app.match(/const norm = ([^\n]+);/)[1]};let category='all',view='all',favourites=new Set(),clinicalVersionCache;
${workflow.match(/function latestClinicalVersion\(\)\{[^\n]+/)[0]}
${workflow.slice(workflow.indexOf('function suggestions('),workflow.indexOf('function renderCompletion('))}
${app.slice(app.indexOf('function filterDrugs('),app.indexOf('function renderResults('))}
db.drugs.forEach(d=>{d.searchText=norm([d.name,...d.aliases,d.drugClass,d.category,...d.routes].join(' '));d.nameKeys=[d.name,...d.aliases].map(norm);});`,ctx);
const run=s=>vm.runInContext(s,ctx);for(const id of ['perindopril','nifedipine','mirabegron','tiotropium','trospium'])assert.equal(run(`filterDrugs('${id}','all',false)[0].id`),id);assert.equal(run("filterDrugs('Norvasc','all',false)[0].id"),'amlodipine');assert.equal(run("latestClinicalVersion()"),'0.10.0');
controls['#content-filter'].value='pk';assert.equal(run("filterDrugs('','all',false).length"),69);controls['#content-filter'].value='all';run("view='new'");assert.equal(run("filterDrugs('','all',false).length"),40);run("view='all'");
const html=read('./dist/index.html');assert.ok(html.includes(read('./dist/interface.js')));assert.ok(html.includes(read('./dist/interface.css')));assert.match(read('./dist/sw.js'),/0.10.0/);
const docs=JSON.parse(html.match(/<script id="renalrounds-docs" type="application\/json">([\s\S]*?)<\/script>/)[1]);assert.equal(docs.plan,read('./dist/COMPLETION_PLAN.md'));
console.log('PASS: 40 new selected renal profiles, 3 PK additions; all v0.9 regimens/PK/unrelated records unchanged; source-specific thresholds, units, routes, dose maxima, 410-entry remaining-work export and actual search/filter functions verified.');

// Execute the actual service worker with deterministic network/cache contracts.
const store=new Map();
const caches={async keys(){return [...store.keys()];},async delete(n){return store.delete(n);},async open(n){if(!store.has(n))store.set(n,new Map());const map=store.get(n);return {async put(k,v){map.set(typeof k==='string'?k:k.url,v.clone());},async match(k){return map.get(typeof k==='string'?k:k.url)?.clone();}};}};
let online=true,servedVersion='0.9.0',httpStatus=200;
function worker(version='0.9.0',build='old'){
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
assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.9.0/);
assert.match(await (await first.navigate('https://example.org/drugs/index.html?x=1')).text(),/0.9.0/);
assert.equal(await first.navigate('https://example.org/other/'),undefined);
assert.equal(await first.navigate('https://source.example/label'),undefined);
await first.fire('message',{data:{type:'CACHE_STATUS'},source:{postMessage:x=>first.messages.push(x)}});assert.equal(first.messages[0].ready,true);
online=true;servedVersion='0.10.0';const second=worker('0.10.0','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.9.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.10.0/);
online=true;const mismatch=worker('0.11.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.10.0','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.10.0','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.10 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
