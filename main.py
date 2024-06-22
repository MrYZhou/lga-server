from fastapi import FastAPI
from util.response import AppResult
from util.system import Env

app = FastAPI()
Env.init(app)


@app.get("/")
async def index():
    return AppResult.success("lga server")
