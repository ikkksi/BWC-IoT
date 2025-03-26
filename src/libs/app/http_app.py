
import tornado.web
from tornado.ioloop import IOLoop



from libs.loger import aloger

from libs.app.interface import IWebsocketApp


class HttpApp:
    def __init__(self,port:int,websocket_app:IWebsocketApp):
        self.port = port
        self.routes = []
        self.websocket_app = websocket_app

    def add_route(self,path:str):
        def rg(handler:tornado.web.RequestHandler):
            self.routes.append((path,handler))
        return rg
    def run(self):

        app = tornado.web.Application(self.routes)

        app.listen(self.port)

        aloger.info(f"Tornado HTTP Server 已启动 http://127.0.0.1:{self.port}")





