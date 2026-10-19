# 可恢復檢查點｜2026-10-19 版 PWA 攻略

- 正式倉庫：https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2
- 正式網站：https://mars0884-chu.github.io/romancing-saga-minstrel-song-ps2/
- 主分支：`main`，內容源自 `data.json`、`index.html`、`sw.js`。
- 備份分支預定：`backup/2026-10-19-pwa-handoff`（以完成當輪部署與測試後、在主分支最新完整 SHA 上建立。是否已建成以 GitHub 分支頁查驗，不得只憑本段判定）。
- 資料：279 筆攻略、350 筆來源（2026-10-19 更新），中日雙語、地圖與金手指資料同一份 JSON。
- 顯示：PWA 點開即載入網站內嵌資料；站內檔案透過 SW 預存，第三方原站真圖部分要看裝置是否能快取。
- 真實地圖：已連結寶石獸四區段、黃玉／沙漠、雙月神殿、梅爾維爾下水道與伊莉莎白宮殿等原作者地形圖；沒有全部高清，更沒有取得所有圖的公開重散布授權。
- 這版新攻略「メルビル襲撃計画」：一般70％以上通報／80％強制，已完成皇帝怪病可能提早觸發的 Remastered 例外；闖海賊據點、通報、旅館、地下神殿連戰、港口布查、霍克追擊、宮殿王房與寶箱。日文頁 `https://kyokugen.info/minsaga/minstrel_story_5_11.html`、`https://kyokugen.info/minsaga/minstrel_map_7_01.html`、`https://jp.samurai-gamers.com/saga_minstrelsong_re/rsmsr-event19/`、`https://saga-remaster.com/?p=368`。
- 最後一輪可核對的 CI 應包含：`Verify 2005 PS2 PWA offline`、`Audit Original Map Image URLs`、`Deploy Remastered PWA to GitHub Pages`；正式部署工作要檢查 LIVE 首頁、完整 JSON、Service Worker 與三個站內示意圖的 HTTP 可讀性。驗收必須相同 SHA。
- 本地檔案清理：2026-10-19 檢查會話工作容器 `/mnt/data` 為**空目錄**，無待備份或待刪除的遊戲專案暫存檔；未取得 Windows 本機磁碟權限，不曾刪除使用者電腦的個人檔案。GitHub 不是使用者其他本機資料的自動備份。
- 重啟從 `docs/RESTART_PROMPT.md` 開始；完整決策和檔案架構見 `docs/DEVELOPMENT_LOG.md`、`docs/MAINTENANCE_GUIDE.md`。

## 恢復原則

1. 用 GitHub `main` 或備份分支取回 `index.html`、`data.json`、`sw.js`、所有 `assets/` 與工作流程，不用舊對話原始工作目錄。
2. 回復／修改後，更新 `data.json` 和 `index.html` 內嵌 `guide-data` **完全一致**。
3. 桌機和手機斷網 PWA 測試、原圖來源稽核、正式 Pages 部署驗證全部成功後才發布。
4. 禁止混用或更動任何非本遊戲的 repo；不使用 ZIP；不使用固定攻略步數衡量完成。
