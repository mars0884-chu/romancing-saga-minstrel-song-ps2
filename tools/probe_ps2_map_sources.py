"""Fetch historic map images for private source comparison; do not republish the scans."""
import urllib.request
from pathlib import Path
from PIL import Image
sources={
 'water-dragon':'https://kyokugen.info/minsaga/map/kjaragt_shuilung.jpeg',
 'twin-moons':'https://kyokugen.info/minsaga/map/walon_pyramid.jpeg',
 'underworld':'https://kyokugen.info/minsaga/map/ligau_netherworld.jpeg',
 'final-trial':'https://kyokugen.info/minsaga/map/drylands_elore.jpeg',
}
out=Path('source-study-only');out.mkdir(exist_ok=True)
for name,url in sources.items():
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as resp:
   data=resp.read()
  f=out/(name+'.jpg');f.write_bytes(data)
  with Image.open(f) as im:
   print('FETCH OK',name,'bytes',len(data),'dimensions',im.size)
   im.thumbnail((640,640))
   im.convert('RGB').save(out/(name+'-preview.png'))
 except Exception as exc:
  print('FETCH FAILED',name,type(exc).__name__,str(exc)[:180])
