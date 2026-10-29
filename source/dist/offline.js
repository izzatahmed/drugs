'use strict';
(async function(){
 const status=document.querySelector('#offline-status'),check=document.querySelector('#check-update'),load=document.querySelector('#load-update');
 let registration=null,cacheReady=false,cachedVersion=null,reloading=false;
 if(!db){status.textContent='Reference unavailable · offline saving disabled';check.hidden=true;return;}
 function show(){status.textContent=cacheReady?`${navigator.onLine?'Offline ready':'Offline copy'} · cached v${cachedVersion} · sources ${db.releaseDate}`:navigator.onLine?'Online · offline copy not ready':'Offline · reopen not yet confirmed';}
 function ping(){navigator.serviceWorker.controller?.postMessage({type:'CACHE_STATUS'});}
 if(!('serviceWorker' in navigator)||!window.isSecureContext||!['https:','http:'].includes(location.protocol)){status.textContent='Local search ready · offline installation unavailable here';check.hidden=true;return;}
 navigator.serviceWorker.addEventListener('message',e=>{if(e.data?.type==='CACHE_STATUS'){cacheReady=Boolean(e.data.ready);cachedVersion=e.data.version;if(cachedVersion!==db.version){status.textContent=`Cached v${cachedVersion} differs from displayed v${db.version}; load the available update when connected.`;}else show();}});
 navigator.serviceWorker.addEventListener('controllerchange',()=>{if(reloading)location.reload();else ping();});
 function waiting(){if(registration?.waiting){load.hidden=false;load.textContent='Load available update';}}
 try{
  registration=await navigator.serviceWorker.register(new URL('sw.js',location.href),{scope:'./',updateViaCache:'none'});
  waiting();
  registration.addEventListener('updatefound',()=>{const w=registration.installing;w?.addEventListener('statechange',()=>{if(w.state==='installed'){waiting();ping();}});});
  await navigator.serviceWorker.ready;ping();
  if(!navigator.serviceWorker.controller){status.textContent='Offline copy saved · reopen this page to activate';}
 }catch{status.textContent='Online/local search ready · offline saving unavailable';}
 check.addEventListener('click',async()=>{if(!registration){status.textContent='Offline saving unavailable · verify sw.js was uploaded';return;}check.disabled=true;status.textContent='Checking for an app update…';try{await registration.update();waiting();if(!registration.waiting&&!registration.installing){show();notify('No new app release found. Clinical source dates are unchanged.');}else notify('Update check started; load it when available.');}catch{status.textContent='Update check failed · existing copy retained';}finally{check.disabled=false;}});
 load.addEventListener('click',()=>{if(registration?.waiting){reloading=true;registration.waiting.postMessage({type:'ACTIVATE_UPDATE'});}});
 window.addEventListener('online',()=>{show();ping();});window.addEventListener('offline',()=>{show();ping();});
})();
