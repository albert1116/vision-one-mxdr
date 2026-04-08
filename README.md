# vision-one-mxdr

這是一個以繁體中文為主的新系統，參考既有 `vision1` 專案的工作流程與功能分類，
但重新整理成較乾淨、可維護的 HTML / Flask 架構。

## 目前版本
目前已完成：
- 第一版：首頁、設定頁、查詢頁、結果說明頁、關於頁
- 第二版：已開始串接 Vision One API，先支援：
  - 端點查詢
  - Insight 查詢

## 設計原則
- 盡量不把 API Key / Token 寫死在原始碼或檔案中
- 需要時由使用者手動輸入
- 目前先以 session 暫存，不直接落地到磁碟
- 先建立可擴充骨架，再逐步串接 Vision One / Insight / Workbench / AI 分析

## 目前功能摘要
### 1. 設定頁
- 可輸入 Vision One API Token
- 可輸入 Region
- 可輸入客戶名稱
- 設定只暫存在 session

### 2. 查詢頁
目前已支援：
- 端點查詢
- Insight 查詢

查詢結果頁面可顯示：
- 筆數
- 表格預覽
- 原始 JSON
- 錯誤訊息

## 啟動方式
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

啟動後預設可從：
- `http://127.0.0.1:5000`

如果要讓區網其他電腦存取，目前會監聽：
- `0.0.0.0:5000`

## 注意事項
- 目前仍是 Flask development server
- 適合開發與測試，不建議直接作為正式對外服務
- 若要長期穩定使用，下一步建議改成 gunicorn + systemd

## 下一步建議
1. 加入 Workbench 查詢
2. 加入事件查詢
3. 補上更完整的分頁與結果格式化
4. 增加匯出 JSON / CSV
5. 將 app.py 再拆成 blueprint / services 結構
