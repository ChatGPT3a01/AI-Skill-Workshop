---
name: proposal-drafter
description: >
  根據需求分析摘要撰寫客戶提案書草稿。
  當使用者提供需求分析結果或要求撰寫提案書時使用。
---

# 客戶提案撰寫器

## 前置條件
- MUST 確認已有需求分析摘要（來自 need-analyzer 的輸出）
- Check if 使用者直接提供原始需求 → 建議先執行 need-analyzer
- Ask user 提供公司名稱和方案定價範圍

## 執行步驟
### Step 2：撰寫提案架構
依照 @assets/proposal-template.md 的範本結構撰寫

### Step 3：填充內容
- MUST 針對每個核心需求提出具體解決方案
- MUST 包含時程規劃（甘特圖式表格）
- MUST 包含報價概估（以範圍呈現）
- NEVER 承諾未確認的技術細節
- NEVER 使用過多技術術語
