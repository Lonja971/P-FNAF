import random, time, json

def debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

def load_json_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class Animatronic:
    def __init__(self, name, default_position_index, path_graph, attack_trigger, wait_delay_range, attack_delay):
        self.map = load_json_template("config/location.json")
        self.name = name
        self.path_graph = path_graph
        self.current_position_index = default_position_index
        self.default_position_index = default_position_index

        self.time_in_position = 0
        self.is_attacking = False

        self.wait_delay_range = wait_delay_range
        self.current_wait_delay = random.uniform(*wait_delay_range)
        self.attack_delay = attack_delay

        self.attack_trigger = attack_trigger
    
    def set_new_wait_delay(self):
        self.current_wait_delay = random.uniform(*self.wait_delay_range)
    
    def reset_position(self):
        self.is_attacking = False
        self.current_position_index = self.default_position_index
        self.time_in_position = 0

    def advance(self, office_position_index):
        if self.time_in_position >= self.current_wait_delay:
            next_positions = self.path_graph[str(self.current_position_index)]
            if next_positions:
                self.current_position_index = random.choice(next_positions)
                debug_log(f"{self.name} перейшов у позицію {self.map[str(self.current_position_index)]["name"]}")
                if office_position_index == self.current_position_index:
                    self.is_attacking = True
                self.time_in_position = 0
                self.set_new_wait_delay()

        self.time_in_position += 0.5