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
    rootPath: str
    AppName: str = "lga"

    def initRouter(app: FastAPI):
        # 解析规则:server模块下面的带controller字符的文件 (文件夹下特定文件)
        for path in Path(Env.rootPath+ "/server").rglob("*.py"):  # 使用pathlib更方便地遍历文件
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
        Env.getPath(os.path.expanduser("~")+"/"+Env.AppName,"resources")
        Env.getPath(Env.rootPath,"tasks")
        app.mount("/img", StaticFiles(directory="resources/img"))
        app.mount("/template", StaticFiles(directory="resources/template"))

    def initSchedule(app: FastAPI):
        Scheduler.init(app)

    def init() -> FastAPI:
        # 加载.env文件属性到环境变量中
        load_dotenv()
        # 是否为打包环境
        if os.getenv("MODE") == "production":
            app = FastAPI(docs_url=None, redoc_url=None)
        else:
            app = FastAPI()
        if getattr(sys, "frozen", False):
            Env.rootPath = os.path.join(sys._MEIPASS)
        else:
            Env.rootPath = os.path.join(os.getcwd())
        # 文件生成
        Env.createFile(Env.rootPath,"tasks",'larry.py')
        # 其他初始化    
        Env.initDataBase(app)
        Env.initSchedule(app)
        Env.initHttp(app)
        Env.initRouter(app)
        Env.initStaticDir(app)
        Env.app = app
        return app

    def getPath(rootPath,*path):
        # 用户目录
        path = os.path.join(rootPath, *path)
        if not os.path.exists(path):
            os.makedirs(
                os.path.dirname(path) if os.path.isfile(path) else path, exist_ok=False
            )

    def createFile(*path):
        filePath = os.path.join( *path)
        if not os.path.exists(filePath):
            with open(filePath, 'w'):        
                pass