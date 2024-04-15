# config/config_loader.py

import json
import os


class ConfigLoader:
    def __init__(self, config_directory, default_config=None):
        self.config_directory = config_directory
        self.default_config = default_config
        self.load_default_config()

    def load_default_config(self):
        # 加载默认配置（如果提供）
        if self.default_config:
            try:
                with open(self.default_config, 'r') as file:
                    self.default_settings = json.load(file)
                    print("Default configuration loaded successfully.")
            except FileNotFoundError:
                print(f"Default configuration file not found at {self.default_config}.")
                self.default_settings = {}
            except json.JSONDecodeError:
                print(f"Error decoding the default configuration file at {self.default_config}.")
                self.default_settings = {}

    def load_config(self, order_id):
        # 为给定的订单ID构建配置文件路径
        config_path = os.path.join(self.config_directory, f"{order_id}_config.json")

        # 尝试读取配置文件
        try:
            with open(config_path, 'r') as file:
                config_data = json.load(file)
                print(f"Configuration for order {order_id} loaded successfully.")
                return config_data
        except FileNotFoundError:
            print(f"No configuration file found for order {order_id}.")
            return self.default_settings  # 返回默认配置作为备选
        except json.JSONDecodeError:
            print(f"Error decoding the configuration file for order {order_id}.")
            return self.default_settings  # 返回默认配置作为备选
