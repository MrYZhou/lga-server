import importlib
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from walrus import RateLimitException

from util.auth import AuthenticationMiddleware
from util.response import AppResult
from util.PPAFastAPI import PPAFastAPI
from util.scheduler import Scheduler


class Env:
    app: FastAPI
    # 项目当前位置
    rootPath: str
    # 应用名称
    AppName: str = "lga"
    home_dir: str
    log_path: str
    log_config: dict

    def initRouter(app: FastAPI):
        # 解析规则:router模块下面的带controller字符的文件 (文件夹下特定文件)
        for path in Path(Env.rootPath + "/router").rglob(
            "*.py"
        ):  # 使用pathlib更方便地遍历文件
            if "controller" in path.name.lower():
                module_name = path.stem  # 不包含扩展名的文件名
                try:
                    # 动态导入模块
                    full_module_name = f"router.{path.parent.name}.{module_name}"
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
        # 限流处理器
        @app.exception_handler(RateLimitException)
        async def handle(request: Request, exc: RateLimitException):
            msg = {"code": 400, "msg": f"太快了哟!,{request.client.host}"}
            return AppResult.fail(412, msg)

        @app.exception_handler(HTTPException)
        async def handle2(request: Request, exc: HTTPException):
            return AppResult.fail(exc.status_code, exc.detail)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 添加认证中间件
        if os.getenv('authCheck'):
            app.add_middleware(AuthenticationMiddleware)

    def initDataBase(app: FastAPI):
        PPAFastAPI.init(app)
        PPAFastAPI.showSql(True)

    def initStaticDir(app: FastAPI):

        Env.getPath(Env.rootPath, "tasks")
        app.mount("/img", StaticFiles(directory=Env.getPath(os.path.expanduser("~") + "/" + Env.AppName, "resources/img")))
        app.mount("/template", StaticFiles(directory=Env.getPath(os.path.expanduser("~") + "/" + Env.AppName, "resources/template")))

    def initSchedule(app: FastAPI):
        Scheduler.init(app)

    def init(self) -> FastAPI:
        Env.initEnv()
        # 是否为打包环境
        if os.getenv("MODE") == "production":
            app = FastAPI(docs_url=None, redoc_url=None)
        else:
            app = FastAPI()

        # 其他初始化
        Env.initDataBase(app)
        Env.initSchedule(app)
        Env.initHttp(app)
        Env.initRouter(app)
        Env.initStaticDir(app)
        Env.app = app
        return app

    @staticmethod
    def start():
        import uvicorn
        uvicorn.run(Env.app, host="0.0.0.0", reload=False, port=8888, workers=1)

    def getPath(rootPath, *path):
        # 用户目录
        path = os.path.join(rootPath, *path)
        if not os.path.exists(path):
            os.makedirs(
                os.path.dirname(path) if os.path.isfile(path) else path, exist_ok=False
            )
        return path

    def createFile(*path):
        filePath = os.path.join(*path)
        if not os.path.exists(filePath):
            with open(filePath, mode="w", encoding="utf-8") as file:
                file.write("")

    def getFilePath(*path):
        return os.path.join(Env.home_dir, *path)
    @staticmethod
    def initEnv():
        # 加载.env文件属性到环境变量中
        load_dotenv()
        if getattr(sys, "frozen", False):
            Env.rootPath = os.path.join(sys._MEIPASS)
        else:
            Env.rootPath = os.path.join(os.getcwd())
        # 文件生成
        Env.createFile(Env.rootPath, ".env")
        Env.home_dir = os.path.join(os.path.expanduser("~"), Env.AppName)
        Env.log_path = Env.getFilePath("logfile.log")
        print("资源目录:", Env.home_dir)
        print("日志文件:", Env.log_path)
        Env.getPath("resources")
        Env.log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
            },
            "handlers": {
                "file_handler": {
                    "class": "logging.FileHandler",
                    "filename": Env.log_path,
                    "formatter": "standard",
                },
                "console_handler": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "standard",
                },
            },
            "root": {
                "handlers": ["file_handler", "console_handler"],
                "level": "INFO",
            },
        }
