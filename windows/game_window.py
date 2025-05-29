import time, curses, random
from core.window.base import Window
from core.game_logic.game_state import GameState

from ui.game.renderer import GameRenderer
from ui.game.loop import GameLoop
from ui.game.input_handler import InputHandler

class GameWindow(Window):
    def __init__(self, current_night=1):
        self.state = GameState(current_night)
        self.current_night = current_night
        self.door_animatronics = {"left": None, "right": None}
        self.current_view = "center"
        self.running = True

        self.next_flicker_in = random.randint(1, 20)
        self.flicker_duration = 0.2
        self.is_flickering = False
        self.flicker_timer = 0
        self.confirming_exit = False

        self.input_handler = InputHandler(self.state)

    def render_window(self, wm):
        loop = GameLoop(self)
        loop.run()
        wm.pop()

    def _main(self, stdscr):
        self.stdscr = stdscr
        self.renderer = GameRenderer(self.stdscr, self.state, self.current_night)

        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)

        self.state.game_start()
        self.renderer.render_all(self.current_view, self.door_animatronics, self.is_flickering)

        last_update = time.time()

        while self.running:

            #---КЛІКИ---
            key = self.stdscr.getch()
            if key != -1:
                if not self.state.is_pause:
                    updated_view, should_render = self.input_handler.handle_key(key, self.current_view)
                    self.current_view = updated_view
                    if should_render:
                        self.renderer.render_content(self.current_view, self.door_animatronics, self.is_flickering)
                        self.renderer.render_bottom()

                if key == ord('q'):
                    if self.confirming_exit == False:
                        self.confirming_exit = True
                    else:
                        self.running = False
                elif key == ord('p'):
                    self.state.is_pause = not self.state.is_pause

            #---ОНОВЛЕННЯ---
            if not self.state.is_pause:
                if time.time() - last_update >= 0.5:
                    self.update_data()

                    if not self.state.game_status["is_going"]:
                        if self.state.game_status["reason"] == "killed":
                            self.renderer.render_screamer(self.state.game_status["killed_by"])

                        self.renderer.render_game_over()
                        while True:
                            key = self.stdscr.getch()
                            if key == ord('q') or key in [10, 13, curses.KEY_ENTER]:
                                self.running = False
                                break
                            time.sleep(0.1)
                        break

                    last_update = time.time()
                time.sleep(0.05)
            
            else:
                self.renderer.render_content(self.current_view, self.door_animatronics, self.is_flickering)
    
    def update_data(self):
        self.door_animatronics = self.state.get_animatronics_at_doors()
        self.update_flicker()
        self.state.action_comment = None

        self.renderer.render_top()
        self.renderer.render_content(self.current_view, self.door_animatronics, self.is_flickering)
        self.renderer.render_bottom()

    def update_flicker(self):
        if self.is_flickering:
            self.flicker_timer += 0.5
            if self.flicker_timer >= self.flicker_duration:
                self.is_flickering = False
                self.flicker_timer = 0
                self.next_flicker_in = random.randint(1, 20)
                self.renderer.render_content(self.current_view, self.door_animatronics, self.is_flickering)
        else:
            self.next_flicker_in -= 0.5
            if self.next_flicker_in <= 0:
                self.is_flickering = True
                self.renderer.render_content(self.current_view, self.door_animatronics, self.is_flickering)