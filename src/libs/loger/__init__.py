import inspect
import datetime
import enum
import os

import libs.config


os.system("")


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
class Level(enum.Enum):
    NONE=0
    DEBUG=1
    INFO=2
    WARN=3
    ERROR=4
class IOut:
    @classmethod
    def write_out(cls, content):
        pass
class Loger(metaclass=SingletonMeta):
    def __init__(self,level):
        self.level=level
        self.Out:IOut = None



    def info(self,content:str):
        if self.Out is not None:
            self.Out.write_out(content)
        if self.level>=Level.INFO.value:
            filename,line,time=self._get_call_stack()
            print(f"[\033[40;36m{time}\033[0m] [\033[40;32mINFO\033[0m] \033[40;36;4m{filename}:{line}\033[0m | \033[40;32m{content}\033[0m")


    def warn(self,content:str):
        if self.Out is not None:
            self.Out.write_out(content)
        if self.level>=Level.WARN.value:
            filename,line,time=self._get_call_stack()
            print(f"[\033[40;36m{time}\033[0m] [\033[40;33mWARNING\033[0m] \033[40;36;4m{filename}:{line}\033[0m | \033[40;33m{content}\033[0m")

    def error(self,content:str):
        if self.Out is not None:
            self.Out.write_out(content)
        if self.level>=Level.ERROR.value:
            filename,line,time=self._get_call_stack()
            print(f"[\033[40;36m{time}\033[0m] [\033[40;31mERROR\033[0m] \033[40;36;4m{filename}:{line}\033[0m | \033[40;31m{content}\033[0m")

    def debug(self,content:str):
        if self.Out is not None:
            self.Out.write_out(content)
        if self.level>=Level.DEBUG.value:
            filename,line,time=self._get_call_stack()
            print(f"[\033[40;36m{time}\033[0m] [\033[40;37mDEBUG\033[0m] \033[40;36;4m{filename}:{line}\033[0m | \033[40;37m{content}\033[0m")

    def _get_call_stack(self):
        caller_frame = inspect.stack()[2]
        # 获取上一级调用者的帧
        filename = caller_frame.filename
        lineno = caller_frame.lineno
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return filename,lineno,current_time

    def patch(self,Out:IOut):
        self.Out = Out





aloger = Loger(level=libs.config.LOG_LEVEL)



