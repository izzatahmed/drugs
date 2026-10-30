import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const script=read('./dist/interface.js'),app=read('./dist/app.js'),shell=read('./app-shell.html');
const themeBoot=shell.match(/<script>(try\{document\.documentElement\.dataset\.theme=[\s\S]*?)<\/script>/)[1];
function environment(saved={},deny=false){
 const storage=new Map(Object.entries(saved)),nodes=new Map(),handlers={},dialogs=[],root={dataset:{},style:{setProperty(k,v){this[k]=v;}}};
 const node=id=>{if(!nodes.has(id))nodes.set(id,{value:id.includes('filter')?'all':'',checked:false,textContent:'',disabled:false,focus(){this.focused=true;},attrs:{},setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,f){this[k]=f;}});return nodes.get(id);};
 const document={documentElement:root,body:{classList:{toggle(){}}},querySelector:q=>q==='meta[name="theme-color"]'?node('meta'):node(q),querySelectorAll:()=>dialogs,addEventListener:(e,f)=>handlers[e]=f};
 const localStorage={getItem:k=>{if(deny)throw Error('blocked');return storage.get(k)??null;},setItem:(k,v)=>{if(deny)throw Error('blocked');storage.set(k,v);}};
 const window={innerWidth:390,scrollY:80,scrollTo({top}){this.scrollY=top;},addEventListener(){}};
 const context=vm.createContext({document,window,localStorage,JSON,console});
 vm.runInContext(`const $=q=>document.querySelector(q);function storageSet(k,v){try{localStorage.setItem(k,v);return true;}catch{return false;}}
 let db={},selected=null,mode='ckd',category='all',view='all',listLimit=60,renderKey=null,returnedToSearch=false;
 function renderResults(){const q=$('#search').value;selected=!q?null:q==='a'?'abacavir':q==='am'?'amikacin':q.startsWith('aml')?'amlodipine':q==='captopril'?'captopril':selected;renderMonograph();}
 function renderMonograph(){}function openSelected(){window.scrollY=600;}function backToSearch(){returnedToSearch=true;}`,context);
 vm.runInContext(app.match(/function resetFilters\(\)\{[^\n]+/)[0],context);
 vm.runInContext(themeBoot,context);vm.runInContext(script,context);
 return {storage,nodes,dialogs,root,context,node,run:s=>vm.runInContext(s,context)};
}
const filterTest=environment();filterTest.node('#filters-toggle').click();assert.equal(filterTest.node('#filter-panel').open,true);assert.equal(filterTest.node('#filters-toggle').attrs['aria-expanded'],'true');filterTest.node('#filters-toggle').click();assert.equal(filterTest.node('#filter-panel').open,false);
const env=environment();assert.equal(env.root.dataset.theme,'light');env.node('#theme-toggle').click();assert.equal(env.root.dataset.theme,'dark');assert.equal(env.storage.get('renalrounds-theme'),'dark');assert.equal(env.node('#theme-toggle').attrs['aria-pressed'],'true');
const reload=environment(Object.fromEntries(env.storage));assert.equal(reload.root.dataset.theme,'dark');reload.node('#theme-toggle').click();assert.equal(reload.root.dataset.theme,'light');
const blocked=environment({},true);blocked.node('#theme-toggle').click();assert.equal(blocked.root.dataset.theme,'dark','Storage denial must not break manual theme changes');
assert.ok(!/prefers-color-scheme|matchMedia/.test(script+themeBoot+read('./dist/interface.css')),'Manual theme must not follow OS settings');
env.run('renderResults()');env.node('#search').value='amlodipine';env.run('renderResults()');env.node('#search').value='captopril';env.run('renderResults()');env.run('goBack()');assert.equal(env.run('selected'),'amlodipine');assert.equal(env.node('#search').value,'amlodipine');
env.run("mode='ihd';renderMonograph();goBack()");assert.equal(env.run('mode'),'ckd');
env.node('#route-filter').value='Oral';env.run('renderResults();goBack()');assert.equal(env.node('#route-filter').value,'all');
let closed=false;env.dialogs.push({close(){closed=true;}});env.run('goBack()');assert.equal(closed,true);env.dialogs.length=0;
const jump=environment();jump.run('renderResults()');jump.node('#search').value='amlodipine';jump.run('renderResults();openSelected()');assert.equal(jump.run('window.scrollY'),600);jump.run('goBack()');assert.equal(jump.run('window.scrollY'),80);assert.equal(jump.node('#search').value,'amlodipine');
const typing=environment();typing.run('renderResults()');for(const q of ['a','am','aml','amlo','amlodipine']){typing.node('#search').value=q;typing.run('renderResults()');}typing.run('goBack()');assert.equal(typing.node('#search').value,'');assert.equal(typing.run('selected'),null);
assert.ok(!/calc-age|calc-sex|calc-creatinine|history\.back|localStorage.*navigation/.test(script),'Back history must neither capture calculator inputs nor leave the app');
const textCode=app.slice(app.indexOf('let readerLevel='),app.indexOf('async function init('));
const boot=app.split('\n').find(x=>x.includes("const stored=localStorage.getItem('renalrounds-reader-level')"));assert.ok(boot);
for(const [saved,deny,expected] of [[{},false,'100%'],[{'renalrounds-large-text':'true'},false,'115%'],[{'renalrounds-reader-level':'2'},false,'130%'],[{'renalrounds-reader-level':'bad'},false,'100%'],[{},true,'100%']]){
 const e=environment(saved,deny);vm.runInContext(textCode,e.context);vm.runInContext(boot,e.context);assert.equal(e.node('#font-reset').textContent,expected);
 e.run('applyTextSize(3);saveTextSize()');assert.equal(e.node('#font-reset').textContent,'150%');assert.equal(e.node('#font-toggle').disabled,true);e.run('applyTextSize(0)');assert.equal(e.node('#font-reset').textContent,'100%');
}
assert.ok(shell.indexOf('<div class="reader-toolbar"')<shell.indexOf('<div class="search-box"'));assert.match(shell,/<div class="search-row">[\s\S]*?id="filters-toggle"[\s\S]*?id="clear-filters"[\s\S]*?<\/div><details id="filter-panel"/);
assert.ok(!/<header class="topbar"|<section class="intro"|class="draft-notice"/.test(shell));assert.equal((shell.match(/class="dialog-back"/g)||[]).length,4);
console.log('PASS: actual theme startup/toggle, persisted choice, storage-denied fallback, no OS theme path; medicine/setting/filter back history and dialog closure; calculator exclusion; text preference migration/clamping and search-first structure.');

const home=environment({'renalrounds-theme':'dark','renalrounds-reader-level':'3','renalrounds-favourites':'["amlodipine"]'});
home.run('renderResults()');home.node('#search').value='captopril';home.run("mode='ihd';category='Cardiovascular';view='new';renderResults()");home.node('#route-filter').value='Oral';home.run('renderResults()');home.node('#filter-panel').open=true;home.node('#results').scrollTop=400;
let prevented=false;home.node('#home-link').click({preventDefault(){prevented=true;}});
assert.ok(prevented);assert.equal(home.run('selected'),null);assert.equal(home.run('mode'),'ckd');assert.equal(home.run('category'),'all');assert.equal(home.run('view'),'all');assert.equal(home.node('#search').value,'');assert.equal(home.node('#route-filter').value,'all');assert.equal(home.node('#filter-panel').open,false);assert.equal(home.node('#filters-toggle').attrs['aria-expanded'],'false');assert.equal(home.node('#results').scrollTop,0);assert.equal(home.run('window.scrollY'),0);assert.equal(home.node('#search').focused,true);
assert.equal(home.root.dataset.theme,'dark');assert.equal(home.storage.get('renalrounds-reader-level'),'3');assert.equal(home.storage.get('renalrounds-favourites'),'["amlodipine"]');home.run('goBack()');assert.equal(home.run('selected'),'captopril');assert.equal(home.run('mode'),'ihd');assert.equal(home.node('#search').value,'captopril');assert.equal(home.node('#route-filter').value,'Oral');
assert.match(shell,/<a id="home-link"[^>]*href="\.\/"[^>]*aria-label="RenalRounds v0\.11\.2 — Home"/);
console.log('PASS: Home click resets browsing state, scroll and focus, preserves reader preferences/favourites, and Back restores the previous medicine/filters/setting.');
