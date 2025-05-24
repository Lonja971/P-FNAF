import random

class Animatronic:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.position_index = 0
        self.time_in_position = 0
        self.at_door_since = None
        self.attack_delay = 3

    @property
    def current_position(self):
        return self.path[self.position_index]

    def advance(self):
        if self.position_index < len(self.path) - 1:
            self.position_index += 1
            self.time_in_position = 0
        else:
            self.time_in_position += 0.5

    def is_at_door(self):
        return self.position_index == len(self.path) - 1