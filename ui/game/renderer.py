import curses, time
from ui.pictures.screamers import BONNIE_SCREAMER_DARK, CHICA_SCREAMER_DARK
from ui.pictures.logo import GAME_OVER_PICTURE_DARK, SIX_AM_PICTURE_DARK

from ui.pictures.office_pictures import OFFICE_CENTER
from ui.pictures.left_door import DOOR_LEFT_LIGHT, DOOR_LEFT, DOOR_LEFT_CLOSED, DOOR_LEFT_BONNIE
from ui.pictures.right_door import DOOR_RIGHT, DOOR_RIGHT_CLOSED, DOOR_RIGHT_LIGHT, DOOR_RIGHT_CHICA

class GameRenderer:
    def __init__(self, stdscr, state, current_night):
        self.stdscr = stdscr
        self.state = state
        self.hours = ["12", "01", "02", "03", "04", "05", "06"]
        self._init_colors()
        self.left_padding = 2
        self.current_night = current_night

    def _init_colors(self):
        curses.start_color()
        if curses.has_colors() and curses.COLORS >= 256:
            curses.use_default_colors()
        GRAY = 244
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(11, GRAY, -1)

    def render_all(self, current_view, door_animatronics, is_flickering):
        self.stdscr.clear()
        self.render_top()
        self.render_content(current_view,door_animatronics, is_flickering)
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
        self.stdscr.addstr(1, self.left_padding, f"Ніч: {self.current_night} | {hours}:{minutes}   Енергія: {power}% :{'[]' * power_usage["items"]}")
        self.stdscr.addstr(2, 0, "=" * 100)
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()

    def render_bottom(self):
        action_comment = self.state.action_comment
        event_comment = self.state.event_comment["text"] if self.state.event_comment["text"] else ""
        line_content = f"← A  |  → D  |  Q - Вихід    {action_comment.ljust(20) if action_comment else ' ' * 20}{event_comment}"

        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(33, 0, "=" * 100)
        self.stdscr.addstr(34, self.left_padding, line_content.ljust(100))
        self.stdscr.addstr(35, 0, "=" * 100)
        self.stdscr.attroff(curses.color_pair(2))
        self.stdscr.refresh()

    def render_content(self, current_view, door_animatronics, is_flickering=False):
        color_pair = 11 if is_flickering else 10
        self.stdscr.attron(curses.color_pair(color_pair))

        for i in range(3, 30):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        lines = []
        if current_view == "center":
            lines = self.get_office()
        elif current_view == "left":
            lines = self.get_left_door(door_animatronics)
        elif current_view == "right":
            lines = self.get_right_door(door_animatronics)

        for idx, line in enumerate(lines):
            self.stdscr.addstr(3 + idx, 0, line[:101])

        self.stdscr.attroff(curses.color_pair(color_pair))
        self.stdscr.refresh()

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
        reason = self.state.game_status.get("reason")
        end_picture = GAME_OVER_PICTURE_DARK

        if reason == "morning":
            end_picture = SIX_AM_PICTURE_DARK

        picture_lines = end_picture.split("\n")
        start_line = max(0, (30 - len(picture_lines)) // 2)

        for i, line in enumerate(picture_lines):
            if i + start_line < 30:
                self.stdscr.addstr(start_line + i, 10, line[:80])

        if reason == "morning":
            self.stdscr.addstr(32, 10, "Ви дожили до ранку!")
        elif reason == "killed":
            killed_by = self.state.game_status.get("killed_by", "невідомо")
            self.stdscr.addstr(31, 10, f"Пійманий {killed_by}...")
        else:
            self.stdscr.addstr(31, 10, "Причина невідома...kek")

        self.stdscr.addstr(34, 10, "Натисніть 'q', щоб вийти.", curses.A_BOLD)
        self.stdscr.refresh()

    def get_office(self):
        return OFFICE_CENTER

    def get_left_door(self, door_animatronics):
        door_picture = DOOR_LEFT
        action_comment = None

        if self.state.light["left"]:
            if door_animatronics["left"]:
                if self.state.doors["left"]:
                    action_comment = "Бонні в дверях..."
                door_picture = DOOR_LEFT_BONNIE
            else:
                action_comment = "Нікого немає..."
                door_picture = DOOR_LEFT_LIGHT
            
        if self.state.doors["left"]:
            door_picture = DOOR_LEFT_CLOSED

        self.state.add_action_comment(action_comment)
        return door_picture

    def get_right_door(self, door_animatronics):
        door_picture = DOOR_RIGHT
        action_comment = None

        if self.state.light["right"]:
            if door_animatronics['right']:
                if self.state.doors["right"]:
                    action_comment = "Чіка в дверях..."
                door_picture = DOOR_RIGHT_CHICA
            else:
                action_comment = "Нікого немає..."
                door_picture = DOOR_RIGHT_LIGHT
            
        if self.state.doors["right"]:
            door_picture = DOOR_RIGHT_CLOSED
        
        self.state.add_action_comment(action_comment)
        return door_picture