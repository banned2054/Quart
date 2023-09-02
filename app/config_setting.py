import json


class Config:
    def __init__(self, config_file, setting_file):
        self.config_file = config_file
        self.setting_file = setting_file
        with open(setting_file, 'r') as f:
            self.setting_data = json.load(f)

    def get_config(self, key):
        """
        获取config文件的信息
        :param str key: 对应的key
        """
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
        return config_data.get(key)

    def get_setting(self, key):
        """
        获取setting文件的信息
        :param str key: 对应的key
        """
        with open(self.setting_file, 'r') as f:
            setting_data = json.load(f)
        return setting_data.get(key)

    def set_config(self, key, value):
        """
        修改config文件的信息
        :param str key: 要修改的key
        :param value: 要设置的新值
        """
        # 首先读取当前的配置数据
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)

        # 修改指定的键的值
        config_data[key] = value

        # 将修改后的数据写回到配置文件中
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent = 4)  # 使用indent参数使输出的JSON格式化，更易读
