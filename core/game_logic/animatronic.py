import random, time
from config.location import LOCATION
from core.translator import Translator

def debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

class Animatronic:
    def __init__(self, name, default_position_index, path_graph, attack_trigger, wait_delay_range, attack_delay_range, activation_time, add_event_comment):
        self.name = name
        self.path_graph = path_graph
        self.activation_time = activation_time
        self.current_position_index = default_position_index
        self.default_position_index = default_position_index

        self.time_in_position = 0
        self.time_before_attack = 0
        self.is_attacking = False

        self.wait_delay_range = wait_delay_range
        self.current_wait_delay = random.uniform(*wait_delay_range)

        self.attack_delay_range = attack_delay_range
        self.current_attack_delay = random.choice(attack_delay_range)

        self.attack_trigger = attack_trigger
        self.add_event_comment = add_event_comment

        if attack_trigger["type"] == "laugh":
            self.laugh_number = 0

        self.translator = Translator()
    
    def set_new_wait_delay(self):
        self.current_wait_delay = random.uniform(*self.wait_delay_range)

    def set_new_attack_delay(self):
        self.current_attack_delay = random.choice(self.attack_delay_range)
    
    def reset_position(self, also_attacking=False):
        if also_attacking:
            self.is_attacking = False
        
        if self.attack_trigger["type"] == "laugh":
            self.laugh_number = 0

        self.current_position_index = self.default_position_index
        self.time_in_position = 0
        self.time_before_attack = 0
        self.set_new_attack_delay()
        self.set_new_wait_delay()

    def advance(self, office_position_index):
        if self.attack_trigger["type"] == "position" and self.attack_trigger["position"] == self.current_position_index:
            if self.time_before_attack >= self.current_attack_delay:
                self.current_position_index = office_position_index
                self.is_attacking = True
            
            self.time_before_attack += 0.5

        elif self.attack_trigger["type"] == "laugh" and self.laugh_number == self.attack_trigger["number"]:
            debug_log(f"1 {self.name} збирається атакувати {self.laugh_number}")
            debug_log(f"2 {self.name} збирається атакувати {self.time_before_attack} >= {self.current_attack_delay}")
            if self.time_before_attack >= self.current_attack_delay:
                self.current_position_index = office_position_index
                debug_log(f"{self.name} АТАКУЄ")
                self.is_attacking = True
            self.time_before_attack += 0.5

        elif self.time_in_position >= self.current_wait_delay:
            next_positions = self.path_graph[self.current_position_index]
            if next_positions:
                self.current_position_index = random.choice(next_positions)
                debug_log(f"{self.name} перейшов у позицію {LOCATION[self.current_position_index]["name"]}")

                if self.attack_trigger["type"] == "laugh":
                    self.laugh_number += 1
                    debug_log(f"{self.name} Сміється [{self.laugh_number}] {LOCATION[self.current_position_index]["name"]}")
                    self.add_event_comment(f"[{self.name}] {self.translator.t("ho_ho_ho")}")

                self.time_in_position = 0
                self.set_new_wait_delay()

        self.time_in_position += 0.5