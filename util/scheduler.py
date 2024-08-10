import ast
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from server.task.model.info import TaskInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI


class Scheduler:
    scheduler: AsyncIOScheduler = None
    second:int = 5

    @staticmethod
    def getInstance() -> AsyncIOScheduler:
        if Scheduler.scheduler is None:
            Scheduler.scheduler = AsyncIOScheduler()
        return Scheduler.scheduler

    @staticmethod
    def init(app: FastAPI, *args, **kwargs):
        app.add_event_handler("startup", Scheduler.startup)
        app.add_event_handler("shutdown", Scheduler.shutdown)
    def add(task):
        type = task.get("type")
        task_id = task.get("id")
        task_name = task.get("task_name")
        content = task.get("content")
        method =  Scheduler.create_function_from_string(content) 
        if "date" == type:
            execute_time: datetime = task.get("execute_time")
            current_time: datetime = datetime.now()
            if execute_time > current_time:
                Scheduler.scheduler.add_job(
                    id=task_id,
                    name=task_name,
                    func=method,
                    trigger=DateTrigger(run_date=execute_time),
                    replace_existing=True,
                    args=[],
                )
        elif "cron" == type:
            job_args = Scheduler.parse_cron_expression(task.get("cron"))
            Scheduler.scheduler.add_job(
                id=task_id,
                name=task_name,
                func=method,
                trigger=CronTrigger(**job_args),
                replace_existing=True,
                args=[],
            )
        elif "interval" == type:
            Scheduler.scheduler.add_job(
                id=task_id,
                name=task_name,
                func=method,
                trigger=IntervalTrigger(seconds=task.get("seconds")),
                replace_existing=True,
                args=[],
            )
    async def getTask():
         # 获取数据库任务
        tasks:list[TaskInfo] = await TaskInfo.where(status=0).getList()
        for task in tasks:
            Scheduler.add(task)
            task.status = 1
        await TaskInfo.update(tasks)    
    async def startup() -> None:
        scheduler = Scheduler.getInstance()
        scheduler.start()

        Scheduler.scheduler.add_job(
                id="-1",
                name="默认任务",
                func= Scheduler.getTask,
                trigger=IntervalTrigger(seconds=Scheduler.second)
            )

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
