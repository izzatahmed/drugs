import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v11.json')),meta=JSON.parse(read('./label_sources_v111.json'));
const drug=id=>db.drugs.find(d=>d.id===id),changes=db.clinicalUpdates,changed=new Set(changes.changedIds);
assert.equal(db.version,'0.11.1');assert.equal(changed.size,52);assert.equal(changes.newRenalIds.length,35);assert.equal(changes.newPDIds.length,17);assert.equal(changes.updatedIHDRemovalIds.length,8);
for(const d of db.drugs){const old=base.drugs.find(x=>x.id===d.id);if(!changed.has(d.id))assert.deepEqual(d,old,d.id);for(const [m,v] of Object.entries(old.modalities)){if(v.tables.length)assert.deepEqual(d.modalities[m],v,`${d.id}/${m}: existing populated regimen changed`);}if(old.pharmacokinetics.status==='source_summary'){for(const k of ['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'])assert.deepEqual(d.pharmacokinetics[k],old.pharmacokinetics[k]);for(const k of ['pd','crrt','sled'])assert.deepEqual(d.pharmacokinetics.dialysability[k],old.pharmacokinetics.dialysability[k]);}}
for(const source of base.sources)assert.deepEqual(db.sources.find(s=>s.id===source.id),source);
for(const m of Object.values(meta)){const s=db.sources.find(s=>s.id==='spl111-'+m.drugId);assert.ok(s);assert.match(s.xmlSha256,/^[0-9a-f]{64}$/);assert.equal(s.xmlSha256,m.xmlSha256);assert.equal(s.labelVersion,m.spl_version);assert.equal(s.labelPublishedDate,m.published_date);assert.ok(s.url.endsWith(m.setid));assert.ok(s.retrievalUrl.endsWith(m.setid+'.xml'));}
for(const id of changes.newPDIds){const d=drug(id);assert.equal(d.modalities.pd.status,'summarized');assert.ok(d.modalities.pd.tables.length);assert.equal(base.drugs.find(d=>d.id===id).modalities.pd.tables.length,0);assert.match(d.modalities.pd.sourceIds[0],/^nm111-/);assert.ok(db.sources.find(s=>s.id===d.modalities.pd.sourceIds[0]).suppliedDocument.pdfPage);}
assert.match(drug('oxcarbazepine').modalities.ckd.tables[0].rows[0].dose,/total 300 mg\/day.*150 mg twice/);
assert.match(drug('lacosamide').modalities.ckd.tables[0].rows[1].dose,/300 mg\/day/);assert.match(drug('lacosamide').modalities.ihd.tables[0].rows[1].dose,/up to 50%/);
assert.match(drug('topiramate').kidneyMetric,/1.73/);assert.match(drug('topiramate').modalities.ckd.tables[0].rows[0].context,/<70/);assert.equal(drug('topiramate').modalities.ihd.tables.length,0);
assert.match(drug('hydromorphone').modalities.ckd.tables[0].rows[0].dose,/25–50%/);assert.match(drug('hydromorphone').formulation,/Oral immediate/);
assert.match(drug('amantadine').modalities.ihd.tables[0].rows[0].dose,/200 mg every 7 days/);assert.match(drug('amantadine').formulation,/immediate/);
assert.match(drug('ropinirole').modalities.ihd.tables[0].rows[0].dose,/18 mg\/day/);assert.match(drug('ropinirole').modalities.ihd.tables[1].rows[0].dose,/3 mg\/day/);
assert.match(drug('pramipexole').modalities.ckd.tables[0].rows[1].dose,/0.125 mg twice.*0.75 mg three/);assert.equal(drug('pramipexole').modalities.ihd.status,'insufficient_data');
assert.equal(drug('brivaracetam').modalities.ihd.status,'avoid');assert.equal(drug('brivaracetam').modalities.pd.status,'avoid');assert.equal(drug('brivaracetam').modalities.ihd.tables.length,0);
for(const id of ['cefixime','lorazepam','buprenorphine'])assert.equal(drug(id).modalities.ckd.tables.length,0);
assert.match(drug('memantine').modalities.ckd.tables[0].rows[1].dose,/5 mg.*twice daily/);assert.match(drug('memantine').formulation,/2 mg\/mL/);
assert.match(drug('entecavir').modalities.ckd.tables[0].rows[3].dose,/0.05 mg.*0.5 mg every 7/);assert.match(drug('entecavir').modalities.pd.tables[1].rows[0].dose,/0.1 mg.*1 mg every 7/);assert.match(drug('entecavir').modalities.pd.tables[0].indication,/CAPD/);
assert.match(drug('sulbactam-durlobactam').modalities.ckd.tables[0].rows[4].dose,/0, 12 and 24 h.*every 24/);assert.match(drug('sulbactam-durlobactam').modalities.ihd.notes,/after/);
assert.match(drug('imipenem-cilastatin-relebactam').modalities.ihd.tables[0].rows[0].dose,/0.5 g.*200\/200\/100.*every 6 h/);assert.equal(drug('imipenem-cilastatin-relebactam').modalities.pd.status,'insufficient_data');
assert.match(drug('delafloxacin').modalities.ckd.tables[0].rows[2].dose,/200 mg IV every 12 h/);assert.equal(drug('delafloxacin').modalities.ihd.status,'avoid');
assert.match(drug('trimethoprim').modalities.ckd.tables[0].rows[1].dose,/50 mg PO every 12 h/);assert.match(drug('trimethoprim').considerations,/alone, not TMP\/SMX/);
assert.match(drug('phenobarbital').considerations,/unapproved/);assert.match(drug('molnupiravir').considerations,/EUA.*not full FDA approval/);
assert.match(drug('cefuroxime').modalities.pd.notes,/oral.*IV/);assert.match(drug('cefazolin').modalities.pd.notes,/not.*intraperitoneally/);
assert.match(drug('fluconazole').modalities.pd.tables[0].rows[0].dose,/load.*200 mg.*every 24 h/);assert.match(drug('piperacillin-tazobactam').modalities.pd.tables[0].rows[0].dose,/4.5 g.*every 12 h.*over 4 h/);
const queue=JSON.parse(read('./dist/CURATION_QUEUE.json'));assert.equal(queue.version,db.version);for(const q of queue.drugs){const d=drug(q.id);assert.equal(q.content,d.entryType);assert.deepEqual(q.modalities,Object.fromEntries(Object.entries(d.modalities).map(([k,m])=>[k,m.status])));}
const remaining=JSON.parse(read('./dist/REMAINING_MEDICATIONS.json'));assert.equal(remaining.remaining.length,373);assert.deepEqual(remaining.remaining.map(d=>d.id),db.drugs.filter(d=>d.entryType!=='renal').map(d=>d.id));
const app=read('./dist/app.js'),workflow=read('./dist/workflow.js'),controls={'#route-filter':{value:'all'},'#content-filter':{value:'all'},'#setting-filter':{value:'all'},'#otc-filter':{checked:false}};
const ctx=vm.createContext({db,controls,performance});vm.runInContext(`const $=q=>controls[q];const norm=${app.match(/const norm = ([^\n]+);/)[1]};let category='all',view='all',favourites=new Set(),clinicalVersionCache;
${workflow.match(/function latestClinicalVersion\(\)\{[^\n]+/)[0]}
${workflow.slice(workflow.indexOf('function suggestions('),workflow.indexOf('function renderCompletion('))}
${app.slice(app.indexOf('function filterDrugs('),app.indexOf('function renderResults('))}
db.drugs.forEach(d=>{d.searchText=norm([d.name,...d.aliases,d.drugClass,d.category,...d.routes].join(' '));d.nameKeys=[d.name,...d.aliases].map(norm);});`,ctx);
const run=s=>vm.runInContext(s,ctx);for(const id of ['entecavir','ropinirole','sulbactam-durlobactam','lacosamide','memantine'])assert.equal(run(`filterDrugs('${id}','all',false)[0].id`),id);controls['#content-filter'].value='pk';assert.equal(run("filterDrugs('','all',false).length"),99);controls['#content-filter'].value='all';run("view='new'");assert.equal(run("filterDrugs('','all',false).length"),52);run("view='all'");

const shell=read('./app-shell.html');assert.match(shell,/program-title.*RenalRounds.*v0.11.1/);assert.ok(shell.indexOf('reader-toolbar')<shell.indexOf('program-title'));assert.ok(shell.indexOf('program-title')<shell.indexOf('search-row'));
const html=read('./dist/index.html');assert.match(html,/RenalRounds version 0.11.1/);assert.match(read('./dist/sw.js'),/0.11.1/);
console.log('PASS: 35 selected SPL renal profiles, 17 explicit systemic PD additions, eight IHD fields, all prior populated regimens and PK core fields retained; product/indication/units/combination boundaries and honest gaps verified.');

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
online=true;servedVersion='0.11.1';const second=worker('0.11.1','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.11.1/);
online=true;const mismatch=worker('0.12.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.11.1','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.11.1','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.11.1 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
