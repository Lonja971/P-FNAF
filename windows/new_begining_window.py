import os, json, time
from core.window.base import Window
from utils.terminal import clear
from ui.elements import input_field, render_menu

class NewBeginingWindow(Window):
    def __init__(self):
        self.default_interlocutor = "chief"
        self.dialog_interlocutors = {
            "chief": {
                "name": "[ШЕФ]",
            },
            "me": {
                "name": "[Я]",
            }
        }

    def ensure_save_file(self, save_path="config/save.json", template_path="config/save.template.json"):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            with open(template_path, "r", encoding="utf-8") as template_file:
                template_data = json.load(template_file)

            with open(save_path, "w", encoding="utf-8") as save_file:
                json.dump(template_data, save_file, indent=4, ensure_ascii=False)

            return template_data

        except FileNotFoundError:
            return None
        except json.JSONDecodeError as e:
            return None

    def print_dialog_phrase(self, text, who=None, is_new_line=False):
        if who is None or who not in self.dialog_interlocutors:
            who = self.default_interlocutor
        print(f"{"\n" if is_new_line else ""}{self.dialog_interlocutors[who]["name"]} {text}")

    def render_window(self, wm):
        clear()
        save = self.ensure_save_file()

        while True:
            self.print_dialog_phrase("Як звуть нашого нового охоронця?")
            name = input_field()
            if not name.strip():
                self.print_dialog_phrase("Вибачте, я нерозчув...", "", True)
            else:
                break

        self.print_dialog_phrase(f"Мене звати {name}.", "me")

        save["player"]["name"] = name
        self.overwrite_json("config/save.json", save)

        time.sleep(1.5)
        self.print_dialog_phrase(f"Вітаю в піцерії, {name}!", "", True)
        time.sleep(3)
        clear()
        time.sleep(3)
        return wm.pop()