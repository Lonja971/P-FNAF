from core.registry import window_registry

class WindowManager:
    def __init__(self, start_window_name, translator):
        self.window_stack = [window_registry[start_window_name]()]
        self.running = True
        self.translator = translator

    def push(self, name, *args, **kwargs):
        if not isinstance(self.window_stack[-1], window_registry[name]):
            self.window_stack.append(window_registry[name](*args, **kwargs))

    def switch_to(self, name, *args, **kwargs):
        self.window_stack = [window_registry[name](*args, **kwargs)]

    def pop(self):
        if len(self.window_stack) > 1:
            self.window_stack.pop()
        else:
            self.switch_to("main") 

    def exit(self):
        self.running = False

    def run(self):
        while self.running:
            self.window_stack[-1].render_window(self)