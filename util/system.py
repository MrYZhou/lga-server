import importlib
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from util.PPAFastAPI import PPAFastAPI
from util.scheduler import Scheduler


class Env:
    AppName = "lga"

    def initRouter(app: FastAPI):
        # 是否为打包环境
        if getattr(sys, "frozen", False):
            base_path = os.path.join(sys._MEIPASS, "router")
        else:
            base_path = os.path.join(os.getcwd(), "router")

        # 获取当前目录下所有非目录项（即文件）
        files_in_current_dir = [
            f
            for f in os.listdir(base_path)
            if os.path.isfile(os.path.join(base_path, f))
        ]

        # 解析规则:放在router文件夹下面的文件
        for file in files_in_current_dir:
            file = file.replace(".py", "")
            if file in ["__init__", ".pyc"]:
                continue
            m = importlib.import_module("router." + file)
            app.include_router(m.router)

    def initHttp(app: FastAPI):
        # 资源访问
        origins = [
            "http://localhost",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def initDataBase(app: FastAPI):
        PPAFastAPI.init(app)
        PPAFastAPI.showSql(True)

    def initStaticDir(app: FastAPI):
        path = Env.getPath("resources")
        app.mount("/static", StaticFiles(directory=path), name="static")

    def initSchedule(app: FastAPI):
        Scheduler.init(app)

    @staticmethod
    def init(app: FastAPI):
        Env.initDataBase(app)
        Env.initHttp(app)
        Env.initRouter(app)
        Env.initStaticDir(app)
        Env.initSchedule(app)

    def getPath(*path):
        path = os.path.join(os.path.expanduser("~"), Env.AppName, *path)
        if not os.path.exists(path):
            os.makedirs(
                os.path.dirname(path) if os.path.isfile(path) else path, exist_ok=False
            )
        return path
