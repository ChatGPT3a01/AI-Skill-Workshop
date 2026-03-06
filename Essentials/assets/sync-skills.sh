#!/bin/bash
# sync-skills.sh - 將 skills-source 同步到各平台目錄
# 用法：在專案根目錄執行 bash sync-skills.sh

SKILL_SOURCE="./skills-source"
ANTIGRAVITY_DIR="./.agent/skills"
CLAUDE_DIR="./.claude/skills"

echo "🔄 開始同步 Skills..."
echo ""

# 同步到 Antigravity
cp -r "$SKILL_SOURCE"/* "$ANTIGRAVITY_DIR"/
echo "✅ 已同步到 Antigravity（.agent/skills/）"

# 同步到 Claude Code
cp -r "$SKILL_SOURCE"/* "$CLAUDE_DIR"/
echo "✅ 已同步到 Claude Code（.claude/skills/）"

echo ""
echo "🎉 全部同步完成！"
echo ""
echo "📁 同步結果："
echo "  skills-source/ → .agent/skills/"
echo "  skills-source/ → .claude/skills/"
