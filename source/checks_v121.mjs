import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v120.json')),lab=JSON.parse(read('./label_extract_v121.json'));
assert.equal(db.version,'0.12.1');assert.equal(base.version,'0.12.0');
const drug=id=>db.drugs.find(d=>d.id===id),changed=new Set(db.clinicalUpdates.changedIds);
const rows=(id,m)=>JSON.stringify(drug(id).modalities[m].tables);
// ISPD 2022 Table 5 values (verified against the table image reproduced by Northwestern Medicine).
const ip=(id)=>drug(id).modalities.pd.tables.find(t=>t.indication.includes('ISPD 2022'));
for(const [id,re] of [['vancomycin',/15–30 mg\/kg IP every 5–7 days.*15 mg\/kg IP every 4 days.*20–25 mg\/kg, then 25 mg\/L/],['gentamicin',/0\.6 mg\/kg IP daily.*Not advised/],['amikacin',/2 mg\/kg IP daily.*Not advised/],['tobramycin',/0\.6 mg\/kg daily.*Not advised/],['cefazolin',/15 mg\/kg daily \(long dwell\); 20 mg\/kg daily \(short dwell\).*500 mg\/L, then 125 mg\/L/],['ceftazidime',/1,000–1,500 mg daily/],['cefepime',/1,000 mg daily/],['meropenem',/500 mg daily \(long dwell, APD\); 1,000 mg daily \(short dwell, CAPD\).*125 mg\/L/],['teicoplanin',/15 mg\/kg every 5 days.*400 mg per bag, then 20 mg\/L/],['daptomycin',/300 mg daily.*100 mg\/L, then 20 mg\/L/],['aztreonam',/2 g daily.*500 mg\/L, then 250 mg\/L/],['fluconazole',/150–200 mg every 24–48 hours/]]){const t=ip(id);assert.ok(t,id);assert.match(JSON.stringify(t.rows),re,id);assert.ok(drug(id).modalities.pd.sourceIds.includes('ispd2022'));}
assert.equal(db.drugs.filter(d=>d.modalities.pd.tables.some(t=>t.indication.includes('ISPD 2022'))).length,26);
// Vancomycin HD (UNMC nephrology protocol) and label anephric dose; aminoglycoside label/protocol numbers.
assert.match(rows('vancomycin','ihd'),/20 mg\/kg IV once \(minimum 1,000 mg, maximum 2,000 mg\).*750 mg IV after each dialysis/);
assert.match(rows('vancomycin','ckd'),/1\.9 mg\/kg every 24 hours/);
assert.match(rows('gentamicin','ihd'),/1–1\.7 mg\/kg/);assert.match(rows('gentamicin','ckd'),/serum creatinine in mg\/dL × 8/);
assert.match(rows('amikacin','ckd'),/7\.5 mg\/kg every 48 h/);assert.match(rows('amikacin','ihd'),/10 mg\/kg once, then 5 mg\/kg after each dialysis/);
assert.match(rows('tobramycin','ckd'),/serum creatinine × 6/);
// Vonoprazan from its label.
assert.match(rows('vonoprazan','ckd'),/"eGFR <30","dose":"10 mg once daily".*"eGFR <30","dose":"Not recommended"/);assert.equal(drug('vonoprazan').drugClass,'Potassium-competitive acid blocker (P-CAB)');
// Pregnancy/lactation excerpts are verbatim label text and cite a source the entry already uses.
let n=0;for(const d of db.drugs){const p=d.pregnancyLactation;if(!p)continue;n++;const e=lab[d.id];assert.ok(e,d.id);
 for(const k of ['pregnancy','lactation'])if(p[k])assert.ok(e.sourceText.includes(p[k].replace(/ …$/,'').replace(/\.$/,'').slice(0,120)),`${d.id} ${k} not verbatim`);
 assert.ok(d.sourceIds.includes(p.sourceIds[0]),d.id);if(p.fdaLetterCategory)assert.match(p.fdaLetterCategory,/^[ABCDX]$/);}
assert.ok(n>=60,'pregnancy excerpts present');
// Everything else unchanged.
for(const d of db.drugs){if(changed.has(d.id))continue;const o=base.drugs.find(x=>x.id===d.id);const {pregnancyLactation,...rest}=d;assert.deepEqual(rest,o,d.id);}
const app=read('./dist/app.js');assert.match(app,/function pregnancyPanel/);assert.ok(!/mono-back/.test(app));assert.match(read('./dist/interface.js'),/is-hidden/);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.12.1'));
console.log(`PASS: ISPD 2022 IP doses on 26 antibiotics; vancomycin/aminoglycoside numbers; vonoprazan; ${n} verbatim pregnancy/lactation excerpts; other entries unchanged.`);
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
online=true;servedVersion='0.12.1';const second=worker('0.12.1','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.12.1/);
online=true;const mismatch=worker('0.13.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.12.1','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.12.1','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.12.1 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
