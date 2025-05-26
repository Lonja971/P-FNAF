from core.window.base import Window
from ui.elements import render_menu, input_field
import os, json
from utils.terminal import clear

class ChangeLanquageWindow(Window):
    def get_lang_label(self, lang_code: str) -> str:
        mapping = {
            "en": "English",
            "ua": "Українська",
            "pl": "Polski"
        }
        return mapping.get(lang_code, lang_code)

    def apply_language(self, wm, lang_code: str):
        config_path = "config.json"
        
        # Читання → модифікація → запис
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        config["language"] = lang_code

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        # Тепер можна оновити перекладач
        wm.translator.update_config()

        print(f"Мову змінено на: {self.get_lang_label(lang_code)}")

        

        print(f"Мову змінено на: {self.get_lang_label(lang_code)}")

    def render_window(self, wm):
        left_padding = "  "
        clear()
        locale_dir = "locales"
        locale_files = [f for f in os.listdir(locale_dir) if f.endswith(".json")]

        if not locale_files:
            print("Не знайдено жодного файлу перекладу.")
            return

        # Список (Назва, Ключ, Action)
        menu = []
        for file in locale_files:
            lang_code = file[:-5]
            label = self.get_lang_label(lang_code)  # e.g. "Українська", "English"
            menu.append((label, None, lambda wm=wm, lc=lang_code: (self.apply_language(wm, lc), wm.pop())))

        print("Оберіть мову інтерфейсу:\n")
        menu_actions = render_menu(menu)

        while True:
            choice = input_field().strip()
            action = menu_actions.get(choice)
            if action:
                action()
                break
            else:
                msg = wm.translator.t("wrong_selection")
                print(f"{left_padding}{msg}")