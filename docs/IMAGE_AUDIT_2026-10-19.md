# 外部真實圖稽核｜2026-10-19（GitHub Actions）

- 稽核工作：https://github.com/mars0884-chu/romancing-saga-minstrel-song-ps2/actions/runs/39243217200
- 與當次正式網站版本相同 SHA：`054f17c2eabaaeb93006c88c2a1b227b7aa75d12`。
- 工具回報：**162 個不同外部圖片網址，成功讀取 110、network_error 52；高解析度（1280×720 以上）只有 3 個**。
- 本檔記錄的是**GitHub Actions runner 當次網路環境結果**；`network_error` 不是 HTTP 404，不代表原站永久失效、圖檔不存在，亦不代表手機瀏覽器一定無法讀到。
- **稽核 workflow 顯示 success 是產生報告成功，而非所有圖片成功載入。** 不可把綠色勾勾當真實原圖已完全可讀、更不能宣稱已全數離線。
- 發生問題的主機：`kyokugen.info`。
- PWA 離線：網站首頁、內嵌攻略與站內 SVG 有自動測試；**第三方原圖能否在 iPhone Edge 斷網載入，仍須在該裝置實際驗證**，不可把來源圖 URL、Opaque Cache、CI 圖片 HTTP 讀取互相當替代。
- 權利：缺少明文禁止轉載**不等於授權公開散布**。保留原站圖網址與來源頁，不擅自放入 GitHub Pages。
- 後續優先：對以下 URL 逐項重試、找同作者的有效鏡像／合法替代、查巴哈外鏈與日文其他可讀來源；先核實高解析可用原圖，再談精確寶箱定位。

## 52 個 GitHub 執行器當次無法讀取的 URL

1. https://kyokugen.info/minsaga/map/bafal_bayer.jpeg
2. https://kyokugen.info/minsaga/map/bafal_elizabeth.jpeg
3. https://kyokugen.info/minsaga/map/bafal_forest.jpeg
4. https://kyokugen.info/minsaga/map/bafal_forest_dark.jpeg
5. https://kyokugen.info/minsaga/map/bafal_gold.jpeg
6. https://kyokugen.info/minsaga/map/bafal_great.jpeg
7. https://kyokugen.info/minsaga/map/bafal_loban.jpeg
8. https://kyokugen.info/minsaga/map/bafal_melville.jpeg
9. https://kyokugen.info/minsaga/map/drylands_desert.jpeg
10. https://kyokugen.info/minsaga/map/drylands_elore.jpeg
11. https://kyokugen.info/minsaga/map/drylands_galessa.jpeg
12. https://kyokugen.info/minsaga/map/drylands_nieca.jpeg
13. https://kyokugen.info/minsaga/map/drylands_oldcastle.jpeg
14. https://kyokugen.info/minsaga/map/etc_faerie.jpeg
15. https://kyokugen.info/minsaga/map/etc_last.jpeg
16. https://kyokugen.info/minsaga/map/etc_mummy.jpeg
17. https://kyokugen.info/minsaga/map/etc_purgatory.jpeg
18. https://kyokugen.info/minsaga/map/etc_sherah.jpeg
19. https://kyokugen.info/minsaga/map/etc_ukkom.jpeg
20. https://kyokugen.info/minsaga/map/frontier_jewelbeast.jpeg
21. https://kyokugen.info/minsaga/map/frontier_newroad.jpeg
22. https://kyokugen.info/minsaga/map/frontier_saoki.jpeg
23. https://kyokugen.info/minsaga/map/frontier_vampire.jpeg
24. https://kyokugen.info/minsaga/map/frontier_yassi.jpeg
25. https://kyokugen.info/minsaga/map/kjaragt_assassin.jpeg
26. https://kyokugen.info/minsaga/map/kjaragt_estamir.jpeg
27. https://kyokugen.info/minsaga/map/kjaragt_shuilung.jpeg
28. https://kyokugen.info/minsaga/map/kjaragt_tarmitta.jpeg
29. https://kyokugen.info/minsaga/map/knight_abandoned.jpeg
30. https://kyokugen.info/minsaga/map/knight_constanzu.jpeg
31. https://kyokugen.info/minsaga/map/knight_dragon.jpeg
32. https://kyokugen.info/minsaga/map/knight_mirsaburg.jpeg
33. https://kyokugen.info/minsaga/map/knight_paganruins.jpeg
34. https://kyokugen.info/minsaga/map/ligau_dinosaurs.jpeg
35. https://kyokugen.info/minsaga/map/ligau_netherworld.jpeg
36. https://kyokugen.info/minsaga/map/ligau_plain.jpeg
37. https://kyokugen.info/minsaga/map/ligau_tomae.jpeg
38. https://kyokugen.info/minsaga/map/ligau_treasure.jpeg
39. https://kyokugen.info/minsaga/map/rosalia_crystal.jpeg
40. https://kyokugen.info/minsaga/map/rosalia_evil.jpeg
41. https://kyokugen.info/minsaga/map/rosalia_isthmus.jpeg
42. https://kyokugen.info/minsaga/map/rosalia_isthmus_castle.jpeg
43. https://kyokugen.info/minsaga/map/rosalia_scurve.jpeg
44. https://kyokugen.info/minsaga/map/valhalland_east.jpeg
45. https://kyokugen.info/minsaga/map/valhalland_field.jpeg
46. https://kyokugen.info/minsaga/map/valhalland_frozen.jpeg
47. https://kyokugen.info/minsaga/map/valhalland_south.jpeg
48. https://kyokugen.info/minsaga/map/valhalland_west.jpeg
49. https://kyokugen.info/minsaga/map/walon_gueccoes.jpeg
50. https://kyokugen.info/minsaga/map/walon_jungle.jpeg
51. https://kyokugen.info/minsaga/map/walon_pyramid.jpeg
52. https://kyokugen.info/minsaga/map/walon_silver.jpeg

## 比較與實測規則

每次更新，必須保留「成功讀取」「網路錯誤」「404／失效」「僅來源文字」「版權限制／未授權重散布」「可在實體 iPhone Edge 斷網顯示」等**不同類別**。不同時間同網址的結果可能改變；不以查不到認定不存在。

> 其他 110 張雖然 GitHub 執行器可讀，並不代表已取得高解析原圖或全數快取到使用者手機。
