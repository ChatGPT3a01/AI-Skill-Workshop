"""NotebookLM 操作服務封裝"""
import asyncio
import subprocess
import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

class NotebookLMService:
    """NotebookLM 操作服務類別"""

    def __init__(self):
        self.storage_path = Path.home() / ".notebooklm" / "storage_state.json"

    def _run_cli(self, args: List[str], timeout: int = 120) -> Dict[str, Any]:
        """執行 notebooklm CLI 指令"""
        try:
            cmd = ["notebooklm"] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )

            if result.returncode == 0:
                # 嘗試解析 JSON 輸出
                try:
                    return {"success": True, "data": json.loads(result.stdout)}
                except json.JSONDecodeError:
                    return {"success": True, "data": result.stdout.strip()}
            else:
                return {"success": False, "error": result.stderr.strip() or result.stdout.strip()}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "操作逾時"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ===== 認證相關 =====

    def check_auth_status(self) -> Dict[str, Any]:
        """檢查認證狀態"""
        result = self._run_cli(["auth", "check", "--json"])
        if result["success"]:
            return {
                "authenticated": True,
                "details": result["data"]
            }
        return {
            "authenticated": False,
            "error": result.get("error", "未登入")
        }

    def trigger_login(self) -> Dict[str, Any]:
        """觸發瀏覽器登入（非同步執行）"""
        try:
            # 使用 subprocess.Popen 啟動登入程序（不等待完成）
            subprocess.Popen(
                ["notebooklm", "login"],
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            return {"success": True, "message": "已開啟瀏覽器，請完成登入後按 Enter"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ===== 筆記本管理 =====

    def list_notebooks(self) -> Dict[str, Any]:
        """列出所有筆記本"""
        return self._run_cli(["list", "--json"])

    def create_notebook(self, title: str) -> Dict[str, Any]:
        """建立新筆記本"""
        return self._run_cli(["create", title, "--json"])

    def delete_notebook(self, notebook_id: str) -> Dict[str, Any]:
        """刪除筆記本"""
        return self._run_cli(["delete", notebook_id])

    def rename_notebook(self, notebook_id: str, new_title: str) -> Dict[str, Any]:
        """重命名筆記本"""
        return self._run_cli(["rename", notebook_id, new_title])

    def use_notebook(self, notebook_id: str) -> Dict[str, Any]:
        """設定當前使用的筆記本"""
        return self._run_cli(["use", notebook_id])

    def get_status(self) -> Dict[str, Any]:
        """取得當前狀態"""
        return self._run_cli(["status"])

    # ===== 來源管理 =====

    def list_sources(self, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """列出筆記本的來源"""
        args = ["source", "list", "--json"]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args)

    def add_source_url(self, url: str, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """新增 URL 來源"""
        args = ["source", "add", url, "--json"]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args)

    def add_source_file(self, file_path: str, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """新增檔案來源"""
        args = ["source", "add", file_path, "--json"]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args)

    def delete_source(self, source_id: str, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """刪除來源"""
        args = ["source", "delete", source_id]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args)

    # ===== 對話功能 =====

    def ask_question(self, question: str, notebook_id: Optional[str] = None,
                     new_conversation: bool = False) -> Dict[str, Any]:
        """向筆記本提問"""
        args = ["ask", question, "--json"]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        if new_conversation:
            args.append("--new")
        return self._run_cli(args, timeout=180)

    # ===== 內容生成 =====

    def generate_audio(self, notebook_id: Optional[str] = None,
                       instructions: str = "", format: str = "deep-dive") -> Dict[str, Any]:
        """生成音訊 Podcast"""
        args = ["generate", "audio", "--json", "--format", format]
        if instructions:
            args.append(instructions)
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args, timeout=60)

    def generate_video(self, notebook_id: Optional[str] = None,
                       instructions: str = "") -> Dict[str, Any]:
        """生成影片"""
        args = ["generate", "video", "--json"]
        if instructions:
            args.append(instructions)
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args, timeout=60)

    def generate_quiz(self, notebook_id: Optional[str] = None,
                      difficulty: str = "medium", quantity: str = "standard") -> Dict[str, Any]:
        """生成測驗"""
        args = ["generate", "quiz", "--json",
                "--difficulty", difficulty, "--quantity", quantity]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args, timeout=60)

    def generate_flashcards(self, notebook_id: Optional[str] = None,
                            difficulty: str = "medium", quantity: str = "standard") -> Dict[str, Any]:
        """生成閃卡"""
        args = ["generate", "flashcards", "--json",
                "--difficulty", difficulty, "--quantity", quantity]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args, timeout=60)

    def generate_report(self, notebook_id: Optional[str] = None,
                        format: str = "briefing-doc") -> Dict[str, Any]:
        """生成報告"""
        args = ["generate", "report", "--json", "--format", format]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args, timeout=60)

    def generate_mindmap(self, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """生成心智圖"""
        args = ["generate", "mind-map", "--json"]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args, timeout=60)

    # ===== 工件管理 =====

    def list_artifacts(self, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """列出工件"""
        args = ["artifact", "list", "--json"]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args)

    def wait_artifact(self, artifact_id: str, notebook_id: Optional[str] = None,
                      timeout: int = 600) -> Dict[str, Any]:
        """等待工件完成"""
        args = ["artifact", "wait", artifact_id, "--timeout", str(timeout)]
        if notebook_id:
            args.extend(["-n", notebook_id])
        return self._run_cli(args, timeout=timeout + 30)

    def download_artifact(self, artifact_type: str, output_path: str,
                          artifact_id: Optional[str] = None,
                          notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """下載工件"""
        args = ["download", artifact_type, output_path]
        if artifact_id:
            args.extend(["-a", artifact_id])
        if notebook_id:
            args.extend(["-n", notebook_id])
        return self._run_cli(args, timeout=300)

    # ===== 研究功能 =====

    def add_research(self, query: str, notebook_id: Optional[str] = None,
                     mode: str = "fast", source: str = "web") -> Dict[str, Any]:
        """新增研究"""
        args = ["source", "add-research", query, "--mode", mode, "--from", source]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        return self._run_cli(args, timeout=300)


# 建立單例
notebooklm_service = NotebookLMService()
