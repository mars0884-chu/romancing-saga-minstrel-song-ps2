# 2005 PS2《吟遊詩人之歌》研究狀態與交接

研究日期：2026-10-14 ｜ 版本：v0.2.0-ps2-research-preview

## 判定標準

- **已確認／有原版史料**：2005–2008 年原版攻略，或明確寫明 PS2 原版的當事研究。
- **原版兼新版**：網站在 2022 年後增修；僅採用可判定在 PS2 既有的概念與事件；其他細節仍須 PS2 原版再比對。
- **推測／待核實**：來源文字存在但尚無第二來源、或版本格式／效果未實測。
- **失效／無法讀取**：歷史來源引用到目前工具無法取得，不推論其資料已不存在。
- **僅歷史引用**：來源索引描述曾經存在，不代表本站已抓到其內頁資料。

## 巴哈姆特內外深查

- `https://forum.gamer.com.tw/listG.php?bsn=691`：精華區總索引可被搜尋引擎讀取，明確包含 `PS2 吟遊詩人之歌` 分區，也包含其他 SaGa 遊戲（已排除）。該頁直接讀取時回傳 **HTTP 403**，所以尚無法展開每一個子頁／全部內鏈，不可稱為完成了全站所有內鏈。
- `https://forum.gamer.com.tw/G2.php?bsn=691&lorder=1&parent=18&sn=3`：2005 主角介紹可透過搜尋索引讀到摘要，直連 HTTP 403。
- `https://forum.gamer.com.tw/G2.php?bsn=691&lorder=7&parent=171&sn=193`：2005 日版金手指，貼文引用舊站 `http://www.vanish-net.com/code/ps2/`，原貼文無法直接進入，舊站目前不可存取，僅保存來源鏈。巴哈作者亦提出格式疑問，不能說已驗證可用。
- `https://forum.gamer.com.tw/C.php?bsn=691&snA=6454`：新玩家推薦 `https://kyokugen.info/minsaga/`（外部連結已繼續追）。
- `https://forum.gamer.com.tw/C.php?bsn=691&snA=7115`：有 PS2 真沙魯因實戰心得，敘述與新版差異；僅作玩家經驗，不當作系統定律。

## 外部路線

1. `https://kyokugen.info/minsaga/`：完整事件、發生進度、地圖、職業、技能、武器基礎頁可檢索，屬 2005 舊站延續到 Remastered 的混合版本。**須嚴格過濾「リマスター版限定」**；特別排除新版 `究極のヒミツ`、新角色、2022 新功能。
2. `https://gamefaqs.gamespot.com/ps2/924486-romancing-saga/faqs`：Kouli 2005 事件 FAQ、格雷攻略及 2005–2006 流程／裝備。部分 GameFAQs 原始網站受 robots 限制，但索引資料可檢索；不可逕自搬運作者完整文字。
3. `https://nyusuke.com/game/minstrel/`：作者明確標示 PS2 專用，含 2005 地名最少通關及其他挑戰資料。
4. `https://eicos.blog.fc2.com/blog-entry-91.html`：重要舊攻略站連結樹，含存活、關閉、鏡像／搬遷、網頁存檔等狀態；搜尋引擎可返回內容，本次後續開頁已成功完整讀到原站歷史連結清單（先前曾遇 403）。已記錄其中 `RITZ CODE`、`ＭＡＳＴＥＲ＆ＤＲＥＡＭ`、`RomaSaga_MS データ置き場`、`Saiseti`、`GAKUのつぶやき` 等，但**尚未逐一追出所有內頁且確認現況**。
5. `https://ffsky.com/Article/bc5739_a8974.aspx` 和 `https://s.ffsky.com/article/bc0_a8982.aspx`：2005 年天幻網依 Ultimania 整理的分區事件攻略。搜尋可見，但直接抓頁受限，未擅自複製全文。
6. `https://kuronokuru1985.blog.fc2.com/blog-entry-1472.html`：另有註明專為 PS2 原版撰寫的系統／經濟／戰鬥／事件分篇。
7. `https://www.neoseeker.com/romancing-saga-minstrel-song/faqs/112579-romancing-saga-ms-barbara-sinningishuman3479.html`：2005 芭芭拉原版流程，明文禁止未授權轉貼。

