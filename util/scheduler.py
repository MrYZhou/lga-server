from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI


class Scheduler:
    _instance = None
    scheduler = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def init(cls, app: FastAPI, *args, **kwargs):
        if cls._instance is None:
            cls._instance = cls()
            cls.scheduler = AsyncIOScheduler()
            app.add_event_handler("startup", cls.startup)
            app.add_event_handler("shutdown", cls.shutdown)

    @classmethod
    def startup(cls):
        cls.scheduler.start()
        # 从数据库获取任务添加
        # cls.scheduler.add_job()

    @classmethod
    async def shutdown(cls):
        await cls.scheduler.shutdown()
