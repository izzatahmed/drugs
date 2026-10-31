import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v113.json')),meta=JSON.parse(read('./label_meta_v120.json'));
assert.equal(db.version,'0.12.0');assert.equal(base.version,'0.11.3');
const changed=new Set(db.clinicalUpdates.changedIds);assert.equal(changed.size,61);assert.deepEqual([...changed].sort(),Object.keys(meta).sort());
const src=new Map(db.sources.map(s=>[s.id,s]));
// 1. No dose table or modality anywhere cites the handbook.
for(const d of db.drugs)for(const [k,m] of Object.entries(d.modalities))assert.ok(!m.sourceIds.some(i=>i.startsWith('rdh5')),`${d.id}/${k} still cites the handbook`);
assert.ok(!db.drugs.some(d=>d.handbookSource||d.doseEvidence),'Handbook dose metadata removed');
// 2. Each rebuilt entry cites its retrieved label, with traceable identifiers.
for(const id of changed){const d=db.drugs.find(x=>x.id===id),m=meta[id];
 const own=d.sourceIds.filter(s=>s.startsWith('us120-')||s.startsWith('uk120-'));assert.ok(own.length,id);
 for(const s of own){const r=src.get(s);assert.ok(r,s);
  if(m.kind==='US'){assert.equal(r.url,`https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=${m.setid}`);assert.equal(r.label.setid,m.setid);assert.match(r.label.effective,/^\d{4}-\d\d-\d\d$/);}
  else assert.match(r.url,/^https:\/\/www\.medicines\.org\.uk\/emc\/product\/\d+\/smpc$/);}
 assert.match(d.jurisdiction,/JFDA/);assert.equal(d.updatedInVersion,'0.12.0');assert.equal(d.review.clinicalApprovedAt,null);
 for(const [k,mo] of Object.entries(d.modalities)){if(mo.status==='not_curated')assert.equal(mo.tables.length,0);else assert.ok(mo.sourceIds.some(s=>own.includes(s)),`${id}/${k} unsourced`);}
 assert.equal(d.modalities.sled.status,'not_curated');
 assert.deepEqual(d.pharmacokinetics,base.drugs.find(x=>x.id===id).pharmacokinetics,`${id} PK unchanged this release`);}
// 3. Every other entry is unchanged.
for(const d of db.drugs)if(!changed.has(d.id))assert.deepEqual(d,base.drugs.find(x=>x.id===d.id),d.id);
assert.deepEqual(db.coverage,base.coverage);assert.deepEqual(db.pharmacokineticCoverage,base.pharmacokineticCoverage);
// 4. Spot values taken from the labels.
const rows=(id,m='ckd')=>JSON.stringify(db.drugs.find(x=>x.id===id).modalities[m].tables);
assert.match(rows('flecainide'),/CrCl ≤35 mL\/min\/1\.73 m².*100 mg once daily \(or 50 mg twice daily\)/);assert.match(rows('flecainide'),/100 mg every 12 hours/);
assert.match(rows('telavancin'),/"30–50".*7\.5 mg\/kg every 24 hours.*"10–<30".*10 mg\/kg every 48 hours/);assert.match(db.drugs.find(x=>x.id==='telavancin').kidneyMetric,/ideal body weight/);
assert.match(rows('repaglinide'),/CrCl 20–40.*0\.5 mg before each meal/);assert.match(rows('vildagliptin'),/50 mg once daily/);
assert.match(rows('calcium-acetate','ihd'),/2 capsules with each meal/);assert.match(rows('paricalcitol','ihd'),/÷ 80/);
assert.equal(db.drugs.find(x=>x.id==='bisacodyl').modalities.ckd.status,'insufficient_data');
// 5. Source line in the app.
const app=read('./dist/app.js');assert.match(app,/jurisdictionStrip\(m\.sourceIds\)/);assert.match(app,/Jordan: check the JFDA-approved leaflet/);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.12.0'));
console.log('PASS: 61 dose entries rebuilt from current labels (US DailyMed set IDs / UK emc product IDs); no handbook citation in any dose table; all other entries unchanged; label spot values; source-country line.');
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
online=true;servedVersion='0.12.0';const second=worker('0.12.0','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.12.0/);
online=true;const mismatch=worker('0.13.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.12.0','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.12.0','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.12.0 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
