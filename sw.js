/* 2005 PS2 guide, offline installation v0.4.6. */
const KEY='minstrel-ps2-2005-v0.4.6';
const FILES=["./","./index.html","./data.json","./manifest.webmanifest","./assets/ps2-original-cover.webp","./assets/icon-192.png","./assets/icon-512.png","./assets/apple-touch-icon.png","./assets/floorplans/bafal_bayer.svg","./assets/floorplans/bafal_elizabeth.svg","./assets/floorplans/bafal_forest.svg","./assets/floorplans/bafal_forest_dark.svg","./assets/floorplans/bafal_gold.svg","./assets/floorplans/bafal_great.svg","./assets/floorplans/bafal_loban.svg","./assets/floorplans/bafal_melville.svg","./assets/floorplans/drylands_desert.svg","./assets/floorplans/drylands_galessa.svg","./assets/floorplans/drylands_nieca.svg","./assets/floorplans/drylands_oldcastle.svg","./assets/floorplans/etc_faerie.svg","./assets/floorplans/etc_last.svg","./assets/floorplans/etc_mummy.svg","./assets/floorplans/etc_purgatory.svg","./assets/floorplans/etc_sherah.svg","./assets/floorplans/etc_ukkom.svg","./assets/floorplans/final-trial.svg","./assets/floorplans/frontier_jewelbeast.svg","./assets/floorplans/frontier_newroad.svg","./assets/floorplans/frontier_saoki.svg","./assets/floorplans/frontier_vampire.svg","./assets/floorplans/frontier_yassi.svg","./assets/floorplans/kjaragt_assassin.svg","./assets/floorplans/kjaragt_estamir.svg","./assets/floorplans/kjaragt_tarmitta.svg","./assets/floorplans/knight_abandoned.svg","./assets/floorplans/knight_constanzu.svg","./assets/floorplans/knight_dragon.svg","./assets/floorplans/knight_mirsaburg.svg","./assets/floorplans/knight_paganruins.svg","./assets/floorplans/ligau_dinosaurs.svg","./assets/floorplans/ligau_plain.svg","./assets/floorplans/ligau_tomae.svg","./assets/floorplans/ligau_treasure.svg","./assets/floorplans/rosalia_crystal.svg","./assets/floorplans/rosalia_evil.svg","./assets/floorplans/rosalia_isthmus.svg","./assets/floorplans/rosalia_isthmus_castle.svg","./assets/floorplans/rosalia_scurve.svg","./assets/floorplans/twin-moons.svg","./assets/floorplans/underworld.svg","./assets/floorplans/valhalland_east.svg","./assets/floorplans/valhalland_field.svg","./assets/floorplans/valhalland_frozen.svg","./assets/floorplans/valhalland_south.svg","./assets/floorplans/valhalland_south2.svg","./assets/floorplans/valhalland_south3.svg","./assets/floorplans/valhalland_west.svg","./assets/floorplans/walon_gueccoes.svg","./assets/floorplans/walon_jungle.svg","./assets/floorplans/walon_silver.svg","./assets/floorplans/water-dragon.svg","./assets/heroes/g001.svg","./assets/heroes/g002.svg","./assets/heroes/g003.svg","./assets/heroes/g004.svg","./assets/heroes/g005.svg","./assets/heroes/g006.svg","./assets/heroes/g007.svg","./assets/heroes/g008.svg","./assets/equipment/g105.svg","./assets/equipment/g106.svg","./assets/equipment/g107.svg","./assets/equipment/g108.svg","./assets/equipment/g109.svg","./assets/equipment/g110.svg","./assets/equipment/g111.svg","./assets/equipment/g112.svg","./assets/equipment/g113.svg","./assets/atlas/map-01.svg","./assets/atlas/map-02.svg","./assets/atlas/map-03.svg","./assets/atlas/map-04.svg","./assets/atlas/map-05.svg","./assets/atlas/map-06.svg","./assets/atlas/map-07.svg","./assets/atlas/map-08.svg","./assets/atlas/map-09.svg","./assets/atlas/map-10.svg","./assets/atlas/map-11.svg"];
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