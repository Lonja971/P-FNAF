from utils.terminal import load_json_data, ensure_json_file

is_first_time = False
config = load_json_data("config.json")
if not config:
    is_first_time = True
    ensure_json_file("config.json", "config.template.json")

from core.window.manager import WindowManager
from core.translator import Translator


def main():
    translator = Translator()

    if is_first_time:
        wm = WindowManager("change_lanquage", translator)
    else:
        wm = WindowManager("main", translator)
    wm.run()

if __name__ == "__main__":
    main()