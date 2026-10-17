/* v0.5.0: offline base guide + personal browser cache of original images; no public redistribution. */
const KEY='minstrel-ps2-2005-v0.5.0';
const FILES=['./','./index.html','./data.json','./manifest.webmanifest','./assets/ps2-original-cover.webp','./assets/icon-192.png','./assets/icon-512.png','./assets/apple-touch-icon.png'];
const IMAGE_HOSTS=new Set(['www.jp.square-enix.com','kyokugen.info','cdn-ak.f.st-hatena.com','blog-imgs-161.fc2.com','stat.ameba.jp']);
async function preload(){
 const cache=await caches.open(KEY);
 const main=await fetch('./index.html',{cache:'reload'});if(!main.ok)throw Error('攻略首頁無法儲存');
 await cache.put('./index.html',main.clone());
 const rest=FILES.filter(f=>f!=='./index.html');
 const missing=[];
 await Promise.all(rest.map(async f=>{try{const r=await fetch(f,{cache:'reload'});if(!r.ok)throw Error(String(r.status));await cache.put(f,r.clone())}catch(e){missing.push(f)}}));
 if(missing.length)throw Error('缺少'+missing.join(','));
 return FILES.length;
}
self.addEventListener('install',e=>e.waitUntil(preload().then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil((async()=>{await Promise.all((await caches.keys()).filter(k=>k.startsWith('minstrel-ps2-')&&k!==KEY).map(k=>caches.delete(k)));await self.clients.claim()})()));
self.addEventListener('message',e=>{if(e.data?.type!=='CACHE_GUIDE')return;e.waitUntil(preload().then(n=>e.ports[0]?.postMessage({ok:true,count:n})).catch(err=>e.ports[0]?.postMessage({ok:false,error:err.message})))});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 const url=new URL(e.request.url),site=new URL('./',self.location.href);
 if(url.origin!==self.location.origin){
  if(e.request.destination!=='image'||url.protocol!=='https:'||!IMAGE_HOSTS.has(url.hostname))return;
  e.respondWith((async()=>{
   const cache=await caches.open(KEY),saved=await cache.match(url.href);
   if(saved)return saved;
   try{const img=await fetch(e.request);if(img.ok||img.type==='opaque')await cache.put(url.href,img.clone());return img}catch(err){return Response.error()}
  })());return;
 }
 if(!url.pathname.startsWith(site.pathname))return;
 if(e.request.mode==='navigate'){
  e.respondWith((async()=>{const cache=await caches.open(KEY);try{const r=await fetch(e.request);if(r.ok){cache.put('./index.html',r.clone()).catch(()=>{});return r}}catch(e){}return await cache.match('./index.html')||Response.error()})());return;
 }
 e.respondWith((async()=>{const cache=await caches.open(KEY),saved=await cache.match(e.request);if(saved)return saved;try{const r=await fetch(e.request);if(r.ok)await cache.put(e.request,r.clone());return r}catch(e){return Response.error()}})());
});
