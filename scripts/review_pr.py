#!/usr/bin/env python3
import os
import subprocess


def get_pr_diff() -> str:
    for base_branch in ["origin/main", "origin/master", "main", "master"]:
        result = subprocess.run(
            ["git", "diff", base_branch, "--stat"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            diff_result = subprocess.run(
                ["git", "diff", base_branch, "--", "*.py", "*.js", "*.ts", "*.go", "*.java"],
                capture_output=True, text=True
            )
            if diff_result.stdout:
                return diff_result.stdout[:8000]
    return os.getenv("PR_DIFF", "")


def review_with_claude(diff: str, pr_title: str, pr_body: str) -> str:
    if not diff:
        return "⚠️ 無法取得 PR diff，跳過 AI 審查"

    prompt = f"""你是一位資深程式碼審查員。請審查以下 Pull Request。

PR 標題：{pr_title}
PR 描述：{pr_body or '（無描述）'}

程式碼變更（git diff）：
```
{diff}
```

請以繁體中文提供審查意見，格式如下：

## 整體評估
（用 2-3 句話描述這個 PR 的整體品質）

## ✅ 做得好的地方
（列出值得稱讚的地方，至少 1 點）

## ⚠️ 需要注意的地方
（列出問題或建議，每點要有具體的修改建議）

## 🔐 安全性
（有無安全疑慮？沒有的話寫「未發現安全疑慮」）

## 結論
**可以合併** 或 **建議修改後再合併** 或 **需要重大修改**
（一行說明原因）"""

    try:
        result = subprocess.run(
            ["claude", "--print", "--model", "claude-sonnet-4-6"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "")}
        )
        if result.returncode != 0:
            return f"❌ Claude 審查失敗：{result.stderr[:500]}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "❌ Claude 審查逾時（超過 120 秒）"
    except FileNotFoundError:
        return "❌ 找不到 claude 指令，請確認 Claude Code 已安裝"


def post_to_github_summary(review: str, pr_number: str):
    summary_file = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(f"# 🤖 Claude AI 程式碼審查\n\n")
            f.write(f"**PR #{pr_number}**\n\n")
            f.write(review)
            f.write("\n\n---\n*由 Claude Code 自動審查*\n")
        print("✅ 審查結果已寫入 GitHub Summary")
    else:
        print("\n" + "=" * 60)
        print("  Claude AI 程式碼審查結果")
        print("=" * 60)
        print(review)
        print("=" * 60)


def main():
    pr_number = os.getenv("PR_NUMBER", "?")
    pr_title = os.getenv("PR_TITLE", "未知標題")
    pr_body = os.getenv("PR_BODY", "")

    print(f"🔍 開始審查 PR #{pr_number}：{pr_title}")
    print("📂 取得程式碼差異...")
    diff = get_pr_diff()

    if not diff:
        print("⚠️ 沒有找到程式碼差異，跳過審查")
        post_to_github_summary("無法取得 PR diff，跳過自動審查", pr_number)
        return

    print(f"✅ 取得 diff（{len(diff)} 字元）")
    print("🤖 Claude 正在審查...")
    review = review_with_claude(diff, pr_title, pr_body)
    post_to_github_summary(review, pr_number)


if __name__ == "__main__":
    main()
