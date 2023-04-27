# 初始化数据库
from sqlmodel import SQLModel

from db import engine
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from nanoid import generate
from sqlmodel import Session, SQLModel, select, update
from fastapi import Body

router = APIRouter(
    prefix="/task",
    tags=["任务"],
    responses={404: {"description": "Not found"}},
)


@router.get("/initDataBase")
async def method():
    SQLModel.metadata.create_all(engine)
    return 'success'


@router.get("/add")
async def method():
    return 'success'
