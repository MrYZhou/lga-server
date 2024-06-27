# 初始化数据库
from fastapi import APIRouter
from util.response import AppResult
from util.exception import exception
from util.base import Common
from util.scheduler import Scheduler
from .model.info import TaskInfo
from .model.page import TaskPage

router = APIRouter(
    prefix="/task",
    tags=["任务"],
    responses={404: {"description": "Not found"}},
)

schedule = Scheduler.getInstance()
@router.post("/add")
@exception
async def add_task(data: TaskInfo):
    # 任务存数据库
    data.id = Common.uuid()
    await TaskInfo.post(data)
    # 生成脚本到task文件夹用户下文件
    # 启用任务
    # Scheduler.initTask()
    return AppResult.success("添加成功")


@router.get("/delete")
@exception
async def delete_task(task_id: str):
    TaskInfo.delete(task_id)
    schedule.delete_task(task_id)
    return AppResult.success("删除成功")


@router.post("/update")
@exception
async def update_task(data: TaskInfo):
    await TaskInfo.post(data)
    # 生成脚本到task文件夹
    # 启用任务
    # Scheduler.initTask()
    schedule.initTask()
    return AppResult.success("更新成功")


@router.post("/list")
@exception
async def list_task(data: TaskPage):
    return AppResult.success("")


@router.post("/get")
@exception
async def get_task(task_id: str):
    task = TaskInfo.get(task_id)
    return AppResult.success(task)
