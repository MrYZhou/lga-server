# 初始化数据库
from fastapi import APIRouter, Body
from util.response import AppResult
from util.exception import exception
from util.base import Common
from util.scheduler import Scheduler
from util.system import Env
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
    taskPath = Env.rootPath + "/tasks"
    with open(taskPath+'/larry.py', 'a+') as fout:
        taskName = 'task'+data.id
        fout.write(f'''def {taskName}():\n  {data.content}\n''')
    # 启用任务
    schedule.initTask('larry',taskName)
    return AppResult.success("添加成功")


@router.get("/delete")
@exception
async def delete_task(task_id: str):
    await TaskInfo.delete(task_id)
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
async def list_task(page=Body(TaskPage)):
    data = await TaskInfo.page(page)
    return AppResult.success(data)


@router.post("/get")
@exception
async def get_task(task_id: str):
    task = await TaskInfo.get(task_id)
    return AppResult.success(task)
