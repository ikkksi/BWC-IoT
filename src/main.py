from distutils.command.config import config

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

@app.add_route('/')
class HttpHandler(tornado.web.RequestHandler):
    """ HTTP 服务器端点 """
    def get(self):
        self.write("Hello, Tornado HTTP Server!")



@app.add_route('/bro')
class HttpHandler(tornado.web.RequestHandler):
    """ HTTP 服务器端点 """
    def get(self):
        WebSocketHandler.broadcast("hello")
        self.write("Hello, Tornado HTTP Server!")

app.add_route('/ws', WebSocketHandler)



if __name__ == "__main__":

    app.run()
    aloger.info(f"WebSocket服务器正在运行 ws://localhost:{config.WS_PORT}")
    tornado.ioloop.IOLoop.current().start()
