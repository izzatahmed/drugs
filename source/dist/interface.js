'use strict';
// Appearance is chosen by the reader. OS colour-scheme changes are never observed.
function applyTheme(theme){
 const dark=theme==='dark';document.documentElement.dataset.theme=dark?'dark':'light';
 const button=$('#theme-toggle');button.setAttribute('aria-pressed',String(dark));
 button.setAttribute('aria-label',dark?'Switch to day theme':'Switch to night theme');
 button.innerHTML=`<span aria-hidden="true">${dark?'☀':'☾'}</span><span class="theme-label">${dark?'Day':'Night'}</span>`;
 document.querySelector('meta[name="theme-color"]').content=dark?'#101b20':'#f7f9f7';
}
applyTheme(document.documentElement.dataset.theme);
$('#theme-toggle').addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';applyTheme(theme);storageSet('renalrounds-theme',theme);});

// In-app history never navigates away from the reference or stores calculator inputs.
const navigationStack=[];let navigationCurrent=null,navigationRendering=false,navigationRestoring=false,navigationSearchActive=false;
function navigationSnapshot(){return {selected,mode,category,view,query:$('#search').value,route:$('#route-filter').value,content:$('#content-filter').value,setting:$('#setting-filter').value,otc:$('#otc-filter').checked,scroll:window.scrollY};}
function navigationKey(s){const {scroll,...state}=s;return JSON.stringify(state);}
function finishNavigation(previous){
 if(!db)return;const next=navigationSnapshot();
 if(!navigationRestoring&&previous&&navigationKey(next)!==navigationKey(previous)){
  // Prefix typing/deleting is one step, even when intermediate results select other drugs.
  const typing=next.query!==previous.query;
  const sameSearch=(previous.query&&next.query.startsWith(previous.query))||(next.query&&previous.query.startsWith(next.query));
  if(!typing||!navigationSearchActive||!sameSearch){
   navigationStack.push({...previous});if(navigationStack.length>60)navigationStack.shift();
  }
  navigationSearchActive=typing;
 }
 navigationCurrent=next;
}
const originalRenderResults=renderResults,originalRenderMonograph=renderMonograph;
renderResults=function(){const previous=navigationCurrent;navigationRendering=true;try{return originalRenderResults();}finally{navigationRendering=false;finishNavigation(previous);}};
renderMonograph=function(){const previous=navigationCurrent;try{return originalRenderMonograph();}finally{if(!navigationRendering)finishNavigation(previous);}};
const originalOpenSelected=openSelected;
openSelected=function(){
 if(window.innerWidth<761&&!navigationRestoring&&selected){navigationStack.push(navigationSnapshot());if(navigationStack.length>60)navigationStack.shift();}
 originalOpenSelected();if(db)navigationCurrent=navigationSnapshot();if(typeof window.showNavBack==='function')window.showNavBack();
};
function goBack(){
 const dialogs=[...document.querySelectorAll('dialog[open]')];if(dialogs.length){dialogs.at(-1).close();return;}
 const previous=navigationStack.pop();if(!previous){backToSearch();return;}
 navigationRestoring=true;try{
  selected=previous.selected;mode=previous.mode;category=previous.category;view=previous.view;
  $('#search').value=previous.query;$('#route-filter').value=previous.route;$('#content-filter').value=previous.content;$('#setting-filter').value=previous.setting;$('#otc-filter').checked=previous.otc;
  listLimit=60;renderKey=null;renderResults();window.scrollTo({top:previous.scroll,behavior:'instant'});
  navigationCurrent=navigationSnapshot();navigationSearchActive=false;
 }finally{navigationRestoring=false;}
}
document.addEventListener('click',e=>{if(e.target.closest('[data-app-back]'))goBack();});
window.addEventListener('scroll',()=>{if(navigationCurrent&&!navigationRestoring)navigationCurrent.scroll=window.scrollY;},{passive:true});

// Home clears the browsing context while preserving reader preferences/favourites.
function goHome(){
 [...document.querySelectorAll('dialog[open]')].forEach(dialog=>dialog.close());
 selected=null;mode='ckd';resetFilters();$('#search').value='';renderKey=null;
 $('#filter-panel').open=false;$('#filters-toggle').setAttribute('aria-expanded','false');
 renderResults();$('#results').scrollTop=0;window.scrollTo({top:0,behavior:'instant'});
 $('#search').focus({preventScroll:true});
 if(db)navigationCurrent=navigationSnapshot();
}
$('#home-link').addEventListener('click',event=>{event.preventDefault();goHome();});

$('#filters-toggle').addEventListener('click',()=>{$('#filter-panel').open=!$('#filter-panel').open;$('#filters-toggle').setAttribute('aria-expanded',String($('#filter-panel').open));});
$('#filter-panel').addEventListener('toggle',()=>$('#filters-toggle').setAttribute('aria-expanded',String($('#filter-panel').open)));

// Back arrow: visible at rest, at the page end and while scrolling up; hidden while scrolling down.
(function(){const btn=typeof document.querySelector==='function'?document.querySelector('#nav-back'):null;if(!btn||!btn.classList||typeof window.addEventListener!=='function')return;let last=window.scrollY,ticking=false,suppressUntil=0;
 window.showNavBack=()=>{btn.classList.remove('is-hidden');suppressUntil=Date.now()+500;last=window.scrollY;};
 function update(){const y=window.scrollY,atEnd=window.innerHeight+y>=document.documentElement.scrollHeight-4;
  if(Date.now()<suppressUntil){last=y;ticking=false;return;}btn.classList.toggle('is-hidden',y>last+4&&!atEnd&&y>80);last=y;ticking=false;}
 window.addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(update);}},{passive:true});})();
