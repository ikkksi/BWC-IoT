

import tornado.web

from libs.app.interface import HttpDocsCORS



from libs.loger import aloger


class DocsHandler(HttpDocsCORS):

    route:list[tuple] = []

    async def get(self):
        view_route = [(t[0],t[1].get_description()) for t in self.route]
        self.write({"route_list":view_route})

    @classmethod
    def get_description(cls) ->str:
        return "获取各路由描述信息"

class HttpApp:
    def __init__(self,port:int):
        self.port = port
        self.routes = []




    def add_route(self,path:str,handler:HttpDocsCORS = None):
        def rg(handler:HttpDocsCORS):
            self.routes.append((path,handler))
            return handler

        if handler is None:
            return rg
        else:
            self.routes.append((path,handler))
    def run(self):


        DocsHandler.route = self.routes
        self.routes.append(("/get_docs",DocsHandler))
        app = tornado.web.Application(self.routes)

        app.listen(self.port)

        aloger.info(f"Tornado HTTP Server 已启动 http://127.0.0.1:{self.port}")
        for path,handler in self.routes:
            aloger.info(f"route:{path} | Description:{handler.get_description()}")






