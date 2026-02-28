"""設定相關 API"""
from flask import jsonify, request
from . import api_bp
from services.config_manager import config_manager

@api_bp.route('/settings', methods=['GET'])
def get_settings():
    """取得所有設定"""
    config = config_manager.get_all()
    options = config_manager.get_options()

    # 隱藏 API Key 的完整內容
    safe_config = config.copy()
    if safe_config.get('gemini_api_key'):
        safe_config['gemini_api_key'] = '***' + safe_config['gemini_api_key'][-4:] if len(safe_config['gemini_api_key']) > 4 else '***'
    if safe_config.get('openai_api_key'):
        safe_config['openai_api_key'] = '***' + safe_config['openai_api_key'][-4:] if len(safe_config['openai_api_key']) > 4 else '***'

    return jsonify({
        "success": True,
        "config": safe_config,
        "options": options
    })

@api_bp.route('/settings', methods=['POST'])
def update_settings():
    """更新設定"""
    data = request.get_json()

    # 驗證設定值
    if 'nlp_mode' in data:
        if data['nlp_mode'] not in config_manager.NLP_MODES:
            return jsonify({"success": False, "error": f"無效的 NLP 模式: {data['nlp_mode']}"}), 400

    if 'theme' in data:
        if data['theme'] not in config_manager.THEMES:
            return jsonify({"success": False, "error": f"無效的主題: {data['theme']}"}), 400

    if 'gemini_model' in data:
        if data['gemini_model'] not in config_manager.GEMINI_MODELS:
            return jsonify({"success": False, "error": f"無效的 Gemini 模型: {data['gemini_model']}"}), 400

    if 'openai_model' in data:
        if data['openai_model'] not in config_manager.OPENAI_MODELS:
            return jsonify({"success": False, "error": f"無效的 OpenAI 模型: {data['openai_model']}"}), 400

    # 更新設定
    success = config_manager.update(data)

    if success:
        return jsonify({"success": True, "message": "設定已更新"})
    else:
        return jsonify({"success": False, "error": "儲存設定失敗"}), 500

@api_bp.route('/settings/options', methods=['GET'])
def get_options():
    """取得所有可用選項"""
    options = config_manager.get_options()
    return jsonify({"success": True, "options": options})
