import threading, time
from core.game_logic.animatronic import Animatronic
from core.window.base import Window

from config.animatronics import ANIMATRONICS
from config.nights import NIGHTS

def debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

class GameState(Window):
    def __init__(self, night_index=1):
        self.night_index = night_index
        self.night_config = NIGHTS[night_index]
        self.default_activation_time  = {'hour_index': 0, "min": 0}

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
            "default": 0.03,
            "light": 0.03,
            "closed": 0.10,
            "camera": 0.023
        }

        self.is_pause = False
        self.game_status = {
            "is_going": True,
            "reason": None,
            "killed_by": None
        }
        self.current_camera = {
            "is_open": False,
            "number": 1
        }
        self.cameras = {
            1: {
                "position": 1,
            },
            2: {
                "position": 2,
            },
            3: {
                "position": 3,
            },
            4: {
                "position": 4,
            },
            5: {
                "position": 12,
            },
            6: {
                "position": 6,
            },
            7: {
                "position": 9,
            },
            8: {
                "position": 5,
            },
            9: {
                "position": 7,
            },
            10: {
                "position": 13
            },
            11: {
                "position": 14
            }
        }

        self.event_comment_time = 1.5
        self.event_comments = {}

        self.doors_index = {
            8: "left",
            10: "right"
        }
        self.doors = {"left": False, "right": False}
        self.light = {"left": False, "right": False}

        self.animatronics = {}
        for name, base_data in ANIMATRONICS.items():
            if name not in self.night_config["animatronics"]:
                continue

            night_data = self.night_config["animatronics"][name]
            self.animatronics[name] = Animatronic(
                name=name,
                default_position_index=base_data["default_position_index"],
                path_graph=base_data["path_graph"],
                attack_trigger=base_data["attack_trigger"],
                wait_delay_range=night_data["wait_delay_range"],
                attack_delay=night_data.get("attack_delay", None),
                activation_time=night_data.get("activation_time", self.default_activation_time),
                add_event_comment=self.add_event_comment,
                reduce_power=self.reduce_power
            )
        
        self.lock = threading.Lock()

    def game_start(self):
        debug_log(" ")
        debug_log(f" --- Night {self.night_index} ---")
        debug_log(" ")
        thread = threading.Thread(target=self._game_tick_loop, daemon=True)
        thread.start()

    def _game_tick_loop(self):
        while self.game_status["is_going"] and self.time["hour_index"] <= self.winning_hour_index:
            if self.is_pause:
                continue
            time.sleep(0.5)
            with self.lock:
                self.advance_time()
                self.consume_power()
                self.update_event_comments()
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
            save = self.load_config_templates("config/save.json")
            if not save["record_night"] or self.night_index > save["record_night"]:
                self.update_json_value("config/save.json", "record_night", self.night_index)
            self.update_json_value("config/save.json", "complated_night", self.night_index)

    def consume_power(self):
        power_usage = self.power_usage_table["default"]
        items = 1

        if self.current_camera["is_open"]:
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

    def update_event_comments(self):
        to_delete = []

        for name, comment in self.event_comments.items():
            comment["time"] += 0.5
            if comment["time"] >= self.event_comment_time:
                to_delete.append(name)

        for name in to_delete:
            del self.event_comments[name]

    def add_event_comment(self, name, comment_text, color=None):
        self.event_comments[name] = {
            "time": 0,
            "text": comment_text,
            "color": color
        }

    def disable_all(self):
        self.current_camera['is_open'] = False
        self.doors = {"left": False, "right": False}
        self.light = {"left": False, "right": False}

    def reset_camera_views(self):
        for camera in self.cameras.values():
            camera["view"] = []

    def update_cameras(self, name, current_position_index, camera_state=None):
        for camera_index, camera in self.cameras.items():
            if current_position_index == camera["position"]:
                camera.setdefault("view", []).append({
                    "name": name,
                    "state": camera_state or 0
                })

    def update_animatronics(self):
        self.reset_camera_views()

        for anim in self.animatronics.values():
            self.update_cameras(anim.name, anim.current_position_index, anim.camera_state)
            if (self.time["hour_index"] * 60 + self.time["min"]) < (anim.activation_time["hour_index"] * 60 + anim.activation_time["min"]):
                continue
            
            anim.advance(self.office_position_index, self.doors, self.doors_index, self.current_camera, self.cameras[self.current_camera["number"]])


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
                    if anim.self_reseat == False:
                        anim.reset_position(True)

    def get_animatronics_at_doors(self):
        result = {"left": [], "right": []}
        for anim in self.animatronics.values():
            if anim.current_position_index in self.doors_index:
                door_side = self.doors_index[anim.current_position_index]
                result[door_side].append(anim.name)
        return result
    
    def reduce_power(self, amount):
        self.power = max(0, self.power - amount)

    def door_handle(self, door):
        if self.power > 0:
            self.doors[door] = not self.doors[door]

    def light_handle(self, light_side):
        if self.power > 0:
            self.light[light_side] = not self.light[light_side]