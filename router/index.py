# 初始化数据库
from fastapi import APIRouter, HTTPException
from util.response import AppResult

from util.scheduler import Scheduler


router = APIRouter(
    prefix="/task",
    tags=["任务"],
    responses={404: {"description": "Not found"}},
)


@router.get("/add")
async def add_task(task_name: str, type: str):
    try:
        # 任务存数据库
        # 生成脚本到task文件夹
        # 启用任务
        Scheduler.initTask()
        return AppResult.success("添加成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e.detail))


@router.get("/delete")
async def delete_task(job_id: str):
    try:
        # 删除任务
        Scheduler.scheduler.delete_job(job_id)
        return AppResult.success("删除任务成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
