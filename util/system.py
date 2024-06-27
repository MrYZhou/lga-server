import importlib
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from util.PPAFastAPI import PPAFastAPI
from util.scheduler import Scheduler


class Env:
    app: FastAPI
    serverPath: str
    AppName: str = "lga"

    def initRouter(app: FastAPI):
        # 解析规则:server模块下面的带controller字符的文件 (文件夹下特定文件)
        for path in Path(Env.serverPath).rglob("*.py"):  # 使用pathlib更方便地遍历文件
            if "controller" in path.name.lower():
                module_name = path.stem  # 不包含扩展名的文件名
                try:
                    # 动态导入模块
                    full_module_name = f"server.{path.parent.name}.{module_name}"
                    module = importlib.import_module(full_module_name)
                    # 添加路由
                    if hasattr(module, "router"):
                        app.include_router(module.router)
                except Exception as e:
                    print(f"导入模块失败: {full_module_name} : {e}")

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
        Env.getPath("resources")
        app.mount("/img", StaticFiles(directory="resources/img"))
        app.mount("/template", StaticFiles(directory="resources/template"))

    def initSchedule(app: FastAPI):
        Scheduler.init(app)

    def init() -> FastAPI:
        load_dotenv()

        # 是否为打包环境
        if os.getenv("MODE") == "production":
            app = FastAPI(docs_url=None, redoc_url=None)
        else:
            app = FastAPI()
        if getattr(sys, "frozen", False):
            Env.serverPath = os.path.join(sys._MEIPASS, "server")
        else:
            Env.serverPath = os.path.join(os.getcwd(), "server")
        Env.initDataBase(app)
        Env.initSchedule(app)
        Env.initHttp(app)
        Env.initRouter(app)
        Env.initStaticDir(app)
        Env.app = app
        return app

    def getPath(*path):
        path = os.path.join(os.path.expanduser("~"), Env.AppName, *path)
        if not os.path.exists(path):
            os.makedirs(
                os.path.dirname(path) if os.path.isfile(path) else path, exist_ok=False
            )
        return path
