import json
import os

class DataManager:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        os.makedirs(self.data_folder, exist_ok=True)

    def get_server_data(self, server_id):
        file_path = os.path.join(self.data_folder, f"{server_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return None
        else:
            return None

    def create_server_data(self, server_id, initial_data):
        file_path = os.path.join(self.data_folder, f"{server_id}.json")
        with open(file_path, "w") as file:
            json.dump(initial_data, file)

    def update_server_data(self, server_id, data):
        file_path = os.path.join(self.data_folder, f"{server_id}.json")
        with open(file_path, "w") as file:
            json.dump(data, file)