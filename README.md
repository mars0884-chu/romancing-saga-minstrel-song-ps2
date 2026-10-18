# 《復活邪神：吟遊詩人之歌 Remastered》繁體中文圖文攻略

- **公開 PWA：** https://mars0884-chu.github.io/romancing-saga-minstrel-song-ps2/
- **多檔案離線 ZIP：** https://mars0884-chu.github.io/romancing-saga-minstrel-song-ps2/offline-guide.zip
- **來源與程式：** https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2
- **離線範圍與使用注意：** [OFFLINE_README.md](OFFLINE_README.md)

## 已有內容（2026-10-18，本版資料）

- 279 筆可搜尋繁中／日文攻略，319 筆來源記錄。可搜尋主角、角色、任務、迷宮、地圖、金手指、寶箱與日文原文。
- 8 位主角、74 筆任務、59 筆迷宮及路線、22 筆城鎮村莊、11 個區域索引、10 筆打法。
- 迷宮卡連結原始真實攻略圖，提供圖片放大／樓層查閱；寶箱固定位置、隨機內容、再生與埋藏財寶分開標示，未核實的精確座標不做假標記。
- 霍克（ホーク）初期五洞窟與事件分歧，另外補充 Remastered 珊瑚海特殊通路及追加頭目「血誓のガーデンイール」。
- 古老之城／叢林固定箱方位與隨機箱重置規則，另依 Square Enix 官方手冊新增地圖能力使用次數耗盡時全隊 LP 減少的提示。
- GitHub Pages 首次連線即可安裝 PWA，攻略文字及 repository 內 103 個 SVG 站內示意圖使用 Service Worker 預存。實際測試以 GitHub Actions 的 Playwright 斷網測試為準。

## 離線 ZIP

部署時執行 `tools/build_offline_zip.py`，依據每次提交重新打包首頁、`data.json`、Service Worker、manifest、站內圖檔及下載說明。CI 會測 ZIP 內容、CRC、資料與 `index.html` 的一致性，部署後再檢查公開 ZIP 是否能下載。

**重要：** ZIP 裡的站內 SVG 很多是參考用索引／示意，不是原版真實迷宮地圖；原作者網站的實際遊戲圖片沒有放入公開 ZIP。原圖要在自己的瀏覽器透過「儲存離線圖文」嘗試保存並檢查成功數；離線圖片完整度及實體 iPhone Edge 仍需個別實測。電腦解壓後可用 `index.html` 讀內建文字；手機 PWA 必須透過 HTTPS 安裝，不能把 `file://` 當 Service Worker 安裝。

## 仍未完成（不宣稱已經全面完成）

- 珊瑚海完整高清實際遊戲地圖；更多村莊實景圖、裝備實物／實際遊戲截圖、所有迷宮逐點寶箱及機關核實。
- 全角色所有周目分歧、全任務逐個條件與失效時間點、全部裝備總表與圖片。
- 第三方原圖全部的合法保存、跨域完整離線與 iPhone Edge 實體斷網驗收。
- PS2 金手指及不同平台遊戲差異尚未全面實機測試。

## 圖片與權利

- 外部圖以原站連結與出處展示；**未明寫禁止轉載 ≠ 授權公開再散布**。
- Square Enix 官方角色／遊戲素材與其他玩家標註圖分別註明來源；不把自畫示意圖稱為遊戲原圖；圖像放大不會補出原本不存在的真實細節。
- © SQUARE ENIX CO., LTD. Romancing SaGa 相關權利歸各權利人。
