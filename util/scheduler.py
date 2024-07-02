from datetime import datetime
import importlib
import inspect
import os
from typing import Self

from server.task.model.info import TaskInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI


class Scheduler:
    _instance:Self = None
    scheduler:AsyncIOScheduler = None

    @classmethod
    def getInstance(cls) -> Self:
        return cls._instance

    @classmethod
    def initAllTask(cls):
        """
        初始化所有任务
        """
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), "tasks")):
            for file in files:
                if file.find("__init__") > -1 or file.find(".pyc") > -1:
                    continue
                file = file.replace(".py", "")
                cls.initTask(file)

    @classmethod
    def initTask(cls, file, updateTaskName=None):
        """
        初始化指定任务
        file 代表是文件名
        updateTaskName 代表是任务名
        """
        m = importlib.import_module("tasks." + file)
        methods = inspect.getmembers(m, predicate=inspect.isfunction)
        for name, method in methods:
            ## 如果有指定任务
            if updateTaskName and updateTaskName != name:
                continue
            task = cls.scheduler.get_job(name)
            if task:
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
    async def startup(cls):
        if cls.scheduler.state == 0:
            cls.scheduler.start()

        # 从数据库获取任务添加
        # 时间触发器，判断时间是未来的
        tasks = await TaskInfo.getList()
        for task in tasks:
            type = task.get('type')
            if 'date' == type:
                time:datetime = task.get('execute_time')
                
                cls.scheduler.add_job()
                # cls.scheduler.add_job(func=method, id='name', trigger="date"
                #                       ,day=2,hour=11, minute=30)
            pass
       

    @classmethod
    async def shutdown(cls):
        cls.scheduler.shutdown()
