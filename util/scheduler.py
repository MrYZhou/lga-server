import importlib
import inspect
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI


class Scheduler:
    _instance = None
    scheduler = None

    @classmethod
    def initAllTask(cls):
        """
        初始化所有任务
        """
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), "task")):
            for file in files:
                if file.find("__init__") > -1 or file.find(".pyc") > -1:
                    continue
                file = file.replace(".py", "")
                cls.initTask(file)

    @classmethod
    def initTask(cls, file, updateTaskName=None):
        """
        初始化指定任务
        """
        m = importlib.import_module("task." + file)
        methods = inspect.getmembers(m, predicate=inspect.isfunction)
        for name, method in methods:
            ## 如果有指定任务
            if updateTaskName and updateTaskName != name:
                continue
            job = cls.scheduler.get_job(name)
            if job:
                cls.scheduler.remove_job(name)
            cls.scheduler.add_job(func=method, id=name, trigger="interval", seconds=1)

    @classmethod
    def init(cls, app: FastAPI, *args, **kwargs):
        if cls._instance is None:
            cls._instance = cls()
            cls.scheduler = AsyncIOScheduler()
            app.add_event_handler("startup", cls.startup)
            app.add_event_handler("shutdown", cls.shutdown)

    @classmethod
    def startup(cls):
        if cls.scheduler.state == 0:
            cls.scheduler.start()
        # 从数据库获取任务添加
        # 时间触发器，判断时间是未来的
        # if 'date' == 1:
        #     target_time = datetime(2024, 6, 24, 9, 25, 50)
        #     scheduler.add_job(task, 'date', run_date=target_time)

        # cls.scheduler.add_job()

    @classmethod
    async def shutdown(cls):
        cls.scheduler.shutdown()
