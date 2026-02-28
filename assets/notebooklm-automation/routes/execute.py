"""自然語言執行 API"""
from flask import jsonify, request
from . import api_bp
from services.nlp_parser import nlp_parser
from services.notebooklm_service import notebooklm_service
from services.task_manager import task_manager

@api_bp.route('/execute', methods=['POST'])
def execute_command():
    """執行自然語言指令"""
    data = request.get_json()
    command = data.get('command', '')
    notebook_id = data.get('notebook_id')  # 可選，指定筆記本

    if not command:
        return jsonify({"success": False, "error": "請提供指令"}), 400

    # 解析自然語言
    parsed = nlp_parser.parse(command)
    intent = parsed.get('intent')
    params = parsed.get('params', {})

    if not intent:
        return jsonify({
            "success": False,
            "error": "無法理解您的指令，請嘗試更明確的描述",
            "parsed": parsed
        })

    # 根據意圖執行對應操作
    result = _execute_intent(intent, params, notebook_id)
    result["parsed"] = parsed

    return jsonify(result)


def _execute_intent(intent: str, params: dict, notebook_id: str = None) -> dict:
    """根據意圖執行操作"""

    # ===== 筆記本管理 =====
    if intent == "list_notebooks":
        return notebooklm_service.list_notebooks()

    elif intent == "create_notebook":
        name = params.get('name', '新筆記本')
        return notebooklm_service.create_notebook(name)

    elif intent == "delete_notebook":
        nb_id = params.get('notebook_id') or notebook_id
        if not nb_id:
            return {"success": False, "error": "請指定要刪除的筆記本"}
        return notebooklm_service.delete_notebook(nb_id)

    elif intent == "use_notebook":
        nb_id = params.get('notebook_id') or notebook_id
        if not nb_id:
            return {"success": False, "error": "請指定要使用的筆記本"}
        return notebooklm_service.use_notebook(nb_id)

    elif intent == "check_status":
        return notebooklm_service.get_status()

    # ===== 來源管理 =====
    elif intent == "list_sources":
        return notebooklm_service.list_sources(notebook_id)

    elif intent == "add_source_url":
        url = params.get('url')
        if not url:
            return {"success": False, "error": "請提供網址"}
        return notebooklm_service.add_source_url(url, notebook_id)

    elif intent == "add_source_youtube":
        url = params.get('youtube_url') or params.get('url')
        if not url:
            return {"success": False, "error": "請提供 YouTube 網址"}
        return notebooklm_service.add_source_url(url, notebook_id)

    elif intent == "add_source_file":
        file_path = params.get('file_path')
        if not file_path:
            return {"success": False, "error": "請提供檔案路徑"}
        return notebooklm_service.add_source_file(file_path, notebook_id)

    # ===== 對話功能 =====
    elif intent == "ask_question":
        question = params.get('question')
        if not question:
            return {"success": False, "error": "請提供問題"}
        return notebooklm_service.ask_question(question, notebook_id)

    # ===== 內容生成 =====
    elif intent == "generate_audio":
        task_id = task_manager.create_task(
            name="生成 Podcast",
            func=notebooklm_service.generate_audio,
            kwargs={"notebook_id": notebook_id}
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成 Podcast，請稍候..."}

    elif intent == "generate_video":
        task_id = task_manager.create_task(
            name="生成影片",
            func=notebooklm_service.generate_video,
            kwargs={"notebook_id": notebook_id}
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成影片，請稍候..."}

    elif intent == "generate_quiz":
        quantity = "more" if params.get('quantity', 0) > 10 else "standard"
        task_id = task_manager.create_task(
            name="生成測驗",
            func=notebooklm_service.generate_quiz,
            kwargs={"notebook_id": notebook_id, "quantity": quantity}
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成測驗，請稍候..."}

    elif intent == "generate_flashcards":
        task_id = task_manager.create_task(
            name="生成閃卡",
            func=notebooklm_service.generate_flashcards,
            kwargs={"notebook_id": notebook_id}
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成閃卡，請稍候..."}

    elif intent == "generate_report":
        task_id = task_manager.create_task(
            name="生成報告",
            func=notebooklm_service.generate_report,
            kwargs={"notebook_id": notebook_id}
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成報告，請稍候..."}

    elif intent == "generate_mindmap":
        return notebooklm_service.generate_mindmap(notebook_id)

    elif intent == "generate_infographic":
        task_id = task_manager.create_task(
            name="生成資訊圖",
            func=lambda: notebooklm_service._run_cli(
                ["generate", "infographic", "--json", "--notebook", notebook_id] if notebook_id
                else ["generate", "infographic", "--json"]
            )
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成資訊圖，請稍候..."}

    elif intent == "generate_slides":
        task_id = task_manager.create_task(
            name="生成簡報",
            func=lambda: notebooklm_service._run_cli(
                ["generate", "slide-deck", "--json", "--notebook", notebook_id] if notebook_id
                else ["generate", "slide-deck", "--json"]
            )
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成簡報，請稍候..."}

    elif intent == "generate_datatable":
        task_id = task_manager.create_task(
            name="生成數據表",
            func=lambda: notebooklm_service._run_cli(
                ["generate", "data-table", "--json", "--notebook", notebook_id] if notebook_id
                else ["generate", "data-table", "--json"]
            )
        )
        return {"success": True, "task_id": task_id, "message": "已開始生成數據表，請稍候..."}

    # ===== 工件管理 =====
    elif intent == "list_artifacts":
        return notebooklm_service.list_artifacts(notebook_id)

    elif intent == "download":
        # 下載需要更多參數，回傳提示
        return {
            "success": False,
            "error": "請指定要下載的內容類型（audio/video/report/mindmap 等）",
            "hint": "例如：下載 Podcast、下載報告"
        }

    # ===== 研究功能 =====
    elif intent == "research":
        query = params.get('question') or params.get('name')
        if not query:
            return {"success": False, "error": "請提供搜尋關鍵字"}
        return notebooklm_service.add_research(query, notebook_id)

    # ===== 幫助 =====
    elif intent == "help":
        return {
            "success": True,
            "message": "可用指令請參考功能總覽頁面",
            "categories": [
                "筆記本管理：建立、列出、刪除、重命名筆記本",
                "來源匯入：新增 URL、YouTube、檔案",
                "互動對話：向筆記本提問",
                "內容生成：Podcast、影片、測驗、閃卡、報告、心智圖",
                "下載匯出：下載生成的內容"
            ]
        }

    else:
        return {
            "success": False,
            "error": f"不支援的操作: {intent}"
        }
