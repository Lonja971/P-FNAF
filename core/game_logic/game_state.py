class GameState:
    def __init__(self):
        self.hour = 12
        self.power = 100
        self.is_alive = True
        self.camera_open = False
        self.doors = {"left": False, "right": False}
        self.animatronic_positions = {
            "freddy": "stage",
            "bonnie": "stage",
            "chica": "stage",
        }

    def advance_time(self):
        # просування часу в грі
        self.hour += 1
        if self.hour > 6:
            self.is_alive = False  # перемагаєш