# 初始化数据库
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, HTTPException

from util.task import scheduler


class TaskInfo:
    @staticmethod
    def my_job2():
        print("Job executed2")


router = APIRouter(
    prefix="/task",
    tags=["任务"],
    responses={404: {"description": "Not found"}},
)


@router.get("/remove")
async def remove_task(job_id: str):
    try:
        # 删除任务
        scheduler.remove_job(job_id)
        return {"message": f" delete job successfully '"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/add")
async def add_task(task_name: str, type: str):
    try:
        trigger = IntervalTrigger(seconds=1)

        job_id = f"{task_name}_{type}"
        print(job_id)
        # 如果任务已经存在，抛出异常
        if job_id in [j.id for j in scheduler.get_jobs()]:
            raise HTTPException(status_code=400, detail="Task already exists")
        # 用反射得到一个新增的动态方法
        task_function = getattr(TaskInfo, "my_job2")
        # 动态添加任务到调度器
        scheduler.add_job(func=task_function, id=job_id, trigger=trigger)
        return {
            "message": f"Task '{task_name}' added successfully with trigger '{trigger}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e.detail))
