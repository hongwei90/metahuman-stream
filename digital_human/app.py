# app.py

from flask import Flask, request
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from authentication.jwt_auth import verify_jwt_token
from nerf.nerf_manager import NeRFManager
from websocket.connection_handler import ConnectionHandler

# 初始化 Flask 应用和 Flask-Sockets
app = Flask(__name__)
sockets = Sockets(app)

# 初始化数字人管理器
nerf_manager = NeRFManager()


# WebSocket 路由
@sockets.route('/human')
def human_socket(ws):
    # 从请求中获取token和order_id
    token = request.args.get('token')
    order_id = request.args.get('order_id')

    # 验证 JWT 令牌
    if not verify_jwt_token(token):
        ws.close()  # 如果验证失败，关闭 WebSocket 连接
        return

    # 实例化连接处理器并处理会话
    handler = ConnectionHandler(ws, nerf_manager)
    handler.handle_session(order_id, "honwee")


# 启动 WebSocket 服务器
if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8800), app, handler_class=WebSocketHandler)
    server.serve_forever()
