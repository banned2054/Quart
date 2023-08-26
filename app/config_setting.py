import json


class Config:
    def __init__(self, config_file, setting_file):
        self.config_file = config_file
        self.setting_file = setting_file
        with open(setting_file, 'r') as f:
            self.setting_data = json.load(f)

    def get_config(self, key, default = None):
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
        return config_data.get(key, default)

    def get_setting(self, key, default = None):
        with open(self.setting_file, 'r') as f:
            setting_data = json.load(f)
        return setting_data.get(key, default)
