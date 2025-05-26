from windows.main_window import MainWindow
from windows.game_window import GameWindow
from windows.new_begining_window import NewBeginingWindow

window_registry = {
    "main": MainWindow,
    "game": GameWindow,
    "new_begining": NewBeginingWindow
}