"""v0.5.0 quality gates: original source imagery, full hero routes, offline text, responsive viewer."""
from pathlib import Path
import json, re, subprocess, time
from urllib.parse import urlparse
from PIL import Image
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent.parent
D=json.loads((root/'data.json').read_text(encoding='utf-8'))
html=(root/'index.html').read_text(encoding='utf-8')
sw=(root/'sw.js').read_text(encoding='utf-8')
match=re.search(r'<script id="guide-data" type="application/json">(.*?)</script>',html,re.S)
assert match and json.loads(match.group(1))==D, "Embedded JSON differs from data.json"
assert D['version'].startswith('0.5.0'),D['version']
assert 'minstrel-ps2-2005-v0.5.0' in sw and 'minstrel-ps2-2005-v0.5.0' in html
recs=D['records']
heroes=[r for r in recs if r['section']=='主角']
regions=[r for r in recs if r['section']=='地圖']
dungeons=[r for r in recs if r['section']=='迷宮' and r.get('gallery')]
gear=[r for r in recs if r['section']=='資料庫' and re.fullmatch(r'G1(?:0[5-9]|1[0-3])',r['id'])]
assert len(heroes)==8 and all(len(r['steps'])>=9 for r in heroes)
assert all(r['gallery'][0]['src'].endswith('_chara.png') and r['gallery'][1]['src'].endswith('_img.jpg') for r in heroes)
assert all(len(r.get('heroChapters',[]))==5 for r in heroes)
assert all(all('ids' in chapter and chapter['ids'] for chapter in r['heroChapters']) for r in heroes)
assert all('square-enix.com' in r['heroSource'] for r in heroes)
assert len(regions)==11 and all(r['gallery'][0]['src']=='https://kyokugen.info/minsaga/pic/13853.jpg' for r in regions)
assert len(dungeons)==52, len(dungeons)
assert len([r for r in recs if r['section']=='地點'])==22
assert all(len(r.get('regionNodes',[]))>0 for r in regions)
assert 'offline.html' not in sw
assert 'offline.html' not in html
assert all(r['gallery'][0]['src'].startswith('https://kyokugen.info/minsaga/map/') and r['gallery'][0]['src'].endswith('.jpeg') for r in dungeons)
assert all(r.get('mapSourceUrl','').startswith('https://kyokugen.info/minsaga/') for r in dungeons)
assert len(gear)==9
assert len([r for r in gear if r.get('equipmentPhotoSource') and r.get('gallery')])==6
assert len([r for r in gear if not r.get('gallery')])==3
assert len([r for r in recs if r['section']=='迷宮' and r.get('landmarks')])>=30
assert len([r for r in recs if r.get('imageHotspots')])==3
assert 'IMAGE_HOSTS' in sw and 'e.request.destination' in sw
assert 'saveImages()' in html and 'imageCoverage()' in html
assert not any(g['src'].endswith('.svg') for r in heroes+regions+dungeons+gear for g in r.get('gallery',[]))
assert len({s['url'] for s in D['sources']})==len(D['sources'])
sourceids={s['id'] for s in D['sources']}
assert all(set(r['sources'])<=sourceids for r in recs)
assert len([r for r in recs if r['section']=='新手'])==20
assert len([r for r in recs if r['section']=='打法'])>=7
for name,size in [('icon-192.png',192),('icon-512.png',512),('apple-touch-icon.png',180)]:
 with Image.open(root/'assets'/name) as im: assert im.size==(size,size)
assert (root/'assets/ps2-original-cover.webp').is_file()
assert json.loads((root/'manifest.webmanifest').read_text(encoding='utf-8'))['display']=='standalone'
print('DATA original official portraits and game screenshots, six real equipment menus, original maps, chapter navigator, floor loot index: PASS')

