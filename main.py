from util.response import AppResult
from util.system import Env

app = Env.init()


@app.get("/")
async def index():
    return AppResult.success("服务启动成功")


if __name__ == "__main__":
    Env.start()
