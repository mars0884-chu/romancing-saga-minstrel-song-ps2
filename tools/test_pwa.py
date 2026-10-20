"""PWA v0.9.8 靜態資料、搜尋、返回、地圖放大、桌機/手機與離線文字驗收。"""
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
assert d['version'].startswith('0.9.7') and 'minstrel-ps2-2005-v0.9.8' in html and 'minstrel-ps2-2005-v0.9.8' in sw
R=d['records'];ids={r['id'] for r in R};sourceids={r['id'] for r in d['sources']}
assert len(R)>=279
assert len(d['sources'])>=350
assert len(d['sources'])>=357
mine=next(r for r in R if r['id']=='G028')
vault=next(r for r in R if r['id']=='G011')
uhanji=next(r for r in R if r['id']=='G013')
assert len(mine.get('floorMaps', [])) == 5 and len({x['src'] for x in mine['floorMaps']}) == 5
assert all(x['sourcePage'].endswith('/rsmsr-event18/') for x in mine['floorMaps'])
assert any('ゴールドドラゴン' in step and '不意打ち' in step for step in mine['steps'])
assert any('30000金' in step for step in mine['steps'])
assert any('15～' in step and '30％' in step for step in vault['steps'])
assert any('未決' in step and '贓物' in step for step in vault['steps'])
assert any('ウハンジ' in step and '水竜の神殿' in step for step in uhanji['steps'])
assert any('やばい仕事大好き！' in step for step in uhanji['steps'])

assert all((root/'docs'/name).exists() for name in ('DEVELOPMENT_LOG.md','MAINTENANCE_GUIDE.md','RESTART_PROMPT.md','RECOVERY_CHECKPOINT_2026-10-19.md')), 'GitHub handoff documents missing'
melville=next(r for r in R if r['id']=='G029')
assert len(melville.get('floorMaps',[]))==2 and len({x['src'] for x in melville['floorMaps']})==2
assert any('ブチ破る！' in step for step in melville['steps'])
assert any('大空飛竜' in step and '暴風' in step for step in melville['steps'])
assert any('オキナスのバンダナ' in step for step in melville['steps'])
assert any('ワナ解除' in step and 'Lv4' in step for step in next(r for r in R if r['id']=='D-07-02')['steps'])
assert all(id in sourceids for id in melville['sources']), 'Missing source evidence for raid'
assert not (root/'offline-guide.zip').exists(), 'ZIP is not the delivery path'

# No arbitrary five-step completion metric: check end-to-end mechanics and real-source floor maps.
jewel=next(r for r in R if r['id']=='G027')
assert len(jewel.get('floorMaps',[]))==4 and any('石化獣' in step for step in jewel['steps'])
assert len({m['src'] for m in jewel['floorMaps']})==4
assert all(m['src'].startswith('https://jp.samurai-gamers.com/wp-content/uploads/') and m['sourcePage'].startswith('https://jp.samurai-gamers.com/') for m in jewel['floorMaps'])
assert any('ジュエルブラスター' in text for text in jewel['steps'])
assert any('98' in text and 'オブシダンソード' in text for text in next(r for r in R if r['id']=='G083')['steps'])
assert any('ジャンプLv3' in text for text in next(r for r in R if r['id']=='G103')['steps'])

