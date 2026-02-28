"""使用者設定管理"""
import json
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """設定管理類別"""

    DEFAULT_CONFIG = {
        "nlp_mode": "keyword",
        "gemini_api_key": "",
        "gemini_model": "gemini-2.5-flash",
        "openai_api_key": "",
        "openai_model": "gpt-4o",
        "theme": "modern",
        "language": "zh_Hant"
    }

    # 可用的選項
    NLP_MODES = ["keyword", "gemini", "openai"]
    THEMES = ["modern", "rich", "dark", "light"]
    GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3.0-flash", "gemini-3.0-pro"]
    OPENAI_MODELS = ["gpt-4o", "gpt-4.1", "gpt-4-turbo", "gpt-5.1"]

    def __init__(self, config_path: Optional[str] = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = Path(__file__).parent.parent / "config.json"
        self._config = None

    def load(self) -> Dict[str, Any]:
        """載入設定"""
        if self._config is not None:
            return self._config

        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                # 補齊缺少的欄位
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in self._config:
                        self._config[key] = value
            except (json.JSONDecodeError, IOError):
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
            self.save()

        return self._config

    def save(self) -> bool:
        """儲存設定"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config or self.DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """取得設定值"""
        config = self.load()
        return config.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """設定值"""
        config = self.load()
        config[key] = value
        self._config = config
        return self.save()

    def update(self, updates: Dict[str, Any]) -> bool:
        """批次更新設定"""
        config = self.load()
        config.update(updates)
        self._config = config
        return self.save()

    def get_all(self) -> Dict[str, Any]:
        """取得所有設定"""
        return self.load()

    def get_options(self) -> Dict[str, Any]:
        """取得所有可用選項"""
        return {
            "nlp_modes": self.NLP_MODES,
            "themes": self.THEMES,
            "gemini_models": self.GEMINI_MODELS,
            "openai_models": self.OPENAI_MODELS
        }


# 建立單例
config_manager = ConfigManager()
