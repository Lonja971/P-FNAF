class InputHandler:
    def __init__(self, state):
        self.state = state

    def handle_key(self, key, current_view):
        updated_view = current_view
        should_render = False

        if self.state.current_camera["is_open"] and key not in (
            [ord(' ')] + [ord(str(num)) for num in self.state.cameras]
        ):
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
        elif key == ord('l'):
            if current_view == "left":
                self.state.door_handle("left")
            elif current_view == "right":
                self.state.door_handle("right")
            should_render = True
        elif key == ord('k'):
            if current_view == "left":
                self.state.light_handle("left")
            elif current_view == "right":
                self.state.light_handle("right")
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

        return updated_view, should_render