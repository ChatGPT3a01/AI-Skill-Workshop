"""Flask 應用程式設定"""
import os

class Config:
    """基礎設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'notebooklm-skill-secret-key'
    JSON_AS_ASCII = False  # 支援中文 JSON

class DevelopmentConfig(Config):
    """開發環境設定"""
    DEBUG = True

class ProductionConfig(Config):
    """生產環境設定"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
