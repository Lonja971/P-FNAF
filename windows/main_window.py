from core.window.base import Window
from utils.terminal import clear
from ui.elements import title, input_field, render_menu
from ui.sprites.logo import LOGO_PICTURE_DARK
from config.nights import NIGHTS

class MainWindow(Window):
    def next_avaible_night(self, next_night_index):
        if next_night_index in NIGHTS:
            return next_night_index
        else:
            return self.next_avaible_night(next_night_index - 1)

    def start_new_game(self, wm):
        current_night = 1
        self.update_json_value("config/save.json", "complated_night", 0)

        wm.switch_to("game", current_night)
    def render_window(self, wm):
        left_padding = "  "
        save = self.load_save_data("config/save.json")
        if not save:
            return wm.switch_to("new_begining")
        
        next_night = save["complated_night"] + 1
        next_avaible_night = self.next_avaible_night(next_night)

        clear()
        print(LOGO_PICTURE_DARK)
        print(f"{left_padding}{wm.translator.t("have_a_good_shift", name=save["player"]["name"])}\n")

        menu_actions = render_menu([
            (wm.translator.t("new_game"), None, lambda wm: self.start_new_game(wm)),
            (f"{wm.translator.t("continue")} {next_avaible_night}", None, lambda wm: wm.switch_to("game", next_avaible_night)),
            (wm.translator.t("change_language"), None, lambda wm: wm.switch_to("change_lanquage")),
            (wm.translator.t("logout"), "q", lambda wm: wm.exit()),
        ], left_padding)
        while True:
            choice = input_field()
            action = menu_actions.get(choice)
            if action:
                action(wm)
                break
            else:
                print(f"{left_padding}{wm.translator.t("wrong_selection")}")