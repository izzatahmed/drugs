'use strict';
const VERSION='0.6.0';
const BUILD='fa9d3ef86abc558639ff';
const ROOT=new URL('./',self.location.href).href;
const PREFIX='renalrounds:'+new URL(ROOT).pathname+':';
const CACHE=PREFIX+BUILD;
const INDEX=new URL('index.html',ROOT).href;
self.addEventListener('install',event=>event.waitUntil((async()=>{
 const response=await fetch(new Request(INDEX,{cache:'reload'}));
 if(!response.ok||!response.headers.get('content-type')?.includes('text/html'))throw new Error('App download failed');
 const text=await response.clone().text();
 if(!text.includes('"version":"'+VERSION+'"')||!text.includes('"renalrounds-data"'))throw new Error('Mismatched app release');
 const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text))),b=>b.toString(16).padStart(2,'0')).join('').slice(0,20);
 if(digest!==BUILD)throw new Error('Incomplete app update');
 const cache=await caches.open(CACHE);await cache.put(INDEX,response);
})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{
 for(const name of await caches.keys())if(name.startsWith(PREFIX)&&name!==CACHE)await caches.delete(name);
 await self.clients.claim();
})()));
self.addEventListener('message',event=>{
 if(event.data?.type==='ACTIVATE_UPDATE'){event.waitUntil(self.skipWaiting());}
 if(event.data?.type==='CACHE_STATUS'){event.waitUntil((async()=>{const cache=await caches.open(CACHE);const ready=Boolean(await cache.match(INDEX));event.source?.postMessage({type:'CACHE_STATUS',ready,version:VERSION,build:BUILD});})());}
});
self.addEventListener('fetch',event=>{
 const u=new URL(event.request.url),base=new URL(ROOT);
 // Only the app entry point belongs to this cache, never other GitHub Pages sites or sources.
 if(event.request.method!=='GET'||event.request.mode!=='navigate'||u.origin!==base.origin||![base.pathname,base.pathname+'index.html'].includes(u.pathname))return;
 event.respondWith((async()=>{const cache=await caches.open(CACHE);const response=await cache.match(INDEX);return response||fetch(event.request);})());
});
