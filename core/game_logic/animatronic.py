import random

class Animatronic:
    def __init__(self, name):
        self.name = name
        self.position = "stage"

    def move(self):
        moves = {
            "stage": "hallway",
            "hallway": "door",
        }
        if self.position in moves:
            self.position = moves[self.position]