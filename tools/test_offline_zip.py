"""ZIP 解壓後在無網路的本機 file:// 測試文字搜尋及本地圖片，不宣稱外部原圖離線。"""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
archive = ROOT / "offline-guide.zip"
assert archive.exists(), "先執行 tools/build_offline_zip.py"
with TemporaryDirectory() as temp:
    with ZipFile(archive) as z:
        assert z.testzip() is None
        z.extractall(temp)
    folder = Path(temp) / "minstrel-song-offline"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        for width, height in [(1366, 768), (390, 844)]:
            ctx = browser.new_context(viewport={"width": width, "height": height}, offline=True)
            page = ctx.new_page()
            page.goto((folder / "index.html").as_uri(), wait_until="domcontentloaded")
            page.wait_for_selector("#cards .item", timeout=30000)
            page.locator("#search").fill("サンゴ海")
            assert page.locator("#cards .item").count() > 0, "Japanese offline search unavailable"
            page.locator("#search").fill("血誓のガーデンイール")
            assert page.locator("#cards .item").count() > 0, "New Remastered boss missing from offline archive"
            pic = page.evaluate("""async () => {
                let p = document.createElement('img');
                p.src = 'assets/atlas/map-01.svg';
                return await new Promise(resolve=>{
                    p.onload=()=>resolve(p.naturalWidth>0);
                    p.onerror=()=>resolve(false);
                    setTimeout(()=>resolve(false),5000);
                });
            }""")
            assert pic, "Local SVG cannot load from extracted ZIP while offline"
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth+1"), "zip site overflows viewport"
            print(f"Unpacked ZIP file:// offline search & SVG: PASS {width}x{height}")
            ctx.close()
        browser.close()
