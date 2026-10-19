# PWA 維護／資料交接文件（給未來接手的 AI 與主編）

**核心使用方式：** 使用者只要打開 https://mars0884-chu.github.io/romancing-saga-minstrel-song-ps2/ ，就應直接可用，沒有 ZIP、沒有另行匯入。

## 哪個檔案做什麼

| GitHub 檔案／資料夾 | 功用及正確更新方式 |
|---|---|
| `data.json` | 所有條目、中文／日文名稱、步驟、原圖網址、分層原圖、來源 ID 及來源目錄的**主資料**。 |
| `index.html` | RWD PWA UI 與內嵌 `<script id="guide-data">` 的同一份資料，可直接搜尋；更新主資料後**一定同步**這個內嵌 JSON。 |
| `sync_site.py` | 自動將 `data.json` 同步到 `index.html` 的輔助工具，供接手 AI 使用；**不可叫使用者操作指令**。 |
| `sw.js` | Service Worker、站內離線預存、外部圖在裝置本機的可行性快取；須與新版 HTML 的 `CACHE` 相容。 |
| `manifest.webmanifest` | PWA 名稱、圖示、啟動網址、scope；圖示應該與遊戲真正封面一致。 |
| `assets/...` | 已納 GitHub 的站內本地素材；原創地圖／角色／裝備 SVG 多數為示意，不能稱為真實遊戲截圖。 |
| `tools/test_pwa.py` | Playwright Chromium 桌機與 390×844 等手機尺寸、圖片與斷網搜尋／縮放的驗收。應檢查實際遊玩流程與圖片而非「五步門檻」。 |
| `tools/audit_images.py` | 圖源有效性／解析度檢查，可能受外站連線限制，不代表所有裝置快取成功。 |
| `.github/workflows/deploy-pages.yml` | 一次 push 後測試、正式部署與 LIVE HTML／SW／JSON／本地圖驗證。 |
| `.github/workflows/verify-pwa.yml` | 獨立 PWA 測試；和部署驗證同時成功較可靠。 |
| `research/` 與各種 `RESEARCH_*.md` | 來源研究與舊追查記錄；舊資料可能過期，需重新讀原網址。 |
| `PROGRESS_2026-10-18.md` | 最新統計與明確未完清單，不能用步數代表完整率。 |
| `docs/DEVELOPMENT_LOG.md` | 每次可追溯的功能／修復／部署紀錄。 |
| `docs/RESTART_PROMPT.md` | 新對話直接接手提示詞，讓未來不用依賴已過量的舊對話。 |

## data.json 條目規格

已有 `records` 陣列，常見欄位：

- `id`：穩定、不可無理由更換（會影響深連結與跨條目跳轉）
- `section`：新手／主角／任務／系統／資料庫／金手指／地圖／迷宮／打法／配裝／地點／同伴
- `title`、`ja`：繁體中文與日文原文同時存在
- `summary`：一句定位（不代表完整攻略）
- `steps`：完整具體的路線、選擇、時限、打怪、獎勵與風險，可任意多步；應適度加章節語意、避免大量重複。
- `sources`：只能填在頂層 `sources` 目錄存在的 ID
- `gallery`：`[{src,caption}]` 真實圖片；須辨別官方畫面、玩家實測截圖、攻略作者自繪平面圖與本站示意 SVG。
- `floorMaps`：`[{floor,src,sourcePage,caption}]`，逐層地圖，標示原作者和原始尺寸；不應對隨機寶箱捏造固定座標。
- `relatedIds`、`quality`、`risk`：關連攻略、證據等級和重要錯過條件。

頂層 `sources` 每筆含 `id/name/url/kind/note`。來源網站即使曾經讀得到，未來失效仍保留歷史資訊並標註，不能直接刪除歷史研究。

## PWA 與離線

1. PWA 打開 `index.html` 應**立即**內嵌攻略、查詢中文與日文，無須等遠端圖片。
2. `sw.js` 預存首頁、資料、icon、封面及 103 個站內 SVG。網頁連線時後臺嘗試快取白名單第三方圖；需要顯示成功張數及來源失效列表。
3. 公開第三方圖的網址 ≠ 已存入本機；Service Worker opaque cache 在 iPhone Edge 尤其需實測。若無權重散布則不要自動上傳外部原圖到 GitHub Pages。
4. 版本切換時清點 `const KEY` 和 HTML 的 `const CACHE`；切勿再造成安裝快取成功、前端卻顯示未保存的問題。
5. 首次測試應看「斷網重新開啟後**不用 ZIP 也能直接查**」；瀏覽器桌機自動測試不能當作實體 iPhone Edge 的驗收。

## 每輪發佈 Checklist

1. GitHub `main` 最新 SHA 與 Actions 先核對；將新資料補到 `data.json`，每條引用 ID 必須存在。
2. 同步 `index.html` 內嵌 JSON；檢查新增中文、日文關鍵字、實際圖像、來源出處與錯過時限。
3. 如果新增本站檔案，補進 SW `FILES` 快取清單；不要把示意圖包裝為遊戲原圖。
4. 更新 CI 的實際劇情斷言、桌機／手機搜尋與斷網測試；不寫固定五步門檻。
5. 更新 `README`、進度、開發歷程／關鍵提示詞。
6. Push，等待**相同 full SHA** 的 `Verify 2005 PS2 PWA offline`、`Audit Original Map Image URLs`、`Deploy Remastered PWA to GitHub Pages` 和 live deployment verification 成功。
7. 公開網站開啟驗證，最終說明「已確認」「推測」「未驗」「不可讀來源」「已部署」「裝置仍需驗證」。
8. 檢查本機工作副本是否真正存在、是否只屬此 repo、GitHub 是否有可復原完整版本；**不得執行廣域磁碟清除**。

## GitHub 儲存庫作為備份

目前倉庫包含 `data.json`、`index.html`、`sw.js`、manifest、圖示與站內素材、歷史研究、PWA 測試、工作流程、開發紀錄與重啟提示詞。屬於可交接的遠端備份；但**使用者個人未提供、無法存取的本機原圖／其他檔案，不能宣稱已備份**。
