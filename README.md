# lga-server

任务调度服务

## 依赖安装

```bash
poetry update
```

## 根目录.envytemp 文件修改后改名为.env

```bash
#应用名称配置
lag-server
#数据库配置
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=study
# 是否开启token校验
AuthCheck = True
```

## 新建数据库 study,并执行放在根目录的 init.sql 脚本

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
docker run --env-file ./.env -d -p 8888:8888  fastweb
```

## 打成可执行文件

```bash
python  build.py
```
