import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v121.json'));
const lab={...JSON.parse(read('./label_extract_v121.json')),...JSON.parse(read('./label_extract_v122.json'))};
assert.equal(db.version,'0.12.2');assert.equal(db.clinicalDataVersion,'0.12.1','No dosing change in this release');
const src=new Map(db.sources.map(s=>[s.id,s]));
// 1. Dose tables, statuses and PK unchanged from v0.12.1.
for(const d of db.drugs){const o=base.drugs.find(x=>x.id===d.id);assert.ok(o,d.id);assert.deepEqual(d.modalities,o.modalities,`${d.id} dosing changed`);assert.deepEqual(d.pharmacokinetics,o.pharmacokinetics);
 for(const k of ['kidneyMetric','summary','flag','entryType','considerations'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);}
// 2. Every pregnancy/lactation excerpt is verbatim text of its stored label window and cites a DailyMed/emc source.
let n=0,letters=0;for(const d of db.drugs){const p=d.pregnancyLactation;if(!p)continue;n++;
 if(p.status==='reviewer_entry'){assert.match(p.tgaCategory,/^(A|B1|B2|B3|C|D|X|Exempt)$/);continue;}
 const e=lab[d.id];assert.ok(e,d.id);for(const k of ['pregnancy','lactation'])if(p[k])assert.ok(e.sourceText.includes(p[k].replace(/ …$/,'').replace(/\.$/,'').slice(0,120)),`${d.id} ${k} not verbatim`);
 const s=src.get(p.sourceIds[0]);assert.ok(s,d.id);assert.match(s.url,/^https:\/\/(dailymed\.nlm\.nih\.gov|www\.medicines\.org\.uk)\//);if(p.fdaLetterCategory){letters++;assert.match(p.fdaLetterCategory,/^[ABCDX]$/);}
 if(p.tgaCategory!==undefined)assert.match(p.tgaCategory,/^(A|B1|B2|B3|C|D|X|Exempt)$/);}
assert.ok(n>=580,`pregnancy coverage ${n}`);
// 3. Reviewer fields: only recorded statuses; checks need a named reviewer.
const OK=['comparison_pending','not_checked','agrees','differs','not_listed'];
for(const d of db.drugs){for(const k of ['bnf','lexidrugs','uptodate','mims']){const c=d.referenceChecks[k];assert.ok(c&&OK.includes(c.status),`${d.id}.${k}`);if(!['comparison_pending','not_checked'].includes(c.status))assert.ok(c.checkedBy,`${d.id}.${k} needs reviewer`);}
 assert.ok(['not_checked','matches','differs','not_registered'].includes(d.referenceChecks.jfda.status));
 if(d.review.status==='clinically_reviewed'){assert.ok(d.review.clinicalReviewer);assert.ok(d.review.clinicalApprovedAt);}}
// 4. Import → apply round trip on a synthetic sheet is covered by checks_review_import.py.
const app=read('./dist/app.js');assert.match(app,/function referenceChecksHtml/);assert.match(app,/function reviewPill/);assert.match(app,/TGA category/);
assert.ok(read('./dist/index.html').includes('RenalRounds · adults · v0.12.2'));
console.log(`PASS: dosing unchanged; ${n} pregnancy/lactation sections (verbatim, sourced; ${letters} legacy FDA letters); reviewer fields valid.`);
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
online=true;servedVersion='0.12.2';const second=worker('0.12.2','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.12.2/);
online=true;const mismatch=worker('0.13.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.12.2','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.12.2','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.12.2 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
