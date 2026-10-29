'use strict';
// Coverage is a curation measure, never a clinical approval signal.
let clinicalVersionCache;
function latestClinicalVersion(){return clinicalVersionCache ||= db.drugs.reduce((v,d)=>[d.addedInVersion,d.updatedInVersion].filter(Boolean).reduce((a,b)=>b.localeCompare(a,undefined,{numeric:true})>0?b:a,v),'0.0.0');}
function suggestions(query){
 const q=norm(query);if(q.length<4||q.length>40||q.includes(' '))return [];
 function distance(a,b){let row=Array.from({length:b.length+1},(_,i)=>i);for(let i=1;i<=a.length;i++){const next=[i];for(let j=1;j<=b.length;j++)next[j]=Math.min(next[j-1]+1,row[j]+1,row[j-1]+(a[i-1]!==b[j-1]));row=next;}return row[b.length];}
 return db.drugs.map(d=>({d,n:Math.min(...d.nameKeys.filter(k=>Math.abs(k.length-q.length)<=2).map(k=>distance(q,k)))})).filter(x=>x.n<=Math.min(2,Math.floor(q.length/4))).sort((a,b)=>a.n-b.n||a.d.name.localeCompare(b.d.name)).slice(0,4).map(x=>x.d);
}
function renderCompletion(){
 const count=(key,status='summarized')=>db.drugs.filter(d=>d.modalities[key].status===status).length;
 const approved=db.drugs.filter(d=>d.review.clinicalApprovedAt&&d.review.clinicalReviewer).length;
 const fieldCount=key=>db.drugs.filter(d=>d.pharmacokinetics[key].status==='sourced').length;
 $('#completion-body').innerHTML=`<div class="modal-callout"><strong>Clinical formulary: incomplete</strong><p>Release ${h(db.version)} expands 12 cardiovascular renal profiles. Source access is separate from independent clinical approval. ${approved} of ${db.drugs.length} entries have recorded independent approval.</p></div><div class="dashboard-grid"><div class="dashboard-stat"><strong>${db.coverage.renal}</strong><span>Renal profiles · partial coverage</span></div><div class="dashboard-stat"><strong>${db.coverage.catalog}</strong><span>Renal-dose-pending entries</span></div><div class="dashboard-stat"><strong>${db.pharmacokineticCoverage.profiles}</strong><span>Source-based PK profiles</span></div><div class="dashboard-stat"><strong>${db.pharmacokineticCoverage.allFourCoreFields}</strong><span>Profiles with 4 core PK items</span></div></div><h3>Setting-specific summaries</h3><p class="dashboard-note">Counts are out of all ${db.drugs.length} entries. “Summarized” can mean monitoring or eligibility guidance; it does not establish a complete numeric regimen or clinical approval. Click a setting to find those existing summaries.</p><table class="dashboard-table"><thead><tr><th scope="col">Setting</th><th scope="col">Summarized</th><th scope="col">Other / pending</th></tr></thead><tbody>${Object.entries(modeNames).map(([key,name])=>`<tr><th scope="row"><button data-coverage-setting="${key}">${h(name)}</button></th><td>${count(key)}</td><td>${db.drugs.length-count(key)}</td></tr>`).join('')}</tbody></table><h3>Source-based PK fields</h3><table class="dashboard-table"><tbody>${[['halfLife','Reference half-life'],['renalHalfLife','Renal / ESRF half-life'],['volumeOfDistribution','Volume of distribution'],['proteinBinding','Protein binding']].map(([key,name])=>`<tr><th scope="row">${name}</th><td>${fieldCount(key)} / ${db.drugs.length}</td></tr>`).join('')}</tbody></table><div class="dashboard-actions"><button id="export-queue">Export completion queue JSON ↓</button><button id="export-plan">Download completion plan ↓</button></div><h3>Next clinical work</h3><p>Prioritize the local adult formulary: antihypertensives, antimicrobials, anticoagulants, diabetes medicines, analgesics and common OTC products. Complete indication/formulation-specific CKD and RRT evidence, reconcile source differences, then record independent nephrology and renal-pharmacy sign-off.</p><p>BNF has been clarified as the British National Formulary. BNF monographs remain inaccessible; no BNF verification is claimed. Only individually linked PDR material has been consulted. The queue records pending, unknown and not-reported fields separately.</p>`;
}
function exportQueue(){
 const drugs=db.drugs.map(d=>({id:d.id,name:d.name,category:d.category,routes:d.routes,content:d.entryType,renalDoseSourceCheckedAt:d.review.sourceCheckedAt,pkSourceCheckedAt:d.pharmacokinetics.sourceCheckedAt,modalities:Object.fromEntries(Object.entries(d.modalities).map(([k,m])=>[k,m.status])),pkFields:Object.fromEntries(['halfLife','renalHalfLife','volumeOfDistribution','proteinBinding'].map(k=>[k,d.pharmacokinetics[k].status])),removal:Object.fromEntries(Object.entries(d.pharmacokinetics.dialysability).map(([k,m])=>[k,m.status])),independentClinicalReview:d.review.status,priority:['Cardiovascular','Antimicrobials','Diabetes & endocrine','Anticoagulation & haematology','Pain & neurology','OTC & medicine safety'].includes(d.category)?'1: common rounds classes':'2: remaining formulary'}));
 downloadText(`RenalRounds_completion_v${db.version}.json`,JSON.stringify({version:db.version,generatedAt:db.softwareReleaseDate,note:'Statuses describe curation coverage, not suitability for an individual patient. Summarized does not mean clinically approved or complete for every indication.',drugs},null,2),'application/json');
}
function attachDrugTools(){
 if(!selected)return;const d=drugMap.get(selected);
 const head=$('#monograph .mono-head');if(head)head.insertAdjacentHTML('beforeend','<div class="utility-actions"><button id="copy-link">Copy drug link</button><button id="print-drug">Print selected setting</button><button data-open="completion">Coverage gaps</button></div>');
 $('#selected-shortcut').hidden=false;$('#selected-shortcut').innerHTML=`<span>Selected: <strong>${h(d.name)}</strong></span><button id="open-selected">Open reference ↓</button>`;
}
function openSelected(){if(!selected)return;$('#filter-panel').open=false;document.activeElement?.blur();$('#monograph').scrollIntoView({block:'start',behavior:'instant'});}
function backToSearch(){document.querySelector('.search-area').scrollIntoView({block:'start',behavior:'instant'});$('#search').focus({preventScroll:true});}
async function copyDrugLink(){
 const link=location.href;
 try{await navigator.clipboard.writeText(link);notify('Drug link copied · preserves the selected setting');}catch{notify('Copy is unavailable here; use the address bar link.');}
}
document.addEventListener('click',e=>{
 if(e.target.closest('[data-open="references"]')){if($('#about').open)$('#about').close();if($('#completion').open)$('#completion').close();renderReferences();$('#references').showModal();return;}
 if(e.target.closest('#close-references')){$('#references').close();return;}
 if(e.target.closest('[data-open="completion"]')){renderCompletion();$('#completion').showModal();return;}
 if(e.target.closest('#close-completion')){$('#completion').close();return;}
 if(e.target.closest('#export-queue')){exportQueue();return;}
 if(e.target.closest('#export-plan')){downloadText('COMPLETION_PLAN.md',JSON.parse($('#renalrounds-docs').textContent).plan);return;}
 const setting=e.target.closest('[data-coverage-setting]');if(setting){resetFilters();$('#search').value='';$('#setting-filter').value=setting.dataset.coverageSetting;mode=setting.dataset.coverageSetting;$('#completion').close();renderResults();backToSearch();return;}
 const suggestion=e.target.closest('[data-suggestion]');if(suggestion){resetFilters();$('#search').value=suggestion.dataset.suggestion;renderResults();return;}
 if(e.target.closest('#open-selected')){openSelected();return;}
 if(e.target.closest('#back-search')){backToSearch();return;}
 if(e.target.closest('#copy-link')){copyDrugLink();return;}
 if(e.target.closest('#print-drug')){window.print();return;}
});
$('#completion').addEventListener('click',e=>{if(e.target===$('#completion')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
let scrollTick=false;
window.addEventListener('scroll',()=>{if(scrollTick)return;scrollTick=true;requestAnimationFrame(()=>{scrollTick=false;$('#back-search').hidden=innerWidth>760||!selected||$('#monograph').getBoundingClientRect().top>innerHeight*.7;});},{passive:true});

function renderReferences(){
 $('#references-body').innerHTML=`<div class="modal-callout"><strong>Use each source for its stated purpose.</strong><p>BNF means British National Formulary. Drug-specific doses below cite their individual sources. A society website, directory or patient page does not establish a complete dialysis regimen.</p></div><div class="context-notice"><strong>Medication stewardship · KDIGO 2024.</strong><p>${h(db.drugStewardship.text)}</p>${db.drugStewardship.sourceIds.map(sourceLink).join(' · ')}</div>${db.referenceResources.map(r=>`<article class="source-card"><div class="source-type">${h(r.organisation)} · ${h(r.role)}</div><a href="${h(r.url)}" target="_blank" rel="noopener noreferrer">${h(r.title)} ↗</a><p>${h(r.use)}</p><small>${h(r.access)}<br>Resource check: ${h(r.sourceCheckedAt)}</small></article>`).join('')}<p>Review date refers to access described on each card. It does not mean all documents on that organisation’s website were reviewed. BNF monograph reconciliation and independent clinical review remain pending.</p>`;
}
$('#references').addEventListener('click',e=>{if(e.target===$('#references')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
