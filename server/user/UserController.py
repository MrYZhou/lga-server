# 初始化数据库
from fastapi import APIRouter
from util.response import AppResult
from util.exception import exception
from model.task import TaskInfo

router = APIRouter(
    prefix="/user",
    tags=["用户"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add")
@exception
async def add_user(data: TaskInfo):
    return AppResult.success("添加成功")
