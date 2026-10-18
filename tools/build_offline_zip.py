"""在 GitHub Pages 部署時產生含本地圖檔的多檔案離線 ZIP。第三方攻略原圖不得自動重打包。"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "offline-guide.zip"
PREFIX = "minstrel-song-offline"
BASIC = ["index.html", "data.json", "sw.js", "manifest.webmanifest", "OFFLINE_README.md"]
assets = sorted(p for p in (ROOT / "assets").rglob("*") if p.is_file())
files = [ROOT / f for f in BASIC] + assets
if not all(p.is_file() for p in files):
    raise RuntimeError("offline package source file missing")
guide = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
html = (ROOT / "index.html").read_text(encoding="utf-8")
match = re.search(r'<script id="guide-data" type="application/json">(.*?)</script>', html, re.S)
if match is None:
    raise RuntimeError("guide-data missing from offline index")
if json.loads(match.group(1)) != guide:
    raise RuntimeError("index.html inline guide diverges from data.json")
if len(guide["records"]) < 279:
    raise RuntimeError("guide appears to have lost records")
for p in assets:
    if p.suffix.lower() not in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".txt"}:
        raise RuntimeError(f"unreviewed asset: {p.relative_to(ROOT)}")

with ZipFile(DEST, "w", compression=ZIP_DEFLATED, compresslevel=8) as out:
    for path in files:
        out.write(path, f"{PREFIX}/{path.relative_to(ROOT).as_posix()}")

with ZipFile(DEST) as check:
    bad = check.testzip()
    if bad:
        raise RuntimeError(f"ZIP CRC failed: {bad}")
    names = check.namelist()
    for required in (f"{PREFIX}/index.html", f"{PREFIX}/data.json", f"{PREFIX}/assets/ps2-original-cover.webp"):
        if required not in names:
            raise RuntimeError(f"missing archive member: {required}")
    offline_json = json.loads(check.read(f"{PREFIX}/data.json"))
    if offline_json != guide:
        raise RuntimeError("ZIP data differs from current site")
    print(f"ZIP verified: {DEST.name}, records={len(guide['records'])}, assets={len(assets)}, files={len(names)}, bytes={DEST.stat().st_size}")
