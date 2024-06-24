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

支持.env文件配置（可选）
```bash
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=study
```

## docker部署

```bash
docker build -t fastweb .
docker run -d -p 8888:8888  fastweb
```

## 打成可执行文件
```bash
python  build.py
```
