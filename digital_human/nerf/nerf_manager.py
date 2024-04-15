# nerf/nerf_manager.py

from digital_human.config import ConfigLoader
from digital_human.nerf.nerf_environment import NeRFEnvironment

from threading import Thread


class NeRFManager:
    def __init__(self):
        # 使用字典来存储不同用户的 NeRF 实例
        self.instances = {}
        self.config_loader = ConfigLoader(config_directory="/home/test/Code/honwee/metahuman-stream/digital_human/data/conf",
                                          default_config="/home/test/Code/honwee/metahuman-stream/digital_human/data/conf/default_config.json")

    def get_instance_key(self, order_id, user_id):
        # 创建基于订单号和用户ID的唯一键
        return f"{order_id}-{user_id}"

    def get_instance(self, order_id, user_id):
        # raise Exception("Not implemented")
        # 获取或创建NeRF实例
        key = self.get_instance_key(order_id, user_id)
        if key not in self.instances:
            self.instances[key] = self.create_instance(order_id, user_id)
            print(self.instances)
        return self.instances[key]

    def create_instance(self, order_id, user_id):
        # 创建新的NeRF实例
        print(f"Creating NeRF instance for order: {order_id}, user: {user_id}")
        # 这里实现数字人实例的创建逻辑
        try:
            config = self.config_loader.load_config(order_id)
            nerf_env = NeRFEnvironment(config,self.config_loader.default_settings)
            # 初始化模型并渲染
            nerf_env.initialize_model()

            rendthrd = Thread(target=nerf_env.render)
            rendthrd.start()
            return nerf_env.instance
        except Exception as e:
            print(f"Error creating NeRF instance: {e}")
            return f"Error creating NeRF instance: {e}"

    def remove_instance(self, order_id, user_id):
        # 删除NeRF实例
        key = self.get_instance_key(order_id, user_id)
        if key in self.instances:
            print(f"Removing NeRF instance for order: {order_id}, user: {user_id}")
            del self.instances[key]

    def get_or_create_instance(self, order_id, user_id, config):
        key = self.get_instance_key(order_id, user_id)
        if key not in self.instances:
            self.instances[key] = NeRFEnvironment(config)
        return self.instances[key]

    def release_instance(self, order_id, user_id):
        key = self.get_instance_key(order_id, user_id)
        if key in self.instances:
            self.instances[key].release_resources()
            del self.instances[key]
