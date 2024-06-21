import importlib
import os
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from walrus import RateLimitException

from fastapi.responses import JSONResponse

from util.PPAFastAPI import PPAFastAPI
from util.scheduler import Scheduler


class Env:
    AppName = "lga"

    # 路由注册
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

        # 解析规则:放在router模块下面的文件 (文件夹下文件)
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

        # 限流处理器
        @app.exception_handler(RateLimitException)
        async def handle(request: Request, exc: RateLimitException):
            msg = {"code": 400, "msg": f"太快了哟!,{request.client.host}"}
            return JSONResponse(status_code=412, content=msg)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def initDataBase(app):
        PPAFastAPI.init(app)
        PPAFastAPI.showSql(True)

    def initStaticDir(app):
        path = Env.getPath("resources")
        app.mount("/static", StaticFiles(directory=path), name="static")

    def initSchedule(app):
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
