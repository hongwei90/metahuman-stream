# nerf/nerf_environment.py
from nerf_triplane.provider import NeRFDataset_Test
from nerf_triplane.network import NeRFNetwork
from nerfreal import NeRFReal

class NeRFEnvironment:
    def __init__(self, config):
        self.config = config
        self.device = 'cuda'  # Assuming using CUDA by default
        self.model = self.initialize_model()

    def initialize_model(self):
        # 根据配置初始化 NeRF 模型
        # Initialize the NeRF network and dataset based on the configuration
        device = torch.device(self.device if torch.cuda.is_available() else 'cpu')
        self.model = NeRFNetwork(self.config)
        self.test_loader = NeRFDataset_Test(self.config, device=device).dataloader()
        self.model.aud_features = self.test_loader._data.auds
        self.model.eye_areas = self.test_loader._data.eye_area
        self.trainer = Trainer('ngp', self.config, self.model, device=device, workspace=self.config.workspace, use_checkpoint=self.config.ckpt)
        return NeRFReal(self.config, self.trainer, self.test_loader)

    def process_command(self, command):
        # 处理从 WebSocket 接收到的命令
        print(f"Processing command: {command}")
        # 返回处理结果
        return f"Processed {command}"

    def render(self):
        # 执行数字人模型的渲染操作
        self.model.render()

    def update(self, parameters):
        # Update model parameters or settings if required
        pass

    def release_resources(self):
        # 释放与此环境关联的资源
        print("Releasing resources of NeRF model.")
        # 实际中可能需要调用模型的清理方法
        pass
