

import tornado
from libs.loger import aloger

from libs.app import WebSocketHandler, HttpApp,Out
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
app = HttpApp(port=config.WS_PORT)

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
@app.add_route('/test')
class HttpHandler(BroadcastHandler):
    """ HTTP 服务器端点 """
    def get(self):
        import random
        self.write(f"帅哥黄汉宏{random.randint(0, 9999)}")





@app.add_route('/bro')
class HttpHandler(BroadcastHandler):
    """ HTTP 服务器端点 """
    async def get(self):
        WebSocketHandler.broadcast("hello")
        self.write("广播成功")

app.add_route('/', WebSocketHandler)



if __name__ == "__main__":

    app.run()
    aloger.info(f"WebSocket服务器正在运行 ws://localhost:{config.WS_PORT}")
    tornado.ioloop.IOLoop.current().start()
