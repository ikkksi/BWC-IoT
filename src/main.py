import asyncio
import tornado.ioloop
from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.web

from libs.app import WebsocketApp, HttpApp
from libs import config

# 打印 Banner 信息
b = r"""
 ____     __      __  ____            ______          ______
/\  _`\  /\ \  __/\ \/\  _`\         /\__  _\        /\__  _\
\ \ \L\ \\ \ \/\ \ \ \ \ \/\_\       \/_/\ \/     ___\/_/\ \/
 \ \  _ <'\ \ \ \ \ \ \ \ \/_/_  _______\ \ \    / __`\ \ \ \
  \ \ \L\ \\ \ \_/ \_\ \ \ \L\ \/\______\\_\ \__/\ \L\ \ \ \ \
   \ \____/ \ `\___x___/\ \____/\/______//\_____\ \____/  \ \_\
    \/___/   '\/__//__/  \/___/          \/_____/\/___/    \/_/
"""
print(b)

# 实例化 WebSocket 与 HTTP 服务
ws_app = WebsocketApp(address=config.ADDRESS, port=config.WS_PORT)
http_app = HttpApp(8888, websocket_app=ws_app)

# 定义 HTTP 请求处理器及 CORS 设置
class CORSetting(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self):
        self.set_status(204)
        self.finish()

@http_app.add_route('/')
class HelloHandler(CORSetting):
    async def get(self):
        self.write('Hello, World!')

async def main():
    await asyncio.gather(
        ws_app.run(),
        asyncio.to_thread(http_app.run)
    )
if __name__ == "__main__":
    asyncio.run(main())
