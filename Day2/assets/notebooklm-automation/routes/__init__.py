"""API 路由模組"""
from flask import Blueprint

# 建立主要 Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 匯入各子路由
from . import auth, notebooks, sources, artifacts, execute, settings
