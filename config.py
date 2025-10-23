import os
import json

class Config:
    def __init__(self):
        self.config_file = "config.json"
        self.default_config = {
            "window_size": "800x600",
            "default_volume": 0.7,
            "supported_formats": {
                "audio": [".mp3", ".wav", ".flac", ".ogg", ".m4a"],
                "video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"]
            },
            "theme": {
                "background": "#2b2b2b",
                "foreground": "#ffffff",
                "button_bg": "#404040",
                "button_fg": "#ffffff"
            },
            "shortcuts": {
                "play_pause": "space",
                "stop": "s",
                "next": "right",
                "previous": "left",
                "volume_up": "up",
                "volume_down": "down",
                "fullscreen": "f11"
            }
        }
        self.config = self.load_config()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return self.merge_config(self.default_config, config)
            except:
                return self.default_config
        else:
            self.save_config(self.default_config)
            return self.default_config
            
    def save_config(self, config=None):
        if config is None:
            config = self.config
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Помилка збереження конфігурації: {e}")
            
    def merge_config(self, default, user):
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_config(result[key], value)
            else:
                result[key] = value
        return result
        
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
        
    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
