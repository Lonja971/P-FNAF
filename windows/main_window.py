from core.window.base import Window
from utils.terminal import clear
from ui.elements import title, input_field, render_menu
from ui.pictures.logo import LOGO_PICTURE_DARK

class MainWindow(Window):
    def render_window(self, wm):
        while True:
            clear()
            print(LOGO_PICTURE_DARK)
            title("Головне вікно")

            menu_actions = render_menu([
                ("Грати", None, lambda wm: wm.switch_to("game")),
                ("Вийти", "q", lambda wm: wm.exit()),
            ])

            choice = input_field()
            action = menu_actions.get(choice)
            if action:
                action(wm)
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")