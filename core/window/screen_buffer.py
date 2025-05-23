from utils.terminal import clear

class ScreenBuffer:
    def __init__(self):
        self.sections = {
            "top": "",
            "content": "",
            "bottom": ""
        }

    def update_section(self, name, content):
        if name in self.sections:
            self.sections[name] = content

    def render(self):
        clear()
        print(self.sections["top"])
        print(self.sections["content"])
        print(self.sections["bottom"])