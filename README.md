# lga-server

任务调度服务

## 依赖安装

```bash
poetry install
```

## config 目录下 .envytemp 文件修改后改名为.env

## 新建数据库 study,并执行放在 config 目录的 init.sql 脚本

## 启动服务(vscode)

```bash
f5
```

## 启动服务(idea)

```bash
点到main.py文件然后点运行按钮
```

## docker 部署

```bash
docker build -t fastweb .
或者
docker build -t base -f Dockerfile2-1 ./build/docker
docker build -t fastweb -f Dockerfile2-1 ./build/docker
```

## 运行

```bash
docker run --env-file ./.env -d -p 8888:8888  fastweb
```

## 打成可执行文件

```bash
python  build.py
```
