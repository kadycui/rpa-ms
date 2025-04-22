#!/bin/bash

# filepath: /home/ubuntu/code/pycode/rpa-ms/deploy.sh

# 设置变量
ENV_NAME="fastapi_env"
PYTHON_VERSION="3.12"
REQUIREMENTS_FILE="requirements.txt"
APP_MODULE="main:app"  # 修改为你的 FastAPI 应用入口
HOST="0.0.0.0"
PORT="5000"
PID_FILE="uvicorn.pid"

# 检查是否安装了 Conda
if ! command -v conda &> /dev/null
then
    echo "Conda 未安装，请先安装 Miniconda 或 Anaconda。"
    exit 1
fi

# 函数：启动服务
start() {
    echo "启动 FastAPI 服务..."
    if [ -f "$PID_FILE" ]; then
        echo "服务已在运行，PID: $(cat $PID_FILE)"
        exit 1
    fi

    # 激活环境
    conda activate "$ENV_NAME"

    # 启动服务并保存 PID
    nohup uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --reload > logs/uvicorn.log 2>&1 &
    echo $! > "$PID_FILE"
    echo "服务已启动，PID: $(cat $PID_FILE)"
}

# 函数：停止服务
stop() {
    echo "停止 FastAPI 服务..."
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            kill -9 "$PID" && echo "服务已停止，PID: $PID"
        else
            echo "服务未运行，但 PID 文件存在，清理 PID 文件。"
        fi
        rm -f "$PID_FILE"
    else
        echo "服务未运行，检查端口占用情况..."
    fi

    # 检查并关闭占用的端口
    PORT_PID=$(lsof -t -i:"$PORT")
    if [ -n "$PORT_PID" ]; then
        echo "端口 $PORT 被进程 $PORT_PID 占用，正在关闭..."
        kill -9 "$PORT_PID"
        echo "端口 $PORT 已释放。"
    else
        echo "端口 $PORT 未被占用。"
    fi
}

# 函数：重启服务
restart() {
    echo "重启 FastAPI 服务..."
    stop
    start
}

# 函数：检查服务状态
status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "服务正在运行，PID: $PID"
        else
            echo "服务未运行，但 PID 文件存在。"
        fi
    else
        echo "服务未运行。"
    fi
}

# 检查命令参数
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac