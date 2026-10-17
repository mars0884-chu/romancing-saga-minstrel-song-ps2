/* 2005 PS2 guide, offline installation v0.4.8. */
const KEY='minstrel-ps2-2005-v0.4.8';
const FILES=["./","./index.html","./data.json","./manifest.webmanifest","./assets/ps2-original-cover.webp","./assets/icon-192.png","./assets/icon-512.png","./assets/apple-touch-icon.png"];
async function preload(){
 const cache=await caches.open(KEY);
 const result=await fetch('./index.html',{cache:'reload'});
 if(!result.ok)throw Error('攻略首頁載入失敗');
 await cache.put('./index.html',result.clone());
 const fail=[];
 const others=FILES.filter(f=>f!=='./index.html');
 for(let i=0;i<others.length;i+=8){
  const batch=others.slice(i,i+8);
  await Promise.all(batch.map(async f=>{
   try{const res=await fetch(f,{cache:'reload'}); if(!res.ok)throw Error(String(res.status)); await cache.put(f,res.clone())}
   catch(e){fail.push(f)}
  }));
 }
 if(fail.length)throw Error('離線資源未完整儲存：'+fail.join(', '));
 return FILES.length;
}
self.addEventListener('install',e=>e.waitUntil(preload().then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil((async()=>{await Promise.all((await caches.keys()).filter(k=>k.startsWith('minstrel-ps2-')&&k!==KEY).map(k=>caches.delete(k))); await self.clients.claim()})()));
self.addEventListener('message',e=>{if(e.data?.type!=='CACHE_GUIDE')return; e.waitUntil(preload().then(n=>e.ports[0]?.postMessage({ok:true,count:n})).catch(err=>e.ports[0]?.postMessage({ok:false,error:err.message})))});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 const url=new URL(e.request.url);if(url.origin!==self.location.origin||!url.pathname.startsWith(new URL('./',self.location.href).pathname))return;
 if(e.request.mode==='navigate'){
  e.respondWith((async()=>{const cache=await caches.open(KEY);try{const res=await fetch(e.request);if(res.ok){cache.put('./index.html',res.clone()).catch(()=>{});return res}}catch(x){}return await cache.match('./index.html')||Response.error()})());return;
 }
 e.respondWith((async()=>{const cached=await caches.match(e.request);if(cached)return cached;try{const res=await fetch(e.request);if(res.ok)(await caches.open(KEY)).put(e.request,res.clone()).catch(()=>{});return res}catch(x){return Response.error()}})());
});