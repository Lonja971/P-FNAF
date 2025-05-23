import threading
import time
import curses

from core.window.base import Window
from core.game_logic.game_state import GameState

class GameWindow(Window):
    def __init__(self):
        self.state = GameState()
        self.current_view = "center"
        self.running = True
        self.energy_thread_started = False

    def render_window(self, wm):
        curses.wrapper(self._main, wm)
        wm.switch_to("main")

    def _main(self, stdscr, wm):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        curses.start_color()
        self.stdscr.keypad(True)
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        if not self.energy_thread_started:
            self.start_energy_drain()
            self.energy_thread_started = True

        self.render_all()

        while self.running:
            key = self.stdscr.getch()
            if key != -1:
                if key == ord('a'):
                    if self.current_view == "center":
                        self.current_view = "left"
                    elif self.current_view == "right":
                        self.current_view = "center"
                    self.render_content()

                elif key == ord('d'):
                    if self.current_view == "center":
                        self.current_view = "right"
                    elif self.current_view == "left":
                        self.current_view = "center"
                    self.render_content()

                elif key == ord('q'):
                    self.running = False

            time.sleep(0.05)

    def render_all(self):
        self.stdscr.clear()
        self.render_top()
        self.render_content()
        self.render_bottom()
        self.stdscr.refresh()

    def render_top(self):
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(0, 0, "=" * 40)
        self.stdscr.addstr(1, 0, " " * 40)
        self.stdscr.addstr(1, 0, f"Ніч: {self.state.hour}   Енергія: {self.state.power}%")
        self.stdscr.addstr(2, 0, "=" * 40)
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()

    def render_bottom(self):
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(18, 0, "=" * 40)
        self.stdscr.addstr(19, 0, "← A  |  → D  |  Q - Вихід")
        self.stdscr.addstr(20, 0, "=" * 40)
        self.stdscr.attroff(curses.color_pair(2))
        self.stdscr.refresh()

    def render_content(self):
        for i in range(3, 18):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        lines = []
        if self.current_view == "center":
            lines = self.get_office()
        elif self.current_view == "left":
            lines = self.get_left_door()
        elif self.current_view == "right":
            lines = self.get_right_door()

        for idx, line in enumerate(lines):
            self.stdscr.addstr(3 + idx, 5, line)

        self.stdscr.refresh()

    def get_office(self):
        return ["""
@%%#%%###%#%###@%%%%%%%%%%%%%%%%%%%%%%%@
@#*=+++==+=%%=#@######%%%%%%%%%%%%%%%%%%
@@@@@@%###%%@@@@###############%%%%%%%%%
@@###+=***++++=+####################%%%%
****++++***==+=-########################
****++*#*****+-*########################
#***#*++*+**+--###########    @%#*****#%
%####@-::::+==-%##########    @@. ..:=-@
@%*##%.------*-%#########%.:-=@@=+***#*@
.:%%#%:----=+*+%########+:...-@@......:*
 -%%%@###%%%#=-===%#####:....-@@..:::::*
.=%@@@+-=@@%@+----@#####-..::=@@::::::-#
-+%%-.:=*%%#@#====@#####+==++#@@---::--%
%%##+=-+#**+=++*####%#####*+==++%%%--#@@
%%%%%###%%%%@%%%%%%%%%%%%%%%%%%%%%%%%%%@
@%%%%%%%%%%%@%%%%%%%%%%%%%%%%%%%%%%%%%%%
@@@@@@@@@@@@@@==%@@==@@%==@@+=+@@++#@@++
%%%%%%%%%@@@@=@@*==@@==*@@+=%@@==@@#++@@
@@@@@%%@@@@@%####################%%%%%%%
@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%%@
******@@@@@@+++++*@@@@@#+++++%@@@@@*+++*
####%#*****+*****+++++++******-+++++*#**
---:+******------=******-------#******::
"""]

    def get_left_door(self):
        return [
            "[]   ← Ліва сторона",
            "",
            "...стіна... темрява..."
        ]

    def get_right_door(self):
        return [
            "Права сторона →   []",
            "",
            "...стіна... темрява..."
        ]

    def start_energy_drain(self):
        def drain():
            while self.state.power > 0:
                time.sleep(1)
                self.state.power -= 1
                self.render_top()

        thread = threading.Thread(target=drain, daemon=True)
        thread.start()