## 尚未完成／無法宣稱

- 巴哈姆特精華區所有內鏈、文章中的所有出站連結，**尚未全部逐頁可讀取**，部分遭 403 封鎖。
- 舊攻略站連結樹有大量歷史關站／改址項目；已找出索引，尚未完成逐條存活性測試。
- 已整理 61 張日文原名對照事件卡，包含索引級條目；但尚未完成 2005 年 Kouli 89 項事件（含吟遊詩人故事等）的全部逐條流程；裝備僅提供 9 筆舊站抽樣數值，非完整表；未建立全部職業資料表或地圖影像檔。
- 尚未 PS2 硬體或模擬器實測金手指、iPhone Edge、PWA 安裝與站點上線。
- 2026-10-15：Work已新建專用獨立儲存庫 `mars0884-chu/romancing-saga-minstrel-song-ps2`，主分支main、Public、初始commit `7fb2a964684aa43c2df996e072c757adb3358782`；以GitHub連接器驗證目前**只有README.md**。本研究稿仍未推送，正式GitHub Pages未啟用。

## 後續整理優先順序

2005 年 Kouli 89 項事件（與 61 張日文事件索引對照）完整核對 → 巴哈精華區原文／內外連結 → 日本 2005 攻略舊站／鏡像 → 角色／術法／裝備／技能細表 → 日版代碼格式與實測 → 手機瀏覽器 PWA 真機驗證 → 單獨 Github 新 repo 部署。

> 原作者文本及圖片不直接重刊；保留出處 URL、日文原文名稱與台灣繁體中文摘要。`data.json` 可做長期更新來源。

## 本輪新找到的 2005 原版網頁封存

- `https://web.archive.org/web/20250621100336/http://romamin.fc2web.com/`：2005 年 **RomaSaga_MS データ置き場** 網頁封存，可讀首頁、武器、防具、改造、寶藏及玩家驗證類別；前站目前已關閉。
- `https://web.archive.org/web/20250621100504/http://romamin.fc2web.com/buki.html`：原版武器性能表存取成功，本站只採 9 筆精選、附來源的客觀數值，不複製完整資料表。
- `https://web.archive.org/web/20250621101123/http://romamin.fc2web.com/zaihoumanyu.htm`：原版財寶挖掘研究封存，存取成功。
- `https://web.archive.org/web/20250621101403/http://romamin.fc2web.com/lv5.htm`：五級寶藏地圖研究，存取成功。
- `https://web.archive.org/web/20240614123801/http://www7a.biglobe.ne.jp/~tokamaku/saga/minsagamain.html`：MASTER＆DREAM 原站網頁封存可取得 Wayback 索引，尚未確認所有內頁。
- `https://ritzcode.web.fc2.com/index.html`：本次測試回傳 503，**不能因連不上推論內容不存在**。
- 巴哈舊精華區 PS2 子區別可確認有新手、格雷／克洛蒂雅／虎克、賺錢、三地點、任務、掉寶、金手指和對外網站類別；站內全文及個別原始連結尚有 403 限制，本站已加入分類卡作追索線索。


## 2026-10-15 後續整理

已補上 11 區地圖、53 個迷宮／探索地點索引及部分入口、地圖技能、相關任務與2005原版路線；新研究稿共189筆、83個來源頁（不代表全部完成）。另請見 `RESEARCH_AUDIT_2026-10-15.md`。

關鍵：RPG INSTITUTE 明示的2005 PS2 研究「オウルの呼び声」約40%開始，與現行混合站約30%矛盾；優先原版研究，不可用現代站覆蓋2005原版。

本次未將任何新攻略推到GitHub，遵循一次集中發布原則。


## 2026-10-15 v0.3.0 批次整理

- 加入2005年巴哈古刀、魔之島、妖精森林、中期任務、火山、提奧多爾、三地點的逐條搜尋索引。
- 原版事件發生研究（surume5）中進度%僅作估算，與時間經過點及連鎖事件一起判斷。
- 攻略與研究來源索引一併更新；請參閱 RESEARCH_UPDATE_2026-10-15.md。
- 舊站403、舊連結失效或亂碼只標現況，不能推論不存在。