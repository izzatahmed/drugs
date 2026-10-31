import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {performance} from 'node:perf_hooks';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json'));
const hash=x=>crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
const baseline=JSON.parse(read('./baseline_v05_fingerprints.json'));
const expanded=['losartan','valsartan','candesartan','irbesartan','telmisartan','bisoprolol','enalapril','ramipril','clonidine','hydralazine','methyldopa','indapamide'];
for(const d of db.drugs){if(!expanded.includes(d.id))assert.equal(hash(d),baseline.drugs[d.id],`${d.id}: unrelated clinical record changed`);assert.equal(hash(d.pharmacokinetics),baseline.pk[d.id],`${d.id}: PK changed unexpectedly`);}
for(const s of db.sources)if(baseline.sources[s.id])assert.equal(hash(s),baseline.sources[s.id],`${s.id}: existing source changed`);
assert.equal(hash(db.sharedGuidance),baseline.sharedGuidance);
assert.equal(db.referenceScope.updatedEntries,12);
assert.equal(db.referenceResources.length,9);
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
controls['#content-filter'].value='pk';assert.equal(run("filterDrugs('','all',false).length"),27);
controls['#content-filter'].value='all';controls['#setting-filter'].value='sled';assert.equal(run("filterDrugs('','all',false).length"),0);
controls['#setting-filter'].value='pd';assert.equal(run("filterDrugs('','all',false).length"),10);
controls['#setting-filter'].value='all';run("view='new'");assert.equal(run("filterDrugs('','all',false).length"),12);run("view='all'");
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
console.log('PASS: 656 unrelated clinical records and all 668 PK profiles unchanged; 12 source-based renal expansions; 668-row queue; actual service-worker install, offline reopen, explicit update activation, mismatched/404 rejection and per-path cache isolation. HTTPS/physical-phone integration remains to be checked after GitHub upload.');
