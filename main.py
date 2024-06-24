from util.response import AppResult
from util.system import Env

app = Env.init()


@app.get("/")
async def index():
    return AppResult.success("lga server")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", reload=True, port=8888, workers=1)
