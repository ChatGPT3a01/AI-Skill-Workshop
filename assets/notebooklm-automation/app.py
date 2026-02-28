"""
亮言~NotebookLM 自動化 Skill
Flask Web GUI 主程式
"""
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from config import config
from routes import api_bp

def create_app(config_name='default'):
    """建立 Flask 應用程式"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 啟用 CORS
    CORS(app)

    # 註冊 API Blueprint
    app.register_blueprint(api_bp)

    # ===== 頁面路由 =====

    @app.route('/')
    def splash():
        """啟動畫面"""
        return render_template('splash.html')

    @app.route('/main')
    def index():
        """主頁 - 執行介面"""
        return render_template('index.html')

    @app.route('/settings')
    def settings():
        """設定頁"""
        return render_template('settings.html')

    @app.route('/features')
    def features():
        """功能總覽頁"""
        return render_template('features.html')

    # 靜態檔案路由
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)

    return app


if __name__ == '__main__':
    app = create_app('development')
    print("\n" + "=" * 50)
    print("   亮言~NotebookLM 自動化Skill")
    print("=" * 50)
    print("\n   啟動網頁伺服器...")
    print("   請開啟瀏覽器訪問: http://localhost:5000")
    print("\n" + "=" * 50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
