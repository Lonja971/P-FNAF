from core.window.base import Window
from utils.terminal import clear
from ui.elements import title, input_field, render_menu
from ui.sprites.logo import LOGO_PICTURE_DARK
from config.nights import NIGHTS

class MainWindow(Window):
    def __init__(self):
        self.is_first = True
        self.left_padding = "  "
        self.confirming_new_game = False
        self.confirm_key = "y"
        self.menu_actions = {}

    def confirm_new_game(self, wm):
        self.confirming_new_game = True
        print(f"{self.left_padding}{wm.translator.t('are_you_sure_new_game')}")
        print(f"{self.left_padding}{wm.translator.t('confirm_new_game', confirm_key=self.confirm_key.upper())}")

    def next_avaible_night(self, next_night_index):
        if next_night_index in NIGHTS:
            return next_night_index
        else:
            return self.next_avaible_night(next_night_index - 1)

    def start_new_game(self, wm, player_name):
        if self.confirming_new_game == True:
            current_night = 1
            self.update_json_value("config/save.json", "complated_night", 0)

            wm.switch_to("game", player_name, current_night)

    def render_window(self, wm):
        save = self.load_save_data("config/save.json")
        if not save or not save["player"]["name"]:
            return wm.switch_to("new_begining")

        next_night = save["complated_night"] + 1
        next_avaible_night = self.next_avaible_night(next_night)

        if self.is_first:
            clear()
            print(LOGO_PICTURE_DARK)
            print(f"{self.left_padding}{wm.translator.t('have_a_good_shift', name=save['player']['name'])}!")
            if save["record_night"]:
                print(f"{self.left_padding}{wm.translator.t('record_night')}: {save['record_night']}")
            print(" ")

            self.menu_actions = render_menu([
                (wm.translator.t("new_game"), None, lambda wm: self.confirm_new_game(wm)),
                (f"{wm.translator.t('night')} {next_avaible_night}", None, lambda wm: wm.switch_to("game", save["player"]["name"], next_avaible_night)),
                (wm.translator.t("change_language"), None, lambda wm: wm.switch_to("change_lanquage")),
                (wm.translator.t("logout"), "q", lambda wm: wm.exit()),
            ], self.left_padding)

            self.is_first = False

        while True:
            choice = input_field()

            if self.confirming_new_game:
                if choice.lower() == self.confirm_key:
                    self.start_new_game(wm, save["player"]["name"])
                    break
                else:
                    self.confirming_new_game = False
                    continue

            action = self.menu_actions.get(choice)
            if action:
                action(wm)
                break
            else:
                print(f"{self.left_padding}{wm.translator.t('wrong_selection')}")