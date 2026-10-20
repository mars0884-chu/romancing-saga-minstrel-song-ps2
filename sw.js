/* v0.9.8: PWA automatically loads searchable data and installs local guide images; permitted third-party images are cached on-device. */
const KEY='minstrel-ps2-2005-v0.9.8-local-maps4';
const IMG_KEY='minstrel-ps2-2005-images-v1';
const FILES=['./','./index.html','./data.json','./manifest.webmanifest','./assets/ps2-original-cover.webp','./assets/icon-192.png','./assets/icon-512.png','./assets/apple-touch-icon.png',
"./assets/atlas/map-01.svg",
"./assets/atlas/map-02.svg",
"./assets/atlas/map-03.svg",
"./assets/atlas/map-04.svg",
"./assets/atlas/map-05.svg",
"./assets/atlas/map-06.svg",
"./assets/atlas/map-07.svg",
"./assets/atlas/map-08.svg",
"./assets/atlas/map-09.svg",
"./assets/atlas/map-10.svg",
"./assets/atlas/map-11.svg",
"./assets/diagrams/dinosaur-eggs.svg",
"./assets/diagrams/final-trial.svg",
"./assets/diagrams/fortress-ruins.svg",
"./assets/diagrams/frozen-castle.svg",
"./assets/diagrams/heretic-ruins.svg",
"./assets/diagrams/region-01.svg",
"./assets/diagrams/region-02.svg",
"./assets/diagrams/region-03.svg",
"./assets/diagrams/region-04.svg",
"./assets/diagrams/region-05.svg",
"./assets/diagrams/region-06.svg",
"./assets/diagrams/region-07.svg",
"./assets/diagrams/region-08.svg",
"./assets/diagrams/region-09.svg",
"./assets/diagrams/region-10.svg",
"./assets/diagrams/region-11.svg",
"./assets/diagrams/three-destinations.svg",
"./assets/diagrams/treasure-cave.svg",
"./assets/diagrams/twinmoon-temple.svg",
"./assets/diagrams/underworld.svg",
"./assets/diagrams/water-dragon-temple.svg",
"./assets/equipment/g105.svg",
"./assets/equipment/g106.svg",
"./assets/equipment/g107.svg",
"./assets/equipment/g108.svg",
"./assets/equipment/g109.svg",
"./assets/equipment/g110.svg",
"./assets/equipment/g111.svg",
"./assets/equipment/g112.svg",
"./assets/equipment/g113.svg",
"./assets/floorplans/bafal_bayer.svg",
"./assets/floorplans/bafal_elizabeth.svg",
"./assets/floorplans/bafal_forest.svg",
"./assets/floorplans/bafal_forest_dark.svg",
"./assets/floorplans/bafal_gold.svg",
"./assets/floorplans/bafal_great.svg",
"./assets/floorplans/bafal_loban.svg",
"./assets/floorplans/bafal_melville.svg",
"./assets/floorplans/drylands_desert.svg",
"./assets/floorplans/drylands_galessa.svg",
"./assets/floorplans/drylands_nieca.svg",
"./assets/floorplans/drylands_oldcastle.svg",
"./assets/floorplans/etc_faerie.svg",
"./assets/floorplans/etc_last.svg",
"./assets/floorplans/etc_mummy.svg",
"./assets/floorplans/etc_purgatory.svg",
"./assets/floorplans/etc_sherah.svg",
"./assets/floorplans/etc_ukkom.svg",
"./assets/floorplans/final-trial.svg",
"./assets/floorplans/frontier_jewelbeast.svg",
"./assets/floorplans/frontier_newroad.svg",
"./assets/floorplans/frontier_saoki.svg",
"./assets/floorplans/frontier_vampire.svg",
"./assets/floorplans/frontier_yassi.svg",
"./assets/floorplans/kjaragt_assassin.svg",
"./assets/floorplans/kjaragt_estamir.svg",
"./assets/floorplans/kjaragt_tarmitta.svg",
"./assets/floorplans/knight_abandoned.svg",
"./assets/floorplans/knight_constanzu.svg",
"./assets/floorplans/knight_dragon.svg",
"./assets/floorplans/knight_mirsaburg.svg",
"./assets/floorplans/knight_paganruins.svg",
"./assets/floorplans/ligau_dinosaurs.svg",
"./assets/floorplans/ligau_plain.svg",
"./assets/floorplans/ligau_tomae.svg",
"./assets/floorplans/ligau_treasure.svg",
"./assets/floorplans/rosalia_crystal.svg",
"./assets/floorplans/rosalia_evil.svg",
"./assets/floorplans/rosalia_isthmus.svg",
"./assets/floorplans/rosalia_isthmus_castle.svg",
"./assets/floorplans/rosalia_scurve.svg",
"./assets/floorplans/twin-moons.svg",
"./assets/floorplans/underworld.svg",
"./assets/floorplans/valhalland_east.svg",
"./assets/floorplans/valhalland_field.svg",
"./assets/floorplans/valhalland_frozen.svg",
"./assets/floorplans/valhalland_south.svg",
"./assets/floorplans/valhalland_south2.svg",
"./assets/floorplans/valhalland_south3.svg",
"./assets/floorplans/valhalland_west.svg",
"./assets/floorplans/walon_gueccoes.svg",
"./assets/floorplans/walon_jungle.svg",
"./assets/floorplans/walon_silver.svg",
"./assets/floorplans/water-dragon.svg",
"./assets/heroes/g001.svg",
"./assets/heroes/g002.svg",
"./assets/heroes/g003.svg",
"./assets/heroes/g004.svg",
"./assets/heroes/g005.svg",
"./assets/heroes/g006.svg",
"./assets/heroes/g007.svg",
"./assets/heroes/g008.svg"];
const IMAGE_HOSTS=new Set(['www.jp.square-enix.com','kyokugen.info','cdn-ak.f.st-hatena.com','blog-imgs-161.fc2.com','stat.ameba.jp','assets.st-note.com','jp.samurai-gamers.com']);
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
async function migrateOldImages(){
 const names=await caches.keys(),destination=await caches.open(IMG_KEY);
 for(const name of names){
  if(!name.startsWith('minstrel-ps2-')||name===KEY||name===IMG_KEY)continue;
  const old=await caches.open(name);
  for(const req of await old.keys()){
   if(new URL(req.url).origin===self.location.origin||await destination.match(req))continue;
   const response=await old.match(req);
   if(response)try{await destination.put(req,response)}catch(e){}
  }
  await caches.delete(name);
 }
}
self.addEventListener('activate',e=>e.waitUntil((async()=>{await migrateOldImages();await self.clients.claim()})()));
async function saveOfflineImages(urls,port){
 const imageCache=await caches.open(IMG_KEY),safe=[...new Set(urls.filter(v=>typeof v==='string'&&v.startsWith('https://')&&(()=>{try{return IMAGE_HOSTS.has(new URL(v).hostname)}catch(e){return false}})()))].slice(0,350);
 let index=0,done=0,success=0,failed=[];
 async function saveOne(url){
  if(await imageCache.match(url))return true;
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),12000);
  try{
   const response=await fetch(new Request(url,{mode:'no-cors',credentials:'omit',referrerPolicy:'no-referrer',cache:'reload',signal:controller.signal}));
   if(!response.ok&&response.type!=='opaque')return false;
   await imageCache.put(url,response.clone());
   return true;
  }catch(err){return false}finally{clearTimeout(timer)}
 }
 const workers=Array.from({length:3},async()=>{while(index<safe.length){
  const url=safe[index++],ok=await saveOne(url);done++;if(ok)success++;else failed.push(url);
  if(done%2===0||done===safe.length)port?.postMessage({type:'IMAGE_PROGRESS',done,total:safe.length,success,failed:failed.length});
 }});
 await Promise.all(workers);
 port?.postMessage({type:'IMAGE_COMPLETE',done,total:safe.length,success,failedUrls:failed});
}
self.addEventListener('message',e=>{
 const type=e.data?.type,port=e.ports?.[0];
 if(type==='CACHE_GUIDE'){e.waitUntil(preload().then(n=>port?.postMessage({ok:true,count:n})).catch(err=>port?.postMessage({ok:false,error:err.message})));return}
 if(type==='CACHE_IMAGES')e.waitUntil(saveOfflineImages(Array.isArray(e.data?.urls)?e.data.urls:[],port).catch(err=>port?.postMessage({type:'IMAGE_ERROR',error:err.message})));
});
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 const url=new URL(e.request.url),site=new URL('./',self.location.href);
 if(url.origin!==self.location.origin){
  if(e.request.destination!=='image'||url.protocol!=='https:'||!IMAGE_HOSTS.has(url.hostname))return;
  e.respondWith((async()=>{
   const cache=await caches.open(IMG_KEY),saved=await cache.match(url.href);
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
