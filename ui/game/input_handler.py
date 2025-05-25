class InputHandler:
    def __init__(self, state):
        self.state = state

    def handle_key(self, key, current_view, power):
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
        elif key == ord('l') and power > 0:
            if current_view == "left":
                self.state.doors["left"] = not self.state.doors["left"]
            elif current_view == "right":
                self.state.doors["right"] = not self.state.doors["right"]
            should_render = True
        elif key == ord('k') and power > 0:
            if current_view == "left":
                self.state.light["left"] = not self.state.light["left"]
            elif current_view == "right":
                self.state.light["right"] = not self.state.light["right"]
            should_render = True
        elif key == ord('q'):
            self.running = False

        return updated_view, should_render