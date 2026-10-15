"""維護工具：從 data.json 更新離線 index.html 中的資料。使用者不必執行此程式。"""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parent
data=json.loads((root/"data.json").read_text(encoding="utf-8"))
assert isinstance(data["records"],list) and isinstance(data["sources"],list)
valid={s["id"] for s in data["sources"]}
for x in data["records"]:
    assert all(s in valid for s in x["sources"]),x["id"]
p=root/"index.html";h=p.read_text(encoding="utf-8")
payload=json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
h,n=re.subn(r'(<script type="application/json" id="dataset">).*?(</script>)',lambda m:m.group(1)+payload+m.group(2),h,count=1,flags=re.DOTALL)
if n!=1: raise ValueError("未找到內嵌資料")
p.write_text(h,encoding="utf-8")
print("已更新",len(data["records"]),"筆")
