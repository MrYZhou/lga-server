FROM python:3.13-slim

# 设置工作目录为/app
WORKDIR /app

# 将当前目录的内容复制到容器的/app目录下
COPY . /app

# pip换源,更新依赖
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
# 使用Poetry国内源和不创建虚拟环境
RUN pip install poetry 
RUN poetry config virtualenvs.create false && poetry config repositories.pypi https://mirrors.aliyun.com/pypi/simple
# 使用Poetry安装生产依赖项
RUN poetry install --only main

# 指定启动命令
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]

## 网络监听端口
EXPOSE 8888
