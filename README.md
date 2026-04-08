# vision-one-mxdr

這是一個以繁體中文為主的新系統，參考既有 `vision1` 專案的工作流程與功能分類，
但重新整理成較乾淨、可維護的 HTML / Flask 架構。

## 目前版本
目前已進到「全功能初版」階段，已包含：
- 首頁 Dashboard
- 設定頁（session-based secret handling）
- 查詢頁
- 結果頁
- 關於頁
- 詳細頁骨架
- JSON / CSV 匯出

## 目前已支援的查詢
- 端點查詢
- Insight 查詢
- Workbench 查詢
- 事件查詢

## 目前已支援的結果處理
- 查詢結果表格預覽
- 原始 JSON 顯示
- JSON 匯出
- CSV 匯出
- Insight 詳細頁骨架
- Workbench 詳細頁骨架

## 設計原則
- 盡量不把 API Key / Token 寫死在原始碼或檔案中
- 需要時由使用者手動輸入
- 目前先以 session 暫存，不直接落地到磁碟
- 先建立可擴充骨架，再逐步串接更深的分析能力

## 啟動方式
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 注意事項
- 目前仍是 Flask development server
- 適合開發與測試，不建議直接作為正式對外服務
- 後續若要穩定部署，建議改成 gunicorn + systemd

## 後續建議
1. 補 Workbench / Insight 更完整的詳細資料整理
2. 補事件查詢更多欄位與分頁
3. 補 AI 摘要與報表模板
4. 把 app.py 再拆成 blueprint / routes 層級
