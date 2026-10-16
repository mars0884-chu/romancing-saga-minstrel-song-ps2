"""Privately catalog historic PS2 map rasters for factual geometry comparison. Do NOT publish originals."""
from urllib.parse import urljoin, urlparse
import requests, bs4, time, os, json, re
from pathlib import Path
from PIL import Image
from io import BytesIO
BASE='https://kyokugen.info/minsaga/'
out=Path('source-study-all');out.mkdir(exist_ok=True)
s=requests.Session();s.headers.update({'User-Agent':'Mozilla/5.0 (guide compatibility research)'})
html_pages={}
fronts=['minstrel_map_00.html']+[f'minstrel_map_{x}.html' for x in range(1,12)]
queue=list(fronts);seen=set()
while queue and len(seen)<100:
    path=queue.pop(0)
    if path in seen:continue
    seen.add(path)
    try:
        response=s.get(urljoin(BASE,path),timeout=20)
        response.raise_for_status()
        soup=bs4.BeautifulSoup(response.content,'html.parser')
        html_pages[path]=soup
        for a in soup.select('a[href]'):
            href=a['href'].split('?')[0]
            basename=os.path.basename(href)
            if re.fullmatch(r'minstrel_map_\d{1,2}_\d{2}\.html',basename) and basename not in seen:
                queue.append(basename)
        print('PAGE OK',path)
    except Exception as exc:print('PAGE FAILED',path,str(exc)[:100])
    time.sleep(.13)
print('PAGES',len(html_pages))
images={}
for path,soup in html_pages.items():
    for tag in soup.select('img[src], a[href]'):
        url=tag.get('src') if tag.name=='img' else tag.get('href')
        url=urljoin(urljoin(BASE,path),url)
        pu=urlparse(url)
        if pu.hostname not in ('kyokugen.info','www.kyokugen.info'): continue
        if '/minsaga/map/' not in pu.path: continue
        if not re.search(r'\.(?:jpe?g|png|gif)$',pu.path,re.I):continue
        images.setdefault(url,[]).append(path)
print('IMAGE URLS',len(images))
manifest=[]
for i,(url,referers) in enumerate(images.items()):
    try:
        response=s.get(url,timeout=25);response.raise_for_status()
        if len(response.content)>3_000_000:continue
        with Image.open(BytesIO(response.content)) as im:
            n=f'{i:03d}-{os.path.basename(urlparse(url).path)}'
            target=out/n;target.write_bytes(response.content)
            m={'name':n,'url':url,'referers':list(set(referers)),'width':im.width,'height':im.height,'bytes':len(response.content)}
            manifest.append(m)
            print('IMAGE OK',i,im.size,n)
    except Exception as exc:print('IMAGE FAILED',i,url,str(exc)[:130])
    time.sleep(.13)
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',len(manifest),'images, total bytes',sum(x['bytes'] for x in manifest))