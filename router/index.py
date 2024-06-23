# 初始化数据库
from fastapi import APIRouter, HTTPException
from util.response import AppResult
from util.exception import exception
from util.base import Common
from util.scheduler import Scheduler
from model.task import TaskInfo

router = APIRouter(
    prefix="/task",
    tags=["任务"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add", description="创建新任务")
@exception
async def add_task(data: TaskInfo) -> AppResult:
    # 任务存数据库
    data.id = Common.randomkey()
    await TaskInfo.post(data)
    # 生成脚本到task文件夹
    # 启用任务
    # Scheduler.initTask()
    return AppResult.success("添加成功")


@router.get("/delete")
async def delete_task(job_id: str):
    try:
        # 删除任务
        Scheduler.scheduler.delete_job(job_id)
        return AppResult.success("删除任务成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
