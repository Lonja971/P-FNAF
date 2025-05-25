import curses

class GameLoop:
    def __init__(self, window):
        self.window = window

    def run(self):
        curses.wrapper(self.window._main)