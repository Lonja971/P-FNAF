class Window:
    def render(self):
        raise NotImplementedError

    def handle_input(self, window_manager):
        raise NotImplementedError