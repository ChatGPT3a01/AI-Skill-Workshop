---
name: proposal-workflow
description: >
  客戶提案全流程自動化工作鏈。
  當使用者要求「走完提案流程」「從需求到提案」時使用。
  此技能依序呼叫 need-analyzer、proposal-drafter、
  proposal-reviewer 完成完整提案流程。
---

# 客戶提案工作流程

## 執行流程（5個階段）

### Phase 1：需求收集與確認
- Ask user 提供客戶的原始需求描述
- MUST 確認資訊足夠才能繼續

### Phase 2：需求分析（need-analyzer 邏輯）
- 依照 need-analyzer 規則分析需求
- 展示結果 → Ask user 確認

### Phase 3：撰寫提案（proposal-drafter 邏輯）
- Ask user 補充公司優勢和報價範圍
- 依照 proposal-drafter 規則撰寫提案

### Phase 4：審查定稿（proposal-reviewer 邏輯）
- 依照 proposal-reviewer 規則審查
- 自動修正明確問題，人工判斷大改動

### Phase 5：輸出交付
- MUST 產出最終版提案書（完整 Markdown）

## 進度顯示（每個階段都要顯示）
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 目前進度：Phase N/5 - [階段名稱]
[■■■□□] 60%
━━━━━━━━━━━━━━━━━━━━━━━━━━━
