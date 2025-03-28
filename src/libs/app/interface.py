from typing import Tuple

import tornado
import websockets


class IWebsocketApp:
    WK: dict
    RK: dict
    ILLEGAL: dict

    def __init__(self, address: str, port: int) -> None: ...

    async def _auth_bridge(self, websocket: websockets.WebSocketServerProtocol, path: str) -> bool: ...

    async def _middleware(self, websocket: websockets.WebSocketServerProtocol, path: str) -> Tuple[bool, websockets.WebSocketServerProtocol, str]: ...

    async def _handler(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None: ...

    async def _broadcast(self, message: str, sender: websockets.WebSocketServerProtocol) -> None: ...

    async def run(self) -> None: ...

class BroadcastHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """ 允许跨域访问 """
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有域
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

    def options(self):
        """ 处理 preflight 预检请求 """
        self.set_status(204)  # No Content
        self.finish()

class IDocs:
    @staticmethod
    def get_description()->str:
        return "Default"

class HttpDocsCORS(BroadcastHandler,IDocs):
    pass