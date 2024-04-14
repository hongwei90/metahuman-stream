# websocket/connection_handler.py

import json


class ConnectionHandler:
    def __init__(self, ws, nerf_manager):
        self.ws = ws
        self.nerf_manager = nerf_manager
        self.is_connected = True

    def handle_session(self, order_id, user_id):
        # 获取对应订单的 NeRF 实例，创建直播流并发送给客户端
        try:
            nerf_instance = self.nerf_manager.get_instance(order_id, user_id)
        except Exception as e:
            print(f"Error getting NeRF instance: {e}")
            self.ws.send(json.dumps({'type': 'error', 'msg': 'Failed to get NeRF instance.'}))
            self.ws.close()
            return
        stream_url = f"https://127.0.0.1:8800/live/livestream_{order_id}_{user_id}.flv"
        self.ws.send(json.dumps({'type': 'stream_url', 'url': stream_url}))
        while self.is_connected:
            # 接收客户端的消息
            message = self.ws.receive()

            if message is None:
                self.is_connected = False
                break

            # 解析消息
            data = json.loads(message)

            # 根据消息类型进行处理
            if data['type'] == 'heartbeat':
                self.handle_heartbeat()
            elif data['type'] == 'command':
                self.handle_command(data, nerf_instance)
            else:
                print(f"Unknown message type: {data['type']}")

        # 如果连接断开，执行清理操作
        self.close_session(order_id)

    def handle_heartbeat(self):
        # 处理心跳消息
        print("Heartbeat received.")
        self.ws.send(json.dumps({"type": "heartbeat_ack"}))

    def handle_command(self, data, nerf_instance):
        # 处理来自客户端的指令
        print(f"Command received: {data['data']}")
        # 这里应该调用 nerf_instance 来处理指令并生成回应
        # 拼接nerf实例
        response = nerf_instance.process_command(data['data'])
        # 模拟回应的过程
        response = f"Processed command: {data['data']}"
        self.ws.send(json.dumps({"type": "command_response", "msg": response}))

    def close_session(self, order_id):
        pass

