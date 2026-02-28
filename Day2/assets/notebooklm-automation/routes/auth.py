"""認證相關 API"""
from flask import jsonify
from . import api_bp
from services.notebooklm_service import notebooklm_service

@api_bp.route('/auth/status', methods=['GET'])
def get_auth_status():
    """檢查認證狀態"""
    result = notebooklm_service.check_auth_status()
    return jsonify(result)

@api_bp.route('/auth/login', methods=['POST'])
def trigger_login():
    """觸發瀏覽器登入"""
    result = notebooklm_service.trigger_login()
    return jsonify(result)
