import curses, time
from config.animatronics import ANIMATRONICS
from ui.sprites.logo import GAME_OVER_PICTURE_DARK, SIX_AM_PICTURE_DARK
from ui.sprites.office import PAUSE
from ui.sprites.office import OFFICE_CENTER
from ui.sprites.left_door import DOOR_LEFT, DOOR_LEFT_BONNIE, DoorLeftSprites
from ui.sprites.right_door import DOOR_RIGHT, DOOR_RIGHT_CHICA, DoorRightSprites
from core.translator import Translator
from core.window.base import Window

class GameRenderer(Window):
    def __init__(self, stdscr, state, current_night):
        self.stdscr = stdscr
        self.state = state
        self.hours = ["12", "01", "02", "03", "04", "05", "06"]
        self._init_colors()
        self.left_padding = 2
        self.current_night = current_night
        self.action_comment = None

        self.translator = Translator()
        self.door_left_sprites = DoorLeftSprites(self.translator)
        self.door_right_sprites = DoorRightSprites(self.translator)

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
        self.stdscr.addstr(1, self.left_padding, f"{self.translator.t("night")}: {self.current_night} | {hours}:{minutes}   {self.translator.t("energy")}: {power}% :{'[]' * power_usage["items"]}")
        self.stdscr.addstr(2, 0, "=" * 100)
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()

    def render_bottom(self):
        action_comment = self.action_comment
        event_comment = self.state.event_comment["text"] if self.state.event_comment["text"] else ""
        line_content = f"← A  |  → D  |  Q - {self.translator.t("exit")}    {action_comment.ljust(20) if action_comment else ' ' * 20}{event_comment}"

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
        if self.state.is_pause == True:
            lines = PAUSE
        elif current_view == "center":
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

        lines = ANIMATRONICS[killer_name]["screamer_sprite"]

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
        anim_info = {
            "Freddy": "freddy_info",
            "Chica": "chica_info",
            "Bonnie": "bonnie_info"
        }
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
            self.stdscr.addstr(32, 10, self.translator.t("survived_until_the_morning"))
        elif reason == "killed":
            killed_by = self.state.game_status.get("killed_by", "unknown")
            info_lines = self.translator.t(anim_info[killed_by], anim_name=killed_by).split("\n")
            start_y = 33
            start_x = 10

            self.stdscr.addstr(31, 10, self.translator.t("caught", killed_by=killed_by))
            for i, line in enumerate(info_lines):
                self.stdscr.addstr(start_y + i, start_x, line, curses.A_BOLD)
        else:
            self.stdscr.addstr(31, 10, self.translator.t("the_reason_is_unknown"))

        self.stdscr.addstr(36, 10, self.translator.t("press_q_to_exit"), curses.A_BOLD)
        self.stdscr.refresh()

    def get_office(self):
        return OFFICE_CENTER

    def get_left_door(self, door_animatronics):
        door_picture = DOOR_LEFT
        action_comment = None

        if self.state.light["left"]:
            if door_animatronics["left"]:
                if self.state.doors["left"]:
                    action_comment = self.translator.t("bonnie_in_the_door")
                door_picture = DOOR_LEFT_BONNIE
            else:
                action_comment = self.translator.t("no_one")
                door_picture = self.door_left_sprites.get_door_left_light_sprite()
            
        if self.state.doors["left"]:
            door_picture = self.door_left_sprites.get_door_left_closed_sprite()

        self.add_action_comment(action_comment)
        return door_picture

    def get_right_door(self, door_animatronics):
        door_picture = DOOR_RIGHT
        action_comment = None

        if self.state.light["right"]:
            if door_animatronics['right']:
                if self.state.doors["right"]:
                    action_comment = self.translator.t("chica_in_the_door")
                door_picture = DOOR_RIGHT_CHICA
            else:
                action_comment = self.translator.t("no_one")
                door_picture = self.door_right_sprites.get_door_right_light_sprite()
            
        if self.state.doors["right"]:
            door_picture = self.door_right_sprites.get_door_right_closed_sprite()
        
        self.add_action_comment(action_comment)
        return door_picture
    
    def add_action_comment(self, comment_text=None):
        self.action_comment = comment_text