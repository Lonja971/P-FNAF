import threading, time, random
from core.game_logic.animatronic import Animatronic

def debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

class GameState:
    def __init__(self):
        self.time = {"hour_index": 0, "min": 0}
        self.time_tick = 0.5
        self.winning_hour_index = 6
        
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
        self.is_alive = {
            "status": True,
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
        self.doors = {"left": False, "right": False}
        self.light = {"left": False, "right": False}

        self.animatronics = {
            "Bonnie": Animatronic("Bonnie", ["ShowStage", "DiningArea", "Backstage", "Hallway", "LeftDoor"]),
            "Chica": Animatronic("Chica", ["ShowStage", "DiningArea", "Restroom", "Kitchen", "RightDoor"])
        }
        
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
            debug_log(f"Updating time: {self.comment["time"]}")
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
            anim.time_in_position += 0.5

            # Рандомний рух через 2-5 секунд
            if anim.time_in_position >= random.uniform(2, 5):
                anim.advance()
                debug_log(f"{anim.name} moved to {anim.current_position}")

            # Якщо біля дверей
            if anim.is_at_door():
                side = "left" if anim.name == "Bonnie" else "right"
                if not self.doors[side]:
                    anim.at_door_since = anim.at_door_since or time.time()

                    # Якщо двері відкриті і чекає довше delay — атакує
                    if time.time() - anim.at_door_since >= anim.attack_delay:
                        self.game_status = {
                            "is_going": False,
                            "reason": "killed",
                            "killed_by": anim.name
                        }
                        self.is_alive = {"status": False, "killed_by": anim.name}
                        debug_log(f"{anim.name} напав!")
                else:
                    anim.at_door_since = None  # двері закриті — скидаємо таймер
            else:
                anim.at_door_since = None

    def get_animatronics_at_doors(self):
        result = {"left": None, "right": None}
        for anim in self.animatronics.values():
            if anim.is_at_door():
                side = "left" if anim.name == "Bonnie" else "right"
                result[side] = anim.name
        return result