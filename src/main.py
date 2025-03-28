import json

import tornado
from libs.loger import aloger

from libs.app import WebSocketHandler, HttpApp
from libs import config
from libs.app.interface import HttpDocsCORS
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
app.add_route('/', WebSocketHandler)



if __name__ == "__main__":

    app.run()
    aloger.info(f"WebSocket服务器正在运行 ws://localhost:{config.WS_PORT}")
    tornado.ioloop.IOLoop.current().start()
