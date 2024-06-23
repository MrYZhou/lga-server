from util.response import AppResult
from util.system import Env

app = Env.init()


@app.get("/")
async def index():
    return AppResult.success("lga server")
