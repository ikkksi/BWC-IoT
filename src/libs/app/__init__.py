import json
import asyncio

import tornado
import tornado.websocket


import libs.config as config
from libs.loger import aloger
from libs.app.const import Out
from libs.app.http_app import HttpApp
from libs.app.interface import IWebsocketApp,IDocs
import websockets
import random
class WebsocketApp(IWebsocketApp):
    WK = {
        "sender": "server",
        "type": "notice",
        "content": "wrong-key",
        "time": "2024-8-5-17-17",
    }
    RK = {
        "sender": "server",
        "type": "notice",
        "content": "right-key",
        "time": "2024-8-5-17-17",
    }

    ILLEGAL={
        "sender": "server",
        "type": "notice",
        "content": "illegal-data",
        "time": "2024-8-5-17-17",
    }

    def __init__(self,address :str,port :int):
        self.address = address
        self.port = port
        self.connected_users = set()


    async def _auth_bridge(self,websocket,path)->bool:
        """

        :param websocket:
        :param path:
        :return: 验证通过与否
        """
        headers = websocket.request_headers

        key = headers.get("X-Auth-Key")

        # 检查密钥是否有效
        if key != config.VALID_KEY:
            await websocket.send(json.dumps(self.WK))

            return False
        # 如果密钥有效，则处理连接
        await websocket.send(json.dumps(self.RK))
        return True

    async def _middleware(self,websocket,path):
        return True,websocket,path


    async def _handler(self ,websocket,path):
        aloger.info(f"{websocket.local_address} {Out.BUILDING_CONNECT.value}")
        result = await self._auth_bridge(websocket,path)
        if result == False:
            aloger.info(f"{websocket.local_address} {Out.FAILURE_FOR_WRONG_KEY.value}")
            return


        result,websocket,path = await self._middleware(websocket,path)
        if result == False:
            return

        self.connected_users.add(websocket)
        aloger.info(f"{websocket.local_address} {Out.SUCCESS.value}")
        try:
            async for message in websocket:
                aloger.info(message)
                data = json.loads(message)

                if data["type"] == "message":
                    await self._broadcast(message, websocket)
        except websockets.ConnectionClosed:
            aloger.error(Out.CONNECT_CLOSE.value)
        except KeyError:
            websocket.send(json.dumps(self.ILLEGAL))
            aloger.error(Out.ILLEGAL_DATA_PACK.value)

        finally:
            # 连接关闭时，从集合中移除用户
            self.connected_users.remove(websocket)

    async def _broadcast(self,message, sender):
        # 向所有其他连接的用户发送消息
        for user in self.connected_users:
            if user != sender:

                await user.send(message)

    async def run(self):
        aloger.info(f"{Out.SERVER_RUNNING.value} ws://{self.address}:{self.port}")
        async with websockets.serve(self._handler, self.address, self.port):
            await asyncio.Future()

    def get_serve(self):
        return websockets.serve(self._handler, self.address, self.port)




class WebSocketHandler(tornado.websocket.WebSocketHandler,IDocs):
    connected_users = set()

    user_device_name_map = dict()

    def check_origin(self, origin):
        """ 允许跨域 WebSocket 连接 """
        return True

    def open(self):
        """ 处理 WebSocket 连接 """
        aloger.debug(self.request.remote_ip)
        auth_key = self.request.headers.get("X-Auth-Key")
        device_name = self.request.headers.get("Device-Name")
        if device_name == None:

            device_name = f"未知设备{random.randint(0, 10000)}"


        if auth_key != config.VALID_KEY:
            self.write_message(json.dumps({
                "sender": "server",
                "type": "notice",
                "content": "wrong-key",
                "time": "2024-8-5-17-17",
            }))
            self.close()
            aloger.info(f"{self.request.remote_ip} {Out.FAILURE_FOR_WRONG_KEY.value}")
            return

        # 认证成功，添加到连接用户列表
        WebSocketHandler.connected_users.add(self)
        WebSocketHandler.user_device_name_map[device_name] = self

        self.write_message(json.dumps({
            "sender": "server",
            "type": "notice",
            "content": "right-key",
            "time": "2024-8-5-17-17",
        }))
        aloger.info(f"{self.request.remote_ip} {Out.SUCCESS.value}")

    def on_message(self, message):
        """ 处理客户端消息并广播 """
        aloger.info(f"{message}")
        try:
            data = json.loads(message)


            if data.get("type") == "message":
                self.broadcast(data['content'],sender=self,sender_name=data['sender'])
            else:
                self.write_message(json.dumps({
                    "sender": "server",
                    "type": "notice",
                    "content": "illegal-data",
                    "time": "2024-8-5-17-17",
                }))
        except json.JSONDecodeError:
            self.write_message(json.dumps({
                "sender": "server",
                "type": "notice",
                "content": "illegal-data",
                "time": "2024-8-5-17-17",
            }))
            aloger.error(Out.ILLEGAL_DATA_PACK.value)

    def on_close(self):
        """ 处理 WebSocket 断开 """
        WebSocketHandler.connected_users.discard(self)
        aloger.error(Out.CONNECT_CLOSE.value)

    @classmethod
    def broadcast(cls, message:str,sender:tornado.websocket.WebSocketHandler = None,sender_name:str = "server",type:str = "message"):
        """ 向所有 WebSocket 客户端广播消息 """
        for user in cls.connected_users:
            if user != sender:

                data = {'sender': f'{sender_name}', 'type': f'{type}', 'content':message, 'time': '2024-8-5-17-17'}
                user.write_message(json.dumps(data))

    @staticmethod
    def get_description() ->str:
        return "websocket路由"
