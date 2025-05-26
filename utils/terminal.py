import os, json

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
