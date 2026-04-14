import json
import os

DEFAULT_SETTINGS = {
    "api_key": "",
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1024,
}

class SettingsFile:
    def __init__(self, filename=None):
        self.plugin_dir = os.path.dirname(__file__)
        self.path = filename or os.path.join(self.plugin_dir, "settings.json")
        self.settings = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    if isinstance(data, dict):
                        merged = DEFAULT_SETTINGS.copy()
                        merged.update(data)
                        return merged
            except (ValueError, OSError):
                pass
        return DEFAULT_SETTINGS.copy()

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fp:
            json.dump(self.settings, fp, indent=2)

    def get(self, key, default=None):
        return self.settings.get(key, default if default is not None else DEFAULT_SETTINGS.get(key))

    def get_int(self, key, default=None):
        return int(self.get(key, default))
    
    def get_float(self, key, default=None):
        return float(self.get(key, default))

    def set(self, key, value):
        self.settings[key] = value
        self.save()