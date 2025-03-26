
import tornado.web
from tornado.ioloop import IOLoop



from libs.loger import aloger




class HttpApp:
    def __init__(self,port:int):
        self.port = port
        self.routes = []


    def add_route(self,path:str,handler:tornado.web.RequestHandler = None):
        def rg(handler:tornado.web.RequestHandler):
            self.routes.append((path,handler))

        if handler is None:
            return rg
        else:
            self.routes.append((path,handler))
    def run(self):

        app = tornado.web.Application(self.routes)

        app.listen(self.port)

        aloger.info(f"Tornado HTTP Server 已启动 http://127.0.0.1:{self.port}")





