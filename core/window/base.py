import json, os

class Window:
    def render(self):
        raise NotImplementedError

    def handle_input(self, window_manager):
        raise NotImplementedError
        
    def load_config_templates(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def load_save_data(self, path):
        if not os.path.exists(path):
            return None

        if os.path.getsize(path) == 0:
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError as e:
            return None
        
    def update_json_value(self, file_path, key_path, value):
        """
        Оновлює значення у JSON-файлі за шляхом key_path.
        Наприклад: key_path = "user.name" або ["user", "name"]
        """
        if isinstance(key_path, str):
            key_path = key_path.split(".")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не знайдено.")

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise ValueError(f"Файл {file_path} містить некоректний JSON.")

        d = data
        for key in key_path[:-1]:
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
            d = d[key]

        d[key_path[-1]] = value

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def overwrite_json(self, file_path, new_data):
        """
        Повністю перезаписує JSON-файл новими даними.
        
        :param file_path: Шлях до JSON-файлу.
        :param new_data: Об'єкт Python (dict або list), який буде записаний у файл.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)