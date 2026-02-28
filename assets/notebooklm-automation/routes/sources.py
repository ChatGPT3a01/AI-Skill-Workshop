"""來源管理 API"""
from flask import jsonify, request
from . import api_bp
from services.notebooklm_service import notebooklm_service

@api_bp.route('/notebooks/<notebook_id>/sources', methods=['GET'])
def list_sources(notebook_id):
    """列出筆記本的來源"""
    result = notebooklm_service.list_sources(notebook_id)
    return jsonify(result)

@api_bp.route('/notebooks/<notebook_id>/sources', methods=['POST'])
def add_source(notebook_id):
    """新增來源"""
    data = request.get_json()
    source_type = data.get('type', 'url')
    source_value = data.get('value', '')

    if not source_value:
        return jsonify({"success": False, "error": "請提供來源內容"}), 400

    if source_type == 'url':
        result = notebooklm_service.add_source_url(source_value, notebook_id)
    elif source_type == 'file':
        result = notebooklm_service.add_source_file(source_value, notebook_id)
    else:
        result = notebooklm_service.add_source_url(source_value, notebook_id)

    return jsonify(result)

@api_bp.route('/notebooks/<notebook_id>/sources/<source_id>', methods=['DELETE'])
def delete_source(notebook_id, source_id):
    """刪除來源"""
    result = notebooklm_service.delete_source(source_id, notebook_id)
    return jsonify(result)

@api_bp.route('/notebooks/<notebook_id>/research', methods=['POST'])
def add_research(notebook_id):
    """新增研究"""
    data = request.get_json()
    query = data.get('query', '')
    mode = data.get('mode', 'fast')
    source = data.get('source', 'web')

    if not query:
        return jsonify({"success": False, "error": "請提供搜尋關鍵字"}), 400

    result = notebooklm_service.add_research(query, notebook_id, mode, source)
    return jsonify(result)
