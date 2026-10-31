import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const db=JSON.parse(read('./dist/database.json')),base=JSON.parse(read('./baseline_v112.json')),classes=JSON.parse(read('./drug_classes_v113.json'));
assert.equal(db.version,'0.11.3');assert.equal(base.version,'0.11.2');assert.equal(db.clinicalDataVersion,'0.11.2','Drug content version unchanged');
// 1. Dosing content is byte-identical to 0.11.2: every table, status, metric, flag, PK field, source URL/id.
assert.equal(db.drugs.length,base.drugs.length);
for(const d of db.drugs){const o=base.drugs.find(x=>x.id===d.id);assert.ok(o,d.id);
 for(const m of Object.keys(o.modalities)){assert.deepEqual(d.modalities[m].tables,o.modalities[m].tables,`${d.id}/${m} tables`);assert.equal(d.modalities[m].status,o.modalities[m].status);assert.deepEqual(d.modalities[m].sourceIds,o.modalities[m].sourceIds);}
 for(const k of ['name','aliases','category','routes','otc','kidneyMetric','flag','entryType','sourceIds','review','addedInVersion','completeness'])assert.deepEqual(d[k],o[k],`${d.id}.${k}`);
 const pk=(p)=>JSON.stringify(p,(k,v)=>k==='context'||k==='notes'?undefined:v);assert.equal(pk(d.pharmacokinetics),pk(o.pharmacokinetics),`${d.id} PK values`);
 if(classes[d.id]){assert.equal(o.drugClass,o.category);assert.equal(d.drugClass,classes[d.id]);}else assert.equal(d.drugClass,o.drugClass);
}
assert.equal(db.drugs.filter(d=>d.drugClass===d.category).length,0);
for(const s of base.sources){const n=db.sources.find(x=>x.id===s.id);assert.ok(n);assert.equal(n.url,s.url);assert.equal(n.accessed,s.accessed);assert.deepEqual(n.suppliedDocument,s.suppliedDocument);}
assert.equal(db.sources.length,base.sources.length);
// 2. No internal working notes in reader-facing data or app text.
const visible=JSON.stringify({...db,sources:db.sources.map(({suppliedDocument,...s})=>s)})+read('./dist/app.js')+read('./dist/workflow.js')+read('./app-shell.html');
for(const re of [/this environment/i,/by the user/i,/Search service unavailable/i,/inaccessible in/i,/content inaccessible/i,/User-supplied/i,/uploaded (book|PDFs?)/i,/supplied PDF/i,/Supplied (fifth|historical|institutional|handbook)/i,/the new PIRRT row/i,/access blocked/i])assert.ok(!re.test(visible),`Internal wording remains: ${re}`);
// 3. Cockcroft–Gault arithmetic against hand-worked values.
const ctx=vm.createContext({});vm.runInContext(read('./dist/renal-math.js')+';this.C=CrClMath;this.R=RenalMath;',ctx);const C=ctx.C;
const cg=o=>C.compute({context:'stable',unit:'mgdl',height:'',...o});
let r=cg({age:60,sex:'male',creatinine:1.4,weight:90,height:175});assert.ok(r.ok);
assert.ok(Math.abs(r.actual-7200/100.8)<1e-9);assert.ok(Math.abs(r.ibw-(50+2.3*(175-152.4)/2.54))<1e-9);
assert.ok(Math.abs(r.ideal-80*r.ibw/100.8)<1e-9);assert.ok(Math.abs(r.adjbw-(r.ibw+0.4*(90-r.ibw)))<1e-9);assert.ok(Math.abs(r.adjusted-80*r.adjbw/100.8)<1e-9);
r=cg({age:80,sex:'female',creatinine:110,unit:'umol',weight:55});assert.ok(Math.abs(r.actual-60*55/(72*110/88.4)*0.85)<1e-9);assert.equal(r.ideal,null);assert.equal(r.adjusted,null);
r=cg({age:40,sex:'female',creatinine:1,weight:50,height:165});assert.ok(r.ideal!==null);assert.equal(r.adjusted,null,'No adjusted weight when actual ≤ ideal');
assert.ok(cg({age:50,sex:'male',creatinine:1,weight:150,height:170}).warnings.some(w=>/130%/.test(w)));
for(const bad of [{context:'aki'},{context:'dialysis'},{context:'pregnancy'},{context:''},{age:17},{age:121},{sex:''},{creatinine:0},{creatinine:''},{weight:''},{weight:9},{weight:501},{height:49},{height:251},{unit:'mg/L'}]){const x=cg({age:60,sex:'male',creatinine:1,weight:70,...bad});assert.equal(x.ok,false,JSON.stringify(bad));assert.equal('actual' in x,false);}
// 4. Interface contracts.
const shell=read('./app-shell.html'),app=read('./dist/app.js'),calc=read('./dist/calculator.js'),html=read('./dist/index.html');
assert.match(shell,/name="calc-measure" value="crcl"/);assert.match(shell,/doi\.org\/10\.1159\/000180580/);assert.match(shell,/og:title/);
assert.ok(html.includes(read('./dist/renal-math.js'))&&html.includes(calc)&&html.includes('RenalRounds · adults · v0.11.3'));
assert.ok(!/localStorage|sessionStorage|fetch\s*\(|downloadText|location\./.test(calc),'Calculator values must not be persisted or sent');
assert.match(app,/class="mono-back" data-app-back/);assert.match(app,/e\.key==='Enter'&&document\.activeElement===\$\('#search'\)/);
assert.match(read('./dist/interface.css'),/max-width:760px\)\{\.nav-back\{display:none!important\}/);
assert.match(read('./dist/workflow.js'),/github\.com\/izzatahmed\/drugs\/issues\/new/);
console.log('PASS: v0.11.3 dosing tables, statuses, PK values and sources identical to v0.11.2; 426 classes added; no internal wording; Cockcroft–Gault arithmetic and validation; phone back control, Enter-to-open, report link.');
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
online=true;servedVersion='0.11.3';const second=worker('0.11.3','next');await second.fire('install');
assert.equal(second.activated,false);assert.match(await (await first.navigate('https://example.org/drugs/')).text(),/0.10.0/);
await second.fire('message',{data:{type:'ACTIVATE_UPDATE'}});assert.equal(second.activated,true);await second.fire('activate');online=false;
assert.match(await (await second.navigate('https://example.org/drugs/')).text(),/0.11.3/);
online=true;const mismatch=worker('0.12.0','bad');await assert.rejects(mismatch.fire('install'),/Mismatched/);
await assert.rejects(worker('0.11.3','partial').fire('install'),/Incomplete app update/);
httpStatus=404;await assert.rejects(worker('0.11.3','404').fire('install'),/download failed/);
console.log('PASS: actual worker offline reopen, old-release retention, explicit v0.11.3 activation, mismatched/partial/404 rejection and scoped cache isolation. Hosted HTTPS/physical-phone integration pending.');
