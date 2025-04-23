#!/bin/bash

set -e

# ========== 配置 ==========
VERSION="v1.1"
REGION="cn-guangzhou"
NAMESPACE="kadycui"
REPO_NAME="rpa_api"
IMAGE_NAME="$NAMESPACE/$REPO_NAME"
ACR_REGISTRY="registry.$REGION.aliyuncs.com"
FULL_IMAGE="$ACR_REGISTRY/$IMAGE_NAME"
CONTAINER_NAME="rpa-ms-container"

# ========== 环境变量配置 ==========
MYSQL_HOST="172.19.188.206"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DATABASE="fd_plateform"


# 登录 ACR
login_acr() {
    echo "🔐 正在登录阿里云 ACR..."
    docker login --username=kadycui@qq.com $ACR_REGISTRY
}

# 构建镜像
build_image() {
    echo "📦 构建镜像..."
    docker build -f build/Dockerfile -t $IMAGE_NAME:$VERSION .
    echo "🏷️ 打Tag: $FULL_IMAGE:$VERSION"
    docker tag $IMAGE_NAME:$VERSION $FULL_IMAGE:$VERSION
    docker tag $IMAGE_NAME:$VERSION $FULL_IMAGE:latest
}

# 推送镜像
push_image() {
    login_acr
    echo "⬆️ 推送镜像到 ACR..."
    docker push $FULL_IMAGE:$VERSION
    docker push $FULL_IMAGE:latest
}

# 运行容器
run_container() {
    echo "🚀 运行容器..."
    docker rm -f $CONTAINER_NAME 2>/dev/null || true
    docker run -d --name $CONTAINER_NAME \
        -p 5000:5000 \
        -v $(pwd)/logs:/app/logs \
        -e MYSQL_HOST="$MYSQL_HOST" \
        -e MYSQL_PORT="$MYSQL_PORT" \
        -e MYSQL_USER="$MYSQL_USER" \
        -e MYSQL_PASSWORD="$MYSQL_PASSWORD" \
        -e MYSQL_DATABASE="$MYSQL_DATABASE" \
        $IMAGE_NAME:$VERSION
    echo "✅ 容器运行中：$CONTAINER_NAME"
}

# 主流程
COMMAND=$1

case "$COMMAND" in
    login)
        login_acr
        ;;
    build)
        build_image
        ;;
    push)
        push_image
        ;;
    run)
        build_image
        push_image
        run_container
        ;;
    *)
        echo "❗ 用法: $0 {login|build|push|run}"
        exit 1
        ;;
esac
