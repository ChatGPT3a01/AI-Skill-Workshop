"""內容生成 API"""
from flask import jsonify, request
from . import api_bp
from services.notebooklm_service import notebooklm_service
from services.task_manager import task_manager

@api_bp.route('/notebooks/<notebook_id>/generate/<artifact_type>', methods=['POST'])
def generate_artifact(notebook_id, artifact_type):
    """生成內容"""
    data = request.get_json() or {}

    # 根據類型呼叫對應的生成方法
    if artifact_type == 'audio':
        instructions = data.get('instructions', '')
        format_type = data.get('format', 'deep-dive')

        # 建立背景任務
        task_id = task_manager.create_task(
            name=f"生成 Podcast",
            func=notebooklm_service.generate_audio,
            kwargs={
                "notebook_id": notebook_id,
                "instructions": instructions,
                "format": format_type
            }
        )
        return jsonify({"success": True, "task_id": task_id, "message": "已開始生成 Podcast"})

    elif artifact_type == 'video':
        instructions = data.get('instructions', '')

        task_id = task_manager.create_task(
            name=f"生成影片",
            func=notebooklm_service.generate_video,
            kwargs={
                "notebook_id": notebook_id,
                "instructions": instructions
            }
        )
        return jsonify({"success": True, "task_id": task_id, "message": "已開始生成影片"})

    elif artifact_type == 'quiz':
        difficulty = data.get('difficulty', 'medium')
        quantity = data.get('quantity', 'standard')

        task_id = task_manager.create_task(
            name=f"生成測驗",
            func=notebooklm_service.generate_quiz,
            kwargs={
                "notebook_id": notebook_id,
                "difficulty": difficulty,
                "quantity": quantity
            }
        )
        return jsonify({"success": True, "task_id": task_id, "message": "已開始生成測驗"})

    elif artifact_type == 'flashcards':
        difficulty = data.get('difficulty', 'medium')
        quantity = data.get('quantity', 'standard')

        task_id = task_manager.create_task(
            name=f"生成閃卡",
            func=notebooklm_service.generate_flashcards,
            kwargs={
                "notebook_id": notebook_id,
                "difficulty": difficulty,
                "quantity": quantity
            }
        )
        return jsonify({"success": True, "task_id": task_id, "message": "已開始生成閃卡"})

    elif artifact_type == 'report':
        format_type = data.get('format', 'briefing-doc')

        task_id = task_manager.create_task(
            name=f"生成報告",
            func=notebooklm_service.generate_report,
            kwargs={
                "notebook_id": notebook_id,
                "format": format_type
            }
        )
        return jsonify({"success": True, "task_id": task_id, "message": "已開始生成報告"})

    elif artifact_type == 'mindmap':
        result = notebooklm_service.generate_mindmap(notebook_id)
        return jsonify(result)

    else:
        return jsonify({"success": False, "error": f"不支援的類型: {artifact_type}"}), 400


@api_bp.route('/notebooks/<notebook_id>/artifacts', methods=['GET'])
def list_artifacts(notebook_id):
    """列出工件"""
    result = notebooklm_service.list_artifacts(notebook_id)
    return jsonify(result)


@api_bp.route('/notebooks/<notebook_id>/ask', methods=['POST'])
def ask_question(notebook_id):
    """向筆記本提問"""
    data = request.get_json()
    question = data.get('question', '')
    new_conversation = data.get('new', False)

    if not question:
        return jsonify({"success": False, "error": "請提供問題"}), 400

    result = notebooklm_service.ask_question(question, notebook_id, new_conversation)
    return jsonify(result)


@api_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """取得任務狀態"""
    task = task_manager.get_task(task_id)
    if task:
        return jsonify({"success": True, "task": task})
    return jsonify({"success": False, "error": "任務不存在"}), 404


@api_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """列出所有任務"""
    tasks = task_manager.get_all_tasks()
    return jsonify({"success": True, "tasks": tasks})