server=subprocess.Popen(['python','-m','http.server','8765','--bind','127.0.0.1','--directory',str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 time.sleep(2)
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,args=['--no-sandbox'])
  for width,height in [(1366,768),(390,844),(844,390)]:
   ctx=b.new_context(viewport={'width':width,'height':height},service_workers='allow')
   page=ctx.new_page();errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('http://127.0.0.1:8765/',wait_until='domcontentloaded')
   page.wait_for_function('navigator.serviceWorker.controller !== null',timeout=45000)
   assert str(len(recs)) in page.locator('#count').inner_text()
   page.get_by_role('button',name='新手',exact=True).click()
   page.locator('#search').fill('チェーンバトル')
   assert '連鎖戰不能中途逃跑' in page.locator('#cards').inner_text()
   page.locator('#search').fill('')
   page.get_by_role('button',name='主角',exact=True).click()
   page.locator('#search').fill('アルベルト')
   assert page.locator('.hero-art img').count()==1
   assert page.locator('.hero-art img').get_attribute('src').endswith('_chara.png')
   assert page.locator('.hero-game img').count()==1
   assert page.locator('.hero-chapters .chapter').count()==5
   assert page.locator('.hero-art .map-open').count()==1
   assert page.locator('.hero-game .map-open').count()==1
   assert page.locator('.quest-jump').count()>15
   assert page.locator('.hero-card .guide-flow li').count()>=9
   assert '城陷落' in page.locator('#cards').inner_text()
   page.locator('.quest-jump[data-jump="G009"]').first.click()
   assert '開拓村誘拐事件' in page.locator('#cards').inner_text()
   page.get_by_role('button',name='裝備資料',exact=True).click()
   page.locator('#search').fill('レフトハンドソード')
   assert page.locator('.gear-no-photo').count()==1
   assert page.locator('.equip-gallery img').count()==0
   page.locator('#search').fill('竜鱗の剣')
   assert page.locator('.equip-gallery img').count()==1
   assert page.locator('.equip-gallery .map-open').count()==1
   page.locator('.equip-gallery .map-open').click()
   assert page.locator('#mapRaw').get_attribute('href').startswith('https://')
   page.locator('#mapContrast').click()
   assert 'contrast(1.65)' in page.locator('#mapZoomImg').get_attribute('style')
   page.locator('#mapClose').click()
   page.get_by_role('button',name='區域索引',exact=True).click()
   page.locator('#search').fill('フロンティア')
   assert page.locator('.region-card').count()>=1
   assert 'https://kyokugen.info/minsaga/pic/13853.jpg' in page.locator('.region-card .guide-diagram img').first.get_attribute('src')
   page.locator('.map-open').first.click()
   assert page.locator('#mapDialog').evaluate('(x)=>x.open')
   page.locator('#zoomIn').click()
   assert int(page.locator('#zoomLabel').inner_text().strip('%')) >= (375 if width<700 else 180)
   page.locator('#mapClose').click()
   assert not page.locator('#mapDialog').evaluate('(x)=>x.open')
   page.get_by_role('button',name='區域索引',exact=True).click()
   page.locator('#search').fill('バファル')
   assert page.locator('.region-card .region-nodes').count()==1
   assert page.locator('.region-card .place-jump').count()>=8
   page.locator('.region-card .place-jump[data-jump="LOC-07-01"]').click()
   assert page.locator('.place-card').count()>=1
   assert 'メルビル' in page.locator('.place-card').inner_text()
   assert '真實遊戲地圖' in page.locator('.place-card').inner_text()
   page.get_by_role('button',name='迷宮',exact=True).click()
   page.locator('#search').fill('財宝の穴')
   assert page.locator('.dungeon-card .image-pin').count()>=1
   page.locator('.dungeon-card .image-pin').first.click()
   assert 'さびた古刀' in page.locator('.dungeon-card .hotspot-explain').inner_text()
   page.locator('.dungeon-card .map-open').first.click()
   assert page.locator('#mapPins .image-pin').count()>=1
   page.locator('#mapPins .image-pin').first.click()
   assert 'さびた古刀' in page.locator('#mapPinDetail').inner_text()
   page.locator('#mapClose').click()
   page.locator('#search').fill('')
   # Base assets must be present before the network is disabled.
   # Third-party image CDN responses are not mocked: synthetic images are prohibited by project policy.
   assert page.locator('a[download][href="./offline.html"]').count()==0
   assert page.evaluate('window.IMAGE_URLS===undefined')
   cache_count=page.evaluate("""async () => {
       const c=await caches.open('minstrel-ps2-2005-v0.5.0');
       return (await Promise.all([
           c.match('./index.html'),c.match('./data.json'),c.match('./assets/icon-192.png')
       ])).filter(Boolean).length
   }""")
   assert cache_count==3,cache_count
   # Confirm a real original map is renderable and cached when upstream access is available.
   page.locator('#search').fill('水竜の神殿')
   image_ready=False
   try:
    page.wait_for_function("document.querySelector('.dungeon-card .guide-diagram img')?.naturalWidth>0",timeout=20000)
    image_ready=True
   except Exception as ex:
    print('UPSTREAM ORIGINAL MAP UNAVAILABLE; no offline image guarantee:',str(ex)[:160])
   page.locator('#search').fill('')
   ctx.set_offline(True)
   page.reload(wait_until='domcontentloaded')
   page.get_by_role('button',name='新手',exact=True).click()
   page.locator('#search').fill('クイックセーブ')
   assert '遊戲不會自動替 PS2 存檔' in page.locator('#cards').inner_text()
   page.get_by_role('button',name='迷宮',exact=True).click()
   page.locator('#search').fill('水竜の神殿')
   assert '水龍神殿' in page.locator('#cards').inner_text()
   assert '瀑布' in page.locator('#cards').inner_text()
   assert page.locator('.dungeon-card .marker-legend').count()>=1
   assert page.locator('.dungeon-card .landmark-row').count()>=8
   # Actual original images may be blocked by their original host. Check offline only if online was confirmed.
   if image_ready:
    page.wait_for_function("document.querySelector('.dungeon-card .guide-diagram img')?.naturalWidth>0",timeout=12000)
    print('REAL ORIGINAL MAP OFFLINE-DECODE: PASS',width,height)
   assert page.locator('.source-photo-link').count()>=1
   page.locator('.dungeon-card .map-open').first.click()
   assert page.locator('#mapDialog').evaluate('(x)=>x.open')
   page.locator('#zoomIn').click()
   assert int(page.locator('#zoomLabel').inner_text().strip('%')) >= (375 if width<700 else 180)
   page.locator('#mapClose').click()
   assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
   assert not errors,errors
   print('OFFLINE text + zoom controls + mobile/desktop responsive: PASS',width,height)
   ctx.close()
  b.close()
finally:
 server.terminate();server.wait()
print('PASS ALL (PWA text/offline search + 22 detailed town pages; original images require host cache)')
