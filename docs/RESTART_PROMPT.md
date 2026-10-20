# 新對話／Work 重啟提示詞（直接複製整段）

> **目標**：舊對話達上限或 Work 重開時，交給下一個 AI **完整接手而非重建**。以下內容只針對獨立《復活邪神：吟遊詩人之歌 Remastered》攻略專案。

```text
直接接續《復活邪神：吟遊詩人之歌 Remastered／PS2原版對照》PWA 專案。
僅能使用獨立 GitHub repo：
https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2
正式網站：https://mars0884-chu.github.io/romancing-saga-minstrel-song-ps2/
絕不可修改 baseball-GM、族譜、任何其他 repository 或專案。

請先在 GitHub 讀取：README.md、docs/DEVELOPMENT_LOG.md、
docs/MAINTENANCE_GUIDE.md、PROGRESS_2026-10-18.md、
research/ 及 data.json、index.html、sw.js、tools/test_pwa.py、
.github/workflows/deploy-pages.yml。
再讀取最新 main commit 和 Actions，確認當下真正部署的版本，不能以提示詞寫死的舊 SHA 當最新成果。

使用者的嚴格需求：
- 桌機 Edge、iPhone Edge 直接打開同一 PWA 就能即時搜尋與查閱，不要 ZIP、不需要下載／匯入或點選手動初始化按鈕。
- 首次連線時自動保存內建攻略與站內資源；已快取的可斷網搜尋及縮放；第三方真實圖片嘗試合法本機快取，清楚標出成功／失敗；沒有實機斷網證據不能聲稱所有圖片離線成功。
- 每項攻略按完整事件前置、時限、主角分歧、路線入口、逐層地圖、固定/隨機寶箱、解謎機關、頭目與戰術、裝備組合、報酬、失敗條件與回程逐一編寫。完全沒有「最多五步」或「至少五步即完成」的規則，內容不夠就續挖。
- 主角、地區、村莊、迷宮、裝備圖片必須是實際遊戲對應的原圖或明確來源的攻略圖，不可生成假地圖或把 SVG 示意當原版原圖。需支援清晰放大與手機捲動縮放。
- 日文原文、繁體中文同時保留，中文日文全文可搜尋。金手指分類搜尋，注意 PS2 與 Remastered 平台差異。
- 巴哈精華區內部及外部連結都要追查到可檢索可讀來源無新資料為止；標已確認／推測／失效／403可檢索但不可讀／歷史引用。搜尋不到不等於不存在。
- 不要用未標示禁止轉載推導出公開重新散布授權，來源圖片以連結／合法素材為主，本站離線 SVG 必須標明示意。
- 使用者不是工程師，不要讓他貼程式、操作命令列、手動整理資料，也不要每一步停下來詢問。連續做完可以完成的所有部分才回報。
- 改動後務必 data.json 和 index.html 的 guide-data 同步、Service Worker 快取鍵與版本同步、更新自動測試、實際推送 GitHub、部署 GitHub Pages，最後核對同 SHA Actions 與公開網址，誠實交代尚缺內容。
- GitHub 必須保留開發記錄、失敗修復、未完待辦及此重啟提示詞，讓人可永久接手。
- 使用者曾要求刪本機檔案：只有在能辨認為本遊戲專案工作副本且已確認 GitHub 備份與復原方式後，才可清理該工作副本；絕不可刪使用者其他本機資料，也不得說自己已清掉無法接觸的電腦。此對話容器 /mnt/data 當時為空。

從最新 GitHub 狀態開始，不要重做既有已完成的工作。
請實際續挖、補齊、更新、推送、完整圖文、真實地圖、詳細攻略、可搜尋、可離線與正式部署。
最後交代：完成項目、受阻／不實機可驗部分、有效網站網址、最新 full commit SHA、Actions 驗收狀態、GitHub 備份與工作目錄清理狀態；沒有產出 ZIP 就不要給 ZIP。
```

## 可用資訊

資料皆在上方 GitHub repo 的 `main`；不需要舊對話本地工作檔。原始攻略與圖片權利狀態詳 `docs/DEVELOPMENT_LOG.md` 與 `docs/MAINTENANCE_GUIDE.md`。此提示詞刻意不寫固定最新 SHA，避免未來接手跳到過時版本。

## 2026-10-20 新版接手補充（置頂優先事項）

若未來重啟：先讀 `docs/RECOVERY_CHECKPOINT_2026-10-20.md` 和 `research/goldmine-uhanji-2026-10-20.md`。舊版0.9.7的資料計數與圖片稽核僅供歷史對照，以當前GitHub main、最新data.json及圖片測試為準。最新基線為v0.9.8，任務G011/G028已分開、後期礦坑5張原站地圖與G013烏漢吉完整分歧已整合，不得回退改成早期金庫追賊流程。確認 `index.html`、`data.json` 同步且快取鍵一致，查同SHA GitHub Actions完成。使用者要的是PWA直接開啟查找，不是ZIP。離線原站真實圖片尚非全部經實體iPhone Edge證實。若本機工作目錄空，不能為了回應刪除要求而刪其他人的資料或其他專案。

**可直接用的後續短提示詞：**「接手 mars0884-chu/romancing-saga-minstrel-song-ps2 的 main 與最新 docs/RECOVERY_CHECKPOINT_2026-10-20.md，繼續補真實高清原圖、逐層機關寶箱、完整角色任務與中日搜尋、PWA自動快取及斷網驗證；不能做ZIP、不能以五步當完成；請實際推送並等待同SHA全部Actions成功，更新GitHub開發歷程、可重啟提示詞、來源狀態與備份分支，只清理確認備份且僅屬本repo的本機暫存，最後完整回報。」

**最新圖片稽核附記：** 2026-10-20 GitHub runner對167個URL全部可讀，但只有3張達1280×720；請讀 `docs/IMAGE_AUDIT_2026-10-20.md`，不可用runner成功宣稱iPhone Edge原圖全離線。
