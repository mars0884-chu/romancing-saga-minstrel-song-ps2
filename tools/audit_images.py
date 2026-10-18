"""Audit source image availability & original dimensions; never rehost or upload copyrighted images."""
import concurrent.futures as cf
import io,json,urllib.request,urllib.error
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image,UnidentifiedImageError
root=Path(__file__).resolve().parent.parent
data=json.loads((root/'data.json').read_text(encoding='utf-8'))
image_to_titles={}
for rec in data['records']:
 for item in (rec.get('gallery') or [])+(rec.get('floorMaps') or []):
  url=item.get('src','')
  if url.startswith('https://'):
   image_to_titles.setdefault(url,[]).append(rec.get('title',rec['id']))
def audit(pair):
 url,titles=pair
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; MinstrelSongPersonalGuideImageAudit/1.0)','Accept':'image/avif,image/webp,image/png,image/jpeg,image/*;q=0.8'})
  with urllib.request.urlopen(request,timeout=9) as response:
   code=response.getcode()
   kind=response.headers.get('Content-Type','')
   raw=response.read(8000001)
  if len(raw)>8000000:return {'url':url,'titles':titles,'status':'too_large','http':code}
  try:
   im=Image.open(io.BytesIO(raw))
   im.load();width,height=im.size
  except (UnidentifiedImageError,OSError):
   return {'url':url,'titles':titles,'status':'invalid_image','http':code,'content_type':kind}
  return {'url':url,'titles':titles,'status':'readable','http':code,'width':width,'height':height,'high_resolution':width>=1280 and height>=720,'content_type':kind}
 except urllib.error.HTTPError as e:
  return {'url':url,'titles':titles,'status':'http_error','http':e.code}
 except Exception as e:
  return {'url':url,'titles':titles,'status':'network_error','error':str(e)[:160]}
if __name__=='__main__':
 with cf.ThreadPoolExecutor(max_workers=4) as exe:
  rows=list(exe.map(audit,sorted(image_to_titles.items())))
 counts=Counter(x['status'] for x in rows)
 hi=sum(x.get('high_resolution',False) for x in rows)
 report={'tested_at_utc':datetime.now(timezone.utc).isoformat(),'note':'HTTP/Pillow audit from GitHub Actions, not iPhone Edge offline test and not image redistribution','total_unique':len(rows),'status_counts':dict(counts),'high_resolution_readable':hi,'items':rows}
 output=root/'image-audit.json'
 output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('IMAGE SOURCE AUDIT',len(rows),'unique images',dict(counts),'high-resolution',hi,flush=True)
 for item in rows:
  if item['status']!='readable':print('FAILED',item['status'],item.get('http'),item['url'],flush=True)
 print('REPORT image-audit.json',flush=True)
