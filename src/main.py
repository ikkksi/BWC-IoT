import json
import os


import tornado


from libs.loger import aloger

from libs.app import WebSocketHandler, HttpApp,LogWebsocketHandler

aloger.patch(LogWebsocketHandler)

from libs import config
from libs.app.interface import HttpDocsCORS


import psutil

aloger.patch(LogWebsocketHandler)
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




@app.add_route('/get_cpu_info')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def get(self):
        cpu_percent = psutil.cpu_percent()  # 每1秒采样一次CPU使用率
        cpu_count = psutil.cpu_count(logical=False)  # 获取物理CPU核心数


        self.write({"percent": cpu_percent, "cpu_count":cpu_count})
    @classmethod
    def get_description(cls)->str:
        return "获取cpu占用情况"

@app.add_route('/get_memory_info')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def get(self):
        virtual_memory = psutil.virtual_memory()
        total_memory = virtual_memory.total  # 总内存
        used_memory = virtual_memory.used  # 已用内存
        memory_percent = virtual_memory.percent  # 内存使用率


        self.write({"percent": memory_percent, "used_memory":int(used_memory/(1024**3)),'total_memory': int(total_memory / (1024 ** 3))} )
    @classmethod
    def get_description(cls)->str:
        return "获取内存占用情况"

@app.add_route('/get_version_info')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def get(self):
        version = (1,0,0)
        version_str = f"{version[0]}.{version[1]}.{version[2]}"

        source_code_address = "https://github.com/ikkksi/BWC-IoT"


        self.write( {"version":version_str, "source_code_address":source_code_address} )
    @classmethod
    def get_description(cls)->str:
        return "获取版本信息"

@app.add_route('/bro')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def get(self):
        WebSocketHandler.broadcast("hello")
        self.write("广播成功")


    async def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            WebSocketHandler.broadcast(data)
            self.write({"result": "success","reason":None})
        except KeyError as e:
            self.write({"result":"failed","reason":"wrong json"})
    @classmethod
    def get_description(cls)->str:
        return "异步测试接口，广播测试接口"






@app.add_route('/index')
class HttpHandler(HttpDocsCORS):

    async def get(self):

        self.render("webui/html/index.html")
    @classmethod
    def get_description(cls)->str:
        return "主页路由"


@app.add_route('/webui/(.*)')
class StaticHandler(HttpDocsCORS):

    async def get(self,slue):
        path = os.path.join(os.getcwd(),f"webui/{slue}")

        _, ext = os.path.splitext(path)
        with open(path,'rb') as f:
            content = f.read()



        self.set_header("Content-Type", EXT_TO_MIME.get(ext.lower(),"application/octet-stream"))
        self.write(content)

    @classmethod
    def get_description(cls) -> str:
        return "静态资源"


@app.add_route('/get_online_list')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def get(self):
        onlines = [k for k,v in WebSocketHandler.user_device_name_map.items()]

        self.write({"list": onlines})
    @classmethod
    def get_description(cls)->str:
        return "获取在线设备"

@app.add_route('/kick')
class HttpHandler(HttpDocsCORS):
    """ HTTP 服务器端点 """
    async def post(self):
        name = ""
        try:
            data: dict = json.loads(self.request.body.decode('utf-8'))
            name = data.get("name")
            client: WebSocketHandler = WebSocketHandler.user_device_name_map.get(name)
            client.close()
            self.write({"result": f"踢出{name}成功"})
        except Exception as e:
            self.write({"result": f"踢出{name}失败"})
            aloger.error(e)
    @classmethod
    def get_description(cls)->str:
        return "异步测试接口，广播测试接口"







app.add_route('/', WebSocketHandler)
app.add_route("/ws/log",LogWebsocketHandler)

if __name__ == "__main__":


    app.run()
    aloger.info(f"WebSocket服务器正在运行 ws://localhost:{config.WS_PORT}")
    tornado.ioloop.IOLoop.current().start()
