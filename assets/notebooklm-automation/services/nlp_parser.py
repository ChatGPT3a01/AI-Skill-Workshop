"""自然語言解析器"""
import re
from typing import Dict, Any, Optional, List, Tuple
from .config_manager import config_manager

class NLPParser:
    """自然語言解析器類別"""

    # 意圖模式 - 關鍵字匹配
    INTENT_PATTERNS = {
        "list_notebooks": [
            "列出筆記本", "顯示筆記本", "我的筆記本", "筆記本列表",
            "所有筆記本", "查看筆記本"
        ],
        "create_notebook": [
            "建立筆記本", "新增筆記本", "創建筆記本", "新建筆記本"
        ],
        "delete_notebook": [
            "刪除筆記本", "移除筆記本"
        ],
        "use_notebook": [
            "使用筆記本", "選擇筆記本", "切換筆記本", "打開筆記本"
        ],
        "list_sources": [
            "列出來源", "顯示來源", "來源列表", "查看來源"
        ],
        "add_source_url": [
            "加入網址", "新增URL", "匯入網頁", "加入連結",
            "新增網址", "添加網頁"
        ],
        "add_source_youtube": [
            "加入YouTube", "新增影片", "匯入影片", "加入視頻",
            "YouTube影片"
        ],
        "add_source_file": [
            "上傳檔案", "新增檔案", "加入PDF", "匯入文件",
            "上傳PDF", "加入檔案"
        ],
        "ask_question": [
            "問", "查詢", "詢問", "問一下", "請問", "幫我問"
        ],
        "generate_audio": [
            "生成Podcast", "製作音訊", "產生播客", "生成音檔",
            "製作Podcast", "做Podcast", "建立Podcast"
        ],
        "generate_video": [
            "生成影片", "製作視頻", "產生影片", "做影片"
        ],
        "generate_quiz": [
            "生成測驗", "製作題目", "出題", "產生測驗",
            "做測驗", "建立測驗"
        ],
        "generate_flashcards": [
            "生成閃卡", "製作字卡", "產生閃卡", "做閃卡",
            "建立閃卡"
        ],
        "generate_report": [
            "生成報告", "製作摘要", "產生報告", "做報告",
            "建立報告"
        ],
        "generate_mindmap": [
            "生成心智圖", "製作心智圖", "產生心智圖", "做心智圖",
            "建立心智圖", "心智圖"
        ],
        "generate_infographic": [
            "生成資訊圖", "製作圖表", "產生資訊圖", "做資訊圖"
        ],
        "generate_slides": [
            "生成簡報", "製作投影片", "產生簡報", "做簡報",
            "建立簡報"
        ],
        "generate_datatable": [
            "生成數據表", "製作表格", "產生數據表", "做數據表",
            "建立數據表", "生成資料表"
        ],
        "download": [
            "下載", "匯出", "儲存", "導出"
        ],
        "list_artifacts": [
            "列出工件", "顯示工件", "查看生成內容", "工件列表"
        ],
        "research": [
            "搜尋", "研究", "查找資料", "網頁研究"
        ],
        "check_status": [
            "狀態", "目前狀態", "查看狀態"
        ],
        "help": [
            "幫助", "說明", "怎麼用", "功能"
        ]
    }

    # 參數提取模式
    PARAM_PATTERNS = {
        "notebook_name": r"[「『\"]([^」』\"]+)[」』\"]|叫做\s*(\S+)|名為\s*(\S+)|名稱\s*(\S+)",
        "url": r"(https?://[^\s]+)",
        "youtube": r"((?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)",
        "file_path": r"([A-Za-z]:\\[^\s]+|/[^\s]+|\./[^\s]+)",
        "quantity": r"(\d+)\s*(?:題|個|張)",
    }

    def __init__(self):
        self.config = config_manager

    def parse(self, text: str) -> Dict[str, Any]:
        """解析自然語言輸入"""
        nlp_mode = self.config.get("nlp_mode", "keyword")

        if nlp_mode == "keyword":
            return self._parse_keyword(text)
        elif nlp_mode == "gemini":
            return self._parse_with_gemini(text)
        elif nlp_mode == "openai":
            return self._parse_with_openai(text)
        else:
            return self._parse_keyword(text)

    def _parse_keyword(self, text: str) -> Dict[str, Any]:
        """使用關鍵字匹配解析"""
        text_lower = text.lower()

        # 找出意圖
        intent = None
        confidence = 0.0

        for intent_name, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    intent = intent_name
                    confidence = 0.9
                    break
            if intent:
                break

        if not intent:
            # 嘗試模糊匹配
            intent = self._fuzzy_match(text_lower)
            confidence = 0.6 if intent else 0.0

        # 提取參數
        params = self._extract_params(text)

        return {
            "intent": intent,
            "confidence": confidence,
            "params": params,
            "original_text": text,
            "parse_mode": "keyword"
        }

    def _fuzzy_match(self, text: str) -> Optional[str]:
        """模糊匹配意圖"""
        # 簡單的關鍵字檢測
        if "筆記本" in text and ("建" in text or "新" in text or "創" in text):
            return "create_notebook"
        if "筆記本" in text and ("列" in text or "顯" in text or "看" in text):
            return "list_notebooks"
        if "podcast" in text.lower() or "播客" in text or "音訊" in text:
            return "generate_audio"
        if "影片" in text or "視頻" in text or "video" in text.lower():
            return "generate_video"
        if "測驗" in text or "題目" in text or "quiz" in text.lower():
            return "generate_quiz"
        if "閃卡" in text or "字卡" in text or "flashcard" in text.lower():
            return "generate_flashcards"
        if "報告" in text or "摘要" in text or "report" in text.lower():
            return "generate_report"
        if "心智圖" in text or "mindmap" in text.lower():
            return "generate_mindmap"
        if "資訊圖" in text or "圖表" in text or "infographic" in text.lower():
            return "generate_infographic"
        if "簡報" in text or "投影片" in text or "slides" in text.lower():
            return "generate_slides"
        if "數據表" in text or "資料表" in text or "表格" in text or "datatable" in text.lower():
            return "generate_datatable"
        if "下載" in text or "匯出" in text or "download" in text.lower():
            return "download"
        if "問" in text or "查詢" in text or "?" in text or "？" in text:
            return "ask_question"
        if "來源" in text and ("加" in text or "新" in text):
            return "add_source_url"
        if "youtube" in text.lower() or "yt" in text.lower():
            return "add_source_youtube"

        return None

    def _extract_params(self, text: str) -> Dict[str, Any]:
        """提取參數"""
        params = {}

        # 提取筆記本名稱
        for pattern in [r"[「『\"]([^」』\"]+)[」』\"]", r"叫做\s*[「『\"]?(\S+)[」』\"]?", r"名為\s*(\S+)"]:
            match = re.search(pattern, text)
            if match:
                params["name"] = match.group(1)
                break

        # 提取 URL
        url_match = re.search(r"(https?://[^\s]+)", text)
        if url_match:
            params["url"] = url_match.group(1)

        # 提取 YouTube URL
        yt_match = re.search(r"((?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)", text)
        if yt_match:
            params["youtube_url"] = yt_match.group(1)

        # 提取數量
        qty_match = re.search(r"(\d+)\s*(?:題|個|張)", text)
        if qty_match:
            params["quantity"] = int(qty_match.group(1))

        # 提取問題內容（對於 ask_question 意圖）
        question_patterns = [
            r"問[一]?下?\s*[「『\"]?(.+?)[」』\"]?\s*$",
            r"查詢\s*[「『\"]?(.+?)[」』\"]?\s*$",
            r"請問\s*(.+)",
        ]
        for pattern in question_patterns:
            match = re.search(pattern, text)
            if match:
                params["question"] = match.group(1).strip()
                break

        return params

    def _parse_with_gemini(self, text: str) -> Dict[str, Any]:
        """使用 Gemini API 解析"""
        api_key = self.config.get("gemini_api_key")
        model = self.config.get("gemini_model", "gemini-2.5-flash")

        if not api_key:
            # 沒有 API Key，回退到關鍵字匹配
            result = self._parse_keyword(text)
            result["parse_mode"] = "keyword (gemini fallback - no api key)"
            return result

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            prompt = self._build_llm_prompt(text)
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(prompt)

            return self._parse_llm_response(response.text, text, "gemini")
        except Exception as e:
            # 錯誤時回退到關鍵字匹配
            result = self._parse_keyword(text)
            result["parse_mode"] = f"keyword (gemini error: {str(e)})"
            return result

    def _parse_with_openai(self, text: str) -> Dict[str, Any]:
        """使用 OpenAI API 解析"""
        api_key = self.config.get("openai_api_key")
        model = self.config.get("openai_model", "gpt-4o")

        if not api_key:
            # 沒有 API Key，回退到關鍵字匹配
            result = self._parse_keyword(text)
            result["parse_mode"] = "keyword (openai fallback - no api key)"
            return result

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            prompt = self._build_llm_prompt(text)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            return self._parse_llm_response(response.choices[0].message.content, text, "openai")
        except Exception as e:
            # 錯誤時回退到關鍵字匹配
            result = self._parse_keyword(text)
            result["parse_mode"] = f"keyword (openai error: {str(e)})"
            return result

    def _build_llm_prompt(self, text: str) -> str:
        """建構 LLM 提示詞"""
        intents = list(self.INTENT_PATTERNS.keys())

        return f"""分析以下使用者輸入，判斷其意圖和參數。

使用者輸入：{text}

可能的意圖（選擇一個最匹配的）：
{', '.join(intents)}

請以 JSON 格式回覆：
{{
  "intent": "意圖名稱",
  "confidence": 0.0-1.0 的信心分數,
  "params": {{
    "name": "筆記本名稱（如有）",
    "url": "網址（如有）",
    "question": "問題內容（如有）",
    "quantity": 數量（如有）
  }}
}}

只回覆 JSON，不要其他文字。"""

    def _parse_llm_response(self, response: str, original_text: str, mode: str) -> Dict[str, Any]:
        """解析 LLM 回應"""
        import json

        try:
            # 嘗試提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "intent": data.get("intent"),
                    "confidence": data.get("confidence", 0.8),
                    "params": data.get("params", {}),
                    "original_text": original_text,
                    "parse_mode": mode
                }
        except json.JSONDecodeError:
            pass

        # 解析失敗，回退到關鍵字匹配
        result = self._parse_keyword(original_text)
        result["parse_mode"] = f"keyword ({mode} parse failed)"
        return result


# 建立單例
nlp_parser = NLPParser()
