# websocket/session.py

import json
from geventwebsocket import WebSocketError

class WebSocketSession:
    def __init__(self, websocket, nerf_instance):
        self.websocket = websocket
        self.nerf_instance = nerf_instance
        self.active = True

    def send_message(self, message):
        # 发送消息到客户端
        try:
            self.websocket.send(json.dumps(message))
        except WebSocketError as e:
            print(f"WebSocket error occurred: {e}")
            self.active = False

    def receive_message(self):
        # 接收客户端的消息
        try:
            message = self.websocket.receive()
            if message is None:
                self.active = False
            return message
        except WebSocketError as e:
            print(f"WebSocket error occurred: {e}")
            self.active = False
            return None

    def process_messages(self):
        # 循环处理所有接收到的消息
        while self.active:
            message = self.receive_message()
            if message:
                self.handle_message(json.loads(message))

    def handle_message(self, data):
        # 根据消息类型处理消息
        if data['type'] == 'command':
            response = self.nerf_instance.process_command(data['command'])
            self.send_message({'type': 'response', 'content': response})
        elif data['type'] == 'heartbeat':
            self.send_message({'type': 'heartbeat_ack'})

    def close(self):
        # 关闭 WebSocket 连接
        self.websocket.close()
        self.active = False
        print("Session closed.")
