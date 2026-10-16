"""Regression checks: 2005 PS2 v0.4.4 beginner guide, map labels and offline search."""
from pathlib import Path
import json,re,subprocess,time
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent
D=json.loads((root/'data.json').read_text(encoding='utf-8'))
html=(root/'index.html').read_text(encoding='utf-8')
match=re.search(r'<script id="guide-data" type="application/json">(.*?)</script>',html,re.S)
assert match and json.loads(match.group(1))==D
assert D['version'].startswith('0.4.5'),D['version']
assert len([r for r in D['records'] if r['section']=='新手'])==20
assert len({s['url'] for s in D['sources']})==len(D['sources'])
sourceids={s['id'] for s in D['sources']}
assert all(set(r['sources'])<=sourceids for r in D['records'])
assert '非遊戲地形地圖' in html and '區域索引' in html
assert not re.search(r'<script[^>]*src=|https?://[^" ]+\.js',html[:8000])
assert (root/'assets/ps2-original-cover.webp').is_file()
assert json.loads((root/'manifest.webmanifest').read_text(encoding='utf-8'))['display']=='standalone'
for name,size in [('icon-192.png',192),('icon-512.png',512),('apple-touch-icon.png',180)]:
 with Image.open(root/'assets'/name) as im: assert im.size==(size,size),(name,im.size)
print('Original PS2 data, 20 beginner tips, cover, aliases: PASS')
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
   assert str(len(D['records'])) in page.locator('#count').inner_text()
   assert page.locator('a[href^="http"]').count()==0
   page.get_by_role('button',name='新手',exact=True).click()
   assert '新手' in page.locator('#cards').inner_text()
   assert '先選主角' in page.locator('#cards').inner_text()
   page.locator('#search').fill('チェーンバトル')
   assert '連鎖戰不能中途逃跑' in page.locator('#cards').inner_text()
   page.locator('#search').fill('フロンティア不存在')
   assert '找到 0 筆' in page.locator('#count').inner_text()
   page.locator('#search').fill('')
   page.locator('#saveOffline').click()
   page.wait_for_function("document.querySelector('#offlineStatus').textContent.includes('已儲存')",timeout=45000)
   ctx.set_offline(True)
   page.reload(wait_until='domcontentloaded')
   page.get_by_role('button',name='新手',exact=True).click()
   page.locator('#search').fill('クイックセーブ')
   assert '遊戲不會自動替 PS2 存檔' in page.locator('#cards').inner_text()
   page.get_by_role('button',name='迷宮',exact=True).click()
   page.locator('#search').fill('水竜の神殿')
   assert '水龍神殿' in page.locator('#cards').inner_text()
   img=page.locator('.guide-diagram img').first
   img.scroll_into_view_if_needed()
   page.wait_for_function("document.querySelector('.guide-diagram img')?.complete && document.querySelector('.guide-diagram img')?.naturalWidth>0",timeout=10000)
   assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
   assert not errors,errors
   print('OFFLINE beginner & PS2 dungeon diagram: PASS',width,height)
   ctx.close()
  b.close()
finally:
 server.terminate();server.wait()
print('PASS ALL')