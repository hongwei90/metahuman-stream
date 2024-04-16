# nerf/nerf_environment.py
from nerf_triplane.provider import NeRFDataset_Test
from nerf_triplane.utils import *
from nerf_triplane.network import NeRFNetwork
from nerfreal import NeRFReal

import requests
from typing import Iterator

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
        txt_to_audio("hello!",self.instance)
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

def xtts(text, speaker, server_url) -> Iterator[bytes]:
        # 从speaker字典中提取character和emotion，如果没有提供，则使用默认值
        # character = speaker.get('character', '默认角色')
        # emotion = speaker.get('emotion', 'default')

        # 构建POST请求的body
        data = {
            "character": "eileen",
            "emotion": "default",
            "text": text,
            "stream": "true",
            # 根据需要添加其他参数
        }

        try:
            # 发送POST请求到声音克隆服务
            response = requests.post(server_url + '/tts', json=data)
            if response.status_code == 200:
                # 返回音频流
                for chunk in response.iter_content(chunk_size=1024):
                    yield chunk
            else:
                print(f"声音克隆服务调用失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"调用声音克隆服务出错: {e}")

def stream_xtts(audio_stream, render):
    for chunk in audio_stream:
        if chunk is not None:
            render.push_audio(chunk)

def txt_to_audio(text_, nerfreal):
    print("2222222222222222222222222222")
    audio_stream = xtts(
        text_,
        "",
        "http://localhost:5000"  # 假设你的本地声音克隆服务运行在这个地址
    )
    stream_xtts(audio_stream, nerfreal)

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

