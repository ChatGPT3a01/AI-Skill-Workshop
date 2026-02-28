# 亮言~NotebookLM 自動化 Skill（學員版）

> AI Skill 實作課 Day 2 - Part 10 實作專案

## 快速安裝（4 步驟）

### Step 1：安裝核心工具
```bash
pip install notebooklm-py
pip install "notebooklm-py[browser]"
playwright install chromium
```

### Step 2：安裝專案依賴
```bash
cd notebooklm-automation
pip install -r requirements.txt
```

### Step 3：登入 Google 帳號
```bash
notebooklm login
```
瀏覽器會自動開啟，完成 Google 登入後回到終端機按 Enter。

### Step 4：啟動應用程式
```bash
python app.py
```
開啟瀏覽器訪問 http://localhost:5000

## 自然語言指令範例

| 功能 | 指令範例 |
|------|----------|
| 列出筆記本 | 「列出我所有的筆記本」 |
| 建立筆記本 | 「建立一個叫做 AI 研究的筆記本」 |
| 匯入網址 | 「新增這個網址 https://example.com」 |
| 匯入 YouTube | 「加入這個 YouTube 影片 https://...」 |
| 生成 Podcast | 「幫我生成 Podcast」 |
| 生成心智圖 | 「製作心智圖」 |
| 生成測驗 | 「生成 10 題測驗」 |
| 生成報告 | 「做一份報告」 |
| 問答查詢 | 「問一下這份文件的主要觀點」 |

## 系統需求

- Python 3.9 以上
- 穩定網路連線
- Google 帳號
- RAM 8GB 以上（建議）

## 常見問題

**Q: 出現「No notebook specified」？**
→ 先在左側下拉選單選擇筆記本

**Q: 登入狀態失效？**
→ 重新執行 `notebooklm login`

**Q: Podcast 很久沒反應？**
→ 正常！需要 2-5 分鐘，查看右側「任務狀態」

**Q: NLP 解析不準確？**
→ 用更明確的關鍵字，或在設定頁切換 Gemini/OpenAI 模式

## 專案結構

```
notebooklm-automation/
├── app.py                 ← Flask 主程式
├── config.py              ← 設定檔
├── config.json            ← 使用者設定
├── requirements.txt       ← Python 依賴
├── routes/                ← API 路由
│   ├── execute.py         ← 核心：自然語言執行
│   ├── notebooks.py       ← 筆記本管理
│   ├── sources.py         ← 來源管理
│   ├── artifacts.py       ← 工件管理
│   ├── auth.py            ← 認證
│   └── settings.py        ← 設定
├── services/              ← 業務邏輯
│   ├── nlp_parser.py      ← NLP 解析器（3 種模式）
│   ├── notebooklm_service.py ← CLI 封裝
│   ├── config_manager.py  ← 設定管理
│   └── task_manager.py    ← 背景任務
├── templates/             ← HTML 模板
└── static/                ← CSS / JS / 圖片
```

---
Powered by 阿亮老師 | AI Skill 實作課
