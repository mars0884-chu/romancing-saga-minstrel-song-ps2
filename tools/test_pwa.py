"""PWA v0.9.4 靜態資料、搜尋、返回、地圖放大、桌機/手機與離線文字驗收。"""
from pathlib import Path
import json,re,subprocess,time
from playwright.sync_api import sync_playwright
from PIL import Image

root=Path(__file__).resolve().parent.parent
d=json.loads((root/'data.json').read_text(encoding='utf-8'))
html=(root/'index.html').read_text(encoding='utf-8')
sw=(root/'sw.js').read_text(encoding='utf-8')
m=re.search(r'<script id="guide-data" type="application/json">(.*?)</script>',html,re.S)
assert m and json.loads(m.group(1))==d,"首頁資料與data.json不一致"
assert d['version'].startswith('0.9.4') and 'minstrel-ps2-2005-v0.9.4' in html and 'minstrel-ps2-2005-v0.9.4' in sw
R=d['records'];ids={r['id'] for r in R};sourceids={r['id'] for r in d['sources']}
assert len(R)>=276
assert len(next(r for r in R if r['id']=='G016')['steps'])>=9
assert len(next(r for r in R if r['id']=='G017')['steps'])>=8
assert len(next(r for r in R if r['id']=='G084')['steps'])>=12
assert all('迷いの森_%' not in x.get('src','') and '_%E6%98%BC' not in x.get('src','') and '_%E5%A4%9C' not in x.get('src','') for r in R for x in r.get('floorMaps',[]))
assert 'actual-pixels' in html
assert 'related-guides' in html
assert 'QUEST-NEVILLE-FULL' in next(r for r in R if r['id']=='G015').get('relatedIds',[])
assert len(next(r for r in R if r['id']=='G096')['steps'])>=7
assert 'id="offlineMissing"' in html
assert 'updateMissingImages' in html and len(ids)==len(R)
assert all(set(r.get('sources',[]))<=sourceids for r in R)
assert len([r for r in R if r['section']=='地圖'])==11
assert len([r for r in R if r['section']=='地點'])==22
assert len([r for r in R if r['section']=='同伴' and r['id'].startswith('RS-')])==5
assert len([r for r in R if r['id']=='D-03-02'][0]['floorMaps'])==11
assert len([r for r in R if r['id']=='D-04-03'][0]['floorMaps'])==5
assert len([r for r in R if r['id']=='D-05-01'][0]['floorMaps'])==2
assert len([r for r in R if r['id'].startswith('D-')])==53
assert len([r for r in R if r['section']=='主角' and r['id'].startswith('G00')])==8
assert sum(len(r.get('floorMaps',[])) for r in R) >=64
assert len([r for r in R if r['id']=='D-04-04'][0]['floorMaps'])==4
assert len([r for r in R if r['id']=='D-09-04'][0]['floorMaps'])==25
for name,expected in [('icon-192.png',192),('icon-512.png',512),('apple-touch-icon.png',180)]:
 with Image.open(root/'assets'/name) as im:assert im.size==(expected,expected)
assert 'offline.html' not in html and 'offline.html' not in sw
print('STATIC complete guide/data sync, official icons, 60+ real floor panels: PASS')

server=subprocess.Popen(['python','-m','http.server','8765','--bind','127.0.0.1','--directory',str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 time.sleep(2)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
  for width,height in [(1366,768),(390,844),(844,390)]:
   ctx=browser.new_context(viewport={'width':width,'height':height},service_workers='allow')
   page=ctx.new_page();errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto('http://127.0.0.1:8765/',wait_until='domcontentloaded')
   page.wait_for_function('navigator.serviceWorker.controller !== null',timeout=45000)
   assert page.locator('#cards .item').count()>0
   page.get_by_role('button',name='區域索引',exact=True).click()
   page.locator('#search').fill('バファル')
   assert page.locator('.region-card .place-jump').count()>0
   page.locator('.region-card .place-jump').first.click()
   assert page.locator('#backToList').count()==1
   assert page.locator('#backToAll').count()==1
   page.locator('#backToList').click()
   page.wait_for_timeout(300)
   assert page.locator('.region-card').count()>0, '上一層返回失敗'
   page.get_by_role('button',name='任務',exact=True).click()
   page.locator('#search').fill('ネビルの依頼')
   assert page.locator('[data-jump="QUEST-NEVILLE-FULL"]').count()>=1
   page.locator('[data-jump="QUEST-NEVILLE-FULL"]').first.click()
   assert page.locator('#backToList').count()==1
   page.locator('#backToList').click()
   page.wait_for_timeout(300)
   page.get_by_role('button',name='同伴',exact=True).click()
   page.locator('#search').fill('モニカ')
   assert '東の風、雨' in page.locator('#cards').inner_text()
   page.get_by_role('button',name='迷宮',exact=True).click()
   page.locator('#search').fill('最終試練')
   assert page.locator('.floor-fig').count()==4
   page.locator('.floor-fig .map-open').first.click()
   assert page.locator('#mapDialog').evaluate('(d)=>d.open')
   page.locator('#zoomIn').click()
   assert int(page.locator('#zoomLabel').inner_text().replace('%',''))>=200
   page.locator('#mapClose').click()
   page.locator('#search').fill('') 
   ctx.set_offline(True)
   page.reload(wait_until='domcontentloaded')
   page.get_by_role('button',name='迷宮',exact=True).click()
   page.locator('#search').fill('最終試練')
   assert 'オーガチャンピオン' in page.locator('#cards').inner_text()
   assert page.locator('.floor-fig').count()==4
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+1')
   assert not errors,errors
   print('PWA responsive + back + zoom + offline searchable guide: PASS',width,height)
   ctx.close()
  browser.close()
finally:
 server.terminate();server.wait(timeout=10)
print('PASS: Offline TEXT tested; third-party IMAGE offline depends on external host, browser storage, and true offline validation')
