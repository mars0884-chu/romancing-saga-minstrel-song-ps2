"""Automated local HTTP & offline browser test, run by GitHub Actions."""
import json, re, subprocess, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent.parent
D=json.loads((root/'data.json').read_text(encoding='utf-8'))
text=(root/'index.html').read_text(encoding='utf-8')
m=re.search(r'<script type="application/json" id="dataset">(.*?)</script>',text,re.S)
assert m and json.loads(m.group(1))==D
assert len(D['records'])==218 and len(D['sources'])==128
assert len(set(s['url'] for s in D['sources']))==len(D['sources'])
assert all(set(r['sources']).issubset({x['id'] for x in D['sources']}) for r in D['records'])
assert '2022 年 Remastered 專屬' not in repr([r['title'] for r in D['records']])
manifest=json.loads((root/'manifest.webmanifest').read_text(encoding='utf-8'))
assert manifest['display']=='standalone'
assert manifest['icons'][0]['src']=='assets/icon-192.png'
from PIL import Image
for f,size in [('icon-192.png',192),('icon-512.png',512),('apple-touch-icon.png',180)]:
 with Image.open(root/'assets'/f) as image:
  assert image.size==(size,size)
print('Data integrity, icon sizes & PWA manifest: PASS')
proc=subprocess.Popen(['python','-m','http.server','8765','--bind','127.0.0.1','--directory',str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 time.sleep(2)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
  for width,height in [(1366,768),(390,844),(844,390)]:
   ctx=browser.new_context(viewport={'width':width,'height':height},service_workers='allow')
   page=ctx.new_page();errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
   page.goto('http://127.0.0.1:8765/',wait_until='domcontentloaded')
   page.wait_for_function("navigator.serviceWorker.controller !== null",timeout=30000)
   page.locator('#search').fill('財宝の穴')
   assert '財寶洞穴' in page.locator('#cards').inner_text()
   page.locator('#search').fill('不存在的遊戲隱藏詞測試XXXX')
   assert '0 筆' in page.locator('#resultCount').inner_text()
   page.locator('#search').fill('')
   assert not page.evaluate('document.documentElement.scrollWidth>window.innerWidth'),(width,height)
   assert not errors,errors
   # After SW precache, simulate connection loss without allowing HTTP fetch.
   if width==390:
    page.wait_for_timeout(600)
    ctx.set_offline(True)
    page.reload(wait_until='domcontentloaded')
    page.locator('#search').fill('トマエ火山')
    assert '托馬耶火山' in page.locator('#cards').inner_text()
    assert '離線' in page.locator('#offlineMode').inner_text()
    print('OFFLINE re-open + Japanese search: PASS')
   print(f'Viewport {width}x{height}, search, scroll, JS: PASS')
   ctx.close()
  browser.close()
finally:
 proc.terminate(); proc.wait()
print('PASS ALL')