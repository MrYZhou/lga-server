import uvicorn
from fastapi import FastAPI
from util.response import AppResult

from util.system import Env


app = FastAPI()
Env.init(app)


@app.get("/")
async def index():
    return AppResult.success("lga server")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
