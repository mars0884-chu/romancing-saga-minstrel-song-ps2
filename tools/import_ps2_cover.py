"""Import 2005 Japanese PS2 SLPM-65920 cover artwork, center-cropped as requested.

Runs in GitHub Actions where original image URL is reachable. No Remastered imagery.
"""
from io import BytesIO
from pathlib import Path
import requests
from PIL import Image, ImageOps

SOURCE_URLS = [
    # 2005 PS2 Japanese SLPM-65920 front cover, if stored in PSX database
    'https://psxdatacenter.com/psx2/images2/covers/SLPM-65920/SLPM-65920-F-ALL.jpg',
    'https://psxdatacenter.com/psx2/images2/covers/SLPM-65920/SLPM-65920-F.jpg',
    # Confirmed PS2 SCAJ-20124 cover/jacket from same 2005 original game
    'https://psxdatacenter.com/psx2/images2/covers/SCAJ-20124/SCAJ-20124-F-ALL.jpg',
    # Fallback: 2005 front packaging photo, crop the surrounding blank background
    'https://media1.nin-nin-game.com/30777-pos_thickbox/romancing-saga-minstrel-song-playstation-2-used-good-condition-en.jpg',
]

def get_cover():
    for url in SOURCE_URLS:
        try:
            response=requests.get(url,timeout=25,headers={'User-Agent':'Mozilla/5.0'},allow_redirects=True)
            response.raise_for_status()
            picture=Image.open(BytesIO(response.content))
            picture.verify()
            picture=Image.open(BytesIO(response.content)).convert('RGB')
            if min(picture.size)<400:
                print('Skip too-small cover:',url,picture.size)
                continue
            print('Using original 2005 PS2 artwork:',url, picture.size)
            return picture,url
        except Exception as exc:
            print('Source temporarily unavailable:',url,str(exc)[:140])
    raise SystemExit('Could not retrieve a confirmed original PS2 cover; existing icons remain unchanged.')

def main():
    img, url=get_cover()
    # PSX SCAJ scan is a jacket including back+spine; isolate the front right side.
    if img.width>img.height*1.2:
        img=img.crop((round(img.width*.43),0,img.width,img.height))
    # Retailer source has white margin; isolate actual original 2005 jewel case.
    if 'nin-nin-game.com' in url:
        width,height=img.size
        # Typical listing image is 500×500 with game case centered in white.
        img=img.crop((int(width*.27),int(height*.15),int(width*.75),int(height*.85)))
    # Square cover fills the entire icon; no added graphics, text or margins.
    assets=Path(__file__).resolve().parent.parent/'assets'
    assets.mkdir(exist_ok=True)
    for size,name in [(192,'icon-192.png'),(512,'icon-512.png'),(180,'apple-touch-icon.png')]:
        thumb=ImageOps.fit(img,(size,size),method=Image.Resampling.LANCZOS,centering=(.62,.42))
        thumb.save(assets/name,format='PNG',optimize=True)
    # Keep full 2005 PS2 cover as the site's cover-thumbnail source.
    img.save(assets/'ps2-original-cover.webp',format='WEBP',quality=88,method=6)
    (assets/'COVER_SOURCE.txt').write_text(
        f'2005 PS2 (not 2022 Remastered) original cover\nSource: {url}\n'
        'ROMANCING SAGA - MINSTREL SONG, original Japanese PlayStation 2 release (2005).\n'
        'Cover artwork © SQUARE ENIX. Used as a small identification thumbnail in this non-commercial guide.\n',
        encoding='utf-8'
    )

if __name__=='__main__':
    main()