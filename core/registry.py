from windows.main_window import MainWindow
from windows.game_window import GameWindow
from windows.new_begining_window import NewBeginingWindow
from windows.change_language_window import ChangeLanquageWindow

window_registry = {
    "main": MainWindow,
    "game": GameWindow,
    "new_begining": NewBeginingWindow,
    "change_lanquage": ChangeLanquageWindow,
}