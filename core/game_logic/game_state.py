import threading, time, json
from core.game_logic.animatronic import Animatronic

def debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

def load_json_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class GameState:
    def __init__(self, night_index=1):
        animatronic_templates = load_json_template("config/animatronics.json")
        night_templates = load_json_template("config/nights.json")

        self.night_config = night_templates[str(night_index)]
        self.time = {"hour_index": 0, "min": 0}
        self.time_tick = 0.5
        self.winning_hour_index = 6
        self.office_position_index = 11
        
        self.power = 100
        self.power_usage = {
            "items": 1,
            "spend": 0.1
        }
        self.power_usage_table = {
            "default": 0.1,
            "light": 0.1,
            "closed": 0.3,
            "camera": 0.1
        }

        self.game_status = {
            "is_going": True,
            "reason": None,
            "killed_by": None
        }
        self.camera = {
            "is_open": False,
            "position": 1
        }

        self.comment_time = 2
        self.comment = {
            "time": 0,
            "text": None 
        }
        self.doors_index = {
            8: "left",
            10: "right"
        }
        self.doors = {"left": False, "right": False}
        self.light = {"left": False, "right": False}

        self.animatronics = {}
        for name, base_data in animatronic_templates.items():
            if name not in self.night_config["animatronics"]:
                continue

            night_data = self.night_config["animatronics"][name]
            self.animatronics[name] = Animatronic(
                name=name,
                default_position_index=base_data["default_possition_index"],
                path_graph=base_data["path_graph"],
                attack_trigger=base_data["attack_trigger"],
                wait_delay_range=night_data["wait_delay_range"],
                attack_delay=night_data["attack_delay"]
            )
        
        self.lock = threading.Lock()

    def game_start(self):
        thread = threading.Thread(target=self._game_tick_loop, daemon=True)
        thread.start()

    def _game_tick_loop(self):
        while self.game_status["is_going"] and self.power > 0 and self.time["hour_index"] <= self.winning_hour_index:
            time.sleep(0.5)
            with self.lock:
                self.advance_time()
                self.consume_power()
                self.update_comment()
                self.update_animatronics()

    def advance_time(self):
        self.time["min"] += self.time_tick
        if self.time["min"] >= 60:
            self.time["min"] = self.time["min"] - 60
            self.time["hour_index"] += 1
        if self.time["hour_index"] >= self.winning_hour_index:
            self.game_status = {
                "is_going": False,
                "reason": "morning"
            }

    def consume_power(self):
        power_usage = self.power_usage_table["default"]
        items = 1

        if self.camera["is_open"]:
            power_usage += self.power_usage_table["camera"]
            items +=1
        if self.doors["left"]:
            power_usage += self.power_usage_table["closed"]
            items +=1
        if self.doors["right"]:
            power_usage += self.power_usage_table["closed"]
            items +=1
        if self.light["left"]:
            power_usage += self.power_usage_table["light"]
            items +=1
        if self.light["right"]:
            power_usage += self.power_usage_table["light"]
            items +=1

        self.power -= power_usage
        if self.power <= 0:
            self.power = 0
            self.power_usage = {
                "items": 0,
                "spend": 0
            }
            self.disable_all()
        else:
            self.power_usage = power_usage
            self.power_usage = {
                "items": items,
                "spend": power_usage
            }

    def update_comment(self):
        if self.comment["text"]:
            self.comment["time"] += 0.5
            if self.comment["time"] >= self.comment_time:
                self.comment = {
                    "time": 0,
                    "text": None
                }

    def add_comment(self, comment_text):
        self.comment = {
            "time": 0,
            "text": comment_text
        }

    def disable_all(self):
        self.camera['is_open'] = False
        self.doors = {"left": False, "right": False}
        self.light = {"left": False, "right": False}

    def update_animatronics(self):
        for anim in self.animatronics.values():
            anim.advance(self.office_position_index)

            #---ПЕРЕВІРИТИ-АТАКУ---
            if anim.is_attacking:
                side = self.doors_index[anim.attack_trigger["position"]]

                if not self.doors[side]:
                    self.game_status = {
                        "is_going": False,
                        "reason": "killed",
                        "killed_by": anim.name
                    }
                else:
                    anim.reset_position()

    def get_animatronics_at_doors(self):
        result = {"left": [], "right": []}
        for anim in self.animatronics.values():
            if anim.current_position_index in self.doors_index:
                door_side = self.doors_index[anim.current_position_index]
                result[door_side].append(anim.name)
        return result