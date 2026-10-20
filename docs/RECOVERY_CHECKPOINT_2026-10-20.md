# 可恢復檢查點｜2026-10-20 v0.9.8

- 倉庫：https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2
- PWA：https://mars0884-chu.github.io/romancing-saga-minstrel-song-ps2/
- 預定固定備份分支：backup/2026-10-20-pwa-v098-handoff（以最終GitHub實際分支指向確認）
- 先讀 docs/DEVELOPMENT_LOG.md、docs/MAINTENANCE_GUIDE.md、docs/RESTART_PROMPT.md、PROGRESS_2026-10-18.md、research/goldmine-uhanji-2026-10-20.md。
- 主要檔案：data.json（主資料）、index.html（內嵌guide-data與搜尋UI）、sw.js（PWA預存）、manifest.webmanifest、assets/、tools/test_pwa.py、.github/workflows/。
- v0.9.8 內容：279筆攻略、357筆來源，中文與日文並存；167個不重複外站圖片URL，115處樓層圖片引用（含同一圖在多筆攻略重複使用）；不同數字非「遊戲全部完成百分比」。
- 重要更正：G011早期金庫襲擊15～30%與G028後期70%礦坑救援為不同事件。G028及D-07-05五張實際遊戲截圖連結；G013烏漢吉與水龍後續分支已詳細補入。
- 離線：開啟PWA立即搜尋，不使用ZIP；首次連線SW預存站內HTML、JSON與103個本地SVG（大多是示意）並嘗試使用者裝置本地快取外站圖。2026-10-19歷史圖片稽核162張中52個kyokugen.info network_error，非404；本次新增圖請看新稽核，不能保證手機圖片全離線。
- 版本：data.json內version 0.9.8-mines-branch-guide；HTML/SW cache名 minstrel-ps2-2005-v0.9.8-local-maps4；自動測試也要0.9.8。之前版本號硬寫0.9.7令CI假失敗，已在0f28a154ee6f9966bd14324864cbfe1fdcef8fc5修正。
- 文件含來源出處、權利、未完成及失效／不可讀研究。不可因未標禁止轉載就公開重打包第三方圖。缺珊瑚海高清圖、礦坑B1真原圖、全部裝備圖與村莊實景、逐箱精確位置、真實iPhone Edge所有圖片斷網。
- 2026-10-20實際檢查本輪工作容器/mnt/data為空，無臨時檔需刪；沒有使用者私人Windows/iPhone磁碟存取權，沒有備份或刪除那些不可讀的檔案。絕不能刪任何非本專案檔案。
- **恢復操作**：先查GitHub main最新SHA及Actions；若需回復，使用本分支或main並校驗data.json＝首頁內嵌guide-data、SW key與test_pwa.py。CI驗收須verify-pwa、Audit Original Map Image URLs（綠燈不等於所有遠端圖成功）、Deploy Remastered PWA to GitHub Pages及正式live HTML/SW/JSON/圖可讀同SHA。不要要求非技術使用者貼程式或操作命令列。

## 2026-10-20 最後有效測試紀錄
在程式與研究已上主分支的commit eaa674912e0d18e6b532e723bf9de8a8c30c722d，GitHub Actions當次全部成功；部署：https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2/actions/runs/39408471054 ，PWA：https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2/actions/runs/39408471187 ，圖片稽核：https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2/actions/runs/39408471006 。舊版runner網路錯誤已在這次167/167恢復可讀（但僅3張高解析），詳 docs/IMAGE_AUDIT_2026-10-20.md 。本次新增純文檔之後的SHA，仍應重新核對Actions。
