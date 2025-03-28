import json
import os

import tornado
from libs.loger import aloger

from libs.app import WebSocketHandler, HttpApp
from libs import config
from libs.app.interface import HttpDocsCORS

EXT_TO_MIME = {
    ".js": "application/javascript",
    ".css": "text/css",
    ".html": "text/html",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".eot": "application/vnd.ms-fontobject",
    ".otf": "font/otf",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
}

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
app = HttpApp(port=config.WS_PORT)



@app.add_route('/test')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    def get(self):
        import random
        self.write(f"帅哥黄汉宏{random.randint(0, 9999)}")
    @staticmethod
    def get_description() ->str:
        return "同步测试接口"

@app.add_route('/test/like_game')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def post(self):
        try:
            # 异步读取 JSON 请求体
            data:dict = json.loads(self.request.body.decode('utf-8'))

            c = f"{ data.get('name') }啥也不是"

            if data["game"] == "无畏契约":

                c = f"""{data["name"]}是瓦学弟"""

            elif data["game"] == "csgo":

                c = f"""{data["name"]}是go学长"""

            self.write({"name":data["name"],"content":c})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"status": "error", "message": "Invalid JSON"})

    @staticmethod
    def get_description() ->str:
        return "异步post测试接口"



@app.add_route('/bro')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def get(self):
        WebSocketHandler.broadcast("hello")
        self.write("广播成功")
    @staticmethod
    def get_description()->str:
        return "异步测试接口，广播测试接口"

@app.add_route('/index')
class HttpHandler(HttpDocsCORS):

    async def get(self):

        self.render("webui/html/index.html")
    @staticmethod
    def get_description()->str:
        return "主页路由"


@app.add_route('/webui/(.*)')
class StaticHandler(HttpDocsCORS):

    async def get(self,slue):
        path = os.path.join(os.getcwd(),f"webui/{slue}")

        _, ext = os.path.splitext(path)
        with open(path,'rb') as f:
            content = f.read()


        aloger.debug(ext.lower())
        self.set_header("Content-Type", EXT_TO_MIME.get(ext.lower(),"application/octet-stream"))
        self.write(content)

    @staticmethod
    def get_description() -> str:
        return "静态资源"


@app.add_route('/get_online_list')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def get(self):
        onlines = [k for k,v in WebSocketHandler.user_device_name_map.items()]

        self.write({"list": onlines})
    @staticmethod
    def get_description()->str:
        return "获取在线设备"

app.add_route('/', WebSocketHandler)

if __name__ == "__main__":


    app.run()
    aloger.info(f"WebSocket服务器正在运行 ws://localhost:{config.WS_PORT}")
    tornado.ioloop.IOLoop.current().start()
