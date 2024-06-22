# lga-server

任务调度服务

## step:
1.依赖安装

```bash
poetry update
```

2.启动服务

```bash
f5
```

## docker运行

```bash
docker build -t fastweb .
docker run -d -p 8000:8000 -e  DB_HOST="192.168.1.4"  fastweb
```

