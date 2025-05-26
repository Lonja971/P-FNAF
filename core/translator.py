import json
import os
from utils.terminal import load_config

class Translator:
    def __init__(self, path="locales"):
        config = load_config("config.json")

        self.language_code = config.get("language", "en")
        self.path = path
        self.translations = {}
        self.load_translations()

    def update_config(self):
        config = load_config("config.json")
        self.language_code = config.get("language", "en")
        self.load_translations()

    def load_translations(self):
        file_path = os.path.join(self.path, f"{self.language_code}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print(f"[WARN] Translation file {file_path} not found.")
            self.translations = {}

    def t(self, key, **kwargs):
        raw = self.translations.get(key, f"[{key}]")
        return raw.format(**kwargs)