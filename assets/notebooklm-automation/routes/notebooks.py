"""筆記本管理 API"""
from flask import jsonify, request
from . import api_bp
from services.notebooklm_service import notebooklm_service

@api_bp.route('/notebooks', methods=['GET'])
def list_notebooks():
    """列出所有筆記本"""
    result = notebooklm_service.list_notebooks()
    return jsonify(result)

@api_bp.route('/notebooks', methods=['POST'])
def create_notebook():
    """建立新筆記本"""
    data = request.get_json()
    title = data.get('title', '新筆記本')
    result = notebooklm_service.create_notebook(title)
    return jsonify(result)

@api_bp.route('/notebooks/<notebook_id>', methods=['DELETE'])
def delete_notebook(notebook_id):
    """刪除筆記本"""
    result = notebooklm_service.delete_notebook(notebook_id)
    return jsonify(result)

@api_bp.route('/notebooks/<notebook_id>/rename', methods=['POST'])
def rename_notebook(notebook_id):
    """重命名筆記本"""
    data = request.get_json()
    new_title = data.get('title', '')
    if not new_title:
        return jsonify({"success": False, "error": "請提供新名稱"}), 400
    result = notebooklm_service.rename_notebook(notebook_id, new_title)
    return jsonify(result)

@api_bp.route('/notebooks/<notebook_id>/use', methods=['POST'])
def use_notebook(notebook_id):
    """設定當前使用的筆記本"""
    result = notebooklm_service.use_notebook(notebook_id)
    return jsonify(result)

@api_bp.route('/notebooks/status', methods=['GET'])
def get_notebook_status():
    """取得當前狀態"""
    result = notebooklm_service.get_status()
    return jsonify(result)
