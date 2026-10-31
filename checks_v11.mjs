import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {performance} from 'node:perf_hooks';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),baseline=JSON.parse(read('./baseline_v10.json'));
const drug=id=>db.drugs.find(d=>d.id===id),changed=new Set(db.clinicalUpdates.changedIds);
assert.equal(db.version,'0.11.0');assert.equal(changed.size,32);assert.equal(db.clinicalUpdates.newRenalIds.length,2);assert.equal(db.clinicalUpdates.newPKIds.length,30);
for(const d of db.drugs){const old=baseline.drugs.find(x=>x.id===d.id);assert.ok(old);if(!changed.has(d.id))assert.deepEqual(d,old,`${d.id}: unrelated record changed`);if(old.entryType==='renal')assert.deepEqual(d.modalities,old.modalities);if(old.pharmacokinetics.status==='source_summary')assert.deepEqual(d.pharmacokinetics,old.pharmacokinetics);}
for(const s of baseline.sources)assert.deepEqual(db.sources.find(x=>x.id===s.id),s);assert.deepEqual(db.sharedGuidance,baseline.sharedGuidance);
for(const id of db.clinicalUpdates.newPKIds){const d=drug(id),p=d.pharmacokinetics;assert.equal(d.entryType,'catalog');assert.equal(d.review.sourceCheckedAt,null);assert.equal(p.historical,true);assert.match(p.evidenceDate,/2018/);for(const m of Object.values(d.modalities))assert.equal(m.tables.length,0);for(const m of Object.values(p.dialysability)){assert.equal(m.value,null);assert.equal(m.status,'not_curated');}assert.match(p.notes,/withheld pending current-source verification/);}
assert.equal(drug('valproate').pharmacokinetics.volumeOfDistribution.value,'0.1–0.4 L/kg');assert.equal(drug('memantine').pharmacokinetics.renalHalfLife.value,'117–156 h');assert.equal(drug('brivaracetam').pharmacokinetics.renalHalfLife.value,'9.8 h in source table');assert.equal(drug('oxycodone').pharmacokinetics.volumeOfDistribution.value,'1.2–6.31 L/kg');
assert.equal(drug('pramipexole').pharmacokinetics.volumeOfDistribution.value,'400–500 L');assert.equal(drug('sumatriptan').pharmacokinetics.volumeOfDistribution.value,'170 L');assert.match(drug('oxcarbazepine').pharmacokinetics.proteinBinding.value,/metabolite/);
assert.equal(drug('tramadol-extended-release').pharmacokinetics.status,'not_curated');assert.equal(drug('paracetamol-iv').pharmacokinetics.status,'not_curated','Do not copy unmatched generic kinetics to the IV-specific entry');
assert.equal(drug('omadacycline').modalities.ckd.tables[0].rows.length,1);assert.equal(drug('omadacycline').modalities.ihd.tables.length,0);assert.equal(drug('telavancin').modalities.ckd.tables.length,0);assert.equal(drug('telavancin').modalities.ckd.status,'specialist');assert.ok(db.sourceConflicts.some(c=>c.drug==='telavancin'));assert.match(db.researchLimitations.onlinePrimarySourceLookup,/Unavailable/);
const inventory=JSON.parse(read('./source_inventory_v07.json'));for(const s of db.sources.filter(s=>s.suppliedDocument)){const f=inventory.find(f=>f.fileName===s.suppliedDocument.fileName);assert.equal(s.suppliedDocument.sha256,f.sha256);assert.ok(s.suppliedDocument.pdfPage>0&&s.suppliedDocument.pdfPage<=f.pages);}
assert.deepEqual(JSON.parse(read('./dist/REFERENCE_DIRECTORY.json')),db.referenceResources);
const remaining=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));assert.equal(remaining.remaining.length,408);assert.equal(remaining.notComplete,true);assert.deepEqual(remaining.remaining.map(d=>d.id),db.drugs.filter(d=>d.entryType!=='renal').map(d=>d.id));
const queue=JSON.parse(read('./dist/CURATION_QUEUE.json'));assert.equal(queue.version,db.version);for(const q of queue.drugs){const d=drug(q.id);assert.equal(q.content,d.entryType);assert.equal(q.pkSourceCheckedAt,d.pharmacokinetics.sourceCheckedAt);assert.equal(q.renalDoseSourceCheckedAt,d.review.sourceCheckedAt);assert.deepEqual(q.modalities,Object.fromEntries(Object.entries(d.modalities).map(([k,m])=>[k,m.status])));}
const app=read('./dist/app.js'),workflow=read('./dist/workflow.js'),controls={'#route-filter':{value:'all'},'#content-filter':{value:'all'},'#setting-filter':{value:'all'},'#otc-filter':{checked:false}};
const ctx=vm.createContext({db,controls,performance});vm.runInContext(`const $=q=>controls[q];const norm=${app.match(/const norm = ([^\n]+);/)[1]};let category='all',view='all',favourites=new Set(),clinicalVersionCache;
${workflow.match(/function latestClinicalVersion\(\)\{[^\n]+/)[0]}
${workflow.slice(workflow.indexOf('function suggestions('),workflow.indexOf('function renderCompletion('))}
${app.slice(app.indexOf('function filterDrugs('),app.indexOf('function renderResults('))}
db.drugs.forEach(d=>{d.searchText=norm([d.name,...d.aliases,d.drugClass,d.category,...d.routes].join(' '));d.nameKeys=[d.name,...d.aliases].map(norm);});`,ctx);
const run=s=>vm.runInContext(s,ctx);for(const id of ['morphine','phenytoin','omadacycline','telavancin','memantine'])assert.equal(run(`filterDrugs('${id}','all',false)[0].id`),id);controls['#content-filter'].value='pk';assert.equal(run("filterDrugs('','all',false).length"),99);controls['#content-filter'].value='all';run("view='new'");assert.equal(run("filterDrugs('','all',false).length"),32);run("view='all'");
const html=read('./dist/index.html'),docs=JSON.parse(html.match(/<script id="renalrounds-docs" type="application\/json">([\s\S]*?)<\/script>/)[1]);assert.equal(docs.plan,read('./dist/COMPLETION_PLAN.md'));assert.match(read('./dist/sw.js'),/0.11.0/);assert.ok(!/CLINICAL APPROVAL PENDING/.test(app.slice(app.indexOf("$('#monograph').innerHTML=`<div class=\"mono-head\""),app.indexOf('<div class="mode-tabs"'))),'Approval status belongs below findings');
console.log('PASS: v0.10 regimens/PK/unrelated records retained; 30 historical PK panels with explicit uncurated RRT/dose fields, two bounded institutional renal profiles, source page/hash checks, reference-number/unit distinctions, queue consistency, search and compact-status structure verified.');

// Execute the actual service worker with deterministic network/cache contracts.
const store=new Map();
const caches={async keys(){return [...store.keys()];},async delete(n){return store.delete(n);},async open(n){if(!store.has(n))store.set(n,new Map());const map=store.get(n);return {async put(k,v){map.set(typeof k==='string'?k:k.url,v.clone());},async match(k){return map.get(typeof k==='string'?k:k.url)?.clone();}};}};
let online=true,servedVersion='0.10.0',httpStatus=200;
function worker(version='0.10.0',build='old'){
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
assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
assert.match(await (await first.navigate('https://example.org/drugs/index.html?x=1')).text(),/0.10.0/);
assert.equal(await first.navigate('https://example.org/other/'),undefined);
assert.equal(await first.navigate('https://source.example/label'),undefined);
await first.fire('message',{data:{type:'CACHE_STATUS'},source:{postMessage:x=>first.messages.push(x)}});assert.equal(first.messages[0].ready,true);
online=true;servedVersion='0.11.0';const second=worker('0.11.0','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.11.0/);
online=true;const mismatch=worker('0.12.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.11.0','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.11.0','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.11 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
