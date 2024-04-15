# nerf/nerf_environment.py
from nerf_triplane.provider import NeRFDataset_Test
from nerf_triplane.utils import *
from nerf_triplane.network import NeRFNetwork
from nerfreal import NeRFReal



class NeRFEnvironment:
    def __init__(self, config, default_settings):
        self.config = config
        self.default_settings = default_settings
        self.device = 'cuda'  # Assuming using CUDA by default
        self.model = None
        self.instance = None

    def initialize_model(self):
        # Merge default settings with config, with config taking precedence
        # merged_config = {**self.default_settings, **self.config}
        #
        # config = Config(**merged_config)

        config = Config(**self.default_settings)

        print(config)  # Print merged config
        # 根据配置初始化 NeRF 模型
        # Initialize the NeRF network and dataset based on the configuration
        device = torch.device(self.device if torch.cuda.is_available() else 'cpu')
        self.model = NeRFNetwork(config)

        # 创建损失函数和训练器
        criterion = torch.nn.MSELoss(reduction='none')
        metrics = []
        self.trainer = Trainer('ngp', config, self.model, device=device, workspace=config.workspace, criterion=criterion, fp16=config.fp16, metrics=metrics,
                               use_checkpoint=config.ckpt)

        # 准备数据加载器
        self.test_loader = NeRFDataset_Test(config, device=device).dataloader()
        self.model.aud_features = self.test_loader._data.auds
        self.model.eye_areas = self.test_loader._data.eye_area

        self.instance = NeRFReal(config, self.trainer, self.test_loader)
        return

    def process_command(self, command):
        # 处理从 WebSocket 接收到的命令
        
        print(f"Processing command: {command}")
        # 返回处理结果
        return f"Processed {command}"

    def render(self):
        # 执行数字人模型的渲染操作
        self.instance.render()

    def update(self, parameters):
        # Update model parameters or settings if required
        pass

    def release_resources(self):
        # 释放与此环境关联的资源
        print("Releasing resources of NeRF model.")
        # 实际中可能需要调用模型的清理方法
        pass


class Config:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        # Set defaults if not provided
        self.test = self.__dict__.get('test', True)
        self.test_train = self.__dict__.get('test_train', False)
        self.smooth_path = self.__dict__.get('smooth_path', True)
        self.smooth_lips = self.__dict__.get('smooth_lips', True)

        # Conditionally set values based on other config parameters
        self.check_conditions()

    def check_conditions(self):
        # Assertions and conditional adjustments
        # Must provide a pose source
        assert self.pose != '', 'Must provide a pose source'

        self.fp16 = True
        self.cuda_ray = True
        self.exp_eye = True
        self.smooth_eye = True

        if self.torso_imgs == '':
            self.torso = True

        self.asr = True

        if self.patch_size > 1:
            assert self.num_rays % (self.patch_size ** 2) == 0, "patch_size ** 2 should be dividable by num_rays."

        seed_everything(self.seed)



    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())})"

