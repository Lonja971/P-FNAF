import os, json, time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def debug_log(message):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_json_data(path):
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        return None

def ensure_json_file(save_path="config/save.json", template_path="config/save.template.json"):
    dir_path = os.path.dirname(save_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    try:
        with open(template_path, "r", encoding="utf-8") as template_file:
            template_data = json.load(template_file)
        with open(save_path, "w", encoding="utf-8") as save_file:
            json.dump(template_data, save_file, indent=4, ensure_ascii=False)
        return template_data

    except FileNotFoundError as e:
        print(f"[ERROR] Template file not found: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        return None