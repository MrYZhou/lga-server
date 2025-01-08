import ast
from datetime import datetime,timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from router.task.model.info import TaskInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import os,importlib

class Scheduler:
    scheduler: AsyncIOScheduler = None
    second: int = 5

    @staticmethod
    def getInstance() -> AsyncIOScheduler:
        if Scheduler.scheduler is None:
            Scheduler.scheduler = AsyncIOScheduler()
        return Scheduler.scheduler

    @staticmethod
    def init(app: FastAPI, *args, **kwargs):
        app.add_event_handler("startup", Scheduler.startup)
        app.add_event_handler("shutdown", Scheduler.shutdown)
    def addTask(type,task_name,task_id,method,seconds,cron,execute_time: datetime=None):

        if "date" == type or "delay" == type:
            current_time: datetime = datetime.now()
            # 延迟任务
            if "delay" == type:
                delay = timedelta(seconds=20)
                execute_time = current_time + delay
            if execute_time > current_time:
                Scheduler.scheduler.add_job(
                    id=task_id,
                    name=task_name,
                    func=method,
                    trigger=DateTrigger(run_date=execute_time),
                    replace_existing=True,
                    args=[],
                )
        # cron表达式        
        elif "cron" == type:
            job_args = Scheduler.parse_cron_expression(cron)
            Scheduler.scheduler.add_job(
                id=task_id,
                name=task_name,
                func=method,
                trigger=CronTrigger(**job_args),
                replace_existing=True,
                args=[],
            )
        # 间隔    
        elif "interval" == type:
            Scheduler.scheduler.add_job(
                id=task_id,
                name=task_name,
                func=method,
                trigger=IntervalTrigger(seconds=seconds),
                replace_existing=True,
                args=[],
            )

    def add(task: TaskInfo):
        method = Scheduler.create_function_from_string(content)
        Scheduler.addTask(task.type,task.task_name,task.task_id,method,task.cron,task.execute_time)
    @staticmethod
    async def initTask():
        # 获取tasks文件夹下的任务
        base_path = os.path.join(os.getcwd(), "tasks")
        # 获取当前目录下所有非目录项（即文件）
        files_in_current_dir = [
            f
            for f in os.listdir(base_path)
            if os.path.isfile(os.path.join(base_path, f))
        ]

        for file in files_in_current_dir:
            file = file.replace(".py", "")
            if file in ["__init__", ".pyc"]:
                continue
            module = importlib.import_module("tasks." + file)

            if hasattr(module, "main"):
                # todo 后续从数据库读取配置信息
                Scheduler.addTask(type=module.type,
                task_name=module.task_name,
                task_id="tasks." + file,
                method=module.main,
                seconds=module.seconds if hasattr(module, "seconds") else None,
                cron=module.cron if hasattr(module, "cron") else None,
                execute_time=module.execute_time if hasattr(module, "execute_time") else None
                )
    @staticmethod
    async def getTask():
        # 获取数据库任务
        tasks: list[TaskInfo] = await TaskInfo.where(status=0).getList()
        if not tasks:
            return
        for task in tasks:
            Scheduler.add(task)
            task.status = 1
        await TaskInfo.update(tasks)

        
    @staticmethod
    async def startup() -> None:
        scheduler = Scheduler.getInstance()
        scheduler.start()

        await Scheduler.initTask()


    @staticmethod
    async def shutdown():
        Scheduler.scheduler.shutdown()

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
        namespace = {"datetime": datetime}
        exec(func_code, namespace)

        # 返回定义的函数
        return namespace[func_name]

    def parse_cron_expression(expression):
        expression = expression.replace("?", "*")
        fields = expression.split()
        return {
            "second": fields[0],
            "minute": fields[1],
            "hour": fields[2],
            "day": fields[3],
            "month": fields[4],
            "day_of_week": fields[5],
        }
