class InputHandler:
    def __init__(self, state, running):
        self.state = state
        self.running = running

    def handle_key(self, key, current_view):
        updated_view = current_view
        should_render = False

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
        elif key == ord('q'):
            self.running = False

        return updated_view, should_render