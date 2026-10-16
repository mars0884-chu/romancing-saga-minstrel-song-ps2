"""Automated browser check: local guide must work with network disabled, without outbound links."""
import json, re, subprocess, time
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent.parent
D=json.loads((root/'data.json').read_text(encoding='utf-8'))
html=(root/'index.html').read_text(encoding='utf-8')
match=re.search(r'<script id="guide-data" type="application/json">(.*?)</script>',html,re.S)
assert match and json.loads(match.group(1))==D
assert D['version'].startswith('0.4.3')
assert not any(x['section']=='來源' for x in D['records'])
assert len({s['url'] for s in D['sources']})==len(D['sources'])
assert all(set(x['sources'])<=set(s['id'] for s in D['sources']) for x in D['records'])
assert not re.search(r'<script[^>]*src=|https?://[^" ]+\.js',html[:8000])
assert 'assets/ps2-original-cover.webp' in html
assert (root/'assets/ps2-original-cover.webp').is_file()
assert json.loads((root/'manifest.webmanifest').read_text())['display']=='standalone'
for name,size in [('icon-192.png',192),('icon-512.png',512),('apple-touch-icon.png',180)]:
 with Image.open(root/'assets'/name) as im: assert im.size==(size,size),(name,im.size)
print('JSON, cover, manifest, local-only links: PASS')
server=subprocess.Popen(['python','-m','http.server','8765','--bind','127.0.0.1','--directory',str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 time.sleep(2)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
  for width,height in [(1366,768),(390,844),(844,390)]:
   ctx=browser.new_context(viewport={'width':width,'height':height},service_workers='allow')
   page=ctx.new_page(); errors=[]
   page.on('pageerror',lambda err:errors.append(str(err)))
   page.goto('http://127.0.0.1:8765/',wait_until='domcontentloaded')
   page.wait_for_function('navigator.serviceWorker.controller !== null',timeout=30000)
   assert str(len(D['records'])) in page.locator('#count').inner_text()
   assert page.locator('a[href^="http"]').count()==0,'outbound guide links exist'
   page.locator('#search').fill('財宝の穴')
   assert '財寶洞穴' in page.locator('#cards').inner_text()
   assert 'B3' in page.locator('#cards').inner_text()
   assert page.locator('.guide-flow li').count() >= 1
   assert page.locator('.guide-diagram img').count() >= 1
   page.locator('#search').fill('XYZ不存在的測試值')
   assert '找到 0 筆' in page.locator('#count').inner_text()
   page.locator('#search').fill('')
   page.get_by_role('button',name='資料來源').click()
   assert page.locator('#sources a').count()==0
   page.get_by_role('button',name='迷宮',exact=True).click()
   page.locator('#search').fill('水竜の神殿')
   assert '水龍神殿' in page.locator('#cards').inner_text()
   assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
   page.locator('#search').fill('')
   page.locator('#saveOffline').click()
   page.wait_for_function("document.querySelector('#offlineStatus').textContent.includes('已儲存')",timeout=30000)
   ctx.set_offline(True)
   page.reload(wait_until='domcontentloaded')
   page.locator('#search').fill('アクアマリン')
   assert '水晶湖' in page.locator('#cards').inner_text() or '海藍寶石' in page.locator('#cards').inner_text()
   page.locator('#search').fill('水竜の神殿')
   img=page.locator('.guide-diagram img').first
   img.scroll_into_view_if_needed()
   page.wait_for_function("document.querySelector('.guide-diagram img')?.complete && document.querySelector('.guide-diagram img')?.naturalWidth>0",timeout=10000)
   assert not errors,errors
   print('OFFLINE reboot, native guide steps and no external links: PASS',width,height)
   ctx.close()
  browser.close()
finally:
 server.terminate();server.wait()
print('PASS ALL')