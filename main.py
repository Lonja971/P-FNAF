import json
from core.window.manager import WindowManager
from core.translator import Translator

def main():
    translator = Translator()

    wm = WindowManager("main", translator)
    wm.run()

if __name__ == "__main__":
    main()