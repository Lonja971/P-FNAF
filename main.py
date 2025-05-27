from utils.terminal import load_json_data, ensure_json_file

config = load_json_data("config.json")
if not config:
    ensure_json_file("config.json", "config.template.json")

from core.window.manager import WindowManager
from core.translator import Translator


def main():
    translator = Translator()

    wm = WindowManager("main", translator)
    wm.run()

if __name__ == "__main__":
    main()