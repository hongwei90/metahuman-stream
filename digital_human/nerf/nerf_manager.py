# nerf/nerf_manager.py

class NeRFManager:
    def __init__(self):
        # 使用字典来存储不同用户的 NeRF 实例
        self.instances = {}

    def get_instance_key(self, order_id, user_id):
        # 创建基于订单号和用户ID的唯一键
        return f"{order_id}-{user_id}"

    def get_instance(self, order_id, user_id):
        # 获取或创建NeRF实例
        key = self.get_instance_key(order_id, user_id)
        if key not in self.instances:
            self.instances[key] = self.create_instance(order_id, user_id)
        return self.instances[key]

    def create_instance(self, order_id, user_id):
        # 创建新的NeRF实例
        print(f"Creating NeRF instance for order: {order_id}, user: {user_id}")
        # 这里实现数字人实例的创建逻辑
        return NeRFInstance()

    def remove_instance(self, order_id, user_id):
        # 删除NeRF实例
        key = self.get_instance_key(order_id, user_id)
        if key in self.instances:
            print(f"Removing NeRF instance for order: {order_id}, user: {user_id}")
            del self.instances[key]
