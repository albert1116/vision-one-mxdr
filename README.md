# vision-one-mxdr

這是一個以繁體中文為主的新系統，參考既有 `vision1` 專案的工作流程與功能分類，
但重新整理成較乾淨、可維護的 HTML / Flask 架構。

## 目前第一版介面包含
- 首頁
- 設定頁
- 查詢頁
- 結果說明頁
- 關於頁

## 設計原則
- 盡量不把 API Key / Token 寫死在原始碼或檔案中
- 需要時由使用者手動輸入
- 目前先以 session 暫存，不直接落地到磁碟
- 先建立可擴充骨架，再逐步串接 Vision One / Insight / Workbench / AI 分析

## 啟動方式
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

啟動後預設可從：
- `http://127.0.0.1:5000`

## 下一步建議
1. 加入真正的 Vision One API client
2. 實作查詢結果表格
3. 增加 Workbench / Insight 頁面
4. 加入匯出與報表管理
5. 將 app.py 再拆成 blueprint / services 結構
