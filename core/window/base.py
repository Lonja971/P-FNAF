import json

class Window:
    def render(self):
        raise NotImplementedError

    def handle_input(self, window_manager):
        raise NotImplementedError
    
    def get_config_path(config_name):
        with open("config.json", "r", encoding="utf-8") as f:
            config_json = json.load(f)
            if config_json["config_name"]:
                return config_json["config_name"]
            return False
        
    def load_config_templates(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)