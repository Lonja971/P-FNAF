import curses

class InputHandler:
    def __init__(self, state):
        self.state = state

    def handle_key(self, key, current_view):
        updated_view = current_view
        should_render = False

        allowed_keys = (
            [ord(' ')] + 
            [ord(str(num)) for num in self.state.cameras if num <= 9] +
            [curses.KEY_LEFT, curses.KEY_RIGHT, ord('k'), ord('l')]
        )

        if self.state.current_camera["is_open"] and key not in allowed_keys:
            return updated_view, should_render

        if key == ord('a'):
            updated_view = (
                "left" if current_view == "center" else
                "center" if current_view == "right" else current_view
            )
            should_render = True

        elif key == ord('d'):
            updated_view = (
                "right" if current_view == "center" else
                "center" if current_view == "left" else current_view
            )
            should_render = True

        elif key == ord('k'):
            if self.state.current_camera["is_open"]:
                self.change_camera_view_to_left()

            else:
                if current_view == "left":
                    self.state.light_handle("left")
                elif current_view == "right":
                    self.state.light_handle("right")

            should_render = True

        elif key == ord('l'):
            if self.state.current_camera["is_open"]:
                self.change_camera_view_to_right()

            else:
                if current_view == "left":
                    self.state.door_handle("left")
                elif current_view == "right":
                    self.state.door_handle("right")

            should_render = True

        elif key == ord(' '):
            if current_view == "center":
                self.state.current_camera["is_open"] = not self.state.current_camera["is_open"]
                should_render = True

        elif chr(key).isdigit():
            camera_number = int(chr(key))
            if camera_number in self.state.cameras:
                self.state.current_camera["number"] = camera_number
                should_render = True

        elif key == curses.KEY_LEFT:
            should_render = self.change_camera_view_to_left()

        elif key == curses.KEY_RIGHT:
            should_render = self.change_camera_view_to_right()

        return updated_view, should_render
    
    def change_camera_view_to_left(self):
        available = sorted(self.state.cameras.keys())
        current = self.state.current_camera["number"]
        idx = available.index(current)
        self.state.current_camera["number"] = (
            available[idx - 1] if idx > 0 else available[-1]
        )
        return True

    def change_camera_view_to_right(self):
        available = sorted(self.state.cameras.keys())
        current = self.state.current_camera["number"]
        idx = available.index(current)
        self.state.current_camera["number"] = (
            available[idx + 1] if idx < len(available) - 1 else available[0]
        )
        return True