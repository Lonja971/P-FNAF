import time, curses, random

from core.window.base import Window
from core.game_logic.game_state import GameState

from ui.pictures.office_pictures import OFFICE_CENTER
from ui.pictures.left_door import DOOR_LEFT_LIGHT, DOOR_LEFT, DOOR_LEFT_CLOSED, DOOR_LEFT_BONNIE
from ui.pictures.right_door import DOOR_RIGHT, DOOR_RIGHT_CLOSED, DOOR_RIGHT_LIGHT, DOOR_RIGHT_CHICA
from ui.pictures.screamers import BONNIE_SCREAMER_DARK, CHICA_SCREAMER_DARK
from ui.pictures.logo import GAME_OVER_PICTURE_DARK

def debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

class GameWindow(Window):
    def __init__(self):
        self.state = GameState()
        self.door_animatronics = {"left": None, "right": None}
        self.current_view = "center"
        self.running = True
        self.hours = ["12", "1", "2", "3", "4", "5", "6"]

        self.next_flicker_in = random.randint(1, 20)
        self.flicker_duration = 0.2
        self.is_flickering = False
        self.flicker_timer = 0

    def render_window(self, wm):
        curses.wrapper(self._main)
        wm.pop()

    def _main(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        curses.start_color()
        if curses.has_colors() and curses.COLORS >= 256:
            curses.use_default_colors()
        self.stdscr.keypad(True)
        GRAY = 244
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(11, GRAY, -1)

        self.state.game_start()
        self.render_all()

        last_update = time.time()

        while self.running:
            key = self.stdscr.getch()
            if key != -1:
                if key == ord('a'):
                    self.current_view = (
                        "left" if self.current_view == "center" else
                        "center" if self.current_view == "right" else self.current_view
                    )
                    self.render_content()
                elif key == ord('d'):
                    self.current_view = (
                        "right" if self.current_view == "center" else
                        "center" if self.current_view == "left" else self.current_view
                    )
                    self.render_content()
                elif key == ord('l'):
                    if (self.state.power > 0):
                        if self.current_view == "left":
                            self.state.doors["left"] = not self.state.doors["left"]
                        elif self.current_view == "right":
                            self.state.doors["right"] = not self.state.doors["right"]
                        self.render_content()
                elif key == ord('k'):
                    if (self.state.power > 0):
                        if self.current_view == "left":
                            self.state.light["left"] = not self.state.light["left"]
                        elif self.current_view == "right":
                            self.state.light["right"] = not self.state.light["right"]
                        self.render_content()
                elif key == ord('q'):
                    self.running = False

            if time.time() - last_update >= 0.5:
                self.render_top()
                self.render_bottom()

                self.update_data()

                if not self.state.game_status["is_going"]:
                    if self.state.game_status["reason"] == "killed":
                        self.render_screamer(self.state.game_status["killed_by"])

                    self.render_game_over()
                    while True:
                        key = self.stdscr.getch()
                        if key == ord('q'):
                            self.running = False
                            break
                        time.sleep(0.1)
                    break

                last_update = time.time()

            time.sleep(0.05)

    def render_all(self):
        self.stdscr.clear()
        self.render_top()
        self.render_content()
        self.render_bottom()
        self.stdscr.refresh()

    def render_top(self):
        with self.state.lock:
            hours = self.hours[self.state.time["hour_index"]]
            int_minutes = int(self.state.time["min"])
            minutes = "0" + str(int_minutes) if len(str(int_minutes)) <= 1 else int_minutes
            power = int(self.state.power)
            power_usage = self.state.power_usage

        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(0, 0, "=" * 100)
        self.stdscr.addstr(1, 0, " " * 100)
        self.stdscr.addstr(1, 0, f"{hours}:{minutes}   Енергія: {power}% :{'[]' * power_usage["items"]}")
        self.stdscr.addstr(2, 0, "=" * 100)
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()

    def render_bottom(self):
        comment = self.state.comment["text"] if self.state.comment["text"] else ""
        line_content = f"← A  |  → D  |  Q - Вихід    {comment}"

        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(33, 0, "=" * 100)
        self.stdscr.addstr(34, 0, line_content.ljust(100))
        self.stdscr.addstr(35, 0, "=" * 100)
        self.stdscr.attroff(curses.color_pair(2))
        self.stdscr.refresh()

    def render_content(self):
        color_pair = 11 if self.is_flickering else 10
        self.stdscr.attron(curses.color_pair(color_pair))

        for i in range(3, 30):
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
            self.stdscr.addstr(3 + idx, 0, line[:101])

        self.stdscr.attroff(curses.color_pair(color_pair))
        self.stdscr.refresh()

    def get_office(self):
        return OFFICE_CENTER

    def get_left_door(self):
        if self.state.doors["left"]:
            return DOOR_LEFT_CLOSED
        if self.state.light["left"]:
            if self.door_animatronics['left']:
                return DOOR_LEFT_BONNIE
            else:
                self.state.add_comment("Нікого немає...")
                return DOOR_LEFT_LIGHT
        return DOOR_LEFT

    def get_right_door(self):
        if self.state.doors["right"]:
            return DOOR_RIGHT_CLOSED
        if self.state.light["right"]:
            if self.door_animatronics['right']:
                return DOOR_RIGHT_CHICA
            else:
                self.state.add_comment("Нікого немає...")
                return DOOR_RIGHT_LIGHT
        return DOOR_RIGHT
    
    def update_data(self):
        self.door_animatronics = self.state.get_animatronics_at_doors()
        self.update_flicker()

    def update_flicker(self):
        if self.is_flickering:
            self.flicker_timer += 0.5
            if self.flicker_timer >= self.flicker_duration:
                self.is_flickering = False
                self.flicker_timer = 0
                self.next_flicker_in = random.randint(1, 20)
                self.render_content()
        else:
            self.next_flicker_in -= 0.5
            if self.next_flicker_in <= 0:
                self.is_flickering = True
                self.render_content()
    
    def render_screamer(self, killer_name):
        self.stdscr.clear()

        if killer_name == "Bonnie":
            lines = BONNIE_SCREAMER_DARK
        elif killer_name == "Chica":
            lines = CHICA_SCREAMER_DARK
        else:
            lines = BONNIE_SCREAMER_DARK

        self.stdscr.attron(curses.color_pair(10))

        for i in range(3, 30):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        for idx, line in enumerate(lines):
            if 3 + idx >= 30:
                break
            self.stdscr.addstr(3 + idx, 0, line[:100])

        self.stdscr.attroff(curses.color_pair(10))
        self.stdscr.refresh()
        time.sleep(3)

    def render_game_over(self):
        self.stdscr.clear()

        picture_lines = GAME_OVER_PICTURE_DARK.split("\n")
        start_line = max(0, (30 - len(picture_lines)) // 2)

        for i, line in enumerate(picture_lines):
            if i + start_line < 30:
                self.stdscr.addstr(start_line + i, 10, line[:80])

        reason = self.state.game_status.get("reason")
        if reason == "morning":
            self.stdscr.addstr(31, 10, "6:00")
            self.stdscr.addstr(32, 10, "Ви дожили до ранку!")
        elif reason == "killed":
            killed_by = self.state.game_status.get("killed_by", "невідомо")
            self.stdscr.addstr(31, 10, f"Пійманий {killed_by}...")
        else:
            self.stdscr.addstr(31, 10, "Причина невідома...kek")

        self.stdscr.addstr(34, 10, "Натисніть 'q', щоб вийти.", curses.A_BOLD)
        self.stdscr.refresh()