assert any("ゾディアック" in step for step in next(r for r in R if r['id']=='G019')['steps']) and any("ムーンストーン" in step for step in next(r for r in R if r['id']=='G019')['steps']), 'missing substantive quest detail: G019'
assert any("一角蝶" in step for step in next(r for r in R if r['id']=='G014')['steps']) and any("ジャンプ" in step for step in next(r for r in R if r['id']=='G014')['steps']), 'missing substantive quest detail: G014'
assert any("冥府" in step for step in next(r for r in R if r['id']=='G046')['steps']) and any("オールドキャッスル" in step for step in next(r for r in R if r['id']=='G046')['steps']), 'missing substantive quest detail: G046'
assert any("トパーズ" in step for step in next(r for r in R if r['id']=='G089')['steps']) and any("バガー" in step for step in next(r for r in R if r['id']=='G089')['steps']), 'missing substantive quest detail: G089'
assert 'runOfflineSync(false)' in html, 'PWA must start image cache automatically'
assert 'minstrel-ps2-2005-v0.9.8-local-maps4' in sw and 'minstrel-ps2-2005-v0.9.8-local-maps4' in html
assert any("ムクロペンダント" in step for step in next(r for r in R if r['id']=='G016')['steps']), 'missing substantive quest detail: G016'
assert any("クローディア" in step for step in next(r for r in R if r['id']=='G017')['steps']), 'missing substantive quest detail: G017'
assert any("アムト" in step for step in next(r for r in R if r['id']=='G084')['steps']), 'missing substantive quest detail: G084'
assert all('迷いの森_%' not in x.get('src','') and '_%E6%98%BC' not in x.get('src','') and '_%E5%A4%9C' not in x.get('src','') for r in R for x in r.get('floorMaps',[]))
assert 'actual-pixels' in html
assert 'related-guides' in html
assert any("アイスソード" in step for step in next(r for r in R if r['id']=='G033')['steps']), 'missing substantive quest detail: G033'
assert any("あまぐもの腕輪" in step for step in next(r for r in R if r['id']=='G074')['steps']), 'missing substantive quest detail: G074'
assert 'QUEST-NEVILLE-FULL' in next(r for r in R if r['id']=='G015').get('relatedIds',[])
assert any("ミイラ" in step for step in next(r for r in R if r['id']=='G096')['steps']), 'missing substantive quest detail: G096'
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
   # Open PWA directly while disconnected; source-backed Melville maps and search remain available as metadata.
   page.get_by_role('button',name='任務',exact=True).click()
   page.locator('#search').fill('メルビル襲撃計画')
   assert 'ブチ破る！' in page.locator('#cards').inner_text()
   assert page.locator('.floor-fig').count()>=2, 'Melville dungeon maps lost offline'
   page.get_by_role('button',name='迷宮',exact=True).click()
   page.locator('#search').fill('最終試練')

   assert page.locator('.floor-fig').count()==4
   # Verify genuine same-origin image bytes can be read without network, not just visible remote thumbnails.
   local_images=['assets/floorplans/final-trial.svg','assets/atlas/map-01.svg','assets/heroes/g001.svg','assets/equipment/g105.svg']
   for image_path in local_images:
    result=page.evaluate("""async p=>{const r=await fetch(p);return {ok:r.ok,bytes:(await r.text()).length}}""",image_path)
    assert result['ok'] and result['bytes']>100, f'offline local image failure: {image_path}: {result}'
   image_cache_count=page.evaluate("""async()=>{const k=(await caches.keys()).find(n=>n.includes('local-maps4'));return k?(await (await caches.open(k)).keys()).length:0}""")
   assert image_cache_count>=111,f'Expected 103 local graphics plus guide assets in offline cache; got {image_cache_count}'
   # Check Japanese search and floor panels are available offline without ZIP and without a save button.
   page.get_by_role('button',name='任務',exact=True).click()
   page.locator('#search').fill('ジュエルビースト')
   assert page.locator('#cards .item').count()>0
   assert 'ラミア' in page.locator('#cards').inner_text()
   assert page.locator('.floor-fig').count()>=4, 'Four source-backed Jewel Beast maps missing from offline UI'
   page.get_by_role('button',name='任務',exact=True).click()
   page.locator('#search').fill('鉱山襲撃')
   assert 'ゴールドドラゴン' in page.locator('#cards').inner_text()
   assert page.locator('.floor-fig').count() >= 5, 'Late mine genuine game maps not visible while offline'
   page.locator('#search').fill('ウハンジの秘密')
   assert '水竜の神殿' in page.locator('#cards').inner_text()
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+1')
   assert not errors,errors
   print('PWA responsive + back + zoom + offline searchable guide: PASS',width,height)
   ctx.close()
  browser.close()
finally:
 server.terminate();server.wait(timeout=10)
print('PASS: Offline TEXT tested; third-party IMAGE offline depends on external host, browser storage, and true offline validation')
