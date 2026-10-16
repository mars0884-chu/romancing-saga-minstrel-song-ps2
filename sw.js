/* Original 2005 PS2 PWA: offline-first for complete embedded guide. */
const CACHE='minstrel-ps2-2005-v0.4.1';
const SHELL=['./','./index.html','./manifest.webmanifest','./assets/icon-192.png','./assets/icon-512.png','./assets/apple-touch-icon.png','./assets/icon.svg'];
self.addEventListener('install',event=>{event.waitUntil((async()=>{
  const cache=await caches.open(CACHE);
  // The guide and all search data are in index.html, and must be cached successfully.
  await cache.add('./index.html');
  await Promise.allSettled(SHELL.filter(x=>x!=='./index.html').map(async path=>{
    const response=await fetch(path,{cache:'reload'});
    if(response.ok)await cache.put(path,response);
  }));
  await self.skipWaiting();
})());});
self.addEventListener('activate',event=>event.waitUntil((async()=>{
 const names=await caches.keys();await Promise.all(names.filter(k=>k.startsWith('minstrel-ps2-')&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim();
})()));
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET')return;
 const url=new URL(event.request.url);if(url.origin!==self.location.origin)return;
 if(event.request.mode==='navigate'){
   event.respondWith((async()=>{
     try{const response=await fetch(event.request);if(response.ok){const cache=await caches.open(CACHE);cache.put('./index.html',response.clone());return response}}
     catch(_){}
     return (await caches.match('./index.html'))||Response.error();
   })());return;
 }
 event.respondWith((async()=>{const hit=await caches.match(event.request);if(hit)return hit;try{const response=await fetch(event.request);if(response.ok){const cache=await caches.open(CACHE);cache.put(event.request,response.clone())}return response}catch(_){return Response.error()}})());
});