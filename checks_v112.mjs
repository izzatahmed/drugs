import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v111.json')),facts=JSON.parse(read('./book_facts_v112.json'));
const drug=id=>db.drugs.find(d=>d.id===id),changed=new Set(db.clinicalUpdates.changedIds);
assert.equal(db.version,'0.11.2');assert.equal(changed.size,60);assert.equal(facts.length,60);assert.equal(db.clinicalUpdates.newPKIds.length,58);assert.equal(db.clinicalUpdates.newPDIds.length,56);
for(const d of db.drugs){const old=base.drugs.find(x=>x.id===d.id);if(!changed.has(d.id))assert.deepEqual(d,old,d.id);else{assert.equal(old.entryType,'catalog');assert.equal(d.entryType,'renal');assert.equal(d.doseEvidence.publicationYear,2018);assert.equal(d.review.clinicalApprovedAt,null);assert.match(d.kidneyMetric,/GFR.*not stated as indexed/);for(const m of ['ckd','ihd','pd'])for(const t of d.modalities[m].tables)assert.match(t.indication,/5th ed.*2018/);assert.equal(d.modalities.crrt.tables.length,0);assert.equal(d.modalities.crrt.status,'specialist');assert.match(d.modalities.crrt.notes,/effluent.*downtime/);assert.deepEqual(d.modalities.sled,old.modalities.sled);for(const m of ['crrt','sled'])assert.deepEqual(d.pharmacokinetics.dialysability[m],old.pharmacokinetics.dialysability[m]);}if(old.entryType==='renal')assert.deepEqual(d,old,`${d.id}: existing renal profile changed`);if(old.pharmacokinetics.status==='source_summary')assert.deepEqual(d.pharmacokinetics,old.pharmacokinetics,`${d.id}: existing PK changed`);}
for(const source of base.sources)assert.deepEqual(db.sources.find(s=>s.id===source.id),source);
const sourceHash='f918bdcd99034cb93b5a24dbc7bf626bdb1fc831dcbb0d85e0f57ceecff83c20';
for(const f of facts){const d=drug(f.id),s=db.sources.find(s=>s.id==='rdh5-v112-'+f.id);assert.equal(s.suppliedDocument.sha256,sourceHash);assert.equal(s.suppliedDocument.pdfPage,f.pdfPage);assert.deepEqual(s.suppliedDocument.additionalPdfPages,f.additionalPdfPages);assert.deepEqual(d.handbookSource.additionalPdfPages,f.additionalPdfPages);assert.match(s.section,/2018.*2019.*Current local product/);if(f.id!=='verapamil')for(const k of ['halfLife','renalHalfLife','proteinBinding','volumeOfDistribution'])assert.equal(d.pharmacokinetics[k].value,f[k],`${f.id}/${k}`);if(d.modalities.ihd.tables.length){assert.match(d.modalities.ihd.tables[0].rows[0].context,/HD \(historical/);assert.match(d.modalities.ihd.tables[0].rows[1].context,/HDF \/ high-flux/);}if(d.modalities.pd.tables.length)assert.match(d.modalities.pd.notes,/not an intraperitoneal/);}
const rows=(id,m='ckd')=>JSON.stringify(drug(id).modalities[m].tables);
for(const id of ['hydroxychloroquine','mesalazine','cholecalciferol'])for(const m of ['ckd','ihd','pd']){assert.equal(drug(id).modalities[m].status,'specialist');assert.equal(drug(id).modalities[m].tables.length,0);}
assert.match(rows('acetazolamide'),/GFR <10.*Avoid/);assert.equal(drug('acetazolamide').modalities.ihd.status,'avoid');assert.equal(drug('acetazolamide').modalities.pd.status,'avoid');
assert.match(rows('flecainide'),/initial total 100 mg\/day.*50 mg twice daily.*IV: reduce by 50%/);assert.equal(drug('flecainide').pharmacokinetics.volumeOfDistribution.value,'8.31 L/kg');
assert.match(rows('nicardipine'),/1–5 mg\/hour.*0.5 mg\/hour every 30 min.*15 mg\/hour/);
assert.match(rows('midodrine','ihd'),/2.5 mg if weight <70 kg, 5 mg if >70 kg.*exactly 70 kg/);assert.match(drug('midodrine').considerations,/30 min/);
assert.match(rows('vildagliptin'),/50 mg orally once daily/);assert.match(drug('vildagliptin').pharmacokinetics.dialysability.ihd.value,/3% parent.*3–4 h/);
assert.match(drug('aminophylline').pharmacokinetics.dialysability.ihd.value,/Theophylline is removed/);assert.ok(drug('aminophylline').handbookSource.additionalPdfPages.includes(73));
assert.equal(drug('hydrocortisone').pharmacokinetics.dialysability.ihd.status,'source_difference');
assert.match(rows('domperidone'),/adult ≥35 kg.*maximum 30 mg\/day.*one week.*once or twice daily/);assert.ok(!/80 mg|12 weeks/.test(rows('domperidone')));assert.match(drug('domperidone').considerations,/Do not use with impaired cardiac conduction/);assert.ok(db.sources.some(s=>s.id==='mhra-domperidone-v112'));
assert.match(rows('calcium-acetate'),/elemental-calcium/);assert.equal(drug('calcium-acetate').pharmacokinetics.status,'not_reported');
for(const id of ['clopidogrel','hydroxychloroquine'])assert.equal(drug(id).pharmacokinetics.halfLife.value,null);assert.equal(drug('levothyroxine').pharmacokinetics.volumeOfDistribution.value,null);assert.match(drug('levothyroxine').pharmacokinetics.halfLife.value,/days/);assert.match(drug('adenosine').pharmacokinetics.halfLife.value,/seconds/);
assert.deepEqual(drug('minoxidil-systemic').routes,['Oral']);assert.match(rows('calcitriol'),/0.25 microgram/);assert.match(drug('acetylcysteine').considerations,/contrast-prophylaxis.*not imported/);
const queue=JSON.parse(read('./dist/CURATION_QUEUE.json'));assert.equal(queue.version,db.version);for(const q of queue.drugs){const d=drug(q.id);assert.equal(q.content,d.entryType);assert.deepEqual(q.modalities,Object.fromEntries(Object.entries(d.modalities).map(([k,m])=>[k,m.status])));}
const remaining=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));assert.equal(remaining.remaining.length,313);assert.deepEqual(remaining.remaining.map(d=>d.id),db.drugs.filter(d=>d.entryType!=='renal').map(d=>d.id));
const app=read('./dist/app.js'),workflow=read('./dist/workflow.js'),controls={'#route-filter':{value:'all'},'#content-filter':{value:'all'},'#setting-filter':{value:'all'},'#otc-filter':{checked:false}};
const ctx=vm.createContext({db,controls,performance});vm.runInContext(`const $=q=>controls[q];const norm=${app.match(/const norm = ([^\n]+);/)[1]};let category='all',view='all',favourites=new Set(),clinicalVersionCache;
${workflow.match(/function latestClinicalVersion\(\)\{[^\n]+/)[0]}
${workflow.slice(workflow.indexOf('function suggestions('),workflow.indexOf('function renderCompletion('))}
${app.slice(app.indexOf('function filterDrugs('),app.indexOf('function renderResults('))}
db.drugs.forEach(d=>{d.searchText=norm([d.name,...d.aliases,d.drugClass,d.category,...d.routes].join(' '));d.nameKeys=[d.name,...d.aliases].map(norm);});`,ctx);
const run=s=>vm.runInContext(s,ctx);for(const id of ['flecainide','vildagliptin','aminophylline','calcium-acetate','nicardipine'])assert.equal(run(`filterDrugs('${id}','all',false)[0].id`),id);controls['#content-filter'].value='pk';assert.equal(run("filterDrugs('','all',false).length"),157);controls['#content-filter'].value='all';run("view='new'");assert.equal(run("filterDrugs('','all',false).length"),60);run("view='all'");


assert.match(read('./app-shell.html'),/<a id="home-link"[^>]*href="\.\/"/);assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.11.2'),'Current footer version');
console.log('PASS: 60 dated handbook additions, 58 new partial PK profiles, source-page provenance, clinically consequential units and conflicts; all previous clinical records retained.');
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
online=true;servedVersion='0.11.2';const second=worker('0.11.2','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.11.2/);
online=true;const mismatch=worker('0.12.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.11.2','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.11.2','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.11.2 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');

for(const id of ['flecainide','nicardipine','palonosetron','aminophylline'])assert.deepEqual(drug(id).routes,['Oral','Parenteral']);
