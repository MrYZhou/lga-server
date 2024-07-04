import ast
from datetime import datetime
import importlib
import inspect
import os
from typing import Self
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from server.task.model.info import TaskInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI


class Scheduler:
    _instance: Self = None
    scheduler: AsyncIOScheduler = None

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
    def startTask(cls, file, updateTaskName, executeType, time):
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
            if executeType == "date":
                cls.scheduler.add_job(func=method, id=name, trigger=type, run_date=time)
            else:
                cls.scheduler.add_job(func=method, id=name, trigger=type, cron=time)

    @classmethod
    def init(cls, app: FastAPI, *args, **kwargs):
        if cls._instance is None:
            cls._instance = cls()
            cls.scheduler = AsyncIOScheduler()
            app.add_event_handler("startup", cls.startup)
            app.add_event_handler("shutdown", cls.shutdown)

    @classmethod
    async def startup(cls):
        # 时间触发器，判断时间是未来的
        tasks = await TaskInfo.getList()
        for task in tasks:
            type = task.get("type")
            taskId= task.get("id")
            content = task.get("content")
            method = cls.create_function_from_string(content)
            if "date" == type:
                execute_time: datetime = task.get("execute_time")
                current_time: datetime = datetime.now()
                if execute_time < current_time:
                    # TODO 把数据库的任务状态设置-1
                    continue
                cls.scheduler.add_job(
                   id=taskId, func=method, trigger=DateTrigger(run_date=execute_time), args=[], 
                )
            if "cron" == type:
                job_args =  cls.parse_cron_expression(task.get("cron"))
                cls.scheduler.add_job(
                    id=taskId, func=method, trigger=CronTrigger(**job_args), args=[]
                )
        cls.scheduler.start()
    @classmethod
    async def shutdown(cls):
        cls.scheduler.shutdown()

    def create_function_from_string(func_str):
        # 将字符串转换为AST，然后编译为可执行代码
        parsed_func = ast.parse(func_str, mode="exec")
        # 确保字符串中只有一个顶级定义（比如函数定义）
        if len(parsed_func.body) != 1 or not isinstance(
            parsed_func.body[0], ast.FunctionDef
        ):
            raise ValueError(
                "Function string must contain exactly one function definition."
            )

        # 动态定义函数
        func_def = parsed_func.body[0]
        func_name = func_def.name
        func_code = compile(parsed_func, "<string>", "exec")

        # 执行代码以定义函数
        namespace = {'datetime': datetime} 
        exec(func_code, namespace)

        # 返回定义的函数
        return namespace[func_name]
    @classmethod
    def parse_cron_expression(cls,expression):
        fields = expression.split()
        return {
            'second': fields[0],
            'minute': fields[1],
            'hour': fields[2],
            'day': fields[3],
            'month': fields[4],
            'day_of_week': fields[5]
        }